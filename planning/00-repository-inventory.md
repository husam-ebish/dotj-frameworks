# Repository inventory

Inspection date: 2026-10-18. Reconnaissance is a scoped sample, not Stage-2 analysis. All architectural targets are proposed.

| ID | Original project | Original GitHub URL | Proposed product | Target repository | Category | Inspection status |
|---|---|---|---|---|---|---|
| DJ-001 | .NET runtime and base libraries | https://github.com/dotnet/runtime | .j Core | [dotj-core](repos/dotj-core/MAIN-PLAN.md) | Platform and developer tools | Partial reconnaissance |
| DJ-002 | .NET SDK | https://github.com/dotnet/sdk | .j SDK | [dotj-sdk](repos/dotj-sdk/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-003 | Roslyn | https://github.com/dotnet/roslyn | .j Code | [dotj-code](repos/dotj-code/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-004 | Razor | https://github.com/dotnet/razor | .j Razor | [dotj-razor](repos/dotj-razor/MAIN-PLAN.md) | Platform and developer tools | Partial reconnaissance |
| DJ-005 | MSBuild | https://github.com/dotnet/msbuild | .j Build | [dotj-build](repos/dotj-build/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-006 | .NET Extensions | https://github.com/dotnet/extensions | .j Extensions | [dotj-extensions](repos/dotj-extensions/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-007 | .NET diagnostics | https://github.com/dotnet/diagnostics | .j Diagnostics | [dotj-diagnostics](repos/dotj-diagnostics/MAIN-PLAN.md) | Platform and developer tools | Partial reconnaissance |
| DJ-008 | .NET Interactive | https://github.com/dotnet/interactive | .j Interactive | [dotj-interactive](repos/dotj-interactive/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-009 | .NET scaffolding | https://github.com/dotnet/Scaffolding | .j Scaffold | [dotj-scaffold](repos/dotj-scaffold/MAIN-PLAN.md) | Platform and developer tools | Partial reconnaissance |
| DJ-010 | .NET template engine | https://github.com/dotnet/templating | .j Templates | [dotj-templates](repos/dotj-templates/MAIN-PLAN.md) | Platform and developer tools | Partial reconnaissance |
| DJ-011 | .NET container images | https://github.com/dotnet/dotnet-docker | .j Containers | [dotj-containers](repos/dotj-containers/MAIN-PLAN.md) | Platform and developer tools | Scoped reconnaissance |
| DJ-012 | ASP.NET Core | https://github.com/dotnet/aspnetcore | .j Web | [dotj-web](repos/dotj-web/MAIN-PLAN.md) | Web, authentication and distributed applications | Scoped reconnaissance |
| DJ-013 | Aspire | https://github.com/microsoft/aspire | .j Aspire | [dotj-aspire](repos/dotj-aspire/MAIN-PLAN.md) | Web, authentication and distributed applications | Scoped reconnaissance |
| DJ-014 | YARP | https://github.com/dotnet/yarp | .j Proxy | [dotj-proxy](repos/dotj-proxy/MAIN-PLAN.md) | Web, authentication and distributed applications | Scoped reconnaissance |
| DJ-015 | Orleans | https://github.com/dotnet/orleans | .j Actors | [dotj-actors](repos/dotj-actors/MAIN-PLAN.md) | Web, authentication and distributed applications | Scoped reconnaissance |
| DJ-016 | OpenIddict | https://github.com/openiddict/openiddict-core | .j Auth | [dotj-auth](repos/dotj-auth/MAIN-PLAN.md) | Web, authentication and distributed applications | Partial reconnaissance |
| DJ-017 | WCF client libraries | https://github.com/dotnet/wcf | .j Service Client | [dotj-service-client](repos/dotj-service-client/MAIN-PLAN.md) | Web, authentication and distributed applications | Partial reconnaissance |
| DJ-018 | CoreWCF | https://github.com/CoreWCF/CoreWCF | .j Services | [dotj-services](repos/dotj-services/MAIN-PLAN.md) | Web, authentication and distributed applications | Partial reconnaissance |
| DJ-019 | Entity Framework Core | https://github.com/dotnet/efcore | .j Entity | [dotj-entity](repos/dotj-entity/MAIN-PLAN.md) | Database access and serialization | Partial reconnaissance |
| DJ-020 | Dapper | https://github.com/DapperLib/Dapper | .j SQL | [dotj-sql](repos/dotj-sql/MAIN-PLAN.md) | Database access and serialization | Partial reconnaissance |
| DJ-021 | Npgsql | https://github.com/npgsql/npgsql | .j PostgreSQL | [dotj-postgresql](repos/dotj-postgresql/MAIN-PLAN.md) | Database access and serialization | Partial reconnaissance |
| DJ-022 | StackExchange.Redis | https://github.com/StackExchange/StackExchange.Redis | .j Redis | [dotj-redis](repos/dotj-redis/MAIN-PLAN.md) | Database access and serialization | Partial reconnaissance |
| DJ-023 | Newtonsoft.Json | https://github.com/JamesNK/Newtonsoft.Json | .j JSON | [dotj-json](repos/dotj-json/MAIN-PLAN.md) | Database access and serialization | Scoped reconnaissance |
| DJ-024 | Mapster | https://github.com/MapsterMapper/Mapster | .j Mapster | [dotj-mapster](repos/dotj-mapster/MAIN-PLAN.md) | Database access and serialization | Partial reconnaissance |
| DJ-025 | Autofac | https://github.com/autofac/Autofac | .j Container | [dotj-container](repos/dotj-container/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-026 | FluentValidation | https://github.com/FluentValidation/FluentValidation | .j Validation | [dotj-validation](repos/dotj-validation/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-027 | Polly | https://github.com/App-vNext/Polly | .j Resilience | [dotj-resilience](repos/dotj-resilience/MAIN-PLAN.md) | Application libraries, jobs and communication | Scoped reconnaissance |
| DJ-028 | Reactive Extensions | https://github.com/dotnet/reactive | .j Reactive | [dotj-reactive](repos/dotj-reactive/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-029 | Hangfire | https://github.com/HangfireIO/Hangfire | .j Jobs | [dotj-jobs](repos/dotj-jobs/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-030 | Quartz.NET | https://github.com/quartznet/quartznet | .j Scheduler | [dotj-scheduler](repos/dotj-scheduler/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-031 | MailKit | https://github.com/jstedfast/MailKit | .j Mail | [dotj-mail](repos/dotj-mail/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-032 | RestSharp | https://github.com/restsharp/RestSharp | .j REST | [dotj-rest](repos/dotj-rest/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-033 | Refit | https://github.com/reactiveui/refit | .j Refit | [dotj-refit](repos/dotj-refit/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-034 | MQTTnet | https://github.com/dotnet/MQTTnet | .j MQTT | [dotj-mqtt](repos/dotj-mqtt/MAIN-PLAN.md) | Application libraries, jobs and communication | Partial reconnaissance |
| DJ-035 | ASP.NET API Versioning | https://github.com/dotnet/aspnet-api-versioning | .j Versioning | [dotj-versioning](repos/dotj-versioning/MAIN-PLAN.md) | API tooling and GraphQL | Partial reconnaissance |
| DJ-036 | Swashbuckle | https://github.com/domaindrivendev/Swashbuckle.AspNetCore | .j Swagger | [dotj-swagger](repos/dotj-swagger/MAIN-PLAN.md) | API tooling and GraphQL | Partial reconnaissance |
| DJ-037 | NSwag | https://github.com/RicoSuter/NSwag | .j OpenAPI | [dotj-openapi](repos/dotj-openapi/MAIN-PLAN.md) | API tooling and GraphQL | Partial reconnaissance |
| DJ-038 | Hot Chocolate / Strawberry Shake | https://github.com/ChilliCream/graphql-platform | .j Graph Platform | [dotj-graph-platform](repos/dotj-graph-platform/MAIN-PLAN.md) | API tooling and GraphQL | Partial reconnaissance |
| DJ-039 | GraphQL.NET | https://github.com/graphql-dotnet/graphql-dotnet | .j GraphQL | [dotj-graphql](repos/dotj-graphql/MAIN-PLAN.md) | API tooling and GraphQL | Partial reconnaissance |
| DJ-040 | WPF | https://github.com/dotnet/wpf | .j Presentation | [dotj-presentation](repos/dotj-presentation/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-041 | Windows Forms | https://github.com/dotnet/winforms | .j Forms | [dotj-forms](repos/dotj-forms/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-042 | .NET MAUI | https://github.com/dotnet/maui | .j MultiUI | [dotj-multiui](repos/dotj-multiui/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-043 | Avalonia | https://github.com/AvaloniaUI/Avalonia | .j Avalonia | [dotj-avalonia](repos/dotj-avalonia/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-044 | Uno Platform | https://github.com/unoplatform/uno | .j Uno | [dotj-uno](repos/dotj-uno/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-045 | .NET Community Toolkit | https://github.com/CommunityToolkit/dotnet | .j Toolkit | [dotj-toolkit](repos/dotj-toolkit/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-046 | MudBlazor | https://github.com/MudBlazor/MudBlazor | .j Material | [dotj-material](repos/dotj-material/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-047 | Radzen Blazor | https://github.com/radzenhq/radzen-blazor | .j Components | [dotj-components](repos/dotj-components/MAIN-PLAN.md) | Desktop, mobile and UI | Partial reconnaissance |
| DJ-048 | Serilog | https://github.com/serilog/serilog | .j Structured Log | [dotj-structured-log](repos/dotj-structured-log/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-049 | NLog | https://github.com/NLog/NLog | .j Log | [dotj-log](repos/dotj-log/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-050 | xUnit.net | https://github.com/xunit/xunit | .j XTest | [dotj-xtest](repos/dotj-xtest/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-051 | NUnit | https://github.com/nunit/nunit | .j Test | [dotj-test](repos/dotj-test/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-052 | Moq | https://github.com/devlooped/moq | .j Mock | [dotj-mock](repos/dotj-mock/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-053 | NSubstitute | https://github.com/nsubstitute/NSubstitute | .j Substitute | [dotj-substitute](repos/dotj-substitute/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-054 | Coverlet | https://github.com/coverlet-coverage/coverlet | .j Coverage | [dotj-coverage](repos/dotj-coverage/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-055 | BenchmarkDotNet | https://github.com/dotnet/BenchmarkDotNet | .j Benchmark | [dotj-benchmark](repos/dotj-benchmark/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-056 | Testcontainers for .NET | https://github.com/testcontainers/testcontainers-dotnet | .j Testcontainers | [dotj-testcontainers](repos/dotj-testcontainers/MAIN-PLAN.md) | Logging, testing and performance | Partial reconnaissance |
| DJ-057 | ClosedXML | https://github.com/ClosedXML/ClosedXML | .j Excel | [dotj-excel](repos/dotj-excel/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-058 | Open XML SDK | https://github.com/dotnet/Open-XML-SDK | .j OpenXML | [dotj-openxml](repos/dotj-openxml/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-059 | Markdig | https://github.com/xoofx/markdig | .j Markdown | [dotj-markdown](repos/dotj-markdown/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-060 | ML.NET | https://github.com/dotnet/machinelearning | .j ML | [dotj-ml](repos/dotj-ml/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-061 | Semantic Kernel | https://github.com/microsoft/semantic-kernel | .j Semantic | [dotj-semantic](repos/dotj-semantic/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-062 | NuGet client | https://github.com/NuGet/NuGet.Client | .j Packages | [dotj-packages](repos/dotj-packages/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-063 | NuGet Gallery | https://github.com/NuGet/NuGetGallery | .j Registry | [dotj-registry](repos/dotj-registry/MAIN-PLAN.md) | Documents, AI and package infrastructure | Partial reconnaissance |
| DJ-064 | AutoMapper | https://github.com/LuckyPennySoftware/AutoMapper | .j Automap | [dotj-automap](repos/dotj-automap/MAIN-PLAN.md) | Additional application frameworks | Partial reconnaissance |
| DJ-065 | MediatR | https://github.com/LuckyPennySoftware/MediatR | .j Mediator | [dotj-mediator](repos/dotj-mediator/MAIN-PLAN.md) | Additional application frameworks | Partial reconnaissance |
| DJ-066 | MassTransit | https://github.com/MassTransit/MassTransit | .j Bus | [dotj-bus](repos/dotj-bus/MAIN-PLAN.md) | Additional application frameworks | Partial reconnaissance |

## Official Java foundation, separate from the 66 targets

| Repository | Official URL | Purpose | Checkout | Proposed baseline status |
|---|---|---|---|---|
| OpenJDK mainline | https://github.com/openjdk/jdk | Official JVM, compiler and standard-library source | Optional; installed JDK normally sufficient | Research reference only; no production mainline target |
| OpenJDK 25 updates | https://github.com/openjdk/jdk25u | Java 25 update source | Optional; installed JDK normally sufficient | Proposed pinned GA-tag baseline; binary lock and tag-content verification open |

### Foundation evidence pins

- [https://github.com/openjdk/jdk](https://github.com/openjdk/jdk), inspected default-branch revision `3104115c2a0587895997965c9e88a1181f52ee47`. This is not the selected production target. README, license/build material retrieved where listed in the [foundation evidence](evidence/java-foundation.json).
- [https://github.com/openjdk/jdk25u](https://github.com/openjdk/jdk25u), inspected default-branch revision `49411542a96435cd403500592fbb586395fbaed5`. This is not the selected production target. README, license/build material retrieved where listed in the [foundation evidence](evidence/java-foundation.json).

See [baseline and dependency policy](03-java-foundation-and-dependency-policy.md) for the distinct proposed immutable source pin and remaining binary-selection gate.
