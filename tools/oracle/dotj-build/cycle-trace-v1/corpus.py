"""Materialize the byte-frozen import corpus; no evaluator-derived expectations."""
import base64
import hashlib
import json
from pathlib import Path

PROFILES = {'DEFAULT': 'Default', 'RECORD_DUPLICATES': 'RecordDuplicateButNotCircularImports',
            'REJECT_CIRCULAR': 'RejectCircularImports'}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def descriptor(path):
    path = Path(path)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=sha(path))

def read_contract(path):
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    assert len(value['cases']) == 19 and len(value['controls']) == 14
    assert len({c['id'] for c in value['cases']}) == 19
    for case in value['cases']:
        for name, item in case['files'].items():
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
            raw = base64.b64decode(item['base64'], validate=True)
            assert len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256']
        for profile, traces in case['traces'].items():
            assert profile in PROFILES
            for trace in traces:
                nodes, edges, start = trace['nodes'], trace['edges'], trace['cycleStartIndex']
                assert 2 <= len(nodes) <= 17 and len(edges) == len(nodes)-1
                assert 0 <= start < len(nodes)-1 and nodes[start] == nodes[-1]
                assert nodes[0] == 'main.proj'
                for i, edge in enumerate(edges):
                    assert edge['owner'] == nodes[i] and edge['target'] == nodes[i+1]
                    assert edge['line'] > 0 and edge['column'] > 0
    return value

def materialize(contract, destination, ids=None):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for case in contract['cases']:
        if ids is not None and case['id'] not in ids:
            continue
        for name, item in case['files'].items():
            path = destination/case['id']/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(base64.b64decode(item['base64']))

def verify_fixtures(contract, destination, ids):
    expected = {c['id']+'/'+n: v['sha256'] for c in contract['cases'] if c['id'] in ids
                for n, v in c['files'].items()}
    actual = {p.relative_to(destination).as_posix(): sha(p)
              for p in Path(destination).rglob('*') if p.is_file()}
    assert actual == expected, 'Frozen fixture bytes/inventory differ'
