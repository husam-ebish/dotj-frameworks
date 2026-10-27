import System.IO.FileNotFoundException;
import System.Exception;
import java.nio.file.*;
import java.util.*;
class FileNotFoundExceptionRenderingProbe {
    static String units(String text) { if (text == null) return "~"; StringJoiner csv = new StringJoiner(","); for (char value : text.toCharArray()) csv.add(Integer.toString(value)); return csv.toString(); }
    static String text(String csv) { if (csv.equals("~")) return null; StringBuilder text = new StringBuilder(); if (!csv.isEmpty()) for (String value : csv.split(",")) text.append((char)Integer.parseInt(value)); return text.toString(); }
    static void check(String actual, String expected, String context) { if (!actual.equals(expected)) throw new AssertionError(context + ": actual=" + actual + " expected=" + expected); }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1); String message = text(p[1]), file = text(p[2]);
            Exception inner = p[3].equals("plain") ? new Exception() : p[3].equals("named") ? new Exception("inner") : null;
            FileNotFoundException value = switch (p[0]) {
                case "default" -> new FileNotFoundException();
                case "message" -> new FileNotFoundException(message);
                case "inner" -> new FileNotFoundException(message, inner);
                case "file" -> new FileNotFoundException(message, file);
                case "file-inner" -> new FileNotFoundException(message, file, inner);
                default -> throw new AssertionError(p[0]);
            };
            check(units(value.get_Message()), p[4], line); check(units(value.get_FileName()), p[5], "FileName " + line);
            check(units(value.get_FusionLog()), p[6], "FusionLog " + line); check(Integer.toString(value.get_HResult()), p[7], "HResult " + line);
            check(value.get_InnerException() == inner ? "1" : "0", p[8], "Inner reference " + line); check(units(value.ToString()), p[9], "ToString " + line);
            calls++;
        }
        java.lang.System.out.println("PASS FileNotFoundException rendering calls=" + calls + " groups=" + (6 * calls));
    }
}
