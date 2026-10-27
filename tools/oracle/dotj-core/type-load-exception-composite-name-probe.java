import System.Type;
import System.TypeLoadException;
import System.Exception;
import java.nio.file.*;
import java.util.*;
class TypeLoadExceptionCompositeNameProbe {
    static String units(String text) { if (text == null) return "~"; StringJoiner csv = new StringJoiner(","); for (char value : text.toCharArray()) csv.add(Integer.toString(value)); return csv.toString(); }
    static String text(String csv) { if (csv.equals("~")) return null; StringBuilder text = new StringBuilder(); if (!csv.isEmpty()) for (String value : csv.split(",")) text.append((char)Integer.parseInt(value)); return text.toString(); }
    static void check(String actual, String expected, String context) { if (!actual.equals(expected)) throw new AssertionError(context + ": actual=" + actual + " expected=" + expected); }
    public static void main(String[] args) throws java.lang.Exception {
        int calls = 0, groups = 0;
        for (String line : Files.readAllLines(Path.of(args[0]))) {
            String[] p = line.split("\t", -1);
            if (p[0].equals("C")) {
                Exception inner = p[3].equals("plain") ? new Exception() : p[3].equals("named") ? new Exception("inner") : null;
                TypeLoadException value = p[1].equals("default") ? new TypeLoadException() : p[1].equals("message") ? new TypeLoadException(text(p[2])) : new TypeLoadException(text(p[2]), inner);
                check(units(value.get_Message()), p[4], line); check(units(value.get_TypeName()), p[5], "TypeName " + line);
                check(Integer.toString(value.get_HResult()), p[6], "HResult " + line);
                check(value.get_InnerException() == inner ? "1" : "0", p[7], "Inner reference " + line);
                calls++; groups += 4;
            } else {
                try { Type.GetType(text(p[1]), true, p[2].equals("1")); throw new AssertionError("Missing lookup succeeded: " + line); }
                catch (TypeLoadException expected) {
                    check(units(expected.get_TypeName()), p[3], line); check(Integer.toString(expected.get_HResult()), p[4], "lookup HResult " + line);
                }
                calls++; groups += 2;
            }
        }
        if (TypeLoadException.class.getDeclaredMethod("get_Message").getReturnType() != String.class
                || TypeLoadException.class.getDeclaredMethod("get_TypeName").getReturnType() != String.class) throw new AssertionError("Declared getters");
        java.lang.System.out.println("PASS TypeLoadException getters calls=" + calls + " groups=" + groups + " declaredControls=2");
    }
}
