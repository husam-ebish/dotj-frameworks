"""Differentially test selected TimeSpan contract vectors against a JAR."""
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
    kinds = parser.add_mutually_exclusive_group()
    kinds.add_argument('--constructors', action='store_true')
    kinds.add_argument('--arithmetic', action='store_true')
    kinds.add_argument('--properties', action='store_true')
    kinds.add_argument('--constants', action='store_true')
    kinds.add_argument('--integer-factories', action='store_true')
    kinds.add_argument('--composite-factories', action='store_true')
    kinds.add_argument('--comparison', action='store_true')
    kinds.add_argument('--checked-arithmetic', action='store_true')
    kinds.add_argument('--formats', action='store_true')
    kinds.add_argument('--custom-formats', action='store_true')
    kinds.add_argument('--parsing', action='store_true')
    kinds.add_argument('--char-formatting', action='store_true')
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
    section = ('charFormatting' if args.char_formatting else 'parsing' if args.parsing else 'customFormats' if args.custom_formats else 'formats' if args.formats else 'checkedArithmetic' if args.checked_arithmetic else 'comparisons' if args.comparison else 'compositeFactories' if args.composite_factories else 'integerFactories' if args.integer_factories else 'constants' if args.constants else 'properties' if args.properties else 'arithmetic' if args.arithmetic else
               'constructors' if args.constructors else 'factories')
    vectors = oracle['operations'] + oracle['ratios'] if args.arithmetic else oracle[section]
    for index, case in enumerate(vectors):
        if args.comparison and 'rightTicks' in case:
            checks = [f'TimeSpan left = TimeSpan.FromTicks({case["ticks"]}L);',
                      f'TimeSpan right = TimeSpan.FromTicks({case["rightTicks"]}L);']
            expressions = {
                'compareStatic': 'TimeSpan.Compare(left, right)', 'compareTyped': 'left.CompareTo(right)',
                'compareObject': 'left.CompareTo((java.lang.Object) right)',
                'equalsStatic': 'TimeSpan.Equals(left, right)', 'equalsTyped': 'left.Equals(right)',
                'equalsObject': 'left.Equals((java.lang.Object) right)',
            }
            for key, expression in expressions.items():
                expected = str(case[key]).lower() if isinstance(case[key], bool) else str(case[key])
                checks.append(f'check({expression} == {expected}, {index});')
            checks += [f'check(left.GetHashCode() == {case["hash"]}L && left.hashCode() == {case["hash"]}L, {index});',
                       f'check(left.equals(right) == {str(case["equalsObject"]).lower()}, {index});']
            cases.append('{\n' + '\n'.join(checks) + '\n}')
            continue
        if args.char_formatting:
            expression = f'((ISpanFormattable) TimeSpan.FromTicks({case["ticks"]}L)).TryFormat(buffer, written, {json.dumps(case["format"])}, null)'
        elif args.parsing:
            expression = f'TimeSpan.Parse({json.dumps(case["input"])})'
        elif args.formats or args.custom_formats:
            arguments = json.dumps(case['format']) + (', null' if args.custom_formats or case['withProvider'] else '')
            expression = f"TimeSpan.FromTicks({case['ticks']}L).ToString({arguments})"
        elif args.checked_arithmetic:
            operand = f"TimeSpan.FromTicks({case['operandTicks']}L)" if 'operandTicks' in case else ''
            expression = f"TimeSpan.FromTicks({case['ticks']}L).{case['method']}({operand})"
        elif args.comparison:
            value = {'Null': 'null', 'Int32': 'Integer.valueOf(0)', 'String': '"wrong"', 'Object': 'new java.lang.Object()'}[case['objectKind']]
            expression = f"TimeSpan.FromTicks({case['ticks']}L).{case['operation']}((java.lang.Object) {value})"
        elif args.composite_factories:
            arguments = ', '.join(str(value) + ('' if kind == 'System.Int32' else 'L')
                                  for value, kind in zip(case['values'], case['parameterTypes']))
            expression = f"TimeSpan.{case['method']}({arguments})"
        elif args.integer_factories:
            suffix = '' if case['inputType'] == 'System.Int32' else 'L'
            expression = f"TimeSpan.{case['method']}({case['value']}{suffix})"
        elif args.constants:
            expression = f"TimeSpan.{case['name']}"
        elif args.properties:
            expression = f"TimeSpan.FromTicks({case['ticks']}L).get_{case['property']}()"
        elif args.arithmetic:
            operand = (f"TimeSpan.FromTicks({case['divisorTicks']}L)" if 'divisorTicks' in case
                       else f"Double.longBitsToDouble(0x{case['operandBits']}L)")
            expression = f"TimeSpan.FromTicks({case['ticks']}L).{case['method']}({operand})"
        elif args.constructors:
            expression = 'new TimeSpan(' + ','.join(str(value) for value in case['components']) + ')'
        else:
            expression = f"TimeSpan.{case['method']}(Double.longBitsToDouble(0x{case['inputBits']}L))"
        result = case['result']
        if 'text' in result:
            cases.append(f'check({expression}.equals({json.dumps(result["text"])}), {index});')
            if args.formats and case['withProvider']:
                cases[-1] += (f'\ncheck(((IFormattable) TimeSpan.FromTicks({case["ticks"]}L)).ToString('
                              f'{json.dumps(case["format"])}, type -> {{ throw new AssertionError("constant provider queried"); }})'
                              f'.equals({json.dumps(result["text"])}), {index});')
        elif 'boolean' in result:
            cases.append(f'check({expression} == {str(result["boolean"]).lower()}, {index});')
        elif 'bits' in result:
            predicate = f'Double.isNaN({expression})' if result['isNaN'] else f'Double.doubleToRawLongBits({expression}) == 0x{result["bits"]}L'
            cases.append(f'check({predicate}, {index});')
        elif 'value' in result:
            cases.append(f'check({expression} == {result["value"]}L, {index});')
        elif 'ticks' in result:
            cases.append(f'check({expression}.get_Ticks() == {result["ticks"]}L, {index});')
        else:
            parameter = 'null' if result['paramName'] is None else json.dumps(result['paramName'])
            cases.append(f'''try {{ {expression}; throw new AssertionError("missing exception {index}"); }}
                catch ({result['exception'].split('.')[-1]} expected) {{
                    check(expected.getClass().getName().equals("{result['exception']}"), {index});
                    check(expected.get_HResult() == {result['hResult']}, {index});
                    {'check(java.util.Objects.equals(expected.get_ParamName(), ' + parameter + '), ' + str(index) + ');' if result['exception'] in ('System.ArgumentException', 'System.ArgumentOutOfRangeException', 'System.ArgumentNullException') else ''}
                }}''')
        if args.constants:
            field_type = {'System.Int64': 'long.class', 'System.Int32': 'int.class', 'System.TimeSpan': 'TimeSpan.class'}[case['type']]
            cases[-1] = (f'check(TimeSpan.class.getField("{case["name"]}").getType() == {field_type}, {index});\n'
                         f'check(java.lang.reflect.Modifier.isStatic(TimeSpan.class.getField("{case["name"]}").getModifiers()) && '
                         f'java.lang.reflect.Modifier.isFinal(TimeSpan.class.getField("{case["name"]}").getModifiers()), {index});\n' + cases[-1])
        if args.integer_factories:
            parameter_type = 'int.class' if case['inputType'] == 'System.Int32' else 'long.class'
            cases[-1] = f'check(TimeSpan.class.getMethod("{case["method"]}", {parameter_type}).getReturnType() == TimeSpan.class, {index});\n' + cases[-1]
        if args.composite_factories:
            parameter_types = ', '.join('int.class' if kind == 'System.Int32' else 'long.class' for kind in case['parameterTypes'])
            cases[-1] = f'check(TimeSpan.class.getMethod("{case["method"]}", {parameter_types}).getReturnType() == TimeSpan.class, {index});\n' + cases[-1]
        if args.parsing:
            cases[-1] = ('{\n' + cases[-1] + '\nTimeSpan[] output = {TimeSpan.FromTicks(99L)};\n' +
                         f'check(TimeSpan.TryParse({json.dumps(case["input"])}, output) == {str(case["trySuccess"]).lower()}, {index});\n' +
                         f'check(output[0].get_Ticks() == {case["tryTicks"]}L, {index});\n}}')
        if args.char_formatting:
            cases[-1] = ('{\n' + f'char[] buffer = new char[{case["capacity"]}]; java.util.Arrays.fill(buffer, \'#\'); int[] written = {{99}};\n' +
                         cases[-1] + f'\ncheck(written[0] == {case["written"]}, {index});\n' +
                         f'check(new String(buffer).equals({json.dumps(case["buffer"])}), {index});\n}}')
    if args.constants:
        cases.append(f'check(new TimeSpan().get_Ticks() == {oracle["defaultValueTicks"]}L, {len(cases)});')
        cases.append(f'check(TimeSpan.class.getFields().length == {len(vectors)}, {len(cases)});')
    args.work = args.work / section
    args.work.mkdir(parents=True, exist_ok=True)
    source = args.work / 'TimeSpanIntervalProbe.java'
    # Keep independent blocks in small methods so larger oracle sets cannot exceed JVM method limits.
    methods = ['static void group' + str(offset // 40) + '() throws java.lang.Exception {\n' +
               '\n'.join(cases[offset:offset + 40]) + '\n}\n' for offset in range(0, len(cases), 40)]
    source.write_text('import System.TimeSpan;\nimport System.IFormattable;\nimport System.ISpanFormattable;\nimport System.ArgumentException;\nimport System.ArgumentNullException;\nimport System.ArgumentOutOfRangeException;\nimport System.OverflowException;\nimport System.FormatException;\npublic class TimeSpanIntervalProbe {\n'
                      'static void check(boolean ok, int id) { if (!ok) throw new AssertionError("case " + id); }\n'
                      + ''.join(methods) + 'public static void main(String[] args) throws java.lang.Exception {\n' +
                      '\n'.join(f'group{index}();' for index in range(len(methods))) +
                      f'\njava.lang.System.out.println("PASS TimeSpan {section}: {len(cases)} pinned vectors");\n}}\n}}\n', encoding='utf-8')
    subprocess.run(['javac', '--release', '21', '-cp', str(args.jar), '-d', str(args.work), str(source)], check=True)
    subprocess.run(['java', '-cp', str(args.jar) + ';' + str(args.work), 'TimeSpanIntervalProbe'], check=True)
    record = {
        'schemaVersion': 1, 'scope': f'TimeSpan {section}; selected pinned boundary vectors',
        'oracleEvidence': oracle_path.name, 'oracleSha256': hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
        'candidateJarSha256': hashlib.sha256(args.jar.read_bytes()).hexdigest(),
        'casesPassed': len(cases), 'qualification': 'BOUNDED_DIFFERENTIAL_PASS; PUBLIC_QUALIFICATION_OPEN',
    }
    name = ('timespan-char-format-differential-v1.json' if args.char_formatting else
            'timespan-parse-differential-v1.json' if args.parsing else
            'timespan-custom-format-differential-v1.json' if args.custom_formats else
            'timespan-format-differential-v1.json' if args.formats else
            'timespan-checked-arithmetic-differential-v1.json' if args.checked_arithmetic else
            'timespan-comparison-differential-v1.json' if args.comparison else
            'timespan-composite-factory-differential-v1.json' if args.composite_factories else
            'timespan-integer-factory-differential-v1.json' if args.integer_factories else
            'timespan-constant-differential-v1.json' if args.constants else
            'timespan-property-differential-v1.json' if args.properties else
            'timespan-arithmetic-differential-v1.json' if args.arithmetic else
            'timespan-constructor-differential-v1.json' if args.constructors else 'timespan-interval-differential-v1.json')
    (EVIDENCE / name).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
