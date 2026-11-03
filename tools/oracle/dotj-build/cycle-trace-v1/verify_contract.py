"""Pure source/fixture freeze validation, before native or Java execution."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus import read_contract, sha

def verify(path, source_root, baseline=False):
    contract = read_contract(path)
    for item in contract['inputs']:
        p = Path(item['path'])
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], str(p)
    if baseline:
        for item in contract['baselineSources']:
            assert sha(Path(source_root)/item['relative']) == item['sha256'], item['relative']
    assert contract['nativeSchedule']['newRowPasses'] == 190
    assert sum(len(r['ids']) for r in contract['nativeSchedule']['runs']) == 190
    return contract

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--baseline', action='store_true')
    args = parser.parse_args()
    contract = verify(args.contract, args.source_root, args.baseline)
    print(json.dumps(dict(status='PASS_CONTRACT_FREEZE', graphs=len(contract['cases']),
                          controls=len(contract['controls']), newRowPasses=190, sha256=sha(args.contract))))
