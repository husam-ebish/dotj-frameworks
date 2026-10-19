# DJ-034 .j MQTT: pinned upstream

| Field | Value |
|---|---|
| Requested source | https://github.com/dotnet/MQTTnet |
| Effective canonical source | https://github.com/dotnet/MQTTnet |
| Immutable analysis revision | `798a0e2250f40a241e0c8d2e7c9a366051be1b97` |
| Immutable tree | [798a0e2250f40a241e0c8d2e7c9a366051be1b97](https://github.com/dotnet/MQTTnet/tree/798a0e2250f40a241e0c8d2e7c9a366051be1b97) |
| Retrieval date | 2026-10-19 |
| Recorded tree scope | recursive complete |
| Listed blob paths | 499 |
| New sampled source/API/test files | 5 |
| Eligible release family | OPEN: select a release/tag or explicitly qualify this analysis pin |
| Oracle executable | OPEN: pin compiler/runtime/build flags and license eligibility; none run here |


## Reproduction and baseline gate

Fetch an immutable archive or checkout at the hash above, verify its identity, retain license/notice files, and record submodule commits and generated-input hashes. Restore/build only within a controlled reference environment after evaluating repository build scripts and dependency rights. Resolve the selected release against this pin; a new pin invalidates affected API/test/dependency mappings and must be recorded as a reviewable diff. Do not equate a GitHub default branch or a successful download with a supported release.

## New evidence manifest

| File | SHA-256 |
|---|---|
| [Source/MQTTnet.AspnetCore/DuplexPipe.cs](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/DuplexPipe.cs) | `ada5c79d2c144a0264a8a23ffa93c394e85e88f0fab2ecdee86ffacc3dbb9c59` |
| [Source/MQTTnet.AspnetCore/SocketSender.cs](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/SocketSender.cs) | `c643c30b0cc00add561ddaa5c69e279b2c7c8f106967852c7559385eb94d261e` |
| [Source/MQTTnet/MqttClient.cs](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet/MqttClient.cs) | `4c88641a7ae25ffb9669f7691fe620a7c20a6e38a3184c624c0dd2cf7501eee6` |
| [Source/MQTTnet.Tests/Protocol_Tests.cs](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/Protocol_Tests.cs) | `44e80c36f2a62e253c1fd3b1aaf0f468e4732b6bdea8e667a7da00cca1bb67bc` |
| [Source/MQTTnet.Tests/RoundtripTime_Tests.cs](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.Tests/RoundtripTime_Tests.cs) | `8f3959c512b5a01c5d31004ca30dc01b1107ad5fd4ffb391bc90166b99318264` |


The [machine-readable inventory](evidence/inventory.json) includes all listed paths and sampled-file hashes. Retrieval errors: none in this pass.
