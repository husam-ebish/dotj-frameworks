"""Finding T113-EVIDENCE-I2: real same-JAR build inventory, helper + entrypoint."""
import copy,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_candidate as v
q=v.q;p=q.p;c=p.c
OUT=q.A/'fix1/source-inventory-controls-v1'
def main():
    c.require(not OUT.exists(),'fresh controls output');OUT.mkdir()
    e=c.read(p.E/'public-task-run-token-v1.json');artifact=c.read(p.E/'foundation-product-candidate-v1.json');build=e['build'];jar=e['candidateJar']
    results=[]
    chosen,mode=v.qualified_artifact(artifact,jar,p.ROOT,build);c.require(c.sha(chosen)==jar['sha256'],'real full inventory positive')
    results.append(dict(control='actual-full-build-manifest-current-source',passed=True))
    bad_jar=dict(jar,sha256='0'*64)
    try:v.qualified_artifact(artifact,bad_jar,p.ROOT,e['build'])
    except ValueError as error:c.require('same-JAR build receipt' in str(error),'same-JAR binding predicate');results.append(dict(control='wrong-qualified-JAR-build-binding',passed=True))
    else:raise AssertionError('wrong JAR binding accepted')
    task=next(x for x in artifact['productSources'] if x['path'].endswith('/Tasks/Task.java'))
    other=next(x for x in artifact['productSources'] if x['path'].endswith('/IDisposable.java'))
    variants=[]
    for label,target in [('omit-Task',task),('omit-unrelated',other)]:
        a=copy.deepcopy(artifact);a['productSources'].remove(target);variants.append((label,a))
    a=copy.deepcopy(artifact);a['productSources'].append(copy.deepcopy(task));variants.append(('duplicate',a))
    a=copy.deepcopy(artifact);duplicate=copy.deepcopy(task);duplicate['path']=duplicate['path'].replace('/Tasks/Task.java','/Tasks/../Tasks/Task.java');a['productSources'].append(duplicate);variants.append(('normalized-duplicate',a))
    a=copy.deepcopy(artifact);a['productSources'].append(dict(path='never-compiled.java',sha256='0'*64));variants.append(('extra',a))
    a=copy.deepcopy(artifact);next(x for x in a['productSources'] if x['path']==other['path'])['path']='substituted.java';variants.append(('substituted',a))
    a=copy.deepcopy(artifact);next(x for x in a['productSources'] if x['path']==task['path'])['sha256']=c.sha(Path('C:/source/repos/dotj Frameworks')/task['path']);variants.append(('refreshed-to-actual-old-C-source',a))
    for label,forged in variants:
        for route,call in [('helper',lambda:v.qualified_artifact(forged,jar,Path('C:/source/repos/dotj Frameworks'),build)),('entrypoint-validate',lambda:v.validate(e,artifact_override=forged))]:
            try:call()
            except ValueError as error:
                c.require('compiled source inventory' in str(error),'must fail relevant compiled inventory predicate: '+str(error));results.append(dict(control=label+'/'+route,passed=True,refusal=str(error)))
            else:raise AssertionError('accepted false compiled source inventory '+label+'/'+route)
    # Real trusted build + complete copied sources; only artifact presence varies.
    model=OUT/'canonical-model'
    for row in artifact['productSources']:
        dest=model/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p.ROOT/row['path'],dest)
    chosen,mode=v.qualified_artifact(artifact,jar,model,build,model);c.require(mode=='ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION','canonical absent-JAR projection')
    results.append(dict(control='complete-source-model-canonical-projection',passed=True))
    target=model/artifact['jarPath'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'wrong JAR')
    try:v.qualified_artifact(artifact,jar,model,build,model)
    except ValueError as error:c.require('present current JAR mismatches' in str(error),'present mismatch predicate');results.append(dict(control='present-canonical-wrong-JAR',passed=True))
    else:raise AssertionError('present mismatch fallback')
    target.unlink()
    try:v.qualified_artifact(artifact,jar,model,build)
    except ValueError as error:c.require('actual D/gate JAR required' in str(error),'missing D predicate');results.append(dict(control='missing-D-JAR',passed=True))
    else:raise AssertionError('missing D fallback')
    try:v.qualified_artifact(artifact,jar,Path('C:/source/repos/dotj Frameworks'),build)
    except ValueError as error:c.require('complete current product source closure' in str(error),'actual old C source negative');results.append(dict(control='actual-premerge-C-refused',passed=True))
    else:raise AssertionError('old C accepted')
    proof=dict(status='PASS',controls=results,actualNativeExecutions=0,actualJvmExecutions=0,sourceCount=len(artifact['productSources']),sameJarBuild=build,candidateJar=jar,verifier=c.descriptor(q.HERE/'verify_candidate.py'),source=c.descriptor(__file__))
    p.write(OUT/'receipt.json',proof);print('PASS compiled source inventory',len(results),'controls through helper and final validate entrypoint')
if __name__=='__main__':main()
