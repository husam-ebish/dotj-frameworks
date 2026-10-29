"""Derive selected Default-cycle comparisons from retained native observations.

No native execution or recapture: the same-profile location capture already
contains these exact inputs. Context envelopes are private comparison data,
not a native cycle-chain API. Historical producers and bridges remain intact.
"""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import runpy

ROOT = Path(r'D:\AI\Implementation\dotj Frameworks')
REPO = Path(__file__).resolve().parents[3]
BASE = REPO/'dotj-build/evaluation-candidate'
CASES = ['BI03-two-file-cycle', 'BI07-prior-cycle', 'BI08-nonroot-cycle']
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def derive(capture):
    if capture['profile'] != 'Default':
        raise ValueError('Only the selected Default profile is qualified')
    selected = [r for r in capture['rows'] if r['id'] in CASES]
    if [r['id'] for r in selected] != CASES:
        raise ValueError('Missing, duplicated or reordered cycle observation')
    rows = []
    for row in selected:
        prefix = '<fixtures>\\'+row['id']+'\\'
        def relative(path):
            if not isinstance(path, str) or not path.startswith(prefix):
                raise ValueError('Unexpected cycle path')
            value = path[len(prefix):].replace('\\', '/')
            if not value or any(p in {'', '.', '..'} for p in value.split('/')) or ':' in value:
                raise ValueError('Malformed cycle relative path')
            return value
        def coordinate(value, positive=False):
            if type(value) is not int or value < (1 if positive else 0):
                raise ValueError('Malformed cycle coordinate')
            return value
        evaluation = row['evaluation']
        if not evaluation['success'] or row['cleanup'] != {'before':0, 'loaded':1, 'afterUnload':0, 'disposed':True} or row['taskMarkerAbsent'] is not True:
            raise ValueError('Cycle success/cleanup/marker envelope changed')
        if evaluation['duplicateImports'] is not None or evaluation['duplicateGetterFailure']['type'] != 'System.InvalidOperationException':
            raise ValueError('Unexpected Default duplicate getter envelope')
        imports = {}
        for imported in evaluation['imports']:
            relative(imported['owner']); relative(imported['project'])
            coordinate(imported['line'], True); coordinate(imported['column'], True)
            if imported['project'] in imports:
                raise ValueError('Default import list must be unique')
            imports[imported['project']] = imported
        notices = []
        for warning in row['diagnostics']:
            if warning['kind'] != 'warning' or warning['code'] not in {'MSB4210', 'MSB4011'}:
                raise ValueError('Unqualified cycle diagnostic kind/code, including null')
            message = warning['message']
            if not isinstance(message, str) or not message.startswith('"'):
                raise ValueError('Missing native target/root context')
            target = message.split('"', 2)[1]
            current = {k:coordinate(warning[k], k in {'line','column'}) for k in ['line','column','endLine','endColumn']}
            previous = None
            root = None
            if warning['code'] == 'MSB4210':
                if target != prefix+'main.proj' or target in imports or not message.startswith('"'+target+'" is attempting to import itself, directly or indirectly.'):
                    raise ValueError('Mismatched root self-import context')
                root = relative(target)
            else:
                first = imports[target]
                context = 'It was already imported at "'+first['owner']+' ('+str(first['line'])+','+str(first['column'])+')".'
                if target == prefix+'main.proj' or context not in message:
                    raise ValueError('Mismatched previous-import context')
                previous = {'owner':relative(first['owner']), 'line':first['line'], 'column':first['column']}
            notices.append({'code':warning['code'], 'owner':relative(warning['file']), 'target':relative(target),
                            'current':current, 'previous':previous, 'rootContext':root})
        if len(notices) != 1:
            raise ValueError('Selected inputs require exactly one observed notice')
        rows.append({'id':row['id'], 'properties':evaluation['properties'],
                     'files':['main.proj']+[relative(i['project']) for i in evaluation['imports']], 'notices':notices})
    return rows


def bridge(rows):
    encode = lambda s:base64.b64encode(s.encode('utf-8')).decode('ascii')
    lines = []
    for row in rows:
        lines.append('\t'.join(['CASE', row['id'], encode(row['properties']['P']), encode(row['properties']['Q']), encode('\n'.join(row['files'])), str(len(row['notices']))]))
        for n in row['notices']:
            context = n['previous']
            lines.append('\t'.join(map(str, ['NOTICE', row['id'], n['code'], n['owner'], n['target'],
                *[n['current'][k] for k in ['line','column','endLine','endColumn']],
                'PREVIOUS' if context is not None else 'ROOT', context['owner'] if context is not None else n['rootContext'],
                context['line'] if context is not None else '-', context['column'] if context is not None else '-'])))
    return '\n'.join(lines)+'\n'


def require_envelope(rows, capture):
    # Exact native derivation also enforces root/previous exclusivity and absence;
    # no zero/zero previous-import position is invented for a root notice.
    if rows != derive(capture):
        raise ValueError('Cycle comparison envelope differs from native evidence')


def controls(capture):
    results = []
    def refused(name, operation):
        try: operation()
        except (ValueError, KeyError): results.append({'control':name, 'disposition':'REFUSED'})
        else: raise RuntimeError('Malformed cycle evidence accepted: '+name)
    for name, case, mutation in [
        ('null-native-code', CASES[0], lambda r:r['diagnostics'][0].update(code=None)),
        ('missing-current-end', CASES[0], lambda r:r['diagnostics'][0].pop('endColumn')),
        ('negative-current-line', CASES[2], lambda r:r['diagnostics'][0].update(line=-1)),
        ('missing-root-context', CASES[0], lambda r:r['diagnostics'][0].update(message='No root context')),
        ('mismatched-root-context', CASES[0], lambda r:r['diagnostics'][0].update(message=r['diagnostics'][0]['message'].replace('main.proj','one.props'))),
        ('mismatched-previous-context', CASES[2], lambda r:r['evaluation']['imports'][0].update(column=76)),
        ('failed-cleanup', CASES[2], lambda r:r['cleanup'].update(afterUnload=1)),
        ('task-marker-present', CASES[0], lambda r:r.update(taskMarkerAbsent=False)),
    ]:
        bad = copy.deepcopy(capture)
        mutation(next(r for r in bad['rows'] if r['id'] == case))
        refused(name, lambda:derive(bad))
    for name, index, mutation in [
        ('root-with-invented-previous', 0, lambda n:n.update(previous={'owner':'main.proj','line':0,'column':0})),
        ('root-without-root-context', 0, lambda n:n.update(rootContext=None)),
        ('root-with-mismatched-root-path', 0, lambda n:n.update(rootContext='one.props')),
        ('nonroot-without-previous', 2, lambda n:n.update(previous=None)),
        ('nonroot-with-root-context', 2, lambda n:n.update(rootContext='main.proj')),
        ('mismatched-current-envelope', 2, lambda n:n['current'].update(column=57)),
    ]:
        bad = derive(capture)
        mutation(bad[index]['notices'][0])
        refused(name, lambda:require_envelope(bad, capture))
    bad = copy.deepcopy(capture); bad['profile'] = 'RejectCircularImports'
    refused('nondefault-profile', lambda:derive(bad))
    return results


def verify_inputs():
    # Each predecessor lock continues to validate its own immutable producers,
    # inputs, raw outputs and bridges. Never edit or rebaseline those locks.
    runpy.run_path(str(Path(__file__).with_name('verify-import-locations-v1.py')))['verify_inputs']()
    lock = json.loads((BASE/'evidence/cycle-observation-lock-v1.json').read_text())
    for item in lock['inputs']:
        path = (REPO/item['path']).resolve(strict=True)
        if not path.is_relative_to(REPO) or sha(path) != item['sha256']:
            raise RuntimeError('Cycle evidence integrity mismatch: '+item['path'])
    capture = json.loads((BASE/'evidence/location-observations-v1.json').read_text())['capture']
    expected = derive(capture)
    evidence = json.loads((BASE/'evidence/cycle-comparison-v1.json').read_text())
    require_envelope(evidence['comparisons'], capture)
    if evidence['controls'] != controls(capture) or (BASE/'evidence/cycle-comparison-v1.tsv').read_text() != bridge(expected):
        raise ValueError('Cycle bridge/controls mismatch')
    return evidence


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if a.out.exists() or not a.out.resolve().is_relative_to(ROOT):
        raise RuntimeError('New private D: output required')
    observation = runpy.run_path(str(Path(__file__).with_name('verify-import-locations-v1.py')))['verify_inputs']()
    capture = observation['capture']
    comparisons = derive(capture)
    a.out.mkdir(parents=True)
    evidence = {'schemaVersion':1, 'status':'PASS_RETAINED_NATIVE_DEFAULT_CYCLES',
                'nativeRecaptureRequired':False, 'reason':'All three exact selected immutable inputs already have same-Default success, order, diagnostic coordinates/context and cleanup observations',
                'sourceObservation':{'path':'dotj-build/evaluation-candidate/evidence/location-observations-v1.json', 'sha256':sha(BASE/'evidence/location-observations-v1.json')},
                'normalization':'Existing exact fixture-root prefix only; no new native normalization',
                'contextRepresentation':'Private native-derived root-path versus previous-import-site envelope; no native full cycle-chain API is asserted',
                'comparisons':comparisons, 'controls':controls(capture)}
    (a.out/'cycle-comparison-v1.json').write_text(json.dumps(evidence, indent=2)+'\n', encoding='utf-8', newline='\n')
    (a.out/'cycle-comparison-v1.tsv').write_text(bridge(comparisons), encoding='utf-8', newline='\n')
    print('PASS 3 retained native Default cycles; 15 malformed evidence/context controls refused; no native recapture')


if __name__ == '__main__': main()
