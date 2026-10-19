# Module and API inventory: first Stage-2 increment

Status: **INCOMPLETE**. Upstream analysis pin: `9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819`. Inspection date: 2026-10-19.

## Verified inventory boundary

The complete non-recursive `src/libraries` tree contains **218 directories**. This is a directory count, not a package, public API or implementation count. The API response has `truncated=false`. Full recursive per-directory enumeration remains pending. The former Stage-1 truncated root listing must not be used as a complete inventory.

Read **47 selected files**, including **8 reference API files** and **12 test-source files**. The reference files contain **1061 lexical public/protected declaration candidates**. This count is not a semantic API count: overloads, nested types, conditional compilation and generated declarations still need parser/build-aware analysis. The test extraction similarly includes helper-method candidates and is not a test count.

The machine-readable [directory inventory](evidence/library-directory-inventory.json), [API candidates](evidence/public-api-candidates.json), [source manifest](evidence/source-manifest.json), [dependency declarations](evidence/declared-dependencies.json) and [test-method candidates](evidence/test-method-candidates.json) preserve the extraction scope and source links.

## Runtime source branches

| src child | Type | Stage-2 disposition |
|---|---|---|
| coreclr | tree | Retained; detailed mapping pending |
| installer | tree | Retained; detailed mapping pending |
| libraries | tree | Library subtree inventory started |
| mono | tree | Retained; detailed mapping pending |
| native | tree | Retained; detailed mapping pending |
| samples | tree | Retained; detailed mapping pending |
| tasks | tree | Retained; detailed mapping pending |
| tests | tree | Retained; detailed mapping pending |
| tools | tree | Retained; detailed mapping pending |

CoreCLR, Mono, native runtime support, tests and build infrastructure are retained. A JVM library implementation does not implicitly reproduce those runtime backends. VM/compiler/ABI/native tracks remain separate feasibility work.

## Every library directory, without silent exclusions

| Directory | Family | Selected files read | Detailed status |
|---|---|---|---|
| [Common](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Common/) | Infrastructure/compatibility | 0 | PENDING |
| [Fuzzing](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Fuzzing/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Bcl.AsyncInterfaces](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Bcl.AsyncInterfaces/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Bcl.Cryptography](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Bcl.Cryptography/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Bcl.Memory](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Bcl.Memory/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Bcl.Numerics](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Bcl.Numerics/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Bcl.TimeProvider](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Bcl.TimeProvider/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.CSharp](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.CSharp/) | Base libraries | 0 | PENDING |
| [Microsoft.Extensions.Caching.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Caching.Abstractions/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Caching.Memory](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Caching.Memory/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Abstractions/) | Extensions | 2 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.Configuration.Binder](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Binder/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.CommandLine](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.CommandLine/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.EnvironmentVariables](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.EnvironmentVariables/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.FileExtensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.FileExtensions/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.Ini](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Ini/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.Json](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Json/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.UserSecrets](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.UserSecrets/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration.Xml](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration.Xml/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Configuration](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Configuration/) | Extensions | 6 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.DependencyInjection.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection.Abstractions/) | Extensions | 2 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.DependencyInjection.Specification.Tests](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection.Specification.Tests/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.DependencyInjection](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyInjection/) | Extensions | 8 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.DependencyModel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.DependencyModel/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Diagnostics.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Diagnostics.Abstractions/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Diagnostics](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Diagnostics/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.FileProviders.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Abstractions/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.FileProviders.Composite](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Composite/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.FileProviders.Physical](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileProviders.Physical/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.FileSystemGlobbing](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.FileSystemGlobbing/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.HostFactoryResolver](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.HostFactoryResolver/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Hosting.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.Abstractions/) | Extensions | 4 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.Hosting.Systemd](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.Systemd/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Hosting.WindowsServices](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting.WindowsServices/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Hosting](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Hosting/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Http](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Http/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.Abstractions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Abstractions/) | Extensions | 3 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.Logging.Configuration](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Configuration/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.Console](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Console/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.Debug](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.Debug/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.EventLog](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.EventLog/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.EventSource](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.EventSource/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging.TraceSource](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging.TraceSource/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Logging](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Logging/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Options.ConfigurationExtensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options.ConfigurationExtensions/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Options.DataAnnotations](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options.DataAnnotations/) | Extensions | 0 | PENDING |
| [Microsoft.Extensions.Options](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Options/) | Extensions | 6 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Extensions.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Extensions.Primitives/) | Extensions | 5 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [Microsoft.Internal.Runtime.AspNetCore.Transport](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Internal.Runtime.AspNetCore.Transport/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Internal.Runtime.DotNetApiDocs.Transport](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Internal.Runtime.DotNetApiDocs.Transport/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.Internal.Runtime.WindowsDesktop.Transport](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Internal.Runtime.WindowsDesktop.Transport/) | Runtime/platform | 0 | PENDING |
| [Microsoft.NET.WebAssembly.Threading](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.NET.WebAssembly.Threading/) | Runtime/platform | 0 | PENDING |
| [Microsoft.NETCore.Platforms](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.NETCore.Platforms/) | Infrastructure/compatibility | 0 | PENDING |
| [Microsoft.VisualBasic.Core](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.VisualBasic.Core/) | Base libraries | 0 | PENDING |
| [Microsoft.Win32.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Win32.Primitives/) | Runtime/platform | 0 | PENDING |
| [Microsoft.Win32.Registry.AccessControl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Win32.Registry.AccessControl/) | Runtime/platform | 0 | PENDING |
| [Microsoft.Win32.Registry](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Win32.Registry/) | Runtime/platform | 0 | PENDING |
| [Microsoft.Win32.SystemEvents](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.Win32.SystemEvents/) | Runtime/platform | 0 | PENDING |
| [Microsoft.XmlSerializer.Generator](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/Microsoft.XmlSerializer.Generator/) | Base libraries | 0 | PENDING |
| [System.CodeDom](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.CodeDom/) | Base libraries | 0 | PENDING |
| [System.Collections.Concurrent](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Collections.Concurrent/) | Base libraries | 0 | PENDING |
| [System.Collections.Immutable](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Collections.Immutable/) | Base libraries | 0 | PENDING |
| [System.Collections.NonGeneric](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Collections.NonGeneric/) | Base libraries | 0 | PENDING |
| [System.Collections.Specialized](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Collections.Specialized/) | Base libraries | 0 | PENDING |
| [System.Collections](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Collections/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.Annotations](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.Annotations/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.Composition.Registration](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.Composition.Registration/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.Composition](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.Composition/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.EventBasedAsync](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.EventBasedAsync/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.Primitives/) | Base libraries | 0 | PENDING |
| [System.ComponentModel.TypeConverter](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel.TypeConverter/) | Base libraries | 0 | PENDING |
| [System.ComponentModel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ComponentModel/) | Base libraries | 0 | PENDING |
| [System.Composition.AttributedModel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition.AttributedModel/) | Base libraries | 0 | PENDING |
| [System.Composition.Convention](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition.Convention/) | Base libraries | 0 | PENDING |
| [System.Composition.Hosting](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition.Hosting/) | Base libraries | 0 | PENDING |
| [System.Composition.Runtime](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition.Runtime/) | Base libraries | 0 | PENDING |
| [System.Composition.TypedParts](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition.TypedParts/) | Base libraries | 0 | PENDING |
| [System.Composition](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Composition/) | Base libraries | 0 | PENDING |
| [System.Configuration.ConfigurationManager](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Configuration.ConfigurationManager/) | Base libraries | 0 | PENDING |
| [System.Console](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Console/) | Base libraries | 0 | PENDING |
| [System.Data.Common](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Data.Common/) | Base libraries | 0 | PENDING |
| [System.Data.Odbc](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Data.Odbc/) | Runtime/platform | 0 | PENDING |
| [System.Data.OleDb](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Data.OleDb/) | Runtime/platform | 0 | PENDING |
| [System.Diagnostics.Contracts](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.Contracts/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.DiagnosticSource](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.DiagnosticSource/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.EventLog](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.EventLog/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.FileVersionInfo](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.FileVersionInfo/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.PerformanceCounter](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.PerformanceCounter/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.Process](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.Process/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.StackTrace](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.StackTrace/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.TextWriterTraceListener](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.TextWriterTraceListener/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.TraceSource](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.TraceSource/) | Base libraries | 0 | PENDING |
| [System.Diagnostics.Tracing](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Diagnostics.Tracing/) | Base libraries | 0 | PENDING |
| [System.DirectoryServices.AccountManagement](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.DirectoryServices.AccountManagement/) | Runtime/platform | 0 | PENDING |
| [System.DirectoryServices.Protocols](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.DirectoryServices.Protocols/) | Runtime/platform | 0 | PENDING |
| [System.DirectoryServices](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.DirectoryServices/) | Runtime/platform | 0 | PENDING |
| [System.Drawing.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Drawing.Primitives/) | Base libraries | 0 | PENDING |
| [System.Formats.Asn1](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Formats.Asn1/) | Base libraries | 0 | PENDING |
| [System.Formats.Cbor](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Formats.Cbor/) | Base libraries | 0 | PENDING |
| [System.Formats.Nrbf](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Formats.Nrbf/) | Base libraries | 0 | PENDING |
| [System.Formats.Tar](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Formats.Tar/) | Base libraries | 0 | PENDING |
| [System.IO.Compression.Brotli](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Compression.Brotli/) | Base libraries | 0 | PENDING |
| [System.IO.Compression.ZipFile](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Compression.ZipFile/) | Base libraries | 0 | PENDING |
| [System.IO.Compression](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Compression/) | Base libraries | 0 | PENDING |
| [System.IO.FileSystem.AccessControl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.FileSystem.AccessControl/) | Base libraries | 0 | PENDING |
| [System.IO.FileSystem.DriveInfo](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.FileSystem.DriveInfo/) | Base libraries | 0 | PENDING |
| [System.IO.FileSystem.Watcher](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.FileSystem.Watcher/) | Base libraries | 0 | PENDING |
| [System.IO.Hashing](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Hashing/) | Base libraries | 0 | PENDING |
| [System.IO.IsolatedStorage](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.IsolatedStorage/) | Base libraries | 0 | PENDING |
| [System.IO.MemoryMappedFiles](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.MemoryMappedFiles/) | Base libraries | 0 | PENDING |
| [System.IO.Packaging](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Packaging/) | Base libraries | 0 | PENDING |
| [System.IO.Pipelines](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Pipelines/) | Base libraries | 0 | PENDING |
| [System.IO.Pipes.AccessControl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Pipes.AccessControl/) | Base libraries | 0 | PENDING |
| [System.IO.Pipes](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Pipes/) | Base libraries | 0 | PENDING |
| [System.IO.Ports](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.IO.Ports/) | Base libraries | 0 | PENDING |
| [System.Linq.AsyncEnumerable](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq.AsyncEnumerable/) | Base libraries | 0 | PENDING |
| [System.Linq.Expressions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq.Expressions/) | Base libraries | 0 | PENDING |
| [System.Linq.Parallel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq.Parallel/) | Base libraries | 0 | PENDING |
| [System.Linq.Queryable](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq.Queryable/) | Base libraries | 0 | PENDING |
| [System.Linq](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Linq/) | Base libraries | 0 | PENDING |
| [System.Management](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Management/) | Runtime/platform | 0 | PENDING |
| [System.Memory.Data](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Memory.Data/) | Base libraries | 0 | PENDING |
| [System.Memory](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Memory/) | Base libraries | 0 | PENDING |
| [System.Net.Http.Json](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Http.Json/) | Base libraries | 0 | PENDING |
| [System.Net.Http.WinHttpHandler](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Http.WinHttpHandler/) | Base libraries | 0 | PENDING |
| [System.Net.Http](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Http/) | Base libraries | 0 | PENDING |
| [System.Net.HttpListener](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.HttpListener/) | Base libraries | 0 | PENDING |
| [System.Net.Mail](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Mail/) | Base libraries | 0 | PENDING |
| [System.Net.NameResolution](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.NameResolution/) | Base libraries | 0 | PENDING |
| [System.Net.NetworkInformation](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.NetworkInformation/) | Base libraries | 0 | PENDING |
| [System.Net.Ping](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Ping/) | Base libraries | 0 | PENDING |
| [System.Net.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Primitives/) | Base libraries | 0 | PENDING |
| [System.Net.Quic](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Quic/) | Base libraries | 0 | PENDING |
| [System.Net.Requests](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Requests/) | Base libraries | 0 | PENDING |
| [System.Net.Security](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Security/) | Base libraries | 0 | PENDING |
| [System.Net.ServerSentEvents](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.ServerSentEvents/) | Base libraries | 0 | PENDING |
| [System.Net.Sockets](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.Sockets/) | Base libraries | 0 | PENDING |
| [System.Net.WebClient](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.WebClient/) | Base libraries | 0 | PENDING |
| [System.Net.WebHeaderCollection](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.WebHeaderCollection/) | Base libraries | 0 | PENDING |
| [System.Net.WebProxy](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.WebProxy/) | Base libraries | 0 | PENDING |
| [System.Net.WebSockets.Client](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.WebSockets.Client/) | Base libraries | 0 | PENDING |
| [System.Net.WebSockets](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Net.WebSockets/) | Base libraries | 0 | PENDING |
| [System.Numerics.Tensors](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Numerics.Tensors/) | Base libraries | 0 | PENDING |
| [System.Numerics.Vectors](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Numerics.Vectors/) | Base libraries | 0 | PENDING |
| [System.ObjectModel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ObjectModel/) | Base libraries | 0 | PENDING |
| [System.Private.CoreLib](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Private.CoreLib/) | Base libraries | 6 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [System.Private.DataContractSerialization](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Private.DataContractSerialization/) | Base libraries | 0 | PENDING |
| [System.Private.Uri](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Private.Uri/) | Base libraries | 0 | PENDING |
| [System.Private.Xml.Linq](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Private.Xml.Linq/) | Base libraries | 0 | PENDING |
| [System.Private.Xml](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Private.Xml/) | Base libraries | 0 | PENDING |
| [System.Reflection.Context](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Context/) | Base libraries | 0 | PENDING |
| [System.Reflection.DispatchProxy](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.DispatchProxy/) | Base libraries | 0 | PENDING |
| [System.Reflection.Emit.ILGeneration](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Emit.ILGeneration/) | Runtime/platform | 0 | PENDING |
| [System.Reflection.Emit.Lightweight](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Emit.Lightweight/) | Runtime/platform | 0 | PENDING |
| [System.Reflection.Emit](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Emit/) | Runtime/platform | 0 | PENDING |
| [System.Reflection.Extensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Extensions/) | Base libraries | 0 | PENDING |
| [System.Reflection.Metadata](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Metadata/) | Base libraries | 0 | PENDING |
| [System.Reflection.MetadataLoadContext](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.MetadataLoadContext/) | Base libraries | 0 | PENDING |
| [System.Reflection.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.Primitives/) | Base libraries | 0 | PENDING |
| [System.Reflection.TypeExtensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Reflection.TypeExtensions/) | Base libraries | 0 | PENDING |
| [System.Resources.Extensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Resources.Extensions/) | Base libraries | 0 | PENDING |
| [System.Resources.Writer](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Resources.Writer/) | Base libraries | 0 | PENDING |
| [System.Runtime.Caching](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Caching/) | Base libraries | 0 | PENDING |
| [System.Runtime.CompilerServices.VisualC](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.CompilerServices.VisualC/) | Base libraries | 0 | PENDING |
| [System.Runtime.InteropServices.JavaScript](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.InteropServices.JavaScript/) | Runtime/platform | 0 | PENDING |
| [System.Runtime.InteropServices](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.InteropServices/) | Runtime/platform | 0 | PENDING |
| [System.Runtime.Intrinsics](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Intrinsics/) | Runtime/platform | 0 | PENDING |
| [System.Runtime.Loader](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Loader/) | Base libraries | 0 | PENDING |
| [System.Runtime.Numerics](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Numerics/) | Base libraries | 0 | PENDING |
| [System.Runtime.Serialization.Formatters](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Serialization.Formatters/) | Base libraries | 0 | PENDING |
| [System.Runtime.Serialization.Json](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Serialization.Json/) | Base libraries | 0 | PENDING |
| [System.Runtime.Serialization.Primitives](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Serialization.Primitives/) | Base libraries | 0 | PENDING |
| [System.Runtime.Serialization.Schema](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Serialization.Schema/) | Base libraries | 0 | PENDING |
| [System.Runtime.Serialization.Xml](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime.Serialization.Xml/) | Base libraries | 0 | PENDING |
| [System.Runtime](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Runtime/) | Base libraries | 1 | INITIAL SAMPLE ANALYZED; full module audit pending |
| [System.Security.AccessControl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.AccessControl/) | Base libraries | 0 | PENDING |
| [System.Security.Claims](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Claims/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.Cng](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.Cng/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.Cose](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.Cose/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.Csp](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.Csp/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.OpenSsl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.OpenSsl/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.Pkcs](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.Pkcs/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.ProtectedData](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.ProtectedData/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography.Xml](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography.Xml/) | Base libraries | 0 | PENDING |
| [System.Security.Cryptography](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Cryptography/) | Base libraries | 0 | PENDING |
| [System.Security.Permissions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Permissions/) | Base libraries | 0 | PENDING |
| [System.Security.Principal.Windows](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Security.Principal.Windows/) | Runtime/platform | 0 | PENDING |
| [System.ServiceModel.Syndication](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ServiceModel.Syndication/) | Base libraries | 0 | PENDING |
| [System.ServiceProcess.ServiceController](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.ServiceProcess.ServiceController/) | Base libraries | 0 | PENDING |
| [System.Speech](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Speech/) | Runtime/platform | 0 | PENDING |
| [System.Text.Encoding.CodePages](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Text.Encoding.CodePages/) | Base libraries | 0 | PENDING |
| [System.Text.Encoding.Extensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Text.Encoding.Extensions/) | Base libraries | 0 | PENDING |
| [System.Text.Encodings.Web](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Text.Encodings.Web/) | Base libraries | 0 | PENDING |
| [System.Text.Json](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Text.Json/) | Base libraries | 0 | PENDING |
| [System.Text.RegularExpressions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Text.RegularExpressions/) | Base libraries | 0 | PENDING |
| [System.Threading.AccessControl](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.AccessControl/) | Base libraries | 0 | PENDING |
| [System.Threading.Channels](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Channels/) | Base libraries | 0 | PENDING |
| [System.Threading.Overlapped](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Overlapped/) | Base libraries | 0 | PENDING |
| [System.Threading.RateLimiting](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.RateLimiting/) | Base libraries | 0 | PENDING |
| [System.Threading.Tasks.Dataflow](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Tasks.Dataflow/) | Base libraries | 0 | PENDING |
| [System.Threading.Tasks.Parallel](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Tasks.Parallel/) | Base libraries | 0 | PENDING |
| [System.Threading.Thread.WebAssembly.Threading](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Thread.WebAssembly.Threading/) | Runtime/platform | 0 | PENDING |
| [System.Threading.Thread](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.Thread/) | Base libraries | 0 | PENDING |
| [System.Threading.ThreadPool.WebAssembly.Threading](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.ThreadPool.WebAssembly.Threading/) | Runtime/platform | 0 | PENDING |
| [System.Threading.ThreadPool](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.ThreadPool/) | Base libraries | 0 | PENDING |
| [System.Threading.WebAssembly.Threading](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading.WebAssembly.Threading/) | Runtime/platform | 0 | PENDING |
| [System.Threading](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Threading/) | Base libraries | 0 | PENDING |
| [System.Transactions.Local](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Transactions.Local/) | Base libraries | 0 | PENDING |
| [System.Web.HttpUtility](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Web.HttpUtility/) | Base libraries | 0 | PENDING |
| [System.Windows.Extensions](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Windows.Extensions/) | Runtime/platform | 0 | PENDING |
| [System.Xml.ReaderWriter](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Xml.ReaderWriter/) | Base libraries | 0 | PENDING |
| [System.Xml.XDocument](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Xml.XDocument/) | Base libraries | 0 | PENDING |
| [System.Xml.XPath.XDocument](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Xml.XPath.XDocument/) | Base libraries | 0 | PENDING |
| [System.Xml.XPath](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Xml.XPath/) | Base libraries | 0 | PENDING |
| [System.Xml.XmlSerializer](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/System.Xml.XmlSerializer/) | Base libraries | 0 | PENDING |
| [apicompat](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/apicompat/) | Infrastructure/compatibility | 0 | PENDING |
| [shims](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/shims/) | Infrastructure/compatibility | 0 | PENDING |
| [testPackages](https://github.com/dotnet/runtime/tree/9b1b0e9c699a54a2b8e8241bbc2ab650bd89d819/src/libraries/testPackages/) | Infrastructure/compatibility | 0 | PENDING |

## Ownership findings to reconcile with Stage 1

- System.Text.Json remains a runtime-origin capability under dotj-core. dotj-json remains the Newtonsoft.Json port. Separate behavior profiles are required; sharing a future lower-level codec is an architecture decision, not evidence of compatibility.
- Microsoft.Extensions implementation packages in runtime remain owned by dotj-core, including its default DI engine. dotj-container is the separate Autofac-derived product.
- Configuration.Json adapters can depend on the runtime JSON artifact without making every core abstraction load JSON. No umbrella core artifact should require all core modules.
- System.IO.Packaging remains visible as runtime-origin source while dotj-openxml owns Office Open XML behavior. Shared OPC ownership needs an explicit decision; neither capability may disappear.
- System.Net.Mail and MailKit have different source scopes. Retain both; any shared transport must preserve their separate public behavior.
- System.Threading.RateLimiting and Polly-derived resilience are separate capabilities. Reuse must not erase distinct contracts.

## Remaining census work

Enumerate each subtree fully; inventory all public symbols with namespace/signature/conditions; resolve type forwarding, shims, shared compile items, generated files and native branches. Map every API to JDK direct use, owned Java behavior, explicit Java adaptation, or feasibility blocker. Enumerate attributed test cases and data sources semantically before reporting a definitive test count. All unsampled directories remain pending, not excluded.
