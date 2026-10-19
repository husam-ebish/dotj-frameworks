# DJ-029 .j Jobs: dependencies and licenses

## Proposed Java dependencies

core,postgresql,scheduler;web(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Executors, own storage client and web stack.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| ProjectReference | ..\Hangfire.NetCore\Hangfire.NetCore.csproj | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | Microsoft.AspNetCore.Http.Abstractions | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | Microsoft.AspNetCore.Antiforgery | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | Microsoft.AspNetCore.Http.Abstractions | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | Microsoft.AspNetCore.Antiforgery | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| FrameworkReference | Microsoft.AspNetCore.App | [src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.AspNetCore/Hangfire.AspNetCore.csproj) |
| PackageReference | MoreLinq.Source.MoreEnumerable.Pairwise | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | LibLog | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Cronos | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | StackTraceFormatter.Source | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | StackTraceParser.Source | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Owin | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | CronExpressionDescriptor | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Newtonsoft.Json | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Microsoft.Owin | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | System.Threading.Thread | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | System.Threading.ThreadPool | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Newtonsoft.Json | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Microsoft.CSharp | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Newtonsoft.Json | [src/Hangfire.Core/Hangfire.Core.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/src/Hangfire.Core/Hangfire.Core.csproj) |
| PackageReference | Moq.Sequences | [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |
| PackageReference | Microsoft.NETFramework.ReferenceAssemblies | [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |
| PackageReference | Newtonsoft.Json | [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |
| PackageReference | Newtonsoft.Json | [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |
| ProjectReference | ..\..\src\Hangfire.Core\Hangfire.Core.csproj | [tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/tests/Hangfire.Core.Tests/Hangfire.Core.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `NOASSERTION`.

The inspected Hangfire material describes LGPL v3-or-later and commercial alternatives. Separate core, storage adapters and commercial extension rights. No linking/distribution conclusion is asserted here.

| Retrieved notice/license | Immutable source |
|---|---|
| [COPYING](evidence/notices/COPYING) | [COPYING](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/COPYING) |
| [COPYING.LESSER](evidence/notices/COPYING.LESSER) | [COPYING.LESSER](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/COPYING.LESSER) |
| [NOTICES](evidence/notices/NOTICES) | [NOTICES](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/NOTICES) |
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/LICENSE.md) |
| [LICENSE_ROYALTYFREE](evidence/notices/LICENSE_ROYALTYFREE) | [LICENSE_ROYALTYFREE](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/LICENSE_ROYALTYFREE) |
| [LICENSE_STANDARD](evidence/notices/LICENSE_STANDARD) | [LICENSE_STANDARD](https://github.com/HangfireIO/Hangfire/blob/c35077110cc8364b06ea30d39947bd5f688b2e8b/LICENSE_STANDARD) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-jobs-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
