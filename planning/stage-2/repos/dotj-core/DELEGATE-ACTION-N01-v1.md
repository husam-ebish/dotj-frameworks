# Public delegates: System.Action

Batch 2507 adds the owner-selected delegate representation for `DJ-001-N01-T2`: public delegates are real classes, and plain javac callers wrap a lambda.

```java
Action log = new Action(() -> Log());
Action both = (Action) Delegate.Combine(log, audit);
both.Invoke();
```

## Selected public surface

| Type | Members |
|---|---|
| `System.Delegate` | `Combine(a, b)`, `Combine(params)`, `Remove`, `RemoveAll`, `CombineImpl`, `RemoveImpl`, `GetInvocationList`, `Equals`, `GetHashCode` |
| `System.MulticastDelegate` | Immutable invocation list behind the same members |
| `System.Action` | Constructor from a lambda, `Invoke` |

`DelegateFixtures.java` compiles against the public sources, and `DelegateOracle.cs` runs the same scenarios on .NET 10.0.12. All 34 observations match. They cover invocation order, null handling, immutable lists, last-occurrence and group removal, `RemoveAll`, equality, hash codes and stopping at the first exception.

## Syntax difference

C# converts a method group or lambda to `Action` directly. Plain javac cannot convert a lambda to a class, so callers write `new Action(() -> ...)`. The constructor takes `org.dotj.internal.delegates.ActionBody`, a lambda target that callers never name. A later compiler step may drop the wrapper.

## Limits

- A Java lambda is compared by object identity, so two separately written identical lambdas are not equal. In C#, two delegates to the same method are equal. Reuse the same lambda value, as the fixture does.
- `Delegate.Target`, `Method`, `DynamicInvoke`, `CreateDelegate`, `Clone`, `==` and `!=`, `ICloneable`, `ISerializable`, `BeginInvoke` and `EndInvoke` are not provided.
- Generic `Action<T>`, `Func<>` and `Type` metadata for the new classes are not provided.
- `System.Reflection.TypeFilter` and `MemberFilter` are still interfaces and must migrate to this representation.
- No acceptance credit is granted.
