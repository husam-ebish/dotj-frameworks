"""Exercise the actual read-only predicates and a physically relocated reader/source/JAR."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile
from product import A,B,W,descriptor

def execute(run,out,receipt):
    source=Path(__file__).with_name('read_proof_final_wave.py');proof=A/'qualification-proof-final-wave-v1.json'
    jar=A/'product-build-v5/dotj-build-evaluation-candidate.jar';python=B/'toolchains/python-3.13.9/python.exe'
    receipt['inputs'] += [descriptor(p) for p in (source,proof,jar,python)]
    relocated=out/'relocated-root';shutil.copytree(W/'dotj-build/evaluation-candidate/src',relocated/'dotj-build/evaluation-candidate/src')
    relocated_reader=relocated/'reader/read_proof_final_wave.py';relocated_reader.parent.mkdir();shutil.copyfile(source,relocated_reader)
    shutil.copyfile(source.with_name('read_proof.py'),relocated_reader.with_name('read_proof.py'))
    shutil.copyfile(source.with_name('read_proof_fix1.py'),relocated_reader.with_name('read_proof_fix1.py'))
    relocated_jar=relocated/'product.jar';shutil.copyfile(jar,relocated_jar)
    def argv(reader,product,root):return [python,'-B',reader,'--proof',proof,'--sha256',descriptor(proof)['sha256'],'--jar',product,'--source-root',root]
    run('canonical-reader',argv(source,jar,W),30)
    run('relocated-reader',argv(relocated_reader,relocated_jar,relocated),30)
    wrong=out/'present-wrong.jar';wrong.write_bytes(b'present but unqualified product')
    run('wrong-jar',argv(relocated_reader,wrong,relocated),30,False)
    assert receipt['operations'][-1]['process']['exitCode']!=0
    assert 'Qualified JAR required; no fallback' in (out/'wrong-jar.stderr').read_text()
    run('missing-jar',argv(relocated_reader,out/'missing.jar',relocated),30,False)
    assert receipt['operations'][-1]['process']['exitCode']!=0
    spec=importlib.util.spec_from_file_location('actual_reader',source);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    frozen=json.loads(proof.read_text());negatives=[]
    def refused(name,operation,message):
        try:operation()
        except ValueError as error:
            assert message in str(error),(name,str(error));negatives.append(dict(name=name,status='PASS',refusal=str(error)))
        else:raise AssertionError(name+' accepted')
    execution=frozen['executions'][1];actual=json.loads(Path(execution['receipt']['path']).read_text())
    bad=copy.deepcopy(actual);bad['operations'][-1]['process']['argv'][-1]='wrong-qualified-hash'
    refused('argv',lambda:reader.execution(bad,execution['expectedOperations']),'argv mismatch')
    bad=copy.deepcopy(actual);bad['operations'][-1]['process']['timedOut']=True
    refused('timeout',lambda:reader.execution(bad,execution['expectedOperations']),'Execution failure')
    linux=frozen['executions'][2];bad=json.loads(Path(linux['receipt']['path']).read_text());bad['container']['absenceVerified']=False
    refused('cleanup',lambda:reader.execution(bad,linux['expectedOperations']),'terminal/cleanup')
    bad=json.loads(Path(linux['receipt']['path']).read_text());bad['container']['cid']='0'*64
    refused('container-identity',lambda:reader.execution(bad,linux['expectedOperations']),'Container identity')
    negative=out/'changed-source-root';shutil.copytree(relocated/'dotj-build',negative/'dotj-build')
    altered=negative/'dotj-build/evaluation-candidate/src/org/dotj/internal/build/evaluation/ItemExpressions.java'
    altered.write_bytes(altered.read_bytes()+b'\n// altered source\n')
    refused('source',lambda:reader.source(frozen,negative),'Source differs')
    embedded=out/'embedded-product-consumer.jar'
    with zipfile.ZipFile(embedded,'w') as z:z.writestr('org/dotj/internal/build/evaluation/ProjectEvaluationComponent.class',b'not a consumer')
    refused('consumer-origin',lambda:reader.consumer(embedded),'Embedded product class')
    wrong_descriptor=dict(descriptor(jar),sha256='0'*64)
    refused('artifact-hash',lambda:reader.descriptor(wrong_descriptor),'Changed evidence')
    refused('proof-hash',lambda:reader.check(proof,'0'*64,jar,W),'Proof manifest hash')
    bad_sort=json.loads(Path(frozen['rawSortRegression']['windows']['path']).read_text());bad_sort['pair'].reverse()
    refused('raw-sort-order',lambda:reader.sort_result(bad_sort,frozen['jar']['sha256']),'Raw-sort pair order')
    rows=[json.loads(line) for line in Path(frozen['finalWaveRegression']['windows']['path']).read_text().splitlines()]
    bad=copy.deepcopy(rows);bad[0]['identities'][0]='a%40\\x.cs'
    refused('escaped-prefix',lambda:reader.boundary_result(bad,frozen['jar']['sha256'],'windows'),'Escaped-prefix boundary')
    bad=copy.deepcopy(rows);bad[1]['excludeCount']=1
    refused('normalized-selector',lambda:reader.boundary_result(bad,frozen['jar']['sha256'],'windows'),'Normalized-selector boundary')
    bad=copy.deepcopy(rows);bad[2]['direct'][0]='.'
    refused('trailing-dot',lambda:reader.boundary_result(bad,frozen['jar']['sha256'],'windows'),'Trailing-dot boundary')
    result=dict(status='PASS',canonical=True,relocated=True,wrongJarRefused=True,missingJarRefused=True,negativePredicates=negatives,
        source=descriptor(source),relocatedReader=descriptor(relocated_reader),relocatedJar=descriptor(relocated_jar),proof=descriptor(proof))
    (out/'controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    receipt['outputs']=[descriptor(out/'controls.json'),descriptor(out/'canonical-reader.stdout'),descriptor(out/'relocated-reader.stdout')]
