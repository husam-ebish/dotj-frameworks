"""Differentially test all selected TimeSpan interval factory vectors against a JAR."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'planning/stage-2/repos/dotj-core/evidence'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jar', type=Path)
    parser.add_argument('--constructors', action='store_true')
    parser.add_argument('--work', type=Path, default=Path('D:/AI/Implementation/dotj Frameworks/verification/timespan-intervals'))
    args = parser.parse_args()
    if args.jar is None:
        artifact = json.loads((EVIDENCE / 'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))
        args.jar = ROOT / artifact['jarPath']
    if args.work.resolve().drive.lower() != 'd:':
        raise ValueError('Probe sources and classes must be stored on D:')
    oracle_path = EVIDENCE / 'timespan-contract-v10.0.12.json'
    oracle = json.loads(oracle_path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion'] == '10.0.12'
    assert oracle['coreLibSha256'] == '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256'] == hashlib.sha256((ROOT / 'tools/oracle/dotj-core/capture-timespan-contract.ps1').read_bytes()).hexdigest()
    cases = []
    section = 'constructors' if args.constructors else 'factories'
    for index, case in enumerate(oracle[section]):
        expression = ('new TimeSpan(' + ','.join(str(value) for value in case['components']) + ')') if args.constructors else f"TimeSpan.{case['method']}(Double.longBitsToDouble(0x{case['inputBits']}L))"
        result = case['result']
        if 'ticks' in result:
            cases.append(f'check({expression}.get_Ticks() == {result["ticks"]}L, {index});')
        else:
            parameter = 'null' if result['paramName'] is None else json.dumps(result['paramName'])
            cases.append(f'''try {{ {expression}; throw new AssertionError("missing exception {index}"); }}
                catch ({result['exception'].split('.')[-1]} expected) {{
                    check(expected.getClass().getName().equals("{result['exception']}"), {index});
                    {'check(java.util.Objects.equals(expected.get_ParamName(), ' + parameter + '), ' + str(index) + ');' if result['exception'] in ('System.ArgumentException', 'System.ArgumentOutOfRangeException') else ''}
                }}''')
    args.work = args.work / section
    args.work.mkdir(parents=True, exist_ok=True)
    source = args.work / 'TimeSpanIntervalProbe.java'
    source.write_text('import System.TimeSpan;\nimport System.ArgumentException;\nimport System.ArgumentOutOfRangeException;\nimport System.OverflowException;\npublic class TimeSpanIntervalProbe {\n'
                      'static void check(boolean ok, int id) { if (!ok) throw new AssertionError("case " + id); }\n'
                      'public static void main(String[] args) {\n' + '\n'.join(cases) +
                      f'\njava.lang.System.out.println("PASS TimeSpan {section}: {len(cases)} pinned vectors");\n}}\n}}\n', encoding='utf-8')
    subprocess.run(['javac', '--release', '21', '-cp', str(args.jar), '-d', str(args.work), str(source)], check=True)
    subprocess.run(['java', '-cp', str(args.jar) + ';' + str(args.work), 'TimeSpanIntervalProbe'], check=True)
    record = {
        'schemaVersion': 1, 'scope': f'TimeSpan {section}; selected pinned boundary vectors',
        'oracleEvidence': oracle_path.name, 'oracleSha256': hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
        'candidateJarSha256': hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        'casesPassed': len(cases), 'qualification': 'BOUNDED_DIFFERENTIAL_PASS; PUBLIC_QUALIFICATION_OPEN',
    }
    name = 'timespan-constructor-differential-v1.json' if args.constructors else 'timespan-interval-differential-v1.json'
    (EVIDENCE / name).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
