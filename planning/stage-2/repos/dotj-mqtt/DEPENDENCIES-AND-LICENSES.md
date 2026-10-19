# DJ-034 .j MQTT: dependencies and licenses

## Proposed Java dependencies

core;web(optional)

These are proposed target edges, not dependencies proven by the upstream build. Parenthesized optional/dev edges stay outside the base runtime artifact. Split adapters before resolving a cycle; core never imports a downstream product implementation.

JDK/platform basis: NIO, SSLEngine, buffers and scheduled executors.

Bootstrap with locked installed javac/jar and small standalone fixture runners. Tool repositories must run before SDK/registry exist; use local deterministic artifact folders and explicit module/class paths. Existing Java frameworks are not implementation substitutes. External platforms/native libraries require a dependency record with capability, version, source, license, ABI and reason a JDK/owned implementation cannot satisfy the need.

## Observed upstream declarations

The following are declarations retrieved from source metadata, not a fully restored conditional/transitive graph. Version catalogs alone are not proof that an artifact ships in this product.

| Kind | Identity | Evidence |
|---|---|---|
| FrameworkReference | Microsoft.AspNetCore.App | [Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj) |
| ProjectReference | ..\MQTTnet.Server\MQTTnet.Server.csproj | [Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj) |
| ProjectReference | ..\MQTTnet\MQTTnet.csproj | [Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspnetCore/MQTTnet.AspNetCore.csproj) |
| ProjectReference | ..\..\Source\MQTTnet.AspnetCore\MQTTnet.AspNetCore.csproj | [Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj) |
| ProjectReference | ..\..\Source\MQTTnet.Server\MQTTnet.Server.csproj | [Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj) |
| ProjectReference | ..\MQTTnet\MQTTnet.csproj | [Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/Source/MQTTnet.AspTestApp/MQTTnet.AspTestApp.csproj) |


## License evidence and eligibility gate

Observed metadata hint: `MIT`.

Observed root metadata/license text is evidence, not a completed eligibility review. Resolve conditional/transitive dependencies, embedded assets, generated inputs and redistributable binaries before source reuse or release.

| Retrieved notice/license | Immutable source |
|---|---|
| [LICENSE](evidence/notices/LICENSE) | [LICENSE](https://github.com/dotnet/MQTTnet/blob/798a0e2250f40a241e0c8d2e7c9a366051be1b97/LICENSE) |

## Dependency closure deliverable

E02 must produce one row per effective dependency: consuming module; declaration and condition; resolved version/hash; runtime/dev/test/native/asset role; canonical source; license/notice evidence; proposed JDK/owned/optional-external disposition; required redistribution files; unresolved eligibility and owner role. Track missing upstreams as UD-mqtt-NNN. Do not increase the 66 target count merely because an additional source is required.

[Shared ownership and discovery ledger](../../04-OWNERSHIP-AND-DEPENDENCIES.md)
