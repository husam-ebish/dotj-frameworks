# DJ-008 .j Interactive: dependencies and licenses

## Proposed Java dependencies

json,packages

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JShell, ProcessBuilder, sockets and structured serialization.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Assent | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Azure.Core | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | DuckDB.NET.Data.Full | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | DuckDB.NET.Data | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions.Json | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | FSharp.Compiler.Service | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | FSharp.Core | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | HtmlAgilityPack | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Humanizer.Core | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Humanizer | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Iced | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | ICSharpCode.Decompiler | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | JsonDiffPatch.Net | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | JsonSchema.Net | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Markdig.Signed | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.AspNetCore | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Html.Abstractions | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.SignalR.Client | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Data | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Tasks.Core | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Common | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Features | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Features | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Scripting.Common | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Scripting | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.Common | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Workspaces.MSBuild | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Analysis | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.SqlClient | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Sqlite | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Diagnostics.Runtime | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.PlatformAbstractions | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Design | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityClient | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | microsoft.playwright | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.PowerShell.Archive | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.PowerShell.SDK | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.PowerShell.SecretManagement | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.PowerShell.SecretStore | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Reactive.Testing | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Microsoft.Win32.Registry | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Nerdbank.Streams | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | NetMQ | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Npgsql | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PackageManagement | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Pocket.Disposable | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Pocket.TypeDiscovery | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PocketLogger.For.ApplicationInsights | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PocketLogger.For.Xunit | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PocketLogger.Subscribe | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PocketLogger | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | PowerShellGet | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.RollingFileAlternate | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | Serilog | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | SkiaSharp | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | StreamJsonRpc | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.CommandLine | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Annotations | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.DiagnosticSource | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Drawing.Common | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Reactive | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Runtime.Caching | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Runtime.Loader | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.X509Certificates | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | ThreadJob | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/Directory.Packages.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/common/internal/Tools.csproj) |
| FrameworkReference | Microsoft.AspNetCore.App | [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj) |
| PackageReference | PocketLogger | [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj) |
| ProjectReference | ..\Microsoft.DotNet.Interactive.CSharp\Microsoft.DotNet.Interactive.CSharp.csproj | [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj) |
| ProjectReference | ..\Microsoft.DotNet.Interactive\Microsoft.DotNet.Interactive.csproj | [src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.AspNetCore/Microsoft.DotNet.Interactive.AspNetCore.csproj) |
| PackageReference | BenchmarkDotNet | [eng/perf-tests/perf-tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/perf-tests/perf-tests.csproj) |
| PackageReference | Newtonsoft.Json | [eng/perf-tests/perf-tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/eng/perf-tests/perf-tests.csproj) |
| PackageReference | microsoft.playwright | [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj) |
| PackageReference | Pocket.Disposable | [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj) |
| PackageReference | PocketLogger | [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj) |
| ProjectReference | ..\Microsoft.DotNet.Interactive\Microsoft.DotNet.Interactive.csproj | [src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/src/Microsoft.DotNet.Interactive.Browser/Microsoft.DotNet.Interactive.Browser.csproj) |
| PackageReference | microsoft.dotnet.interactive.csharp | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | microsoft.dotnet.interactive.fsharp | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | Newtonsoft.Json | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | xunit | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | xunit.runner.visualstudio | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | coverlet.collector | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| PackageReference | AwesomeAssertions | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |
| ProjectReference | ..\ClockExtension\ClockExtension.csproj | [samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/samples/extensions/SampleExtensions.Tests/SampleExtensions.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [License.txt](evidence/notices/License.txt) | [License.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/License.txt) |
| [NOTICE.txt](evidence/notices/NOTICE.txt) | [NOTICE.txt](https://github.com/dotnet/interactive/blob/098a01b9183103186805a186a7dee3a3a70b2997/NOTICE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-interactive-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
