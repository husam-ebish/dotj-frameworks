"""Java-only Task adaptation controls against an explicit hash-bound product JAR.

Reuses the frozen owned-process/resource/environment primitives. No native launch,
source fallback, product compilation, or implicit discovery of a candidate JAR.
"""
import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('task_comparison', HERE / 'run-comparison.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def inputs(jar, expected):
    c.require(c.sha(jar) == expected, 'candidate JAR hash mismatch')
    return [c.descriptor(path) for path in [jar, Path(__file__), HERE / 'TaskBoundaryControls.java',
        HERE / 'run-comparison.py', HERE / 'owned_process.py', c.JDK / 'bin/javac.exe', c.JDK / 'bin/java.exe']]


def execute(a):
    out = c.confined(a.out)
    jar = c.confined(a.candidate_jar)
    c.require((out / 'controller.json').exists() and not (out / 'receipt.json').exists(), 'fresh owned inner run required')
    pinned = c.read(out / 'inputs.json')
    env = c.environment(out)
    deadline = time.monotonic() + 420
    receipt = {'status': 'RUNNING', 'inputs': pinned, 'environment': env, 'commands': [], 'nativeExecutions': 0}
    def save(): c.write(out / 'receipt.json', receipt)
    save()
    try:
        commands = [
            ('compile-boundary', [str(c.JDK / 'bin/javac.exe'), *['-J' + x for x in c.jvm(out)],
                '-encoding', 'UTF-8', '-implicit:none', '-sourcepath', str(out / 'empty-sourcepath'),
                '-cp', str(jar), '-d', str(out / 'classes'), str(HERE / 'TaskBoundaryControls.java')]),
            ('run-boundary', [str(c.JDK / 'bin/java.exe'), *c.jvm(out), '-cp',
                str(out / 'classes') + os.pathsep + str(jar), 'System.Threading.Tasks.TaskBoundaryControls', str(jar)])]
        for label, argv in commands:
            for item in pinned + receipt.get('artifacts', []): c.validate_descriptor(item)
            sampled, samples = c.owned.wait_resources(deadline)
            entry = {'label': label, 'resources': samples}
            receipt['commands'].append(entry)
            def update(record): entry.update(record); save()
            def prelaunch(): c.require(time.monotonic() - sampled <= 2 and time.monotonic() + 125 < deadline, 'expired resource/budget')
            entry.update(c.owned.run(argv, out, env, label, 120, on_update=update, prelaunch=prelaunch))
            entry['streams'] = c.stream_descriptors(entry)
            save(); c.successful(entry)
            if label == 'compile-boundary':
                receipt['artifacts'] = [c.descriptor(path) for path in sorted((out / 'classes').rglob('*.class'))]
                c.require([Path(x['path']).relative_to(out / 'classes').as_posix() for x in receipt['artifacts']] ==
                    ['System/Threading/Tasks/TaskBoundaryControls.class'], 'unexpected fixture/product classes')
        for item in pinned + receipt['artifacts']: c.validate_descriptor(item)
        output = c.bounded_bytes(out / 'run-boundary.stdout').decode('utf-8').strip()
        c.require(output.startswith('PASS Task Java boundary controls: ') and output.rsplit(' ', 1)[1].isdigit(), 'missing boundary proof')
        c.require((out / 'run-boundary.stderr').stat().st_size == 0, 'unexpected boundary stderr')
        receipt.update(status='PASS_TASK_JAVA_BOUNDARIES', result=output)
        save()
    except BaseException as error:
        receipt.update(status='FAILED_STOP_NO_RETRY', error=str(error)); save(); raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate-jar', required=True, type=Path)
    p.add_argument('--candidate-sha256', required=True)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--inner', action='store_true')
    a = p.parse_args()
    c.require(os.name == 'nt', 'Windows ownership profile required')
    if a.inner:
        execute(a)
    else:
        out = c.confined(a.out)
        jar = c.confined(a.candidate_jar)
        pins = inputs(jar, a.candidate_sha256)
        c.require(not out.exists(), 'fresh output directory required')
        out.mkdir(parents=True)
        for name in ['tmp', 'home/AppData/Roaming', 'home/AppData/Local', 'cache', 'classes', 'empty-sourcepath']:
            (out / name).mkdir(parents=True, exist_ok=True)
        c.write(out / 'inputs.json', pins)
        env = c.environment(out)
        argv = [str(c.PYTHON), '-B', str(Path(__file__)), *sys.argv[1:], '--inner']
        c.write(out / 'controller.json', {'argv': argv, 'environment': env})
        result = c.owned.run(argv, out, env, 'controller', 480,
            on_update=lambda record: c.write(out / 'controller.json', dict(record, environment=env)))
        result['streams'] = c.stream_descriptors(result)
        c.write(out / 'controller.json', dict(result, environment=env)); c.successful(result)
    print(json.dumps(c.read(a.out / 'receipt.json')['status']))


if __name__ == '__main__':
    main()
