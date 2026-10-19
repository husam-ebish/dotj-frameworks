# DJ-011 .j Containers: dependencies and licenses

## Proposed Java dependencies

sdk

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Installed JDK/jlink, OCI-compatible build tools and Linux base images as build/platform dependencies.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | NuGet.Versioning | [eng/shared/Microsoft.DotNet.Docker.Shared.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/shared/Microsoft.DotNet.Docker.Shared.csproj) |
| ProjectReference | ../shared/Microsoft.DotNet.Docker.Shared.csproj | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Azure.Identity | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Azure.Storage.Blobs | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | LibGit2Sharp | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Microsoft.DotNet.DarcLib | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Microsoft.DotNet.GitAutomation | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Microsoft.Extensions.Hosting | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Microsoft.TeamFoundationServer.Client | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Octokit | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | System.CommandLine | [eng/update-dependencies/update-dependencies.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/eng/update-dependencies/update-dependencies.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| PackageReference | xunit | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| PackageReference | xunit.runner.visualstudio | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| PackageReference | coverlet.collector | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| ProjectReference | ..\LibFoo\LibFoo.csproj | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| ProjectReference | ..\LibBar\LibBar.csproj | [samples/MultiProjectApp/Tests/Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/samples/MultiProjectApp/Tests/Tests.csproj) |
| ProjectReference | ../../eng/update-dependencies/update-dependencies.csproj | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |
| PackageReference | Moq | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |
| PackageReference | Shouldly | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |
| PackageReference | xunit.v3 | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |
| PackageReference | xunit.runner.visualstudio | [tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/tests/UpdateDependencies.Tests/UpdateDependencies.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/dotnet-docker/blob/a5ada4c290f2dc087c6926beeeaffcd07912abe7/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-containers-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
