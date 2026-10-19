# DJ-018 .j Services: dependencies and licenses

## Proposed Java dependencies

service-client,web,extensions

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Own web server, XML APIs and sockets; optional native authentication bindings.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| PackageVersion | Nerdbank.GitVersioning | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | AngleSharp | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | AngleSharp.Diffing | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Confluent.Kafka | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Docker.DotNet | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Humanizer.Core | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | IsExternalInit | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authentication | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authentication.Negotiate | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Authorization | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.DataProtection | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.DataProtection.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Http | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Http.Features | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Http.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Hosting | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Hosting.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Hosting.Server.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Server.HttpSys | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Server.Kestrel | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Server.Kestrel.Core | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebSockets | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.WebUtilities | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Build | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Build.Locator | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.AsyncInterfaces | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Bcl.HashCode | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.Analyzers | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.Analyzer.Testing | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.CodeAnalysis.CSharp.SourceGenerators.Testing | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Caching.Memory | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.DependencyInjection.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Hosting.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Configuration | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Console | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Logging.Debug | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.ObjectPool | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Options | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.Extensions.Primitives | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Protocols.WsFederation | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Tokens | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.IdentityModel.Tokens.Saml | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | MSMQ.Messaging | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Newtonsoft.Json | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | RabbitMQ.Client | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Swashbuckle.AspNetCore.Swagger | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Buffers | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Configuration.ConfigurationManager | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.DirectoryServices | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.DirectoryServices.Protocols | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.IdentityModel.Tokens.Jwt | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.IO.Pipelines | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Memory | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Net.Http | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Private.Uri | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Reflection.DispatchProxy | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Runtime.InteropServices.RuntimeInformation | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.ProtectedData | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Security.Cryptography.Xml | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Security.Principal.Windows | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Text.Json | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Text.Encodings.Web | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Threading.Tasks.Extensions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Web.Services.Description | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.NET.Test.Sdk | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | xunit.v3 | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | xunit.v3.extensibility.core | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | xunit.analyzers | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | coverlet.collector | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | xunit.runner.visualstudio | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Xunit.StaFact | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Testcontainers | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Testcontainers.RabbitMq | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.Reflection.Metadata | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.Primitives | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.NetTcp | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.Http | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.NetNamedPipe | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.UnixDomainSocket | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | System.ServiceModel.Federation | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Connections.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Mvc.Testing | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageVersion | Microsoft.AspNetCore.Connections.Abstractions | [Directory.Packages.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Packages.props) |
| PackageReference | Nerdbank.GitVersioning | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | Microsoft.NET.Test.Sdk | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | xunit.v3 | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | xunit.analyzers | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | coverlet.collector | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | xunit.runner.visualstudio | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | System.Reflection.Metadata | [Directory.Build.props](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/Directory.Build.props) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzers | [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn3.11.csproj) |
| PackageReference | Microsoft.CodeAnalysis.CSharp | [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj) |
| PackageReference | Microsoft.CodeAnalysis.Analyzers | [src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/CoreWCF.BuildTools/src/CoreWCF.BuildTools.Roslyn4.0.csproj) |
| PackageReference | System.Runtime.InteropServices.RuntimeInformation | [src/Common/UnitTests.Common/UnitTests.Common.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/Common/UnitTests.Common/UnitTests.Common.csproj) |
| ProjectReference | $(SourceDir)CoreWCF.Primitives\src\CoreWCF.Primitives.csproj | [src/Common/UnitTests.Common/UnitTests.Common.csproj](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/src/Common/UnitTests.Common/UnitTests.Common.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/CoreWCF/CoreWCF/blob/6e2cce88349fe41056fe8afda0dbbdf98d54bb00/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-services-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
