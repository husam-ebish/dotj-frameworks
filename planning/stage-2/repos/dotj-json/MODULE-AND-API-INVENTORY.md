# DJ-023 .j JSON: module and API inventory

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

| Observed item | Count | Interpretation |
|---|---|---|
| Listed blob paths | 1176 | recursive complete |
| Project-definition paths | 4 | Files, not restored packages |
| API-definition/ref paths | 0 | Candidate declarations, not a complete public API census |
| Test/fixture candidate paths | 734 | Lexical path classification, not runnable test count |
| Sampled text files | 8 | Metadata plus selected API/implementation/tests |
| Lexical public/protected declarations | 78 | May include test helpers; not semantic API count |
| Lexical test-method candidates | 19 | Attribute inference only; no test discovery or execution |

## Extraction method and remaining closure

The tree supplies path identity. Project suffixes identify structural module candidates. Public/protected lines and test-like methods are extracted lexically from sampled files; multiline declarations, conditional compilation, generated code, extension methods, overload relationships and fixture parameter expansion require compiler-aware extraction. E02 must evaluate every target framework/configuration, generated source and conditional reference. Unassigned members remain retained scope, never implicitly removed.

## Observed project/module ledger

| Pinned path | Role candidate | Disposition |
|---|---|---|
| [Src/Newtonsoft.Json.FuzzTests/Newtonsoft.Json.FuzzTests.csproj](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.FuzzTests/Newtonsoft.Json.FuzzTests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Src/Newtonsoft.Json.TestConsole/Newtonsoft.Json.TestConsole.csproj](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.TestConsole/Newtonsoft.Json.TestConsole.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Src/Newtonsoft.Json.Tests/Newtonsoft.Json.Tests.csproj](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/Newtonsoft.Json.Tests.csproj) | test/verification | Retained; semantic assignment and conditional build closure in E02 |
| [Src/Newtonsoft.Json/Newtonsoft.Json.csproj](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json/Newtonsoft.Json.csproj) | product/source candidate | Retained; semantic assignment and conditional build closure in E02 |

## Sampled declaration candidates

| Source | Declaration candidate |
|---|---|
| [Src/Newtonsoft.Json/Required.cs:31](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json/Required.cs#L31) | `public enum Required` |
| [Src/Newtonsoft.Json/JsonToken.cs:35](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json/JsonToken.cs#L35) | `public enum JsonToken` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:56](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L56) | `public class DemoTests : TestFixtureBase` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:58](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L58) | `public class HtmlColor` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:60](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L60) | `public int Red { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:61](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L61) | `public int Green { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:62](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L62) | `public int Blue { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:66](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L66) | `public void JsonConverter()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:104](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L104) | `public class PersonDemo` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:106](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L106) | `public string Name { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:107](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L107) | `public int Age { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:108](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L108) | `public string Job { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:111](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L111) | `public class Session` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:113](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L113) | `public string Name { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:114](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L114) | `public DateTime Date { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:117](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L117) | `public class HtmlColorConverter : JsonConverter` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:119](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L119) | `public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:137](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L137) | `public override object ReadJson(JsonReader reader, Type objectType,` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:153](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L153) | `public override bool CanConvert(Type objectType)` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:160](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L160) | `public void SerializationGuide()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:196](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L196) | `public void SerializationBasics()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:223](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L223) | `public void SerializationBasics2()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:250](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L250) | `public void DeserializationBasics1()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:268](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L268) | `public void DeserializationBasics2()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:282](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L282) | `public class City` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:284](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L284) | `public string Name { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:285](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L285) | `public int Population { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:288](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L288) | `public class Employee` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:290](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L290) | `public string Name { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:293](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L293) | `public class Manager : Employee` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:295](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L295) | `public IList<Employee> Reportees { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:299](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L299) | `public void SerializeReferencesByValue()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:345](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L345) | `public void SerializeReferencesWithMetadata()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:408](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L408) | `public void RoundtripTypesAndReferences()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:450](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L450) | `public class House` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:452](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L452) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:453](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L453) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:454](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L454) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:455](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L455) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:458](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L458) | `public class House1` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:460](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L460) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:463](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L463) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:466](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L466) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:469](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L469) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:473](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L473) | `public class House3` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:476](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L476) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:478](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L478) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:479](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L479) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:480](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L480) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:484](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L484) | `public class House2` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:487](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L487) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:489](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L489) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:490](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L490) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:491](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L491) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:495](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L495) | `public class House4` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:498](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L498) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:500](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L500) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:501](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L501) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:504](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L504) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:508](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L508) | `public class House5` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:511](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L511) | `public string StreetAddress { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:513](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L513) | `public int Bedrooms { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:514](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L514) | `public decimal FloorArea { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:518](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L518) | `public DateTime BuildDate { get; set; }` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:522](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L522) | `public void SerializeAttributes()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:558](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L558) | `public void MergeJson()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:601](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L601) | `public void ArrayPooling()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:619](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L619) | `public void SerializeDataTable()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:661](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L661) | `public void JsonPathRegex()` |
| [Src/Newtonsoft.Json.Tests/DemoTests.cs:686](https://github.com/JamesNK/Newtonsoft.Json/blob/52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa/Src/Newtonsoft.Json.Tests/DemoTests.cs#L686) | `public async Task AsyncDemo()` |

Full lexical records (78) and complete listed paths are in [inventory.json](evidence/inventory.json). A display limit does not remove omitted records from scope.

## Capability ownership

| Package | Retained capability | Internal planning labels; public names come from source |
|---|---|---|
| WP-01 | Token reader and writer | JsonToken; JsonReader; JsonWriter |
| WP-02 | Object contracts and converters | JsonContract; TypeResolver; Converter |
| WP-03 | DOM and query operations | JToken; JObject; JArray; JsonPath |
| WP-04 | Reference identity dates and legacy behaviors | ReferenceResolver; DatePolicy; CompatibilityProfile |
| WP-05 | Schema of settings and compatibility corpus | SerializerSettings; JsonCompatibilityCase; StreamingBenchmark |


Map every observed source module/member onto one of these packages or a new explicitly retained package during E02. Structural listing is complete only to the scope stated above; behavioral analysis is sampled.
