"""Pure finite consumer export from the adopted 308 native rows; launches nothing."""
import argparse
import base64
import hashlib
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[3]
B = Path('D:/AI/Implementation/dotj Frameworks')
NATIVE = B/'agents/batch2518-build-ordering-preparation-v1/frozen-native-contract-v3/contract.json'
NATIVE_SHA = '9beb122636b028f01dccbdf4988c517160abcfdfcf06d374fcab470c70732452'
ORDERING = HERE.parent/'condition-ordering-v1'
BOOLEAN = HERE.parent/'condition-boolean-product-v1'
RESTRICTIONS = {
    'ORD-EXPAND-unicode-left': 'UNICODE_COMPARISON',
    'ORD-EXPAND-unicode-right': 'UNICODE_COMPARISON',
    'ORD-REACH-nbsp': 'UNICODE_COMPARISON',
    'ORD-REACH-unicode-digit': 'UNICODE_COMPARISON',
    'ORD-GRAMMAR-skipped-malformed': 'CONDITION_PROFILE',
    'ORD-BOUND-group65': 'CONDITION_BOUND',
    'ORD-BOUND-node257': 'CONDITION_BOUND',
}
ERRORS = {'MSB4086': 'CONDITION_NON_NUMERIC', 'MSB4105': 'CONDITION_PROFILE',
          'MSB4092': 'CONDITION_PROFILE', 'MSB4019': 'MSB4019'}


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def enc(value):
    return base64.b64encode(value.encode('utf-8')).decode('ascii')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def relative(value, ident):
    prefix = '<fixture-root>\\'+ident+'\\'
    require(value.startswith(prefix), 'native path outside case: '+value)
    value = value[len(prefix):].replace('\\', '/')
    require(all(x not in ['', '.', '..'] for x in value.split('/')), 'relative path')
    return value


def fields(row):
    ident = row['id']
    ev = row['evaluation']
    imports = '|'.join(relative(x['owner'], ident)+'>'+relative(x['project'], ident)
                       +'@'+str(x['line'])+':'+str(x['column']) for x in ev['imports'])
    warnings, notices = [], []
    for d in row['diagnostics']:
        require(d['kind'] == 'warning', 'success diagnostic kind')
        prefix = d['code']+':'+relative(d['file'], ident)+'@'+str(d['line'])+':'+str(d['column'])
        if d['code'] == 'MSB4130':
            match = re.fullmatch(r'The condition "(.*)" may have been evaluated incorrectly in an earlier version of MSBuild\. Please verify that the order of the AND and OR clauses is written as intended\. To avoid this warning, add parentheses to make the evaluation order explicit\.', d['message'])
            require(match is not None, 'closed warning message')
            warnings.append(prefix+':'+match[1])
        else:
            require(d['code'] in ['MSB4011', 'MSB4210'], 'notice code')
            notices.append(prefix)
    return [ev['properties']['P'], ev['properties']['Q'], imports, '|'.join(warnings), '|'.join(notices)]


def boolean_bridge(records):
    result = []
    for r in records:
        result.append('\t'.join(['CASE', r['id'], r['disposition'], *r['expectedFields']]))
        result.extend('GLOBAL\t'+enc(k)+'\t'+enc(v) for k, v in r['globals'].items())
        result.append('END')
    return '\n'.join(result)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    require(out.is_relative_to(B.resolve()) and out != B.resolve() and not out.exists(), 'new D-only export')
    require(sha(NATIVE) == NATIVE_SHA, 'adopted native contract SHA')
    native = read(NATIVE)
    manifest = read(ORDERING/'manifest.json')['cases']
    rows = native['rows']
    require(len(rows) == len(manifest) == 308 and [r['id'] for r in rows] == [r['id'] for r in manifest], 'closed308 IDs/order')
    out.mkdir(parents=True)
    lines, dispositions, input_pins = [], [], []
    for row, case in zip(rows, manifest):
        ident = row['id']
        require(row['globals'] == case['globals'] and row['taskMarkerAbsent'] is True, 'globals/marker')
        require(row['profile'] == 'Default' and row['cleanup']['disposed'] is True
                and row['cleanup']['afterUnload'] == 0, 'native profile/cleanup')
        ev = row['evaluation']
        if ident in RESTRICTIONS:
            disposition, expected = 'PRIVATE_RESTRICTION', [RESTRICTIONS[ident]]
        elif ev['success']:
            disposition, expected = 'NATIVE_SUCCESS', fields(row)
        else:
            require(ev['type'] == 'Microsoft.Build.Exceptions.InvalidProjectFileException' and ev['code'] in ERRORS, 'reviewed native error mapping')
            disposition, expected = 'PRIVATE_ERROR_MAPPING', [ERRORS[ev['code']]]
        lines.append('\t'.join(['CASE', ident, disposition, *map(enc, expected)]))
        for key, value in row['globals'].items():
            lines.append('GLOBAL\t'+enc(key)+'\t'+enc(value))
        for item in case['files']:
            relative_path = Path(item['relativePath'])
            require(relative_path.parts[0] == ident and '..' not in relative_path.parts, 'manifest containment')
            src = ORDERING/'fixtures'/relative_path
            require(sha(src) == item['sha256'] and src.stat().st_size == item['sizeBytes'], 'original fixture bytes '+str(src))
            dst = out/'fixtures'/relative_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            lines.append('FILE\t'+enc(relative_path.relative_to(ident).as_posix())+'\t'+item['sha256']+'\t'+str(item['sizeBytes']))
            input_pins.append({'path': str(dst), 'sha256': item['sha256'], 'sizeBytes': item['sizeBytes']})
        lines.append('END')
        dispositions.append({'id': ident, 'disposition': disposition, 'expected': expected,
                             'nativeEvaluation': ev, 'nativeDiagnostics': row['diagnostics'],
                             'nativePairedParityEligible': disposition == 'NATIVE_SUCCESS'})
    (out/'ordering-bridge.tsv').write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    old = read(BOOLEAN/'CONTRACT.json')
    private = old['privateRecords']
    transitions = [x for x in private if x['id'] == 'BOOL-BOUND-ordering']
    witness = next(x for x in rows if x['id'] == 'ORD-HISTORY-BOOL-BOUND-ordering')
    require(len(transitions) == 1 and witness['evaluation']['success'] is True, 'sole transition witness')
    require(witness['evaluation']['properties'] == {'P': 'yes', 'Q': 'taken'}, 'observed historical result')
    transition = transitions[0]
    require(transition['disposition'] == 'PRIVATE_DESIGN_REFUSAL' and transition['expectedFields'] == ['CONDITION_PROFILE'], 'original historical restriction')
    transition.update(disposition='MATCHED_EVALUATION', expectedFields=list(map(enc, fields(witness)[:4])))
    (out/'boolean-bridge.tsv').write_text(boolean_bridge(old['nativeRecords']), encoding='utf-8', newline='\n')
    (out/'boolean-private-bridge.tsv').write_text(boolean_bridge(private), encoding='utf-8', newline='\n')
    for source, target in [(HERE.parent/'condition-boolean-v1/fixtures', 'boolean-fixtures'),
                           (HERE.parent/'condition-boolean-v1/private-fixtures', 'boolean-private-fixtures')]:
        shutil.copytree(source, out/target)
    original = out/'boolean-private-fixtures/BOOL-BOUND-ordering/main.proj'
    successor = out/'fixtures/ORD-HISTORY-BOOL-BOUND-ordering/main.proj'
    require(original.read_bytes() == successor.read_bytes(), 'historical transition exact raw fixture reuse')
    contract = {'schemaVersion': 1, 'status': 'EXPORTED_NOT_EXECUTED',
                'nativeContract': {'path': str(NATIVE), 'sha256': NATIVE_SHA},
                'rows': dispositions, 'fixtureInputs': input_pins,
                'counts': {kind: sum(r['disposition'] == kind for r in dispositions)
                           for kind in ['NATIVE_SUCCESS', 'PRIVATE_ERROR_MAPPING', 'PRIVATE_RESTRICTION']},
                'soleHistoricalTransition': {'id': transition['id'], 'observedNativeId': witness['id'],
                                             'P': 'yes', 'Q': 'taken', 'qualification': 'NOT_RUN'},
                'retainedNative297': {'success': 239, 'errorMappings': 46, 'restrictions': 9, 'faultAdaptations': 3},
                'acceptedTasksAdded': 0}
    (out/'consumer-contract.json').write_text(json.dumps(contract, indent=2, ensure_ascii=True)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': contract['status'], 'out': str(out), 'counts': contract['counts'],
                      'bridgeSha256': sha(out/'ordering-bridge.tsv')}))


if __name__ == '__main__':
    main()
