"""Verify OLE Automation conversion bits, range boundaries and operation-specific failures."""
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
    path=EVIDENCE/'datetime-oadate-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-datetime-oadate-contract.ps1').read_bytes()).hexdigest()
    cases=[]
    def literal(value):return 'Long.MIN_VALUE' if int(value)==-(2**63) else str(value)+'L'
    for direction in ('fromOADate','toOADate'):
        for row in oracle[direction]:
            index=len(cases);result=row['result']
            expression=f'DateTime.FromOADate(Double.longBitsToDouble({literal(row["bits"])}))' if direction=='fromOADate' else f'new DateTime({literal(row["ticks"])},DateTimeKind.{row["kind"]}).ToOADate()'
            if 'exception' in result:
                param=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith('ArgumentException') else ''
                cases.append(f'try{{{expression};throw new AssertionError("missing error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{param},{index});}}')
            else:
                round_trip=result['roundTrip']
                if direction=='fromOADate':
                    prefix='{DateTime actual='+expression+f';check(actual.get_Ticks()=={literal(result["ticks"])} && actual.get_Kind()==DateTimeKind.{result["kind"]},{index});'
                    follow='actual.ToOADate()';check=f'Double.doubleToRawLongBits({follow})=={literal(round_trip["bits"])}' if 'bits' in round_trip else ''
                else:
                    prefix='{double actual='+expression+f';check(Double.doubleToRawLongBits(actual)=={literal(result["bits"])},{index});'
                    follow='DateTime.FromOADate(actual)';check=f'{follow}.get_Ticks()=={literal(round_trip["ticks"])}' if 'ticks' in round_trip else ''
                if 'exception' in round_trip:
                    suffix=f'try{{{follow};throw new AssertionError("missing round-trip error {index}");}}catch({round_trip["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{round_trip["exception"]}") && expected.get_HResult()=={round_trip["hResult"]},{index});}}'
                else:suffix=f'check({check},{index});'
                cases.append(prefix+suffix+'}')
    assert len(oracle['fromOADate'])>=120 and len(oracle['toOADate'])>=140
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-oadate');work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeOADateProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.DateTime;import System.DateTimeKind;import System.OverflowException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass DateTimeOADateProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DateTimeOADateProbe'],check=True)
    record=dict(schemaVersion=1,scope='OLE Automation imports and exports, floating bit patterns, millisecond rounding, signed fractions, bounds and Kind',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),fromCases=len(oracle['fromOADate']),toCases=len(oracle['toOADate']),casesPassed=len(cases),qualification='BOUNDED_OADATE_CONVERSION_PASS; FULL_INTEROP_LANGUAGE_AND_RELEASE_OPEN')
    (EVIDENCE/'datetime-oadate-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS OLE Automation DateTime conversions: {len(cases)} pinned groups')

if __name__=='__main__':main()
