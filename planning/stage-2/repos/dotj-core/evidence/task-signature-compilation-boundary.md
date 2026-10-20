# Restricted Task signature compilation experiment

Batch-717 connects the bounded Task-family signature binder and source renderer to the supported JDK 21 `JavaCompiler` API. It accepts an explicit list of abstract method signatures and emits one abstract Java class. The caller supplies fixture classes and owns the output directory. The experiment verifies that `Task` and `Task<T>` retain their source identities while receiving distinct JVM names (`Task` and `Task_1`). It rejects malformed signatures and colliding imports through the existing binder and renderer.

This is internal compiler integration evidence. It does not parse a `.j` file, resolve an arbitrary .NET type, implement Task semantics, or establish the `dotj-code` language profile. `dotj-code` E01-E03/N01 and the public core contract remain open. Generated fixture support types are test inputs, not product API implementations.

Verification: `tools/oracle/dotj-core/run-arity-source-compiler.ps1` compiles the internal sources, compiles a generated abstract class against fixture Task types, checks emitted bytecode, and removes its temporary output. `tools/oracle/dotj-core/build-internal-core.ps1` packages only internal development classes and refreshes its hash manifest.
