# DJ-052 .j Mock: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JDK Proxy for interfaces; class-file API, java.lang.instrument and optional agents for classes.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | NuGetizer | [src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Common | [src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis/Moq.CodeAnalysis.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | Microsoft.TestPlatform.ObjectModel | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | xunit | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | xunit.runner.console | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | xunit.runner.msbuild | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | xunit.runner.visualstudio | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| ProjectReference | ..\Moq.CodeAnalysis\Moq.CodeAnalysis.csproj | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| ProjectReference | ..\Moq\Moq.csproj | [src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq.CodeAnalysis.UnitTests/Moq.CodeAnalysis.UnitTests.csproj) |
| PackageReference | NuGetizer | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |
| PackageReference | IFluentInterface | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |
| PackageReference | Microsoft.CSharp | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp.CodeStyle | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |
| ProjectReference | ..\Moq.Sdk\Moq.Sdk.csproj | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |
| ProjectReference | ..\Moq.DynamicProxy\Moq.DynamicProxy.csproj | [src/Moq/Moq.csproj](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/src/Moq/Moq.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [license.txt](evidence/notices/license.txt) | [license.txt](https://github.com/devlooped/moq/blob/bdf16e758e8022c40cef2bfd025181f845bbd2a9/license.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-mock-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
