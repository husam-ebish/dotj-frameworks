# DJ-063 .j Registry: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/NgTests/Db2CatalogTests.cs:66](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L66) | Dispose | not confirmed |
| [tests/NgTests/Db2CatalogTests.cs:84](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L84) | RunInternal_WithNoCatalogAndNoActivity_DoesNotCreateCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:96](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L96) | RunInternal_CanSetLeaveNoStoreOnAllBlobs | yes |
| [tests/NgTests/Db2CatalogTests.cs:122](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L122) | RunInternal_CanSetCacheControlOnlyOnItems | yes |
| [tests/NgTests/Db2CatalogTests.cs:158](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L158) | RunInternal_CanSetCacheControlOnlyOnFinishedPages | yes |
| [tests/NgTests/Db2CatalogTests.cs:194](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L194) | RunInternal_DoesNotSetCacheControlOnUnfinishedLatestPage | yes |
| [tests/NgTests/Db2CatalogTests.cs:233](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L233) | RunInternal_WritesPageCacheControlAfterIndex | yes |
| [tests/NgTests/Db2CatalogTests.cs:280](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L280) | RunInternal_WithNoCatalogAndCreatedPackageInFeed_CreatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:302](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L302) | RunInternal_WithNoCatalogAndCreatedPackageInFeedAndWithCreatedPackagesSkipped_DoesNotCreateCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:319](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L319) | RunInternal_WithCatalogAndNoActivity_DoesNotUpdateCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:350](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L350) | RunInternal_WithCatalogAndNoActivityAndWithCreatedPackagesSkipped_DoesNotUpdateCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:384](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L384) | RunInternal_WithPackagesWithSameCreatedTimeInFeedAndWhenProcessedInDifferentCatalogBatches_SkipsSecondEntry | yes |
| [tests/NgTests/Db2CatalogTests.cs:411](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L411) | RunInternal_WithPackagesWithSameLastEditedTimeInFeedAndWhenProcessedInDifferentCatalogBatches_SkipsSecondEntry | yes |
| [tests/NgTests/Db2CatalogTests.cs:446](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L446) | RunInternal_WithCreatedPackagesInFeedAtDifferentTimes_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:477](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L477) | RunInternal_WithCreatedPackagesInFeedAtDifferentTimesAndWithCreatedPackagesSkipped_DoesNotUpdateCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:498](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L498) | RunInternal_WithCreatedPackageAndEditedPackageInFeedAtDifferentTimes_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:529](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L529) | RunInternal_WithCreatedPackageAndEditedPackageInFeedAtDifferentTimesAndWithCreatedPackagesSkipped_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:560](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L560) | RunInternal_WithCreatedPackageAndEditedPackageInFeedAtSameTime_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:590](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L590) | RunInternal_WithCreatedPackageAndEditedPackageInFeedAtSameTimeAndWithCreatedPackagesSkipped_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:621](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L621) | RunInternal_WithEditedPackagesAndWithCreatedPackagesSkipped_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:654](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L654) | RunInternal_WithCreatedPackageThenDeletedPackage_UpdatesCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:685](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L685) | RunInternal_WithMultipleDeletedPackagesWithDifferentPackageIdentities_ProcessesAllDeletions | yes |
| [tests/NgTests/Db2CatalogTests.cs:718](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L718) | RunInternal_WithMultipleDeletedPackagesWithSamePackageIdentity_PutsEachPackageInSeparateCommit | yes |
| [tests/NgTests/Db2CatalogTests.cs:752](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L752) | RunInternal_WithDeletedPackageOlderThan15MinutesAgo_SkipsDeletedPackage | yes |
| [tests/NgTests/Db2CatalogTests.cs:784](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L784) | RunInternal_WithMultipleCreatedPackages_ProcessesAllCreations | yes |
| [tests/NgTests/Db2CatalogTests.cs:807](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L807) | RunInternal_WithMultipleEditedPackages_ProcessesAllEdits | yes |
| [tests/NgTests/Db2CatalogTests.cs:842](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L842) | CreatesNewCatalogFromCreatedAndEditedAndDeletedPackages | yes |
| [tests/NgTests/Db2CatalogTests.cs:963](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L963) | AppendsDeleteToExistingCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:1081](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L1081) | AppendsDeleteAndReinsertToExistingCatalog | yes |
| [tests/NgTests/Db2CatalogTests.cs:1212](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/Db2CatalogTests.cs#L1212) | RunInternal_CallsCatalogStorageLoadStringExactlyOnce | yes |
| [tests/NgTests/NgJobFactoryTests.cs:19](https://github.com/NuGet/NuGetGallery/blob/d6b9e689606e174e05c064a3531320200d4033c7/tests/NgTests/NgJobFactoryTests.cs#L19) | CanActivateJobs | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-063-F01-01 | WP-01 | Published content hashes match responses | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F01-02 | WP-01 | unlisted versions obey protocol semantics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F01-03 | WP-01 | Java artifacts and NuGet packages remain distinguishable | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F02-01 | WP-02 | Interrupted uploads never appear as valid packages | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F02-02 | WP-02 | duplicate identical uploads are idempotent | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F02-03 | WP-02 | conflicting bytes at one identity are rejected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F03-01 | WP-03 | Revoked keys cannot publish | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F03-02 | WP-03 | owners cannot overwrite unrelated packages | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F03-03 | WP-03 | audit records exclude raw secrets | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F04-01 | WP-04 | Search lag is visible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F04-02 | WP-04 | hostile README/metadata cannot execute script | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F04-03 | WP-04 | registry bootstraps without relying on its own published packages | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F05-01 | WP-05 | Restored registry reconciles metadata with blobs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F05-02 | WP-05 | claimed endpoints pass client fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-063-F05-03 | WP-05 | cloud-storage guarantees are not assumed universally | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Upload atomicity; duplicate versions; feed conformance; search index lag; access control; restore after backup.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-063-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-063-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-063-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.

## Detailed SDK integration requirement

[DOTNET-SDK-EXPERIENCE-001](../../10-SDK-AND-DISTRIBUTION-PLAN.md) supplements this repository's existing feature work. The detailed [integration tasks and acceptance cases](../../sdk/07-AGENT-EXECUTION-AND-ACCEPTANCE.md) are mandatory, all NOT STARTED as implementation. Their task IDs also appear in the global machine-readable backlogs.

- `SDK-I10`: Hosted feed protocol and immutable distribution; five named tasks and five designed cases in the integration plan.

These are integration packages, not a replacement for source-derived E01-E03/N01 mapping. The detailed specifications take precedence over earlier generic SDK/distribution proposals; blocked platform/language/rights features remain blocked.
