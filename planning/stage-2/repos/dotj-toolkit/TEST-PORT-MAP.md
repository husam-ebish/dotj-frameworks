# DJ-045 .j Toolkit: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:23](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L23) | Test_Messenger_UnregisterRecipientWithMessageType | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:34](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L34) | Test_Messenger_UnregisterRecipientWithMessageTypeAndToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:45](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L45) | Test_Messenger_UnregisterRecipientWithToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:56](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L56) | Test_Messenger_UnregisterRecipientWithRecipient | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:67](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L67) | Test_Messenger_RegisterAndUnregisterRecipientWithMessageType | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:84](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L84) | Test_Messenger_RegisterAndUnregisterRecipientWithMessageTypeAndToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:101](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L101) | Test_Messenger_RegisterAndUnregisterRecipientWithMessageTypeAndMultipleTokens | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:171](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L171) | Test_Messenger_RegisterAndUnregisterRecipientWithToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:188](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L188) | Test_Messenger_RegisterAndUnregisterRecipientWithRecipient | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:205](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L205) | Test_Messenger_IsRegistered_Register_Send_UnregisterOfTMessage_WithNoToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:244](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L244) | Test_Messenger_IsRegistered_Register_Send_UnregisterRecipient_WithNoToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:273](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L273) | Test_Messenger_IsRegistered_Register_Send_UnregisterOfTMessage_WithToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:302](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L302) | Test_Messenger_DuplicateRegistrationWithMessageType | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:318](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L318) | Test_Messenger_DuplicateRegistrationWithMessageTypeAndToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:334](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L334) | Test_Messenger_IRecipient_NoMessages | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:348](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L348) | Test_Messenger_IRecipient_SomeMessages_NoToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:381](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L381) | Test_Messenger_IRecipient_SomeMessages_WithGenericTypeParameters | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:414](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L414) | Test_Messenger_IRecipient_SomeMessages_WithToken | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:450](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L450) | Test_Messenger_RegisterWithTypeParameter | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:467](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L467) | Test_Messenger_Collect_Test | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:498](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L498) | Test_Messenger_Reset | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:517](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L517) | Test_Messenger_Default | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:532](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L532) | Test_Messenger_Cleanup | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:567](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L567) | Test_Messenger_ManyRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:614](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L614) | Test_Messenger_RegisterMultiple_UnregisterSingle | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:638](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L638) | Test_Messenger_ConcurrentOperations_DefaultChannel_SeparateRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:708](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L708) | Test_Messenger_ConcurrentOperations_DefaultChannel_SharedRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:777](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L777) | Test_Messenger_ConcurrentOperations_WithToken_SeparateRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:845](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L845) | Test_Messenger_ConcurrentOperations_WithToken_SharedRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:916](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L916) | Test_Messenger_ConcurrentOperations_Combined_SeparateRecipients | yes |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1052](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1052) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1057](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1057) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1079](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1079) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1084](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1084) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1107](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1107) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1112](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1112) | Receive | not confirmed |
| [tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs:1117](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Mvvm.UnitTests/Test_Messenger.cs#L1117) | Receive | not confirmed |
| [tests/CommunityToolkit.Common.UnitTests/Test_Converters.cs:20](https://github.com/CommunityToolkit/dotnet/blob/b135626dd54d33b8f05f2ff31591592c004aa848/tests/CommunityToolkit.Common.UnitTests/Test_Converters.cs#L20) | Test_ToFileSizeString | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-045-F01-01 | WP-01 | Notification order is deterministic | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F01-02 | WP-01 | concurrent command execution obeys policy | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F01-03 | WP-01 | cancelled commands expose cancellation distinctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F02-01 | WP-02 | Unsubscribed recipients stop receiving future deliveries | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F02-02 | WP-02 | token scopes do not collide | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F02-03 | WP-02 | weak subscriptions do not retain recipients indefinitely | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F03-01 | WP-03 | Generated sources compile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F03-02 | WP-03 | conflicts point to annotations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F03-03 | WP-03 | generated semantics match handwritten equivalents in fixtures | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F04-01 | WP-04 | Owned buffers have explicit lifetimes | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F04-02 | WP-04 | unsupported ref-struct semantics are documented | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F04-03 | WP-04 | optimizations preserve reference behavior | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F05-01 | WP-05 | Core toolkit has no UI runtime dependency | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F05-02 | WP-05 | generated code has stable diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-045-F05-03 | WP-05 | GC tests do not depend on arbitrary sleep timing | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Property-change order; command reentrancy; weak messenger lifetime; generated-source diagnostics; buffer boundary safety.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-045-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-045-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-045-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
