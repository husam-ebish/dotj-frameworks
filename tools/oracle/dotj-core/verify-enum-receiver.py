"""Verify native argument-versus-receiver validation order for selected enum queries."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path);args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    path=EVIDENCE/'enum-receiver-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-enum-receiver-contract.ps1').read_bytes()).hexdigest()
    assert len({row['type'] for row in oracle['queries']})==9
    assert all(row['exception'] in ('System.ArgumentException','System.ArgumentNullException') for row in oracle['queries'])
    cases=[]
    for row in oracle['queries']:
        v=row['value'];op=row['operation'];argument=''
        if op in ('GetEnumName','IsEnumDefined'):
            if v is None:argument='null'
            elif isinstance(v,str):argument=json.dumps(v)
            elif isinstance(v,bool):argument='true'
            else:argument=str(v)
        # Capture retains input category: CLR integer, long, enum and floating boxes must stay distinct.
        kind=row['kind']
        if kind=='double':argument='1.0'
        elif kind=='long':argument='1L'
        elif kind=='day':argument='DayOfWeek.Monday'
        name=row['type'];receiver=f'Type.GetType("{name}")'
        for suffix,factory in [('*','MakePointerType'),('&','MakeByRefType'),('[]','MakeArrayType')]:
            if name.endswith(suffix):receiver=f'Type.GetType("{name[:-len(suffix)]}").{factory}()';break
        index=len(cases);expression=f'{receiver}.{op}({argument})'
        cases.append(f'try{{{expression};throw new AssertionError("missing error {index}");}}catch({row["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{row["exception"]}") && expected.get_HResult()=={row["hResult"]} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(row["paramName"])}),{index});}}')
    assert len(cases)==162
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/enum-receiver');work.mkdir(parents=True,exist_ok=True)
    source=work/'EnumReceiverProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass EnumReceiverProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'EnumReceiverProbe'],check=True)
    record=dict(schemaVersion=1,scope='Non-enum receiver and argument validation precedence across nine selected types',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_ENUM_QUERY_PASS; OTHER_UNDERLYING_TYPES_AND_FULL_REFLECTION_OPEN')
    (EVIDENCE/'enum-receiver-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected non-enum receiver validation: {len(cases)} pinned groups')

if __name__=='__main__':main()
