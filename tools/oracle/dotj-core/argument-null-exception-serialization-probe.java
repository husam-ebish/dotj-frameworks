import System.Exception;
import System.ArgumentNullException;
import System.Int32;
import System.Type;
import System.ArgumentNullException;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class ArgumentNullExceptionSerializationProbe {
    static String units(String text) { if (text == null) return "~"; StringJoiner csv = new StringJoiner(","); for (char value : text.toCharArray()) csv.add(Integer.toString(value)); return csv.toString(); }
    static String text(String csv) { if (csv.equals("~")) return null; StringBuilder text = new StringBuilder(); if (!csv.isEmpty()) for (String value : csv.split(",")) text.append((char)Integer.parseInt(value)); return text.toString(); }
    static void check(String actual, String expected, String context) { if (!actual.equals(expected)) throw new AssertionError(context + ": actual=" + actual + " expected=" + expected); }
    static Exception create(String family, String route, String message, String file, Exception inner) {
        if (family.equals("base")) return route.equals("default") ? new Exception() : route.equals("message") ? new Exception(message) : new Exception(message, inner);
        return switch (route) {
            case "default" -> new ArgumentNullException(); case "message" -> new ArgumentNullException(message);
            case "inner" -> new ArgumentNullException(message, inner); case "file" -> new ArgumentNullException(file, message);
 default -> throw new AssertionError(route);
        };
    }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0, groups = 0; Exception inner = null; SerializationInfoEnumerator enumerator = null;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1);
            if (p[0].equals("S")) {
                inner = p[5].equals("plain") ? new Exception() : p[5].equals("named") ? new Exception("inner") : null;
                Exception value = create(p[1], p[2], text(p[3]), text(p[4]), inner);
                if (p[7].equals("1")) value.get_Message();
                SerializationInfo info = new SerializationInfo(Type.GetType(p[1].equals("base") ? "System.Exception" : "System.ArgumentNullException"), new FormatterConverter());
                value.GetObjectData(info, new StreamingContext(StreamingContextStates.FromInt32(Integer.parseInt(p[6]))));
                check(Integer.toString(info.get_MemberCount()), p[8], line); enumerator = info.GetEnumerator(); calls++; groups++;
            } else if (p[0].equals("E")) {
                if (!enumerator.MoveNext()) throw new AssertionError("Missing entry: " + line);
                SerializationEntry entry = enumerator.get_Current(); check(entry.get_Name(), p[1], line);
                check(entry.get_ObjectType().get_FullName(), p[2], "declared type " + line);
                Object value = entry.get_Value(); String actual;
                if (value == null) actual = "null|~";
                else if (value == inner) actual = "inner|~";
                else if (value instanceof String string) actual = "text|" + units(string);
                else if (value instanceof Int32 number) actual = "int|" + number.get_Value();
                else if (value instanceof java.lang.Integer number) actual = "int|" + number;
                else throw new AssertionError("Unexpected value carrier: " + value.getClass());
                check(actual, p[3] + "|" + p[4], "entry value " + line); groups += 3;
            } else {
                Exception value = create(p[1], "default", null, null, null);
                try { value.GetObjectData(null, new StreamingContext(StreamingContextStates.FromInt32(Integer.parseInt(p[2])))); throw new AssertionError("Null info accepted"); }
                catch (ArgumentNullException expected) {
                    check(expected.getClass().getName(), p[3], line); check(units(expected.get_Message()), p[4], line);
                    check(Integer.toString(expected.get_HResult()), p[5], line); check(units(expected.get_ParamName()), p[6], line);
                }
                calls++; groups += 4;
            }
        }
        java.lang.System.out.println("PASS exception/file serialization calls=" + calls + " groups=" + groups);
    }
}
