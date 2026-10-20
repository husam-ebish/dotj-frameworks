package consumer;

import System.Type;
import System.TypeCandidateFactory;
import java.util.List;

/** Calls the candidate's public members from outside the System package. */
public final class ProductTypeIdentityConsumer {
    public static void main(String[] args) {
        Type definition = TypeCandidateFactory.Of(List.class);
        Type string = TypeCandidateFactory.Of(String.class);
        Type integer = TypeCandidateFactory.Of(Integer.class);
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
        java.lang.System.out.println("PASS external System.Type selected identity consumer");
    }
}
