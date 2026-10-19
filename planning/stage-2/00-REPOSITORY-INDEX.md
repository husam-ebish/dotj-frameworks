# All 66 Stage-2 repository plans

**Owner requirement:** exact upstream .NET public names, casing and concepts across all 66 repositories. Read [the mandatory naming policy](08-DOTNET-API-COMPATIBILITY-POLICY.md). N01 adds a source-to-Java public API mapping and concept-preservation gate; Java implementation details must not become a replacement learning path.

All rows have the eleven required detailed documents, a navigation README and machine-readable evidence. Written planning coverage is complete across the retained capability families. Exhaustive API/test/dependency audits, eligible release qualification and implementation remain separate statuses.

| ID | Target | Upstream | Feature + integration packages | Wave | Source evidence |
|---|---|---|---|---|---|
| DJ-001 | [dotj-core](repos/dotj-core/README.md) | [.NET runtime and base libraries](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819) | 9 | 1 | partial listing; sampled semantics |
| DJ-002 | [dotj-sdk](repos/dotj-sdk/README.md) | [.NET SDK](https://github.com/dotnet/sdk/tree/c70b3856e7948678daa3950ec5517759754bf47c) | 12 | 5 | recursive complete; sampled semantics |
| DJ-003 | [dotj-code](repos/dotj-code/README.md) | [Roslyn](https://github.com/dotnet/roslyn/tree/3645b6aa36ad41775a73e57a620787a3d38327a0) | 5 | 1 | recursive complete; sampled semantics |
| DJ-004 | [dotj-razor](repos/dotj-razor/README.md) | [Razor](https://github.com/dotnet/roslyn/tree/3645b6aa36ad41775a73e57a620787a3d38327a0) | 5 | 4 | recursive complete; sampled semantics |
| DJ-005 | [dotj-build](repos/dotj-build/README.md) | [MSBuild](https://github.com/dotnet/msbuild/tree/6348d0c087aeec18c323b01a2c77da089ddafea0) | 7 | 1 | recursive complete; sampled semantics |
| DJ-006 | [dotj-extensions](repos/dotj-extensions/README.md) | [.NET Extensions](https://github.com/dotnet/extensions/tree/42a0f358b14bb27bc324939d858dd04309f30477) | 5 | 2 | recursive complete; sampled semantics |
| DJ-007 | [dotj-diagnostics](repos/dotj-diagnostics/README.md) | [.NET diagnostics](https://github.com/dotnet/diagnostics/tree/1d95e75015fa3ccd063a59ed3d0bfe26040a6637) | 5 | 5 | recursive complete; sampled semantics |
| DJ-008 | [dotj-interactive](repos/dotj-interactive/README.md) | [.NET Interactive](https://github.com/dotnet/interactive/tree/098a01b9183103186805a186a7dee3a3a70b2997) | 5 | 5 | recursive complete; sampled semantics |
| DJ-009 | [dotj-scaffold](repos/dotj-scaffold/README.md) | [.NET scaffolding](https://github.com/dotnet/Scaffolding/tree/107111c945bcf1264c035457a0744318b6bae3d9) | 5 | 5 | recursive complete; sampled semantics |
| DJ-010 | [dotj-templates](repos/dotj-templates/README.md) | [.NET template engine](https://github.com/dotnet/sdk/tree/c70b3856e7948678daa3950ec5517759754bf47c) | 6 | 1 | recursive complete; sampled semantics |
| DJ-011 | [dotj-containers](repos/dotj-containers/README.md) | [.NET container images](https://github.com/dotnet/dotnet-docker/tree/a5ada4c290f2dc087c6926beeeaffcd07912abe7) | 5 | 5 | recursive complete; sampled semantics |
| DJ-012 | [dotj-web](repos/dotj-web/README.md) | [ASP.NET Core](https://github.com/dotnet/aspnetcore/tree/c09e2b89bd8cf25e819230a94e9061023f508afe) | 8 | 4 | recursive complete; sampled semantics |
| DJ-013 | [dotj-aspire](repos/dotj-aspire/README.md) | [Aspire](https://github.com/microsoft/aspire/tree/118781118dddea1f7a524ab3d244fa4cee3c62cf) | 5 | 5 | recursive complete; sampled semantics |
| DJ-014 | [dotj-proxy](repos/dotj-proxy/README.md) | [YARP](https://github.com/dotnet/yarp/tree/2aa3d83550a9b7a719e347ef6a0363e5ea9505a9) | 5 | 4 | recursive complete; sampled semantics |
| DJ-015 | [dotj-actors](repos/dotj-actors/README.md) | [Orleans](https://github.com/dotnet/orleans/tree/9f8310cb6e5bbe35cd3bbb0752052993578eb083) | 5 | 4 | recursive complete; sampled semantics |
| DJ-016 | [dotj-auth](repos/dotj-auth/README.md) | [OpenIddict](https://github.com/openiddict/openiddict-core/tree/ab23a1625279b8b656912202c2b81a63d3438ca6) | 5 | 4 | recursive complete; sampled semantics |
| DJ-017 | [dotj-service-client](repos/dotj-service-client/README.md) | [WCF client libraries](https://github.com/dotnet/wcf/tree/d2d2036c3839b5dee95545ee08c613cfd34b86be) | 5 | 3 | recursive complete; sampled semantics |
| DJ-018 | [dotj-services](repos/dotj-services/README.md) | [CoreWCF](https://github.com/CoreWCF/CoreWCF/tree/6e2cce88349fe41056fe8afda0dbbdf98d54bb00) | 5 | 4 | recursive complete; sampled semantics |
| DJ-019 | [dotj-entity](repos/dotj-entity/README.md) | [Entity Framework Core](https://github.com/dotnet/efcore/tree/2e8882748cc45b317a98a6f27f0680948221ae3b) | 6 | 3 | recursive complete; sampled semantics |
| DJ-020 | [dotj-sql](repos/dotj-sql/README.md) | [Dapper](https://github.com/DapperLib/Dapper/tree/eb47546a408bbf6c178bda4f04dc205bc51ffbfe) | 5 | 3 | recursive complete; sampled semantics |
| DJ-021 | [dotj-postgresql](repos/dotj-postgresql/README.md) | [Npgsql](https://github.com/npgsql/npgsql/tree/1083526ef25018bd65772f18f313240fd36037bb) | 6 | 2 | recursive complete; sampled semantics |
| DJ-022 | [dotj-redis](repos/dotj-redis/README.md) | [StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis/tree/84765eede5c49419ed251a9cfc491a2d58667fb9) | 5 | 2 | recursive complete; sampled semantics |
| DJ-023 | [dotj-json](repos/dotj-json/README.md) | [Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json/tree/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa) | 5 | 1 | recursive complete; sampled semantics |
| DJ-024 | [dotj-mapster](repos/dotj-mapster/README.md) | [Mapster](https://github.com/MapsterMapper/Mapster/tree/cbc1e5f04e6e003744b04f83d4705670a85e459b) | 5 | 3 | recursive complete; sampled semantics |
| DJ-025 | [dotj-container](repos/dotj-container/README.md) | [Autofac](https://github.com/autofac/Autofac/tree/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2) | 5 | 2 | recursive complete; sampled semantics |
| DJ-026 | [dotj-validation](repos/dotj-validation/README.md) | [FluentValidation](https://github.com/FluentValidation/FluentValidation/tree/299ef377bde844af7d28b7aa21786a6853f930e3) | 5 | 2 | recursive complete; sampled semantics |
| DJ-027 | [dotj-resilience](repos/dotj-resilience/README.md) | [Polly](https://github.com/App-vNext/Polly/tree/3f3adad9d5af85658fc3585018f02a2d8c2173e8) | 5 | 2 | recursive complete; sampled semantics |
| DJ-028 | [dotj-reactive](repos/dotj-reactive/README.md) | [Reactive Extensions](https://github.com/dotnet/reactive/tree/89e05b8730107983c3f77af54a52974ae12d37f4) | 5 | 2 | recursive complete; sampled semantics |
| DJ-029 | [dotj-jobs](repos/dotj-jobs/README.md) | [Hangfire](https://github.com/HangfireIO/Hangfire/tree/c35077110cc8364b06ea30d39947bd5f688b2e8b) | 5 | 4 | recursive complete; sampled semantics |
| DJ-030 | [dotj-scheduler](repos/dotj-scheduler/README.md) | [Quartz.NET](https://github.com/quartznet/quartznet/tree/a94922ad3b1c2efa6d2613916fa2f386aede6681) | 5 | 3 | recursive complete; sampled semantics |
| DJ-031 | [dotj-mail](repos/dotj-mail/README.md) | [MailKit](https://github.com/jstedfast/MailKit/tree/7418d38dc27a47d8db9108d8fa994b2b784f1578) | 5 | 3 | recursive complete; sampled semantics |
| DJ-032 | [dotj-rest](repos/dotj-rest/README.md) | [RestSharp](https://github.com/restsharp/RestSharp/tree/64ee12995b8d7409a5863da7b71cddfa526ffb7a) | 5 | 3 | recursive complete; sampled semantics |
| DJ-033 | [dotj-refit](repos/dotj-refit/README.md) | [Refit](https://github.com/reactiveui/refit/tree/92ae878250798dc103a01304704a99bb8033ed77) | 5 | 3 | recursive complete; sampled semantics |
| DJ-034 | [dotj-mqtt](repos/dotj-mqtt/README.md) | [MQTTnet](https://github.com/dotnet/MQTTnet/tree/798a0e2250f40a241e0c8d2e7c9a366051be1b97) | 5 | 3 | recursive complete; sampled semantics |
| DJ-035 | [dotj-versioning](repos/dotj-versioning/README.md) | [ASP.NET API Versioning](https://github.com/dotnet/aspnet-api-versioning/tree/1a22bb4281c03d44f387169eefa46765a6219118) | 5 | 4 | recursive complete; sampled semantics |
| DJ-036 | [dotj-swagger](repos/dotj-swagger/README.md) | [Swashbuckle](https://github.com/domaindrivendev/Swashbuckle.AspNetCore/tree/1e2b358b23cb9f041e8a395d4541d46566be7f81) | 5 | 4 | recursive complete; sampled semantics |
| DJ-037 | [dotj-openapi](repos/dotj-openapi/README.md) | [NSwag](https://github.com/RicoSuter/NSwag/tree/63daf8fcc3a25151b62eb4b326a1e8ea048a0d41) | 8 | 4 | recursive complete; sampled semantics |
| DJ-038 | [dotj-graph-platform](repos/dotj-graph-platform/README.md) | [Hot Chocolate / Strawberry Shake](https://github.com/ChilliCream/graphql-platform/tree/284f0b5f44cf1670a546f5cb1a4311bab08ffd5c) | 5 | 4 | recursive complete; sampled semantics |
| DJ-039 | [dotj-graphql](repos/dotj-graphql/README.md) | [GraphQL.NET](https://github.com/graphql-dotnet/graphql-dotnet/tree/af0b3e77b874cc73167d70910103ac708f14ed28) | 5 | 4 | recursive complete; sampled semantics |
| DJ-040 | [dotj-presentation](repos/dotj-presentation/README.md) | [WPF](https://github.com/dotnet/wpf/tree/65d15adece1df9a73e3d1abc11f8bbf99e9fc7a9) | 5 | 6 | recursive complete; sampled semantics |
| DJ-041 | [dotj-forms](repos/dotj-forms/README.md) | [Windows Forms](https://github.com/dotnet/winforms/tree/c4891de0851184dcbe95d16ca543969fe2540245) | 5 | 6 | recursive complete; sampled semantics |
| DJ-042 | [dotj-multiui](repos/dotj-multiui/README.md) | [.NET MAUI](https://github.com/dotnet/maui/tree/3a7d72870b9c2ed006de7268a6257ae039cb7f99) | 5 | 6 | recursive complete; sampled semantics |
| DJ-043 | [dotj-avalonia](repos/dotj-avalonia/README.md) | [Avalonia](https://github.com/AvaloniaUI/Avalonia/tree/66b7273b9a2b5ba8416feb4376b9cdc3078b8573) | 5 | 6 | recursive complete; sampled semantics |
| DJ-044 | [dotj-uno](repos/dotj-uno/README.md) | [Uno Platform](https://github.com/unoplatform/uno/tree/78728530f26880286be77d9042a8e4118a42df43) | 5 | 6 | recursive complete; sampled semantics |
| DJ-045 | [dotj-toolkit](repos/dotj-toolkit/README.md) | [.NET Community Toolkit](https://github.com/CommunityToolkit/dotnet/tree/b135626dd54d33b8f05f2ff31591592c004aa848) | 5 | 2 | recursive complete; sampled semantics |
| DJ-046 | [dotj-material](repos/dotj-material/README.md) | [MudBlazor](https://github.com/MudBlazor/MudBlazor/tree/f28086704d9d488c3c200e74ff960022af34a6ef) | 6 | 6 | recursive complete; sampled semantics |
| DJ-047 | [dotj-components](repos/dotj-components/README.md) | [Radzen Blazor](https://github.com/radzenhq/radzen-blazor/tree/47709dc6fedfd92d66266017a0b50e0d327fa2c1) | 6 | 6 | recursive complete; sampled semantics |
| DJ-048 | [dotj-structured-log](repos/dotj-structured-log/README.md) | [Serilog](https://github.com/serilog/serilog/tree/81af75f3a5e28ec9f5be18ef74357a9914a51745) | 5 | 2 | recursive complete; sampled semantics |
| DJ-049 | [dotj-log](repos/dotj-log/README.md) | [NLog](https://github.com/NLog/NLog/tree/d9ebf823ee8ba54977c336709928a96ea58c6259) | 5 | 2 | recursive complete; sampled semantics |
| DJ-050 | [dotj-xtest](repos/dotj-xtest/README.md) | [xUnit.net](https://github.com/xunit/xunit/tree/e91cdbe7557649b1179fbc47b01e8d3a615d1256) | 5 | 1 | recursive complete; sampled semantics |
| DJ-051 | [dotj-test](repos/dotj-test/README.md) | [NUnit](https://github.com/nunit/nunit/tree/55d908f8cc4402f8d53955d20aefcee9f55a59ec) | 5 | 1 | recursive complete; sampled semantics |
| DJ-052 | [dotj-mock](repos/dotj-mock/README.md) | [Moq](https://github.com/devlooped/moq/tree/bdf16e758e8022c40cef2bfd025181f845bbd2a9) | 5 | 3 | recursive complete; sampled semantics |
| DJ-053 | [dotj-substitute](repos/dotj-substitute/README.md) | [NSubstitute](https://github.com/nsubstitute/NSubstitute/tree/f2b623d762fc28fc1a2fe3932b3b360d113c734d) | 5 | 3 | recursive complete; sampled semantics |
| DJ-054 | [dotj-coverage](repos/dotj-coverage/README.md) | [Coverlet](https://github.com/coverlet-coverage/coverlet/tree/b5ba9197f032e22627836d899aa3956a50cd5017) | 5 | 3 | recursive complete; sampled semantics |
| DJ-055 | [dotj-benchmark](repos/dotj-benchmark/README.md) | [BenchmarkDotNet](https://github.com/dotnet/BenchmarkDotNet/tree/730b8b7cc67b8d75a7478e67eaa2b10af5ec562d) | 5 | 3 | recursive complete; sampled semantics |
| DJ-056 | [dotj-testcontainers](repos/dotj-testcontainers/README.md) | [Testcontainers for .NET](https://github.com/testcontainers/testcontainers-dotnet/tree/84f485caeded1cf8f8f983ddd2c0163c47e258fa) | 5 | 3 | recursive complete; sampled semantics |
| DJ-057 | [dotj-excel](repos/dotj-excel/README.md) | [ClosedXML](https://github.com/ClosedXML/ClosedXML/tree/09f2f21a60e821ce7fb18ca3576b272e5dd6d921) | 5 | 3 | recursive complete; sampled semantics |
| DJ-058 | [dotj-openxml](repos/dotj-openxml/README.md) | [Open XML SDK](https://github.com/dotnet/Open-XML-SDK/tree/431ab05cf160248cc3885a4a766026d4f8243792) | 5 | 2 | recursive complete; sampled semantics |
| DJ-059 | [dotj-markdown](repos/dotj-markdown/README.md) | [Markdig](https://github.com/xoofx/markdig/tree/ccb9d8593f7a0aac232342a6705e8afc8c4f374d) | 5 | 2 | recursive complete; sampled semantics |
| DJ-060 | [dotj-ml](repos/dotj-ml/README.md) | [ML.NET](https://github.com/dotnet/machinelearning/tree/655f469b0d54bccf94dc251b8db457b57d56d084) | 5 | 5 | recursive complete; sampled semantics |
| DJ-061 | [dotj-semantic](repos/dotj-semantic/README.md) | [Semantic Kernel](https://github.com/microsoft/semantic-kernel/tree/7a92cd4e7c2712370b8d85b687a474b2e858cdcc) | 5 | 5 | recursive complete; sampled semantics |
| DJ-062 | [dotj-packages](repos/dotj-packages/README.md) | [NuGet client](https://github.com/NuGet/NuGet.Client/tree/4c4510d29a64fcbcba6360e29c3a1e8288a87f9f) | 6 | 2 | recursive complete; sampled semantics |
| DJ-063 | [dotj-registry](repos/dotj-registry/README.md) | [NuGet Gallery](https://github.com/NuGet/NuGetGallery/tree/d6b9e689606e174e05c064a3531320200d4033c7) | 6 | 5 | recursive complete; sampled semantics |
| DJ-064 | [dotj-automap](repos/dotj-automap/README.md) | [AutoMapper](https://github.com/LuckyPennySoftware/AutoMapper/tree/3019d86b3e2f1c879dfcf7d1026c90f51519a9a1) | 5 | 3 | recursive complete; sampled semantics |
| DJ-065 | [dotj-mediator](repos/dotj-mediator/README.md) | [MediatR](https://github.com/LuckyPennySoftware/MediatR/tree/916ef1b3d68ccdc96db8f914eaf1b32fc7db52c5) | 5 | 3 | recursive complete; sampled semantics |
| DJ-066 | [dotj-bus](repos/dotj-bus/README.md) | [MassTransit](https://github.com/MassTransit/MassTransit/tree/d9f61f764c802785cc9a4be92547d8f5b63018d4) | 5 | 4 | recursive complete; sampled semantics |

Counts include the 12 additional SDK integration packages assigned to their accountable repositories. The original 344 feature packages remain intact. See [SDK agent execution](sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md).
