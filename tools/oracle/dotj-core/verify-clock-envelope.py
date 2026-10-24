"""Run designed native clock-frame cases, including old-policy DST counterexamples."""
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ORACLE=Path(__file__).parent
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ORACLE/'run-pinned-contract-oracle.ps1'),'-Contract','clock-envelope'],check=True)
    path=EVIDENCE/'clock-envelope-contract-v10.0.12.json';record=json.loads(path.read_text(encoding='utf-8'))
    assert record['runtimeVersion']=='10.0.12' and record['casesPassed']==13 and record['validFoldCounterexamples']==2
    assert record['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert record['oracleSha256']==hashlib.sha256((ORACLE/'capture-clock-envelope-contract.ps1').read_bytes()).hexdigest()
    assert record['helperSha256']==hashlib.sha256((ORACLE/'clock-envelope-v1.ps1').read_bytes()).hexdigest()
    assert Counter(row['actualStatus'] for row in record['cases'])=={'Pass':8,'Fail':4,'ReferenceClockReversed':1}
    assert all(row['actualStatus']==row['expectedStatus'] and row['passed'] for row in record['cases'])
    print('PASS UTC clock-frame classifier: 13 designed native cases; accepted valid fold reads and rejected malformed samples')


if __name__=='__main__':main()
