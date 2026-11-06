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
from pathlib import Path, PurePosixPath, PureWindowsPath
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


def observed_unicode_application_failure(probe):
    """Inventory may retain this exact terminal transport failure, unchanged."""
    operations = probe.get("operations")
    if (probe.get("mode") != "javac-unicode" or not isinstance(operations, list) or len(operations) != 2 or
            [op.get("id") for op in operations] != ["native-javac", "compiled-application"]):
        return False
    compile_op, app = operations
    if (compile_op.get("disposition") != "EXITED" or compile_op.get("exitCode") != 0 or
            app.get("disposition") != "IO_FAILED" or type(app.get("exitCode")) is not int or app["exitCode"] == 0 or
            app.get("childObservation") is not None):
        return False
    handles = fields(app.get("handles"), ("pid", "startIdentity", "retained", "terminal", "observedExit", "exitCode"))
    require(type(app.get("childPid")) is int and app["childPid"] > 0 and handles["pid"] == app["childPid"])
    nonempty(handles["startIdentity"])
    require(handles["retained"] is True and handles["terminal"] is True and handles["observedExit"] is True and
            handles["exitCode"] == app["exitCode"])
    require(set(app["workers"]) == {"stdin", "stdout", "stderr"})
    for worker in app["workers"].values():
        require(all(worker.get(k) is True for k in ("started", "closed", "terminal", "joined")) and
                worker.get("errorCategory") is None)
    timing = fields(app["timing"], ("startNanos", "endNanos", "deadlineNanos", "cleanupStartNanos"))
    require(all(type(timing[k]) is int for k in ("startNanos", "endNanos", "deadlineNanos", "cleanupStartNanos")))
    require(0 <= timing["startNanos"] <= timing["cleanupStartNanos"] <= timing["endNanos"] <= timing["deadlineNanos"])
    require(set(app["streams"]) == {"stdout", "stderr"})
    require(all(embedded(stream) is not None for stream in app["streams"].values()))
    return probe.get("errors") == [{"category":"IO_FAILED", "actorPid":probe["actor"]["pid"]}]


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
    transport_failure = observed_unicode_application_failure(probe)
    require(probe["expectedOuterExitCode"] == exit_code and (not probe["errors"] or transport_failure))
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
        require(operation["disposition"] in ("EXITED", "CANCELED") or
                (transport_failure and operation["id"] == "compiled-application" and operation["disposition"] == "IO_FAILED"))
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


def native_path(value, platform):
    """Validate child paths with the declared native OS, never the host OS.

    This is lexical validation only. Artifact containment still uses host Path
    resolution and checked_output; raw native observations are never rewritten.
    """
    value = text(value)
    require(platform in ("windows", "linux"), "NATIVE_PLATFORM_INVALID")
    if platform == "windows":
        path = PureWindowsPath(value)
        require(path.is_absolute() and bool(path.drive), "NATIVE_PATH_NOT_ABSOLUTE")
    else:
        path = PurePosixPath(value)
        require(path.is_absolute() and not value.startswith("//") and "\\" not in value,
                "NATIVE_PATH_NOT_ABSOLUTE")
    require(".." not in path.parts, "NATIVE_PATH_PARENT_TRAVERSAL")
    return path


def validate_request(request, contract):
    require(request.keys() >= contract["protocol"]["requestFields"].keys(), "REQUEST_FIELDS_MISSING")
    require(request["schema"] == "dotj.owned-process.request/1" and request["platform"] in ("windows", "linux"))
    require(request["engine"] in ("sdk-command", "dotnet-process-api", "jdk-probe", "packaged-product"))
    payload({key: request[key] for key in ("argv", "argvCodepoints", "argvUtf16Lengths")})
    child_environment(request["environment"], request["platform"])
    require(request["limits"] == contract["typedBounds"])
    require(type(request["deadlineMillis"]) is int and 0 < request["deadlineMillis"] <= contract["typedBounds"]["operationMillis"])
    native_path(request["cwd"], request["platform"])
    executable = request["executable"]
    native_path(executable["path"], request["platform"])
    require(isinstance(executable["sha256"], str) and len(executable["sha256"]) == 64 and all(c in "0123456789abcdef" for c in executable["sha256"]))
    stdin = request["stdin"]
    data = base64.b64decode(stdin["base64"], validate=True)
    require(type(stdin["length"]) is int and stdin["length"] == len(data) <= contract["typedBounds"]["stdinBytes"])
    require(stdin["sha256"] == sha256(data))
    require(isinstance(request["inputs"], list) and request["inputs"])
    require(set(request["effectsRoots"]) == {"source", "priorSDK", "siblings", "staging"})
    for value in request["effectsRoots"].values():
        native_path(value, request["platform"])
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


def fields(value, required):
    require(isinstance(value, dict) and value.keys() >= set(required), "MANDATORY_EVIDENCE_MISSING")
    return value


def nonempty(value):
    require(bool(text(value)), "EMPTY_EVIDENCE")


def digest_shape(value):
    require(isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value))


def network_shape(value):
    fields(value, ("isolation", "observation", "unqualifiedScope"))
    for item in value.values():
        nonempty(item)


def invocation_shape(value, platform):
    fields(value, ("executable", "argv", "cwd", "environment", "inputSha256"))
    native_path(value["executable"], platform)
    native_path(value["cwd"], platform)
    require(isinstance(value["argv"], list))
    for arg in value["argv"]:
        text(arg)
    child_environment(value["environment"], platform)
    digest_shape(value["inputSha256"])


def inventory_shape(value):
    require(isinstance(value, dict))
    for relative, entry in value.items():
        require(bool(text(relative)) and not Path(relative).is_absolute() and ".." not in Path(relative).parts)
        fields(entry, ("type", "bytes", "sha256"))
        require(entry["type"] in ("file", "directory") and type(entry["bytes"]) is int and entry["bytes"] >= 0)
        if entry["type"] == "file":
            digest_shape(entry["sha256"])
        else:
            require(entry["bytes"] == 0 and entry["sha256"] is None)


def optional_observation(value, required_fields):
    """Inapplicable evidence needs an explicit reason, never an absent/null fact."""
    require(isinstance(value, dict))
    if value.get("required") is False:
        nonempty(value.get("reason"))
        return False
    fields(value, required_fields)
    return True


def validate_effects(effects, request, request_raw, complete):
    fields(effects, ("schema", "rowId", "requestSha256", "before", "after", "delta", "publication",
                     "priorSdkSmoke", "sentinelProcess", "network", "cleanup"))
    require(effects["schema"] == "dotj.owned-process.effects/1" and effects["rowId"] == request["rowId"])
    require(effects["requestSha256"] == sha256(request_raw))
    for phase in ("before", "after"):
        require(isinstance(effects[phase], dict) and set(effects[phase]) == {"source", "priorSDK", "siblings", "staging"})
        for value in effects[phase].values():
            inventory_shape(value)
    fields(effects["delta"], ("added", "removed", "changed"))
    for value in effects["delta"].values():
        inventory_shape(value)
    publication = fields(effects["publication"], ("published", "successMarkers"))
    require(type(publication["published"]) is bool)
    inventory_shape(publication["successMarkers"])
    smoke = effects["priorSdkSmoke"]
    if optional_observation(smoke, ("invocation", "streams", "exitCode")):
        invocation_shape(smoke["invocation"], request["platform"])
        require(type(smoke["exitCode"]) is int and set(smoke["streams"]) == {"stdout", "stderr"})
        for stream in smoke["streams"].values():
            require(embedded(stream) is not None)
    sentinel = effects["sentinelProcess"]
    if optional_observation(sentinel, ("identity", "before", "after", "unaffected")):
        fields(sentinel["identity"], ("pid", "startIdentity"))
        require(type(sentinel["identity"]["pid"]) is int and sentinel["identity"]["pid"] > 0)
        nonempty(sentinel["identity"]["startIdentity"])
        require(type(sentinel["before"]) is bool and type(sentinel["after"]) is bool and type(sentinel["unaffected"]) is bool)
        if complete:
            require(sentinel["before"] and sentinel["after"] and sentinel["unaffected"])
    network_shape(effects["network"])
    cleanup = fields(effects["cleanup"], ("productActions", "outerGuardActions", "observedTerminal"))
    require(isinstance(cleanup["productActions"], list) and isinstance(cleanup["outerGuardActions"], list) and type(cleanup["observedTerminal"]) is bool)
    if complete:
        require(cleanup["observedTerminal"] and not cleanup["outerGuardActions"])


def sdk_boundary_request(request):
    return (request.get("engine") == "sdk-command" and
            request.get("mode") in ("sdk-parent-death", "sdk-signal") and
            request.get("platform") in ("windows", "linux") and
            request.get("rowId") == request["platform"] + "-telemetry-ownership")


def validate_sdk_boundary(value, request, request_raw):
    """Separately observed SDK boundary, with observer cleanup never credited.

    Only the explicitly mapped Windows/no-console signal case can be unavailable.
    This gate does not turn inventory completeness into a lifecycle guarantee.
    """
    fields(value, ("schema", "rowId", "mode", "requestSha256", "availability", "platform", "source",
                   "sdkParent", "targetChild", "action", "observerCleanup", "qualification"))
    require(value["schema"] == "dotj.owned-process.sdk-boundary/1")
    require(value["rowId"] == request["rowId"] and value["mode"] == request["mode"] and
            value["requestSha256"] == sha256(request_raw), "SDK_BOUNDARY_BINDING")
    require(request["rowId"] == request["platform"] + "-telemetry-ownership" and
            request["mode"] in ("sdk-parent-death", "sdk-signal"))
    require(value["qualification"] == "UNQUALIFIED_STRONGER_LIFECYCLE_GUARANTEES")
    platform = fields(value["platform"], ("os", "arch", "profile"))
    require(platform["os"] == request["platform"] and platform["arch"] == "x64")
    source = fields(value["source"], ("path", "bytes", "sha256"))
    require(source["bytes"] == 8073 and source["sha256"] == "d56a0685399da7c0c8082e7a52d3ed70895b5e915fe287d8ef8673f40453706f")
    nonempty(source["path"])
    availability = fields(value["availability"], ("state", "reason"))
    nonempty(availability["reason"])
    if availability["state"] == "NOT_APPLICABLE":
        require(request["platform"] == "windows" and request["mode"] == "sdk-signal" and
                platform["profile"] == "CREATE_NO_WINDOW", "SDK_BOUNDARY_UNAVAILABLE_NOT_ALLOWED")
        fields(platform, ("nativeVersion", "creationFlags"))
        nonempty(platform["nativeVersion"])
        require(platform["creationFlags"] == 0x08000004)
        require(all(value[k] is None for k in ("sdkParent", "targetChild", "action", "observerCleanup")),
                "SDK_BOUNDARY_UNOBSERVED_LIFECYCLE")
        return False
    require(availability["state"] == "MEASURED")
    def identity(item):
        fields(item, ("pid", "startIdentity"))
        require(type(item["pid"]) is int and item["pid"] > 0)
        nonempty(item["startIdentity"])
    def terminal(item, final=False):
        fields(item, ("observedTerminal", "exitCode", "method", "observedNanos"))
        require(type(item["observedTerminal"]) is bool and type(item["observedNanos"]) is int and item["observedNanos"] >= 0)
        require(item["exitCode"] is None or type(item["exitCode"]) is int)
        require(item["observedTerminal"] or item["exitCode"] is None)
        require(not final or item["observedTerminal"])
        nonempty(item["method"])
    parent = fields(value["sdkParent"], ("identity", "invocation", "terminal"))
    child = fields(value["targetChild"], ("identity", "ready", "beforeObserverCleanup", "afterObserverCleanup"))
    identity(parent["identity"]); identity(child["identity"])
    require(parent["identity"]["pid"] != child["identity"]["pid"])
    invocation_shape(parent["invocation"], request["platform"])
    require(parent["invocation"]["inputSha256"] == sha256(request_raw))
    terminal(parent["terminal"], True)
    fields(child["ready"], ("pid", "receivedPayload"))
    require(child["ready"]["pid"] == child["identity"]["pid"])
    payload(child["ready"]["receivedPayload"])
    terminal(child["beforeObserverCleanup"])
    terminal(child["afterObserverCleanup"], True)
    action = fields(value["action"], ("kind", "identity", "requestedNanos", "completedNanos", "succeeded"))
    require(action["identity"] == parent["identity"] and action["succeeded"] is True)
    require(action["kind"] == ("TerminateProcess" if request["platform"] == "windows" else
                               "SIGTERM" if request["mode"] == "sdk-signal" else "SIGKILL"))
    require(type(action["requestedNanos"]) is int and type(action["completedNanos"]) is int and
            0 <= action["requestedNanos"] <= action["completedNanos"] <= child["beforeObserverCleanup"]["observedNanos"])
    cleanup = fields(value["observerCleanup"], ("actions", "terminalObserved", "workersJoined"))
    require(isinstance(cleanup["actions"], list) and cleanup["terminalObserved"] is True and cleanup["workersJoined"] is True)
    for item in cleanup["actions"]:
        fields(item, ("kind", "identity", "requestedNanos", "completedNanos", "succeeded"))
        require(item["identity"] == child["identity"] and item["succeeded"] is True)
        require(item["kind"] in ("TerminateProcess", "SIGTERM", "SIGKILL"))
        require(child["beforeObserverCleanup"]["observedNanos"] <= item["requestedNanos"] <= item["completedNanos"] <=
                child["afterObserverCleanup"]["observedNanos"])
    require(bool(cleanup["actions"]) or child["beforeObserverCleanup"]["observedTerminal"])
    target_streams = fields(value.get("targetStreams"), ("stdout", "stderr"))
    raw_ready = embedded(target_streams["stdout"])
    require(raw_ready is not None and embedded(target_streams["stderr"]) is not None)
    require(strict_json(raw_ready.split(b"\n", 1)[0]) == child["ready"], "SDK_TARGET_READY_RAW_MISMATCH")
    if request["platform"] == "linux":
        native = fields(value.get("nativeReceipt"), ("schema", "rowId", "mode", "requestSha256", "sdkPid", "sdkStart",
                        "childPid", "childStart", "sdkExit", "parentEndNanos", "actionStartNanos", "actionEndNanos",
                        "cleanupPerformed", "cleanupStartNanos", "cleanupEndNanos", "ready", "before", "after",
                        "invocation", "clockDomain", "drainers"))
        require(native["schema"] == "dotj.owned-process.sdk-boundary-native/1" and
                all(native[k] == value[k] for k in ("rowId", "mode", "requestSha256")))
        require(parent["identity"] == {"pid":native["sdkPid"],"startIdentity":"linux-proc-startticks:"+text(native["sdkStart"])})
        require(child["identity"] == {"pid":native["childPid"],"startIdentity":"linux-proc-startticks:"+text(native["childStart"])})
        require(parent["invocation"] == native["invocation"] and parent["terminal"]["exitCode"] == native["sdkExit"] and
                parent["terminal"]["observedNanos"] == native["parentEndNanos"])
        require(child["ready"] == native["ready"] and child["beforeObserverCleanup"] == native["before"] and
                child["afterObserverCleanup"] == native["after"])
        require(action["requestedNanos"] == native["actionStartNanos"] and action["completedNanos"] == native["actionEndNanos"])
        require(type(native["cleanupPerformed"]) is bool and bool(cleanup["actions"]) == native["cleanupPerformed"])
        if cleanup["actions"]:
            require(len(cleanup["actions"]) == 1 and cleanup["actions"][0]["kind"] == "SIGTERM" and
                    cleanup["actions"][0]["requestedNanos"] == native["cleanupStartNanos"] and
                    cleanup["actions"][0]["completedNanos"] == native["cleanupEndNanos"])
        else:
            require(native["cleanupStartNanos"] is None and native["cleanupEndNanos"] is None)
        require(native["clockDomain"] == "Linux /proc/uptime monotonic nanoseconds")
        nonempty(native["drainers"])
    return True


def validate_result(facts, request, request_raw, contract):
    """Shared typed availability gate for ordinary rows and boundary modes."""
    fields(facts, contract["protocol"]["resultFields"])
    require(facts["schema"] == "dotj.owned-process.observation/1" and facts["rowId"] == request["rowId"] and facts["engine"] == request["engine"])
    require(facts["requestSha256"] == sha256(request_raw))
    boundary = sdk_boundary_request(request)
    measured_boundary = validate_sdk_boundary(facts.get("sdkBoundaryObservation"), request, request_raw) if boundary else None
    if boundary and not measured_boundary:
        require(facts["status"] == "CAPTURE_COMPLETE" and facts["disposition"] == "NOT_APPLICABLE" and facts["launched"] is False)
        require(all(facts[k] is None for k in ("handles", "workers", "timing", "exitCode", "fixtureObservation", "jdkProbeObservation", "invocation")))
        require(facts["parentEnvironmentBefore"] == facts["parentEnvironmentAfter"])
        string_map(facts["parentEnvironmentBefore"])
        require(facts["argvCodepoints"] is None and facts["argvUtf16Lengths"] is None)
        require(facts["outerGuard"] == {"used":False,"actions":[],"observedTerminal":None})
        require(facts["container"] is None and facts["platform"]["os"] == "windows")
        fields(facts["platform"], ("arch", "locale", "toolVersion"))
        for key in ("arch", "locale", "toolVersion"):
            nonempty(facts["platform"][key])
        diagnostics = fields(facts["diagnostics"], ("available", "base64", "bytes", "sha256", "redactionChecks"))
        raw_diagnostics = embedded({key:diagnostics[key] for key in ("available", "base64", "bytes", "sha256")})
        require(raw_diagnostics is not None and len(raw_diagnostics) <= contract["typedBounds"]["diagnosticBytes"])
        require(isinstance(diagnostics["redactionChecks"], dict) and diagnostics["redactionChecks"] and
                all(item is True for item in diagnostics["redactionChecks"].values()))
        fields(facts["observationActors"], ("outerProcess", "parentEnvironment", "payload", "apiOperations"))
        for actor in facts["observationActors"].values():
            nonempty(actor)
        network_shape(facts["network"])
        return True
    platform = fields(facts["platform"], ("os", "arch", "locale", "toolVersion"))
    require(platform["os"] == request["platform"])
    for key in ("arch", "locale", "toolVersion"):
        nonempty(platform[key])
    invocation_shape(facts["invocation"], request["platform"])
    require(type(facts["launched"]) is bool)
    require(facts["status"] in ("CAPTURE_COMPLETE", "CAPTURE_FAILED"))
    complete = facts["status"] == "CAPTURE_COMPLETE"
    require(facts["disposition"] in ("EXITED", "START_FAILED", "CANCELED", "TIMED_OUT", "IO_FAILED", "CLEANUP_FAILED", "CAPTURE_FAILED"))
    handles = fields(facts["handles"], ("launchSlot", "pid", "startIdentity", "retained", "events", "observedExit", "exitCode", "terminal"))
    nonempty(handles["launchSlot"])
    require(all(type(handles[key]) is bool for key in ("retained", "observedExit", "terminal")))
    require(isinstance(handles["events"], list))
    for event in handles["events"]:
        fields(event, ("kind",))
        nonempty(event["kind"])
    if facts["launched"]:
        require(type(handles["pid"]) is int and handles["pid"] > 0 and handles["retained"])
        nonempty(handles["startIdentity"])
    else:
        require(handles["pid"] is None and handles["startIdentity"] is None and not handles["retained"] and not handles["observedExit"])
    if handles["observedExit"]:
        require(type(facts["exitCode"]) is int and type(handles["exitCode"]) is int and facts["exitCode"] == handles["exitCode"])
    else:
        require(facts["exitCode"] is None and handles["exitCode"] is None)
    require(isinstance(facts["workers"], dict) and set(facts["workers"]) == {"stdin", "stdout", "stderr"})
    for worker in facts["workers"].values():
        fields(worker, ("started", "closed", "terminal", "joined", "errorCategory"))
        require(all(type(worker[key]) is bool for key in ("started", "closed", "terminal", "joined")))
        require(worker["errorCategory"] is None or isinstance(worker["errorCategory"], str))
        if complete:
            require(worker["closed"] and worker["terminal"] and (worker["joined"] or not worker["started"]) and worker["errorCategory"] is None)
    timing = fields(facts["timing"], ("startNanos", "endNanos", "deadlineNanos", "cleanupStartNanos"))
    require(all(type(timing[key]) is int and timing[key] >= 0 for key in timing))
    require(timing["startNanos"] <= timing["cleanupStartNanos"] <= timing["endNanos"])
    diagnostics = fields(facts["diagnostics"], ("available", "base64", "bytes", "sha256", "redactionChecks"))
    diagnostic_bytes = embedded({key: diagnostics[key] for key in ("available", "base64", "bytes", "sha256")})
    require(diagnostic_bytes is not None and len(diagnostic_bytes) <= contract["typedBounds"]["diagnosticBytes"])
    require(isinstance(diagnostics["redactionChecks"], dict) and diagnostics["redactionChecks"] and all(type(v) is bool for v in diagnostics["redactionChecks"].values()))
    network_shape(facts["network"])
    if request["platform"] == "windows":
        require(facts["container"] is None)
    else:
        container = fields(facts["container"], ("identity", "caps", "exitCode", "removed"))
        nonempty(container["identity"])
        require(isinstance(container["caps"], dict) and container["caps"] and type(container["exitCode"]) is int and type(container["removed"]) is bool)
        if complete:
            require(container["removed"])
    require(facts["fixtureObservation"] is None if boundary or request["engine"] not in ("sdk-command", "dotnet-process-api") else isinstance(facts["fixtureObservation"], dict))
    require(isinstance(facts["jdkProbeObservation"], dict) if request["engine"] == "jdk-probe" else facts["jdkProbeObservation"] is None)
    string_map(facts["parentEnvironmentBefore"])
    require(facts["parentEnvironmentBefore"] == facts["parentEnvironmentAfter"])
    fields(facts["observationActors"], ("outerProcess", "parentEnvironment", "payload", "apiOperations"))
    for actor in facts["observationActors"].values():
        nonempty(actor)
    fields(facts["streams"], ("stdout", "stderr"))
    fields(facts["effects"], ("path", "bytes", "sha256"))
    guard = fields(facts["outerGuard"], ("used", "actions", "observedTerminal"))
    require(type(guard["used"]) is bool and isinstance(guard["actions"], list) and type(guard["observedTerminal"]) is bool)
    if complete:
        require(not guard["actions"] and guard["observedTerminal"] and handles["terminal"])
        require(facts["disposition"] in ("EXITED", "CANCELED", "START_FAILED"))
        require(handles["observedExit"] if facts["launched"] else facts["disposition"] == "START_FAILED")
        require(timing["endNanos"] <= timing["deadlineNanos"] and all(diagnostics["redactionChecks"].values()))
    return complete


def validate_row_files(output, request_raw, facts, effects, contract):
    """Seal observations supplied by a platform adapter after real cleanup.

    The adapter writes raw stdout.bin/stderr.bin first and supplies every final
    result field. No missing lifecycle/guard/network facts receive defaults.
    """
    output = Path(output)
    request = strict_json(request_raw)
    validate_request(request, contract)
    complete = validate_result(facts, request, request_raw, contract)
    validate_effects(effects, request, request_raw, complete)
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
    require(".." not in path.parts, "OUTPUT_PARENT_TRAVERSAL")
    scratch = Path("D:/AI/Implementation/dotj Frameworks/agents")
    require(path.is_relative_to(scratch), "OUTPUT_NOT_TASK_SCRATCH")
    relative = path.relative_to(scratch)
    require(len(relative.parts) >= 2 and relative.parts[0].startswith("task"), "OUTPUT_NOT_ASSIGNED_CHILD")
    task_root = scratch / relative.parts[0]
    normalized = path.resolve()
    require(normalized.is_relative_to(task_root.resolve()) and task_root.resolve().is_relative_to(scratch.resolve()), "OUTPUT_RESOLVED_ESCAPE")
    require(not path.exists(), "OUTPUT_EXISTS")
    for parent in path.parents:
        require(not parent.is_symlink() and not parent.is_junction(), "OUTPUT_REPARSE")
    return normalized


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
            complete = validate_result(result, request, raw, contract)
            require(request["secrets"] == fixtures["corpus"]["syntheticSecrets"])
            require(result.keys() >= contract["protocol"]["resultFields"].keys())
            require(result["status"] == "CAPTURE_COMPLETE" and result["rowId"] == request["rowId"] == group_id)
            require(result["parentEnvironmentBefore"] == result["parentEnvironmentAfter"] == parent_before)
            unavailable_boundary = (sdk_boundary_request(request) and
                                    result["sdkBoundaryObservation"]["availability"]["state"] == "NOT_APPLICABLE")
            if not unavailable_boundary:
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
            elif sdk_boundary_request(request):
                boundary = result["sdkBoundaryObservation"]
                if unavailable_boundary:
                    require(streams == {"stdout":b"", "stderr":b""})
                else:
                    expected_raw = boundary["nativeReceipt"] if request["platform"] == "linux" else boundary
                    require(strict_json(streams["stdout"]) == expected_raw, "SDK_BOUNDARY_RAW_MISMATCH")
                    require(result["argvCodepoints"] == boundary["targetChild"]["ready"]["receivedPayload"]["argvCodepoints"])
                    require(result["argvUtf16Lengths"] == boundary["targetChild"]["ready"]["receivedPayload"]["argvUtf16Lengths"])
            effects_path = verify_descriptor(result["effects"], path.parent)
            effect = strict_json(effects_path.read_bytes())["modes"][request["mode"]]
            validate_effects(effect, request, raw, complete)
            require(effect["rowId"] == group_id and effect["requestSha256"] == sha256(raw))
            require(set(effect["before"]) == set(effect["after"]) == {"source", "priorSDK", "siblings", "staging"})
        for relative in groups[group_id]["files"]:
            require((output / relative).is_file())
    for relative in fixtures["expectedInventories"]["referenceAggregates"]:
        if relative.endswith("observations-" + ("linux" if platform == "windows" else "windows") + ".json"):
            continue  # the opposite platform is joined only at OP02C checkpoint
        require((output / relative).is_file(), "REFERENCE_AGGREGATE_MISSING")



# Fixed expectations, adopted from reviewed source/archive and historical build
# evidence. Installed-file hashes are observations, never their own expectations.
_CLOSURE_BASE = Path("D:/AI/Implementation/dotj Frameworks")
_REVIEWED_SOURCE_MAP_SHA = "d0b0535442c9de18f86c87df80677ef6da1db17bb22f70709ec78d3849f68050"
_ARCHIVE_CLOSURES = {'windows-sdk': {'path': 'D:\\AI\\Implementation\\dotj Frameworks\\agents\\task149-op02c-native-captures-v1\\fix-wave-r153-v1\\windows-sdk-archive-closure.json', 'bytes': 1168887, 'sha256': 'c7e3e4639375ccd3a7fe1bb23d0702987309e6a4e9d8548d09abab78e232ac0e'}, 'windows-jdk': {'path': 'D:\\AI\\Implementation\\dotj Frameworks\\agents\\task149-op02c-native-captures-v1\\fix-wave-r153-v1\\windows-jdk-archive-closure.json', 'bytes': 73801, 'sha256': 'c155385a8acbb529a7f6e67b136851083b2b2bd3d70c1554e4af5325e6229a9f'}, 'linux-sdk': {'path': 'D:\\AI\\Implementation\\dotj Frameworks\\agents\\task149-op02c-native-captures-v1\\fix-wave-r153-v1\\linux-sdk-archive-closure.json', 'bytes': 1028880, 'sha256': '4a8c7f6d03dc841fa7af57fc509dd1a5ac5fb2c4c6c133d13369a39dd6dac7a5'}, 'linux-jdk': {'path': 'D:\\AI\\Implementation\\dotj Frameworks\\agents\\task149-op02c-native-captures-v1\\fix-wave-r153-v1\\linux-jdk-archive-closure.json', 'bytes': 68187, 'sha256': '806f7477dbdd9eca9742d21f421d3a1f15ca6b1ddeb07aa0faf38d69a71a1224'}}
_FIXTURE_GIT_SOURCES = [{'name': 'Program.cs', 'gitBlob': 'fb36d66cd9dd146585751218a57bc09b0c6143f5', 'reviewedGitBytes': 23791, 'normalizedSha256': '24613fb89cf3fe8a984eac24e81e0ac48e07c60b9a7adf8f487f07923a733483', 'physicalSha256': '24613fb89cf3fe8a984eac24e81e0ac48e07c60b9a7adf8f487f07923a733483'}, {'name': 'Reference.csproj', 'gitBlob': '6a314ff21a5333f0241db46bd6583dee311fe553', 'reviewedGitBytes': 792, 'normalizedSha256': '2883516c5295845c118cb9f6cf19fc6c37e07552e6301fe3102a5667b2e1f2f6', 'physicalSha256': '2883516c5295845c118cb9f6cf19fc6c37e07552e6301fe3102a5667b2e1f2f6'}, {'name': 'NuGet.Config', 'gitBlob': 'a3f3aea61c8f0a0b796eb417dc4ed9a056934afb', 'reviewedGitBytes': 125, 'normalizedSha256': '5256a7e3e07d2c5c94f7a1e6c45f39aab011c659c5e2d53e452dea525ce04575', 'physicalSha256': '5256a7e3e07d2c5c94f7a1e6c45f39aab011c659c5e2d53e452dea525ce04575'}]
_FIXTURE_ROOT = _CLOSURE_BASE/"agents/task142-op02a-reference-fixture-v1/green-v4"
_SOURCE_ROLE_PREFIX = "tools/oracle/dotj-sdk/owned-process-v1/"
_QUALIFIED_SOURCE_HASHES = {
    **{_SOURCE_ROLE_PREFIX+"reference/"+entry["name"]:entry["normalizedSha256"] for entry in _FIXTURE_GIT_SOURCES},
    _SOURCE_ROLE_PREFIX+"java/ProcessProbe.java":"f2d38106d57a58b6b73a3e88c1c1671c6376ad594047f6589097c122be5bf311",
    _SOURCE_ROLE_PREFIX+"java/ProbeChild.java":"95873b80ccec01ec4b93919ec50130e24e277190bc37b2729f8f02cb3d2cd5e0",
}


def qualified_source(relative, path=None):
    """Only these five reviewed source roles permit CRLF-to-LF conversion.

    No decoding, whitespace cleanup, bare-CR conversion or live hash adoption.
    Binary/config outputs continue through fixed_file with exact byte checks.
    """
    role = _SOURCE_ROLE_PREFIX+relative
    require(role in _QUALIFIED_SOURCE_HASHES, "UNQUALIFIED_SOURCE_ROLE")
    path = Path(path) if path is not None else Path(__file__).parent/relative
    require(path.is_file() and not path.is_symlink() and not path.is_junction(), "TRUSTED_SOURCE_MISSING_OR_REPARSE")
    physical = path.read_bytes()
    qualified = physical.replace(b"\r\n", b"\n")
    require(b"\r" not in qualified, "TRUSTED_SOURCE_BARE_CR")
    require(sha256(qualified) == _QUALIFIED_SOURCE_HASHES[role], "TRUSTED_SOURCE_DIGEST")
    return qualified, {"role":role, "path":str(path), "physicalBytes":len(physical),
                       "physicalSha256":sha256(physical), "qualifiedBytes":len(qualified),
                       "qualifiedSha256":_QUALIFIED_SOURCE_HASHES[role], "normalization":"CRLF-to-LF only"}


def qualified_probe_source_roles(bound):
    """Bind unique explicit repository suffixes, independent of checkout root."""
    expected = {role:value for role,value in _QUALIFIED_SOURCE_HASHES.items() if role.startswith(_SOURCE_ROLE_PREFIX+"java/")}
    require(type(bound) is dict and len(bound) == len(expected), "PROBE_SOURCE_ROLE_SET")
    resolved = {}
    for path, digest in bound.items():
        require(type(path) is str, "PROBE_SOURCE_ROLE_PATH")
        parts = PurePosixPath(path.replace("\\", "/")).parts
        matches = [role for role in expected if tuple(parts[-len(PurePosixPath(role).parts):]) == PurePosixPath(role).parts]
        require(len(matches) == 1 and ".." not in parts, "PROBE_SOURCE_ROLE_UNKNOWN")
        role = matches[0]
        require(role not in resolved, "PROBE_SOURCE_ROLE_AMBIGUOUS")
        require(digest == expected[role], "PROBE_SOURCE_RECEIPT_DIGEST")
        resolved[role] = digest
    require(resolved == expected, "PROBE_SOURCE_ROLE_SET")
    return resolved


def fixed_file(expected):
    path = Path(expected["path"])
    require(path.is_file() and not path.is_symlink() and not path.is_junction(), "TRUSTED_FILE_MISSING_OR_REPARSE")
    require(path.stat().st_size == expected["bytes"], "TRUSTED_FILE_SIZE")
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == expected["sha256"], "TRUSTED_FILE_DIGEST")
    return dict(expected)


def verify_closure_tree(root, expected, prefixes=None):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink() and not root.is_junction(), "CLOSURE_ROOT_INVALID")
    require(bool(expected), "CLOSURE_EMPTY")
    for relative, entry in expected.items():
        rel = PurePosixPath(relative)
        require(not rel.is_absolute() and ".." not in rel.parts and not PureWindowsPath(relative).drive, "CLOSURE_PATH_ESCAPE")
        path = root/relative
        require(path.resolve().is_relative_to(root.resolve()), "CLOSURE_RESOLVED_ESCAPE")
        for parent in [path, *path.parents]:
            if parent == root.parent:
                break
            require(not parent.is_symlink() and not parent.is_junction(), "CLOSURE_REPARSE")
        fixed_file(dict(entry, path=str(path)))
    actual = set()
    for base in ([root/prefix for prefix in prefixes] if prefixes else [root]):
        require(base.is_dir(), "CLOSURE_PREFIX_MISSING")
        for path in base.rglob("*"):
            require(not path.is_symlink() and not path.is_junction(), "CLOSURE_REPARSE")
            if path.is_file():
                actual.add(path.relative_to(root).as_posix())
    require(actual == set(expected), "CLOSURE_INVENTORY_MISMATCH")
    return {"root":str(root), "verifiedFiles":len(expected)}


def reviewed_source_map(path=None):
    path = Path(path) if path else Path(__file__).with_name("source-map.json")
    fixed_file({"path":str(path), "bytes":48716, "sha256":_REVIEWED_SOURCE_MAP_SHA})
    return strict_json(path.read_bytes())


def trusted_fixture_closure(root, staged=False):
    root = Path(root)
    require(staged or root.resolve() == _FIXTURE_ROOT.resolve(), "FIXTURE_ORIGIN_PATH")
    history = {"path":str(_CLOSURE_BASE/"agents/task149-op02c-native-captures-v1/artifact-manifest-v1.json"),
               "bytes":54537, "sha256":"0a08b3b265eb09fa39a662040d1a77de5726ae656584f43613fe00d04ad27eb2"}
    compile_receipt = {"path":str(_FIXTURE_ROOT/"receipt.json"), "bytes":166707,
                       "sha256":"d623a2fbd28c736e720aa0db640b73af79be6b005be4df6a745d14c56b6f067a"}
    report = {"path":str(_FIXTURE_ROOT.parent/"task142-implementation-report-v1.json"), "bytes":611431,
              "sha256":"ed6e0cd1abe40eb54398981c82e1ef019777423f8f1675e3e311a3a0a86fda30"}
    for pin in (history, compile_receipt, report):
        fixed_file(pin)
    adopted = strict_json(Path(history["path"]).read_bytes())
    original_copy = _CLOSURE_BASE/"agents/task149-op02c-native-captures-v1/windows-v4/fixture"
    files = {Path(v["path"]).relative_to(original_copy).as_posix():{k:v[k] for k in ("bytes", "sha256")}
             for v in adopted["artifacts"] if Path(v["path"]).is_relative_to(original_copy)}
    required = {"bin/Reference.dll", "bin/Reference.deps.json", "bin/Reference.runtimeconfig.json", "bin/Reference.pdb",
                "obj/project.assets.json", "obj/project.nuget.cache", "obj/Reference.csproj.nuget.g.props",
                "obj/Reference.csproj.nuget.g.targets", "obj/Debug/net10.0/Reference.dll"}
    require(len(files) == 25 and required <= files.keys(), "FIXTURE_OUTPUT_NOT_COVERED")
    build = strict_json(Path(compile_receipt["path"]).read_bytes())
    source_report = strict_json(Path(report["path"]).read_bytes())
    require(build["status"] == "PASS" and build["phase"] == "green-v4", "FIXTURE_BUILD_UNQUALIFIED")
    round = source_report["completionRounds"][-1]
    require(round["status"] == "PASS" and round["receipt"] == compile_receipt, "FIXTURE_COMPILE_BINDING")
    reviewed = reviewed_source_map()
    dotnet = next(x for x in reviewed["tools"] if x["id"] == "windows-nativeSdk-dotnet.exe")
    compile_tools = source_report["toolchain"]
    require(all(compile_tools["dotnet"][key] == dotnet[key] for key in ("bytes", "sha256")) and
            Path(compile_tools["dotnet"]["path"]).resolve() == Path(dotnet["path"]).resolve() and
            compile_tools["sdk"] == "10.0.401" and compile_tools["runtime"] == "10.0.12", "FIXTURE_COMPILE_SDK_PIN")
    offline = compile_tools["offlineClosure"]
    require(offline["sha256"] == "78a90a661ee4292dc275a1797c5a897b47f83d3879fce1ec2c7825e666cc3686", "FIXTURE_COMPILE_ARCHIVE_MANIFEST")
    fixed_file(offline)
    offline_archive = strict_json(Path(offline["path"]).read_bytes())
    sdk_archive = next(x for x in reviewed["toolArchives"] if Path(x["path"]).name == "dotnet-sdk-10.0.401.zip")
    require(offline_archive["archiveSha256"] == sdk_archive["sha256"] and
            Path(offline_archive["archive"]).resolve() == Path(sdk_archive["path"]).resolve(), "FIXTURE_COMPILE_ARCHIVE_PIN")
    for label in ("restore", "compile-build"):
        operation = next(x for x in build["operations"] if x["label"] == label)["process"]
        require(operation["exitCode"] == 0 and not any(operation.get(k) for k in
                ("error", "cleanupError", "timedOut", "outputLimitExceeded")), "FIXTURE_BUILD_FAILED")
        require(Path(operation["argv"][0]).resolve() == Path(dotnet["path"]).resolve() and
                str(_FIXTURE_ROOT/"source/Reference.csproj") in operation["argv"], "FIXTURE_COMPILE_TOOL_OR_SOURCE")
    checkout_sources = []
    for source in _FIXTURE_GIT_SOURCES:
        name = source["name"]
        pin = next(x for x in round["actualBuildSourceManifest"] if Path(x["path"]).name == name)
        require(pin["sha256"] == source["physicalSha256"] and files["source/"+name]["sha256"] == source["physicalSha256"], "FIXTURE_SOURCE_BINDING")
        fixed_file(pin)
        qualified, provenance = qualified_source("reference/"+name)
        require(len(qualified) == pin["bytes"] and provenance["qualifiedSha256"] == source["physicalSha256"], "FIXTURE_REVIEWED_GIT_SOURCE")
        checkout_sources.append(provenance)
    verified = verify_closure_tree(root, files, prefixes=("source", "bin", "obj"))
    runtime = strict_json((root/"bin/Reference.runtimeconfig.json").read_bytes())["runtimeOptions"]
    require(runtime["framework"]["version"] == "10.0.12" and runtime["rollForward"] == "Disable", "FIXTURE_RUNTIME_PIN")
    return {"schema":"dotj.owned-process.fixture-closure/1", **verified, "files":files,
            "sourceGitPins":_FIXTURE_GIT_SOURCES, "checkoutSources":checkout_sources, "origins":{"firstCheckpointCopyManifest":history,
             "qualifiedCompileReceipt":compile_receipt,"sourceBoundReport":report,"compileSdkClosure":offline},
            "trustAdoption":"ROOT R153 fix-wave adoption of retained first-checkpoint copy-output manifest linked to original controlled A142 build/source/SDK pins; no compile-time full-output hash manifest was recorded."}


def trusted_tool_closure(platform, selected=None, sources_path=None):
    require(platform in ("windows", "linux"))
    sources = reviewed_source_map(sources_path)
    ids = {"dotnet":platform+"-nativeSdk-"+("dotnet.exe" if platform=="windows" else "dotnet"),
           "java":platform+"-files-bin/java"+(".exe" if platform=="windows" else ""),
           "javac":platform+"-files-bin/javac"+(".exe" if platform=="windows" else "")}
    tools = {name:next(v for v in sources["tools"] if v["id"]==key) for name,key in ids.items()}
    if selected is not None:
        require(set(selected)==set(tools), "SELECTED_TOOL_SET")
        for name,path in selected.items():
            require(Path(path).resolve()==Path(tools[name]["path"]).resolve(), "SELECTED_TOOL_NOT_PINNED")
    distributions = {}
    for kind in ("sdk", "jdk"):
        pin = _ARCHIVE_CLOSURES[platform+"-"+kind]
        fixed_file(pin)
        manifest = strict_json(Path(pin["path"]).read_bytes())
        require(manifest["platform"]==platform and manifest["distribution"]==kind, "ARCHIVE_MANIFEST_PLATFORM")
        archive = next(x for x in sources["toolArchives"] if Path(x["path"]).resolve()==Path(manifest["archive"]["path"]).resolve())
        require(archive==manifest["archive"], "ARCHIVE_SOURCE_PIN")
        fixed_file(archive)
        root = Path(tools["dotnet"]["path"]).parent if kind=="sdk" else Path(tools["java"]["path"]).parent.parent
        require(root.resolve()==Path(manifest["root"]).resolve(), "DISTRIBUTION_ROOT_BINDING")
        for name in (["dotnet"] if kind=="sdk" else ["java", "javac"]):
            relative=Path(tools[name]["path"]).relative_to(root).as_posix()
            require(all(manifest["files"][relative][k]==tools[name][k] for k in ("bytes","sha256")), "ARCHIVE_ENTRY_TOOL_PIN")
        verified=verify_closure_tree(root, manifest["files"])
        distributions[kind]={**verified,"manifest":pin,"archive":archive}
    return {"schema":"dotj.owned-process.tool-closure/1", "platform":platform,
            "reviewedSourceMap":{"path":str(sources_path or Path(__file__).with_name("source-map.json")), "bytes":48716,"sha256":_REVIEWED_SOURCE_MAP_SHA},
            "distributions":distributions, "selectedTools":{k:{f:v[f] for f in ("path","bytes","sha256")} for k,v in tools.items()}}


def retain_verified_closure(output, tool_closure, fixture=None):
    output=Path(output);folder=output/"inputs/closures";folder.mkdir(parents=True,exist_ok=True)
    receipt={"toolClosure":tool_closure,"fixtureClosure":fixture}
    retained=[]
    for kind,value in tool_closure["distributions"].items():
        pin=value["manifest"];fixed_file(pin)
        path=folder/(tool_closure["platform"]+"-"+kind+".json");path.write_bytes(Path(pin["path"]).read_bytes())
        retained.append({"path":str(path),"bytes":pin["bytes"],"sha256":pin["sha256"]})
    if fixture is not None:
        path=folder/"windows-fixture.json";raw=json_bytes(fixture);path.write_bytes(raw)
        retained.append({"path":str(path),"bytes":len(raw),"sha256":sha256(raw)})
    path=folder/(tool_closure["platform"]+("-fixture-preflight.json" if fixture else "-tool-preflight.json"));raw=json_bytes(receipt);path.write_bytes(raw)
    retained.append({"path":str(path),"bytes":len(raw),"sha256":sha256(raw)})
    return retained


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
        parent_before = controlled_snapshot()
        adapter_path = Path(__file__).with_name("capture_" + args.platform + ".py")
        require(adapter_path.is_file(), "PLATFORM_ADAPTER_UNAVAILABLE")
        trusted_tool_closure(args.platform, sources_path=sources_path)
        if args.platform == "windows":
            trusted_fixture_closure(_FIXTURE_ROOT)
        spec = importlib.util.spec_from_file_location("owned_process_capture_adapter", adapter_path)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        if hasattr(adapter, "prepare_output"):
            adapter.prepare_output(output)
        (output / "inputs").mkdir()
        for name, source in (("contract.json", args.contract), ("fixtures.json", fixtures_path), ("source-map.json", sources_path)):
            (output / "inputs" / name).write_bytes(source.read_bytes())
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
