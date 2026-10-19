# Naming and concept correction

Owner instruction, 2026-10-19: preserve exact original names and concepts so C# developers can transfer their framework knowledge to Java with minimal relearning.

Changed all 66 plans: mandatory DOTNET-API-EXACT-001; repository API-COMPATIBILITY.md; case-sensitive N01 mapping/validation; paired C#/.j examples; exact public namespaces and upstream types; private-only status for invented architecture labels. Corrected cancellation/time/disposal examples and the rule that previously exposed CompletionStage as the default public async contract. Properties/events/generics/expression trees and other Java language gaps are explicit representations or blockers, not permission to rename.

At the naming-only revision, there were 344 feature packages plus 66 N01 gates, 1,296 named tasks and 1,251 designed acceptance cases. The added 264 tasks and 198 cases enforce naming, concept and language-gap rules. Original task/fixture IDs remain stable. Source evidence and notice bytes are unchanged. Complete semantic API mapping and implementation remain open; this is a plan correction, not an implementation or compatibility claim.

The subsequent [SDK and distribution revision](10-SDK-AND-DISTRIBUTION-PLAN.md) adds 12 integration packages, 60 tasks and 60 cases. Current totals are in [STATUS.md](STATUS.md).
