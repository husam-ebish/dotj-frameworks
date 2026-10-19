# DJ-051 .j Test: module and API inventory

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1169 | recursive complete |
| Project-definition paths | 14 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 626 | Lexical path classification, not runnable test count |
| Sampled text files | 13 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 37 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 9 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [CakeScripts.Tests/CakeScripts.Tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/CakeScripts.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [CakeScripts/CakeScripts.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/CakeScripts.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/framework/nunit.framework.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/framework/nunit.framework.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/mock-assembly/mock-assembly.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/mock-assembly/mock-assembly.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/nunit.framework.legacy.tests/nunit.framework.legacy.tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/nunit.framework.legacy.tests/nunit.framework.legacy.tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/nunit.framework.legacy/nunit.framework.legacy.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/nunit.framework.legacy/nunit.framework.legacy.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/nunitlite-runner/nunitlite-runner.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/nunitlite-runner/nunitlite-runner.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/nunitlite.tests/nunitlite.tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/nunitlite.tests/nunitlite.tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/nunitlite/nunitlite.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/nunitlite/nunitlite.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/slow-tests/slow-nunit-tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/slow-tests/slow-nunit-tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/testdata.fsharp/nunit.testdata.fsharp.fsproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/testdata.fsharp/nunit.testdata.fsharp.fsproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/testdata/nunit.testdata.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/testdata/nunit.testdata.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/tests/nunit.framework.tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/nunit.framework.tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [src/NUnitFramework/windows-tests/windows-tests.csproj](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/windows-tests/windows-tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [CakeScripts/MinVerTool.cs:5](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/MinVerTool.cs#L5) | `public enum AutoIncrement` |
| [CakeScripts/MinVerTool.cs:12](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/MinVerTool.cs#L12) | `public static class MinVerTool` |
| [CakeScripts/MinVerTool.cs:14](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/MinVerTool.cs#L14) | `public static string GetVersion(AutoIncrement autoIncrement = AutoIncrement.Minor, string tagPrefix = "v")` |
| [CakeScripts/VersionParsers.cs:3](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/VersionParsers.cs#L3) | `public static class VersionParsers` |
| [CakeScripts/VersionParsers.cs:5](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts/VersionParsers.cs#L5) | `public static string ParseAssemblyVersion(string version)` |
| [CakeScripts.Tests/VersionParsersTests.cs:5](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/VersionParsersTests.cs#L5) | `public class CakeTests` |
| [CakeScripts.Tests/VersionParsersTests.cs:9](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/CakeScripts.Tests/VersionParsersTests.cs#L9) | `public void ThatWeCanParseAssemblyVersionStrings(string versionString, string expected)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:14](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L14) | `public class WorkItemTests` |
| [src/NUnitFramework/tests/WorkItemTests.cs:20](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L20) | `public void CreateWorkItems()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:31](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L31) | `public void DisposeWorkItems()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:37](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L37) | `public void ConstructWorkItem()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:48](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L48) | `public void ExecuteWorkItem()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:61](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L61) | `public void CanStopRun()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:79](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L79) | `public static void DummyTest()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:87](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L87) | `public void GetsTargetApartmentFromParentTests(Test test, ApartmentState expected)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:95](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L95) | `public void GetsTargetApartmentFromParentTestsInWrappedTests(Test test, ApartmentState expected)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:127](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L127) | `public FakeTest(string name, ApartmentState apartmentState) : base(name)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:133](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L133) | `public override object[] Arguments => throw new System.NotImplementedException();` |
| [src/NUnitFramework/tests/WorkItemTests.cs:135](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L135) | `public override string XmlElementName => "MockTest";` |
| [src/NUnitFramework/tests/WorkItemTests.cs:137](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L137) | `public override bool HasChildren => Tests.Count > 0;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:139](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L139) | `public override IList<ITest> Tests => new List<ITest>();` |
| [src/NUnitFramework/tests/WorkItemTests.cs:141](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L141) | `public override TNode AddToXml(TNode parentNode, bool recursive)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:146](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L146) | `public override TestResult MakeTestResult() => new FakeTestResult(this);` |
| [src/NUnitFramework/tests/WorkItemTests.cs:151](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L151) | `public FakeTestResult(ITest test) : base(test)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:155](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L155) | `public override int TotalCount => 1;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:157](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L157) | `public override int PassCount => 1;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:159](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L159) | `public override int FailCount => 0;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:161](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L161) | `public override int WarningCount => 0;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:163](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L163) | `public override int SkipCount => 0;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:165](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L165) | `public override int InconclusiveCount => 0;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:167](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L167) | `public override bool HasChildren => false;` |
| [src/NUnitFramework/tests/WorkItemTests.cs:169](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L169) | `public override IEnumerable<ITestResult> Children => Enumerable.Empty<ITestResult>();` |
| [src/NUnitFramework/tests/WorkItemTests.cs:171](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L171) | `protected internal override TestResult CalculateDeltaResult(TestResult previous, Exception? exception)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:185](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L185) | `public override TestResult Clone()` |
| [src/NUnitFramework/tests/WorkItemTests.cs:193](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L193) | `public FakeWorkItem(WorkItem wrappedItem) : base(wrappedItem)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:197](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L197) | `public FakeWorkItem(Test test, ITestFilter filter) : base(test, filter)` |
| [src/NUnitFramework/tests/WorkItemTests.cs:201](https://github.com/nunit/nunit/blob/55d908f8cc4402f8d53955d20aefcee9f55a59ec/src/NUnitFramework/tests/WorkItemTests.cs#L201) | `protected override void PerformWork()` |

Full lexical records (37) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Proposed contract names |
|---|---|---|
| WP-01 | Test model discovery and attributes | TestSuite; TestCase; TestAttribute; Category |
| WP-02 | Constraint assertions and diagnostics | Constraint; ConstraintResult; ActualValue |
| WP-03 | Setup teardown and execution context | LifecyclePlan; ExecutionContext; TestResult |
| WP-04 | Parameterized parallel and isolated execution | CaseSource; ParallelScope; WorkerSession |
| WP-05 | Runner reporting extensions and bootstrap | EngineProtocol; ResultXml; ExtensionPoint |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
