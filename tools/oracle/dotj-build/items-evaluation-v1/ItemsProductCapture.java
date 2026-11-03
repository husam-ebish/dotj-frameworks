package org.dotj.internal.build.evaluation;

import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import static org.dotj.internal.build.evaluation.ItemsJson.*;

/** Same-JAR observations of the frozen 42 scenarios, with genuine retained-result probes. */
public final class ItemsProductCapture {
    static String hash(Path path) throws Exception { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(path))); }
    static Path child(Path root,String relative) {
        Path value=root.resolve(relative).normalize();if(!value.startsWith(root)||value.equals(root))throw new IllegalArgumentException("Fixture escape");return value;
    }
    static Map<String,String> globals(Object value) {
        Map<String,String> result=new LinkedHashMap<>();map(value).forEach((k,v)->result.put(k,(String)v));return result;
    }
    static List<String> strings(Map<String,Object> row,String key) { return list(row.get(key)).stream().map(String.class::cast).toList(); }
    static List<Object> metadata(Collection<ItemSnapshot.Metadata> values) {
        return values.stream().map(m->(Object)object("Name",m.name(),"EvaluatedValue",m.value())).toList();
    }
    static Map<String,Object> snapshot(ProjectEvaluationComponent.Result result,Map<String,Object> row) {
        Map<String,Object> properties=new LinkedHashMap<>(),types=new LinkedHashMap<>(),definitions=new LinkedHashMap<>();
        for(String name:strings(row,"queryProperties"))properties.put(name,result.property(name));
        List<Object> items=new ArrayList<>();
        for(ItemSnapshot item:result.items()) {
            Map<String,Object> queried=new LinkedHashMap<>(),builtins=new LinkedHashMap<>();
            for(String name:strings(row,"queryMetadata"))queried.put(name,object("present",item.hasMetadata(name),"value",item.metadataValue(name)));
            for(String name:strings(row,"queryBuiltIns"))builtins.put(name,item.metadataValue(name));
            items.add(object("ItemType",item.itemType(),"EvaluatedInclude",item.evaluatedInclude(),"metadata",queried,
                "direct",metadata(item.directMetadata()),"effective",metadata(item.metadata()),"builtIns",builtins));
            types.putIfAbsent(item.itemType(),result.items(item.itemType()).stream().map(ItemSnapshot::evaluatedInclude).toList());
        }
        for(var definition:result.itemDefinitions().values()) {
            Map<String,Object> queried=new LinkedHashMap<>();
            for(String name:strings(row,"queryMetadata"))queried.put(name,definition.metadataValue(name));
            definitions.put(definition.itemType(),object("metadata",metadata(definition.metadata().values()),"queried",queried));
        }
        var imports=result.imports().stream().map(i->object("owner",i.owner().toString(),"path",i.target().toString(),"line",i.line())).toList();
        return object("properties",properties,"items",items,"byType",types,"definitions",definitions,"imports",imports);
    }
    static Object warning(ProjectEvaluationComponent.ConditionWarning warning) {
        return object("kind","warning","Code",warning.referenceCode(),"File",warning.file().toString(),"LineNumber",warning.line(),"ColumnNumber",warning.column());
    }
    static final class Observed {
        final Map<String,Object> wire;
        final ProjectEvaluationComponent.Result retained;
        Observed(Map<String,Object> wire,ProjectEvaluationComponent.Result retained) { this.wire=wire;this.retained=retained; }
    }
    static Observed evaluate(Path project,Map<String,String> globals,Map<String,Object> row,boolean mutation) throws Exception {
        try {
            var result=ProjectEvaluationComponent.evaluate(project,project.getParent(),globals);
            Map<String,Object> before=snapshot(result,row);List<Object> diagnostics=new ArrayList<>();
            result.conditionWarnings().forEach(w->diagnostics.add(warning(w)));
            for(var duplicate:result.duplicateImports()) {
                // Position record is private by historical design: reflected accessor, no fabricated coordinates.
                var position=duplicate.getClass().getMethod("current").invoke(duplicate);
                var line=position.getClass().getDeclaredMethod("line");line.setAccessible(true);
                var column=position.getClass().getDeclaredMethod("column");column.setAccessible(true);
                diagnostics.add(object("kind","warning","Code",duplicate.referenceCode(),"File",duplicate.owner().toString(),"LineNumber",line.invoke(position),"ColumnNumber",column.invoke(position)));
            }
            Object probe=null;
            if(mutation) {
                globals.put("P","mutated");boolean refused=false;
                try{result.items().clear();}catch(UnsupportedOperationException expected){refused=true;}
                if(!refused)throw new AssertionError("Mutable items snapshot");
                probe=object("caller",new LinkedHashMap<>(globals),"collectionMutationRefused",true,"after",snapshot(result,row));
            }
            return new Observed(object("result",object("success",true,"snapshot",before,"mutation",probe),"diagnostics",diagnostics),result);
        } catch(ProjectEvaluationComponent.ProfileRejected failure) {
            List<Object> diagnostics=new ArrayList<>();failure.conditionWarnings.forEach(w->diagnostics.add(warning(w)));
            var site=failure.conditionSite;
            return new Observed(object("result",object("success",false,"privateCode",failure.code,"message",failure.getMessage(),
                "file",site==null?null:site.file().toString(),"line",site==null?null:site.line(),"column",site==null?null:site.column()),"diagnostics",diagnostics),null);
        }
    }
    public static void main(String[] args) throws Exception {
        if(args.length!=4)throw new IllegalArgumentException("ROOT MANIFEST PRODUCT_JAR SHA256");
        Path root=Path.of(args[0]).toRealPath(),manifest=Path.of(args[1]).toRealPath(),jar=Path.of(args[2]).toRealPath();
        Path loaded=Path.of(ProjectEvaluationComponent.class.getProtectionDomain().getCodeSource().getLocation().toURI()).toRealPath();
        if(!loaded.equals(jar)||!hash(jar).equals(args[3]))throw new IllegalArgumentException("Product JAR identity differs");
        var cases=list(map(read(Files.readString(manifest))).get("cases"));if(cases.size()!=42)throw new IllegalArgumentException("Expected 42 scenarios");
        List<Object> rows=new ArrayList<>();
        for(Object definition:cases) {
            var row=map(definition);String id=(String)row.get("id");Path folder=child(root,id);
            System.err.println("DOTJ_ITEMS_PRODUCT BEGIN "+id);
            Map<String,String> globals=globals(row.get("globals"));
            Observed first=evaluate(child(folder,"main.proj"),globals,row,id.equals("IS02"));
            String firstSnapshot=first.retained==null?null:write(snapshot(first.retained,row));
            List<Object> observations=new ArrayList<>();observations.add(first.wire);
            for(Object value:list(row.get("steps"))) {
                var step=map(value);String kind=(String)step.get("kind");
                switch(kind) {
                    case "filesystem-change" -> {
                        for(var entry:map(step.get("write")).entrySet())Files.writeString(child(folder,entry.getKey()),(String)entry.getValue());
                        for(String path:strings(step,"delete"))Files.delete(child(folder,path));
                        observations.add(object("action",kind,"completed",true));
                    }
                    case "caller-global-mutation" -> {
                        globals.put((String)step.get("name"),(String)step.get("value"));
                        observations.add(object("action",kind,"caller",new LinkedHashMap<>(globals)));
                    }
                    case "private-snapshot-mutation-attempt" -> {
                        if(first.retained==null)throw new AssertionError("Missing retained snapshot");
                        int refusals=0;
                        try{first.retained.items().clear();}catch(UnsupportedOperationException expected){refusals++;}
                        try{first.retained.items("I").clear();}catch(UnsupportedOperationException expected){refusals++;}
                        try{first.retained.itemDefinitions().clear();}catch(UnsupportedOperationException expected){refusals++;}
                        try{first.retained.items().getFirst().directMetadata().clear();}catch(UnsupportedOperationException expected){refusals++;}
                        if(refusals!=4)throw new AssertionError("Snapshot mutation allowed");
                        observations.add(object("action",kind,"refusals",refusals));
                    }
                    case "repeat-owner", "evaluate-xml" -> {
                        Path target=child(folder,(String)step.get("owner"));
                        if(kind.equals("evaluate-xml"))Files.writeString(target,(String)step.get("xml"));
                        else if(!target.equals(child(folder,"main.proj")))Files.copy(child(folder,"main.proj"),target);
                        observations.add(evaluate(target,step.containsKey("globals")?globals(step.get("globals")):new LinkedHashMap<>(globals),row,false).wire);
                    }
                    default -> throw new IllegalArgumentException("Unknown declared step "+kind);
                }
            }
            boolean unchanged=first.retained==null||firstSnapshot.equals(write(snapshot(first.retained,row)));
            boolean absent=!Files.exists(child(folder,"must-not-exist.txt"));
            if(!unchanged||!absent)throw new AssertionError("Snapshot or task boundary violated");
            rows.add(object("id",id,"observations",observations,"retainedFirstSnapshotUnchanged",unchanged,"taskMarkerAbsent",absent));
            System.err.println("DOTJ_ITEMS_PRODUCT END "+id);
        }
        System.out.println(write(object("schemaVersion",1,"scenarioCount",rows.size(),"rows",rows,"jar",jar.toString(),"jarSha256",hash(jar),
            "os",System.getProperty("os.name"),"javaVersion",System.getProperty("java.runtime.version"),"root",root.toString())));
    }
}
