using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.Json;
using Microsoft.Build.Evaluation;
using Microsoft.Build.Exceptions;
using Microsoft.Build.Framework;

// Owned evaluation-only observer. Every operation, including cleanup, has its own outcome.
internal static class CaptureLifecycleBehaviorV1
{
    private static readonly List<object> Actions = new();
    private static void Observe(string id, Func<object?> operation, bool cleanup = false)
    {
        try { Actions.Add(new { id, cleanup, success = true, value = operation() }); }
        catch (Exception e)
        {
            object? diagnostic = e is InvalidProjectFileException p ? new {
                code = p.ErrorCode, file = p.ProjectFile, line = p.LineNumber, column = p.ColumnNumber,
                endLine = p.EndLineNumber, endColumn = p.EndColumnNumber } : null;
            Actions.Add(new { id, cleanup, success = false, exception = new {
                type = e.GetType().FullName, hresult = e.HResult, message = e.Message, diagnostic } });
        }
    }
    private static Dictionary<string,string> Globals(string value) => new() { ["P"] = value };
    private static object Snapshot(IDictionary<string,string> values) =>
        values.OrderBy(p => p.Key, StringComparer.Ordinal).ToDictionary(p => p.Key, p => p.Value);
    private static void Main(string[] args)
    {
        string root = Path.GetFullPath(args[0]), id = args[1], file = Path.Combine(root,"valid.proj");
        ProjectCollection? c = null, other = null;
        Project? p = null, q = null, constructed = null;
        IDictionary<string,string>? snapshot = null;
        var caller = Globals("caller-original");
        try
        {
            switch (id)
            {
                case "LCB01":
                    Observe("collection", () => { c = new ProjectCollection(); return null; });
                    Observe("load1", () => { p = c!.LoadProject(file); return null; });
                    Observe("load2", () => { q = c!.LoadProject(file); return null; });
                    Observe("same", () => ReferenceEquals(p,q));
                    Observe("read", () => p!.GetPropertyValue("P"));
                    Observe("constructor", () => { constructed = new Project(file,null,null,c!); return null; });
                    break;
                case "LCB02":
                    Observe("collection", () => { c = new ProjectCollection(new Dictionary<string,string> {
                        ["P"] = "collection-default", ["Q"] = "collection-only" }); return null; });
                    Observe("callerBefore1", () => Snapshot(caller));
                    Observe("load1", () => { p = c!.LoadProject(file,caller,null); return null; });
                    Observe("callerAfter1", () => Snapshot(caller));
                    var equivalent = Globals("caller-original");
                    Observe("callerBefore2", () => Snapshot(equivalent));
                    Observe("loadEquivalent", () => { q = c!.LoadProject(file,equivalent,null); return null; });
                    Observe("callerAfter2", () => Snapshot(equivalent));
                    Observe("sameEquivalent", () => ReferenceEquals(p,q));
                    var different = Globals("caller-different");
                    Observe("callerBefore3", () => Snapshot(different));
                    Observe("loadDifferent", () => { q = c!.LoadProject(file,different,null); return null; });
                    Observe("callerAfter3", () => Snapshot(different));
                    Observe("sameDifferent", () => ReferenceEquals(p,q));
                    Observe("readFirst", () => p!.GetPropertyValue("P"));
                    Observe("readDifferent", () => q!.GetPropertyValue("P"));
                    Observe("readCollectionDefault", () => q!.GetPropertyValue("Q"));
                    break;
                case "LCB03":
                    Observe("collection", () => { c = new ProjectCollection(caller); return null; });
                    Observe("snapshot", () => { snapshot = c!.GlobalProperties; return Snapshot(snapshot); });
                    Observe("mutateCaller", () => { caller["P"] = "caller-mutated"; return null; });
                    Observe("snapshotAfterCallerMutation", () => Snapshot(snapshot!));
                    Observe("load", () => { p = c!.LoadProject(file); return null; });
                    Observe("read", () => p!.GetPropertyValue("P"));
                    Observe("mutateSnapshot", () => { snapshot!["P"] = "snapshot-mutated"; return null; });
                    Observe("snapshotAfterAttempt", () => Snapshot(snapshot!));
                    break;
                case "LCB04":
                    Observe("collection1", () => { c = new ProjectCollection(Globals("first")); return null; });
                    Observe("collection2", () => { other = new ProjectCollection(Globals("second")); return null; });
                    Observe("load1", () => { p = c!.LoadProject(file); return null; });
                    Observe("load2", () => { q = other!.LoadProject(file); return null; });
                    Observe("same", () => ReferenceEquals(p,q));
                    Observe("read1", () => p!.GetPropertyValue("P"));
                    Observe("read2", () => q!.GetPropertyValue("P"));
                    Observe("unload1", () => { c!.UnloadProject(p!); return null; });
                    Observe("readOther", () => q!.GetPropertyValue("P"));
                    break;
                case "LCB05":
                    Observe("collection", () => { c = new ProjectCollection(); return null; });
                    Observe("load", () => { p = c!.LoadProject(file); return null; });
                    Observe("unload", () => { c!.UnloadProject(p!); return null; });
                    Observe("readAfterUnload", () => p!.GetPropertyValue("P"));
                    Observe("secondUnload", () => { c!.UnloadProject(p!); return null; });
                    Observe("reload", () => { q = c!.LoadProject(file); return null; });
                    Observe("sameReload", () => ReferenceEquals(p,q));
                    Observe("readReload", () => q!.GetPropertyValue("P"));
                    break;
                case "LCB06":
                    Observe("collection", () => { c = new ProjectCollection(); return null; });
                    Observe("missing", () => { c!.LoadProject(Path.Combine(root,"missing.proj")); return null; });
                    Observe("malformed", () => { c!.LoadProject(Path.Combine(root,"malformed.proj")); return null; });
                    Observe("loadValid", () => { p = c!.LoadProject(file); return null; });
                    Observe("reloadValid", () => { q = c!.LoadProject(file); return null; });
                    Observe("sameRecovery", () => ReferenceEquals(p,q));
                    Observe("readRecovery", () => p!.GetPropertyValue("P"));
                    break;
                case "LCB07":
                    Observe("collection", () => { c = new ProjectCollection(); return null; });
                    Observe("load", () => { p = c!.LoadProject(file); return null; });
                    Observe("dispose1", () => { c!.Dispose(); return null; });
                    Observe("dispose2", () => { c!.Dispose(); return null; });
                    Observe("retainedRead", () => p!.GetPropertyValue("P"));
                    Observe("reload", () => { q = c!.LoadProject(file); return null; });
                    Observe("sameReload", () => ReferenceEquals(p,q));
                    Observe("unloadRetained", () => { c!.UnloadProject(p!); return null; });
                    break;
                case "LCB08":
                    Observe("implicitConstructor", () => { p = new Project(file); return null; });
                    Observe("globalCollection", () => { c = ProjectCollection.GlobalProjectCollection; return null; });
                    Observe("globalLoad", () => { q = c!.LoadProject(file); return null; });
                    Observe("sameGlobal", () => ReferenceEquals(p,q));
                    Observe("repeatConstructor", () => { constructed = new Project(file); return null; });
                    Observe("read", () => p!.GetPropertyValue("P"));
                    break;
                default: throw new ArgumentException("Unknown scenario");
            }
        }
        finally
        {
            void Unload(string name, ProjectCollection? owner, Project? project) =>
                Observe(name, () => { if (project != null) owner!.UnloadProject(project); return null; },true);
            void Dispose(string name, ProjectCollection? owner) =>
                Observe(name, () => { owner?.Dispose(); return null; },true);
            switch (id)
            {
                case "LCB01": Unload("unload1",c,p); Unload("unloadConstructor",c,constructed); Dispose("dispose",c); break;
                case "LCB02": Unload("unload1",c,p); Unload("unloadDifferent",c,q); Dispose("dispose",c); break;
                case "LCB03": Unload("unload",c,p); Dispose("dispose",c); break;
                case "LCB04": Unload("unload2",other,q); Dispose("dispose1",c); Dispose("dispose2",other); break;
                case "LCB05": Unload("unloadReload",c,q); Dispose("dispose",c); break;
                case "LCB06": Unload("unloadValid",c,p); Dispose("dispose",c); break;
                case "LCB07": Unload("unloadReload",c,q); Dispose("disposeFinally",c); break;
                case "LCB08":
                    Unload("unloadOwned",c,p);
                    Observe("unloadOtherOwned", () => {
                        if (q != null && !ReferenceEquals(p,q)) c!.UnloadProject(q);
                        if (constructed != null && !ReferenceEquals(p,constructed) && !ReferenceEquals(q,constructed)) c!.UnloadProject(constructed);
                        return null; },true);
                    break;
            }
        }
        Console.WriteLine(JsonSerializer.Serialize(new { schemaVersion = 1, id,
            runtime = RuntimeInformation.FrameworkDescription, msbuildPath = typeof(Project).Assembly.Location,
            frameworkPath = typeof(ILogger).Assembly.Location, corePath = typeof(string).Assembly.Location,
            actions = Actions },new JsonSerializerOptions { WriteIndented = true }));
    }
}
