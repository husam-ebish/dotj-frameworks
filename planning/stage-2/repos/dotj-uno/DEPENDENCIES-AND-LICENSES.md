# DJ-044 .j Uno: dependencies and licenses

## Proposed Java dependencies

core,toolkit;web(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: Native SDKs and owned bindings; browser DOM/JS/Wasm bridge requires a separate execution design.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|

No declaration was captured in the earlier metadata sample. This is an evidence gap, not proof of zero dependencies.

## License evidence and eligibility gate

Observed metadata hint: `unavailable`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [License.md](evidence/notices/License.md) | [License.md](https://github.com/unoplatform/uno/blob/78728530f26880286be77d9042a8e4118a42df43/License.md) |
| [THIRD-PARTY-NOTICES.md](evidence/notices/THIRD-PARTY-NOTICES.md) | [THIRD-PARTY-NOTICES.md](https://github.com/unoplatform/uno/blob/78728530f26880286be77d9042a8e4118a42df43/THIRD-PARTY-NOTICES.md) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-uno-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
