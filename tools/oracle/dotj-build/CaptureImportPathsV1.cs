using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.IO;
using System.Runtime.InteropServices;
using Microsoft.Build.Evaluation;
using Microsoft.Build.Framework;
using Microsoft.Build.Exceptions;

// Owned, development-only evaluation probe. No target, task, restore or Build API.
internal sealed class CaptureLogger : ILogger
{
    public LoggerVerbosity Verbosity { get; set; } = LoggerVerbosity.Diagnostic;
    public string? Parameters { get; set; }
    public List<object> Events { get; } = new();
    public void Initialize(IEventSource source)
    {
        source.WarningRaised += (_, e) => Events.Add(new { kind = "warning", code = e.Code,
            file = e.File, line = e.LineNumber, column = e.ColumnNumber, endLine = e.EndLineNumber, endColumn = e.EndColumnNumber, message = e.Message });
        source.ErrorRaised += (_, e) => Events.Add(new { kind = "error", code = e.Code,
            file = e.File, line = e.LineNumber, column = e.ColumnNumber, endLine = e.EndLineNumber, endColumn = e.EndColumnNumber, message = e.Message });
    }
    public void Shutdown() { }
}
internal static class CaptureImportPathsV1
{
    private static object[] Imports(IList<ResolvedImport> values) => values.Select(i => (object)new {
        owner = i.ImportingElement.ContainingProject.FullPath,
        project = i.ImportedProject.FullPath,
        line = i.ImportingElement.Location.Line,
        column = i.ImportingElement.Location.Column }).ToArray();
    private static void Main(string[] args)
    {
        var settings = ProjectLoadSettings.Default;
        using var manifest = JsonDocument.Parse(File.ReadAllBytes(args[1]));
        var rows = new List<object>();
        foreach (var item in manifest.RootElement.GetProperty("cases").EnumerateArray())
        {
            string id = item.GetProperty("id").GetString()!;
            string folder = Path.Combine(args[0], id);
            var globals = item.GetProperty("globals").EnumerateObject().ToDictionary(p => p.Name, p => p.Value.GetString()!, StringComparer.OrdinalIgnoreCase);
            var logger = new CaptureLogger();
            var collection = new ProjectCollection(new Dictionary<string,string>(), new ILogger[] { logger },
                Array.Empty<Microsoft.Build.Logging.ForwardingLoggerRecord>(), ToolsetDefinitionLocations.Local,
                1, false, false, false, false);
            object? evaluation = null;
            int before = collection.Count;
            int loaded = -1, after = -1;
            try
            {
                var project = new Project(Path.Combine(folder, "main.proj"), new Dictionary<string,string>(globals, StringComparer.OrdinalIgnoreCase), null, collection, settings);
                object? duplicateImports = null, duplicateGetterFailure = null;
                try { duplicateImports = Imports(project.ImportsIncludingDuplicates); }
                catch (InvalidOperationException e) { duplicateGetterFailure = new { type = e.GetType().FullName, message = e.Message }; }
                evaluation = new { success = true, properties = new { P = project.GetPropertyValue("P"), Q = project.GetPropertyValue("Q") },
                    imports = Imports(project.Imports), duplicateImports, duplicateGetterFailure };
            }
            catch (InvalidProjectFileException e)
            {
                evaluation = new { success = false, type = e.GetType().FullName, code = e.ErrorCode,
                    file = e.ProjectFile, line = e.LineNumber, column = e.ColumnNumber, endLine = e.EndLineNumber, endColumn = e.EndColumnNumber, message = e.Message, hresult = e.HResult };
            }
            finally
            {
                loaded = collection.Count;
                collection.UnloadAllProjects();
                after = collection.Count;
                collection.Dispose();
            }
            if (after != 0 || Directory.GetFiles(folder, "must-not-exist.txt", SearchOption.AllDirectories).Length != 0)
                throw new InvalidOperationException("Cleanup or task marker violation");
            rows.Add(new { id, globals, profile = settings.ToString(), evaluation,
                diagnostics = logger.Events, cleanup = new { before, loaded, afterUnload = after, disposed = true }, taskMarkerAbsent = true });
        }
        Console.WriteLine(JsonSerializer.Serialize(new { runtime = RuntimeInformation.FrameworkDescription,
            msbuildAssembly = typeof(Project).Assembly.FullName, msbuildPath = typeof(Project).Assembly.Location,
            frameworkPath = typeof(ILogger).Assembly.Location, corePath = typeof(string).Assembly.Location,
            profile = settings.ToString(), rows }, new JsonSerializerOptions { WriteIndented = true }));
    }
}
