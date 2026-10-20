# Candidate `System.IDisposable` distribution scope

Pinned reference: `dotnet/runtime` v10.0.12, commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`.

| Input or output | Candidate package treatment | Evidence |
|---|---|---|
| `System.IDisposable` name and `void Dispose()` declaration | Contract input for an independently written Java interface; no upstream source bytes proposed for the package. | `idisposable-rights-v10.0.12.json` and `disposal-source-inventory-v10.0.12/manifest.json` |
| .NET CoreLib binary and source tree | Development reference only; excluded from the proposed Java artifact. | `runtime-artifact-v10.0.12-win-x64.json` and `source-archive-v10.0.12.json` |
| .NET repository `LICENSE.TXT` | Pinned MIT license text is retained in the evidence archive. If upstream code is copied into a later artifact, review the retention requirement for that artifact. | `notices/LICENSE.TXT`, SHA-256 `cfc21f5e8bd655ae997eec916138b707b1d290b83272c02a95c9f821b8c87310` |
| .NET repository `THIRD-PARTY-NOTICES.TXT` | Retained for source-reference analysis; applicability to any future shipped files requires a file-level review. | The local `notices/THIRD-PARTY-NOTICES.TXT` hashes to `5f3cb35ca8d9d9d5ef6f8fab4bcae617c04474d623374f660f6d2d37450d6ea5`; the archived source record lists `66f1d4e44973185519bb4aa8a9718eb22fc7af2cc532e3ae9cfc4c127ee7fc54`. The difference requires reconciliation. |
| Java candidate artifact | Proposed contents are owned Java source/class files and package metadata, with no .NET binary or generated .NET output. Artifact build and contents have not yet been qualified. | This distribution proposal; no release artifact exists. |

This records the proposed distribution form and source inputs. It does not decide notice applicability, license sufficiency, or release clearance. E01 remains open until the notice-byte discrepancy is reconciled, the actual artifact contents and all copied/transitive inputs are audited, and the required repository licensing review is complete.
