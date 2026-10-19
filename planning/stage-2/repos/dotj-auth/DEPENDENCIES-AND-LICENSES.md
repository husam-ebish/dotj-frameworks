# DJ-016 .j Auth: dependencies and licenses

## Proposed Java dependencies

web,json,core

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: JCA/JCE, TLS, secure randomness and own JOSE serialization; existing crypto primitives remain JDK-owned.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | EntityFramework | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | BouncyCastle.Cryptography | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.DataProtection | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Cryptography | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Polly | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Primitives | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.WebEncoders | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.JsonWebTokens | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Protocols | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Tokens | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Windows.SDK.Contracts | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MongoDB.Bson | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MSBuild.Microsoft.VisualStudio.Web.targets | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | NuGet.Build.Tasks.Pack | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | SharpCompress | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Snappier | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Buffers | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Collections.Immutable | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Net.Http.Json | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | AngleSharp | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MartinCostello.Logging.XUnit | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Testing | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Linq.Async | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Xunit.SkippableFact | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Antlr | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Autofac.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Autofac.Mvc5 | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Autofac.Owin | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Autofac.WebApi2.Owin | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.AppServices | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.WinForms | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.Wpf | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Identity.EntityFramework | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Identity.Owin | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Mvc | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Web.Optimization | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.Owin | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeDom.Providers.DotNetCompilerPlatform | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Net.Compilers.Toolset | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Host.SystemWeb | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security.Cookies | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security.OAuth | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Infrastructure | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | SourceGear.sqlite3 | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | SQLite.CodeFirst | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Data.SQLite.EF6 | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | WebGrease | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | EntityFramework | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.DataProtection | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Relational | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Polly | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Resilience | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.JsonWebTokens | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Protocols | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Tokens | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Primitives | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MongoDB.Bson | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MongoDB.Driver | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | SharpCompress | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Snappier | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Xamarin.AndroidX.Browser | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | AngleSharp | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | MartinCostello.Logging.XUnit | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.TestHost | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.TimeProvider.Testing | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Xunit.SkippableFact | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.AppServices | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.WinForms | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Dapplo.Microsoft.Extensions.Hosting.Wpf | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Identity.EntityFrameworkCore | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.Sqlite | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.EntityFrameworkCore.SqlServer | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Maui.Controls | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.Maui.Controls.Compatibility | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Spectre.Console | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | Scriban | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageVersion | System.Interactive | [Directory.Packages.props](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/Directory.Packages.props) |
| PackageReference | Microsoft.ManifestTool.CrossPlatform | [eng/common/internal/Tools.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Core | [eng/common/internal/Tools.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.VisualStudioEng.MicroBuild.Plugins.SwixBuild | [eng/common/internal/Tools.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.DotNet.IBCMerge | [eng/common/internal/Tools.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/eng/common/internal/Tools.csproj) |
| PackageReference | Drop.App | [eng/common/internal/Tools.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/eng/common/internal/Tools.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzers | [gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj) |
| PackageReference | Scriban | [gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj) |
| PackageReference | System.Interactive | [gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/gen/OpenIddict.Client.WebIntegration.Generators/OpenIddict.Client.WebIntegration.Generators.csproj) |
| ProjectReference | ..\..\src\OpenIddict.Abstractions\OpenIddict.Abstractions.csproj | [test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection | [test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj) |
| PackageReference | Moq | [test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/test/OpenIddict.Abstractions.Tests/OpenIddict.Abstractions.Tests.csproj) |
| ProjectReference | ..\..\src\OpenIddict.EntityFramework\OpenIddict.EntityFramework.csproj | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| ProjectReference | ..\..\src\OpenIddict.Owin\OpenIddict.Owin.csproj | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Antlr | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Autofac.Extensions.DependencyInjection | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Autofac.Mvc5 | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Autofac.Owin | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.AspNet.Mvc | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.AspNet.Web.Optimization | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.Extensions.DependencyInjection | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.Owin.Host.SystemWeb | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.Owin.Security.Cookies | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Microsoft.Web.Infrastructure | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | MSBuild.Microsoft.VisualStudio.Web.targets | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | Newtonsoft.Json | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | NuGet.Build.Tasks.Pack | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |
| PackageReference | WebGrease | [sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/sandbox/OpenIddict.Sandbox.AspNet.Client/OpenIddict.Sandbox.AspNet.Client.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `Apache-2.0`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.md](evidence/notices/LICENSE.md) | [LICENSE.md](https://github.com/openiddict/openiddict-core/blob/ab23a1625279b8b656912202c2b81a63d3438ca6/LICENSE.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-auth-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
