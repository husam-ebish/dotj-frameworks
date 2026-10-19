# Provenance, license evidence and upstream maintenance

## Immutable baseline record

Every repository has a source URL, analysis commit and sample hashes in PINNED-UPSTREAM and evidence/inventory.json. These are analysis pins, not automatically approved releases. Qualify the chosen release, submodules, generated inputs, compiler/runtime, dependency locks, native binaries and browser assets before implementation. The runtime pin requests a release-candidate .NET SDK; do not label it a GA release.

## Rights gates

AutoMapper and MediatR inspected LICENSE.md texts reference RPL 1.5 or a separate agreement. Historical MIT assumptions do not clear those revisions. Hangfire has LGPL/commercial distinctions; commercial add-ons need their own scope. Avalonia root MIT text coexists with third-party NOTICE entries. MassTransit terms observed at one pin do not prove every release/product uses the same terms. Similar per-version checks apply to all targets. These are evidence observations, not legal clearance.

Record what is copied, adapted, independently implemented, generated or merely used as a behavior reference. Preserve exact license/notice obligations for source, tests, schemas, icons, fonts, snippets, generated templates and native helper images. Build-time-only dependencies still require a record, even when they are not shipped. Do not publish under a chosen project license until the composition of applicable rights is established.

## Change tracking

Compare old/new immutable trees and effective build manifests; classify changes as API, behavior, protocol, schema, test, dependency, license, asset or platform. Re-run affected oracle fixtures. Update adapters only after the shared contract diff is reviewed. Keep each .j release's supported upstream profile and known deviations; never use an unqualified “latest compatible” label.

## Artifacts and release evidence

Use stable task/fixture IDs, source/dependency/toolchain locks, SBOM, notices, build commands, artifact hashes, signed provenance where configured, platform results and migration examples. Reproducibility means identical artifacts or explicitly explained non-reproducible fields, not merely two successful builds. Publishing is outside this planning task.

## Retention and examples

Store small fixtures with source provenance; large external datasets/binaries need hashes and reproducible retrieval instructions plus redistribution eligibility. Strip credentials and personal data from captured traffic. Keep source locations and line numbers as navigation aids; the immutable commit and content hash provide identity when layout changes.
