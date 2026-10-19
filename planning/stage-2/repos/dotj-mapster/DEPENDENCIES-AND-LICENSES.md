# DJ-024 .j Mapster: dependencies and licenses

## Proposed Java dependencies

core;entity(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Reflection, MethodHandles and annotation processors.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| ProjectReference | ..\ExpressionDebugger\ExpressionDebugger.csproj | [src/ExpressionDebugger.Console/ExpressionDebugger.Console.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Console/ExpressionDebugger.Console.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/ExpressionDebugger/ExpressionDebugger.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionDebugger.csproj) |
| ProjectReference | ..\ExpressionTranslator\ExpressionTranslator.csproj | [src/ExpressionDebugger/ExpressionDebugger.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger/ExpressionDebugger.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj) |
| PackageReference | MSTest.TestAdapter | [src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj) |
| PackageReference | MSTest.TestFramework | [src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj) |
| ProjectReference | ..\ExpressionDebugger\ExpressionDebugger.csproj | [src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/src/ExpressionDebugger.Tests/ExpressionDebugger.Tests.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/MapsterMapper/Mapster/blob/cbc1e5f04e6e003744b04f83d4705670a85e459b/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-mapster-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
