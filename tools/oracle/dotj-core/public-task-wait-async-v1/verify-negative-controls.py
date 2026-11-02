"""Owned consumed-predicate controls through helper and full selected entrypoint."""
import copy,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_candidate as v
q=v.q;p=v.p;c=v.c
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else q.A/'negative-controls-v3'
def main():
    c.confined(OUT)
    c.require(not OUT.exists(),'fresh negative output');OUT.mkdir();e=c.read(p.E/'public-task-wait-async-v1.json');artifact=c.read(p.E/'foundation-product-candidate-v1.json');jar=e['candidateJar'];results=[]
    def passed(name):results.append(dict(control=name,passed=True))
    def refuses(name,call,reason):
        try:call()
        except (ValueError,KeyError,FileNotFoundError) as error:
            c.require(reason in str(error),'relevant refusal '+name+': '+str(error));results.append(dict(control=name,passed=True,refusal=str(error)))
        else:raise AssertionError('accepted false predicate '+name)
    v.validate(e);passed('full-real-positive')
    task=next(row for row in artifact['productSources'] if row['path'].endswith('/Tasks/Task.java'));other=next(row for row in artifact['productSources'] if row['path'].endswith('/IDisposable.java'))
    variants=[]
    for label,row in [('missing-Task',task),('missing-unrelated',other)]:
        a=copy.deepcopy(artifact);a['productSources'].remove(row);variants.append((label,a))
    a=copy.deepcopy(artifact);a['productSources'].append(dict(task));variants.append(('duplicate',a))
    a=copy.deepcopy(artifact);a['productSources'].append(dict(task,path=task['path'].replace('/Tasks/Task.java','/Tasks/../Tasks/Task.java')));variants.append(('normalized-duplicate',a))
    a=copy.deepcopy(artifact);a['productSources'].append(dict(path='never-compiled.java',sha256='0'*64));variants.append(('extra',a))
    a=copy.deepcopy(artifact);next(row for row in a['productSources'] if row['path']==other['path'])['path']='substituted.java';variants.append(('substituted',a))
    a=copy.deepcopy(artifact);next(row for row in a['productSources'] if row['path']==task['path'])['sha256']=c.sha(Path('C:/source/repos/dotj Frameworks')/task['path']);variants.append(('refreshed-uncompiled-old-C-source',a))
    for label,a in variants:
        refuses(label+'/helper',lambda a=a:v.qualified_artifact(a,jar,p.ROOT,e['build']),'compiled source inventory')
        refuses(label+'/entrypoint',lambda a=a:v.validate(e,artifact_override=a),'compiled source inventory')
    wrong=dict(jar,sha256='0'*64);refuses('wrong-JAR/helper',lambda:v.qualified_artifact(artifact,wrong,p.ROOT,e['build']),'same final JAR');bad=copy.deepcopy(e);bad['candidateJar']=wrong;refuses('wrong-JAR/entrypoint',lambda:v.validate(bad),'stale input')
    model=OUT/'source-model'
    for row in artifact['productSources']:
        target=model/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p.ROOT/row['path'],target)
    selected,mode=v.qualified_artifact(artifact,jar,model,e['build'],model);c.require(mode=='ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION' and c.sha(selected)==jar['sha256'],'real complete source projection');passed('absent-C-JAR/helper')
    v.validate(e,source_root=model,canonical_root=model);passed('absent-C-JAR/entrypoint')
    target=model/artifact['jarPath'];target.parent.mkdir(parents=True);target.write_bytes(b'present wrong canonical JAR')
    refuses('present-wrong-C-JAR/helper',lambda:v.qualified_artifact(artifact,jar,model,e['build'],model),'present current JAR mismatches')
    refuses('present-wrong-C-JAR/entrypoint',lambda:v.validate(e,source_root=model,canonical_root=model),'present current JAR mismatches')
    # Remove only this explicitly created wrong-JAR control file; model sources remain.
    target.unlink()
    refuses('missing-D-JAR/helper',lambda:v.qualified_artifact(artifact,jar,model,e['build']),'actual D/gate JAR required')
    refuses('missing-D-JAR/entrypoint',lambda:v.validate(e,source_root=model),'actual D/gate JAR required')
    refuses('actual-premerge-C-source',lambda:v.qualified_artifact(artifact,jar,Path('C:/source/repos/dotj Frameworks'),e['build']),'complete current product source closure')
    build=c.read(e['build']['path']);rec=build['commands'][0]
    mutations=[('unlaunched','launched',False,'failed actual child'),('typed-exit','exitCode','0','failed actual child'),('job-not-assigned','jobAssigned',False,'failed actual child'),('not-resumed','resumed',False,'failed actual child'),('timeout','timedOut',True,'failed actual child'),('output-limit','outputLimitExceeded',True,'failed actual child'),('stale-admission','resourceSampleAgeSeconds',3,'fresh physical/commit'),('cleanup-bound','cleanupSeconds',6,'cleanup/output'),('timeout-budget','timeoutSeconds',1,'fixed child/output')]
    for label,key,value,reason in mutations:
        forged=copy.deepcopy(rec);forged[key]=value
        refuses(label+'/helper',lambda forged=forged:v.command(forged),reason)
        changed=copy.deepcopy(build);changed['commands'][0]=forged;path=OUT/(label+'.json');p.write(path,changed);bad=copy.deepcopy(e);bad['build']=c.descriptor(path)
        refuses(label+'/entrypoint',lambda bad=bad:v.validate(bad),reason)
    forged=copy.deepcopy(rec);forged['environment']['TEMP']='C:/forbidden';refuses('D-environment/helper',lambda:v.command(forged),'exact explicit D environment')
    changed=copy.deepcopy(build);changed['commands'][0]=forged;path=OUT/'environment.json';p.write(path,changed);bad=copy.deepcopy(e);bad['build']=c.descriptor(path);refuses('D-environment/entrypoint',lambda:v.validate(bad),'exact explicit D environment')
    for label,mutation,reason in [('source-argv',lambda r:r['commands'][0]['argv'].append('uncompiled.java'),'compiled source inventory exact actual compiler argv'),('raw-path',lambda r:r['commands'][0].update(stdoutPath='D:/wrong.stdout'),'complete actual stream'),('stream-size',lambda r:r['commands'][0]['outputSizesBytes'].update(stdout=-1),'complete actual stream')]:
        changed=copy.deepcopy(build);mutation(changed);path=OUT/(label+'.json');p.write(path,changed);bad=copy.deepcopy(e);bad['build']=c.descriptor(path);refuses(label+'/entrypoint',lambda bad=bad:v.validate(bad),reason)
    proof=dict(status='PASS',controls=results,source=c.descriptor(__file__),reader=c.descriptor(Path(v.__file__)),candidateJar=jar,sourceCount=len(artifact['productSources']),actualNativeExecutions=0,actualJvmExecutions=0,scope='Pure mutations of exact owned metadata, helper and final selected validation; no recursive old producer replay')
    p.write(OUT/'receipt.json',proof);print('PASS',len(results),'source/artifact/consumed-predicate controls')
if __name__=='__main__':main()
