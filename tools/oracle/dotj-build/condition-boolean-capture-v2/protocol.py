"""Versioned operational adapter. Imports immutable pure helpers, never launches."""
import argparse
import importlib.util
import re
from pathlib import Path

B = Path('D:/AI/Implementation/dotj Frameworks')
W = B / 'worktrees/dotj-build-boolean-conditions-v1'
HERE = W / 'tools/oracle/dotj-build/condition-boolean-capture-v2'
ORIGINAL = W / 'tools/oracle/dotj-build/condition-boolean-v1'
A2 = B / 'agents/batch2516-native-trace-recovery-v1'
O = B / 'orchestration/two-frameworks'
REVIEW = O / 'batch2516-native-trace-recovery-review.json'
ORIGINAL_LOCK_SHA = 'db304ea82a28915e85e1c695e154837a107ac770017369e815c93a7fed72c719'
PYTHON_SHA = 'f467dcc5b0c22a0a8f92e79d91e285a4f918fea82c66776428b0ed10f9a236a3'
FAILURE_SHA = '06ca6b11eeb139f0c0f6fefafcb4af73abe871056f9b97485c52af76540868ef'
ORIGINAL_PROTOCOL_SHA = 'a4c6bd18433bb1c808b6e81915ed75ff4652d78fc185796874b6a2cfe7d1b1eb'
TRACE_POLICY = {'DOTNET_HOST_TRACE': '1', 'DOTNET_HOST_TRACE_VERBOSITY': '3',
                'traceSideFiles': 0, 'stderrBytes': 524288, 'stdoutBytes': 2097152,
                'pollSeconds': 0.1, 'overflowDisposition': 'retained failure; no retry'}

def load_fixed(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Bootstrap source identity is checked before interpreting the immutable library.
import hashlib
with (ORIGINAL / 'protocol.py').open('rb') as stream:
    if hashlib.file_digest(stream, 'sha256').hexdigest() != ORIGINAL_PROTOCOL_SHA:
        raise ValueError('immutable original protocol changed')
old = load_fixed('boolean_v1_immutable_protocol', ORIGINAL / 'protocol.py')
require, sha, read, write, descriptor, pin, keys = old.require, old.sha, old.read, old.write, old.descriptor, old.pin, old.keys

def digest(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None,
            '64 lowercase hex digest required')
    return value

def environment(out):
    result = dict(old.environment(out))
    result['DOTNET_HOST_TRACE_VERBOSITY'] = '3'
    return result

def native_argv(out):
    return old.native_argv(out)

def output_path(value, fresh=False):
    out = Path(value).resolve()
    require(out.parent == A2 and out.name in ['native-pass1', 'native-pass2'],
            'two designated recovery outputs only')
    require(not out.is_symlink(), 'output symlink')
    if fresh:
        require(not out.exists(), 'one attempt only; no overwrite or retry')
    return out

def fixtures(out):
    def inventory(root):
        return {str(x.relative_to(root)): sha(x) for x in root.rglob('*') if x.is_file()}
    expected = inventory(ORIGINAL / 'fixtures')
    require(len(expected) == 362, 'original copied fixture count')
    require(inventory(Path(out) / 'fixtures') == expected, 'exact copied fixture inventory/hash or task marker')

def verify_execution(lock_sha):
    digest(lock_sha)
    require(sha(HERE / 'execution-lock.json') == lock_sha, 'external recovery execution lock SHA')
    lock = read(HERE / 'execution-lock.json')
    keys(lock, ['schemaVersion', 'originalNativeLock', 'pythonRuntimeManifest', 'oldFailure',
                'protectedManifest', 'pins', 'profileInventory', 'futureReviewPath', 'tracePolicy'], 'execution lock')
    require(type(lock['schemaVersion']) is int and lock['schemaVersion'] == 2, 'execution schema')
    require(lock['originalNativeLock'] == descriptor(ORIGINAL / 'native-input-lock.json')
            and lock['originalNativeLock']['sha256'] == ORIGINAL_LOCK_SHA, 'immutable native lock binding')
    require(lock['pythonRuntimeManifest'] == descriptor(ORIGINAL / 'python-runtime-manifest.json')
            and lock['pythonRuntimeManifest']['sha256'] == PYTHON_SHA, 'Python manifest binding')
    require(lock['oldFailure'] == descriptor(O / 'batch2516-native-attempt1-failure-v1.json')
            and lock['oldFailure']['sha256'] == FAILURE_SHA, 'failed attempt binding')
    require(lock['futureReviewPath'] == str(REVIEW) and lock['tracePolicy'] == TRACE_POLICY,
            'fixed review/diagnostic policy')
    pin(lock['protectedManifest'])
    protected = read(lock['protectedManifest']['path'])
    for item in protected['pins']:
        pin(item)
    for root in protected['roots']:
        expected = {x['path'] for x in protected['pins'] if Path(x['path']).is_relative_to(Path(root))}
        actual = {str(x.resolve()) for x in Path(root).rglob('*') if x.is_file()}
        require(actual == expected, 'immutable original inventory changed')
    for item in lock['pins']:
        pin(item)
    expected = {str(x.resolve()) for x in HERE.rglob('*') if x.is_file() and x.name != 'execution-lock.json'}
    require(set(lock['profileInventory']) == expected, 'new profile additions/removals')
    require(set(lock['profileInventory']).issubset({x['path'] for x in lock['pins']}), 'profile source closure')
    old.verify_lock(ORIGINAL_LOCK_SHA)
    return lock

def review_authorization(path, review_sha, execution_sha):
    require(Path(path).resolve() == REVIEW and not REVIEW.is_symlink(), 'fixed future independent review path')
    require(sha(REVIEW) == digest(review_sha), 'external recovery review SHA')
    review = read(REVIEW)
    validate_review(review, execution_sha)
    return descriptor(REVIEW)

def validate_review(review, execution_sha):
    require(type(review) is dict, 'review object')
    require(review.get('readyForNativeCapture') is True, 'independent approval required')
    require(review.get('inputLockSha256') == ORIGINAL_LOCK_SHA
            and review.get('executionLockSha256') == execution_sha
            and review.get('pythonRuntimeManifestSha256') == PYTHON_SHA
            and review.get('oldFailureSha256') == FAILURE_SHA
            and review.get('tracePolicy') == TRACE_POLICY,
            'new recovery approval bindings')
    return review

def capture_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--original-lock-sha256', required=True)
    parser.add_argument('--execution-lock-sha256', required=True)
    parser.add_argument('--review', type=Path, required=True)
    parser.add_argument('--review-sha256', required=True)
    parser.add_argument('--root-reviewed-authorization', action='store_true', required=True)
    return parser

def verify_parser(pair=False):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in (['first', 'second'] if pair else ['receipt']):
        parser.add_argument('--' + name, type=Path, required=True)
        parser.add_argument('--' + name + '-sha256', required=True)
    parser.add_argument('--original-lock-sha256', required=True)
    parser.add_argument('--execution-lock-sha256', required=True)
    return parser

def resource_samples(samples):
    require(type(samples) is list and len(samples) >= 2, 'resource evidence')
    for admission in samples[:-1]:
        keys(admission, ['freePhysicalBytes', 'freeVirtualBytes'], 'admission sample')
        require(all(type(v) is int and v >= 0 for v in admission.values()), 'typed admission sample')
    final = samples[-1]
    keys(final, ['prelaunch', 'durationSeconds'], 'fresh sample')
    sample = final['prelaunch']
    keys(sample, ['freePhysicalBytes', 'freeVirtualBytes'], 'memory sample')
    require(type(final['durationSeconds']) in [int, float] and 0 <= final['durationSeconds'] <= 2, 'freshness')
    require(type(sample['freePhysicalBytes']) is int and sample['freePhysicalBytes'] >= 512 * 1024**2
            and type(sample['freeVirtualBytes']) is int and sample['freeVirtualBytes'] >= 16 * 1024**3,
            'resource floors')

def host_trace(path):
    raw = old.bounded(path, 512 * 1024)
    # trace::setup emits this at info level. Raw bytes remain independently bound;
    # this is presence evidence, never a filter or a replacement for loaded paths.
    require(b'Tracing enabled @ ' in raw or 'Tracing enabled @ '.encode('utf-16le') in raw,
            'retained info host startup trace required')

RECEIPT_FIELDS = ['schemaVersion', 'status', 'inputLockSha256', 'executionLockSha256',
                  'pythonRuntimeManifestSha256', 'oldFailureSha256', 'tracePolicy', 'review',
                  'fixtureRoot', 'environment', 'resourceSamples', 'process', 'raw',
                  'nativeExecutions', 'compilerExecutions', 'failure']

def validate_receipt(r, out, execution_sha):
    """Pure receipt semantics, separate from external filesystem/approval binding."""
    keys(r, RECEIPT_FIELDS, 'recovery receipt')
    require(type(r['schemaVersion']) is int and r['schemaVersion'] == 2
            and r['status'] == 'CAPTURED_PENDING_ROOT_REVIEW' and r['failure'] is None,
            'successful recovery status')
    require(r['inputLockSha256'] == ORIGINAL_LOCK_SHA and r['executionLockSha256'] == execution_sha
            and r['pythonRuntimeManifestSha256'] == PYTHON_SHA and r['oldFailureSha256'] == FAILURE_SHA
            and r['tracePolicy'] == TRACE_POLICY, 'recovery receipt closure/policy')
    require(type(r['nativeExecutions']) is int and r['nativeExecutions'] == 1
            and type(r['compilerExecutions']) is int and r['compilerExecutions'] == 0, 'actual process counts')
    require(r['fixtureRoot'] == str(out / 'fixtures') and r['environment'] == environment(out),
            'explicit trace3 environment/root')
    old.process(r['process'], native_argv(out), out, 'native', 30)
    resource_samples(r['resourceSamples'])
    keys(r['raw'], ['stdout', 'stderr'], 'raw streams')
    for stream in ['stdout', 'stderr']:
        pin(r['raw'][stream])
        require(r['raw'][stream]['path'] == str((out / ('native.' + stream)).resolve()), 'raw stream path')
    require(r['review']['path'] == str(REVIEW), 'recovery review path')
    host_trace(out / 'native.stderr')
    return old.observation(read(out / 'native.stdout'))

def receipt(path, receipt_sha, original_sha, execution_sha):
    require(original_sha == ORIGINAL_LOCK_SHA, 'fixed original lock')
    require(sha(path) == digest(receipt_sha), 'external receipt SHA')
    verify_execution(execution_sha)
    out = output_path(Path(path).resolve().parent)
    require(Path(path).resolve() == out / 'receipt.json', 'fixed receipt name')
    r = read(path)
    keys(r, RECEIPT_FIELDS, 'recovery receipt')
    pin(r['review'])
    review_authorization(r['review']['path'], r['review']['sha256'], execution_sha)
    value = validate_receipt(r, out, execution_sha)
    fixtures(out)
    return r, value

def normalized(value, root):
    # Reuse the original exact, declared path/message-only normalization.
    comparator = load_fixed('boolean_v1_immutable_comparator', ORIGINAL / 'compare_pair.py')
    return comparator.normalized(value, root)

def compare_values(r1, v1, r2, v2):
    require(r1['fixtureRoot'] != r2['fixtureRoot']
            and r1['process']['processId'] != r2['process']['processId'], 'two distinct new runs')
    require(normalized(v1, r1['fixtureRoot']) == normalized(v2, r2['fixtureRoot']),
            'native outcomes differ; preserve failure, no retry')
