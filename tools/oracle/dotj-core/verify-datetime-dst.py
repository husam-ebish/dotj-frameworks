"""Compare modern Europe/Zurich gap, overlap and local round-trip behavior with pinned CLR evidence."""
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--filetime',action='store_true');mode.add_argument('--binary',action='store_true');args=parser.parse_args()
    if args.jar is None:
        artifact=json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'));args.jar=ROOT/artifact['jarPath']
    contract='datetime-binary' if args.binary else 'datetime-filetime' if args.filetime else 'datetime-dst'
    path=EVIDENCE/(contract+'-contract-v10.0.12.json');oracle=json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion']=='10.0.12'
    assert oracle['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+contract+'-contract.ps1').read_bytes()).hexdigest()
    assert oracle['nativeLocalZone']=='W. Europe Standard Time' and oracle['javaZoneProfile']=='Europe/Zurich'
    assert any(row['isAmbiguous'] for row in oracle['selectedZoneFacts']) and any(row['isInvalid'] for row in oracle['selectedZoneFacts'])
    calls={'ToUniversalTime':'value.ToUniversalTime()','ToLocalTime':'value.ToLocalTime()',
        'IsDaylightSavingTime':'value.IsDaylightSavingTime()','AddTicksZeroThenUtc':'value.AddTicks(0L).ToUniversalTime()',
        'AddTickThenUtc':'value.AddTicks(1L).ToUniversalTime()','AddMonthsZeroThenUtc':'value.AddMonths(0).ToUniversalTime()',
        'AddYearsZeroThenUtc':'value.AddYears(0).ToUniversalTime()','DateThenUtc':'value.get_Date().ToUniversalTime()',
        'SpecifyLocalThenUtc':'DateTime.SpecifyKind(value,DateTimeKind.Local).ToUniversalTime()',
        'SpecifyUnspecifiedThenUtc':'DateTime.SpecifyKind(value,DateTimeKind.Unspecified).ToUniversalTime()',
        'DateThen230ThenUtc':'value.get_Date().AddHours(2.5).ToUniversalTime()',
        'AddDayRoundTripUtc':'value.AddDays(1.0).AddDays(-1.0).ToUniversalTime()',
        'AddMonthsRoundTripUtc':'value.AddMonths(1).AddMonths(-1).ToUniversalTime()',
        'AddYearsRoundTripUtc':'value.AddYears(1).AddYears(-1).ToUniversalTime()'}
    if args.filetime:
        calls={'ToFileTime':'value.ToFileTime()','ToFileTimeUtc':'value.ToFileTimeUtc()',
            'FileTimeRoundTrip':'DateTime.FromFileTime(value.ToFileTime())',
            'FileTimeRoundTripUtc':'DateTime.FromFileTimeUtc(value.ToFileTimeUtc())',
            'FileTimeRoundTripLocalThenUtc':'DateTime.FromFileTime(value.ToFileTime()).ToUniversalTime()',
            'FileTimeUtcRoundTripLocal':'DateTime.FromFileTime(value.ToFileTimeUtc())',
            'FileTimeImportedThenAddTickUtc':'DateTime.FromFileTime(value.ToFileTime()).AddTicks(1L).ToUniversalTime()',
            'FileTimeImportedThenDaylight':'DateTime.FromFileTime(value.ToFileTime()).IsDaylightSavingTime()'}
    if args.binary:
        calls={'ToBinary':'value.ToBinary()','BinaryRoundTrip':'DateTime.FromBinary(value.ToBinary())',
            'BinaryRoundTripUtc':'DateTime.FromBinary(value.ToBinary()).ToUniversalTime()',
            'BinaryImportedThenDaylight':'DateTime.FromBinary(value.ToBinary()).IsDaylightSavingTime()',
            'BinaryImportedThenAddTickUtc':'DateTime.FromBinary(value.ToBinary()).AddTicks(1L).ToUniversalTime()',
            'BinaryImportedDateThen230Utc':'DateTime.FromBinary(value.ToBinary()).get_Date().AddHours(2.5).ToUniversalTime()',
            'BinaryImportedSpecifyLocalUtc':'DateTime.SpecifyKind(DateTime.FromBinary(value.ToBinary()),DateTimeKind.Local).ToUniversalTime()',
            'BinaryWithLocalAmbiguousFlag':'DateTime.FromBinary(value.get_Kind() == DateTimeKind.Local ? value.ToBinary() | 0x4000_0000_0000_0000L : value.ToBinary())'}
    cases=[]
    for index,row in enumerate(oracle['cases']):
        checks=[f'DateTime input=new DateTime({row["inputTicks"]}L,DateTimeKind.{row["inputKind"]});',
                'DateTime value='+('input' if row['route']=='direct' else 'input.ToLocalTime()')+';',
                f'check(value.get_Ticks() == {row["valueTicks"]}L && value.get_Kind() == DateTimeKind.{row["valueKind"]},{index});']
        result=row['result'];expression=calls[row['operation']]
        if 'boolean' in result:checks.append(f'check({expression} == {str(result["boolean"]).lower()},{index});')
        elif 'integer' in result:checks.append(f'check({expression} == {result["integer"]}L,{index});')
        else:
            checks.append(f'DateTime result={expression};')
            checks.append(f'check(result.get_Ticks() == {result["ticks"]}L && result.get_Kind() == DateTimeKind.{result["kind"]},{index});')
        cases.append('{\n'+'\n'.join(checks)+'\n}')
    assert len(cases)==(2304 if args.filetime or args.binary else 4032)
    historical_count=0
    if args.binary:
        assert len(oracle['binaryScalars'])==18
        for row in oracle['binaryScalars']:
            index=len(cases);result=row['result'];expression=f'DateTime.FromBinary({row["dateData"]}L)'
            if 'exception' in result:
                checks=[f'''try{{{expression};throw new AssertionError("missing binary exception {index}");}}
catch(ArgumentException expected){{check(expected.getClass().getName().equals("{result['exception']}") && expected.get_HResult() == {result['hResult']} && java.util.Objects.equals(expected.get_ParamName(),{json.dumps(result['paramName'])}),{index});}}''']
            else:
                checks=[f'DateTime result={expression};',
                    f'check(result.get_Kind() == DateTimeKind.{result["kind"]} && result.ToBinary() == {result["normalizedBinary"]}L,{index});']
                if row['comparison']=='exact':checks.append(f'check(result.get_Ticks() == {result["ticks"]}L,{index});')
                else:
                    historical_count+=1
                    checks.append(f'check(result.get_Ticks() >= 0L && result.get_Ticks() < 864000000000L,{index});')
            cases.append('{\n'+'\n'.join(checks)+'\n}')
        assert historical_count==2
    work=Path('D:/AI/Implementation/dotj Frameworks/verification')/contract;work.mkdir(parents=True,exist_ok=True)
    source=work/'DateTimeDstProbe.java'
    methods=['static void group'+str(offset//20)+'(){\n'+'\n'.join(cases[offset:offset+20])+'\n}' for offset in range(0,len(cases),20)]
    source.write_text('import System.DateTime;import System.DateTimeKind;import System.ArgumentException;\npublic class DateTimeDstProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+
        '\n'.join(methods)+'\npublic static void main(String[] args){'+'\n'.join(f'group{index}();' for index in range(len(methods)))+
        '\njava.lang.System.out.println("TZDB "+java.time.zone.ZoneRulesProvider.getVersions("Europe/Zurich").lastKey());\n}}\n',encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    result=subprocess.run(['java','-Duser.timezone=Europe/Zurich','-cp',str(args.jar)+';'+str(work),'DateTimeDstProbe'],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    versions=[line[5:] for line in result.stdout.splitlines() if line.startswith('TZDB ')];assert len(versions)==1
    record=dict(schemaVersion=1,scope='Selected modern local binary encoding, decoding and overlap propagation; UTC/Unspecified scalar bounds; two historical scalars test classification and normalization only' if args.binary else 'Selected modern local file-time export/import and overlap propagation' if args.filetime else 'Selected 2024/2026 Windows W. Europe and JDK Europe/Zurich gap/overlap profile',
        oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        casesPassed=len(cases),operations=dict(Counter(row['operation'] for row in oracle['cases'])),javaZoneProfile='Europe/Zurich',javaZoneRulesVersion=versions[0],
        historicalClassificationAndNormalizationOnly=historical_count,
        qualification='BOUNDED_MODERN_BINARY_PASS; HISTORICAL_LOCAL_TICK_PARITY_OTHER_ZONES_FULL_EXTREMA_AND_LANGUAGE_OPEN' if args.binary else 'BOUNDED_MODERN_FILETIME_PASS; OTHER_ZONES_HISTORICAL_RULES_EXTREMA_BINARY_AND_LANGUAGE_OPEN' if args.filetime else 'BOUNDED_MODERN_DST_PASS; OTHER_ZONES_HISTORICAL_RULES_BINARY_AND_LANGUAGE_OPEN')
    (EVIDENCE/(contract+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(f'PASS {contract}: {len(cases)} pinned groups; JDK zone rules {versions[0]}')


if __name__=='__main__':main()
