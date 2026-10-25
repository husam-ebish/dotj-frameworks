"""Pair volatile time-only offset formatting with pinned native clock frames."""
import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ORACLE=Path(__file__).parent
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
ROUTES={'provider','single','interface','Char','Utf8'}


def validate(oracle):
    assert len(oracle['frames'])==4 and len(oracle['cases'])==468
    assert {frame['sample'] for frame in oracle['frames']}==set(range(4))
    for frame in oracle['frames']:
        assert frame['consumerExitCode']==0 and 0<=frame['elapsedMilliseconds']<=10000
        assert 0<=int(frame['afterUtcTicks'])-int(frame['beforeUtcTicks'])<=100000000
    seen=set()
    for row in oracle['cases']:
        key=(row['sample'],row['id']);assert key not in seen;seen.add(key)
        assert row['kind'] in {'Utc','Local','Unspecified'} and int(row['inputTicks']) in {0,1,863999999999}
        assert set(row['before'])==set(row['after'])==set(row['actual'])==ROUTES
        for route in ROUTES:
            assert row['actual'][route] in {row['before'][route],row['after'][route]},(row['sample'],row['id'],row['format'],route)
    assert seen=={(sample,index) for sample in range(4) for index in range(117)}
    return len(seen)*len(ROUTES)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:args.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-timeonly-offset');work.mkdir(parents=True,exist_ok=True)
    fixture=ORACLE/'fixtures/TimeOnlyOffsetProbe.java'
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(fixture)],check=True)
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ORACLE/'run-pinned-contract-oracle.ps1'),'-Contract','datetime-timeonly-offset','-JarPath',str(args.jar.resolve()),'-ConsumerClassPath',str(work)],check=True)
    path=EVIDENCE/'datetime-timeonly-offset-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256((ORACLE/'capture-datetime-timeonly-offset-contract.ps1').read_bytes()).hexdigest()
    assert oracle['consumerSourceSha256']==hashlib.sha256(fixture.read_bytes()).hexdigest() and oracle['candidateJarSha256']==hashlib.sha256(args.jar.read_bytes()).hexdigest()
    assert oracle['javaExecutableSha256']=='1f41cc782de7ddd8824376568f9011413d710cf225047906106d2a01a0e3f7a9'
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    count=validate(oracle)
    controls=[]
    for name in ['wrong-offset','missing-route','duplicate-row','expired-frame']:
        bad=copy.deepcopy(oracle)
        if name=='wrong-offset':bad['cases'][0]['actual']['provider']='unrelated offset'
        elif name=='missing-route':del bad['cases'][0]['actual']['Char']
        elif name=='duplicate-row':bad['cases'][1]=copy.deepcopy(bad['cases'][0])
        else:bad['frames'][0]['elapsedMilliseconds']=10001
        try:validate(bad)
        except AssertionError:controls.append(name)
        else:raise AssertionError('Invalid paired evidence accepted: '+name)
    record=dict(schemaVersion=1,casesPassed=count,pairedFrames=4,casesPerFrame=117,routes=sorted(ROUTES),rejectedControls=controls,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),qualification='PAIRED_CURRENT_HOST_TIMEONLY_OFFSET_PASS; HISTORICAL_OTHER_ZONES_CLOCK_CHANGE_LIFETIME_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-timeonly-offset-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS paired time-only DateTime offsets: {count} native comparisons; 4 rejected evidence controls')


if __name__=='__main__':main()
