import java.io.*;
import java.nio.ByteBuffer;
import java.nio.charset.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.*;
import java.util.logging.*;
import jdk.jfr.Recording;
import jdk.jfr.consumer.RecordingFile;

/** Bounded reference feasibility fixture, not the SDK process implementation. */
public final class ProcessProbe {
    static final int PIPE_LIMIT = 1048576;
    static Map<String,Object> object(Object... pairs) {
        Map<String,Object> map = new LinkedHashMap<>();
        for (int i=0;i<pairs.length;i+=2) map.put((String)pairs[i],pairs[i+1]);
        return map;
    }
    static void need(boolean value) { if (!value) throw new IllegalArgumentException("PROBE_INPUT"); }
    static String hash(byte[] bytes) throws Exception { return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes)); }
    static Map<String,Object> embedded(byte[] bytes) throws Exception {
        return object("available",true,"base64",Base64.getEncoder().encodeToString(bytes),"bytes",bytes.length,"sha256",hash(bytes));
    }
    static Object payload(String[] args) {
        List<Object> points=new ArrayList<>(); List<Integer> lengths=new ArrayList<>();
        need(args.length<=256); int total=0;
        for(String arg:args) { valid(arg); need(arg.indexOf(0)<0); total+=arg.length(); points.add(arg.codePoints().boxed().toList()); lengths.add(arg.length()); }
        need(total<=32768); return object("argv",args,"argvCodepoints",points,"argvUtf16Lengths",lengths);
    }
    static Object comparison(String[] requested,String[] observed) {
        List<Object> differences=new ArrayList<>();
        for(int i=0;i<Math.max(requested.length,observed.length);i++) {
            String wanted=i<requested.length?requested[i]:null,actual=i<observed.length?observed[i]:null;
            if(!Objects.equals(wanted,actual))differences.add(object("index",i,"requested",wanted,"observed",actual));
        }
        return object("roundTrip",differences.isEmpty(),"differences",differences);
    }
    static void valid(String value) {
        for(int i=0;i<value.length();i++) {
            char c=value.charAt(i);
            if(Character.isHighSurrogate(c)) need(++i<value.length()&&Character.isLowSurrogate(value.charAt(i)));
            else need(!Character.isLowSurrogate(c));
        }
    }
    @SuppressWarnings("unchecked") static Map<String,Object> map(Object value) { need(value instanceof Map); return (Map<String,Object>)value; }
    static String str(Object value) { need(value instanceof String); valid((String)value); return (String)value; }
    static long number(Object value) { need(value instanceof Long || value instanceof Integer); return ((Number)value).longValue(); }
    static String[] strings(Object value) { need(value instanceof List); return ((List<?>)value).stream().map(ProcessProbe::str).toArray(String[]::new); }
    static TreeMap<String,String> environment(Object value) {
        Map<String,Object> wire=map(value); need(wire.keySet().equals(Set.of("baseline","set","remove")));
        Map<String,Object> baseline=map(wire.get("baseline")); need(baseline.keySet().equals(Set.of("values")));
        Comparator<String> order=(a,b)->Arrays.compare(a.codePoints().toArray(),b.codePoints().toArray());
        TreeMap<String,String> env=new TreeMap<>(System.getProperty("os.name").startsWith("Windows")?String.CASE_INSENSITIVE_ORDER:order);
        for(Map<String,Object> source:List.of(map(baseline.get("values")))) apply(env,source,order);
        for(String name:strings(wire.get("remove"))) { name(name); env.remove(name); }
        apply(env,map(wire.get("set")),order); return env;
    }
    static void name(String key) { valid(key); need(!key.isEmpty()&&key.indexOf('=')<0&&key.indexOf(0)<0); }
    static void apply(Map<String,String> env,Map<String,Object> source,Comparator<String> order) {
        source.keySet().stream().sorted(order).forEach(key->{name(key);String val=str(source.get(key));need(val.indexOf(0)<0);env.remove(key);env.put(key,val);});
    }
    public static void main(String[] args) {
        try { System.exit(observe(args)); }
        catch(Exception error) { System.err.println("PROBE_INPUT_OR_IO_FAILURE"); System.exit(2); }
    }
    static int observe(String[] args) throws Exception {
        need(args.length>=5&&args[0].equals("--mode")&&args[2].equals("--request")&&args[4].equals("--"));
        String mode=args[1];need(Set.of("java-argv","javac-unicode","jdk-trace","jdk-jfr").contains(mode));
        Path requestPath=Path.of(args[3]);need(requestPath.isAbsolute()&&Files.size(requestPath)<=PIPE_LIMIT);
        byte[] raw=Files.readAllBytes(requestPath);Map<String,Object> request=map(Json.read(raw));
        need(str(request.get("schema")).equals("dotj.owned-process.request/1")&&str(request.get("mode")).equals(mode));
        need(str(request.get("engine")).equals("jdk-probe"));
        String platform=System.getProperty("os.name").startsWith("Windows")?"windows":"linux";
        need(str(request.get("platform")).equals(platform));
        String row=str(request.get("rowId"));need(row.equals(platform+(mode.equals("java-argv")||mode.equals("javac-unicode")?"-transport":"-telemetry-ownership")));
        String[] received=Arrays.copyOfRange(args,5,args.length);payload(received);payload(strings(request.get("argv")));
        Path cwd=Path.of(str(request.get("cwd")));need(cwd.isAbsolute()&&Files.isDirectory(cwd)&&!Files.isSymbolicLink(cwd));
        long millis=number(request.get("deadlineMillis"));need(millis>0&&millis<=120000);
        Map<String,Object> limits=map(request.get("limits"));need(number(limits.get("stdoutBytes"))==PIPE_LIMIT&&number(limits.get("stderrBytes"))==PIPE_LIMIT&&number(limits.get("stdinBytes"))==65536);
        Map<String,Object> stdin=map(request.get("stdin"));byte[] input=Base64.getDecoder().decode(str(stdin.get("base64")));
        need(input.length<=65536&&number(stdin.get("length"))==input.length&&hash(input).equals(str(stdin.get("sha256"))));
        Map<String,String> env=environment(request.get("environment"));
        need(!env.containsKey("JAVA_TOOL_OPTIONS")&&!env.containsKey("JDK_JAVA_OPTIONS")&&!env.containsKey("_JAVA_OPTIONS"));
        Map<String,Object> executable=map(request.get("executable"));Path selected=Path.of(str(executable.get("path")));
        need(selected.isAbsolute()&&hash(Files.readAllBytes(selected)).equals(str(executable.get("sha256"))));
        Map<String,String> before=new TreeMap<>(System.getenv());
        List<Object> operations=new ArrayList<>(), telemetry=new ArrayList<>(), errors=new ArrayList<>();
        long deadline=System.nanoTime()+TimeUnit.MILLISECONDS.toNanos(millis);
        Path classes=Path.of(ProcessProbe.class.getProtectionDomain().getCodeSource().getLocation().toURI());
        need(Files.isDirectory(classes));
        boolean windows=platform.equals("windows");String suffix=windows?".exe":"";
        Path java=selected.getParent().resolve("java"+suffix), javac=selected.getParent().resolve("javac"+suffix);
        need(selected.getFileName().toString().equals((mode.equals("javac-unicode")?"javac":"java")+suffix));
        verifyTool(request,java);if(mode.equals("javac-unicode"))verifyTool(request,javac);
        FileHandler trace=null;Logger logger=null;Level oldLevel=null;boolean oldParent=true;
        Recording recording=null;
        try {
            if(mode.equals("jdk-trace")) {
                logger=Logger.getLogger("java.lang.ProcessBuilder");oldLevel=logger.getLevel();oldParent=logger.getUseParentHandlers();
                trace=new FileHandler(cwd.resolve("trace.log").toString(),false);trace.setEncoding("UTF-8");trace.setFormatter(new SimpleFormatter());trace.setLevel(Level.ALL);
                logger.setUseParentHandlers(false);logger.setLevel(Level.FINEST);logger.addHandler(trace);
            }
            if(mode.equals("jdk-jfr")) { recording=new Recording();recording.enable("jdk.ProcessStart").withThreshold(Duration.ZERO);recording.start(); }
            String[] requested=strings(request.get("argv"));
            if(mode.equals("javac-unicode")) {
                Path source=cwd.resolve("UnicodeApp.java"), output=cwd.resolve("classes");Files.createDirectory(output);
                Files.writeString(source,"public class UnicodeApp { public static void main(String[] a) throws Exception { ProbeChild.main(a); } }\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE_NEW);
                List<String> command=new ArrayList<>();command.add(javac.toString());for(String flag:jvm())command.add("-J"+flag);
                command.addAll(List.of("--release","21","-encoding","UTF-8","-proc:none","-cp",classes.toString(),"-d",output.toString(),source.toString()));
                Map<String,Object> compile=run("native-javac",command,cwd,env,new byte[0],false,false,deadline);operations.add(compile);
                if(Objects.equals(compile.get("exitCode"),0)&&Files.isRegularFile(output.resolve("UnicodeApp.class")))
                    operations.add(run("compiled-application",childCommand(java,output+File.pathSeparator+classes,"UnicodeApp","echo",requested),cwd,env,input,false,true,deadline));
            } else {
                operations.add(run("argv-child",childCommand(java,classes.toString(),"ProbeChild","echo",requested),cwd,env,input,false,true,deadline));
                if(mode.equals("java-argv"))operations.add(run("wait-cancel-force",childCommand(java,classes.toString(),"ProbeChild","hold",new String[0]),cwd,env,new byte[0],true,true,deadline));
            }
        } catch(Exception error) { errors.add(object("category",error instanceof InterruptedException?"INTERRUPTED":"PROBE_OPERATION_FAILED","actorPid",ProcessHandle.current().pid())); }
        finally {
            if(trace!=null) { logger.removeHandler(trace);trace.close();logger.setLevel(oldLevel);logger.setUseParentHandlers(oldParent); }
            if(recording!=null) { try {recording.stop();recording.dump(cwd.resolve("recording.jfr"));}finally{recording.close();} }
        }
        if(mode.equals("jdk-trace")||mode.equals("jdk-jfr")) {
            Path file=cwd.resolve(mode.equals("jdk-trace")?"trace.log":"recording.jfr");byte[] data=Files.readAllBytes(file);
            need(data.length<=PIPE_LIMIT);String secret=str(map(request.get("secrets")).get("argv"));List<String> commands=new ArrayList<>();
            if(mode.equals("jdk-jfr"))try(RecordingFile fileReader=new RecordingFile(file)) {
                while(fileReader.hasMoreEvents()){var event=fileReader.readEvent();if(event.getEventType().getName().equals("jdk.ProcessStart"))commands.add(event.getString("command"));}
            }
            boolean exposed=mode.equals("jdk-trace")?new String(data,StandardCharsets.UTF_8).contains(secret):commands.stream().anyMatch(command->command.contains(secret));
            telemetry.add(object("path",file.getFileName().toString(),"bytes",data.length,"sha256",hash(data),"argvSecretExposed",exposed,"eventCommands",commands));
        }
        for(Object item:operations) {
            Map<String,Object> operation=map(item);
            if(!Set.of("EXITED","CANCELED").contains(operation.get("disposition")))errors.add(object("category",operation.get("disposition"),"actorPid",ProcessHandle.current().pid()));
        }
        int exit=errors.isEmpty()?0:1;
        Map<String,String> after=new TreeMap<>(System.getenv());need(before.equals(after));
        System.out.write((Json.write(object("schema","dotj.owned-process.jdk-probe-observation/1","rowId",row,
            "requestSha256",hash(raw),"mode",mode,"actor",object("kind","jdk-probe","pid",ProcessHandle.current().pid()),
            "receivedPayload",payload(received),"cwd",Path.of("").toAbsolutePath().toString(),"environment",object("values",System.getenv()),
            "transportComparison",comparison(strings(request.get("argv")),received),
            "parentEnvironmentBefore",before,"parentEnvironmentAfter",after,"operations",operations,"telemetry",telemetry,
            "errors",errors,"expectedOuterExitCode",exit))+"\n").getBytes(StandardCharsets.UTF_8));
        return exit;
    }
    static void verifyTool(Map<String,Object> request,Path tool) throws Exception {
        need(request.get("inputs") instanceof List);boolean verified=false;
        for(Object entry:(List<?>)request.get("inputs")) {
            Map<String,Object> descriptor=map(entry);
            if(Path.of(str(descriptor.get("path"))).equals(tool)) {
                byte[] bytes=Files.readAllBytes(tool);need(number(descriptor.get("bytes"))==bytes.length&&str(descriptor.get("sha256")).equals(hash(bytes)));verified=true;
            }
        }
        need(verified);
    }
    static List<String> jvm() {
        return List.of("-Xmx128m","-XX:ActiveProcessorCount=2","-XX:+UseSerialGC","-XX:ReservedCodeCacheSize=32m","-XX:-UsePerfData",
            "-Djava.io.tmpdir="+System.getProperty("java.io.tmpdir"),"-Duser.home="+System.getProperty("user.home"));
    }
    static List<String> childCommand(Path java,String classes,String main,String mode,String[] args) {
        List<String> command=new ArrayList<>();command.add(java.toString());command.addAll(jvm());
        command.addAll(List.of("-cp",classes,main,"--child-mode",mode));command.addAll(Arrays.asList(args));return command;
    }
    static final class Pipe implements Runnable {
        final InputStream stream;final ByteArrayOutputStream data=new ByteArrayOutputStream();volatile String error;volatile boolean terminal;
        Pipe(InputStream stream){this.stream=stream;}
        public void run(){try(stream){byte[] chunk=new byte[4096];for(int n;(n=stream.read(chunk))!=-1;){synchronized(data){if(data.size()+n>PIPE_LIMIT){error="OUTPUT_OVERFLOW";break;}data.write(chunk,0,n);}}}catch(IOException e){error="READ_FAILED";}finally{terminal=true;}}
        byte[] bytes(){synchronized(data){return data.toByteArray();}}
    }
    static long remaining(long deadline) { return Math.max(0,deadline-System.nanoTime()); }
    static void join(Thread worker,long deadline) throws InterruptedException { if(worker!=null&&remaining(deadline)>0)worker.join(Math.max(1,TimeUnit.NANOSECONDS.toMillis(remaining(deadline)))); }
    static Map<String,Object> run(String id,List<String> command,Path cwd,Map<String,String> env,byte[] input,boolean cancel,boolean childProtocol,long probeDeadline) throws Exception {
        long started=System.nanoTime(),deadline=Math.min(probeDeadline,started+TimeUnit.SECONDS.toNanos(20)),workEnd=deadline-TimeUnit.SECONDS.toNanos(5);
        need(remaining(workEnd)>0);int nativeBound=1;for(String arg:command){valid(arg);need(arg.indexOf(0)<0);nativeBound+=arg.length()*2+3;}
        if(System.getProperty("os.name").startsWith("Windows"))need(nativeBound<=30000);
        Process process=null;Pipe stdout=null,stderr=null;Thread outWorker=null,errWorker=null,inWorker=null;
        List<Object> events=new ArrayList<>();boolean futureCanceled=false,aliveAfterCancel=false,interrupted=false,observed=false;
        String disposition="EXITED",startIdentity=null;Integer exit=null;String[] inputError={null};boolean[] inputTerminal={false};long cleanupStart=0;
        try {
            ProcessBuilder builder=new ProcessBuilder(command).directory(cwd.toFile());builder.environment().clear();builder.environment().putAll(env);
            process=builder.start();events.add(object("kind","RETAINED","nanoTime",System.nanoTime()));
            startIdentity=process.info().startInstant().map(Object::toString).orElse(null);
            stdout=new Pipe(process.getInputStream());stderr=new Pipe(process.getErrorStream());
            outWorker=new Thread(stdout,"probe-stdout");errWorker=new Thread(stderr,"probe-stderr");outWorker.start();errWorker.start();
            OutputStream destination=process.getOutputStream();
            inWorker=new Thread(()->{try(destination){destination.write(input);destination.flush();}catch(IOException error){inputError[0]="WRITE_FAILED";}finally{inputTerminal[0]=true;}},"probe-stdin");inWorker.start();
            if(cancel) {
                while(stdout.bytes().length==0&&process.isAlive()&&remaining(workEnd)>0)Thread.sleep(5);
                need(stdout.bytes().length>0);var future=process.onExit();futureCanceled=future.cancel(true);aliveAfterCancel=process.isAlive();
                events.add(object("kind","WAIT_FUTURE_CANCELED","nanoTime",System.nanoTime(),"alive",aliveAfterCancel));disposition="CANCELED";
            } else {
                while(process.isAlive()&&remaining(workEnd)>0&&stdout.error==null&&stderr.error==null)process.waitFor(Math.min(50,Math.max(1,TimeUnit.NANOSECONDS.toMillis(remaining(workEnd)))),TimeUnit.MILLISECONDS);
                if(process.isAlive())disposition=stdout.error!=null||stderr.error!=null?"IO_FAILED":"TIMED_OUT";
            }
        } catch(InterruptedException error){interrupted=true;disposition="IO_FAILED";}
        catch(IOException error){disposition=process==null?"START_FAILED":"IO_FAILED";}
        catch(RuntimeException error){disposition="IO_FAILED";}
        finally {
            cleanupStart=System.nanoTime();
            if(process!=null) {
                try {
                    process.getOutputStream().close();
                    if(process.isAlive()){events.add(object("kind","DESTROY","nanoTime",System.nanoTime()));process.destroy();process.waitFor(Math.min(TimeUnit.SECONDS.toNanos(1),remaining(deadline)),TimeUnit.NANOSECONDS);}
                    if(process.isAlive()){events.add(object("kind","FORCE","nanoTime",System.nanoTime()));process.destroyForcibly();}
                    if(remaining(deadline)>0)observed=process.waitFor(remaining(deadline),TimeUnit.NANOSECONDS);
                    if(observed){exit=process.exitValue();events.add(object("kind","EXIT_OBSERVED","nanoTime",System.nanoTime()));}
                    join(inWorker,deadline);join(outWorker,deadline);join(errWorker,deadline);
                }catch(InterruptedException error){interrupted=true;disposition="CLEANUP_FAILED";process.destroyForcibly();}
                catch(IOException error){disposition="CLEANUP_FAILED";process.destroyForcibly();}
            }
        }
        boolean joined=inWorker!=null&&!inWorker.isAlive()&&outWorker!=null&&!outWorker.isAlive()&&errWorker!=null&&!errWorker.isAlive();
        if(!observed||!joined||System.nanoTime()>deadline)disposition="CLEANUP_FAILED";
        else if(inputError[0]!=null||stdout.error!=null||stderr.error!=null)disposition="IO_FAILED";
        Object child=null;byte[] out=stdout==null?null:stdout.bytes(),err=stderr==null?null:stderr.bytes();
        if(childProtocol&&out!=null) {
            try {Map<String,Object> value=map(Json.read(out));need(str(value.get("schema")).equals("dotj.owned-process.probe-child/1")&&number(value.get("pid"))==process.pid());
                String[] received=strings(map(value.get("receivedPayload")).get("argv"));need(Json.write(payload(received)).equals(Json.write(value.get("receivedPayload"))));child=value;
            }catch(Exception error){disposition="IO_FAILED";}
        }
        Map<String,Object> unavailable=object("available",false,"base64",null,"bytes",null,"sha256",null);
        Map<String,Object> result=object("id",id,"parentActorPid",ProcessHandle.current().pid(),"childPid",process==null?null:process.pid(),
            "invocation",object("executable",command.getFirst(),"argv",command.subList(1,command.size()),"cwd",cwd.toString(),"environment",object("baseline",object("values",env),"set",object(),"remove",List.of())),
            "disposition",disposition,"exitCode",exit,"handles",object("launchSlot",id,"pid",process==null?null:process.pid(),"startIdentity",startIdentity,
                "retained",process!=null,"events",events,"observedExit",observed,"exitCode",exit,"terminal",observed,"onExitFutureCanceled",futureCanceled,"aliveAfterFutureCancel",aliveAfterCancel),
            "workers",object("stdin",object("started",inWorker!=null,"closed",inputTerminal[0],"terminal",inputTerminal[0],"joined",inWorker!=null&&!inWorker.isAlive(),"errorCategory",inputError[0]),
                "stdout",worker(stdout,outWorker),"stderr",worker(stderr,errWorker)),
            "timing",object("startNanos",started,"endNanos",System.nanoTime(),"deadlineNanos",deadline,"cleanupStartNanos",cleanupStart,"cleanupReserveMillis",5000),
            "streams",object("stdout",out==null?unavailable:embedded(out),"stderr",err==null?unavailable:embedded(err)),"childObservation",child);
        if(child!=null) {
            int payloadStart=command.indexOf("--child-mode")+2;
            result.put("transportComparison",comparison(command.subList(payloadStart,command.size()).toArray(String[]::new),strings(map(map(child).get("receivedPayload")).get("argv"))));
        }
        if(interrupted)Thread.currentThread().interrupt();return result;
    }
    static Object worker(Pipe pipe,Thread thread){return object("started",thread!=null,"closed",pipe!=null&&pipe.terminal,"terminal",pipe!=null&&pipe.terminal,"joined",thread!=null&&!thread.isAlive(),"errorCategory",pipe==null?null:pipe.error);}
    /** Small strict wire codec shared with the child; no general JSON library. */
    static final class Json {
        final String source; int cursor;
        Json(String source) { this.source=source; }
        static Object read(byte[] raw) throws Exception {
            String decoded=StandardCharsets.UTF_8.newDecoder().onMalformedInput(CodingErrorAction.REPORT).decode(ByteBuffer.wrap(raw)).toString();
            Json parser=new Json(decoded);Object value=parser.value(0);parser.space();need(parser.cursor==decoded.length());return value;
        }
        void space(){while(cursor<source.length()&&" \n\r\t".indexOf(source.charAt(cursor))>=0)cursor++;}
        char take(){need(cursor<source.length());return source.charAt(cursor++);}
        Object value(int depth) {
            need(depth<=32);space();char c=take();
            if(c=='"')return quoted();
            if(c=='{') { Map<String,Object> out=new LinkedHashMap<>();space();if(cursor<source.length()&&source.charAt(cursor)=='}'){cursor++;return out;}
                do {space();need(take()=='"');String key=quoted();need(!out.containsKey(key));space();need(take()==':');out.put(key,value(depth+1));space();c=take();if(c=='}')return out;need(c==',');}while(true); }
            if(c=='[') { List<Object> out=new ArrayList<>();space();if(cursor<source.length()&&source.charAt(cursor)==']'){cursor++;return out;}
                do {out.add(value(depth+1));space();c=take();if(c==']')return out;need(c==',');}while(true); }
            for(String literal:List.of("true","false","null")) if(c==literal.charAt(0)&&source.startsWith(literal,cursor-1)){cursor+=literal.length()-1;return literal.equals("null")?null:literal.equals("true");}
            int start=cursor-1;while(cursor<source.length()&&"0123456789.eE+-".indexOf(source.charAt(cursor))>=0)cursor++;
            String token=source.substring(start,cursor);need(token.matches("-?(0|[1-9][0-9]*)"));return Long.parseLong(token);
        }
        String quoted(){StringBuilder out=new StringBuilder();while(true){char c=take();if(c=='"'){valid(out.toString());return out.toString();}need(c>=32);if(c=='\\'){c=take();switch(c){case '"','\\','/'->out.append(c);case 'b'->out.append('\b');case 'f'->out.append('\f');case 'n'->out.append('\n');case 'r'->out.append('\r');case 't'->out.append('\t');case 'u'->{need(cursor+4<=source.length());out.append((char)Integer.parseInt(source.substring(cursor,cursor+4),16));cursor+=4;}default->throw new IllegalArgumentException();}}else out.append(c);}}
        static String write(Object value){
            if(value==null)return "null";if(value instanceof Boolean||value instanceof Number)return value.toString();
            if(value instanceof String s){valid(s);StringBuilder out=new StringBuilder("\"");for(char c:s.toCharArray()){switch(c){case '"'->out.append("\\\"");case '\\'->out.append("\\\\");case '\n'->out.append("\\n");case '\r'->out.append("\\r");case '\t'->out.append("\\t");default->{if(c<32||c>126)out.append(String.format(Locale.ROOT,"\\u%04x",(int)c));else out.append(c);}}}return out.append('"').toString();}
            if(value instanceof Map<?,?> m){List<String> values=new ArrayList<>();for(var e:m.entrySet())values.add(write(e.getKey())+":"+write(e.getValue()));return "{"+String.join(",",values)+"}";}
            if(value instanceof Object[] a)return write(Arrays.asList(a));
            if(value instanceof Collection<?> a)return "["+String.join(",",a.stream().map(Json::write).toList())+"]";
            throw new IllegalArgumentException();
        }
    }
}
