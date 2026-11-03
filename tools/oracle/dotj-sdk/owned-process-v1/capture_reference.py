"""Common reference wire/evidence handling; native launch policy belongs to adapters.

Adapters implement run_capture(contract, fixtures, output). They use capture_row
with independently observed facts, and return their aggregate receipt. This
module never launches a subprocess or substitutes requested data for observations.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys


def require(condition, category="INVALID_EVIDENCE"):
    if not condition:
        raise ValueError(category)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def strict_json(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_KEY")
            value[key] = item
        return value

    def invalid(_):
        raise ValueError("NONFINITE_NUMBER")

    def finite(value):
        number = float(value)
        require(math.isfinite(number), "NONFINITE_NUMBER")
        return number
    result = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs, parse_constant=invalid, parse_float=finite)
    def strings(value):
        if isinstance(value, str):
            value.encode("utf-8", "strict")
        elif isinstance(value, dict):
            for key, item in value.items():
                strings(key)
                strings(item)
        elif isinstance(value, list):
            for item in value:
                strings(item)
    strings(result)
    return result


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=True, allow_nan=False, indent=2) + "\n").encode("utf-8")


def text(value):
    require(isinstance(value, str) and "\0" not in value)
    value.encode("utf-8", "strict")
    return value


def string_map(value):
    require(isinstance(value, dict))
    return {text(key): text(item) for key, item in value.items()}


def child_environment(wire, platform):
    require(platform in ("windows", "linux"))
    require(isinstance(wire, dict) and set(wire) == {"baseline", "set", "remove"})
    require(isinstance(wire["baseline"], dict) and set(wire["baseline"]) == {"values"})
    baseline, setting = string_map(wire["baseline"]["values"]), string_map(wire["set"])
    remove = wire["remove"]
    require(isinstance(remove, list))
    for name in list(baseline) + list(setting) + remove:
        require(bool(text(name)) and "=" not in name)
    result = {}
    # Native Windows ordinal-ignore-case differs from Unicode casefold. The
    # frozen name corpus is ASCII; reject ambiguous non-ASCII Windows names.
    if platform == "windows":
        require(all(name.isascii() for name in list(baseline) + list(setting) + remove), "WINDOWS_NAME_PROFILE")
    def erase(name):
        for old in list(result):
            if old == name or (platform == "windows" and old.upper() == name.upper()):
                del result[old]
    for key in sorted(baseline):
        erase(key)
        result[key] = baseline[key]
    for key in remove:
        erase(key)
    for key in sorted(setting):
        erase(key)
        result[key] = setting[key]
    return result


def payload(value):
    require(isinstance(value, dict) and set(value) == {"argv", "argvCodepoints", "argvUtf16Lengths"})
    argv = value["argv"]
    require(isinstance(argv, list) and len(argv) <= 256)
    require(isinstance(value["argvCodepoints"], list) and all(isinstance(row, list) and all(type(c) is int for c in row) for row in value["argvCodepoints"]))
    require(isinstance(value["argvUtf16Lengths"], list) and all(type(n) is int for n in value["argvUtf16Lengths"]))
    require(value["argvCodepoints"] == [[ord(c) for c in text(arg)] for arg in argv])
    require(value["argvUtf16Lengths"] == [len(arg.encode("utf-16-le")) // 2 for arg in argv])
    require(sum(value["argvUtf16Lengths"]) <= 32768)


def embedded(value):
    require(isinstance(value, dict) and set(value) == {"available", "base64", "bytes", "sha256"})
    if value["available"] is False:
        require(all(value[k] is None for k in ("base64", "bytes", "sha256")))
        return None
    require(value["available"] is True)
    raw = base64.b64decode(value["base64"], validate=True)
    require(type(value["bytes"]) is int and len(raw) <= 1048576 and value["bytes"] == len(raw) and value["sha256"] == sha256(raw))
    return raw


def verify_fixture(stdout, request, request_raw, exit_code):
    require(stdout.endswith(b"\n") and not stdout.startswith(b"\xef\xbb\xbf"))
    fixture = strict_json(stdout)
    require(fixture["schema"] == "dotj.owned-process.fixture-observation/1")
    require(fixture["rowId"] == request["rowId"] and fixture["mode"] == request["mode"])
    require(fixture["requestSha256"] == sha256(request_raw))
    actor = fixture["actor"]
    require(actor["kind"] == "reference-fixture" and type(actor["pid"]) is int and actor["pid"] > 0)
    payload(fixture["receivedPayload"])
    text(fixture["cwd"])
    string_map(fixture["environment"]["values"])
    require(string_map(fixture["parentEnvironmentBefore"]) == string_map(fixture["parentEnvironmentAfter"]))
    require(fixture["expectedOuterExitCode"] == exit_code and not fixture["errors"])
    ids = set()
    for op in fixture["apiOperations"]:
        require(op["id"] not in ids and op["parentActorPid"] == actor["pid"])
        ids.add(op["id"])
        require(set(op["streams"]) == {"stdout", "stderr"})
        for value in op["streams"].values():
            embedded(value)
        child = op["childObservation"]
        if child is not None:
            require(child["pid"] == op["childPid"] and child["pid"] != actor["pid"])
            payload(child["receivedPayload"])
            string_map(child["environment"]["values"])
        for field in ("invocation", "disposition", "exitCode", "handles", "workers", "timing"):
            require(field in op)
    for field in ("events", "apiOperations", "errors"):
        require(isinstance(fixture[field], list))
    return fixture


def verify_jdk(stdout, request, request_raw, exit_code):
    require(stdout.endswith(b"\n") and not stdout.startswith(b"\xef\xbb\xbf"))
    probe = strict_json(stdout)
    require(probe["schema"] == "dotj.owned-process.jdk-probe-observation/1")
    require(probe["rowId"] == request["rowId"] and probe["mode"] == request["mode"])
    require(probe["requestSha256"] == sha256(request_raw))
    require(probe["actor"]["kind"] == "jdk-probe" and type(probe["actor"]["pid"]) is int and probe["actor"]["pid"] > 0)
    payload(probe["receivedPayload"])
    string_map(probe["environment"]["values"])
    require(string_map(probe["parentEnvironmentBefore"]) == string_map(probe["parentEnvironmentAfter"]))
    require(probe["expectedOuterExitCode"] == exit_code and not probe["errors"])
    observed = probe["receivedPayload"]["argv"]
    differences = [{"index": i, "requested": request["argv"][i] if i < len(request["argv"]) else None,
                    "observed": observed[i] if i < len(observed) else None}
                   for i in range(max(len(request["argv"]), len(observed)))
                   if (request["argv"][i] if i < len(request["argv"]) else None) != (observed[i] if i < len(observed) else None)]
    require(probe["transportComparison"] == {"roundTrip": not differences, "differences": differences})
    require(isinstance(probe["operations"], list) and probe["operations"])
    ids = set()
    for operation in probe["operations"]:
        require(operation["id"] not in ids and operation["parentActorPid"] == probe["actor"]["pid"])
        ids.add(operation["id"])
        require(operation["childPid"] != probe["actor"]["pid"])
        require(operation["handles"]["terminal"] is True and operation["handles"]["observedExit"] is True)
        require(type(operation["exitCode"]) is int)
        require(operation["disposition"] in ("EXITED", "CANCELED"))
        for worker in operation["workers"].values():
            require(worker["terminal"] is True and worker["joined"] is True and worker["errorCategory"] is None)
        for stream in operation["streams"].values():
            require(embedded(stream) is not None)
        child = operation["childObservation"]
        if child is not None:
            require(child["pid"] == operation["childPid"])
            payload(child["receivedPayload"])
            string_map(child["environment"]["values"])
    return probe


def row_envelope(request_raw, result):
    strict_json(request_raw)
    digest = sha256(request_raw)
    require(result["requestSha256"] == digest)
    return {"schema": "dotj.owned-process.row-envelope/1", "requestBytesBase64": base64.b64encode(request_raw).decode("ascii"),
            "requestBytesLength": len(request_raw), "requestSha256": digest, "result": result}


def validate_request(request, contract):
    require(request.keys() >= contract["protocol"]["requestFields"].keys(), "REQUEST_FIELDS_MISSING")
    require(request["schema"] == "dotj.owned-process.request/1" and request["platform"] in ("windows", "linux"))
    require(request["engine"] in ("sdk-command", "dotnet-process-api", "jdk-probe", "packaged-product"))
    payload({key: request[key] for key in ("argv", "argvCodepoints", "argvUtf16Lengths")})
    child_environment(request["environment"], request["platform"])
    require(request["limits"] == contract["typedBounds"])
    require(type(request["deadlineMillis"]) is int and 0 < request["deadlineMillis"] <= contract["typedBounds"]["operationMillis"])
    require(Path(text(request["cwd"])).is_absolute())
    executable = request["executable"]
    require(Path(text(executable["path"])).is_absolute())
    require(isinstance(executable["sha256"], str) and len(executable["sha256"]) == 64 and all(c in "0123456789abcdef" for c in executable["sha256"]))
    stdin = request["stdin"]
    data = base64.b64decode(stdin["base64"], validate=True)
    require(type(stdin["length"]) is int and stdin["length"] == len(data) <= contract["typedBounds"]["stdinBytes"])
    require(stdin["sha256"] == sha256(data))
    require(isinstance(request["inputs"], list) and request["inputs"])
    require(set(request["effectsRoots"]) == {"source", "priorSDK", "siblings", "staging"})
    require(all(Path(text(value)).is_absolute() for value in request["effectsRoots"].values()))
    string_map(request["secrets"])


def descriptor(path, root):
    raw = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "bytes": len(raw), "sha256": sha256(raw)}


def verify_descriptor(value, root):
    require(isinstance(value, dict) and set(value) >= {"path", "bytes", "sha256"})
    require(type(value["bytes"]) is int and value["bytes"] >= 0)
    relative = Path(value["path"])
    require(not relative.is_absolute() and ".." not in relative.parts)
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()) and not path.is_symlink() and not path.is_junction())
    require(all(value[key] == item for key, item in descriptor(path, root).items()))
    return path


def inventory(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "EFFECT_ROOT_INVALID")
    result = {}
    for path in sorted(root.rglob("*")):
        require(not path.is_symlink() and not path.is_junction(), "REPARSE_EFFECT")
        key = path.relative_to(root).as_posix()
        if path.is_dir():
            result[key] = {"type": "directory", "bytes": 0, "sha256": None}
        else:
            raw = path.read_bytes()
            result[key] = {"type": "file", "bytes": len(raw), "sha256": sha256(raw)}
    return result


def validate_row_files(output, request_raw, facts, effects, contract):
    """Seal observations supplied by a platform adapter after real cleanup.

    The adapter writes raw stdout.bin/stderr.bin first and supplies every final
    result field. No missing lifecycle/guard/network facts receive defaults.
    """
    output = Path(output)
    request = strict_json(request_raw)
    validate_request(request, contract)
    require(facts.keys() >= contract["protocol"]["resultFields"].keys())
    require(facts["schema"] == "dotj.owned-process.observation/1")
    require(facts["rowId"] == request["rowId"] and facts["engine"] == request["engine"])
    require(effects["rowId"] == request["rowId"] and effects["requestSha256"] == sha256(request_raw))
    require(set(effects["before"]) == set(effects["after"]) == {"source", "priorSDK", "siblings", "staging"})
    require(facts["parentEnvironmentBefore"] == facts["parentEnvironmentAfter"])
    string_map(facts["parentEnvironmentBefore"])
    if request["engine"] in ("sdk-command", "dotnet-process-api"):
        fixture = verify_fixture((output / "stdout.bin").read_bytes(), request, request_raw, facts["exitCode"])
        require(facts["fixtureObservation"] == fixture)
        require(facts["argvCodepoints"] == fixture["receivedPayload"]["argvCodepoints"])
        require(facts["argvUtf16Lengths"] == fixture["receivedPayload"]["argvUtf16Lengths"])
        require(facts["observationActors"] == {"outerProcess": "driver-owned-outer", "parentEnvironment": "driver",
                                               "payload": "reference-fixture", "apiOperations": "reference-fixture-child-operations"})
    elif request["engine"] == "jdk-probe":
        probe = verify_jdk((output / "stdout.bin").read_bytes(), request, request_raw, facts["exitCode"])
        require(facts["jdkProbeObservation"] == probe and facts["fixtureObservation"] is None)
        require(facts["argvCodepoints"] == probe["receivedPayload"]["argvCodepoints"])
        require(facts["argvUtf16Lengths"] == probe["receivedPayload"]["argvUtf16Lengths"])
        require(facts["observationActors"] == {"outerProcess": "driver-owned-outer", "parentEnvironment": "driver",
                                               "payload": "jdk-probe", "apiOperations": "jdk-probe-child-operations"})
        for artifact in probe["telemetry"]:
            # Adapter stages telemetry alongside this row, retaining exact bytes.
            verify_descriptor(artifact, output)
    for channel in ("stdout", "stderr"):
        desc = descriptor(output / (channel + ".bin"), output)
        require(all(facts["streams"][channel][key] == value for key, value in desc.items()))
        require(desc["bytes"] <= contract["typedBounds"][channel + "Bytes"])
        require(facts["streams"][channel]["truncated"] is False)
    guard = facts["outerGuard"]
    complete = facts["status"] == "CAPTURE_COMPLETE"
    if complete:
        require(guard["actions"] == [] and guard["observedTerminal"] is True)
        require(facts["disposition"] not in ("TIMED_OUT", "IO_FAILED", "CLEANUP_FAILED", "CAPTURE_FAILED"))
        require(facts["handles"]["terminal"] is True)
        require(all(w["terminal"] is True and w["joined"] is True for w in facts["workers"].values()))
    effect_bytes = json_bytes(effects)
    require(facts["effects"] == {"path": "effects.json", "bytes": len(effect_bytes), "sha256": sha256(effect_bytes)})


def capture_row(output, request_raw, facts, effects, contract):
    output = Path(output)
    validate_row_files(output, request_raw, facts, effects, contract)
    (output / "effects.json").write_bytes(json_bytes(effects))
    (output / "request.json").write_bytes(json_bytes(row_envelope(request_raw, facts)))
    return descriptor(output / "request.json", output)


def checked_output(path):
    require(path.is_absolute() and path.drive.upper() == "D:", "OUTPUT_NOT_ASSIGNED_D_PATH")
    scratch = Path("D:/AI/Implementation/dotj Frameworks/agents")
    require(path.is_relative_to(scratch), "OUTPUT_NOT_TASK_SCRATCH")
    relative = path.relative_to(scratch)
    require(len(relative.parts) >= 2 and relative.parts[0].startswith("task"), "OUTPUT_NOT_ASSIGNED_CHILD")
    require(not path.exists(), "OUTPUT_EXISTS")
    for parent in path.parents:
        require(not parent.is_symlink() and not parent.is_junction(), "OUTPUT_REPARSE")
    return path


def controlled_snapshot():
    allowed = {"SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "JAVA_HOME", "TEMP", "TMP", "USERPROFILE", "HOME",
               "LANG", "LC_ALL", "PYTHONDONTWRITEBYTECODE", "PYTHONUTF8", "DOTNET_ROOT", "DOTNET_CLI_HOME",
               "DOTNET_CLI_TELEMETRY_OPTOUT", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE", "DOTNET_NOLOGO",
               "DOTNET_MULTILEVEL_LOOKUP", "NUGET_PACKAGES", "NUGET_HTTP_CACHE_PATH", "DOTJ_FIXTURE_REMOVE",
               "DOTJ_SECRET_ENV", "DOTJ_FIXTURE_SET", "DOTJ_CASE"}
    require(all(name.upper() in allowed for name in os.environ), "CALLER_ENVIRONMENT_NOT_CONTROLLED")
    return dict(os.environ)  # only after complete allowlist validation


def validate_receipt(receipt, output, platform, contract, fixtures, parent_before):
    require(receipt["status"] == "CAPTURE_COMPLETE" and receipt["platform"] == platform)
    rows = {r["id"]: r for r in fixtures["referenceRows"] if r["platform"] == platform}
    groups = {r["id"]: r for r in fixtures["boundaryGroups"] if r["platform"] == platform}
    require(set(receipt["referenceRows"]) == set(rows), "REFERENCE_ROWS_INCOMPLETE")
    require(set(receipt["boundaryGroups"]) == set(groups), "BOUNDARY_GROUPS_INCOMPLETE")
    for name in ("contract", "fixtures", "sourceMap"):
        verify_descriptor(receipt["inputs"][name], output)
    for row_id, desc in receipt["referenceRows"].items():
        path = verify_descriptor(desc, output)
        require(desc["path"] == rows[row_id]["files"][0])
        envelope = strict_json(path.read_bytes())
        require(envelope["schema"] == "dotj.owned-process.row-envelope/1")
        raw = base64.b64decode(envelope["requestBytesBase64"], validate=True)
        require(envelope["requestBytesLength"] == len(raw) and envelope["requestSha256"] == sha256(raw))
        result = envelope["result"]
        require(row_envelope(raw, result) == envelope)
        request = strict_json(raw)
        require(request["secrets"] == fixtures["corpus"]["syntheticSecrets"])
        require(request["rowId"] == row_id and request["engine"] == rows[row_id]["engine"])
        require(result["status"] == "CAPTURE_COMPLETE" and result["parentEnvironmentBefore"] == parent_before)
        effects_path = verify_descriptor(result["effects"], path.parent)
        # Revalidate sealed rows through the same evidence checks without writes.
        validate_row_files(path.parent, raw, result, strict_json(effects_path.read_bytes()), contract)
    for group_id, desc in receipt["boundaryGroups"].items():
        path = verify_descriptor(desc, output)
        require(desc["path"] == groups[group_id]["files"][1])
        group = strict_json(path.read_bytes())
        require(group["status"] == "CAPTURE_COMPLETE" and group["rowId"] == group_id)
        require([strict_json(base64.b64decode(e["requestBytesBase64"], validate=True))["mode"] for e in group["modes"]] == groups[group_id]["modes"])
        for envelope in group["modes"]:
            raw = base64.b64decode(envelope["requestBytesBase64"], validate=True)
            require(row_envelope(raw, envelope["result"]) == envelope and envelope["requestBytesLength"] == len(raw))
            result = envelope["result"]
            request = strict_json(raw)
            validate_request(request, contract)
            require(request["secrets"] == fixtures["corpus"]["syntheticSecrets"])
            require(result.keys() >= contract["protocol"]["resultFields"].keys())
            require(result["status"] == "CAPTURE_COMPLETE" and result["rowId"] == request["rowId"] == group_id)
            require(result["parentEnvironmentBefore"] == result["parentEnvironmentAfter"] == parent_before)
            require(result["outerGuard"]["actions"] == [] and result["outerGuard"]["observedTerminal"] is True)
            require(result["handles"]["terminal"] is True)
            require(all(w["terminal"] is True and w["joined"] is True for w in result["workers"].values()))
            require(result["disposition"] not in ("TIMED_OUT", "IO_FAILED", "CLEANUP_FAILED", "CAPTURE_FAILED"))
            streams = {}
            for name in ("stdout", "stderr"):
                stream = result["streams"][name]
                require(stream["path"] == name + ".bin" and type(stream["offset"]) is int and stream["offset"] >= 0)
                whole = (path.parent / stream["path"]).read_bytes()
                require(type(stream["bytes"]) is int and 0 <= stream["bytes"] <= contract["typedBounds"][name + "Bytes"])
                require(stream["offset"] + stream["bytes"] <= len(whole) and stream["truncated"] is False)
                streams[name] = whole[stream["offset"]:stream["offset"] + stream["bytes"]]
                require(sha256(streams[name]) == stream["sha256"])
            if request["engine"] == "jdk-probe":
                probe = verify_jdk(streams["stdout"], request, raw, result["exitCode"])
                require(result["jdkProbeObservation"] == probe and result["fixtureObservation"] is None)
                require(result["argvCodepoints"] == probe["receivedPayload"]["argvCodepoints"])
                require(result["argvUtf16Lengths"] == probe["receivedPayload"]["argvUtf16Lengths"])
                require(result["observationActors"] == {"outerProcess": "driver-owned-outer", "parentEnvironment": "driver",
                                                        "payload": "jdk-probe", "apiOperations": "jdk-probe-child-operations"})
                for artifact in probe["telemetry"]:
                    verify_descriptor(artifact, path.parent)
            effects_path = verify_descriptor(result["effects"], path.parent)
            effect = strict_json(effects_path.read_bytes())["modes"][request["mode"]]
            require(effect["rowId"] == group_id and effect["requestSha256"] == sha256(raw))
            require(set(effect["before"]) == set(effect["after"]) == {"source", "priorSDK", "siblings", "staging"})
        for relative in groups[group_id]["files"]:
            require((output / relative).is_file())
    for relative in fixtures["expectedInventories"]["referenceAggregates"]:
        if relative.endswith("observations-" + ("linux" if platform == "windows" else "windows") + ".json"):
            continue  # the opposite platform is joined only at OP02C checkpoint
        require((output / relative).is_file(), "REFERENCE_AGGREGATE_MISSING")


def main(argv=None):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--platform", required=True, choices=("windows", "linux"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        require(args.contract.is_absolute(), "CONTRACT_NOT_ABSOLUTE")
        output = checked_output(args.output)
        contract = strict_json(args.contract.read_bytes())
        fixtures_path = args.contract.with_name("fixtures.json")
        sources_path = args.contract.with_name("source-map.json")
        fixtures = strict_json(fixtures_path.read_bytes())
        sources = strict_json(sources_path.read_bytes())
        require(contract["schema"] == "dotj.owned-process.contract")
        require(fixtures["schema"] == "dotj.owned-process.fixtures" and sources["schema"] == "dotj.owned-process.source-map")
        for name, source in (("fixtures.json", fixtures_path), ("source-map.json", sources_path)):
            binding = contract["inventoryBindings"][name]
            raw = source.read_bytes()
            require(binding["bytes"] == len(raw) and binding["sha256"] == sha256(raw), "CONTRACT_INPUT_BINDING")
        output.mkdir(parents=True)
        (output / "inputs").mkdir()
        for name, source in (("contract.json", args.contract), ("fixtures.json", fixtures_path), ("source-map.json", sources_path)):
            (output / "inputs" / name).write_bytes(source.read_bytes())
        parent_before = controlled_snapshot()
        adapter_path = Path(__file__).with_name("capture_" + args.platform + ".py")
        require(adapter_path.is_file(), "PLATFORM_ADAPTER_UNAVAILABLE")
        spec = importlib.util.spec_from_file_location("owned_process_capture_adapter", adapter_path)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        receipt = adapter.run_capture(contract, fixtures, output)
        require(controlled_snapshot() == parent_before, "CALLER_ENVIRONMENT_CHANGED")
        validate_receipt(receipt, output, args.platform, contract, fixtures, parent_before)
        for name, filename in (("contract", "contract.json"), ("fixtures", "fixtures.json"), ("sourceMap", "source-map.json")):
            require(receipt["inputs"][name] == descriptor(output / "inputs" / filename, output))
        (output / "capture-receipt.json").write_bytes(json_bytes(receipt))
        return 0
    except Exception as error:
        # Categorical only: exception text may contain paths/requested secrets.
        if "output" in locals() and output.exists():
            (output / "capture-failure.json").write_bytes(json_bytes({"status": "CAPTURE_FAILED", "category": type(error).__name__}))
        print("CAPTURE_FAILED", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
