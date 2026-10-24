"""Verify selected Stopwatch metadata, counter arithmetic and native-checked live states."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ORACLE=Path(__file__).parent
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/stopwatch');work.mkdir(parents=True,exist_ok=True)
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(ORACLE/'fixtures/StopwatchProbe.java')],check=True)
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ORACLE/'run-pinned-contract-oracle.ps1'),
        '-Contract','stopwatch','-JarPath',str(args.jar.resolve()),'-ConsumerClassPath',str(work.resolve())],check=True)
    path=EVIDENCE/'stopwatch-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['frequency']==10_000_000 and oracle['isHighResolution']
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256((ORACLE/'capture-stopwatch-contract.ps1').read_bytes()).hexdigest()
    assert oracle['consumerSourceSha256']==hashlib.sha256((ORACLE/'fixtures/StopwatchProbe.java').read_bytes()).hexdigest()
    assert oracle['candidateJarSha256']==hashlib.sha256(args.jar.read_bytes()).hexdigest()
    assert oracle['liveStateChecksPassed']==21 and len(oracle['arithmetic'])==196
    metadata=oracle['metadata'];assert metadata['name']=='System.Diagnostics.Stopwatch' and metadata['baseType']=='System.Object' and not metadata['isSealed'] and metadata['constructorCount']==1
    output=subprocess.run(['javap','-public','-classpath',str(args.jar),'System.Diagnostics.Stopwatch'],check=True,capture_output=True,text=True).stdout
    assert 'public class System.Diagnostics.Stopwatch {' in output and 'public System.Diagnostics.Stopwatch();' in output
    declarations=[line.strip() for line in output.splitlines() if line.strip().startswith('public ') and line.strip().endswith(';')]
    type_map={'System.Void':'void','System.Boolean':'boolean','System.Int64':'long','System.String':'java.lang.String',
        'System.TimeSpan':'System.TimeSpan','System.Diagnostics.Stopwatch':'System.Diagnostics.Stopwatch'}
    methods={}
    for declaration in declarations:
        match=re.fullmatch(r'public (static )?(final )?([\w.$]+) ([\w]+)\(([^)]*)\);',declaration)
        if match:
            signature=match[3]+' '+match[4]+'('+match[5].replace(' ','')+')';methods[signature]=bool(match[1])
    expected={type_map[row['returnType']]+' '+row['name']+'('+','.join(type_map[item] for item in row['parameters'])+')':row['isStatic'] for row in metadata['methods']}
    extra='java.lang.String toString()';assert methods.pop(extra) is False
    assert methods==expected,(methods,expected)
    assert len(metadata['fields'])==2
    for field in metadata['fields']:
        assert field['isStatic'] and field['isInitOnly']
        assert f'public static final {type_map[field["type"]]} {field["name"]};' in declarations
    checks=[f'check(Stopwatch.GetElapsedTime({row["start"]}L,{row["end"]}L).get_Ticks() == {row["ticks"]}L,{index});' for index,row in enumerate(oracle['arithmetic'])]
    source=work/'StopwatchArithmeticProbe.java'
    methods=['static void group'+str(offset//30)+'(){'+'\n'.join(checks[offset:offset+30])+'}' for offset in range(0,len(checks),30)]
    source.write_text('import System.Diagnostics.Stopwatch;class StopwatchArithmeticProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'StopwatchArithmeticProbe'],check=True)
    record=dict(schemaVersion=1,scope='Selected 100 ns Stopwatch counter profile, declared API and native-checked running/stopped states',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        arithmeticCasesPassed=len(checks),liveStateStepsPassed=oracle['liveStateChecksPassed'],nativeDeclaredMethodsMapped=len(expected),javaExtraMethods=[extra],
        qualification='BOUNDED_STOPWATCH_CANDIDATE_PASS; ORIGIN_LIFETIME_RESOLUTION_SUSPEND_CONCURRENCY_REFLECTION_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'stopwatch-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS Stopwatch: {len(expected)} native declared methods, 196 arithmetic vectors and 21 native-checked live states')


if __name__=='__main__':main()
