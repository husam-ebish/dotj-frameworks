# DJ-063 .j Registry: dependencies and licenses

## Proposed Java dependencies

web,packages,postgresql,auth

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Owned web/data stack and filesystem/object-storage SPI.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Aspire.Hosting.Azure.Search | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Azure.Storage | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Aspire.Hosting.Testing | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac.Mvc5.Owin | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac.Mvc5 | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac.Owin | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac.WebApi2 | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Autofac | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Core | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Data.Tables | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Identity | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Messaging.ServiceBus | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Search.Documents | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Keys | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Security.KeyVault.Secrets | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Blobs | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Azure.Storage.Queues | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | CommonMark.NET | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | CsvHelper | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | d3 | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Dapper.StrongName | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | dotNetRDF | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | EntityFramework | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | FluentAssertions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | FluentLinkChecker | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | HtmlSanitizer | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Knapcode.MiniZip | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | LibGit2Sharp | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Lucene.Net.Contrib | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Lucene.Net | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Markdig.Signed | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | MicroBuild.Core | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.AspNetCore | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.DependencyCollector | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.TraceListener | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights.Web | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.ApplicationInsights | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.DynamicData.EFProvider | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Identity.Core | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Mvc | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Razor | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.Web.Optimization | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.Client | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.Core | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.MessageHandlers.Compression.StrongName | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.OData | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebApi.WebHost | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebHelpers | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebPages.Data | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebPages.WebData | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNet.WebPages | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Cryptography.Internal | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Cryptography.KeyDerivation | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Http | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Kusto.Data | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Azure.Storage.DataMovement | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Compression | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.Memory | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.NetAnalyzers | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeDom.Providers.DotNetCompilerPlatform | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Services.Client | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Data.Services | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.CommandLineUtils | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Abstractions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Binder | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.EnvironmentVariables | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.FileExtensions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Configuration.Json | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http.Polly | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Http | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options.ConfigurationExtensions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Primitives | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Client | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Identity.Web | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Internal.NuGet.Testing.SignedPackages | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Net.Http | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Playwright.Xunit | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Host.SystemWeb | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security.Cookies | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security.MicrosoftAccount | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security.OpenIdConnect | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin.Security | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Owin | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Rest.ClientRuntime | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Security.Utilities.Core | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.SourceLink.GitHub | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.TestPlatform | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.VisualStudio.Setup.Configuration.Interop | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Infrastructure | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.Web.Xdt | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Microsoft.WindowsAzure.ConfigurationManager | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Modernizr | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Moment.js | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Moq | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | MvcTreeView | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.CommandLine | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Commands | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Frameworks | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.PackageManagement | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Packaging | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Protocol | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Resolver | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.AnglicanGeek.MarkdownMailer | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.DynamicData.EFCodeFirstProvider | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.elmah.sqlserver | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.elmah | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.json-ld.net | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.Octokit | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.QueryInterceptor | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.WebActivator | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.WebBackgrounder.EntityFramework | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.StrongName.WebBackgrounder | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | NuGet.Versioning | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Octokit | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Owin | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | RouteMagic | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Enrichers.Environment | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Enrichers.Process | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Extensions.Logging | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.ApplicationInsights | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.Console | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Serilog.Sinks.File | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | SerilogTraceListener | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | SharpZipLib | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | Strathweb.CacheOutput.WebApi2.StrongName | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.Annotations | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.ComponentModel.EventBasedAsync | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Data.SqlClient | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Diagnostics.Debug | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Drawing.Common | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Formats.Asn1 | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.IdentityModel.Tokens.Jwt | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Linq.Expressions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Runtime | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Pkcs | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.X509Certificates | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.Syndication | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Text.Encodings.Web | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | System.ValueTuple | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | UAParser | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | WebActivatorEx | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | WebGrease | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | WindowsAzure.Caching | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | WindowsAzure.Storage | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| PackageVersion | xunit | [Directory.Packages.props](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/Directory.Packages.props) |
| ProjectReference | ..\NuGetGallery.Services\NuGetGallery.Services.csproj | [src/AccountDeleter/AccountDeleter.csproj](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/src/AccountDeleter/AccountDeleter.csproj) |
| ProjectReference | ..\Validation.Common.Job\Validation.Common.Job.csproj | [src/AccountDeleter/AccountDeleter.csproj](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/src/AccountDeleter/AccountDeleter.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE.txt](evidence/notices/LICENSE.txt) | [LICENSE.txt](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/LICENSE.txt) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-registry-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
