# DJ-014 .j Proxy: dependencies and licenses

## Proposed Java dependencies

web,resilience,extensions

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Owned web transport plus JDK HTTP client where semantics suffice; SSLEngine for TLS.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/eng/common/internal/Tools.csproj) |
| ProjectReference | ..\..\src\Application\Yarp.Application.csproj | [test/Application.Tests/Yarp.Application.Tests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/Yarp.Application.Tests.csproj) |
| PackageReference | Microsoft.AspNetCore.Mvc.Testing | [test/Application.Tests/Yarp.Application.Tests.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/test/Application.Tests/Yarp.Application.Tests.csproj) |
| PackageReference | Yarp.ReverseProxy | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | Microsoft.Extensions.ServiceDiscovery | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | Microsoft.Extensions.ServiceDiscovery.Yarp | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | OpenTelemetry.Exporter.OpenTelemetryProtocol | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | OpenTelemetry.Extensions.Hosting | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | OpenTelemetry.Instrumentation.AspNetCore | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | OpenTelemetry.Instrumentation.Http | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | OpenTelemetry.Instrumentation.Runtime | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| PackageReference | AspNetCore.HealthChecks.ApplicationStatus | [src/Application/Yarp.Application.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Application/Yarp.Application.csproj) |
| ProjectReference | ..\ReverseProxy\Yarp.ReverseProxy.csproj | [src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj) |
| PackageReference | KubernetesClient | [src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj) |
| PackageReference | YamlDotNet | [src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/src/Kubernetes.Controller/Yarp.Kubernetes.Controller.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/LICENSE.txt) |
| [THIRD-PARTY-NOTICES.TXT](evidence/notices/THIRD-PARTY-NOTICES.TXT) | [THIRD-PARTY-NOTICES.TXT](https://github.com/dotnet/yarp/blob/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9/THIRD-PARTY-NOTICES.TXT) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-proxy-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
