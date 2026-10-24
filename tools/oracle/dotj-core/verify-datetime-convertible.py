"""Verify selected DateTime IConvertible results and retained modern overlap state."""
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
    path=EVIDENCE/'datetime-convertible-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-convertible-contract.ps1').read_bytes()).hexdigest()
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich' and oracle['cultureProfile']=='Invariant'
    overlaps={}
    for row in oracle['queries']:
        if row['operation']=='ToDateTime' and row['route']=='viaLocal':
            overlaps.setdefault(row['result']['ticks'],set()).add(row['result']['utcTicks'])
    assert sum(len(values)==2 for values in overlaps.values())==2
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];op=row['operation']
        prefix='{DateTime value=new DateTime('+row['inputTicks']+'L,DateTimeKind.'+row['inputKind']+');'
        if row['route']=='viaLocal':prefix+='value=value.ToLocalTime();'
        prefix+='IConvertible convertible=value;'
        if op=='GetTypeCode':expression='convertible.GetTypeCode().get_Value()'
        elif op=='ToType':expression='convertible.ToType('+('null' if row['target'] is None else 'Type.GetType("'+row['target']+'")')+',null)'
        else:expression=f'convertible.{op}(null)'
        if 'exception' in result:
            param=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
            suffix=f'try{{{expression};throw new AssertionError("missing conversion error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{param},{index});}}'
        elif 'ticks' in result:
            checks=[f'actual.get_Ticks()=={result["ticks"]}L',f'actual.get_Kind()==DateTimeKind.{result["kind"]}']
            if 'binary' in result:checks += [f'actual.ToBinary()=={result["binary"]}L',f'actual.ToUniversalTime().get_Ticks()=={result["utcTicks"]}L']
            suffix='DateTime actual=(DateTime)'+expression+';check('+' && '.join(checks)+f',{index});'
        elif 'typeCode' in result:suffix=f'check({expression}=={result["typeCode"]},{index});'
        else:suffix=f'check(java.util.Objects.equals({expression},{json.dumps(result["text"])}),{index});'
        cases.append(prefix+suffix+'}')
    assert len(cases)==1332
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-convertible');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeConvertibleProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.DateTime;import System.IConvertible;import System.InvalidCastException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass DateTimeConvertibleProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeConvertibleProbe'],check=True)
    record=dict(schemaVersion=1,scope='DateTime IConvertible primitive failures, type code, invariant String and target type conversions, selected modern local overlap state',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_DATETIME_CONVERTIBLE_PASS; FULL_PROVIDER_HISTORICAL_ZONE_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-convertible-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected DateTime IConvertible: {len(cases)} pinned groups')

if __name__=='__main__':main()
