using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

if (args.Length != 1)
{
    Console.Error.WriteLine("Usage: ApiShapeOracle <System.Private.CoreLib public type full name>");
    return 2;
}

Assembly coreLib = typeof(object).Assembly;
Type? selectedType = coreLib.GetType(args[0], throwOnError: false, ignoreCase: false);
if (selectedType is null || !selectedType.IsPublic)
{
    Console.Error.WriteLine("Public CoreLib type not found: " + args[0]);
    return 3;
}

const BindingFlags declaredPublic = BindingFlags.Public | BindingFlags.DeclaredOnly | BindingFlags.Instance | BindingFlags.Static;
string assemblyHash = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(coreLib.Location))).ToLowerInvariant();
var snapshot = new
{
    runtimeVersion = Environment.Version.ToString(),
    assemblyName = coreLib.GetName().Name,
    assemblySha256 = assemblyHash,
    type = new
    {
        name = selectedType.Name,
        fullName = selectedType.FullName,
        isInterface = selectedType.IsInterface,
        isValueType = selectedType.IsValueType,
        isGenericTypeDefinition = selectedType.IsGenericTypeDefinition,
        baseType = selectedType.BaseType?.FullName,
        genericParameters = selectedType.GetGenericArguments().Select(argument => new
        {
            argument.Name,
            attributes = argument.GenericParameterAttributes.ToString(),
            constraints = argument.GetGenericParameterConstraints().Select(constraint => constraint.ToString()).Order().ToArray()
        }).ToArray(),
        interfaces = selectedType.GetInterfaces().Select(implemented => implemented.ToString()).Order().ToArray(),
        constructors = selectedType.GetConstructors(declaredPublic).Select(constructor => constructor.ToString()).Order().ToArray(),
        methods = selectedType.GetMethods(declaredPublic).Select(method => new
        {
            method.Name,
            signature = method.ToString(),
            returnType = method.ReturnType.ToString(),
            isStatic = method.IsStatic,
            genericArity = method.GetGenericArguments().Length,
            parameters = method.GetParameters().Select(parameter => new
            {
                parameter.Name,
                type = parameter.ParameterType.ToString(),
                parameter.IsOptional,
                parameter.IsOut
            }).ToArray()
        }).OrderBy(method => method.Name).ThenBy(method => method.signature).ToArray(),
        properties = selectedType.GetProperties(declaredPublic).Select(property => new
        {
            property.Name,
            type = property.PropertyType.ToString(),
            hasPublicGet = property.GetMethod?.IsPublic == true,
            hasPublicSet = property.SetMethod?.IsPublic == true,
            indexParameters = property.GetIndexParameters().Select(parameter => parameter.ParameterType.ToString()).ToArray()
        }).OrderBy(property => property.Name).ToArray(),
        events = selectedType.GetEvents(declaredPublic).Select(eventInfo => eventInfo.Name).Order().ToArray(),
        fields = selectedType.GetFields(declaredPublic).Select(field => new
        {
            field.Name,
            type = field.FieldType.ToString(),
            field.IsStatic,
            field.IsLiteral
        }).OrderBy(field => field.Name).ToArray()
    }
};

Console.WriteLine(JsonSerializer.Serialize(snapshot, new JsonSerializerOptions { WriteIndented = true }));
return 0;
