package org.dotj.internal.build.evaluation;

import java.nio.file.Path;
import java.util.*;

/** Immutable private observation, not the mutable public ProjectItem API. */
final class ItemSnapshot {
    record Metadata(String name,String escapedValue) {
        String value() { return ItemExpressions.decode(escapedValue); }
    }
    record Definition(String itemType,Map<String,Metadata> metadata) {
        Definition { metadata=freeze(metadata); }
        String metadataValue(String name) {
            Metadata value=metadata.get(ItemExpressions.key(name));return value==null?"":value.value();
        }
    }
    static final Set<String> BUILTINS=Set.of("IDENTITY","FULLPATH","ROOTDIR","FILENAME","EXTENSION",
        "RELATIVEDIR","DIRECTORY","RECURSIVEDIR","DEFININGPROJECTFULLPATH","DEFININGPROJECTDIRECTORY",
        "DEFININGPROJECTNAME","DEFININGPROJECTEXTENSION");
    static boolean builtIn(String name) { return BUILTINS.contains(ItemExpressions.key(name)); }
    static boolean timestamp(String name) {
        return Set.of("MODIFIEDTIME","CREATEDTIME","ACCESSEDTIME").contains(ItemExpressions.key(name));
    }
    static <T> Map<String,T> freeze(Map<String,T> input) {
        return Collections.unmodifiableMap(new LinkedHashMap<>(input));
    }
    final String itemType, escapedInclude, recursiveDir;
    final Path root, definingProject;
    final Map<String,Metadata> defaults, direct;
    final List<Map<String,Metadata>> inherited;
    private final Map<String,Metadata> effective;
    ItemSnapshot(String type,String include,String recursive,Path root,Path owner,
                 Map<String,Metadata> defaults,List<Map<String,Metadata>> inherited,Map<String,Metadata> direct) {
        this.itemType=type;escapedInclude=include;recursiveDir=recursive;this.root=root;definingProject=owner;
        this.defaults=freeze(defaults);this.direct=freeze(direct);
        this.inherited=inherited.stream().map(ItemSnapshot::freeze).toList();
        Map<String,Metadata> all=new LinkedHashMap<>(defaults);
        for(int i=inherited.size()-1;i>=0;i--)all.putAll(inherited.get(i));
        all.putAll(direct);
        if(all.size()>64)throw ItemExpressions.fail("ITEM_METADATA_BOUND", "More than 64 effective metadata entries");
        effective=freeze(all);
    }
    ItemSnapshot copy(String type,Path owner,Map<String,Metadata> destinationDefaults) {
        List<Map<String,Metadata>> chain=new ArrayList<>(inherited);chain.add(defaults);
        return new ItemSnapshot(type,escapedInclude,recursiveDir,root,owner,destinationDefaults,chain,direct);
    }
    ItemSnapshot withMetadata(String name,String escapedValue) {
        Map<String,Metadata> changed=new LinkedHashMap<>(direct);
        changed.put(ItemExpressions.key(name),new Metadata(name,escapedValue));
        return new ItemSnapshot(itemType,escapedInclude,recursiveDir,root,definingProject,defaults,inherited,changed);
    }
    String itemType() { return itemType; }
    String evaluatedInclude() { return ItemExpressions.decode(escapedInclude); }
    List<Metadata> metadata() { return List.copyOf(effective.values()); }
    List<Metadata> directMetadata() { return List.copyOf(direct.values()); }
    boolean hasMetadata(String name) {
        if(timestamp(name))throw ItemExpressions.fail("METADATA_TIMESTAMP", "Timestamp metadata is not selected");
        return builtIn(name)||effective.containsKey(ItemExpressions.key(name));
    }
    String escapedMetadata(String name) {
        String[] parts=name.split("\\.",-1);
        String simple=parts[parts.length-1];
        if(parts.length>2 || parts.length==2&&!ItemExpressions.key(parts[0]).equals(ItemExpressions.key(itemType)))
            throw ItemExpressions.fail("METADATA_QUALIFIER", "Cross-item metadata is not selected");
        if(timestamp(simple))throw ItemExpressions.fail("METADATA_TIMESTAMP", "Timestamp metadata is not selected");
        if(builtIn(simple))return ItemExpressions.escape(metadataValue(simple));
        Metadata value=effective.get(ItemExpressions.key(simple));return value==null?"":value.escapedValue();
    }
    String metadataValue(String name) {
        String key=ItemExpressions.key(name);
        if(timestamp(name))throw ItemExpressions.fail("METADATA_TIMESTAMP", "Timestamp metadata is not selected");
        if(!BUILTINS.contains(key)) { Metadata value=effective.get(key);return value==null?"":value.value(); }
        String identity=evaluatedInclude();
        return switch(key) {
            case "IDENTITY" -> identity;
            case "RECURSIVEDIR" -> recursiveDir;
            case "FILENAME" -> stem(last(identity));
            case "EXTENSION" -> extension(last(identity));
            case "RELATIVEDIR" -> nativeSlashes(directory(identity));
            case "FULLPATH" -> fullPath(identity).toString();
            case "ROOTDIR" -> fullPath(identity).getRoot().toString();
            case "DIRECTORY" -> {
                Path full=fullPath(identity), parent=full.getParent();
                String value=parent==null?"":full.getRoot().relativize(parent).toString();
                yield value.isEmpty()?"":value+root.getFileSystem().getSeparator();
            }
            case "DEFININGPROJECTFULLPATH" -> definingProject.toString();
            case "DEFININGPROJECTDIRECTORY" -> definingProject.getParent()+root.getFileSystem().getSeparator();
            case "DEFININGPROJECTNAME" -> stem(definingProject.getFileName().toString());
            case "DEFININGPROJECTEXTENSION" -> extension(definingProject.getFileName().toString());
            default -> throw new AssertionError(key);
        };
    }
    private Path fullPath(String identity) {
        // Resolve on demand: ordinary literal identities need not be valid paths or exist.
        try { return root.resolve(nativeSlashes(identity)).toAbsolutePath().normalize(); }
        catch(java.nio.file.InvalidPathException ex) { throw ItemExpressions.fail("ITEM_PATH", "Invalid path metadata request"); }
    }
    private String nativeSlashes(String text) { return text.replace("\\",root.getFileSystem().getSeparator()).replace("/",root.getFileSystem().getSeparator()); }
    private static String last(String text) { return text.substring(Math.max(text.lastIndexOf('/'),text.lastIndexOf('\\'))+1); }
    private static String directory(String text) { return text.substring(0,Math.max(text.lastIndexOf('/'),text.lastIndexOf('\\'))+1); }
    private static String stem(String text) { int dot=text.lastIndexOf('.');return dot<0?text:text.substring(0,dot); }
    private static String extension(String text) { int dot=text.lastIndexOf('.');return dot<0?"":text.substring(dot); }
}
