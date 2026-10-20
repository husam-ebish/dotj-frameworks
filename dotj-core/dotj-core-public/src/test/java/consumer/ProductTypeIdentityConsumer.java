package consumer;

import System.Type;
import System.ArgumentNullException;
import System.TypeLoadException;

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
