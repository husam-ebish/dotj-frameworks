# IDisposable paired usage (contract sketch)

C# reference:
```csharp
IDisposable resource = CreateResource();
try { Use(resource); } finally { resource.Dispose(); }
```

Java syntax probe:
```java
System.IDisposable resource = createResource();
try { use(resource); } finally { resource.Dispose(); }
```

`CreateResource`/`Use` and their Java spellings are example-local functions, not framework API. The `System.IDisposable` Java source lives only in `java-probes`; product release and disposal semantics are open.
