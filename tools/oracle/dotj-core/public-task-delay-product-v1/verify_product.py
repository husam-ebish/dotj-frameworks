"""Pure consumption of actual Task93 evidence; never executes a producer or test."""
from pathlib import Path
import product_support as p
c=p.c
EXECUTED_PROFILE=p.B/'worktrees/dotj-core-task-delay-v1/tools/oracle/dotj-core/public-task-delay-product-v1'
def group_command(rec,name):
    label=rec['label'];prefix='run-'+name+'-'
    return label=='compile-'+name or (label.startswith(prefix) and label[len(prefix):].isdigit())

def qualified_artifact(artifact,evidence,source_root):
    """Canonical source projection reads the exact archived qualified artifact.

    Every D/W17/gate tree must supply its own actual current JAR. The canonical
    read-only path never calls the archived artifact a new canonical build.
    """
    root=Path(source_root).resolve()
    if root==Path('C:/source/repos/dotj Frameworks').resolve():
        path=p.resolve(evidence['candidateJar'])
        c.require(c.sha(path)==artifact['jarSha256']==evidence['candidateJar']['sha256'],'exact archived canonical projection artifact')
        return path,'ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION'
    path=root/artifact['jarPath']
    c.require(path.is_file() and c.sha(path)==artifact['jarSha256']==evidence['candidateJar']['sha256'],'actual current D/gate JAR required; no archive fallback')
    return path,'ACTUAL_CURRENT_D_OR_GATE_ARTIFACT'

def command(rec,success=True):
    c.require(type(rec.get('processId')) is int and rec['processId']>0,'owned positive typed PID')
    for key in ['launched','jobAssigned','resumed']:c.require(rec.get(key) is True,'owned child '+key)
    c.require(type(rec.get('exitCode')) is int and rec['exitCode']==(0 if success else 1),'actual typed exit status')
    c.require(rec.get('timedOut') is False and rec.get('outputLimitExceeded') is False and not rec.get('error') and not rec.get('cleanupError'),'actual successful child')
    c.require(rec['timeoutSeconds'] in [120,180,1800] and rec['cleanupLimitSeconds']==5 and 0<=rec['cleanupSeconds']<=5 and rec['outputPollSeconds']==0.1,'owned process bounds')
    c.require(0<=rec['resourceSampleAgeSeconds']<=2,'resource freshness')
    c.require(p.guard.resource_ready(rec['resources'][-1]),'available physical/commit floor')
    c.require(rec['resourcePolicy']==dict(physicalFloorBytes=512*1024**2,availableCommitFloorBytes=16*1024**3,availableCommitField='ullAvailPageFile',maximumWaitSeconds=120,maximumSampleAgeSeconds=2),'exact resource policy')
    out=Path(rec['cwd']);env=p.frozen_phases.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
    c.require(rec['environment']==env,'explicit D process environment')
    limits=p.guard.OUTPUT_LIMITS[p.guard.output_profile(rec['label'])]
    c.require(rec['outputLimitsBytes']==limits,'fixed stream limits')
    for name in ['stdout','stderr']:
        pin=rec['streams'][name];actual=p.resolve(pin)
        c.require(pin['path']==rec[name+'Path'] and Path(pin['path'])==out/(rec['label']+'.'+name),'owned raw stream path')
        c.require(pin['sizeBytes']==rec['outputSizesBytes'][name] and pin['sizeBytes']<=limits[name],'actual complete bounded stream')

def receipt(pin,jar_hash,status=None):
    path=p.resolve(pin);r=c.read(path)
    if status is not None:c.require(r['status']==status,'exact phase status')
    c.require(r['nativeExecutions']==0 and r['acceptanceCredit']==0,'no native replay or acceptance credit')
    c.require(r['candidateJar']['sha256']==jar_hash and r['candidateJar']['sizeBytes']==p.resolve(r['candidateJar']).stat().st_size,'identical final JAR receipt')
    for item in r['inputs']+r['payload']:p.resolve(item)
    return r

def actual_group(group,records,jar):
    for pin in group['fixture']+group['classes']+group['payloads']:p.resolve(pin)
    name=group['name'];commands=[x for x in records if group_command(x,name)]
    c.require(len(commands)>=2,'actual compile/runtime group closure')
    compile=commands[0];command(compile)
    out=Path(compile['cwd']);args=compile['argv'];source_args=[d['path'] for d in group['fixture']]
    pathargs=['--module-path',jar,'--add-modules','dotj.core.foundation.v1'] if name=='paired' else ['-cp',jar]
    c.require(args==[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(out)],'-parameters','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),*pathargs,'-d',str(out/'classes'),*source_args],'exact compiled consumer argv')
    c.require(args[0]==str(p.JDK/'bin/javac.exe') and '-implicit:none' in args and args[args.index('-sourcepath')+1]==str(out/'empty-sourcepath') and not list((out/'empty-sourcepath').iterdir()),'JAR-only consumer compilation')
    c.require(args[-len(source_args):]==source_args and args.count(jar)==1,'exact bound fixture/JAR compile closure')
    for run in commands[1:]:
        command(run);c.require(run['argv'][0]==str(p.JDK/'bin/java.exe') and any(jar in arg for arg in run['argv']),'exact JDK/candidate runtime closure')
        c.require(Path(run['stderrPath']).read_bytes()==b'','no hidden runtime diagnostics')
    modes={
      'paired':[('PublicTaskDelayProductFixtures',[str(p.FROZEN/'fixture-manifest.json'),str(EXECUTED_PROFILE/'case-inputs.tsv'),part,jar]) for part in ['ordinary','async']],
      'private':[('System.Threading.Tasks.TaskDelayProductControls',[jar,str(n)]) for n in range(1,10)],
      'sample':[('DelayCancellationSample',[jar])],
      'valuetask-task':[('PublicValueTaskTaskFixtures',[jar])],
      'valuetask-boundaries':[('ValueTaskTaskBoundaryControls',[mode,jar,str(EXECUTED_PROFILE/'expected-public-surface-v1.txt')]) for mode in ['controls','task-first','configured-first','conversion-first']],
      'task':[('PublicTaskFixtures',[jar])],
      'task-boundaries':[('System.Threading.Tasks.TaskBoundaryControls',[jar])],
      'worktask':[('PublicWorkTaskCancelAsyncFixtures',[jar])],
      'worktask-boundaries':[('System.Threading.Tasks.WorkTaskBoundaryControls',[jar]),('System.Threading.CancelAsyncBoundaryControls',[jar])],
      'delegate-action-v1':[('DelegateFixtures',[str(out/'observations.txt')])],
      'public-cancellation-v1':[('PublicCancellationFixtures',[str(out/'observations.txt')])],
      'public-valuetask-v1':[('PublicValueTaskFixtures',[str(out/'observations.txt')])]}
    c.require(name in modes and len(commands)==len(modes[name])+1,'closed actual runtime mode count')
    cp=['--module-path',jar,'--add-modules','dotj.core.foundation.v1','-cp',str(out/'classes')] if name=='paired' else ['-cp',str(out/'classes')+';'+jar]
    for run,(owner,arguments) in zip(commands[1:],modes[name]):
        c.require(run['argv']==[str(p.JDK/'bin/java.exe'),*p.frozen_phases.jvm(out),*cp,owner,*arguments],'exact compiled consumer runtime argv')
    c.require(len(commands)==1+len(group['payloads']) or name in ['delegate-action-v1','public-cancellation-v1','public-valuetask-v1'],'actual runtime/payload count')

def validate(e):
    c.keys(e,['schemaVersion','status','candidateJar','contract','build','paired','private','historicalPartial','historicalTailPartial','historicalTail','sample','archiveManifest','historicalAudit','exports','forensicRecovery','acceptanceCredit','qualifiedFrameworks','remainingBoundaries'],'product evidence')
    c.require(type(e['schemaVersion']) is int and e['schemaVersion']==1 and e['status']=='BOUNDED_CANDIDATE_QUALIFIED_INTEGRATION_PENDING','bounded candidate status')
    c.require(e['acceptanceCredit']==0 and e['qualifiedFrameworks']==0,'no acceptance/release promotion')
    artifact=c.read(p.E/'foundation-product-candidate-v1.json');jar,artifactMode=qualified_artifact(artifact,e,p.ROOT);digest=c.sha(jar)
    c.require(e['candidateJar']['sha256']==digest==artifact['jarSha256'],'current canonical candidate must match identical qualified final JAR')
    p.resolve(e['candidateJar']);p.check_surface(jar)
    for pin in artifact['productSources']:c.require(c.sha(p.ROOT/pin['path'])==pin['sha256'],'current source closure')
    build=receipt(e['build'],digest,'PASS_BUILD')
    for rec in build['commands']:command(rec)
    c.require([Path(rec['argv'][0]).name for rec in build['commands']]==['javac.exe','javap.exe','javap.exe','jdeps.exe'],'actual product build tool closure')
    c.require({Path(x['path']).relative_to(p.B/'worktrees/dotj-core-task-delay-v1').as_posix():x['sha256'] for x in build['sourceClosure']}=={x['path']:x['sha256'] for x in artifact['productSources']},'exact originally compiled product source closure')
    for pin in build['sourceClosure']:p.resolve(pin)
    for key in ['contract','archiveManifest','historicalAudit','exports','forensicRecovery']:p.resolve(e[key])
    c.require(c.read(p.resolve(e['historicalAudit']))['additionalUnresolvedCanonicalInputs']==[],'no unresolved canonical history inputs')
    for pair in c.read(p.resolve(e['exports'])):
        original=pair['original'];export=pair['export'];p.resolve(export)
        c.require(original['sha256']==export['sha256'] and original['sizeBytes']==export['sizeBytes'],'verbatim frozen export pair')
    manifest,schema,passes=p.prerequisites()
    paired=receipt(e['paired'],digest,'PASS_PAIRED');group=paired['groups'][0]
    c.require(len(paired['groups'])==1 and group['name']=='paired' and group['cases']==113 and group['fields']==3955 and group['comparedNativePasses']==2,'exact paired execution closure')
    actual_group(group,paired['commands'],e['candidateJar']['path']);actual={}
    for pin,part in zip(group['payloads'],['ordinary','async']):actual.update(c.wire(p.resolve(pin).read_bytes(),schema,manifest,part))
    for native in passes:c.compare(actual,native,manifest)
    private=receipt(e['private'],digest,'PASS_PRIVATE');group=private['groups'][0];actual_group(group,private['commands'],e['candidateJar']['path'])
    markers=[line for pin in group['payloads'] for line in p.resolve(pin).read_text(encoding='utf-8').splitlines()]
    c.require(len(markers)==30 and set(markers)=={f'J{n:02}\tb\ttrue' for n in range(1,31)} and group['actualGroups']==9 and group['actualControls']==30,'all thirty actual private controls/nine actual groups')
    c.require(len(private['commands'])==10,'one fixture compile and nine actual private JVM groups')
    # Reparse all retained historical payloads on the same final artifact.
    from historical_replay import native_references
    references,old,c14,c15=native_references()
    records=[];groups=[]
    for key,status in [('historicalPartial','FAILED_STOP_NO_RETRY'),('historicalTailPartial','FAILED_STOP_NO_RETRY'),('historicalTail','PASS_HISTORICAL')]:
        r=receipt(e[key],digest,status);records.extend(r['commands'])
        groups.extend(g for g in r['groups'] if 'actualCount' in g)
        for rec in r['commands']:
            if rec['exitCode']==0:command(rec)
            else:command(rec,False)
    wanted=['valuetask-task','valuetask-boundaries','task','task-boundaries','worktask','worktask-boundaries','delegate-action-v1','public-cancellation-v1','public-valuetask-v1']
    c.require([g['name'] for g in groups]==wanted,'every historical group exactly once')
    c.require([g['actualCount'] for g in groups]==[1884,8,697,49,612,8,34,48,135],'actual historical counts')
    plan=c.read(p.B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json')['groups']
    for group in groups:
        name=group['name'];matched=[x for x in records if x['exitCode']==0 and group_command(x,name)]
        # Work boundary failed predecessor commands are retained and validated
        # separately; this successful group consumes the corrected successor only.
        if name=='worktask-boundaries':matched=[x for x in matched if Path(x['cwd']).parent.name=='historical-tail-final-v2']
        actual_group(group,matched,e['candidateJar']['path'])
        raw=[p.resolve(pin).read_bytes() for pin in group['payloads']]
        if name in ['valuetask-task','task','worktask']:
            n={'valuetask-task':2515,'task':2512,'worktask':2514}[name]
            if n==2512:observed=old.observations(raw[0],c.read(p.OLD/'schema.json'),False)
            else:
                reader=c14 if n==2514 else c15;observed=reader.observations(raw[0],c.read((p.H14 if n==2514 else p.H15)/'schema.json'))
            c.require(observed==references[n]['payload'],'same-JAR historical native match '+name)
        elif name=='task-boundaries':c.require(raw[0].decode().strip()=='PASS Task Java boundary controls: 49','all old 49 actual assertions')
        elif name=='valuetask-boundaries':
            expected=[{'J-API-ORIGIN','J-PUBLICATION','J-INTERRUPTION','J-DETACH','J-INLINE-THROW','J-DISPATCH','J-FOREIGN-THROWABLE'},*[{f'J-CONSUMER-FIRST.{mode}'} for mode in ['task-first','configured-first','conversion-first']]]
            c.require(len(raw)==4,'ValueTask actual modes')
            for data,keys in zip(raw,expected):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in keys},'ValueTask historical boundary bytes')
        elif name=='worktask-boundaries':
            for data,keys in zip(raw,[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in keys},'historical eight work/cancel groups')
        else:
            data={}
            for line in raw[0].decode().splitlines():
                key,value=line.split('=',1);c.require(key not in data,'unique historical field');data[key]=value
            c.require(data==next(x['expected'] for x in plan if x['name']==name),'legacy native fields')
    sample=receipt(e['sample'],digest,'PASS_SAMPLE');actual_group(sample['groups'][0],sample['commands'],e['candidateJar']['path'])
    c.require(p.resolve(sample['groups'][0]['payloads'][0]).read_text(encoding='utf-8').splitlines()==['sample.success\tb\ttrue','sample.canceled\tb\ttrue'],'actual packaged migration Java sample')
    return dict(cases=113,fields=3955,nativePasses=2,privateControls=30,privateGroups=9,historicalGroups=len(groups),historicalActualFieldsAndControls=sum(g['actualCount'] for g in groups),surfaceAdditions=5,jarSha256=digest,artifactProvenance=artifactMode)

def main():
    result=validate(c.read(p.E/'public-task-delay-v1.json'))
    print('PASS Task delay candidate:113cases/3955fields x2native;30private/9groups;9historicalgroups;exact5APIs;sameJAR '+result['jarSha256']+';'+result['artifactProvenance'])

if __name__=='__main__':main()
