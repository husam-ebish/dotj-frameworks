"""Derive a selected exact-name candidate ledger from the installed CoreLib snapshots."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SHAPES = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-api-shapes-v10.0.12"
OUTPUT = ROOT / "planning/stage-2/repos/dotj-core/evidence/wp02-n01-candidate-v10.0.12.json"
KEYS = (
    "cancellation-token", "cancellation-source", "cancellation-registration",
    "task", "task-generic", "task-completion-source", "task-completion-source-generic",
)


def build():
    symbols = []
    for key in KEYS:
        snapshot = json.loads((SHAPES / f"{key}.json").read_text(encoding="utf-8"))
        t = snapshot["type"]
        namespace, _, type_name = t["fullName"].rpartition(".")
        symbols.append({
            "upstreamType": t["fullName"],
            "javaPackageCandidate": namespace,
            "javaSimpleNameCandidate": type_name.replace("`1", ""),
            "genericArity": len(t["genericParameters"]),
            "valueType": t["isValueType"],
            "selectedDeclaredPublicMethods": [method["Name"] for method in t["methods"]],
            "status": "CANDIDATE_ONLY; no product declaration qualified",
        })
    assert len({item["upstreamType"] for item in symbols}) == 7
    assert {item["javaSimpleNameCandidate"] for item in symbols} == {"CancellationToken", "CancellationTokenSource", "CancellationTokenRegistration", "Task", "TaskCompletionSource"}
    ledger = {
        "schemaVersion": 1,
        "runtimeVersion": "10.0.12",
        "selectedSymbols": symbols,
        "javaLanguageGaps": [
            "CancellationToken and CancellationTokenRegistration are CLR value types; Java class/reference representation must preserve observed value and identity behavior.",
            "Generic and non-generic Task/TaskCompletionSource share a CLR base name; Java source declarations cannot differ only by generic arity in the same package.",
            "Inside Java package System, java.lang.System can shadow a fully qualified System.Threading reference; imports or a .j compiler mapping are needed.",
            "Task, ValueTask, cancellation exception and awaiter semantics remain unimplemented; CompletableFuture is not an exact public substitute.",
        ],
        "decision": "Keep experimental cancellation implementation under org.dotj.internal; public .j source and release qualification remain blocked by E01/E02/E03/N01 gates.",
    }
    OUTPUT.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return symbols


if __name__ == "__main__":
    print(f"PASS {len(build())} selected exact-name WP-02 candidates")
