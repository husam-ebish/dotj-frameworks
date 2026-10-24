# Selected Stopwatch monotonic candidate

Plan scope: `DJ-001-WP-05-T3`, in progress. The product candidate uses JDK APIs only.

| Native concept | Java carrier | Selected scope |
|---|---|---|
| System.Diagnostics.Stopwatch | Public nonfinal class; public empty constructor | Separate native metadata snapshot; the existing thirty-type foundation identity gate remains a selected subset |
| Frequency / IsHighResolution | Static final fields | Selected 10,000,000-count-per-second profile matches the pinned Windows reference; no cross-platform native frequency equivalence claimed |
| GetTimestamp | JDK nanoTime delta from an opaque class-loader origin, divided into 100 ns units | Same-domain differences only; DateTime ticks are wall-clock values and cannot be substituted |
| GetElapsedTime overloads | Existing TimeSpan carrier with unchecked signed counter subtraction and double tick conversion | Pinned signed extrema and boundary vectors |
| Start, Stop, Reset, Restart, StartNew | Selected running/stopped and accumulated-counter behavior | Native-checked live states, repeated Start/Stop, reset/restart and factory paths |
| IsRunning, Elapsed, ElapsedTicks, ElapsedMilliseconds, ToString | get_ property carriers, exact public names and one Java toString hook | Native conversion and constant-format parsing validate elapsed-property windows and text |

The reference is .NET 10.0.12 CoreLib. The pinned source archive contains `src/libraries/System.Private.CoreLib/src/System/Diagnostics/Stopwatch.cs`, SHA-256 `8ee76eff6d199d65064dd6e8b29e05b95722e670a8af8dd048c6d7fb84957955`; platform partials supply the native counter backend. These are reference inputs. The Java implementation uses System.nanoTime and does not add a native runtime library dependency.

The new source and its single class are explicitly registered in the candidate build and file map. Source provenance and notice applicability remain E01 review inputs; no rights decision is closed by these checks.

Counter origin is opaque and isolated to one loaded backend. Clock resolution, suspend/resume behavior, signed nanoTime lifetime limits, arbitrary cross-loader timestamps, thread safety/concurrent state transitions, full Type/reflection projection, source-language dispatch and release qualification remain open. Instance methods use Java final methods for the selected nonvirtual native operations; the native virtual ToString and Java hook remain overridable. This does not qualify all inheritance or language behavior. No implementation task is accepted by a passing candidate gate.
