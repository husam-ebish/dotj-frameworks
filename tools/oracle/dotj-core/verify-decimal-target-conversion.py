"""Verify selected Decimal target dispatch, rounding, result bits and logical carriers."""
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
    path=EVIDENCE/'decimal-target-conversion-contract-v10.0.12.json';oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12' and oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-decimal-target-conversion-contract.ps1').read_bytes()).hexdigest()
    assert oracle['cultureProfile']=='Invariant'
    cases=[]
    for row in oracle['queries']:
        index=len(cases);result=row['result'];target='null' if row['target'] is None else 'Type.GetType("'+row['target']+'")'
        expression=f'Decimal.Parse({json.dumps(row["value"])}).ToType({target},null)' 
        if 'exception' in result:
            param=f' && java.util.Objects.equals(((ArgumentException)expected).get_ParamName(),{json.dumps(result["paramName"])})' if result['exception'].endswith(('ArgumentException','ArgumentNullException')) else ''
            cases.append(f'try{{{expression};throw new AssertionError("missing conversion error {index}");}}catch({result["exception"].split(".")[-1]} expected){{check(expected.getClass().getName().equals("{result["exception"]}") && expected.get_HResult()=={result["hResult"]}{param},{index});}}')
            continue
        typename=result['type']
        carrier={'System.Boolean':'Boolean','System.Char':'Character','System.SByte':'SByte','System.Byte':'Byte','System.Int16':'Short','System.UInt16':'UInt16','System.Int32':'Int32','System.UInt32':'UInt32','System.Int64':'Long','System.UInt64':'java.math.BigInteger','System.Single':'Float','System.Double':'Double','System.Decimal':'Decimal','System.String':'String'}[typename]
        checks=[f'actual instanceof {carrier}']
        if 'boolean' in result:checks.append(f'((Boolean)actual).booleanValue()=={str(result["boolean"]).lower()}')
        elif 'character' in result:checks.append(f'((Character)actual).charValue()=={result["character"]}')
        elif 'singleBits' in result:checks.append(f'Float.floatToRawIntBits((Float)actual)=={result["singleBits"]}')
        elif 'doubleBits' in result:checks.append(f'Double.doubleToRawLongBits((Double)actual)=={result["doubleBits"]}L')
        else:
            accessor='((IConvertible)actual).ToString(null)' if typename in ('System.SByte','System.Byte','System.UInt16','System.Int32','System.UInt32','System.Decimal') else 'actual.toString()'
            checks.append(f'{accessor}.equals({json.dumps(result["text"])})')
        if 'decimalBits' in result:checks.append('java.util.Arrays.equals(Decimal.GetBits((Decimal)actual),new int[]{'+','.join(str(word) for word in result['decimalBits'])+'})')
        cases.append('{Object actual='+expression+';check('+' && '.join(checks)+f',{index});'+'}')
    assert len(cases)==1242
    work=Path('D:/AI/Implementation/dotj Frameworks/verification/decimal-target-conversion');work.mkdir(parents=True,exist_ok=True)
    source=work/'DecimalTargetConversionProbe.java';methods=['static void group'+str(offset//15)+'(){\n'+'\n'.join(cases[offset:offset+15])+'\n}' for offset in range(0,len(cases),15)]
    source.write_text('import System.Type;import System.Globalization.TimeSpanStyles;import System.ArgumentException;import System.ArgumentNullException;import System.Int32;import System.IConvertible;import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Decimal;import System.OverflowException;import System.InvalidCastException;import System.InvalidOperationException;import System.DayOfWeek;import System.DateTimeKind;import System.Globalization.NumberStyles;\nclass DecimalTargetConversionProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+'}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DecimalTargetConversionProbe'],check=True)
    record=dict(schemaVersion=1,scope='Decimal IConvertible target dispatch and signed-zero and halfway floating results, checked ranges, host carriers, floating result bits and error identities',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),casesPassed=len(cases),qualification='BOUNDED_DECIMAL_TARGET_CONVERSION_PASS; PROVIDER_BOXING_IDENTITY_FULL_MESSAGES_AND_LANGUAGE_OPEN')
    (EVIDENCE/'decimal-target-conversion-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS selected Decimal target conversions: {len(cases)} pinned groups')

if __name__=='__main__':main()
