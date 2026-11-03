import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.security.MessageDigest;
import java.util.*;
import java.util.jar.*;
import java.util.spi.ToolProvider;

/** Owned source launcher bootstrap. It compiles in memory before these checks run. */
class Bootstrap {
    static final String MODULE = "org.dotj.build.evaluation.candidate";
    static final String VERSION = "0.1.100-dev.1";
    static final String BASE = "7f7d08b4048ed3fd68d1c5998382aa59085cefb5";
    static void require(boolean condition, String message) throws IOException {
        if (!condition) throw new IOException(message);
    }
    static String hash(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }
    static String hash(Path path) throws Exception {
        MessageDigest digest=MessageDigest.getInstance("SHA-256");
        try (InputStream in=Files.newInputStream(path)) {
            byte[] buffer=new byte[65536]; int n;
            while ((n=in.read(buffer))!=-1) digest.update(buffer,0,n);
        }
        return HexFormat.of().formatHex(digest.digest());
    }
    static Path plain(Path path) throws IOException {
        Path value=path.toAbsolutePath().normalize();
        for (Path p=value;p!=null;p=p.getParent()) if (Files.exists(p,LinkOption.NOFOLLOW_LINKS)) {
            BasicFileAttributes a=Files.readAttributes(p,BasicFileAttributes.class,LinkOption.NOFOLLOW_LINKS);
            require(!a.isSymbolicLink() && !a.isOther() && p.toRealPath().equals(p),"SYMLINK_PROFILE: "+p);
        }
        return value;
    }
    static Properties properties(Path path) throws IOException {
        Properties p=new Properties();
        try (Reader r=Files.newBufferedReader(path,StandardCharsets.UTF_8)) {p.load(r);}
        return p;
    }
    static void environment() throws IOException {
        for (String key:List.of("JAVA_TOOL_OPTIONS","JDK_JAVA_OPTIONS","_JAVA_OPTIONS","CLASSPATH"))
            require(System.getenv(key)==null,"AMBIENT_JAVA_ENVIRONMENT: "+key);
    }
    static void jdk(Properties pins) throws Exception {
        environment(); String selected=System.getenv("JAVA_HOME");
        require(selected!=null && !selected.isBlank(),"JAVA_HOME_REQUIRED");
        Path home=plain(Path.of(selected));
        require(home.equals(Path.of(System.getProperty("java.home")).toRealPath()),"JDK_EXECUTING_HOME_MISMATCH");
        String os=System.getProperty("os.name").startsWith("Windows")?"windows":"linux";
        require(os.equals("windows") || System.getProperty("os.name").equals("Linux"),"OS_PROFILE");
        String[] files=pins.getProperty(os+".files").split(",");
        for (String relative:files) {
            Path file=plain(home.resolve(relative));
            require(Files.isRegularFile(file) && hash(file).equals(pins.getProperty(os+"."+relative)),"JDK_IDENTITY: "+relative);
        }
        Properties release=properties(home.resolve("release"));
        require(release.getProperty("IMPLEMENTOR").equals("\"Microsoft\"") && release.getProperty("OS_ARCH").equals("\"x86_64\""),"JDK_VENDOR_ARCH");
        require(System.getProperty("os.arch").equals("amd64") || System.getProperty("os.arch").equals("x86_64"),"EXECUTING_ARCH");
        require(ToolProvider.findFirst("javac").isPresent() && ToolProvider.findFirst("jar").isPresent(),"JDK_TOOL_PROVIDER_MISSING");
    }
    static void noSelection(Path directory) throws IOException {
        for (Path p=directory.toAbsolutePath().normalize();p!=null;p=p.getParent())
            require(!Files.exists(p.resolve("global.json"),LinkOption.NOFOLLOW_LINKS),"GLOBAL_JSON_SELECTION_UNSUPPORTED: "+p);
    }
    static int tool(String name,List<String> argv) {
        return ToolProvider.findFirst(name).orElseThrow().run(System.out,System.err,argv.toArray(String[]::new));
    }
    static String decode(String value) throws java.nio.charset.CharacterCodingException {
        return StandardCharsets.UTF_8.newDecoder().decode(java.nio.ByteBuffer.wrap(Base64.getDecoder().decode(value))).toString();
    }
    public static void main(String[] args) {
        System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out),true,StandardCharsets.UTF_8));
        System.setErr(new PrintStream(new FileOutputStream(FileDescriptor.err),true,StandardCharsets.UTF_8));
        try {
            if(System.getProperty("dotj.seed.encoded")!=null) {
                require(args.length==0,"BOOTSTRAP_ARGUMENT_TRANSPORT");
                args=new String[3];
                for(int i=0;i<args.length;i++)args[i]=decode(System.getProperty("dotj.seed.arg."+i));
            }
            build(args);
        }
        catch (Exception error) {System.err.println("dotj seed: "+error.getMessage());System.exit(1);}
    }
    static void build(String[] args) throws Exception {
        require(args.length==3,"Expected source root, output root, source-lock digest");
        Path source=plain(Path.of(args[0])); Path output=plain(Path.of(args[1]));
        Path seed=source.resolve("dotj-sdk/seed"); Path lock=seed.resolve("sources.properties");
        require(hash(lock).equals(args[2]),"SOURCE_MANIFEST_IDENTITY");
        Properties inputs=properties(lock); Properties pins=properties(seed.resolve("jdk.properties"));
        jdk(pins);
        String caller=System.getProperty("dotj.cwd.b64");
        noSelection(caller==null?Path.of(""):Path.of(decode(caller)));
        String script=System.getProperty("dotj.seed.script.b64");
        require(plain(Path.of(script==null?System.getProperty("dotj.seed.script",""):decode(script))).getParent().equals(seed),"SEED_LAUNCHER_IDENTITY");
        require(!output.startsWith(source),"OUTPUT_MUST_BE_OUTSIDE_SOURCE");
        require(output.getParent()!=null && Files.isDirectory(output.getParent()),"OUTPUT_PARENT_REQUIRED");
        String dotjRoot=System.getenv("DOTJ_ROOT");
        require(dotjRoot==null || plain(Path.of(dotjRoot)).equals(output),"DOTJ_ROOT_CONFLICT");
        List<String> sources=List.of(inputs.getProperty("sources").split(","));
        require(sources.size()==7 && new HashSet<>(sources).size()==7,"SOURCE_CLOSURE");
        List<String> sorted=new ArrayList<>(sources);Collections.sort(sorted);require(sorted.equals(sources),"SOURCE_ORDER");
        for (String key:inputs.stringPropertyNames()) if (key.startsWith("sha256.")) {
            String relative=key.substring(7);Path file=plain(source.resolve(relative));
            require(file.startsWith(source) && Files.isRegularFile(file),"SOURCE_PATH: "+relative);
            byte[] bytes=Files.readAllBytes(file);
            if (relative.endsWith(".java")) bytes=new String(bytes,StandardCharsets.UTF_8).replace("\r\n","\n").getBytes(StandardCharsets.UTF_8);
            require(hash(bytes).equals(inputs.getProperty(key)),"SOURCE_IDENTITY: "+relative);
        }
        for (String relative:sources) require(inputs.containsKey("sha256."+relative),"UNPINNED_SOURCE");
        String fingerprint=hash(Files.readAllBytes(lock));
        // Every failure above precedes product staging. Stages are retained for diagnosis.
        Path stage=Files.createTempDirectory(output.getParent(),".dotj-stage-");
        Path classes=Files.createDirectory(stage.resolve("classes")); Path empty=Files.createDirectory(stage.resolve("empty"));
        Path frozen=Files.createDirectory(stage.resolve("source"));
        List<String> javac=new ArrayList<>(List.of("--release","21","-encoding","UTF-8","-proc:none","-implicit:none","-classpath",empty.toString(),"-sourcepath",frozen.toString(),"-d",classes.toString()));
        for (String relative:sources) {
            Path target=frozen.resolve(relative.substring(relative.indexOf("/src/")+5));Files.createDirectories(target.getParent());
            Files.writeString(target,Files.readString(source.resolve(relative),StandardCharsets.UTF_8).replace("\r\n","\n"),StandardCharsets.UTF_8);
            require(hash(target).equals(inputs.getProperty("sha256."+relative)),"STAGED_SOURCE_IDENTITY: "+relative);
            javac.add(target.toString());
        }
        try(var files=Files.walk(frozen)) {require(files.filter(Files::isRegularFile).count()==sources.size(),"STAGED_SOURCE_INVENTORY");}
        List<String> jarArgs=List.of("--create","--file",stage.resolve("dotj.jar").toString(),"--date=2020-01-01T00:00:00Z","--manifest",stage.resolve("manifest.mf").toString(),"-C",classes.toString(),".","-C",stage.resolve("resources").toString(),".");
        Properties operations=new Properties();
        for(String name:List.of("javac","jar")) {
            ToolProvider provider=ToolProvider.findFirst(name).orElseThrow();
            operations.setProperty(name+".provider",provider.getClass().getName());
            operations.setProperty(name+".module",provider.getClass().getModule().getName());
            operations.setProperty(name+".origin",String.valueOf(provider.getClass().getResource(provider.getClass().getSimpleName()+".class")));
            List<String> arguments=name.equals("javac")?javac:jarArgs;
            for(int i=0;i<arguments.size();i++)operations.setProperty(name+".arg."+i,arguments.get(i));
        }
        try(Writer writer=Files.newBufferedWriter(stage.resolve("operations.properties"),StandardCharsets.UTF_8)){operations.store(writer,"Actual in-process tool-provider argv; timestamp is retained stage evidence, not JAR input");}
        require(tool("javac",javac)==0,"COMPILATION_FAILED; prior SDK preserved; stage="+stage);
        Path resources=Files.createDirectories(stage.resolve("resources/dotj"));
        Files.copy(seed.resolve("jdk.properties"),resources.resolve("jdk.properties"));
        Manifest manifest=new Manifest();Attributes attrs=manifest.getMainAttributes();
        attrs.putValue("Manifest-Version","1.0");attrs.putValue("Implementation-Title","dotj evaluation SDK");
        attrs.putValue("Implementation-Version",VERSION);attrs.putValue("Dotj-Source-SHA256",fingerprint);attrs.putValue("Dotj-Framework-Base",BASE);
        Path manifestFile=stage.resolve("manifest.mf");try(OutputStream out=Files.newOutputStream(manifestFile)){manifest.write(out);}
        Path jar=stage.resolve("dotj.jar");
        require(tool("jar",jarArgs)==0,"JAR_FAILED");
        try(JarFile archive=new JarFile(jar.toFile())) {
            require(archive.getEntry("module-info.class")!=null && archive.getEntry("org/dotj/internal/build/evaluation/SdkMain.class")!=null,"ARTIFACT_INCOMPLETE");
            require(archive.getManifest().getMainAttributes().getValue("Dotj-Source-SHA256").equals(fingerprint),"ARTIFACT_MANIFEST");
        }
        String jarHash=hash(jar);String payload=fingerprint+"-"+jarHash;
        Path publish=Files.createDirectory(stage.resolve("sdk"));Path version=Files.createDirectories(publish.resolve("versions").resolve(payload));
        Files.copy(jar,version.resolve("dotj.jar"));
        for(String name:List.of("dotj","dotj.ps1"))Files.copy(source.resolve("dotj-sdk/launcher").resolve(name),publish.resolve(name));
        Files.writeString(publish.resolve(".dotj-owned"),"dotj evaluation SDK v1\n",StandardCharsets.UTF_8);
        String selection=payload+"\n"+jarHash+"\n";Files.writeString(publish.resolve("current"),selection,StandardCharsets.UTF_8);
        if (!Files.exists(output)) {
            Files.move(publish,output,StandardCopyOption.ATOMIC_MOVE);
        } else {
            plain(output.resolve("versions"));plain(output.resolve("current"));plain(output.resolve(".dotj-owned"));
            require(Files.readString(output.resolve(".dotj-owned")).equals("dotj evaluation SDK v1\n"),"OUTPUT_NOT_OWNED");
            for(String name:List.of("dotj","dotj.ps1"))require(hash(plain(output.resolve(name))).equals(hash(publish.resolve(name))),"OUTPUT_LAUNCHER_DIFFERS; choose a fresh output root");
            Path destination=plain(output.resolve("versions").resolve(payload));
            if (!Files.exists(destination))Files.move(version,destination,StandardCopyOption.ATOMIC_MOVE);
            else require(hash(plain(destination.resolve("dotj.jar"))).equals(jarHash),"RETAINED_PAYLOAD_IDENTITY");
            Path pointer=Files.createTempFile(output,".current-",".tmp");Files.writeString(pointer,selection,StandardCharsets.UTF_8);
            Files.move(pointer,output.resolve("current"),StandardCopyOption.ATOMIC_MOVE,StandardCopyOption.REPLACE_EXISTING);
        }
        System.out.println("Built dotj "+VERSION+" source="+fingerprint+" jar="+jarHash+" at "+output);
    }
}
