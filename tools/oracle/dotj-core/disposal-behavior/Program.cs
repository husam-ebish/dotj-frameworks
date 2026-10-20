using System.Reflection;
using System.Security.Cryptography;
using System.Text.Json;

namespace Dotj.Core.DisposalBehaviorOracle;

internal static class Program
{
    private static void Main()
    {
        CountingDisposable direct = new();
        IDisposable asInterface = direct;
        asInterface.Dispose();

        CountingDisposable normal = new();
        using (normal)
        {
        }

        CountingDisposable bodyFailure = new();
        string? bodyFailureObserved = null;
        try
        {
            using (bodyFailure)
            {
                throw new InvalidOperationException("body");
            }
        }
        catch (InvalidOperationException exception)
        {
            bodyFailureObserved = exception.Message;
        }

        InvalidOperationException disposeCause = new("cause");
        InvalidOperationException disposeError = new("dispose", disposeCause);
        CountingDisposable disposeFailure = new(() => throw disposeError);
        string? disposeFailureObserved = null;
        bool disposeFailureSameReference = false;
        bool disposeCauseSameReference = false;
        try
        {
            using (disposeFailure)
            {
                throw new InvalidOperationException("body");
            }
        }
        catch (InvalidOperationException exception)
        {
            disposeFailureObserved = exception.Message;
            disposeFailureSameReference = ReferenceEquals(exception, disposeError);
            disposeCauseSameReference = ReferenceEquals(exception.InnerException, disposeCause);
        }

        CountingDisposable repeated = new();
        repeated.Dispose();
        repeated.Dispose();
        CountingDisposable untouched = new();

        if (direct.Count != 1 || normal.Count != 1 || bodyFailure.Count != 1 || bodyFailureObserved != "body"
            || disposeFailure.Count != 1 || disposeFailureObserved != "dispose"
            || !disposeFailureSameReference || !disposeCauseSameReference || repeated.Count != 2
            || untouched.Count != 0)
        {
            throw new InvalidOperationException("The disposal oracle observations changed.");
        }

        Assembly assembly = typeof(IDisposable).Assembly;
        object result = new
        {
            runtimeVersion = Environment.Version.ToString(),
            coreLibSha256 = Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(assembly.Location))).ToLowerInvariant(),
            directInterfaceDispatchCount = direct.Count,
            normalUsingDisposeCount = normal.Count,
            bodyFailureDisposeCount = bodyFailure.Count,
            bodyFailureObserved,
            disposeFailureDisposeCount = disposeFailure.Count,
            disposeFailureObserved,
            disposeFailureSameReference,
            disposeCauseSameReference,
            repeatedExplicitDisposeCount = repeated.Count,
            untouchedDisposeCount = untouched.Count,
        };
        Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
    }
}
