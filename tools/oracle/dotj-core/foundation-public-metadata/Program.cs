using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

Type[] selected = [
    typeof(IDisposable),
    typeof(Type),
    typeof(Exception),
    typeof(SystemException),
    typeof(ArgumentException),
    typeof(ArgumentNullException),
    typeof(TypeLoadException),
];

BindingFlags declaredPublic = BindingFlags.Public | BindingFlags.DeclaredOnly
    | BindingFlags.Instance | BindingFlags.Static;
Exception inner = new("inner");
ArgumentException outer = new("outer", "value", inner);
ArgumentNullException nullArgument = new("typeName", "missing type");
static object ObserveGetType(string? name, bool throwOnError, bool ignoreCase)
{
    try
    {
        Type? resolved = Type.GetType(name!, throwOnError, ignoreCase);
        return new { result = resolved?.FullName, exception = (string?)null, paramName = (string?)null };
    }
    catch (Exception exception)
    {
        return new
        {
            result = (string?)null,
            exception = exception.GetType().FullName,
            paramName = (exception as ArgumentException)?.ParamName,
        };
    }
}
if (outer.ParamName != "value" || outer.Message != "outer (Parameter 'value')"
    || !ReferenceEquals(outer.InnerException, inner)
    || nullArgument.ParamName != "typeName" || nullArgument.Message != "missing type (Parameter 'typeName')")
{
    throw new InvalidOperationException("Selected exception constructor observation changed.");
}
var result = new
{
    runtimeVersion = Environment.Version.ToString(),
    coreLibSha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(typeof(Type).Assembly.Location)))
        .ToLowerInvariant(),
    selectedConstructorBehavior = new
    {
        argumentParamName = outer.ParamName,
        argumentMessage = outer.Message,
        argumentInnerSameReference = ReferenceEquals(outer.InnerException, inner),
        nullArgumentParamName = nullArgument.ParamName,
        nullArgumentMessage = nullArgument.Message,
    },
    selectedGetTypeBehavior = new
    {
        exact = ObserveGetType("System.String", false, false),
        insensitive = ObserveGetType("system.string", false, true),
        sensitiveMiss = ObserveGetType("system.string", false, false),
        missing = ObserveGetType("System.Unknown", false, false),
        missingThrow = ObserveGetType("System.Unknown", true, false),
        nullName = ObserveGetType(null, false, false),
        coreLibString = ObserveGetType("System.String, System.Private.CoreLib", false, false),
        coreLibInt32 = ObserveGetType("System.Int32, System.Private.CoreLib", false, false),
        legacyString = ObserveGetType("System.String, mscorlib", false, false),
        unknownAssembly = ObserveGetType("System.String, NotAnAssembly", false, false),
        unknownAssemblyThrow = ObserveGetType("System.String, NotAnAssembly", true, false),
    },
    types = selected.Select(type => new
    {
        fullName = type.FullName,
        baseType = type.BaseType?.FullName,
        isInterface = type.IsInterface,
        isAbstract = type.IsAbstract,
        declaredPublicMethodCount = type.GetMethods(declaredPublic).Count(method => !method.IsSpecialName),
        declaredPublicPropertyCount = type.GetProperties(declaredPublic).Length,
        selectedMethods = type.GetMethods(declaredPublic)
            .Where(method => !method.IsSpecialName && (
                method.Name is "Dispose" or "Equals" or "GetType" or "MakeGenericType"
                    or "GetGenericArguments" or "GetGenericTypeDefinition"))
            .Select(method => new
            {
                name = method.Name,
                isStatic = method.IsStatic,
                returnType = method.ReturnType.FullName,
                parameters = method.GetParameters()
                    .Select(parameter => new { name = parameter.Name, type = parameter.ParameterType.FullName })
                    .ToArray(),
            }).ToArray(),
        selectedProperties = type.GetProperties(declaredPublic)
            .Where(property => property.Name is "ParamName" or "Message" or "InnerException" or "IsGenericType"
                or "IsConstructedGenericType" or "IsGenericParameter"
                or "GenericParameterPosition" or "GenericTypeArguments")
            .Select(property => new { name = property.Name, type = property.PropertyType.FullName })
            .ToArray(),
        publicConstructors = type.GetConstructors(declaredPublic)
            .Select(constructor => constructor.GetParameters()
                .Select(parameter => new { name = parameter.Name, type = parameter.ParameterType.FullName })
                .ToArray()).ToArray(),
    }).ToArray(),
};
Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
