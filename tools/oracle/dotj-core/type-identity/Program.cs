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
Check(ReferenceEquals(Type.GetType("System.String"), typeof(string)), "string type-name lookup");
Check(ReferenceEquals(Type.GetType("System.Int32"), typeof(int)), "int type-name lookup");
Check(ReferenceEquals(Type.GetType("System.Collections.Generic.List`1"), typeof(List<>)), "list definition lookup");
Check(ReferenceEquals(Type.GetType("System.Collections.Generic.Dictionary`2"), typeof(Dictionary<,>)), "dictionary definition lookup");
Check(Type.GetType("System.Unknown") is null, "unknown type-name lookup");

string? nullTypeArgumentsParameter = null;
try
{
    typeof(List<>).MakeGenericType((Type[])null!);
    throw new Exception("Null type arguments were accepted.");
}
catch (ArgumentNullException exception)
{
    nullTypeArgumentsParameter = exception.ParamName;
}
Check(nullTypeArgumentsParameter == "typeArguments", "null type argument parameter identity");

string? nullTypeNameParameter = null;
try
{
    Type.GetType(null!);
    throw new Exception("Null type name was accepted.");
}
catch (ArgumentNullException exception)
{
    nullTypeNameParameter = exception.ParamName;
}
Check(nullTypeNameParameter == "typeName", "null type-name parameter identity");
Check(typeof(ArgumentNullException).BaseType == typeof(ArgumentException), "argument null hierarchy");
Check(typeof(ArgumentException).BaseType == typeof(SystemException), "argument hierarchy");
Check(typeof(SystemException).BaseType == typeof(Exception), "system exception hierarchy");

Console.WriteLine("sameReference=" + ReferenceEquals(first, same));
Console.WriteLine("runtimeVersion=" + Environment.Version);
Console.WriteLine("constructedEqual=" + first.Equals(constructed));
Console.WriteLine("differentArgumentEqual=" + first.Equals(different));
Console.WriteLine("sameGenericDefinition=" + (first.GetGenericTypeDefinition() == different.GetGenericTypeDefinition()));
Console.WriteLine("secondDefinitionCanonical=" + ReferenceEquals(listOfInt, reconstructedListOfInt));
Console.WriteLine("secondDefinitionDifferentArgumentsSameReference=" + ReferenceEquals(listOfInt, listOfLong));
Console.WriteLine("nullTypeArgumentsParameter=" + nullTypeArgumentsParameter);
Console.WriteLine("nullTypeNameParameter=" + nullTypeNameParameter);
Console.WriteLine("argumentNullHierarchy=True");
Console.WriteLine("selectedTypeNameLookup=True");

static void Check(bool condition, string label)
{
    if (!condition)
    {
        throw new Exception("Oracle assertion failed: " + label);
    }
}
