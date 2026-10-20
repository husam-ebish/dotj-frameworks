package consumer;

import System.Type;
import System.ArgumentNullException;
import System.ArgumentException;
import System.TypeLoadException;
import System.IO.FileNotFoundException;
import System.IO.IOException;

/** Calls the candidate's public members from outside the System package. */
public final class ProductTypeIdentityConsumer {
    public static void main(String[] args) {
        Type definition = Type.GetType("System.Collections.Generic.List`1");
        Type string = Type.GetType("System.String");
        Type integer = Type.GetType("System.Int32");
        if (definition == null || string == null || integer == null
                || Type.GetType("System.Unknown") != null) {
            throw new AssertionError("Selected type-name lookup changed");
        }
        if (Type.GetType("system.string", false, true) != string
                || Type.GetType("system.string", false) != null
                || Type.GetType("System.Unknown", false, true) != null
                || Type.GetType("System.String", true) != string) {
            throw new AssertionError("Selected GetType overload behavior changed");
        }
        if (Type.GetType("System.String, System.Private.CoreLib") != string
                || Type.GetType("System.Int32, System.Private.CoreLib") != integer
                || Type.GetType("System.String, mscorlib") != string
                || Type.GetType("System.String, NotAnAssembly") != null) {
            throw new AssertionError("Selected assembly-qualified lookup changed");
        }
        if (Type.GetType("") != null || Type.GetType(" System.String") != string
                || Type.GetType("System.String ") != null
                || Type.GetType("System.String , System.Private.CoreLib") != null
                || Type.GetType("System.String, ") != null) {
            throw new AssertionError("Selected type-name boundary behavior changed");
        }
        try {
            Type.GetType("System.String, ", true);
            throw new AssertionError("Empty assembly accepted with throwOnError");
        } catch (ArgumentException expected) {
            if (!"typeName@13".equals(expected.get_ParamName())) {
                throw new AssertionError("Empty assembly parameter changed", expected);
            }
        }
        try {
            Type.GetType("System.String, NotAnAssembly", true);
            throw new AssertionError("Missing assembly accepted with throwOnError");
        } catch (FileNotFoundException expected) {
            if (!(expected instanceof IOException)) {
                throw new AssertionError("Missing assembly exception hierarchy changed", expected);
            }
        }
        try {
            Type.GetType("System.Unknown", true, false);
            throw new AssertionError("Missing type accepted with throwOnError");
        } catch (TypeLoadException expected) {
            // Selected error type observed from pinned CoreLib.
        }
        try {
            Type.GetType(null);
            throw new AssertionError("Null type name accepted");
        } catch (ArgumentNullException expected) {
            if (!"typeName".equals(expected.get_ParamName())) {
                throw new AssertionError("Public exception parameter changed", expected);
            }
        }
        Type first = definition.MakeGenericType(new Type[] {string});
        Type dictionary = Type.GetType("System.Collections.Generic.Dictionary`2");
        Type dictionaryStringInt = dictionary.MakeGenericType(new Type[] {string, integer});
        if (Type.GetType("System.Collections.Generic.Dictionary`2[System.String,System.Int32]")
                    != dictionaryStringInt
                || Type.GetType("System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Int32, System.Private.CoreLib]]")
                    != dictionaryStringInt
                || Type.GetType("System.Collections.Generic.Dictionary`2[System.Int32,System.String]")
                    != dictionary.MakeGenericType(new Type[] {integer, string})) {
            throw new AssertionError("Selected Dictionary name lookup changed");
        }
        if (Type.GetType("System.String[]") == null
                || Type.GetType("System.String[]") != Type.GetType("system.string[]", false, true)
                || Type.GetType("System.String[], System.Private.CoreLib") != Type.GetType("System.String[]")
                || Type.GetType("System.Int32[]") == null
                || Type.GetType("System.Collections.Generic.List`1[System.String]") != first
                || Type.GetType("System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]]") != first) {
            throw new AssertionError("Selected array or generic type-name lookup changed");
        }
        Type jagged = Type.GetType("System.String[][]");
        if (jagged == null || jagged == Type.GetType("System.String[]")
                || jagged != Type.GetType("system.string[][]", false, true)) {
            throw new AssertionError("Selected jagged array identity changed");
        }
        Type rectangular = Type.GetType("System.String[,]");
        Type rankThree = Type.GetType("System.String[,,]");
        Type listArray = Type.GetType("System.Collections.Generic.List`1[System.String][]");
        if (rectangular == null || rankThree == null || listArray == null
                || rectangular == rankThree || rectangular == jagged
                || rectangular == Type.GetType("System.String[]")
                || rectangular != Type.GetType("System.String[,]")
                || rankThree != Type.GetType("system.string[,,]", false, true)
                || listArray != Type.GetType("System.Collections.Generic.List`1[System.String][]")
                || listArray.get_IsGenericType()) {
            throw new AssertionError("Selected CLR array-shape identity changed");
        }
        Type same = definition.MakeGenericType(new Type[] {string});
        Type different = definition.MakeGenericType(new Type[] {integer});
        if (first != same || !first.Equals(same) || first.Equals(different)
                || first.GetGenericTypeDefinition() != definition
                || first.GetGenericArguments()[0] != string
                || first.get_GenericTypeArguments()[0] != string
                || !first.get_IsConstructedGenericType() || !definition.get_IsGenericType()) {
            throw new AssertionError("External Type identity call changed");
        }
        Type parameter = definition.GetGenericArguments()[0];
        if (!parameter.get_IsGenericParameter() || parameter.get_GenericParameterPosition() != 0
                || parameter != definition.GetGenericArguments()[0]) {
            throw new AssertionError("External generic parameter identity changed");
        }
        java.lang.System.out.println("PASS external System.Type selected identity consumer");
    }
}
