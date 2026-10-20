# Candidate `System.IDisposable` distribution scope

Pinned reference: `dotnet/runtime` v10.0.12, commit `4271d88e0aebf3d04f188f1334c2220d80555ef6`.

| Input or output | Candidate package treatment | Evidence |
|---|---|---|
| `System.IDisposable` name and `void Dispose()` declaration | Contract input for an independently written Java interface; no upstream source bytes proposed for the package. | `idisposable-rights-v10.0.12.json` and `disposal-source-inventory-v10.0.12/manifest.json` |
| .NET CoreLib binary and source tree | Development reference only; excluded from the proposed Java artifact. | `runtime-artifact-v10.0.12-win-x64.json` and `source-archive-v10.0.12.json` |
| .NET repository `LICENSE.TXT` | Pinned MIT license text is retained in the evidence archive. If upstream code is copied into a later artifact, review the retention requirement for that artifact. | `notices/LICENSE.TXT`, SHA-256 `cfc21f5e8bd655ae997eec916138b707b1d290b83272c02a95c9f821b8c87310` |
| .NET repository `THIRD-PARTY-NOTICES.TXT` | Retained for source-reference analysis; applicability to any future shipped files requires a file-level review. | The local `notices/THIRD-PARTY-NOTICES.TXT` was refreshed from the exact pinned commit and hashes to the archived source record, SHA-256 `66f1d4e44973185519bb4aa8a9718eb22fc7af2cc532e3ae9cfc4c127ee7fc54`. The prior local copy hashed to `5f3cb35ca8d9d9d5ef6f8fab4bcae617c04474d623374f660f6d2d37450d6ea5` and did not match the archive. |
| Java product candidate | `dotj-core/dotj-core-public/src/main/java/System/IDisposable.java` is the compiled source. The built candidate JAR contains only `META-INF/MANIFEST.MF` and `System/IDisposable.class`; its SHA-256 is `4f3df3b621126d6438dfd5703266e7435afcf2362dbd1b9014c131dbd575d7e1`. This is an observed candidate artifact, not a released package. | `idisposable-product-v1.json` and `idisposable-file-notice-map-v10.0.12.json` |

The earlier compile-only `idisposable-candidate.jar` remains a separate historical probe. The product candidate is built by `build-idisposable-product.py` from the public Java source with JDK 21 `javac`; Python `zipfile` writes the two JAR entries. The upstream .NET files and notices are reference evidence and are not entries in this JAR. The two-entry inventory does not establish notice applicability, license sufficiency, or release clearance. E01 remains open pending project-license and file-level notice decisions and the required repository licensing review.
