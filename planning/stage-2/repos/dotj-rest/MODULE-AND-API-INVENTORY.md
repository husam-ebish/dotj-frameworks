# DJ-032 .j REST: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 477 | recursive complete |
| Project-definition paths | 15 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 156 | Lexical path classification, not runnable test count |
| Sampled text files | 8 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 21 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 12 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/benchmarks/RestSharp.Benchmarks/RestSharp.Benchmarks.csproj) | example/benchmark/tool | Retained; semantic assignment and conditional build closure in E02 |
| [gen/SourceGenerator/SourceGenerator.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/gen/SourceGenerator/SourceGenerator.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/RestSharp.Extensions.DependencyInjection/RestSharp.Extensions.DependencyInjection.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp.Extensions.DependencyInjection/RestSharp.Extensions.DependencyInjection.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/RestSharp.Serializers.CsvHelper/RestSharp.Serializers.CsvHelper.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp.Serializers.CsvHelper/RestSharp.Serializers.CsvHelper.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp.Serializers.NewtonsoftJson/RestSharp.Serializers.NewtonsoftJson.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp.Serializers.Xml/RestSharp.Serializers.Xml.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [src/RestSharp/RestSharp.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/RestSharp.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.InteractiveTests/RestSharp.InteractiveTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.DependencyInjection/RestSharp.Tests.DependencyInjection.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.DependencyInjection/RestSharp.Tests.DependencyInjection.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.Integrated/RestSharp.Tests.Integrated.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.Integrated/RestSharp.Tests.Integrated.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.Serializers.Csv/RestSharp.Tests.Serializers.Csv.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.Serializers.Csv/RestSharp.Tests.Serializers.Csv.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.Serializers.Json/RestSharp.Tests.Serializers.Json.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.Serializers.Json/RestSharp.Tests.Serializers.Json.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.Serializers.Xml/RestSharp.Tests.Serializers.Xml.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.Serializers.Xml/RestSharp.Tests.Serializers.Xml.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests.Shared/RestSharp.Tests.Shared.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [test/RestSharp.Tests/RestSharp.Tests.csproj](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestSharp.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [src/RestSharp/Enum.cs:20](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Enum.cs#L20) | `public enum ParameterType {` |
| [src/RestSharp/Enum.cs:65](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Enum.cs#L65) | `public enum DataFormat { Json, Xml, Binary, None }` |
| [src/RestSharp/Enum.cs:70](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Enum.cs#L70) | `public enum Method {` |
| [src/RestSharp/Enum.cs:78](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Enum.cs#L78) | `public struct DateFormat {` |
| [src/RestSharp/Enum.cs:93](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Enum.cs#L93) | `public enum ResponseStatus {` |
| [src/RestSharp/Ensure.cs:18](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Ensure.cs#L18) | `public static T NotNull<T>(T? value, [InvokerParameterName] string name) => value ?? throw new ArgumentNullException(name);` |
| [src/RestSharp/Ensure.cs:20](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/src/RestSharp/Ensure.cs#L20) | `public static string NotEmptyString(object? value, [InvokerParameterName] string name) {` |
| [test/RestSharp.Tests/OptionsTests.cs:3](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/OptionsTests.cs#L3) | `public class OptionsTests {` |
| [test/RestSharp.Tests/OptionsTests.cs:5](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/OptionsTests.cs#L5) | `public void HttpClient_AllowAutoRedirect_Is_Always_False() {` |
| [test/RestSharp.Tests/RestClientTests.cs:6](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L6) | `public class RestClientTests {` |
| [test/RestSharp.Tests/RestClientTests.cs:18](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L18) | `public async Task Execute_with_RestRequest_and_Method_overrides_previous_request_method(Method reqMethod, Method overrideMethod) {` |
| [test/RestSharp.Tests/RestClientTests.cs:28](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L28) | `public async Task ConfigureHttp_will_set_proxy_to_null_with_no_exceptions_When_no_proxy_can_be_found() {` |
| [test/RestSharp.Tests/RestClientTests.cs:36](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L36) | `public void UseJson_leaves_only_json_serializer() {` |
| [test/RestSharp.Tests/RestClientTests.cs:49](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L49) | `public void UseXml_leaves_only_json_serializer() {` |
| [test/RestSharp.Tests/RestClientTests.cs:62](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L62) | `public void UseOnlySerializer_leaves_only_custom_serializer() {` |
| [test/RestSharp.Tests/RestClientTests.cs:75](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L75) | `public void Should_reuse_httpClient_instance() {` |
| [test/RestSharp.Tests/RestClientTests.cs:83](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L83) | `public void Should_use_new_httpClient_instance() {` |
| [test/RestSharp.Tests/RestClientTests.cs:91](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L91) | `public void ConfigureDefaultParameters_sets_user_agent_new_httpClient_instance() {` |
| [test/RestSharp.Tests/RestClientTests.cs:109](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L109) | `public void ConfigureDefaultParameters_sets_user_agent_given_httpClient_instance() {` |
| [test/RestSharp.Tests/RestClientTests.cs:128](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L128) | `public void Should_not_set_expect_continue_on_shared_http_client_default_headers() {` |
| [test/RestSharp.Tests/RestClientTests.cs:141](https://github.com/restsharp/RestSharp/blob/64ee12995b8d7409a5863da7b71cddfa526ffb7a/test/RestSharp.Tests/RestClientTests.cs#L141) | `public void Should_not_set_expect_continue_on_new_http_client_default_headers() {` |

Full lexical records (21) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Request model and URI construction | RestRequest; Parameter; ResourcePath |
| WP-02 | Transport and response lifecycle | RestClient; Response; ResponseBody |
| WP-03 | Serialization and multipart bodies | BodySerializer; MultipartPart; ContentType |
| WP-04 | Authentication redirects and cookies | Authenticator; RedirectPolicy; CookieJar |
| WP-05 | Interceptors adapters and compatibility | RequestInterceptor; ClientOptions; RestCompatibilityCase |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
