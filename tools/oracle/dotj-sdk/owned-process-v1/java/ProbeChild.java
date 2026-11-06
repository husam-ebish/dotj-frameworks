import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.Arrays;

/** Development-only child: observations come from this VM, never request.json. */
public final class ProbeChild {
    public static void main(String[] args) throws Exception {
        if (args.length < 2 || !args[0].equals("--child-mode") ||
                !args[1].equals("echo") && !args[1].equals("hold")) System.exit(2);
        ByteArrayOutputStream input = new ByteArrayOutputStream();
        byte[] chunk = new byte[4096];
        for (int n; (n = System.in.read(chunk)) != -1;) {
            if (input.size() + n > 65536) System.exit(2);
            input.write(chunk, 0, n);
        }
        var observation = ProcessProbe.object("schema", "dotj.owned-process.probe-child/1",
                "pid", ProcessHandle.current().pid(), "receivedPayload", ProcessProbe.payload(Arrays.copyOfRange(args, 2, args.length)),
                "cwd", Path.of("").toAbsolutePath().toString(), "environment", ProcessProbe.object("values", System.getenv()),
                "stdin", ProcessProbe.embedded(input.toByteArray()));
        System.out.write((ProcessProbe.Json.write(observation) + "\n").getBytes(StandardCharsets.UTF_8));
        System.out.flush();
        if (args[1].equals("hold")) Thread.sleep(10000);
    }
}
