# Source ownership and proposed dependencies

Namespace is not source ownership. These boundaries supersede any earlier generic Stage-1 wording that suggested all Microsoft.Extensions implementations belong in dotj-extensions or that all JSON belongs in dotj-json.

| Capability | Owner and boundary |
|---|---|
| Runtime-origin Microsoft.Extensions DI/configuration/options/logging/hosting | dotj-core owns both abstractions and actual baseline implementations; integrations are separate artifacts |
| Extensions-repository AI, vector, compliance, telemetry, service discovery and resilience packages | dotj-extensions; actual source paths determine ownership |
| System.Text.Json | Core system-json behavior profile; Newtonsoft.Json remains dotj-json |
| Default DI versus Autofac | Core default container and independent dotj-container with optional bridge |
| System.Net.Mail versus MailKit/MimeKit | Core mail profile is separate from dotj-mail protocol/MIME scope |
| System.IO.Packaging versus Open XML SDK | Core packaging profile and dotj-openxml document model; neutral packaging contracts may be shared deliberately |
| Core RateLimiting versus Polly | Core rate-limit behavior and dotj-resilience strategy composition remain distinct |
| Razor versus web | dotj-razor compiler/IR/tooling; dotj-web rendering/runtime; Razor source relocated into Roslyn does not merge product ownership |
| Templates versus SDK | dotj-templates reusable engine; dotj-sdk orchestrator; relocation into SDK does not merge targets |
| WCF client/server codecs | Neutral wire submodule in dotj-service-client; dotj-services depends on it, never the reverse |
| GraphQL engines | dotj-graph-platform and dotj-graphql stay independent; shared syntax only through an explicit neutral contract |
| OpenAPI products | dotj-openapi is NSwag: schema/document tooling, client generation, CLI and Studio track. dotj-swagger is Swashbuckle endpoint/UI integration |
| Browser UI products | dotj-material is MudBlazor; dotj-components is Radzen's open component repository; neither is a desktop theme library |
| Semantic Kernel | Requested C# functionality retained; existing Java/Python code and Agent Framework successor are not implicit implementation sources |

## Proposed product edges

These are architecture proposals, not the restored upstream dependency graph. Base edges must form a DAG. Optional/development edges are realized in separate adapter/tool artifacts. For example validation-web depends on validation and web; validation core does not depend on web.

| Consumer | Provider | Role | Status |
|---|---|---|---|
| dotj-sdk | dotj-build | base | proposed |
| dotj-sdk | dotj-templates | base | proposed |
| dotj-sdk | dotj-packages | base | proposed |
| dotj-code | dotj-core | base | proposed |
| dotj-razor | dotj-code | base | proposed |
| dotj-build | dotj-core | base | proposed |
| dotj-extensions | dotj-core | base | proposed |
| dotj-diagnostics | dotj-core | base | proposed |
| dotj-interactive | dotj-json | base | proposed |
| dotj-interactive | dotj-packages | base | proposed |
| dotj-scaffold | dotj-code | base | proposed |
| dotj-scaffold | dotj-templates | base | proposed |
| dotj-scaffold | dotj-web | base | proposed |
| dotj-scaffold | dotj-entity | base | proposed |
| dotj-templates | dotj-core | base | proposed |
| dotj-templates | dotj-json | base | proposed |
| dotj-containers | dotj-sdk | base | proposed |
| dotj-web | dotj-core | base | proposed |
| dotj-web | dotj-razor | base | proposed |
| dotj-web | dotj-json | base | proposed |
| dotj-aspire | dotj-extensions | base | proposed |
| dotj-aspire | dotj-web | base | proposed |
| dotj-aspire | dotj-containers | base | proposed |
| dotj-proxy | dotj-web | base | proposed |
| dotj-proxy | dotj-resilience | base | proposed |
| dotj-proxy | dotj-extensions | base | proposed |
| dotj-actors | dotj-core | base | proposed |
| dotj-actors | dotj-json | base | proposed |
| dotj-actors | dotj-extensions | base | proposed |
| dotj-auth | dotj-web | base | proposed |
| dotj-auth | dotj-json | base | proposed |
| dotj-auth | dotj-core | base | proposed |
| dotj-service-client | dotj-core | base | proposed |
| dotj-services | dotj-service-client | base | proposed |
| dotj-services | dotj-web | base | proposed |
| dotj-services | dotj-extensions | base | proposed |
| dotj-entity | dotj-core | base | proposed |
| dotj-entity | dotj-postgresql | base | proposed |
| dotj-sql | dotj-postgresql | base | proposed |
| dotj-sql | dotj-core | base | proposed |
| dotj-postgresql | dotj-core | base | proposed |
| dotj-redis | dotj-core | base | proposed |
| dotj-json | dotj-core | base | proposed |
| dotj-mapster | dotj-core | base | proposed |
| dotj-mapster | dotj-entity | optional | proposed |
| dotj-container | dotj-core | base | proposed |
| dotj-validation | dotj-core | base | proposed |
| dotj-validation | dotj-web | optional | proposed |
| dotj-resilience | dotj-core | base | proposed |
| dotj-reactive | dotj-core | base | proposed |
| dotj-jobs | dotj-core | base | proposed |
| dotj-jobs | dotj-postgresql | base | proposed |
| dotj-jobs | dotj-scheduler | base | proposed |
| dotj-jobs | dotj-web | optional | proposed |
| dotj-scheduler | dotj-core | base | proposed |
| dotj-scheduler | dotj-postgresql | optional | proposed |
| dotj-mail | dotj-core | base | proposed |
| dotj-rest | dotj-json | base | proposed |
| dotj-rest | dotj-core | base | proposed |
| dotj-refit | dotj-rest | base | proposed |
| dotj-refit | dotj-json | base | proposed |
| dotj-refit | dotj-code | dev-optional | proposed |
| dotj-mqtt | dotj-core | base | proposed |
| dotj-mqtt | dotj-web | optional | proposed |
| dotj-versioning | dotj-web | base | proposed |
| dotj-swagger | dotj-web | base | proposed |
| dotj-swagger | dotj-openapi | base | proposed |
| dotj-openapi | dotj-json | base | proposed |
| dotj-openapi | dotj-code | dev-optional | proposed |
| dotj-graph-platform | dotj-web | base | proposed |
| dotj-graph-platform | dotj-json | base | proposed |
| dotj-graph-platform | dotj-core | base | proposed |
| dotj-graphql | dotj-core | base | proposed |
| dotj-graphql | dotj-json | base | proposed |
| dotj-graphql | dotj-web | optional | proposed |
| dotj-presentation | dotj-core | base | proposed |
| dotj-presentation | dotj-toolkit | base | proposed |
| dotj-forms | dotj-core | base | proposed |
| dotj-multiui | dotj-core | base | proposed |
| dotj-multiui | dotj-toolkit | base | proposed |
| dotj-multiui | dotj-presentation | optional | proposed |
| dotj-avalonia | dotj-core | base | proposed |
| dotj-avalonia | dotj-toolkit | base | proposed |
| dotj-uno | dotj-core | base | proposed |
| dotj-uno | dotj-toolkit | base | proposed |
| dotj-uno | dotj-web | optional | proposed |
| dotj-toolkit | dotj-core | base | proposed |
| dotj-material | dotj-web | base | proposed |
| dotj-material | dotj-validation | base | proposed |
| dotj-components | dotj-web | base | proposed |
| dotj-structured-log | dotj-core | base | proposed |
| dotj-log | dotj-core | base | proposed |
| dotj-xtest | dotj-core | base | proposed |
| dotj-test | dotj-core | base | proposed |
| dotj-mock | dotj-core | base | proposed |
| dotj-substitute | dotj-core | base | proposed |
| dotj-substitute | dotj-mock | optional-spi | proposed |
| dotj-coverage | dotj-core | base | proposed |
| dotj-benchmark | dotj-core | base | proposed |
| dotj-benchmark | dotj-diagnostics | optional | proposed |
| dotj-testcontainers | dotj-core | base | proposed |
| dotj-excel | dotj-openxml | base | proposed |
| dotj-excel | dotj-core | base | proposed |
| dotj-openxml | dotj-core | base | proposed |
| dotj-markdown | dotj-core | base | proposed |
| dotj-ml | dotj-core | base | proposed |
| dotj-semantic | dotj-json | base | proposed |
| dotj-semantic | dotj-rest | base | proposed |
| dotj-semantic | dotj-extensions | base | proposed |
| dotj-packages | dotj-core | base | proposed |
| dotj-packages | dotj-json | base | proposed |
| dotj-registry | dotj-web | base | proposed |
| dotj-registry | dotj-packages | base | proposed |
| dotj-registry | dotj-postgresql | base | proposed |
| dotj-registry | dotj-auth | base | proposed |
| dotj-automap | dotj-core | base | proposed |
| dotj-automap | dotj-entity | optional | proposed |
| dotj-mediator | dotj-core | base | proposed |
| dotj-mediator | dotj-container | optional | proposed |
| dotj-bus | dotj-core | base | proposed |
| dotj-bus | dotj-json | base | proposed |
| dotj-bus | dotj-resilience | base | proposed |
| dotj-bus | dotj-postgresql | optional | proposed |
| dotj-bus | dotj-scheduler | optional | proposed |

## Actual Microsoft.Extensions project locations

These paths were observed in pinned listings. Project files are structural evidence; conditional build/restored package closure remains E02 work.

| Project | Target owner | Source |
|---|---|---|
| Microsoft.Extensions.Caching.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.Caching.Abstractions/src/Microsoft.Extensions.Caching.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Caching.Abstractions/src/Microsoft.Extensions.Caching.Abstractions.csproj) |
| Microsoft.Extensions.Caching.Memory | dotj-core | [src/libraries/Microsoft.Extensions.Caching.Memory/src/Microsoft.Extensions.Caching.Memory.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Caching.Memory/src/Microsoft.Extensions.Caching.Memory.csproj) |
| Microsoft.Extensions.Configuration.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Abstractions/src/Microsoft.Extensions.Configuration.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Abstractions/src/Microsoft.Extensions.Configuration.Abstractions.csproj) |
| Microsoft.Extensions.Configuration.Binder.SourceGeneration | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Binder/gen/Microsoft.Extensions.Configuration.Binder.SourceGeneration.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Binder/gen/Microsoft.Extensions.Configuration.Binder.SourceGeneration.csproj) |
| Microsoft.Extensions.Configuration.Binder | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Binder/src/Microsoft.Extensions.Configuration.Binder.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Binder/src/Microsoft.Extensions.Configuration.Binder.csproj) |
| Microsoft.Extensions.Configuration.CommandLine | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.CommandLine/src/Microsoft.Extensions.Configuration.CommandLine.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.CommandLine/src/Microsoft.Extensions.Configuration.CommandLine.csproj) |
| Microsoft.Extensions.Configuration.EnvironmentVariables | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.EnvironmentVariables/src/Microsoft.Extensions.Configuration.EnvironmentVariables.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.EnvironmentVariables/src/Microsoft.Extensions.Configuration.EnvironmentVariables.csproj) |
| Microsoft.Extensions.Configuration.FileExtensions | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.FileExtensions/src/Microsoft.Extensions.Configuration.FileExtensions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.FileExtensions/src/Microsoft.Extensions.Configuration.FileExtensions.csproj) |
| Microsoft.Extensions.Configuration.Ini | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Ini/src/Microsoft.Extensions.Configuration.Ini.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Ini/src/Microsoft.Extensions.Configuration.Ini.csproj) |
| Microsoft.Extensions.Configuration.Json | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Json/src/Microsoft.Extensions.Configuration.Json.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Json/src/Microsoft.Extensions.Configuration.Json.csproj) |
| Microsoft.Extensions.Configuration.UserSecrets | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.UserSecrets/src/Microsoft.Extensions.Configuration.UserSecrets.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.UserSecrets/src/Microsoft.Extensions.Configuration.UserSecrets.csproj) |
| Microsoft.Extensions.Configuration.Xml | dotj-core | [src/libraries/Microsoft.Extensions.Configuration.Xml/src/Microsoft.Extensions.Configuration.Xml.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Xml/src/Microsoft.Extensions.Configuration.Xml.csproj) |
| Microsoft.Extensions.Configuration | dotj-core | [src/libraries/Microsoft.Extensions.Configuration/src/Microsoft.Extensions.Configuration.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration/src/Microsoft.Extensions.Configuration.csproj) |
| Microsoft.Extensions.DependencyInjection.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.DependencyInjection.Abstractions/src/Microsoft.Extensions.DependencyInjection.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection.Abstractions/src/Microsoft.Extensions.DependencyInjection.Abstractions.csproj) |
| Microsoft.Extensions.DependencyInjection | dotj-core | [src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/src/Microsoft.Extensions.DependencyInjection.csproj) |
| Microsoft.Extensions.DependencyModel | dotj-core | [src/libraries/Microsoft.Extensions.DependencyModel/src/Microsoft.Extensions.DependencyModel.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyModel/src/Microsoft.Extensions.DependencyModel.csproj) |
| Microsoft.Extensions.Diagnostics.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.Diagnostics.Abstractions/src/Microsoft.Extensions.Diagnostics.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Diagnostics.Abstractions/src/Microsoft.Extensions.Diagnostics.Abstractions.csproj) |
| Microsoft.Extensions.Diagnostics | dotj-core | [src/libraries/Microsoft.Extensions.Diagnostics/src/Microsoft.Extensions.Diagnostics.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Diagnostics/src/Microsoft.Extensions.Diagnostics.csproj) |
| Microsoft.Extensions.FileProviders.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.FileProviders.Abstractions/src/Microsoft.Extensions.FileProviders.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Abstractions/src/Microsoft.Extensions.FileProviders.Abstractions.csproj) |
| Microsoft.Extensions.FileProviders.Composite | dotj-core | [src/libraries/Microsoft.Extensions.FileProviders.Composite/src/Microsoft.Extensions.FileProviders.Composite.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Composite/src/Microsoft.Extensions.FileProviders.Composite.csproj) |
| Microsoft.Extensions.FileProviders.Physical | dotj-core | [src/libraries/Microsoft.Extensions.FileProviders.Physical/src/Microsoft.Extensions.FileProviders.Physical.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Physical/src/Microsoft.Extensions.FileProviders.Physical.csproj) |
| Microsoft.Extensions.FileSystemGlobbing | dotj-core | [src/libraries/Microsoft.Extensions.FileSystemGlobbing/src/Microsoft.Extensions.FileSystemGlobbing.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileSystemGlobbing/src/Microsoft.Extensions.FileSystemGlobbing.csproj) |
| Microsoft.Extensions.HostFactoryResolver.Sources | dotj-core | [src/libraries/Microsoft.Extensions.HostFactoryResolver/src/Microsoft.Extensions.HostFactoryResolver.Sources.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.HostFactoryResolver/src/Microsoft.Extensions.HostFactoryResolver.Sources.csproj) |
| Microsoft.Extensions.Hosting.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.Hosting.Abstractions/src/Microsoft.Extensions.Hosting.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.Abstractions/src/Microsoft.Extensions.Hosting.Abstractions.csproj) |
| Microsoft.Extensions.Hosting.Systemd | dotj-core | [src/libraries/Microsoft.Extensions.Hosting.Systemd/src/Microsoft.Extensions.Hosting.Systemd.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.Systemd/src/Microsoft.Extensions.Hosting.Systemd.csproj) |
| Microsoft.Extensions.Hosting.WindowsServices | dotj-core | [src/libraries/Microsoft.Extensions.Hosting.WindowsServices/src/Microsoft.Extensions.Hosting.WindowsServices.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.WindowsServices/src/Microsoft.Extensions.Hosting.WindowsServices.csproj) |
| Microsoft.Extensions.Hosting | dotj-core | [src/libraries/Microsoft.Extensions.Hosting/src/Microsoft.Extensions.Hosting.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting/src/Microsoft.Extensions.Hosting.csproj) |
| Microsoft.Extensions.Http | dotj-core | [src/libraries/Microsoft.Extensions.Http/src/Microsoft.Extensions.Http.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Http/src/Microsoft.Extensions.Http.csproj) |
| Microsoft.Extensions.Logging.Generators.Roslyn3.11 | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn3.11.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn3.11.csproj) |
| Microsoft.Extensions.Logging.Generators.Roslyn4.0 | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn4.0.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn4.0.csproj) |
| Microsoft.Extensions.Logging.Generators.Roslyn4.4 | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn4.4.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Abstractions/gen/Microsoft.Extensions.Logging.Generators.Roslyn4.4.csproj) |
| Microsoft.Extensions.Logging.Abstractions | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Abstractions/src/Microsoft.Extensions.Logging.Abstractions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Abstractions/src/Microsoft.Extensions.Logging.Abstractions.csproj) |
| Microsoft.Extensions.Logging.Configuration | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Configuration/src/Microsoft.Extensions.Logging.Configuration.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Configuration/src/Microsoft.Extensions.Logging.Configuration.csproj) |
| Microsoft.Extensions.Logging.Console | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Console/src/Microsoft.Extensions.Logging.Console.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Console/src/Microsoft.Extensions.Logging.Console.csproj) |
| Microsoft.Extensions.Logging.Debug | dotj-core | [src/libraries/Microsoft.Extensions.Logging.Debug/src/Microsoft.Extensions.Logging.Debug.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Debug/src/Microsoft.Extensions.Logging.Debug.csproj) |
| Microsoft.Extensions.Logging.EventLog | dotj-core | [src/libraries/Microsoft.Extensions.Logging.EventLog/src/Microsoft.Extensions.Logging.EventLog.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.EventLog/src/Microsoft.Extensions.Logging.EventLog.csproj) |
| Microsoft.Extensions.Logging.EventSource | dotj-core | [src/libraries/Microsoft.Extensions.Logging.EventSource/src/Microsoft.Extensions.Logging.EventSource.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.EventSource/src/Microsoft.Extensions.Logging.EventSource.csproj) |
| Microsoft.Extensions.Logging.TraceSource | dotj-core | [src/libraries/Microsoft.Extensions.Logging.TraceSource/src/Microsoft.Extensions.Logging.TraceSource.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.TraceSource/src/Microsoft.Extensions.Logging.TraceSource.csproj) |
| Microsoft.Extensions.Logging | dotj-core | [src/libraries/Microsoft.Extensions.Logging/src/Microsoft.Extensions.Logging.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging/src/Microsoft.Extensions.Logging.csproj) |
| Microsoft.Extensions.Options.ConfigurationExtensions | dotj-core | [src/libraries/Microsoft.Extensions.Options.ConfigurationExtensions/src/Microsoft.Extensions.Options.ConfigurationExtensions.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options.ConfigurationExtensions/src/Microsoft.Extensions.Options.ConfigurationExtensions.csproj) |
| Microsoft.Extensions.Options.DataAnnotations | dotj-core | [src/libraries/Microsoft.Extensions.Options.DataAnnotations/src/Microsoft.Extensions.Options.DataAnnotations.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options.DataAnnotations/src/Microsoft.Extensions.Options.DataAnnotations.csproj) |
| Microsoft.Extensions.Options.SourceGeneration | dotj-core | [src/libraries/Microsoft.Extensions.Options/gen/Microsoft.Extensions.Options.SourceGeneration.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options/gen/Microsoft.Extensions.Options.SourceGeneration.csproj) |
| Microsoft.Extensions.Options | dotj-core | [src/libraries/Microsoft.Extensions.Options/src/Microsoft.Extensions.Options.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options/src/Microsoft.Extensions.Options.csproj) |
| Microsoft.Extensions.Primitives | dotj-core | [src/libraries/Microsoft.Extensions.Primitives/src/Microsoft.Extensions.Primitives.csproj](https://github.com/dotnet/runtime/blob/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Primitives/src/Microsoft.Extensions.Primitives.csproj) |
| Microsoft.Extensions.AI.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Abstractions/Microsoft.Extensions.AI.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Abstractions/Microsoft.Extensions.AI.Abstractions.csproj) |
| Microsoft.Extensions.AI.Evaluation.Console | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.Console/Microsoft.Extensions.AI.Evaluation.Console.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.Console/Microsoft.Extensions.AI.Evaluation.Console.csproj) |
| Microsoft.Extensions.AI.Evaluation.NLP | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.NLP/Microsoft.Extensions.AI.Evaluation.NLP.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.NLP/Microsoft.Extensions.AI.Evaluation.NLP.csproj) |
| Microsoft.Extensions.AI.Evaluation.Quality | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.Quality/Microsoft.Extensions.AI.Evaluation.Quality.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.Quality/Microsoft.Extensions.AI.Evaluation.Quality.csproj) |
| Microsoft.Extensions.AI.Evaluation.Reporting.Azure | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.Reporting.Azure/Microsoft.Extensions.AI.Evaluation.Reporting.Azure.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.Reporting.Azure/Microsoft.Extensions.AI.Evaluation.Reporting.Azure.csproj) |
| Microsoft.Extensions.AI.Evaluation.Reporting | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.Reporting/CSharp/Microsoft.Extensions.AI.Evaluation.Reporting.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.Reporting/CSharp/Microsoft.Extensions.AI.Evaluation.Reporting.csproj) |
| Microsoft.Extensions.AI.Evaluation.Safety | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation.Safety/Microsoft.Extensions.AI.Evaluation.Safety.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation.Safety/Microsoft.Extensions.AI.Evaluation.Safety.csproj) |
| Microsoft.Extensions.AI.Evaluation | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.Evaluation/Microsoft.Extensions.AI.Evaluation.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.Evaluation/Microsoft.Extensions.AI.Evaluation.csproj) |
| Microsoft.Extensions.AI.OpenAI | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI.OpenAI/Microsoft.Extensions.AI.OpenAI.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI.OpenAI/Microsoft.Extensions.AI.OpenAI.csproj) |
| Microsoft.Extensions.AI | dotj-extensions | [src/Libraries/Microsoft.Extensions.AI/Microsoft.Extensions.AI.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AI/Microsoft.Extensions.AI.csproj) |
| Microsoft.Extensions.AmbientMetadata.Application | dotj-extensions | [src/Libraries/Microsoft.Extensions.AmbientMetadata.Application/Microsoft.Extensions.AmbientMetadata.Application.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AmbientMetadata.Application/Microsoft.Extensions.AmbientMetadata.Application.csproj) |
| Microsoft.Extensions.AmbientMetadata.Build | dotj-extensions | [src/Libraries/Microsoft.Extensions.AmbientMetadata.Build/Microsoft.Extensions.AmbientMetadata.Build.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AmbientMetadata.Build/Microsoft.Extensions.AmbientMetadata.Build.csproj) |
| Microsoft.Extensions.AsyncState | dotj-extensions | [src/Libraries/Microsoft.Extensions.AsyncState/Microsoft.Extensions.AsyncState.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.AsyncState/Microsoft.Extensions.AsyncState.csproj) |
| Microsoft.Extensions.Caching.Hybrid | dotj-extensions | [src/Libraries/Microsoft.Extensions.Caching.Hybrid/Microsoft.Extensions.Caching.Hybrid.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Caching.Hybrid/Microsoft.Extensions.Caching.Hybrid.csproj) |
| Microsoft.Extensions.Compliance.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.Compliance.Abstractions/Microsoft.Extensions.Compliance.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Compliance.Abstractions/Microsoft.Extensions.Compliance.Abstractions.csproj) |
| Microsoft.Extensions.Compliance.Redaction | dotj-extensions | [src/Libraries/Microsoft.Extensions.Compliance.Redaction/Microsoft.Extensions.Compliance.Redaction.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Compliance.Redaction/Microsoft.Extensions.Compliance.Redaction.csproj) |
| Microsoft.Extensions.DataIngestion.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.DataIngestion.Abstractions/Microsoft.Extensions.DataIngestion.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.DataIngestion.Abstractions/Microsoft.Extensions.DataIngestion.Abstractions.csproj) |
| Microsoft.Extensions.DataIngestion.MarkItDown | dotj-extensions | [src/Libraries/Microsoft.Extensions.DataIngestion.MarkItDown/Microsoft.Extensions.DataIngestion.MarkItDown.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.DataIngestion.MarkItDown/Microsoft.Extensions.DataIngestion.MarkItDown.csproj) |
| Microsoft.Extensions.DataIngestion.Markdig | dotj-extensions | [src/Libraries/Microsoft.Extensions.DataIngestion.Markdig/Microsoft.Extensions.DataIngestion.Markdig.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.DataIngestion.Markdig/Microsoft.Extensions.DataIngestion.Markdig.csproj) |
| Microsoft.Extensions.DataIngestion | dotj-extensions | [src/Libraries/Microsoft.Extensions.DataIngestion/Microsoft.Extensions.DataIngestion.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.DataIngestion/Microsoft.Extensions.DataIngestion.csproj) |
| Microsoft.Extensions.DependencyInjection.AutoActivation | dotj-extensions | [src/Libraries/Microsoft.Extensions.DependencyInjection.AutoActivation/Microsoft.Extensions.DependencyInjection.AutoActivation.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.DependencyInjection.AutoActivation/Microsoft.Extensions.DependencyInjection.AutoActivation.csproj) |
| Microsoft.Extensions.Diagnostics.ExceptionSummarization | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.ExceptionSummarization/Microsoft.Extensions.Diagnostics.ExceptionSummarization.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.ExceptionSummarization/Microsoft.Extensions.Diagnostics.ExceptionSummarization.csproj) |
| Microsoft.Extensions.Diagnostics.HealthChecks.Common | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.HealthChecks.Common/Microsoft.Extensions.Diagnostics.HealthChecks.Common.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.HealthChecks.Common/Microsoft.Extensions.Diagnostics.HealthChecks.Common.csproj) |
| Microsoft.Extensions.Diagnostics.HealthChecks.ResourceUtilization | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.HealthChecks.ResourceUtilization/Microsoft.Extensions.Diagnostics.HealthChecks.ResourceUtilization.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.HealthChecks.ResourceUtilization/Microsoft.Extensions.Diagnostics.HealthChecks.ResourceUtilization.csproj) |
| Microsoft.Extensions.Diagnostics.Probes | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.Probes/Microsoft.Extensions.Diagnostics.Probes.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.Probes/Microsoft.Extensions.Diagnostics.Probes.csproj) |
| Microsoft.Extensions.Diagnostics.ResourceMonitoring.Kubernetes | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.ResourceMonitoring.Kubernetes/Microsoft.Extensions.Diagnostics.ResourceMonitoring.Kubernetes.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.ResourceMonitoring.Kubernetes/Microsoft.Extensions.Diagnostics.ResourceMonitoring.Kubernetes.csproj) |
| Microsoft.Extensions.Diagnostics.ResourceMonitoring | dotj-extensions | [src/Libraries/Microsoft.Extensions.Diagnostics.ResourceMonitoring/Microsoft.Extensions.Diagnostics.ResourceMonitoring.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Diagnostics.ResourceMonitoring/Microsoft.Extensions.Diagnostics.ResourceMonitoring.csproj) |
| Microsoft.Extensions.Http.Diagnostics | dotj-extensions | [src/Libraries/Microsoft.Extensions.Http.Diagnostics/Microsoft.Extensions.Http.Diagnostics.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Http.Diagnostics/Microsoft.Extensions.Http.Diagnostics.csproj) |
| Microsoft.Extensions.Http.Resilience | dotj-extensions | [src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Http.Resilience/Microsoft.Extensions.Http.Resilience.csproj) |
| Microsoft.Extensions.ObjectPool.DependencyInjection | dotj-extensions | [src/Libraries/Microsoft.Extensions.ObjectPool.DependencyInjection/Microsoft.Extensions.ObjectPool.DependencyInjection.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.ObjectPool.DependencyInjection/Microsoft.Extensions.ObjectPool.DependencyInjection.csproj) |
| Microsoft.Extensions.Options.Contextual | dotj-extensions | [src/Libraries/Microsoft.Extensions.Options.Contextual/Microsoft.Extensions.Options.Contextual.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Options.Contextual/Microsoft.Extensions.Options.Contextual.csproj) |
| Microsoft.Extensions.Resilience | dotj-extensions | [src/Libraries/Microsoft.Extensions.Resilience/Microsoft.Extensions.Resilience.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Resilience/Microsoft.Extensions.Resilience.csproj) |
| Microsoft.Extensions.ServiceDiscovery.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.ServiceDiscovery.Abstractions/Microsoft.Extensions.ServiceDiscovery.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.ServiceDiscovery.Abstractions/Microsoft.Extensions.ServiceDiscovery.Abstractions.csproj) |
| Microsoft.Extensions.ServiceDiscovery.Dns | dotj-extensions | [src/Libraries/Microsoft.Extensions.ServiceDiscovery.Dns/Microsoft.Extensions.ServiceDiscovery.Dns.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.ServiceDiscovery.Dns/Microsoft.Extensions.ServiceDiscovery.Dns.csproj) |
| Microsoft.Extensions.ServiceDiscovery.Yarp | dotj-extensions | [src/Libraries/Microsoft.Extensions.ServiceDiscovery.Yarp/Microsoft.Extensions.ServiceDiscovery.Yarp.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.ServiceDiscovery.Yarp/Microsoft.Extensions.ServiceDiscovery.Yarp.csproj) |
| Microsoft.Extensions.ServiceDiscovery | dotj-extensions | [src/Libraries/Microsoft.Extensions.ServiceDiscovery/Microsoft.Extensions.ServiceDiscovery.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.ServiceDiscovery/Microsoft.Extensions.ServiceDiscovery.csproj) |
| Microsoft.Extensions.Telemetry.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.Telemetry.Abstractions/Microsoft.Extensions.Telemetry.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Telemetry.Abstractions/Microsoft.Extensions.Telemetry.Abstractions.csproj) |
| Microsoft.Extensions.Telemetry | dotj-extensions | [src/Libraries/Microsoft.Extensions.Telemetry/Microsoft.Extensions.Telemetry.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.Telemetry/Microsoft.Extensions.Telemetry.csproj) |
| Microsoft.Extensions.VectorData.Abstractions | dotj-extensions | [src/Libraries/Microsoft.Extensions.VectorData.Abstractions/Microsoft.Extensions.VectorData.Abstractions.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Libraries/Microsoft.Extensions.VectorData.Abstractions/Microsoft.Extensions.VectorData.Abstractions.csproj) |
| Microsoft.Extensions.AuditReports | dotj-extensions | [src/Packages/Microsoft.Extensions.AuditReports/Microsoft.Extensions.AuditReports.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Packages/Microsoft.Extensions.AuditReports/Microsoft.Extensions.AuditReports.csproj) |
| Microsoft.Extensions.StaticAnalysis | dotj-extensions | [src/Packages/Microsoft.Extensions.StaticAnalysis/Microsoft.Extensions.StaticAnalysis.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/Packages/Microsoft.Extensions.StaticAnalysis/Microsoft.Extensions.StaticAnalysis.csproj) |
| Microsoft.Extensions.AI.Templates | dotj-extensions | [src/ProjectTemplates/Microsoft.Extensions.AI.Templates/Microsoft.Extensions.AI.Templates.csproj](https://github.com/dotnet/extensions/blob/42a0f358b14bb27bc324939d858dd04309f30477/src/ProjectTemplates/Microsoft.Extensions.AI.Templates/Microsoft.Extensions.AI.Templates.csproj) |

## Additional upstream source/dependency ledger

These candidates require explicit source/version/license closure, not an automatic addition to the product count or permission to substitute a Java framework.

| Consumer | Additional source/component | Required disposition |
|---|---|---|
| mail | MimeKit submodule/source | Own MIME scope under mail or explicitly justify a bounded dependency; verify submodule commit |
| openapi | NJsonSchema and template-engine dependencies | Own schema/generator scope; canonical source and actual resolved version |
| swagger | Microsoft.OpenApi models; Swagger UI/ReDoc assets | Neutral model contract and separately reviewed browser assets |
| mock/substitute | Castle/DynamicProxy references | Owned JVM proxy/bytecode design; source/reference eligibility |
| jobs | Cronos and storage/commercial extensions | Versioned cron behavior and separate rights scope |
| graph-platform | Product subtrees, tooling and optional commercial services | Retain open C# scope; distinguish separately licensed functionality |
| presentation/forms | Win32/COM/DirectWrite/graphics/SDK inputs | ABI, native binding, OS and redistribution evidence |
| avalonia/uno/multiui | Skia/HarfBuzz/fonts/platform SDKs | Per-backend source/binary/license records and executable feasibility |
| testcontainers | Docker engine protocol; cleanup/reaper image | Owned engine client; independently pinned helper image/source |
| ml | Native math/ONNX/TensorFlow-related inputs | Actual trainer/module use and narrow ABI/model-format qualification |
| auth | IdentityModel/JOSE sources and protocol profiles | Own protocol processing with JDK crypto; algorithm-specific evidence |
| aspire | DCP/orchestration/dashboard assets | Build-tool/runtime separation and canonical source/version closure |
| xtest/test | Runner engines/IDE adapters outside main source | Additional source entries without hiding missing behavior |
| excel | Formula/parser/calculation and format dependencies | Exact consumed source/version and owned implementation plan |
| semantic | Microsoft Agent Framework successor | Reference only unless scope explicitly expands |


For each dependency create UD-target-NNN with consuming module, source declaration/condition, canonical URL, resolved version/hash, runtime/dev/test/native/asset role, license evidence, disposition, required notices, gate owner and affected work packages. Observed PackageReference declarations are included per repository; they are not a full transitive graph.
