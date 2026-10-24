"""Compare represented exception constructor metadata with the pinned CLR oracle."""
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
    path = EVIDENCE / 'exception-contract-v10.0.12.json'
    oracle = json.loads(path.read_text(encoding='utf-8'))
    assert oracle['runtimeVersion'] == '10.0.12'
    assert oracle['coreLibSha256'] == '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
    assert oracle['oracleSha256'] == hashlib.sha256((Path(__file__).with_name('capture-exception-contract.ps1')).read_bytes()).hexdigest()
    types = {'System.String': 'String.class', 'System.Exception': 'Exception.class', 'System.Int32': 'int.class', 'System.Object': 'Object.class'}
    cases = []
    for index, row in enumerate(oracle['constructors']):
        values = []
        for kind, value in zip(row['parameterTypes'], row['arguments']):
            if kind == 'System.Exception':
                values.append('inner' if value else 'null')
            else:
                values.append(json.dumps(value))
        signature = ','.join(types[kind] for kind in row['parameterTypes'])
        checks = [f'Exception value = (Exception) Class.forName("{row["type"]}").getConstructor(new Class<?>[]{{{signature}}}).newInstance(new Object[]{{{",".join(values)}}});',
                  f'check(value.get_HResult() == {row["hResult"]}, {index});',
                  f'check(value.get_InnerException() == {"inner" if row["innerPresent"] else "null"}, {index});']
        for key, getter in [('paramName', 'get_ParamName'), ('fileName', 'get_FileName')]:
            if key in row:
                checks.append(f'check(java.util.Objects.equals(value.getClass().getMethod("{getter}").invoke(value), {json.dumps(row[key])}), {index});')
        cases.append('{\n' + '\n'.join(checks) + '\n}')
    work = Path('D:/AI/Implementation/dotj Frameworks/verification/exception-constructors')
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'ExceptionConstructorProbe.java'
    source.write_text('import System.Exception;\npublic class ExceptionConstructorProbe {\n'
                      'static void check(boolean ok,int id) {if (!ok) throw new AssertionError("case " + id);}\n'
                      'public static void main(String[] args) throws java.lang.Exception {\n'
                      'Exception inner = new Exception("inner-value");\n' + '\n'.join(cases) +
                      f'\njava.lang.System.out.println("PASS exception constructors: {len(cases)} pinned cases");\n}}\n}}\n', encoding='utf-8')
    subprocess.run(['javac', '--release', '21', '-cp', str(args.jar), '-d', str(work), str(source)], check=True)
    subprocess.run(['java', '-cp', str(args.jar) + ';' + str(work), 'ExceptionConstructorProbe'], check=True)
    record = dict(schemaVersion=1, scope=oracle['scope'], oracleEvidence=path.name,
                  oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(), candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                  casesPassed=len(cases), qualification='BOUNDED_DIFFERENTIAL_PASS; MESSAGES_SERIALIZATION_AND_PUBLIC_QUALIFICATION_OPEN')
    (EVIDENCE / 'exception-constructor-differential-v1.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
