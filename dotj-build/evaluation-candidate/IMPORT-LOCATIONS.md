# Internal acyclic import source locations v1

This bounded extension compares selected fields on the existing five supported
acyclic inputs and five immutable source-format inputs. It grants no product,
task, F01/NF, public ABI, cycle-chain or complete-message acceptance.

The reference remains SDK 10.0.401 / MSBuild 18.9.11 / runtime 10.0.12, with
roll-forward disabled and the same Local/synchronous/private-cache Default load
profile. Historical analysis pin 6348d0c087aeec18c323b01a2c77da089ddafea0 differs
from implementation component b44cdcec4c79c50c67560876707d57d4f635fa3b; VMR eng
and global.json differ from standalone component build inputs. Source navigation
is not proof that a standalone source build reproduces installed SDK binaries.
The existing compiled lifecycle mapping remains unchanged and unqualified for a
public Java representation; metadata-locked inputs did not change.

The versioned owned CaptureImportLocationsV1.cs probe captures actual warning
File/LineNumber/ColumnNumber/EndLineNumber/EndColumnNumber and the same load's
public Imports metadata. All nine prior Default rows match the old capture on
every previously observed field, including full messages, failures, diagnostics
and cleanup. The only added fields are actual end coordinates. All original 27
observations across three profiles, their exact producers, locks and fixtures
remain intact. Raw capture logs and exact producer/plan snapshots remain under
the recorded private D: capture directory. The first resource-refused attempt is
also retained with its exact source snapshot; no process was launched for it.

The [plan](evidence/location-plan-v1.json) and fixture hashes preceded the RED
comparison and implementation. Every selected format was observed as supported:

| Input | Source-format coverage | Current warning | First import |
|---|---|---|---|
| BL01 | LF, indentation, multiline tags | main.proj 5:5 | main.proj 2:3 |
| BL02 | CRLF, tab, fake Import comment, supplementary Unicode on the same line | main.proj 3:14 | main.proj 2:49 |
| BL03 | fake Import in CDATA/scalar text, single quotes, explicit closing tag | main.proj 3:2 | main.proj 2:2 |
| BL04 | UTF8 BOM and XML declaration | main.proj 4:3 | main.proj 3:3 |
| BL05 | formatted diamond with distinct current/first owners, CRLF/LF | right.props 2:2 | left.props 3:4 |

Coordinates are one-based XML character positions at the opening `<`, counting
UTF-16 code units rather than UTF8 bytes or display width. XML CR/CRLF sequences
count as one newline; the BOM does not increment the column. All ten selected
duplicate notices report native endLine/endColumn = 0/0 (unavailable). The
candidate preserves those zeros; it does not invent a lexical tag-end span.

| Observable | Disposition |
|---|---|
| Ordered acyclic MSB4011, current owner/target | Exact match on ten native notices |
| Current warning line/column/endLine/endColumn | Exact actual native fields on all selected supported inputs |
| Previous owner/line/column | Same Default load's unique Imports metadata, cross-checked with previous context retained in the raw warning; exact candidate match |
| Previous end coordinates, ancestor chains | Unavailable from consumed public resolved-import metadata; no fields invented |
| Full native messages, root-parenthetical message context | Retained verbatim except identified fixture-root prefix; message equivalence unqualified |
| Cycles, missing-import coordinates and exceptions, other load flags | Retained native evidence and previous explicit dispositions; no new support claim |
| Public diagnostic/ElementLocation/Project/ProjectCollection facade | None; module has zero exports and opens |

The private locator decodes the exact bytes supplied to the secured DOM parser,
using its reported input encoding. It indexes actual start tags, skips comments,
CDATA and processing instructions, and respects quoted attribute delimiters.
Every tag must align by name and preorder with the semantic DOM; mismatches
refuse XML_SOURCE_INDEX. First-import sites are per-call state and are recorded
only after the condition and sandbox checks, before depth-first traversal.
Active cycles retain IMPORT_CYCLE_UNQUALIFIED. Existing file/import bounds,
DTD/unknown-syntax restrictions and no-task behavior remain unchanged.

The verifier reconstructs the bridge from locked native evidence, rejects
malformed coordinates and inconsistent previous context, and rejects a changed
current-coordinate bridge. Raw native messages, nulls, failures and cleanup are
not normalized away. Original 52 case IDs, payload bytes and dispositions remain
separately accounted for; the ten location cases are additional comparisons,
not product acceptance. Runtime dependencies remain JDK java.base/java.xml only.
.NET, reference packs and Roslyn are local development/reference tools only.

Next concrete work is a separately specified bounded cycle policy/chain contract
against the three retained load profiles. Full message equivalence, public
lifecycle/dependency representation and E01-E03/N01/NF gates remain open.
