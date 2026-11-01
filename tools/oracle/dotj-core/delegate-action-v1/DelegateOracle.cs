// Native side of the selected System.Action behavior. DelegateFixtures.java prints the same keys.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

internal static class DelegateOracle
{
    private static readonly List<string> Lines = new();
    private static readonly List<string> Log = new();

    private static void Record(string key, object? value) =>
        Lines.Add(key + "=" + (value is bool flag ? (flag ? "true" : "false") : value));
    private static void BodyA() => Log.Add("a");
    private static void BodyB() => Log.Add("b");
    private static void BodyC() => Log.Add("c");
    private static void Boom() => throw new InvalidOperationException("boom");

    private static string Run(Action? action)
    {
        Log.Clear();
        if (action == null)
        {
            return "null";
        }
        action.Invoke();
        return string.Join(",", Log);
    }

    private static int Main(string[] arguments)
    {
        Action a = new(BodyA), b = new(BodyB), c = new(BodyC);
        Record("single", Run(a));
        Record("combine", Run((Action?)Delegate.Combine(a, b)));
        Record("combineNullLeftSame", ReferenceEquals(Delegate.Combine(null, a), a));
        Record("combineNullRightSame", ReferenceEquals(Delegate.Combine(a, null), a));
        Record("combineBothNull", Delegate.Combine(null, null) == null);
        Record("combineArray", Run((Action?)Delegate.Combine(new Delegate?[] { a, null, b, c })));
        Record("combineEmptyArray", Delegate.Combine(Array.Empty<Delegate>()) == null);
        Record("combineNullArray", Delegate.Combine((Delegate[]?)null) == null);

        var abc = (Action)Delegate.Combine(a, b, c)!;
        Record("listLength", abc.GetInvocationList().Length);
        Record("listIdentity", ReferenceEquals(abc.GetInvocationList()[1], b));
        Record("listFresh", !ReferenceEquals(abc.GetInvocationList(), abc.GetInvocationList()));
        Record("singleListSelf", ReferenceEquals(a.GetInvocationList()[0], a));
        Record("listMutationIgnored", MutateList(abc));

        var abab = (Action)Delegate.Combine(a, b, a, b)!;
        Record("removeLast", Run((Action?)Delegate.Remove(abab, b)));
        Record("removeGroup", Run((Action?)Delegate.Remove(abab, Delegate.Combine(a, b))));
        Record("removeMiddleGroup", Run((Action?)Delegate.Remove(abc, Delegate.Combine(a, c))));
        Record("removeAbsentSame", ReferenceEquals(Delegate.Remove(abc, new Action(Boom)), abc));
        Record("removeToSingleSame", ReferenceEquals(Delegate.Remove(Delegate.Combine(a, b), a), b));
        Record("removeToNull", Delegate.Remove(a, a) == null);
        Record("removeEqualNotSame", Delegate.Remove(a, new Action(BodyA)) == null);
        Record("removeNullSource", Delegate.Remove(null, a) == null);
        Record("removeNullValueSame", ReferenceEquals(Delegate.Remove(a, null), a));
        Record("removeAll", Run((Action?)Delegate.RemoveAll(Delegate.Combine(a, b, a, c, a), a)));
        Record("removeAllToNull", Delegate.RemoveAll(Delegate.Combine(a, a), a) == null);
        Record("originalUnchanged", Run(abab));

        Record("equalSameMethod", a.Equals(new Action(BodyA)));
        Record("hashSameMethod", a.GetHashCode() == new Action(BodyA).GetHashCode());
        Record("equalDifferent", a.Equals(b));
        Record("equalNull", a.Equals(null));
        Record("equalCombined", Delegate.Combine(a, b)!.Equals(Delegate.Combine(new Action(BodyA), new Action(BodyB))));
        Record("hashCombined", Delegate.Combine(a, b)!.GetHashCode() == Delegate.Combine(new Action(BodyA), new Action(BodyB))!.GetHashCode());
        Record("equalOrderMatters", Delegate.Combine(a, b)!.Equals(Delegate.Combine(b, a)));

        Log.Clear();
        var failing = (Action)Delegate.Combine(a, new Action(Boom), b)!;
        try
        {
            failing.Invoke();
            Record("failure", "none");
        }
        catch (InvalidOperationException error)
        {
            Record("failure", error.Message);
        }
        Record("failureStopped", string.Join(",", Log));
        Record("runtime", Environment.Version);
        File.WriteAllLines(arguments[0], Lines);
        return 0;
    }

    private static string MutateList(Action action)
    {
        Delegate[] list = action.GetInvocationList();
        list[0] = list[1];
        return Run(action);
    }
}
