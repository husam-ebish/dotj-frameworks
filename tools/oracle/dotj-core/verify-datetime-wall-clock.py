"""Compile an external consumer and compare its clock values with paired pinned CLR reads."""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ORACLE=Path(__file__).parent
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-wall-clock');work.mkdir(parents=True,exist_ok=True)
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(ORACLE/'fixtures/WallClockProbe.java')],check=True)
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ORACLE/'run-pinned-contract-oracle.ps1'),
                    '-Contract','datetime-clock','-JarPath',str(args.jar.resolve()),'-ConsumerClassPath',str(work.resolve())],check=True)
    path=EVIDENCE/'datetime-clock-contract-v10.0.12.json';record=json.loads(path.read_text(encoding='utf-8'))
    assert record['runtimeVersion']=='10.0.12' and record['casesPassed']==24
    assert record['candidateJarSha256']==hashlib.sha256(args.jar.read_bytes()).hexdigest()
    assert record['oracleSha256']==hashlib.sha256((ORACLE/'capture-datetime-clock-contract.ps1').read_bytes()).hexdigest()
    assert record['consumerSourceSha256']==hashlib.sha256((ORACLE/'fixtures/WallClockProbe.java').read_bytes()).hexdigest()
    assert record['consumerClassSha256']==hashlib.sha256((work/'WallClockProbe.class').read_bytes()).hexdigest()
    assert Counter(row['property'] for row in record['cases'])=={'UtcNow':8,'Now':8,'Today':8}
    assert all(row['passed'] for row in record['cases'])
    print('PASS 24 paired wall-clock samples; monotonic deadlines and full timezone qualification remain open')


if __name__=='__main__':main()
