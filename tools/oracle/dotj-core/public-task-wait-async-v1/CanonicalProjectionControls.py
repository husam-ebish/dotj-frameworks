"""Finite pure controls of the real relocated proof reader and retained execution paths."""
import copy,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_candidate as v
q=v.q;p=v.p;c=v.c

def main():
    out=Path(sys.argv[1]);c.confined(out);c.require(not out.exists(),'fresh relocation controls');out.mkdir()
    e=c.read(p.E/'public-task-wait-async-v1.json');artifact=c.read(p.E/'foundation-product-candidate-v1.json');jar=e['candidateJar'];rows=[]
    def mark(name):rows.append(dict(name=name,passed=True))
    def refused(name,call,reason=None):
        try:call()
        except (ValueError,FileNotFoundError,KeyError) as error:
            if reason:c.require(reason in str(error),'relevant refusal '+name+': '+str(error))
            rows.append(dict(name=name,passed=True,refusal=str(error)));return
        raise AssertionError('accepted counterfeit projection '+name)
    history=c.read(e['historicalPhases'][0]['receipt']['path']);delay=next(group for group in history['groups'] if group['name']=='delay');only=copy.deepcopy(history);only['groups']=[copy.deepcopy(delay)]
    executed=Path(v.executed_delay_case_input(history));c.require(executed.parent!=p.HERE and p.ROOT!=v.COMPILED_ROOT,'genuine relocated imported reader')
    v.groups(only);mark('relocated-reader-accepts-real-Delay-argv')
    pins=[e[key] for key in ['paired','private','sample']]+[item['receipt'] for item in e['historicalPhases']]+[item['paired'] for item in e['supplements']]+[e['observationCorrection'][key] for key in ['paired','controls']]+[e['finalWave'][key] for key in ['depthPaired','depthControls']]
    for pin in pins:c.validate_pin(pin);v.groups(c.read(pin['path']))
    mark('all-retained-consumer-command-projections-accepted')
    retained=c.read(history['retainedDelayPaired']['path']);case=next(pin for pin in retained['inputs'] if Path(pin['path']).name=='case-inputs.tsv');c.require(c.sha(executed)==case['sha256'] and executed.stat().st_size==case['sizeBytes'],'actual executed table/version bytes');mark('actual-retained-case-byte-version')
    for n in [0,1]:
        changed=copy.deepcopy(only);rec=next(rec for rec in changed['commands'] if rec['label']=='run-delay-'+str(n));index=rec['argv'].index('PublicTaskDelayProductFixtures')+2;rec['argv'][index]=str(p.HERE/'case-inputs.tsv')
        refused('current-worktree-case-argv-refused-'+str(n),lambda changed=changed:v.groups(changed),'exact same-JAR runtime argv')
    changed=copy.deepcopy(only);rec=next(rec for rec in changed['commands'] if rec['label']=='run-delay-0');rec['argv'][rec['argv'].index('PublicTaskDelayProductFixtures')+1]=str(p.HERE/'fixture-manifest.json');refused('counterfeit-manifest-argv-refused',lambda:v.groups(changed),'exact same-JAR runtime argv')
    original_root=v.COMPILED_ROOT
    try:
        v.COMPILED_ROOT=out/'missing-executed-root';refused('missing-executed-case-input-refused',lambda:v.executed_delay_case_input(history))
        v.COMPILED_ROOT=out/'wrong-executed-root';wrong=v.COMPILED_ROOT/'tools/oracle/dotj-core/public-task-delay-product-v1/case-inputs.tsv';wrong.parent.mkdir(parents=True);wrong.write_bytes(b'wrong retained table bytes')
        refused('wrong-executed-case-input-bytes-refused',lambda:v.executed_delay_case_input(history),'stale input')
        v.COMPILED_ROOT=p.ROOT;v.executed_delay_case_input(history);refused('mislocated-identical-case-input-refused',lambda:v.groups(only),'exact same-JAR runtime argv')
    finally:v.COMPILED_ROOT=original_root
    model=out/'canonical-source-model'
    for row in artifact['productSources']:
        target=model/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p.ROOT/row['path'],target)
    chosen,mode=v.qualified_artifact(artifact,jar,model,e['build'],model);c.require(mode=='ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION' and c.sha(chosen)==jar['sha256'],'real absent-JAR canonical projection');mark('complete-source-absent-canonical-JAR-accepted')
    refused('missing-noncanonical-JAR-no-arbitrary-fallback',lambda:v.qualified_artifact(artifact,jar,model,e['build']),'actual D/gate JAR required')
    target=model/artifact['jarPath'];target.parent.mkdir(parents=True);target.write_bytes(b'present counterfeit JAR');refused('present-wrong-JAR-refused',lambda:v.qualified_artifact(artifact,jar,model,e['build'],model),'present current JAR mismatches');target.unlink()
    source=model/next(row['path'] for row in artifact['productSources'] if row['path'].endswith('/Tasks/Task.java'));source.write_bytes(source.read_bytes()+b'\n');refused('source-mismatch-refused',lambda:v.qualified_artifact(artifact,jar,model,e['build'],model),'complete current product source closure')
    changed=copy.deepcopy(e);changed['canonicalProjection']['qualifiedReader']['original']['sha256']='0'*64;refused('counterfeit-historical-reader-version-refused',lambda:v.qualified_reader(changed),'exact gate-executed historical reader version')
    changed=copy.deepcopy(retained);changed['inputs']=[pin for pin in changed['inputs'] if Path(pin['path']).name!='case-inputs.tsv'];path=out/'missing-input-version.json';p.write(path,changed);changed_history=copy.deepcopy(history);changed_history['retainedDelayPaired']=c.descriptor(path);refused('missing-retained-case-version-refused',lambda:v.executed_delay_case_input(changed_history),'one retained executed Delay case-input version')
    changed=copy.deepcopy(history);changed['retainedDelayPaired']['sha256']='0'*64;refused('counterfeit-retained-proof-pin-refused',lambda:v.executed_delay_case_input(changed),'stale input')
    c.require(len(rows)==16,'finite relocation control inventory')
    proof=dict(status='PASS',controls=rows,reader=c.descriptor(Path(v.__file__)),source=c.descriptor(__file__),candidateJar=jar,historicalPhase=e['historicalPhases'][0]['receipt'],retainedDelayPaired=history['retainedDelayPaired'],executedCaseInput=c.descriptor(executed),sourceCount=len(artifact['productSources']),actualNativeExecutions=0,actualJvmExecutions=0,actualProductBuilds=0,actualFullGateExecutions=0,actualCanonicalCExecution=False)
    p.write(out/'receipt.json',proof);print('PASS real relocated reader controls',len(rows))
if __name__=='__main__':main()
