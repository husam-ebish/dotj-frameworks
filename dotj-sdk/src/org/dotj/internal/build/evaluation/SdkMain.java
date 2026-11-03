package org.dotj.internal.build.evaluation;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.security.MessageDigest;
import java.util.*;
import java.util.jar.*;
import java.util.spi.ToolProvider;

/** Internal evaluation-only CLI; the module deliberately exports and opens no packages. */
public final class SdkMain {
    private SdkMain() { }
    private static final String VERSION="0.1.100-dev.1";
    private static final class Rejected extends Exception {
        Rejected(String message) {super(message);}
    }
    private static void require(boolean condition,String message) throws Rejected {
        if (!condition)throw new Rejected(message);
    }
    private static String hash(Path file) throws Exception {
        MessageDigest digest=MessageDigest.getInstance("SHA-256");
        try(InputStream in=Files.newInputStream(file)) {
            byte[] buffer=new byte[65536];int n;
            while((n=in.read(buffer))!=-1)digest.update(buffer,0,n);
        }
        return HexFormat.of().formatHex(digest.digest());
    }
    private static Path plain(Path input) throws Exception {
        Path value=input.toAbsolutePath().normalize();
        for(Path p=value;p!=null;p=p.getParent())if(Files.exists(p,LinkOption.NOFOLLOW_LINKS)) {
            BasicFileAttributes a=Files.readAttributes(p,BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);
            require(!a.isSymbolicLink() && !a.isOther() && p.toRealPath().equals(p),"SYMLINK_PROFILE: "+p);
        }
        return value;
    }
    private static void noSelection(Path directory) throws Rejected {
        for(Path p=directory.toAbsolutePath().normalize();p!=null;p=p.getParent())
            require(!Files.exists(p.resolve("global.json"),LinkOption.NOFOLLOW_LINKS),"GLOBAL_JSON_SELECTION_UNSUPPORTED: "+p);
    }
    private static String decode(String property) throws java.nio.charset.CharacterCodingException {
        return StandardCharsets.UTF_8.newDecoder().decode(java.nio.ByteBuffer.wrap(Base64.getDecoder().decode(System.getProperty(property)))).toString();
    }
    private static Path callerDirectory() throws java.nio.charset.CharacterCodingException {
        return System.getProperty("dotj.cwd.b64")==null?Path.of("").toAbsolutePath():Path.of(decode("dotj.cwd.b64"));
    }
    private static Attributes startup() throws Exception {
        for(String key:List.of("JAVA_TOOL_OPTIONS","JDK_JAVA_OPTIONS","_JAVA_OPTIONS","CLASSPATH"))
            require(System.getenv(key)==null,"AMBIENT_JAVA_ENVIRONMENT: "+key);
        String selected=System.getenv("JAVA_HOME");require(selected!=null && !selected.isBlank(),"JAVA_HOME_REQUIRED");
        Path jdk=plain(Path.of(selected));require(jdk.equals(Path.of(System.getProperty("java.home")).toRealPath()),"JDK_EXECUTING_HOME_MISMATCH");
        Properties pins=new Properties();
        try(InputStream stream=SdkMain.class.getResourceAsStream("/dotj/jdk.properties")) {
            require(stream!=null,"JDK_LOCK_MISSING");pins.load(new InputStreamReader(stream,StandardCharsets.UTF_8));
        }
        String os=System.getProperty("os.name").startsWith("Windows")?"windows":"linux";
        require(os.equals("windows") || System.getProperty("os.name").equals("Linux"),"OS_PROFILE");
        for(String relative:pins.getProperty(os+".files").split(",")) {
            Path file=plain(jdk.resolve(relative));
            require(Files.isRegularFile(file) && hash(file).equals(pins.getProperty(os+"."+relative)),"JDK_IDENTITY: "+relative);
        }
        require(System.getProperty("os.arch").equals("amd64") || System.getProperty("os.arch").equals("x86_64"),"EXECUTING_ARCH");
        require(ToolProvider.findFirst("javac").isPresent() && ToolProvider.findFirst("jar").isPresent(),"JDK_TOOL_PROVIDER_MISSING");
        require(SdkMain.class.getModule().isNamed() && SdkMain.class.getModule().getName().equals("org.dotj.build.evaluation.candidate"),"MODULE_IDENTITY");
        Path jar=plain(Path.of(SdkMain.class.getProtectionDomain().getCodeSource().getLocation().toURI()));
        Path root=plain(jar.getParent().getParent().getParent());
        require(Files.isRegularFile(jar) && jar.getFileName().toString().equals("dotj.jar") && jar.getParent().getParent().getParent().equals(root),"SDK_ROOT_IDENTITY");
        Path launcher=plain(Path.of(System.getProperty("dotj.launcher.b64")==null?System.getProperty("dotj.launcher",""):decode("dotj.launcher.b64")));
        require(launcher.getParent().equals(root) && Files.isRegularFile(launcher),"LAUNCHER_ROOT_IDENTITY");
        String dotjRoot=System.getenv("DOTJ_ROOT");require(dotjRoot==null || plain(Path.of(dotjRoot)).equals(root),"DOTJ_ROOT_CONFLICT");
        require(hash(jar).equals(System.getProperty("dotj.jar.sha256")),"ARTIFACT_IDENTITY");
        List<String> pointer=Files.readAllLines(plain(root.resolve("current")),StandardCharsets.UTF_8);
        require(pointer.size()==2 && pointer.get(0).equals(jar.getParent().getFileName().toString()) && pointer.get(1).equals(hash(jar)),"ARTIFACT_SELECTION_IDENTITY");
        noSelection(callerDirectory());
        try(JarFile archive=new JarFile(jar.toFile())) {
            Attributes attrs=archive.getManifest().getMainAttributes();
            require(VERSION.equals(attrs.getValue("Implementation-Version")) && attrs.getValue("Dotj-Source-SHA256").matches("[0-9a-f]{64}"),"PRODUCT_MANIFEST_IDENTITY");
            return attrs;
        }
    }
    public static void main(String[] args) {
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out),true,StandardCharsets.UTF_8));
        System.setErr(new PrintStream(new FileOutputStream(FileDescriptor.err),true,StandardCharsets.UTF_8));
        int code;
        try {
            if(System.getProperty("dotj.arg.count")!=null) {
                require(args.length==0,"ARGUMENT_TRANSPORT");
                int count=Integer.parseInt(System.getProperty("dotj.arg.count"));require(count>=0 && count<=256,"ARGUMENT_BOUND");
                args=new String[count];for(int i=0;i<count;i++)args[i]=decode("dotj.arg."+i);
            }
            code=run(args,startup());
        }
        catch(Exception error) {System.err.println("dotj: "+error.getMessage());code=1;}
        if(code!=0)System.exit(code);
    }
    private static void help(boolean msbuild) {
        System.out.println(msbuild?"Usage: dotj msbuild <explicit-project> -getProperty:<name>[;<name>...] [-p:<name>=<value>]":"Usage: dotj [--help|-h|--version|--info] | msbuild <explicit-project> -getProperty:<name>");
        System.out.println("Evaluation-only SDK. Targets, compilation, restore, SDK selection, SDK-style projects and implicit Directory.Build discovery are unsupported.");
    }
    private static boolean helpFlag(String value) {return value.equals("--help") || value.equals("-h");}
    private static int syntax(String message) {System.out.println("dotj msbuild: "+message);return 1;}
    private static int run(String[] args,Attributes manifest) throws Exception {
        require(args.length<=256 && Arrays.stream(args).mapToInt(String::length).sum()<=32768,"ARGUMENT_BOUND");
        if(args.length==1) {
            if(helpFlag(args[0])) {help(false);return 0;}
            if(args[0].equals("--version")) {System.out.println(VERSION);return 0;}
            if(args[0].equals("--info")) {
                System.out.println("dotj SDK: "+VERSION);
                System.out.println("Profile: SDK-less explicit-project evaluation; existing JDK21");
                System.out.println("Source SHA256: "+manifest.getValue("Dotj-Source-SHA256"));
                System.out.println("Framework base: "+manifest.getValue("Dotj-Framework-Base"));
                System.out.println("Java: "+System.getProperty("java.runtime.version")+" / "+System.getProperty("java.vendor"));
                System.out.println("Platform: "+System.getProperty("os.name")+" / "+System.getProperty("os.arch"));return 0;
            }
        }
        require(args.length>0,"EXPLICIT_COMMAND_REQUIRED");
        if(!args[0].equals("msbuild"))throw new Rejected("COMMAND_UNSUPPORTED: "+args[0]);
        if(args.length==2 && helpFlag(args[1])) {help(true);return 0;}
        List<String> names=new ArrayList<>();List<String> projects=new ArrayList<>();Map<String,String> globals=new LinkedHashMap<>();int overrides=0;
        for(int i=1;i<args.length;i++) {
            String arg=args[i];
            if(arg.isEmpty())return syntax("EMPTY_ARGUMENT: an explicit nonempty argument is required");
            String prefix=arg.contains(":")?arg.substring(0,arg.indexOf(':')):arg;
            if(List.of("-getProperty","--getProperty","/getProperty").contains(prefix)) {
                if(!arg.contains(":"))return syntax("GET_PROPERTY_VALUE_REQUIRED");
                for(String name:arg.substring(arg.indexOf(':')+1).split("[;,]",-1)) {
                    if(!name.matches("[A-Za-z_][A-Za-z0-9_]*"))return syntax("PROPERTY_NAME_PROFILE: "+name);
                    ProjectEvaluationComponent.key(name);names.add(name);
                }
            } else if(List.of("-p","--p","/p","-property","--property","/property").contains(prefix)) {
                if(!arg.contains(":"))return syntax("PROPERTY_ASSIGNMENT_REQUIRED");
                String assignment=arg.substring(arg.indexOf(':')+1);int equal=assignment.indexOf('=');
                if(equal<1)return syntax("PROPERTY_ASSIGNMENT_REQUIRED");
                require(assignment.indexOf(';')<0 && assignment.indexOf(',')<0,"PROPERTY_ASSIGNMENT_LIST_UNSUPPORTED");
                String name=ProjectEvaluationComponent.key(assignment.substring(0,equal));
                globals.put(name,assignment.substring(equal+1));overrides++;
            } else if(List.of("-target","--target","/target","-t","--t","/t","-getItem","--getItem","/getItem","-getTargetResult","--getTargetResult","/getTargetResult","-getResultOutputFile","--getResultOutputFile","/getResultOutputFile").contains(prefix) || arg.startsWith("@")) {
                throw new Rejected("CAPABILITY_UNSUPPORTED: "+prefix);
            } else if(arg.startsWith("-"))return syntax("UNKNOWN_OPTION: "+arg);
            else projects.add(arg);
        }
        if(projects.size()!=1)return syntax("EXPLICIT_PROJECT_REQUIRED: expected one project, received "+projects.size());
        require(!names.isEmpty(),"TARGET_EXECUTION_UNSUPPORTED: property query required");
        require(names.size()<=64 && overrides<=64,"QUERY_PROPERTY_BOUND");
        Path project=callerDirectory().resolve(projects.getFirst()).toAbsolutePath().normalize();
        require(Files.isRegularFile(project),"PROJECT_NOT_FOUND: "+project);
        require(project.toString().endsWith(".proj") || project.toString().endsWith(".props") || project.toString().endsWith(".targets"),"PROJECT_FILE_PROFILE");
        noSelection(project.getParent());
        try {
            ProjectEvaluationComponent.Result result=ProjectEvaluationComponent.evaluate(project,project.getParent(),globals);
            for(var warning:result.duplicateImports())System.err.println(warning.owner()+": warning "+warning.referenceCode()+": import ignored: "+warning.importedProject());
            for(var warning:result.conditionWarnings())System.err.println(warning.file()+"("+warning.line()+","+warning.column()+"): warning "+warning.referenceCode()+": "+warning.condition());
            if(names.size()==1)System.out.println(result.property(names.getFirst()));
            else {
                Map<String,String> values=new LinkedHashMap<>();for(String name:names)values.put(name,result.property(name));
                System.out.println("{");System.out.println("  \"Properties\": {");int index=0;
                for(var entry:values.entrySet())System.out.println("    "+json(entry.getKey())+": "+json(entry.getValue())+(++index<values.size()?",":""));
                System.out.println("  }");System.out.println("}");
            }
            return 0;
        } catch(ProjectEvaluationComponent.EvaluationFailure failure) {
            System.err.println(failure.project+": error "+failure.referenceCode+": "+failure.getMessage());return 1;
        } catch(ProjectEvaluationComponent.ProfileRejected failure) {
            System.err.println(project+": OUTSIDE_ADMITTED_PROFILE "+failure.code+": "+failure.getMessage());return 1;
        }
    }
    private static String json(String value) {
        StringBuilder result=new StringBuilder("\"");
        for(int i=0;i<value.length();i++) {
            char c=value.charAt(i);
            switch(c) {
                case '\b' -> result.append("\\b");case '\t' -> result.append("\\t");case '\n' -> result.append("\\n");
                case '\f' -> result.append("\\f");case '\r' -> result.append("\\r");case '\\' -> result.append("\\\\");
                default -> {
                    if(c<32 || c>126 || "<>&'\"+`".indexOf(c)>=0)result.append(String.format(Locale.ROOT,"\\u%04X",(int)c));
                    else result.append(c);
                }
            }
        }
        return result.append('"').toString();
    }
}
