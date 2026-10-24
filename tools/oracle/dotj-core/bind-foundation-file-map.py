"""Bind an unchanged reviewed class inventory to a newly verified candidate JAR.

This updates the artifact hash only. Any source/class/notice inventory change
requires an explicit map change; no rights or release decision is modified.
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / 'planning/stage-2/repos/dotj-core/evidence'


def main():
    artifact = json.loads((EVIDENCE / 'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))
    path = EVIDENCE / 'foundation-file-notice-map-v1.json'
    raw = path.read_bytes()
    mapping = json.loads(raw)
    jar = ROOT / artifact['jarPath']
    digest = hashlib.sha256(jar.read_bytes()).hexdigest()
    assert digest == artifact['jarSha256']
    sources = {entry['path']: entry['sha256'] for entry in artifact['productSources']}
    assert set(sources) == set(mapping['sourceToClasses']), 'Source inventory changed; review the map explicitly'
    for source, expected in sources.items():
        assert hashlib.sha256((ROOT / source).read_bytes()).hexdigest() == expected
        stem = source.split('/src/main/java/', 1)[1].removesuffix('.java')
        expected_classes = {name for name in artifact['classSha256'] if name == stem + '.class' or name.startswith(stem + '$')}
        assert set(mapping['sourceToClasses'][source]) == expected_classes, source
    mapped = [name for names in mapping['sourceToClasses'].values() for name in names]
    assert len(mapped) == len(set(mapped))
    assert set(mapped) == set(artifact['classSha256'])
    with zipfile.ZipFile(jar) as archive:
        assert archive.namelist() == artifact['jarEntries']
        assert archive.namelist() == [mapping['manifestEntry'], mapping['productLicenseEntry'], *sorted(mapped)]
        assert archive.read(mapping['productLicenseEntry']) == (ROOT / mapping['productLicensePath']).read_bytes()
        for name, expected in artifact['classSha256'].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == expected
        notices = [name for name in archive.namelist() if 'LICENSE' in name.upper() or 'NOTICE' in name.upper()]
        assert notices == mapping['jarNoticeEntries']
    old = mapping['jarSha256'].encode('ascii')
    assert raw.count(old) == 1
    path.write_bytes(raw.replace(old, digest.encode('ascii')))
    print('PASS foundation map artifact binding: source/class/notice inventory unchanged; decisions preserved')


if __name__ == '__main__':
    main()
