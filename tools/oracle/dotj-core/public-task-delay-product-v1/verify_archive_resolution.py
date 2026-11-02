"""Focused new canonical artifact contract controls; no JDK or prior mocks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import product_support as p
import verify_product as v

if __name__=='__main__':
    artifact=p.c.read(p.E/'foundation-product-candidate-v1.json');e=p.c.read(p.E/'public-task-delay-v1.json')
    chosen,mode=v.qualified_artifact(artifact,e,Path('C:/source/repos/dotj Frameworks'))
    p.c.require(p.c.sha(chosen)==e['candidateJar']['sha256'] and mode=='ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION','canonical exact archive projection, never a current C build')
    out=p.A/'archive-resolution-controls-v1';p.prepare(out);passed=['canonical-exact-archive-projection']
    for name,exists in [('D-missing-current-jar',False),('D-wrong-current-jar',True)]:
        root=out/name;root.mkdir();target=root/artifact['jarPath']
        if exists:target.parent.mkdir(parents=True);target.write_bytes(b'explicit forgery, never a JAR')
        try:v.qualified_artifact(artifact,e,root)
        except ValueError:passed.append(name)
        else:raise AssertionError('archive fallback accepted for '+name)
    p.write(out/'receipt.json',dict(status='PASS_FOCUSED_CANONICAL_ONLY_ARCHIVE_CONTRACT',actualControls=len(passed),passed=passed,
        original17Controls=p.c.descriptor(p.A/'changed-consumed-contract-controls-v1.json'),original17Rerun=False,workloadChildren=0,
        qualifiedArtifact=p.c.descriptor(chosen),artifactProvenance=mode))
    print('PASS focused canonical archive contract',len(passed))
