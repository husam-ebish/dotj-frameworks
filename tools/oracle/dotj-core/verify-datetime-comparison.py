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
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--tick-domain', action='store_true')
    modes.add_argument('--component-constructors', action='store_true')
    modes.add_argument('--calendar-properties', action='store_true')
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
    for index, row in enumerate([] if args.tick_domain or args.component_constructors or args.calendar_properties else oracle['comparisons']):
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
    if args.tick_domain or args.component_constructors:
        vectors = oracle['componentConstructors'] if args.component_constructors else oracle['tickConstructors']
        for index, row in enumerate(vectors):
            parameters = (','.join(str(value) for value in row['components']) if args.component_constructors else str(row['ticks']) + 'L')
            parameters += '' if row['kind'] is None else ', DateTimeKind.' + row['kind']
            expression = f'new DateTime({parameters})'
            result = row['result']
            if 'ticks' in result:
                cases.append(f'{{ DateTime value = {expression}; check(value.get_Ticks() == {result["ticks"]}L && value.get_Kind() == DateTimeKind.{result["kind"]}, {index}); }}')
            else:
                cases.append(f'''try {{ {expression}; throw new AssertionError("missing exception {index}"); }}
catch (ArgumentOutOfRangeException expected) {{
check(expected.getClass().getName().equals("{result['exception']}"), {index});
check(expected.get_HResult() == {result['hResult']}, {index});
check(java.util.Objects.equals(expected.get_ParamName(), {json.dumps(result['paramName'])}), {index});
}}''')
        for row in [] if args.component_constructors else oracle['constants']:
            assert row['type'] == 'System.DateTime' and row['isInitOnly']
            index = len(cases)
            cases.append(f'''check(DateTime.{row['name']}.get_Ticks() == {row['ticks']}L && DateTime.{row['name']}.get_Kind() == DateTimeKind.{row['kind']}, {index});
check(DateTime.class.getField("{row['name']}").getType() == DateTime.class, {index});
check(java.lang.reflect.Modifier.isStatic(DateTime.class.getField("{row['name']}").getModifiers()) && java.lang.reflect.Modifier.isFinal(DateTime.class.getField("{row['name']}").getModifiers()), {index});''')
        if args.tick_domain:
            default = oracle['defaultValue']
            cases.append(f'check(new DateTime().get_Ticks() == {default["ticks"]}L && new DateTime().get_Kind() == DateTimeKind.{default["kind"]}, {len(cases)});')
            cases.append(f'check(DateTime.class.getFields().length == {len(oracle["constants"])}, {len(cases)});')
    if args.calendar_properties:
        for index,row in enumerate(oracle['calendarProperties']):
            cases.append(f'''{{ DateTime value = value({row['ticks']}L,DateTimeKind.{row['kind']});
check(value.get_DayOfWeek() == DayOfWeek.{row['dayOfWeek']} && value.get_DayOfWeek().ordinal() == {row['dayOfWeekValue']}, {index});
check(value.get_Date().get_Ticks() == {row['dateTicks']}L && value.get_Date().get_Kind() == DateTimeKind.{row['dateKind']}, {index});
check(value.get_TimeOfDay().get_Ticks() == {row['timeOfDayTicks']}L, {index});
check(value.get_Date().get_Ticks() + value.get_TimeOfDay().get_Ticks() == value.get_Ticks(), {index}); }}''')
        for row in oracle['enums']:
            index=len(cases)
            checks=[f'Type type=Type.GetType("{row["name"]}");',
                    f'check(type != null && type.get_IsEnum() && type.get_IsValueType(), {index});',
                    f'check(type.get_BaseType().get_FullName().equals("System.Enum") && type.GetEnumUnderlyingType().get_FullName().equals("{row["underlyingType"]}"), {index});',
                    f'check(java.util.Arrays.equals(type.GetEnumNames(), new String[]{{{",".join(json.dumps(name) for name in row["names"])}}}), {index});',
                    f'check(java.util.Arrays.equals(type.GetEnumValuesAsUnderlyingType(), new int[]{{{",".join(str(value) for value in row["values"])}}}), {index});',
                    f'check(java.util.Arrays.equals(type.GetEnumValues(), {row["name"].split(".")[-1]}.values()), {index});',
                    f'check(Type.GetType("{row["name"].lower()}",false,true) == type && Type.GetType("{row["name"].lower()}") == null, {index});',
                    f'String[] names = type.GetEnumNames(); names[0]="mutated"; check(type.GetEnumNames()[0].equals("{row["names"][0]}"), {index});']
            for query in row['queries']:
                checks += [f'check(type.IsEnumDefined(Integer.valueOf({query["value"]})) == {str(query["defined"]).lower()}, {index});',
                           f'check(java.util.Objects.equals(type.GetEnumName(Integer.valueOf({query["value"]})), {json.dumps(query["name"])}), {index});']
            cases.append('{\n'+'\n'.join(checks)+'\n}')
    methods = ['static void group' + str(offset//30) + '() throws java.lang.Exception {\n' + '\n'.join(cases[offset:offset+30]) + '\n}' for offset in range(0,len(cases),30)]
    section = 'calendar-properties' if args.calendar_properties else 'component-constructors' if args.component_constructors else 'tick-domain' if args.tick_domain else 'comparison'
    work = Path('D:/AI/Implementation/dotj Frameworks/verification/datetime-' + section)
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'DateTimeComparisonProbe.java'
    source.write_text('import System.DateTime;\nimport System.DateTimeKind;\nimport System.DayOfWeek;\nimport System.Type;\nimport System.IComparable;\nimport System.ArgumentException;\nimport System.ArgumentOutOfRangeException;\n'
                      'public class DateTimeComparisonProbe {\n'
                      'static DateTime value(long ticks, DateTimeKind kind) { return DateTime.SpecifyKind(new DateTime(1,1,1).AddTicks(ticks),kind); }\n'
                      'static void check(boolean ok,int id) {if(!ok) throw new AssertionError("case " + id);}\n' + '\n'.join(methods) +
                      '\npublic static void main(String[] args) throws java.lang.Exception {\n' + '\n'.join(f'group{index}();' for index in range(len(methods))) +
                      f'\njava.lang.System.out.println("PASS DateTime {section}: {len(cases)} pinned cases");\n}}\n}}\n', encoding='utf-8')
    subprocess.run(['javac','--release','21','-cp',str(args.jar),'-d',str(work),str(source)],check=True)
    subprocess.run(['java','-cp',str(args.jar)+';'+str(work),'DateTimeComparisonProbe'],check=True)
    record = dict(schemaVersion=1,scope='DateTime selected ' + section,oracleEvidence=path.name,
                  oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(args.jar.read_bytes()).hexdigest(),
                  casesPassed=len(cases),qualification='BOUNDED_DIFFERENTIAL_PASS; PUBLIC_QUALIFICATION_OPEN')
    name = 'datetime-calendar-property-differential-v1.json' if args.calendar_properties else 'datetime-component-constructor-differential-v1.json' if args.component_constructors else 'datetime-tick-domain-differential-v1.json' if args.tick_domain else 'datetime-comparison-differential-v1.json'
    (EVIDENCE/name).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
