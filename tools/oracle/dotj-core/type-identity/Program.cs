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

Type listOfInt = typeof(List<int>);
Type listOfLong = typeof(List<long>);
Type reconstructedListOfInt = typeof(List<>).MakeGenericType(typeof(int));
Check(ReferenceEquals(listOfInt, reconstructedListOfInt), "second generic definition canonical identity");
Check(!ReferenceEquals(listOfInt, listOfLong), "second generic definition different argument identity");
Check(listOfInt.GetGenericTypeDefinition() == listOfLong.GetGenericTypeDefinition(), "second generic definition shared definition");

Console.WriteLine("sameReference=" + ReferenceEquals(first, same));
Console.WriteLine("runtimeVersion=" + Environment.Version);
Console.WriteLine("constructedEqual=" + first.Equals(constructed));
Console.WriteLine("differentArgumentEqual=" + first.Equals(different));
Console.WriteLine("sameGenericDefinition=" + (first.GetGenericTypeDefinition() == different.GetGenericTypeDefinition()));
Console.WriteLine("secondDefinitionCanonical=" + ReferenceEquals(listOfInt, reconstructedListOfInt));
Console.WriteLine("secondDefinitionDifferentArgumentsSameReference=" + ReferenceEquals(listOfInt, listOfLong));

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
