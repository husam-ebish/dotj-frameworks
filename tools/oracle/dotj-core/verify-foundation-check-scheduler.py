"""Exercise fail-closed checks, bounded workers, stable reporting and phase completion."""
import hashlib
import json
import subprocess
import sys
import threading
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from foundation_check_scheduler import run_checks


def main():
    root=Path(__file__).resolve().parents[3]
    lock=threading.Lock();barrier=threading.Barrier(3)
    active=0;maximum=0;outputs=[]
    def execute(name):
        nonlocal active,maximum
        with lock:
            active+=1;maximum=max(maximum,active)
        try:
            if name<3:barrier.wait(timeout=10)
            time.sleep((3-name%3)*0.005)
            return subprocess.CompletedProcess([str(name)],0,f'PASS {name}\n','')
        finally:
            with lock:active-=1
    assert run_checks(range(9),execute,workers=3,emit=outputs.append)==list(range(9))
    assert maximum==3 and active==0 and outputs==[f'PASS {n}' for n in range(9)]

    calls=[]
    def failing(name):
        calls.append(name)
        return subprocess.CompletedProcess([name],1,'PASS misleading\n','serial sentinel')
    try:run_checks(('fail','must-not-run'),failing)
    except RuntimeError as error:assert 'serial sentinel' in str(error)
    else:raise AssertionError('Failed serial prerequisite accepted')
    assert calls==['fail']

    live=[]
    def concurrent_failure(name):
        with lock:live.append(name)
        try:
            time.sleep(0.01)
            return subprocess.CompletedProcess([name],int(name=='fail'),'PASS fixture\n','parallel sentinel')
        finally:
            with lock:live.remove(name)
    try:run_checks(('slow','fail','queued-a','queued-b'),concurrent_failure,workers=2)
    except RuntimeError as error:assert 'parallel sentinel' in str(error)
    else:raise AssertionError('Failed parallel check accepted')
    assert not live

    def child(code):
        return lambda _:subprocess.run([sys.executable,'-c',code],capture_output=True,text=True,cwd=root)
    try:run_checks(('nonzero',),child('import sys;print("PASS misleading");sys.stderr.write("child sentinel");sys.exit(7)'))
    except RuntimeError as error:assert '(7)' in str(error) and 'child sentinel' in str(error)
    else:raise AssertionError('Nonzero child accepted')
    try:run_checks(('missing-pass',),child('print("BYPASS is not a success marker")'))
    except RuntimeError as error:assert 'missing-pass' in str(error)
    else:raise AssertionError('Missing success marker accepted')

    def missing(_):raise FileNotFoundError('unavailable executable')
    try:run_checks(('missing-tool',),missing,workers=2)
    except FileNotFoundError:pass
    else:raise AssertionError('Missing executable accepted')
    for workers in (0,4):
        try:run_checks((),execute,workers=workers)
        except ValueError:pass
        else:raise AssertionError('Unbounded worker setting accepted')

    module=Path(__file__).with_name('foundation_check_scheduler.py')
    record=dict(schemaVersion=1,casesPassed=7,workerLimit=3,observedMaximumWorkers=maximum,
                schedulerSha256=hashlib.sha256(module.read_bytes()).hexdigest(),
                verifierSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                qualification='DEVELOPMENT_CHECK_SCHEDULER_ONLY; NO_PRODUCT_ACCEPTANCE_CREDIT')
    target=root/'planning/stage-2/repos/dotj-core/evidence/foundation-check-scheduler-v1.json'
    target.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS foundation check scheduler: 7 failure/concurrency groups; maximum three workers')


if __name__=='__main__':main()
