"""Bind every selected differential record to its immutable native oracle file."""
import hashlib,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'

def validate(record,root):
    name=record['oracleEvidence']
    assert isinstance(name,str) and Path(name).name==name and Path(name).suffix=='.json','oracle must name a local JSON fixture'
    path=(root/name).resolve()
    assert path.parent==root.resolve() and path.is_file(),'oracle fixture missing or outside evidence root'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==record['oracleSha256'],'oracle SHA-256 mismatch'
    return digest

def controls():
    base=Path('D:/AI/Implementation/dotj Frameworks/verification/oracle-provenance-controls');base.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=base) as folder:
        root=Path(folder);fixture=root/'reference.json';fixture.write_text('{"native":true}\n',encoding='utf-8')
        valid=dict(oracleEvidence=fixture.name,oracleSha256=hashlib.sha256(fixture.read_bytes()).hexdigest())
        validate(valid,root)
        invalid=[dict(valid,oracleEvidence='BadByteFormat.java'),dict(valid,oracleEvidence='missing.json'),dict(valid,oracleSha256='0'*64),dict(valid,oracleEvidence='../reference.json')]
        for record in invalid:
            try:validate(record,root)
            except AssertionError:continue
            raise AssertionError('corrupted provenance control was accepted')
    return 5

def main():
    count=controls();rows=[]
    for path in sorted(EVIDENCE.glob('*-differential-v1.json')):
        record=json.loads(path.read_text(encoding='utf-8-sig'))
        if 'oracleEvidence' not in record:continue
        digest=validate(record,EVIDENCE)
        rows.append(dict(differential=path.name,oracle=record['oracleEvidence'],oracleSha256=digest))
    assert len(rows)>=113,'selected provenance record coverage unexpectedly shrank'
    result=dict(schemaVersion=1,recordsBound=len(rows),controlGroupsPassed=count,records=rows,qualification='BOUNDED_DIFFERENTIAL_ORACLE_BINDING_PASS; FIXTURE_COVERAGE_API_AND_RELEASE_QUALIFICATION_OPEN')
    (EVIDENCE/'differential-oracle-provenance-v1.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'PASS differential oracle provenance: {len(rows)} bindings; {count} integrity controls')
if __name__=='__main__':main()
