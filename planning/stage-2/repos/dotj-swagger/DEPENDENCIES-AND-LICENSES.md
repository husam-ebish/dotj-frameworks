# DJ-036 .j Swagger: dependencies and licenses

## Proposed Java dependencies

web,openapi

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Reflection and annotations; share OpenAPI model with dotj-openapi; browser UI assets are separate dependencies.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Autofac.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | BenchmarkDotNet | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | GitHubActionsTestLogger | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | IdentityServer4 | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | IdentityServer4.AccessTokenValidation | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | MartinCostello.Logging.XUnit.v3 | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.NewtonsoftJson | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Versioning | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Versioning.ApiExplorer | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.PublicApiAnalyzers | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.InMemory | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.Kiota.Bundle | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.OpenApi | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.OpenApi.YamlReader | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.Playwright | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Microsoft.Testing.Extensions.CodeCoverage | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | MSBuild.ProjectCreation | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | NJsonSchema | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | NSubstitute | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | NSwag.CodeGeneration.CSharp | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | NSwag.MSBuild | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | Verify.XunitV3 | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| PackageVersion | xunit.v3.mtp-v2 | [Directory.Packages.props](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/Directory.Packages.props) |
| ProjectReference | ..\Swashbuckle.AspNetCore.SwaggerGen\Swashbuckle.AspNetCore.SwaggerGen.csproj | [src/Swashbuckle.AspNetCore.Annotations/Swashbuckle.AspNetCore.Annotations.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.Annotations/Swashbuckle.AspNetCore.Annotations.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [src/Swashbuckle.AspNetCore.Annotations/Swashbuckle.AspNetCore.Annotations.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.Annotations/Swashbuckle.AspNetCore.Annotations.csproj) |
| PackageReference | Microsoft.OpenApi | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |
| PackageReference | Newtonsoft.Json | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |
| PackageReference | Microsoft.AspNetCore.Mvc.Testing | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |
| PackageReference | Microsoft.AspNetCore.Mvc.Testing | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |
| PackageReference | Microsoft.AspNetCore.Mvc.Testing | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |
| PackageReference | Microsoft.CodeAnalysis.PublicApiAnalyzers | [src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/src/Swashbuckle.AspNetCore.ApiTesting/Swashbuckle.AspNetCore.ApiTesting.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/blob/1e2b358b23cb9f041e8a395d4541d46566be7f81/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-swagger-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
