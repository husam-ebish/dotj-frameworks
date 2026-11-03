package org.dotj.internal.build.evaluation;

import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;
import java.util.regex.Pattern;

/** Selected Project/FileEntryExpansionCache profile: case-insensitive wildcard filtering,
 * actual filesystem lookup for a fixed prefix. Pure selection never enumerates files. */
final class ItemGlobs {
    record Match(String escapedIdentity,String recursiveDir) { }
    final Path root,sandbox;
    int visited;
    ItemGlobs(Path root,Path sandbox) { this.root=root;this.sandbox=sandbox; }
    static boolean wildcard(String raw) { return raw.indexOf('*')>=0||raw.indexOf('?')>=0; }
    static void validate(String raw) {
        ItemExpressions.ascii(raw);
        if(raw.startsWith("/")||raw.indexOf(':')>=0||raw.indexOf('\\')>=0)
            throw ItemExpressions.fail("ITEM_GLOB_PATH", "Only relative slash patterns are selected");
        String[] parts=raw.split("/",-1);
        if(parts.length>64)throw ItemExpressions.fail("ITEM_PATTERN_BOUND", "More than 64 pattern segments");
        for(String part:parts) {
            if(part.equals(".."))throw ItemExpressions.fail("ITEM_GLOB_PATH", "Parent traversal is not selected");
            if(part.contains("**")&&!part.equals("**"))throw ItemExpressions.fail("ITEM_GLOB_SHAPE", "Recursive wildcard must be a complete segment");
        }
    }
    static boolean matches(String pattern,String identity) {
        validate(pattern);
        return Pattern.compile(regex(stripDot(pattern)),Pattern.CASE_INSENSITIVE).matcher(stripDot(identity.replace('\\','/'))).matches();
    }
    private static String stripDot(String value) { while(value.startsWith("./"))value=value.substring(2);return value; }
    private static String regex(String pattern) {
        String[] segments=pattern.split("/",-1);StringBuilder regex=new StringBuilder("^");
        for(int n=0;n<segments.length;n++) {
            String part=segments[n];
            if(part.equals("**")) {
                regex.append(n==segments.length-1?".*":"(?:[^/]+/)*");continue;
            }
            if(part.equals("*.*"))part="*";
            for(int i=0;i<part.length();i++) {
                char c=part.charAt(i);
                if(c=='*')regex.append("[^/]*");
                else if(c=='?')regex.append("[^/]");
                else if(c=='%') {
                    if(i+2>=part.length())throw ItemExpressions.fail("ITEM_ESCAPE", "Incomplete pattern escape");
                    regex.append(Pattern.quote(ItemExpressions.decode(part.substring(i,i+3))));i+=2;
                } else regex.append(Pattern.quote(String.valueOf(c)));
            }
            if(n<segments.length-1)regex.append('/');
        }
        return regex.append('$').toString();
    }
    List<Match> enumerate(String raw) throws IOException {
        validate(raw);
        String[] parts=raw.split("/",-1);int first=0;
        while(first<parts.length&&!wildcard(parts[first]))first++;
        // Lookup and returned identities use raw names; the stored identity is
        // escaped once by walk, including literal percent sequences.
        String prefix=ItemExpressions.decode(String.join("/",Arrays.copyOfRange(parts,0,first)));
        Path start=root;
        check(start);
        for(int i=0;i<first;i++) {
            if(parts[i].isEmpty()||parts[i].equals("."))continue;
            start=start.resolve(ItemExpressions.decode(parts[i]));
            if(!Files.exists(start,LinkOption.NOFOLLOW_LINKS))return List.of();
            check(start);
        }
        if(!Files.isDirectory(start,LinkOption.NOFOLLOW_LINKS))return List.of();
        String tail=String.join("/",Arrays.copyOfRange(parts,first,parts.length));
        Pattern filter=Pattern.compile(regex(tail),Pattern.CASE_INSENSITIVE);
        boolean recursive=Arrays.asList(parts).contains("**");
        int levels=recursive?Integer.MAX_VALUE:parts.length-first;
        List<Match> result=new ArrayList<>();
        walk(start,start,prefix,filter,levels,0,result);
        // EngineFileUtilities sorts raw names before escaping. Decode our stored
        // representation once to recover that raw ASCII key (including literal %).
        result.sort(Comparator.comparing(m->ItemExpressions.decode(m.escapedIdentity()).toUpperCase(Locale.ROOT)));
        return List.copyOf(result);
    }
    private void walk(Path start,Path directory,String prefix,Pattern filter,int levels,int level,List<Match> result) throws IOException {
        int depth=root.relativize(directory.normalize()).getNameCount();
        if(directory.normalize().equals(root))depth=0;
        if(depth>32)throw ItemExpressions.fail("ITEM_DEPTH_BOUND", "Traversal depth exceeds 32");
        check(directory);
        List<Path> entries=new ArrayList<>();Set<String> siblings=new HashSet<>();
        try(DirectoryStream<Path> stream=Files.newDirectoryStream(directory)) {
            for(Path entry:stream) {
                if(++visited>4096)throw ItemExpressions.fail("ITEM_TRAVERSAL_BOUND", "More than 4096 visited filesystem entries");
                String name=entry.getFileName().toString();ItemExpressions.ascii(name);
                if(!siblings.add(name.toUpperCase(Locale.ROOT)))throw ItemExpressions.fail("ITEM_CASE_COLLISION", "Case-colliding sibling names");
                check(entry);entries.add(entry);
            }
        }
        entries.sort(Comparator.comparing(p->p.getFileName().toString().toUpperCase(Locale.ROOT)));
        for(Path entry:entries) {
            if(Files.isDirectory(entry,LinkOption.NOFOLLOW_LINKS)) {
                if(level+1<levels)walk(start,entry,prefix,filter,levels,level+1,result);
            } else if(Files.isRegularFile(entry,LinkOption.NOFOLLOW_LINKS)) {
                String relative=start.relativize(entry).toString().replace('\\','/');
                if(filter.matcher(relative).matches()) {
                    String identity=(prefix.isEmpty()?"":prefix+"/")+relative;
                    String recursive=relative.substring(0,Math.max(0,relative.lastIndexOf('/')+1));
                    String separator=root.getFileSystem().getSeparator();
                    result.add(new Match(ItemExpressions.escape(identity.replace("/",separator)),recursive.replace("/",separator)));
                }
            }
        }
    }
    private void check(Path path) throws IOException {
        Path normalized=path.toAbsolutePath().normalize();
        if(!normalized.startsWith(sandbox))throw ItemExpressions.fail("ITEM_GLOB_BOUNDARY", "Enumeration outside fixture sandbox");
        BasicFileAttributes attributes=Files.readAttributes(path,BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);
        if(attributes.isSymbolicLink()||attributes.isOther())throw ItemExpressions.fail("ITEM_GLOB_ALIAS", "Filesystem aliases are not selected");
        Path real=path.toRealPath();
        boolean same=root.getFileSystem().getSeparator().equals("\\")
            ?real.toString().equalsIgnoreCase(normalized.toString()):real.equals(normalized);
        if(!same||!real.startsWith(sandbox))throw ItemExpressions.fail("ITEM_GLOB_ALIAS", "Resolved filesystem alias");
    }
}
