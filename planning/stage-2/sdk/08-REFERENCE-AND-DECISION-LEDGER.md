# Reference sources and explicit compatibility decisions

Date checked: 2026-10-19. These documentation references establish terminology and command scope. They are mutable documentation, not immutable implementation evidence. E01 must pin source, release artifacts and oracle executables before exact behavior is certified.

## Baseline and evidence rules

Use .NET 10 as the proposed initial CLI reference family. The exact patch/feature band and matching source revision remain E01 work. Existing repository analysis pins are retained; they may be development revisions with behavior beyond this family. Keep `analysis_revision` and `reference_release_revision` distinct in the implementation evidence.

Each command record must include `reference_sdk_version`, artifact digest, source revision, OS/architecture, locale, relevant environment, invocation, project fixture hash, stdout, stderr, exit code, file delta and network observation. Store an unnormalized result plus a comparison result so normalization is auditable. A page read or a source symbol match is not an executed compatibility test.

## Primary references

| Topic | Official reference | Use in this plan |
|---|---|---|
| CLI command surface | [dotnet command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet) | Command families and launcher responsibilities |
| SDK selection | [global.json](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) | SDK selection vocabulary and policies |
| Package command | [dotnet package add](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-add) | .NET 10 noun-first command and reference editing |
| Templates | [dotnet new](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new) | Template creation/options and subcommands |
| Restore | [dotnet restore](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-restore) | Restore inputs and applicable command options |
| Build | [dotnet build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build) | Build invocation and implicit restore concepts |
| Test | [dotnet test](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test) | Runner-specific invocation contracts |
| Tools | [dotnet tool install](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install) | Tool scopes and manifest concepts |
| Workloads | [dotnet workload install](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-workload-install) | Optional workloads and installation semantics |
| SDK project properties | [SDK project reference](https://learn.microsoft.com/en-us/dotnet/core/tools/csproj) | Existing project/property vocabulary |
| Central versions | [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) | Central package versions and file conventions |
| Package references | [PackageReference](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) | Project references and lock concepts |
| Feed configuration | [NuGet.Config](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file) | Sources and applicable configuration semantics |
| Package types | [Set a package type](https://learn.microsoft.com/en-us/nuget/create-packages/set-package-type) | Custom type declaration and compatibility constraints |
| Feed protocol | [NuGet Server API](https://learn.microsoft.com/en-us/nuget/api/overview) | V3 protocol resource scope |
| Service discovery | [Service index](https://learn.microsoft.com/en-us/nuget/api/service-index) | Resource discovery instead of guessed URLs |
| Package bytes | [Package content resource](https://learn.microsoft.com/en-us/nuget/api/package-base-address-resource) | Version/content retrieval contracts |
| Application deployment | [Publishing overview](https://learn.microsoft.com/en-us/dotnet/core/deploying/) | Framework-dependent/self-contained and other deployment concepts |

The Java storage/layout/hosting choices below are proposed product design, not claims that Microsoft documents prescribe them. Consult the existing immutable SDK/build/packages/registry source inventories for implementation evidence.

## Exactness and platform representation ledger

| ID | Requirement / representation | Status and implementation rule |
|---|---|---|
| SDK-D01 | Exact .NET public type/member/namespace names and concepts | Mandatory owner requirement; N01 mapping and compiled API checks |
| SDK-D02 | `dotj` root executable with corresponding .NET command words/options | Product branding; no alternative command vocabulary for corresponding functions |
| SDK-D03 | Concrete .NET 10 SDK patch and matching source | OPEN evidence gate; never certify against an unspecified moving latest version |
| SDK-D04 | `.jproj`, `Dotj.Sdk`, `.java`, JAR outputs | Proposed Java artifact representation; exact XML concepts retained; not native Microsoft SDK input compatibility |
| SDK-D05 | `java25` target and JDK 25 family | Proposed .j target; exact toolchain build and target schema OPEN qualification |
| SDK-D06 | `.nupkg` envelope with explicit .j Java manifest/types/assets | Proposed package profile; NuGet transport and custom payload handling must both pass |
| SDK-D07 | Source-derived upstream package IDs in isolated .j feed | Identity/rights qualification required; never resolve CLR bytes as Java |
| SDK-D08 | Product-specific SDK/runtime/cache roots and `DOTJ_ROOT` | Coexistence requirement; do not overwrite .NET roots or collide with same-ID CLR packages |
| SDK-D09 | Familiar global.json and tool manifest filenames | Preserve semantics where applicable; mixed-product version/manifest conflicts must be explicit |
| SDK-D10 | C# syntax that javac cannot represent | Explicit language gap; no silent public rename or false claim of unchanged C# compilation |
| SDK-D11 | NativeAOT, single-file, hot reload, browser/mobile runtime semantics | Separate capability gates; JAR/jlink/restart are not evidence of equivalent behavior |
| SDK-D12 | Public feed/download provider, domain, exact costs, signing/installer channel | Deployment decisions after local proof; no service has been provisioned |

These platform representations do not relax the exact-name requirement for framework APIs. They distinguish product artifacts from source API identities. If qualification reveals that a representation changes a required concept or introduces an avoidable learning path, revise it before implementation is accepted. A proposal is not a waiver of a failed parity test.

## Per-feature status vocabulary

Use `not-started`, `contract-mapped`, `implemented-unqualified`, `verified`, `blocked-language`, `blocked-runtime`, `blocked-rights` or `blocked-evidence`. Record retained deferred scope with its future owner and prerequisite. Only `verified` with named evidence may support a public parity claim. Do not use `done` for a document, stub or downloaded manifest when the capability itself is not implemented.

## Contribution rule for all 66 products

Before releasing a repository, record its source-derived public API inventory, package ID/version/type, Java target/runtime matrix, dependency closure, shared framework/reference-pack membership, template/tool/workload contributions, test adapter requirements, notices and SDK version range. Base SDK inclusion requires a justified dependency and size assessment; inclusion is not automatic because a repository is in this ecosystem.

Maintain paired C# and Java-profile usage examples from executable fixtures. The examples must preserve the exact framework names and concepts; explain only real syntax/runtime adaptations. Record both positive and negative cases. Never state zero learning or full platform equivalence as an achieved result while unresolved mappings remain.
