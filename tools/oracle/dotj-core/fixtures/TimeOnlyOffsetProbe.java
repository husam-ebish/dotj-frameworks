import System.DateTime;
import System.DateTimeKind;
import System.IFormattable;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HexFormat;

/** Packaged consumer; inputs and all transient output are supplied on D:. */
public class TimeOnlyOffsetProbe {
    private static void add(ArrayList<String> output, String id, String route, String value) {
        output.add(id + "\t" + route + "\t" + Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8)));
    }

    public static void main(String[] arguments) throws Exception {
        ArrayList<String> output = new ArrayList<>();
        output.add("ZONE\t" + java.time.ZoneId.systemDefault().getId());
        for (String line : Files.readAllLines(Path.of(arguments[0]), StandardCharsets.UTF_8)) {
            String[] fields = line.split("\t", -1);
            DateTime value = new DateTime(Long.parseLong(fields[1]), switch (fields[2]) {
                case "Utc" -> DateTimeKind.Utc;
                case "Local" -> DateTimeKind.Local;
                default -> DateTimeKind.Unspecified;
            });
            String format = new String(Base64.getDecoder().decode(fields[3]), StandardCharsets.UTF_8);
            add(output, fields[0], "provider", value.ToString(format, null));
            add(output, fields[0], "single", value.ToString(format));
            add(output, fields[0], "interface", ((IFormattable) value).ToString(format, null));
            char[] chars = new char[64];
            java.util.Arrays.fill(chars, '#');
            int[] written = {99};
            boolean success = value.TryFormat(chars, written, format, null);
            add(output, fields[0], "Char", success + "|" + written[0] + "|" + new String(chars));
            byte[] bytes = new byte[64];
            java.util.Arrays.fill(bytes, (byte) 35);
            written[0] = 99;
            success = value.TryFormat(bytes, written, format, null);
            add(output, fields[0], "Utf8", success + "|" + written[0] + "|" + HexFormat.of().withUpperCase().formatHex(bytes));
        }
        Files.write(Path.of(arguments[1]), output, StandardCharsets.UTF_8);
    }
}
