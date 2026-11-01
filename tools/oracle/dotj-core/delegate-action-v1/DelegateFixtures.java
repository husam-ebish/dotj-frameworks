import System.Action;
import System.Delegate;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.dotj.internal.delegates.ActionBody;

/** Public consumer side of the selected System.Action behavior; compiled only against the candidate. */
public final class DelegateFixtures {
    private static final List<String> LINES = new ArrayList<>();
    private static final List<String> LOG = new ArrayList<>();
    private static final ActionBody BODY_A = () -> LOG.add("a"), BODY_B = () -> LOG.add("b"), BODY_C = () -> LOG.add("c");
    private static final ActionBody BOOM = () -> { throw new IllegalStateException("boom"); };

    private static void record(String key, Object value) { LINES.add(key + "=" + value); }

    private static String run(Delegate action) {
        LOG.clear();
        if (action == null) {
            return "null";
        }
        ((Action) action).Invoke();
        return String.join(",", LOG);
    }

    public static void main(String[] arguments) throws Exception {
        Action a = new Action(BODY_A), b = new Action(BODY_B), c = new Action(BODY_C);
        record("single", run(a));
        record("combine", run(Delegate.Combine(a, b)));
        record("combineNullLeftSame", Delegate.Combine(null, a) == a);
        record("combineNullRightSame", Delegate.Combine(a, null) == a);
        record("combineBothNull", Delegate.Combine((Delegate) null, (Delegate) null) == null);
        record("combineArray", run(Delegate.Combine(new Delegate[] {a, null, b, c})));
        record("combineEmptyArray", Delegate.Combine(new Delegate[0]) == null);
        record("combineNullArray", Delegate.Combine((Delegate[]) null) == null);

        Delegate abc = Delegate.Combine(a, b, c);
        record("listLength", abc.GetInvocationList().length);
        record("listIdentity", abc.GetInvocationList()[1] == b);
        record("listFresh", abc.GetInvocationList() != abc.GetInvocationList());
        record("singleListSelf", a.GetInvocationList()[0] == a);
        Delegate[] list = abc.GetInvocationList();
        list[0] = list[1];
        record("listMutationIgnored", run(abc));

        Delegate abab = Delegate.Combine(a, b, a, b);
        record("removeLast", run(Delegate.Remove(abab, b)));
        record("removeGroup", run(Delegate.Remove(abab, Delegate.Combine(a, b))));
        record("removeMiddleGroup", run(Delegate.Remove(abc, Delegate.Combine(a, c))));
        record("removeAbsentSame", Delegate.Remove(abc, new Action(BOOM)) == abc);
        record("removeToSingleSame", Delegate.Remove(Delegate.Combine(a, b), a) == b);
        record("removeToNull", Delegate.Remove(a, a) == null);
        record("removeEqualNotSame", Delegate.Remove(a, new Action(BODY_A)) == null);
        record("removeNullSource", Delegate.Remove(null, a) == null);
        record("removeNullValueSame", Delegate.Remove(a, null) == a);
        record("removeAll", run(Delegate.RemoveAll(Delegate.Combine(a, b, a, c, a), a)));
        record("removeAllToNull", Delegate.RemoveAll(Delegate.Combine(a, a), a) == null);
        record("originalUnchanged", run(abab));

        record("equalSameMethod", a.Equals(new Action(BODY_A)));
        record("hashSameMethod", a.GetHashCode() == new Action(BODY_A).GetHashCode());
        record("equalDifferent", a.Equals(b));
        record("equalNull", a.Equals(null));
        record("equalCombined", Delegate.Combine(a, b).Equals(Delegate.Combine(new Action(BODY_A), new Action(BODY_B))));
        record("hashCombined", Delegate.Combine(a, b).GetHashCode() == Delegate.Combine(new Action(BODY_A), new Action(BODY_B)).GetHashCode());
        record("equalOrderMatters", Delegate.Combine(a, b).Equals(Delegate.Combine(b, a)));

        LOG.clear();
        Action failing = (Action) Delegate.Combine(a, new Action(BOOM), b);
        try {
            failing.Invoke();
            record("failure", "none");
        } catch (IllegalStateException error) {
            record("failure", error.getMessage());
        }
        record("failureStopped", String.join(",", LOG));
        Files.write(Path.of(arguments[0]), LINES);
    }
}
