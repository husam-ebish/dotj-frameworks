# DJ-057 .j Excel: dependencies and licenses

## Proposed Java dependencies

openxml,core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Owned OpenXML package layer, ZIP/XML and numeric/date APIs.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageReference | PolySharp | [ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj) |
| ProjectReference | ..\ClosedXML.IO\ClosedXML.IO.csproj | [ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.IO.CodeGen/ClosedXML.IO.CodeGen.csproj) |
| PackageReference | Microsoft.CSharp | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| PackageReference | Microsoft.NET.Test.Sdk | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| PackageReference | NUnit | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| PackageReference | NUnit3TestAdapter | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| PackageReference | System.Data.SqlClient | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| ProjectReference | ..\ClosedXML\ClosedXML.csproj | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| ProjectReference | ..\ClosedXML.Examples\ClosedXML.Examples.csproj | [ClosedXML.Tests/ClosedXML.Tests.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML.Tests/ClosedXML.Tests.csproj) |
| PackageReference | DocumentFormat.OpenXml | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | ExcelNumberFormat | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | Microsoft.SourceLink.GitHub | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | Polyfill | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | RBush.Signed | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | SixLabors.Fonts | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | ClosedXML.Parser | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | System.Buffers | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | System.Memory | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| PackageReference | Microsoft.Bcl.HashCode | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |
| ProjectReference | ..\ClosedXML.IO\ClosedXML.IO.csproj | [ClosedXML/ClosedXML.csproj](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/ClosedXML/ClosedXML.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/ClosedXML/ClosedXML/blob/09f2f21a60e821ce7fb18ca3576b272e5dd6d921/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-excel-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
