using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Build.Evaluation;
using Microsoft.Build.Exceptions;
using Microsoft.Build.Framework;

// Owned development observer. Evaluates projects only; never schedules targets.
internal sealed class ItemLogger : ILogger
{
    public LoggerVerbosity Verbosity { get; set; } = LoggerVerbosity.Diagnostic;
    public string? Parameters { get; set; }
    public List<object> Events { get; } = new();
    public void Initialize(IEventSource source)
    {
        source.WarningRaised += (_, e) => Events.Add(new { kind = "warning", e.Code,
            e.File, e.LineNumber, e.ColumnNumber, e.Message });
        source.ErrorRaised += (_, e) => Events.Add(new { kind = "error", e.Code,
            e.File, e.LineNumber, e.ColumnNumber, e.Message });
    }
    public void Shutdown() { }
}

internal static class CaptureItemsV1
{
    private static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
    private static object Binary(string path) => new { path, sha256 = Hash(path), bytes = new FileInfo(path).Length };
    private static object AssemblyIdentity(Assembly a) => new { identity = a.FullName,
        mvid = a.ManifestModule.ModuleVersionId, file = Binary(a.Location) };
    private static readonly string[] BuiltIns = { "Identity", "FullPath", "RootDir", "Filename", "Extension",
        "RelativeDir", "Directory", "RecursiveDir", "DefiningProjectFullPath", "DefiningProjectDirectory",
        "DefiningProjectName", "DefiningProjectExtension" };

    private static object Evaluate(string projectPath, string toolsetPath,
        Dictionary<string,string> globals, string[] propertyNames, string[] metadataNames,
        string[]? builtInNames = null, bool mutationProbe = false)
    {
        var logger = new ItemLogger();
        using var collection = new ProjectCollection(new Dictionary<string,string>(), new ILogger[] { logger },
            Array.Empty<Microsoft.Build.Logging.ForwardingLoggerRecord>(), ToolsetDefinitionLocations.Local,
            1, false, false, false, false);
        var bootstrapToolsets = collection.Toolsets.Select(ToolsetSnapshot).ToArray();
        collection.RemoveAllToolsets();
        collection.AddToolset(new Toolset("Task128", toolsetPath, new Dictionary<string,string>(), collection, toolsetPath));
        object? result = null;
        int loaded = -1;
        try
        {
            var project = new Project(projectPath, globals, "Task128", collection, ProjectLoadSettings.Default);
            var before = Snapshot(project, propertyNames, metadataNames, builtInNames ?? BuiltIns);
            object? mutation = null;
            if (mutationProbe)
            {
                globals["P"] = "mutated";
                object collectionMutation;
                try { project.Items.Clear(); collectionMutation = new { returned = true }; }
                catch (Exception e) when (e is NotSupportedException || e is InvalidOperationException)
                { collectionMutation = new { returned = false, type = e.GetType().FullName, e.Message, e.HResult }; }
                mutation = new { caller = new Dictionary<string,string>(globals), collectionMutation,
                    after = Snapshot(project, propertyNames, metadataNames, builtInNames ?? BuiltIns) };
            }
            result = new { success = true, snapshot = before, mutation };
        }
        catch (InvalidProjectFileException e)
        {
            result = new { success = false, type = e.GetType().FullName, e.ErrorCode, e.ProjectFile,
                e.LineNumber, e.ColumnNumber, e.Message, e.HResult };
        }
        finally
        {
            loaded = collection.Count;
            collection.UnloadAllProjects();
        }
        return new { result, diagnostics = logger.Events, bootstrapToolsets,
            toolsets = collection.Toolsets.Select(ToolsetSnapshot).ToArray(),
            cleanup = new { loaded, after = collection.Count } };
    }

    private static object ToolsetSnapshot(Toolset t) => new { t.ToolsVersion, t.ToolsPath,
        properties = t.Properties.ToDictionary(p => p.Key, p => p.Value.EvaluatedValue) };

    private static object Snapshot(Project project, string[] properties, string[] metadata, string[] builtIns) => new {
        project.ToolsVersion,
        properties = properties.ToDictionary(n => n, project.GetPropertyValue),
        items = project.Items.Select(i => new { i.ItemType, i.EvaluatedInclude,
            metadata = metadata.ToDictionary(n => n, n => new { present = i.HasMetadata(n), value = i.GetMetadataValue(n) }),
            direct = i.DirectMetadata.Select(m => new { m.Name, m.EvaluatedValue }).ToArray(),
            effective = i.Metadata.Select(m => new { m.Name, m.EvaluatedValue }).ToArray(),
            builtIns = builtIns.ToDictionary(n => n, i.GetMetadataValue) }).ToArray(),
        byType = project.Items.Select(i => i.ItemType).Distinct(StringComparer.OrdinalIgnoreCase).ToDictionary(
            n => n, n => project.GetItems(n).Select(i => i.EvaluatedInclude).ToArray()),
        definitions = project.ItemDefinitions.ToDictionary(p => p.Key,
            p => new { metadata = p.Value.Metadata.Select(m => new { m.Name, m.EvaluatedValue }).ToArray(),
                queried = metadata.ToDictionary(n => n, p.Value.GetMetadataValue) }),
        imports = project.Imports.Select(i => new { owner = i.ImportingElement.ContainingProject.FullPath,
            path = i.ImportedProject.FullPath, line = i.ImportingElement.Location.Line }).ToArray()
    };

    private static string[] Strings(JsonElement element, string name) =>
        element.GetProperty(name).EnumerateArray().Select(v => v.GetString() ?? throw new InvalidDataException(name)).ToArray();

    private static string Child(string root, string relative)
    {
        string value = Path.GetFullPath(Path.Combine(root, relative));
        if (!value.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.Ordinal))
            throw new InvalidDataException("Fixture path outside scenario");
        return value;
    }

    private static object Corpus(string root, string manifestPath, string toolset)
    {
        using var manifest = JsonDocument.Parse(File.ReadAllBytes(manifestPath));
        var cases = manifest.RootElement.GetProperty("cases").EnumerateArray().ToArray();
        if (cases.Length != 42) throw new InvalidDataException("Expected adopted 42 scenarios");
        var rows = new List<object>();
        foreach (var c in cases)
        {
            string id = c.GetProperty("id").GetString() ?? throw new InvalidDataException("ID");
            Console.Error.WriteLine("DOTJ_ITEMS BEGIN " + id);
            string folder = Child(root, id);
            var globals = c.GetProperty("globals").EnumerateObject().ToDictionary(p => p.Name, p => p.Value.GetString() ?? "", StringComparer.OrdinalIgnoreCase);
            string[] properties = Strings(c, "queryProperties"), metadata = Strings(c, "queryMetadata"), builtIns = Strings(c, "queryBuiltIns");
            var observations = new List<object>();
            observations.Add(Evaluate(Child(folder,"main.proj"), toolset, globals, properties, metadata, builtIns, id == "IS02"));
            string firstSnapshot = JsonSerializer.Serialize(observations[0]);
            foreach (var step in c.GetProperty("steps").EnumerateArray())
            {
                string kind = step.GetProperty("kind").GetString() ?? "";
                switch (kind)
                {
                    case "filesystem-change":
                        foreach (var entry in step.GetProperty("write").EnumerateObject())
                            File.WriteAllText(Child(folder,entry.Name),entry.Value.GetString(),new UTF8Encoding(false));
                        foreach (var path in Strings(step,"delete")) File.Delete(Child(folder,path));
                        observations.Add(new { action = kind, completed = true });
                        break;
                    case "caller-global-mutation":
                        globals[step.GetProperty("name").GetString() ?? ""] = step.GetProperty("value").GetString() ?? "";
                        observations.Add(new { action = kind, caller = new Dictionary<string,string>(globals) });
                        break;
                    case "private-snapshot-mutation-attempt":
                        observations.Add(new { action = kind, disposition = "JAVA_PRIVATE_IMMUTABILITY_OBLIGATION_NOT_NATIVE_COLLECTION_EQUIVALENCE" });
                        break;
                    case "repeat-owner":
                    case "evaluate-xml":
                        string target = Child(folder, step.GetProperty("owner").GetString() ?? "");
                        if (kind == "evaluate-xml") File.WriteAllText(target,step.GetProperty("xml").GetString(),new UTF8Encoding(false));
                        else if (target != Child(folder,"main.proj")) File.Copy(Child(folder,"main.proj"),target,false);
                        var nextGlobals = step.TryGetProperty("globals",out var supplied)
                            ? supplied.EnumerateObject().ToDictionary(p => p.Name,p => p.Value.GetString() ?? "",StringComparer.OrdinalIgnoreCase)
                            : new Dictionary<string,string>(globals,StringComparer.OrdinalIgnoreCase);
                        observations.Add(Evaluate(target,toolset,nextGlobals,properties,metadata,builtIns));
                        break;
                    default: throw new InvalidDataException("Unknown declared step " + kind);
                }
            }
            if (File.Exists(Child(folder,"must-not-exist.txt"))) throw new InvalidOperationException("Task marker written");
            rows.Add(new { id, observations, retainedFirstSnapshotUnchanged = firstSnapshot == JsonSerializer.Serialize(observations[0]), taskMarkerAbsent = true });
            Console.Error.WriteLine("DOTJ_ITEMS END " + id);
        }
        return new { scenarioCount = rows.Count, rows,
            filesystem = Filesystem(Path.GetDirectoryName(root) ?? throw new InvalidDataException("No fixture parent")) };
    }

    private static object Filesystem(string root)
    {
        string probe = Path.Combine(root, "filesystem");
        Directory.CreateDirectory(probe);
        File.WriteAllText(Path.Combine(probe, "CaseProbe.txt"), "upper", Encoding.UTF8);
        bool alternateExistsBefore = File.Exists(Path.Combine(probe, "caseprobe.txt"));
        File.WriteAllText(Path.Combine(probe, "caseprobe.txt"), "lower", Encoding.UTF8);
        File.WriteAllText(Path.Combine(probe, "Upper.CS"), "upper-extension", Encoding.UTF8);
        File.WriteAllText(Path.Combine(probe, "lower.cs"), "lower-extension", Encoding.UTF8);
        File.WriteAllText(Path.Combine(probe, "plain"), "extensionless", Encoding.UTF8);
        object link;
        try
        {
            string alias = Path.Combine(probe, "owned-link.txt");
            File.CreateSymbolicLink(alias, "lower.cs");
            link = new { created = true, target = new FileInfo(alias).LinkTarget, attributes = File.GetAttributes(alias).ToString() };
        }
        catch (Exception e) when (e is IOException || e is UnauthorizedAccessException || e is PlatformNotSupportedException)
        { link = new { created = false, type = e.GetType().FullName, e.Message, e.HResult }; }
        return new { alternateExistsBefore,
            upperValueAfter = File.ReadAllText(Path.Combine(probe, "CaseProbe.txt")),
            lowerValueAfter = File.ReadAllText(Path.Combine(probe, "caseprobe.txt")),
            names = Directory.GetFileSystemEntries(probe).Select(Path.GetFileName).ToArray(),
            cs = Directory.GetFiles(probe, "*.cs").Select(Path.GetFileName).ToArray(),
            starDotStar = Directory.GetFiles(probe, "*.*").Select(Path.GetFileName).ToArray(), link,
            mountInfo = File.Exists("/proc/self/mountinfo") ? File.ReadAllText("/proc/self/mountinfo") : null };
    }

    private static object Preflight(string root, string toolset)
    {
        var filesystem = Filesystem(root);
        string empty = Path.Combine(root, "empty.proj"), glob = Path.Combine(root, "glob.proj");
        File.WriteAllText(empty, "<Project />", new UTF8Encoding(false));
        File.WriteAllText(glob, "<Project><ItemGroup><Compile Include=\"filesystem/*.cs\" /></ItemGroup></Project>", new UTF8Encoding(false));
        return new { filesystem,
            empty = Evaluate(empty, toolset, new(), Array.Empty<string>(), Array.Empty<string>()),
            glob = Evaluate(glob, toolset, new(), Array.Empty<string>(), Array.Empty<string>()) };
    }

    private static void Main(string[] args)
    {
        Console.OutputEncoding = new UTF8Encoding(false);
        Console.InputEncoding = new UTF8Encoding(false);
        CultureInfo.DefaultThreadCurrentCulture = CultureInfo.InvariantCulture;
        CultureInfo.DefaultThreadCurrentUICulture = CultureInfo.GetCultureInfo("en-US");
        object observations;
        if (args.Length == 3 && args[0] == "preflight")
            observations = Preflight(Path.GetFullPath(args[1]), Path.GetFullPath(args[2]));
        else if (args.Length == 4 && args[0] == "corpus")
            observations = Corpus(Path.GetFullPath(args[1]),Path.GetFullPath(args[2]),Path.GetFullPath(args[3]));
        else throw new ArgumentException("preflight ROOT TOOLSET or corpus ROOT MANIFEST TOOLSET");
        Console.WriteLine(JsonSerializer.Serialize(new { schemaVersion = 1, mode = args[0],
            os = RuntimeInformation.OSDescription, runtime = RuntimeInformation.FrameworkDescription,
            readyToRun = Environment.GetEnvironmentVariable("DOTNET_ReadyToRun"),
            osArchitecture = RuntimeInformation.OSArchitecture.ToString(), processArchitecture = RuntimeInformation.ProcessArchitecture.ToString(),
            host = Binary(Environment.ProcessPath ?? throw new InvalidOperationException("No host path")),
            core = AssemblyIdentity(typeof(string).Assembly), msbuild = AssemblyIdentity(typeof(Project).Assembly),
            framework = AssemblyIdentity(typeof(ILogger).Assembly), observations,
            loadedAssemblies = AppDomain.CurrentDomain.GetAssemblies().Where(a => !a.IsDynamic && a.Location.Length > 0)
                .OrderBy(a => a.FullName, StringComparer.Ordinal).Select(AssemblyIdentity).ToArray()
        }, new JsonSerializerOptions { WriteIndented = true }));
    }
}
