# Selected compiled lifecycle inventory v1

This bounded E02/N01 reference artifact resolves the installed compiled shapes
behind the twelve declaration anchors in the merged internal evaluation
candidate's [prerequisites](../../../../dotj-build/evaluation-candidate/prerequisites.json).
All E01/E02/E03/N01, public API and product/task acceptance gates remain open.

The historical analysis pin remains `6348d0c087aeec18c323b01a2c77da089ddafea0`.
The implementation component is `b44cdcec4c79c50c67560876707d57d4f635fa3b`,
attributed by the retained official VMR manifest to installed SDK 10.0.401 /
MSBuild 18.9.11. The aggregate is `e34a38d2ae1fc26406a317517196e55c68ff83ab`.
Its `src` subtree matches the component, while `eng` and `global.json` differ.
These facts do not prove a standalone source build reproduces the SDK binary.
The prior provenance reports, current SDK entries, source and host/runtime bytes
are hash-locked in [compiled-lifecycle-lock-v1.json](evidence/compiled-lifecycle-lock-v1.json).

The standalone [reader and verifier](../../../../tools/oracle/dotj-build/README.md)
use MetadataLoadContext on actual installed assemblies, with .NET 10.0.12 and
roll-forward disabled. Reference code cannot execute in that context. No projects
are evaluated and no tasks, application getters or builds run.

The retained [verification record](evidence/compiled-lifecycle-verification-v1.json)
shows two byte-identical captures, all twelve anchors matched, five integrity
refusals before reader launch, and one missing compiled-anchor refusal. Exact
commands and full output logs remain in the recorded private D: directories.

| Selected declaring type / family | Installed declared records |
|---|---:|
| Microsoft.Build.Evaluation.Project instance constructors | 25 (21 public, 1 internal, 3 private) |
| Project compiler-generated type initializer | 1 private static; no explicit source declaration |
| Project.GetPropertyValue | 1 public method |
| Microsoft.Build.Evaluation.ProjectCollection constructors | 8 public |
| ProjectCollection.LoadProject | 6 public overloads: 3 filename, 3 XmlReader |
| ProjectCollection.UnloadProject | 2 public overloads: Project and ProjectRootElement |
| ProjectCollection.Dispose | 1 public parameterless and 1 protected virtual bool overload |
| ProjectCollection.GlobalProjectCollection / GlobalProperties | 2 properties, including accessor metadata |

The [unedited metadata result](evidence/compiled-lifecycle-raw-v1.json) records
declaring assembly/type, MVID/tokens, visibility/static/kind, constructor/method
parameters, ref/in/out/optional/default flags, custom modifiers and attributes,
return types, generic parameters/constraints and selected properties/accessors.
The selected methods/types have no generic parameters; their signatures consume
constructed generic collection contracts. Exact assembly-qualified generic
definitions, constraints, interfaces and enum literals are retained.
For example, the installed IEnumerable`1 parameter is covariant and carries
AllowByRefLike; IDictionary`2 has two invariant parameters without CLR type
constraints. Faithful Java representation of these facts remains unresolved.

The [mapping](evidence/compiled-lifecycle-mapping-v1.json) matches all twelve
anchors case-sensitively and retains navigation for every captured overload.
Source declaration/parameter-name correlation is navigation, not compiler or
PDB proof. The binary signatures are independently read from installed metadata;
one generated `.cctor` has no explicit source constructor match.

The 24 direct contract identities include System.String, IDictionary`2,
IEnumerable`1, IDisposable, XmlReader, ProjectRootElement, ILogger and logger,
load-setting/toolset option types. Internal interfaces and private/internal
constructor dependencies remain labeled by actual visibility; they are not
invented public requirements. The resolved implementation of XmlReader is
System.Private.Xml, with System.Xml.ReaderWriter forwarding metadata retained
among loaded assemblies. System.String and the collection definitions resolve to
System.Private.CoreLib. No Java or dotj-core representation is selected here.

Project's `NET` branch selects an internal SearchValues field; it does not change
these constructor signatures. ProjectCollection's
`FEATURE_SYSTEM_CONFIGURATION` / `FEATURE_REGISTRY_TOOLSETS` branches affect
ToolsetDefinitionLocations.Default; installed Default = Local = 4 is retained
alongside None = 0, ConfigurationFile = 1 and Registry = 2.
`FEATURE_WIN32_REGISTRY` affects toolset implementation bodies. Other target
frameworks/feature configurations and generated-input equivalence are unmeasured.
Both selected source files explicitly disable nullable annotations. Metadata
alone does not resolve permissible nulls or ownership/lifecycle behavior.

InvalidProjectFileException is documented in the selected constructor source
and independently resolved as a public metadata type. CLR signatures do not
declare throws; this does not establish all reachable exception contracts,
diagnostics, HResults, IO failures or semantic compatibility. Recursive public
dependency/member closure, public Java shape/API comparison, language-gap
dispositions, paired C#/.j examples, collection membership, disposal, caching and
evaluation semantics remain open. This inventory provides no public facade or
product/task/batch acceptance credit.
