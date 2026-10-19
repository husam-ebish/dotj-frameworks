using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;

internal static class Program
{
    private const string ExpectedRuntimeVersion = "10.0.12";
    private const string ExpectedRuntimeCommit = "95017c711e6afc1085133d440e42b4bd78155701";

    public static int Main()
    {
        string versionFile = Path.Combine(RuntimeEnvironment.GetRuntimeDirectory(), ".version");
        string[] runtimeIdentity = File.ReadAllLines(versionFile);
        if (runtimeIdentity.Length != 2)
        {
            Console.Error.WriteLine("Unexpected runtime .version format.");
            return 2;
        }

        string runtimeCommit = runtimeIdentity[0];
        string runtimeVersion = runtimeIdentity[1];

        using var source = new CancellationTokenSource();
        source.Cancel();

        bool lateCallbackInvoked = false;
        using CancellationTokenRegistration registration = source.Token.Register(
            () => lateCallbackInvoked = true);

        bool cancellationTokenMatches = false;
        try
        {
            source.Token.ThrowIfCancellationRequested();
        }
        catch (OperationCanceledException exception)
        {
            cancellationTokenMatches = exception.CancellationToken == source.Token;
        }

        Console.WriteLine($"runtime.version={runtimeVersion}");
        Console.WriteLine($"runtime.commit={runtimeCommit}");
        Console.WriteLine($"type.IDisposable={typeof(IDisposable).FullName}");
        Console.WriteLine($"type.IAsyncDisposable={typeof(IAsyncDisposable).FullName}");
        Console.WriteLine($"cancellation.lateRegistrationSynchronous={lateCallbackInvoked}");
        Console.WriteLine($"cancellation.exceptionTokenMatches={cancellationTokenMatches}");

        if (runtimeVersion != ExpectedRuntimeVersion ||
            runtimeCommit != ExpectedRuntimeCommit ||
            !lateCallbackInvoked ||
            !cancellationTokenMatches)
        {
            Console.Error.WriteLine("Oracle bootstrap observation differs from the pinned profile.");
            return 1;
        }

        Console.WriteLine("result=PASS");
        return 0;
    }
}
