# DJ-025 .j Container: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 723 | recursive complete |
| Project-definition paths | 12 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 308 | Lexical path classification, not runnable test count |
| Sampled text files | 11 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 46 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 21 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [bench/Autofac.BenchmarkProfiling/Autofac.BenchmarkProfiling.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/bench/Autofac.BenchmarkProfiling/Autofac.BenchmarkProfiling.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [bench/Autofac.Benchmarks/Autofac.Benchmarks.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/bench/Autofac.Benchmarks/Autofac.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [codegen/Autofac.CodeGen/Autofac.CodeGen.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/codegen/Autofac.CodeGen/Autofac.CodeGen.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/Autofac/Autofac.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Autofac.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Specification.Test/Autofac.Specification.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Specification.Test/Autofac.Specification.Test.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.Aot/Autofac.Test.Aot.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.Aot/Autofac.Test.Aot.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.AotWarnings/Autofac.Test.AotWarnings.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.AotWarnings/Autofac.Test.AotWarnings.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.CodeGen/Autofac.Test.CodeGen.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.CodeGen/Autofac.Test.CodeGen.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.Compilation/Autofac.Test.Compilation.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.Compilation/Autofac.Test.Compilation.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.Scenarios.LoadContext/Autofac.Test.Scenarios.LoadContext.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.Scenarios.LoadContext/Autofac.Test.Scenarios.LoadContext.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test.Scenarios.ScannedAssembly/Autofac.Test.Scenarios.ScannedAssembly.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test.Scenarios.ScannedAssembly/Autofac.Test.Scenarios.ScannedAssembly.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/Autofac.Test/Autofac.Test.csproj](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/Autofac.Test.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/Autofac/Module.cs:47](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L47) | `public abstract class Module : IModule` |
| [src/Autofac/Module.cs:55](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L55) | `protected virtual Assembly ThisAssembly` |
| [src/Autofac/Module.cs:74](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L74) | `public void Configure(IComponentRegistryBuilder componentRegistry)` |
| [src/Autofac/Module.cs:97](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L97) | `protected virtual void Load(ContainerBuilder builder)` |
| [src/Autofac/Module.cs:109](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L109) | `protected virtual void AttachToComponentRegistration(` |
| [src/Autofac/Module.cs:122](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/Module.cs#L122) | `protected virtual void AttachToRegistrationSource(` |
| [src/Autofac/IContainer.cs:31](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/src/Autofac/IContainer.cs#L31) | `public interface IContainer : ILifetimeScope` |
| [test/Autofac.Test/ModuleTests.cs:11](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L11) | `public class ModuleTests` |
| [test/Autofac.Test/ModuleTests.cs:15](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L15) | `protected override void Load(ContainerBuilder builder)` |
| [test/Autofac.Test/ModuleTests.cs:22](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L22) | `public void LoadsRegistrations()` |
| [test/Autofac.Test/ModuleTests.cs:32](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L32) | `public void DetectsNullComponentRegistryArgument()` |
| [test/Autofac.Test/ModuleTests.cs:39](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L39) | `public IList<IComponentRegistration> Registrations { get; set; } = new List<IComponentRegistration>();` |
| [test/Autofac.Test/ModuleTests.cs:41](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L41) | `protected override void AttachToComponentRegistration(IComponentRegistryBuilder componentRegistry, IComponentRegistration registration)` |
| [test/Autofac.Test/ModuleTests.cs:49](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L49) | `public void AttachesToRegistrations()` |
| [test/Autofac.Test/ModuleTests.cs:65](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L65) | `public void AttachesToRegistrationsInScope()` |
| [test/Autofac.Test/ModuleTests.cs:82](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L82) | `public void AttachesToRegistrationsInNestedScope()` |
| [test/Autofac.Test/ModuleTests.cs:101](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L101) | `public void ModifiedScopesHaveTheirOwnDelegate()` |
| [test/Autofac.Test/ModuleTests.cs:149](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L149) | `public Assembly ModuleThisAssembly` |
| [test/Autofac.Test/ModuleTests.cs:159](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L159) | `public void TheAssemblyExposedByThisAssemblyIsTheOneContainingTheConcreteModuleClass()` |
| [test/Autofac.Test/ModuleTests.cs:170](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L170) | `public void IndirectlyDerivedModulesCannotUseThisAssembly()` |
| [test/Autofac.Test/ModuleTests.cs:178](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L178) | `protected override void Load(ContainerBuilder builder)` |
| [test/Autofac.Test/ModuleTests.cs:194](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L194) | `public void CanUseBuilderPropertyBag()` |
| [test/Autofac.Test/ModuleTests.cs:213](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L213) | `protected override void Load(ContainerBuilder builder)` |
| [test/Autofac.Test/ModuleTests.cs:220](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L220) | `public void ModuleWithoutHookDoesNotSubscribeToRegisteredEvent()` |
| [test/Autofac.Test/ModuleTests.cs:236](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L236) | `public void ModuleWithoutHookDoesNotSubscribeToRegistrationSourceAddedEvent()` |
| [test/Autofac.Test/ModuleTests.cs:254](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L254) | `public IList<IComponentRegistration> Seen { get; } = new List<IComponentRegistration>();` |
| [test/Autofac.Test/ModuleTests.cs:256](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L256) | `protected override void AttachToComponentRegistration(` |
| [test/Autofac.Test/ModuleTests.cs:265](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L265) | `public void ModuleOverridingComponentRegistrationHookSubscribesToRegisteredEvent()` |
| [test/Autofac.Test/ModuleTests.cs:280](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L280) | `public void ModuleOverridingComponentRegistrationHookStillReceivesRegistrations()` |
| [test/Autofac.Test/ModuleTests.cs:294](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L294) | `public void ModuleOverridingOnlyComponentRegistrationHookDoesNotSubscribeToRegistrationSourceAddedEvent()` |
| [test/Autofac.Test/ModuleTests.cs:312](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L312) | `public IList<IRegistrationSource> Seen { get; } = new List<IRegistrationSource>();` |
| [test/Autofac.Test/ModuleTests.cs:314](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L314) | `protected override void AttachToRegistrationSource(` |
| [test/Autofac.Test/ModuleTests.cs:323](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L323) | `public void ModuleOverridingRegistrationSourceHookSubscribesToRegistrationSourceAddedEvent()` |
| [test/Autofac.Test/ModuleTests.cs:338](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L338) | `public void ModuleOverridingOnlyRegistrationSourceHookDoesNotSubscribeToRegisteredEvent()` |
| [test/Autofac.Test/ModuleTests.cs:355](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L355) | `public bool IsAdapterForIndividualComponents => false;` |
| [test/Autofac.Test/ModuleTests.cs:357](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L357) | `public IEnumerable<IComponentRegistration> RegistrationsFor(Service service, Func<Service, IEnumerable<ServiceRegistration>> registrationAccessor)` |
| [test/Autofac.Test/ModuleTests.cs:364](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L364) | `public void ModuleOverridingRegistrationSourceHookStillReceivesSources()` |
| [test/Autofac.Test/ModuleTests.cs:381](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L381) | `public IList<IComponentRegistration> Seen { get; } = new List<IComponentRegistration>();` |
| [test/Autofac.Test/ModuleTests.cs:383](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L383) | `protected override void AttachToComponentRegistration(` |
| [test/Autofac.Test/ModuleTests.cs:393](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L393) | `protected override void Load(ContainerBuilder builder)` |
| [test/Autofac.Test/ModuleTests.cs:400](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L400) | `public void ModuleInheritingHookFromIntermediateBaseStillReceivesRegistrations()` |
| [test/Autofac.Test/ModuleTests.cs:415](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/ModuleTests.cs#L415) | `public void ModuleInheritingHookFromIntermediateBaseSubscribesToRegisteredEvent()` |
| [test/Autofac.Test/NamedParameterTests.cs:8](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L8) | `public class NamedParameterTests` |
| [test/Autofac.Test/NamedParameterTests.cs:20](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L20) | `public C(A a)` |
| [test/Autofac.Test/NamedParameterTests.cs:26](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L26) | `public void MatchesIdenticallyNamedParameter()` |
| [test/Autofac.Test/NamedParameterTests.cs:47](https://github.com/autofac/Autofac/blob/ae9e1e1129b9c22e7ab111381308dcb02f80a8d2/test/Autofac.Test/NamedParameterTests.cs#L47) | `public void DoesNotMatchDifferentlyNamedParameter()` |

Full lexical records (46) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Registration model and resolution | ServiceKey; Registration; ResolutionContext |
| WP-02 | Scopes ownership and disposal | LifetimeScope; OwnedValue; ReleaseAction |
| WP-03 | Modules scanning and activation pipelines | RegistrationModule; ComponentScanner; ActivationMiddleware |
| WP-04 | Advanced relationships and interception | LazyService; ServiceFactory; MetadataValue; InterceptorAdapter |
| WP-05 | Core bridge and concurrent acceptance | CoreContainerAdapter; ScopeDiagnostic; StressScenario |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
