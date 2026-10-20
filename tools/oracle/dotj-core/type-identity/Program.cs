using System.Collections.Generic;

Type first = typeof(Dictionary<string, int>);
Type same = typeof(Dictionary<string, int>);
Type different = typeof(Dictionary<string, long>);
Type constructed = typeof(Dictionary<,>).MakeGenericType(typeof(string), typeof(int));

Check(first.IsConstructedGenericType, "closed generic form");
Check(ReferenceEquals(first, same), "repeated closed type identity");
Check(first.Equals(constructed), "reflection construction equality");
Check(!first.Equals(different), "different argument identity");
Check(first.GetGenericTypeDefinition() == different.GetGenericTypeDefinition(), "generic definition");

Console.WriteLine("sameReference=" + ReferenceEquals(first, same));
Console.WriteLine("runtimeVersion=" + Environment.Version);
Console.WriteLine("constructedEqual=" + first.Equals(constructed));
Console.WriteLine("differentArgumentEqual=" + first.Equals(different));
Console.WriteLine("sameGenericDefinition=" + (first.GetGenericTypeDefinition() == different.GetGenericTypeDefinition()));

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
