# Selected exception constructor contract

The pinned .NET 10.0.12 oracle compares nineteen existing candidate exception types. The selected public constructors use String, Exception, Int32 or Object arguments; serialization constructors are excluded. Supplied and null-reference profiles verify constructor availability, default or explicit HRESULT, inner-exception identity, ParamName and FileName where applicable. HRESULT setter exposure remains a separate API qualification question.

SystemException and eight derived candidates now set their own default HRESULT rather than inheriting System.Exception's value. IOException and InvalidCastException preserve explicit error-code arguments. NullReferenceException exposes the message-and-inner constructor.

| Scope | Status |
|---|---|
| Product runtime | JDK APIs only; no additional runtime library |
| Reference validation | Pinned .NET runtime and PowerShell delegate/reflection tooling; Python and JDK probes |
| Broader project | Complete dependency graph and distribution remain open |
| Acceptance | Bounded constructor evidence only; no implementation task, E01 decision or framework accepted |
| Remaining | Default/localized messages, serialization, throw/language integration and full public qualification |
