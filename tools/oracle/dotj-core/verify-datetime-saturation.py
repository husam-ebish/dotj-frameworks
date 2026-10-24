"""Check selected saturation and explicitly separated historical/converter scopes."""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'datetime-saturation-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-saturation-contract.ps1').read_bytes()).hexdigest()
    assert len(oracle['cases'])==36
    groups={};policies=Counter();scenarios=Counter()
    for index,row in enumerate(oracle['cases']):
        policies[row['comparison']]+=1;scenarios[row['scenario']]+=1
        expression=f'DateTime.{row["operation"]}({row["input"]}L)' if row['scenario']=='fileTime' else f'new DateTime({row["input"]}L,DateTimeKind.{row["inputKind"]}).{row["operation"]}()'
        checks=[f'DateTime result={expression};',f'check(result.get_Kind() == DateTimeKind.{row["candidateKind"]},{index});']
        if row['comparison']=='exact':checks.append(f'check(result.get_Ticks() == {row["referenceTicks"]}L,{index});')
        else:
            checks.append(f'check(result.get_Ticks() >= 0L && result.get_Ticks() <= 3155378975999999999L,{index});')
            checks.append(f'check(result.ToUniversalTime().get_Ticks() == {row["normalizedUtcTicks"]}L && result.ToBinary() == {row["normalizedBinary"]}L,{index});')
        groups.setdefault(row['javaZone'],[]).append('{\n'+'\n'.join(checks)+'\n}')
    assert policies['classificationAndNormalizationOnly']==6 and scenarios['explicitNegativeZoneConverter']==4
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-saturation');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeSaturationProbe.java'
    methods=[];dispatch=[]
    for number,(zone,cases) in enumerate(groups.items()):
        methods.append('static void zone'+str(number)+'(){\n'+'\n'.join(cases)+'\n}')
        dispatch.append(f'if(args[0].equals({json.dumps(zone)})){{zone{number}();return;}}')
    source.write_text('import System.DateTime;import System.DateTimeKind;\nclass DateTimeSaturationProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){if(!java.time.ZoneId.systemDefault().getId().equals(args[0]))throw new AssertionError("wrong zone");'+
        '\n'.join(dispatch)+'throw new AssertionError("unknown zone");}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    for zone in groups:subprocess.run(['java','-Duser.timezone='+zone,'-cp',str(args.jar)+';'+str(work),'DateTimeSaturationProbe',zone],check=True)
    record=dict(schemaVersion=1,scope='Selected DateTime conversion and file-time saturation; historical and alternative-converter scopes explicit',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(oracle['cases']),casesByComparison=dict(policies),casesByScenario=dict(scenarios),
        qualification='BOUNDED_SATURATION_PASS; HISTORICAL_LOCAL_TICK_PARITY_OTHER_ZONES_FULL_RANGE_AND_LANGUAGE_OPEN')
    (EVIDENCE/'datetime-saturation-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS selected DateTime saturation: 36 groups; 6 historical normalization-only and 4 explicit converter alternatives')


if __name__=='__main__':main()
