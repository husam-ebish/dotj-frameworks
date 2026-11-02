"""One fresh recovery attempt. Root owns the outer job; no automatic retry."""
import importlib.util
import shutil
import time
from pathlib import Path

s = importlib.util.spec_from_file_location('recovery_protocol', Path(__file__).with_name('protocol.py'))
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)

def update_process(record, value, save):
    record['process'] = value
    record['nativeExecutions'] = 1 if value.get('launched') is True else 0
    save()

def capture(out, execution_sha, review_pin, guard):
    """Guard dependency is explicit for in-process mock tests; CLI fixes its identity."""
    out = p.output_path(out, fresh=True)
    out.mkdir()
    resources = []
    record = dict(schemaVersion=2, status='FAILED_OR_DEFERRED', inputLockSha256=p.ORIGINAL_LOCK_SHA,
                  executionLockSha256=execution_sha, pythonRuntimeManifestSha256=p.PYTHON_SHA,
                  oldFailureSha256=p.FAILURE_SHA, tracePolicy=p.TRACE_POLICY, review=review_pin,
                  fixtureRoot=str(out / 'fixtures'), environment=p.environment(out), resourceSamples=resources,
                  process=None, raw={}, nativeExecutions=0, compilerExecutions=0, failure=None)
    def save():
        p.write(out / 'receipt.json', record)
    save()
    try:
        for name in ['tmp', 'home', 'cache']:
            (out / name).mkdir()
        shutil.copytree(p.ORIGINAL / 'fixtures', out / 'fixtures')
        p.fixtures(out)
        _, samples = guard.wait_resources(time.monotonic() + 160)
        resources.extend(samples)
        # Closure hashing is admission overhead, outside the native guard clock.
        p.verify_execution(execution_sha)
        p.review_authorization(review_pin['path'], review_pin['sha256'], execution_sha)
        def prelaunch():
            started = time.monotonic()
            sample = guard.memory()
            elapsed = time.monotonic() - started
            resources.append(dict(prelaunch=sample, durationSeconds=elapsed))
            p.require(elapsed <= 2 and guard.resource_ready(sample), 'fresh resource floor')
        def update(value):
            update_process(record, value, save)
        child = guard.run(p.native_argv(out), out, record['environment'], 'native', 30,
                          prelaunch=prelaunch, on_update=update)
        update_process(record, child, save)
        for stream in ['stdout', 'stderr']:
            record['raw'][stream] = p.descriptor(out / ('native.' + stream))
        p.old.process(child, p.native_argv(out), out, 'native', 30)
        p.host_trace(out / 'native.stderr')
        p.old.observation(p.read(out / 'native.stdout'))
        p.fixtures(out)
        p.verify_execution(execution_sha)
        p.review_authorization(review_pin['path'], review_pin['sha256'], execution_sha)
        record['status'] = 'CAPTURED_PENDING_ROOT_REVIEW'
    except BaseException as error:
        record['failure'] = {'type': type(error).__name__, 'message': str(error)}
        raise
    finally:
        for stream in ['stdout', 'stderr']:
            path = out / ('native.' + stream)
            if path.exists():
                record['raw'][stream] = p.descriptor(path)
        save()
    return record

def main():
    a = p.capture_parser().parse_args()
    p.require(a.root_reviewed_authorization is True and a.original_lock_sha256 == p.ORIGINAL_LOCK_SHA,
              'explicit root authorization/original lock')
    p.verify_execution(a.execution_lock_sha256)
    review = p.review_authorization(a.review, a.review_sha256, a.execution_lock_sha256)
    p.require(p.sha(p.old.GUARD) == p.old.GUARD_SHA, 'immutable guard changed')
    guard = p.load_fixed('boolean_v2_owned_guard', p.old.GUARD)
    capture(a.out, a.execution_lock_sha256, review, guard)
    print('CAPTURED_PENDING_ROOT_REVIEW nativeExecutions=1 compilerExecutions=0')

if __name__ == '__main__':
    main()
