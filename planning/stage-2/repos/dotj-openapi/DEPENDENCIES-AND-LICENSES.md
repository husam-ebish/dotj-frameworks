# DJ-037 .j OpenAPI: dependencies and licenses

## Proposed Java dependencies

json;code(dev-optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Own JSON, XML where required, Java source generation and filesystem.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | AvalonEdit | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Expression.Interaction | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.Client | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.Core | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.ApiExplorer | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Formatters.Json | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.StaticFiles | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.FileProviders.Embedded | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.StaticFiles | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | MyToolkit | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | MyToolkit.Extended | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Namotion.Reflection | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema.CodeGeneration | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema.CodeGeneration.CSharp | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema.CodeGeneration.TypeScript | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema.NewtonsoftJson | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | NJsonSchema.Yaml | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | System.Runtime.Loader | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Verify.XunitV3 | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | xunit.v3 | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | WixToolset.Util.wixext | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | WixToolset.UI.wixext | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Server.Kestrel.Core | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OpenApi | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OpenApi | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.OpenApi | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/Directory.Packages.props) |
| ProjectReference | ..\NSwag.Commands\NSwag.Commands.csproj | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| ProjectReference | ..\NSwag.Generation.WebApi\NSwag.Generation.WebApi.csproj | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| PackageReference | AvalonEdit | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| PackageReference | Expression.Interaction | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| PackageReference | MyToolkit | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| PackageReference | MyToolkit.Extended | [src/NSwagStudio/NSwagStudio.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwagStudio/NSwagStudio.csproj) |
| PackageReference | NJsonSchema | [src/NSwag.Core/NSwag.Core.csproj](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/src/NSwag.Core/NSwag.Core.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/RicoSuter/NSwag/blob/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41/LICENSE.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-openapi-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
