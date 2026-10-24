"""Compare serial/parallel consumer results in an existing isolated D: worktree."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RELATIVE = Path('tools/oracle/dotj-core/build-foundation-product-candidate.py')
ARTIFACT = Path('planning/stage-2/repos/dotj-core/evidence/foundation-product-candidate-v1.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--workers', type=int, nargs='+', default=[1, 4])
    args = parser.parse_args()
    workspace = args.workspace.resolve(strict=True)
    if workspace.drive.lower() != 'd:':
        raise ValueError('Benchmark workspace must be on D:')
    if not args.workers or any(not 1 <= count <= 8 for count in args.workers):
        raise ValueError('Worker counts must be between 1 and 8')
    script_hash = hashlib.sha256((ROOT / RELATIVE).read_bytes()).hexdigest()
    assert hashlib.sha256((workspace / RELATIVE).read_bytes()).hexdigest() == script_hash
    expected = json.loads((ROOT / ARTIFACT).read_text(encoding='utf-8'))
    temporary = workspace.parent / 'benchmark-tmp'
    cache = workspace.parent / 'benchmark-python-cache'
    temporary.mkdir(exist_ok=True)
    cache.mkdir(exist_ok=True)
    measurements = []
    for workers in args.workers:
        environment = dict(os.environ, DOTJ_JAVA_WORKERS=str(workers))
        environment.update(TEMP=str(temporary), TMP=str(temporary), PYTHONPYCACHEPREFIX=str(cache))
        start = time.perf_counter()
        result = subprocess.run([sys.executable, str(workspace / RELATIVE)],
                                cwd=workspace, env=environment, capture_output=True, text=True)
        elapsed = time.perf_counter() - start
        if result.returncode:
            raise RuntimeError(f'{workers}-worker consumer run failed\n{result.stdout}{result.stderr}')
        assert 'PASS combined foundation candidate JAR and independent consumers' in result.stdout
        actual = json.loads((workspace / ARTIFACT).read_text(encoding='utf-8'))
        assert actual == expected, 'Consumer evidence changed with concurrency'
        jar = workspace / actual['jarPath']
        assert hashlib.sha256(jar.read_bytes()).hexdigest() == expected['jarSha256']
        measurements.append({'workers': workers, 'elapsedSeconds': round(elapsed, 3),
                             'candidateJarSha256': actual['jarSha256'],
                             'allConsumerAssertionsPassed': True, 'evidenceIdentical': True})
        print(f'PASS {workers} worker(s): {elapsed:.3f}s; identical JAR and complete consumer evidence', flush=True)
    record = {
        'schemaVersion': 1, 'scope': 'Packaged consumer concurrency; every consumer remains a separate JVM',
        'runnerSha256': script_hash, 'measurements': measurements,
        'qualification': 'VALIDATION_TOOL_ONLY; NO_PRODUCT_OR_FRAMEWORK_ACCEPTANCE',
    }
    output = ROOT / 'planning/stage-2/repos/dotj-core/evidence/foundation-consumer-concurrency-v1.json'
    output.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
