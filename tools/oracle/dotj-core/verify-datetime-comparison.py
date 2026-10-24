"""Verify selected DateTime comparisons, equality and hash behavior across Kind values."""
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
    args = parser.parse_args()
    if args.jar is None:
        artifact = json.loads((EVIDENCE / 'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))
        args.jar = ROOT / artifact['jarPath']
    path = EVIDENCE / 'datetime-contract-v10.0.12.json'
    oracle = json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion'] == '10.0.12'
    assert oracle['coreLibSha256'] == '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256'] == hashlib.sha256(Path(__file__).with_name('capture-datetime-contract.ps1').read_bytes()).hexdigest()
    cases = []
    for index, row in enumerate(oracle['comparisons']):
        checks = [f'DateTime left = value({row["ticks"]}L, DateTimeKind.{row["kind"]});']
        if 'rightTicks' in row:
            checks.append(f'DateTime right = value({row["rightTicks"]}L, DateTimeKind.{row["rightKind"]});')
            expressions = {'compareStatic': 'DateTime.Compare(left,right)', 'compareTyped': 'left.CompareTo(right)',
                           'compareObject': '((IComparable)left).CompareTo(right)', 'equalsStatic': 'DateTime.Equals(left,right)',
                           'equalsTyped': 'left.Equals(right)', 'equalsObject': 'left.Equals((Object)right)'}
            for key, expression in expressions.items():
                expected = str(row[key]).lower() if isinstance(row[key], bool) else str(row[key])
                checks.append(f'check({expression} == {expected}, {index});')
            checks += [f'check(left.GetHashCode() == {row["hash"]} && left.hashCode() == {row["hash"]}, {index});',
                       f'check(left.equals(right) == {str(row["equalsObject"]).lower()}, {index});']
        else:
            value = {'Null': 'null', 'Int32': 'Integer.valueOf(0)', 'String': '"wrong"', 'Object': 'new Object()'}[row['objectKind']]
            expression = f'left.{row["operation"]}((Object){value})'
            result = row['result']
            if 'exception' in result:
                checks.append(f'''try {{ {expression}; throw new AssertionError("missing exception {index}"); }}
catch (ArgumentException expected) {{
check(expected.getClass().getName().equals("{result['exception']}"), {index});
check(expected.get_HResult() == {result['hResult']}, {index});
check(java.util.Objects.equals(expected.get_ParamName(), {json.dumps(result['paramName'])}), {index});
}}''')
            else:
                expected = str(result['boolean']).lower() if 'boolean' in result else str(result['value'])
                checks.append(f'check({expression} == {expected}, {index});')
        cases.append('{\n' + '\n'.join(checks) + '\n}')
    methods = ['static void group' + str(offset//30) + '() {\n' + '\n'.join(cases[offset:offset+30]) + '\n}' for offset in range(0,len(cases),30)]
    work = Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-comparison')
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'DateTimeComparisonProbe.java'
    source.write_text('import System.DateTime;\nimport System.DateTimeKind;\nimport System.IComparable;\nimport System.ArgumentException;\n'
                      'public class DateTimeComparisonProbe {\n'
                      'static DateTime value(long ticks, DateTimeKind kind) { return DateTime.SpecifyKind(new DateTime(1,1,1).AddTicks(ticks),kind); }\n'
                      'static void check(boolean ok,int id) {if(!ok) throw new AssertionError("case " + id);}\n' + '\n'.join(methods) +
                      '\npublic static void main(String[] args) {\n' + '\n'.join(f'group{index}();' for index in range(len(methods))) +
                      f'\njava.lang.System.out.println("PASS DateTime comparisons: {len(cases)} pinned cases");\n}}\n}}\n', encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DateTimeComparisonProbe'],check=True)
    record = dict(schemaVersion=1,scope='DateTime selected kind-independent comparison, equality and hashing',oracleEvidence=path.name,
                  oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                  casesPassed=len(cases),qualification='BOUNDED_DIFFERENTIAL_PASS; PUBLIC_QUALIFICATION_OPEN')
    (EVIDENCE/'datetime-comparison-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
