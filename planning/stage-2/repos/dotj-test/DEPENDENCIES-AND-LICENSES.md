# DJ-051 .j Test: dependencies and licenses

## Proposed Java dependencies

core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Reflection, classloaders, executors and XML.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | Microsoft.NET.Test.Sdk | [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) |
| PackageReference | NUnit3TestAdapter | [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) |
| PackageReference | coverlet.collector | [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) |
| ProjectReference | ..\CakeScripts\CakeScripts.csproj | [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) |
| ProjectReference | ..\src\NUnitFramework\framework\nunit.framework.csproj | [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/LICENSE.txt) |
| [NOTICES.md](evidence/notices/NOTICES.md) | [NOTICES.md](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/NOTICES.md) |
| [THIRD_PARTY_NOTICES.md](evidence/notices/THIRD_PARTY_NOTICES.md) | [THIRD_PARTY_NOTICES.md](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/THIRD_PARTY_NOTICES.md) |
| [THIRD_PARTY_NOTICES_DEV.md](evidence/notices/THIRD_PARTY_NOTICES_DEV.md) | [THIRD_PARTY_NOTICES_DEV.md](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/THIRD_PARTY_NOTICES_DEV.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-test-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
