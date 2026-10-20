using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

namespace Dotj.Core.DisposalMetadataOracle;

internal static class Program
{
    private static void Main()
    {
        Assembly assembly = typeof(IDisposable).Assembly;
        Type[] types = [typeof(IDisposable), typeof(IAsyncDisposable)];
        object result = new
        {
            runtimeVersion = Environment.Version.ToString(),
            assemblyName = assembly.GetName().Name,
            assemblyVersion = assembly.GetName().Version?.ToString(),
            assemblySha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(assembly.Location))).ToLowerInvariant(),
            interfaces = types.Select(type => new
            {
                fullName = type.FullName,
                isPublic = type.IsPublic,
                isInterface = type.IsInterface,
                methods = type.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
                    .OrderBy(method => method.Name, StringComparer.Ordinal)
                    .Select(method => new
                    {
                        name = method.Name,
                        returnType = method.ReturnType.FullName,
                        isPublic = method.IsPublic,
                        isAbstract = method.IsAbstract,
                        parameterTypes = method.GetParameters().Select(parameter => parameter.ParameterType.FullName).ToArray(),
                    })
                    .ToArray(),
            }).ToArray(),
        };

        Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
    }
}
