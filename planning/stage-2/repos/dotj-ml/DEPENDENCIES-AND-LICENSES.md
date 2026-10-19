# DJ-060 .j ML: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Arrays/buffers, concurrency and optional FFM/JNI bindings to identified native engines.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Apache.Arrow | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Google.Protobuf | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | LightGBM | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Workspaces | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CSharp | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Interactive | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Interactive.Formatting | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ObjectPool | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntime | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.OnnxRuntime.Managed | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | MlNetMklDeps | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging.Core | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | NuGet.Resolver | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Parquet.Net | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Plotly.NET.CSharp | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SciSharp.TensorFlow.Redist | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SciSharp.TensorFlow.Redist-Linux-GPU | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SciSharp.TensorFlow.Redist-Windows-GPU | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SharpZipLib | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SkiaSharp | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | SkiaSharp.NativeAssets.Linux.NoDependencies | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Buffers | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.CodeDom | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Composition | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.IO.FileSystem.AccessControl | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Numerics.Tensors | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Reflection.Emit.Lightweight | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Runtime.CompilerServices.Unsafe | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Security.Principal.Windows | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Text.Encodings.Web | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Threading.Channels | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | TensorFlow.NET | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | TorchSharp | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | libtorch-cpu-linux-x64 | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | libtorch-cpu-osx-x64 | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | libtorch-cpu-win-x64 | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | FSharp.Core | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | ApprovalTests | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | AwesomeAssertions | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet.Diagnostics.Windows | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | coverlet.msbuild | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.CodeFix.Testing.XUnit | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.PlatformAbstractions | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.RemoteExecutor | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.XUnitExtensions | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyModel | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.Onnx.TestModels | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.TensorFlow.TestModels | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.TestDatabases | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.TestModels | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ML.TestTokenizers | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | MSTest.TestAdapter | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | MSTest.TestFramework | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Data.SqlClient | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite.Core | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | runtime.native.System.Data.SqlClient.sni | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Xunit.Combinatorial | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Codecov | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Drop.App | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.Build.Tasks.Templating | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.DotNet.IBCMerge | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.ManifestTool.CrossPlatform | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudioEng.MicroBuild.Core | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | ReportGenerator | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | MathNet.Numerics.Signed | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| PackageVersion | TorchSharp-cuda-windows | [Directory.Packages.props](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/Directory.Packages.props) |
| ProjectReference | ..\Microsoft.ML.DataView\Microsoft.ML.DataView.csproj | [src/Microsoft.ML.Core/Microsoft.ML.Core.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/src/Microsoft.ML.Core/Microsoft.ML.Core.csproj) |
| PackageReference | System.Collections.Immutable | [src/Microsoft.ML.Core/Microsoft.ML.Core.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/src/Microsoft.ML.Core/Microsoft.ML.Core.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.EntryPoints\Microsoft.ML.EntryPoints.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.LightGbm\Microsoft.ML.LightGbm.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Mkl.Components\Microsoft.ML.Mkl.Components.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.OneDal\Microsoft.ML.OneDal.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Core\Microsoft.ML.Core.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Data\Microsoft.ML.Data.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Ensemble\Microsoft.ML.Ensemble.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.ImageAnalytics\Microsoft.ML.ImageAnalytics.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.KMeansClustering\Microsoft.ML.KMeansClustering.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.OnnxConverter\Microsoft.ML.OnnxConverter.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Parquet\Microsoft.ML.Parquet.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.PCA\Microsoft.ML.PCA.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.StandardTrainers\Microsoft.ML.StandardTrainers.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.TensorFlow\Microsoft.ML.TensorFlow.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.TimeSeries\Microsoft.ML.TimeSeries.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Microsoft.ML.Transforms\Microsoft.ML.Transforms.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\Microsoft.ML.TestFramework\Microsoft.ML.TestFramework.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| ProjectReference | ..\Microsoft.ML.Tests\Microsoft.ML.Tests.csproj | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| PackageReference | Microsoft.ML.TestModels | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| PackageReference | SciSharp.TensorFlow.Redist | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |
| PackageReference | Microsoft.ML.TensorFlow.TestModels | [test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/test/Microsoft.ML.Core.Tests/Microsoft.ML.Core.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/LICENSE) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/machinelearning/blob/655f469b0d54bccf94dc251b8db457b57d56d084/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-ml-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
