"""Read actual selected and historical captures; never launch a workload."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q
p=q.p;c=p.c
EXECUTED_PROFILE=p.B/'worktrees/dotj-core-task-run-cancellation-v1/tools/oracle/dotj-core/public-task-run-token-v1'

def qualified_artifact(artifact,qualified,source_root,canonical_root=Path('C:/source/repos/dotj Frameworks')):
    root=Path(source_root).resolve();current=root/artifact['jarPath']
    c.require(artifact['jarSha256']==qualified['sha256'],'qualified artifact identity')
    for pin in artifact['productSources']:
        c.require(c.sha(root/pin['path'])==pin['sha256'],'complete current product source closure '+pin['path'])
    if current.is_file():
        c.require(c.sha(current)==qualified['sha256'],'present current JAR mismatches; no archive fallback')
        return current,'ACTUAL_CURRENT_D_OR_GATE_ARTIFACT'
    c.require(root==Path(canonical_root).resolve(),'actual D/gate JAR required; no archive fallback')
    c.validate_pin(qualified)
    return Path(qualified['path']),'ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION'

def group_command(rec,name):
    label=rec['label'];prefix='run-'+name+'-'
    return label=='compile-'+name or label.startswith(prefix) and label[len(prefix):].isdigit()

def command(rec,expected=0):
    c.successful(rec,expected)
    c.require(type(rec['processId']) is int and rec['processId']>0,'owned actual process ID')
    c.require(rec['cleanupLimitSeconds']==5 and 0<=rec['cleanupSeconds']<=5 and rec['outputPollSeconds']==0.1,'owned cleanup/output bounds')
    c.require(0<=rec['resourceSampleAgeSeconds']<=2 and p.guard.resource_ready(rec['resources'][-1]),'fresh physical/commit admission')
    c.require(rec['resourcePolicy']==dict(physicalFloorBytes=512*1024**2,availableCommitFloorBytes=16*1024**3,availableCommitField='ullAvailPageFile',maximumWaitSeconds=120,maximumSampleAgeSeconds=2),'resource policy')
    c.require(rec['timeoutSeconds']==(30 if rec['label'].startswith('native-pass') else 120) and rec['outputLimitsBytes']==p.guard.OUTPUT_LIMITS[p.guard.output_profile(rec['label'])],'fixed selected child/output limits')
    out=Path(rec['cwd']);env=p.frozen_phases.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
    c.require(rec['environment']==env,'exact selected D environment')
    for name,pin in rec['streams'].items():
        c.validate_pin(pin);c.require(pin['path']==rec[name+'Path'] and pin['sizeBytes']==rec['outputSizesBytes'][name],'complete actual raw stream')
        c.require(Path(pin['path'])==out/(rec['label']+'.'+name),'fixed owned raw stream destination')
        c.require(pin['sizeBytes']<=rec['outputLimitsBytes'][name],'bounded stream')

def receipt(pin,status,jar=None):
    c.validate_pin(pin);r=c.read(pin['path']);c.require(r['status']==status and r['finalized'] is True,'actual phase completion')
    if jar:c.require(r['candidateJar']==jar,'same final JAR descriptor')
    for item in r['inputs']:c.validate_pin(item['durable']);c.require(item['original']['sha256']==item['durable']['sha256'],'executed version snapshot')
    c.validate_pin(r['guard'])
    return r

def groups(r):
    for group in r['groups']:
        for pin in group['fixture']+group['classes']+group['payloads']:c.validate_pin(pin)
        name=group['name'];records=[x for x in r['commands'] if group_command(x,name)]
        c.require(records and records[0]['label']=='compile-'+name,'group command order')
        compiled=records[0];command(compiled)
        args=compiled['argv'];out=Path(compiled['cwd']);jar=r['candidateJar']['path']
        c.require(args[0]==str(p.JDK/'bin/javac.exe') and args.count(jar)==1 and '-implicit:none' in args,'explicit JDK/JAR-only compile')
        sourcepath=Path(args[args.index('-sourcepath')+1]);c.require(sourcepath==out/'empty-sourcepath' and not list(sourcepath.iterdir()),'no source fallback')
        c.require(args[-len(group['fixture']):]==[x['path'] for x in group['fixture']],'exact consumed fixture sources')
        module=name in ['paired','delay'];pathargs=['--module-path',jar,'--add-modules','dotj.core.foundation.v1'] if module else ['-cp',jar]
        c.require(args==[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(out)],'-parameters','-encoding','UTF-8','-implicit:none','-sourcepath',str(sourcepath),*pathargs,'-d',str(out/'classes'),*[x['path'] for x in group['fixture']]],'closed exact consumer compiler argv')
        actual=sorted((out/'classes').rglob('*.class'));c.require({str(x) for x in actual}=={x['path'] for x in group['classes']},'exact class inventory')
        c.require(all(x.name.startswith(tuple(Path(pin['path']).stem for pin in group['fixture'])) for x in actual),'no product classes in consumer output')
        paired_owner=Path(group['fixture'][0]['path']).stem
        expected=EXECUTED_PROFILE/'expected-public-surface-v1.txt'
        modes={
            'paired':[(paired_owner,[jar])],
            'private':[('System.Threading.Tasks.TaskRunTokenControls',[jar])],
            'sample':[('DelayCancellationSample',[jar])],
            'valuetask-task':[('PublicValueTaskTaskFixtures',[jar])],
            'valuetask-boundaries':[('ValueTaskTaskBoundaryControls',[mode,jar,str(expected)]) for mode in ['controls','task-first','configured-first','conversion-first']],
            'task':[('PublicTaskFixtures',[jar])],
            'task-boundaries':[('System.Threading.Tasks.TaskBoundaryControls',[jar])],
            'worktask':[('PublicWorkTaskCancelAsyncFixtures',[jar])],
            'worktask-boundaries':[('System.Threading.Tasks.WorkTaskBoundaryControls',[jar]),('System.Threading.CancelAsyncBoundaryControls',[jar])],
            'delegate-action-v1':[('DelegateFixtures',[str(out/'observations.txt')])],
            'public-cancellation-v1':[('PublicCancellationFixtures',[str(out/'observations.txt')])],
            'public-valuetask-v1':[('PublicValueTaskFixtures',[str(out/'observations.txt')])],
            'delay':[('PublicTaskDelayProductFixtures',[str(p.FROZEN/'fixture-manifest.json'),str(EXECUTED_PROFILE.with_name('public-task-delay-product-v1')/'case-inputs.tsv'),part,jar]) for part in ['ordinary','async']],
            'delay-private':[('System.Threading.Tasks.TaskDelayProductControls',[jar,str(n)]) for n in range(1,10)]}
        c.require(name in modes and len(records)==1+len(modes[name]),'closed runtime mode count')
        cp=['--module-path',jar,'--add-modules','dotj.core.foundation.v1','-cp',str(out/'classes')] if module else ['-cp',str(out/'classes')+';'+jar]
        for rec,(owner,arguments) in zip(records[1:],modes[name]):
            command(rec);c.require(rec['argv']==[str(p.JDK/'bin/java.exe'),*p.frozen_phases.jvm(out),*cp,owner,*arguments],'closed exact bound runtime argv')
            c.require(Path(rec['stderrPath']).read_bytes()==b'','no hidden runtime diagnostics')
        if name in ['delegate-action-v1','public-cancellation-v1','public-valuetask-v1']:
            c.require(group['payloads']==[c.descriptor(out/'observations.txt')],'legacy payload is actual output argument')
        else:c.require(group['payloads']==[rec['streams']['stdout'] for rec in records[1:]],'payloads bind actual runtime stdout')

def validate(e):
    c.require(e['status']=='SELECTED_BEHAVIOR_CHECKS_PASSED','selected workload status')
    jar=e['candidateJar'];c.validate_pin(jar);artifact=c.read(p.E/'foundation-product-candidate-v1.json')
    chosen,provenance=qualified_artifact(artifact,jar,p.ROOT)
    c.require(q.surface(Path(jar['path']))==e['publicSurface'],'compiled one-overload delta')
    c.validate_pin(e['contract']);contract=c.read(e['contract']['path'])
    c.validate_pin(contract['runtimeSource']);c.validate_pin(contract['upstreamTests'])
    text=(p.ROOT/'dotj-core/dotj-core-public/src/main/java/System/Threading/Tasks/Task.java').read_text()
    run=text[text.index('public static Task Run(Action action)'):text.index('public TaskStatus get_Status()')]
    c.require(all(word not in run for word in ['.Register(','.register(', 'CancellationTokenRegistration','Timer','DelayState']),'selected call path acquires no cancellation resource')
    c.require('new Thread(null, body, name, 0, false)' in text,'fresh daemon construction adaptation')
    baseline=receipt(e['baseline'],'PASS_BASELINE');c.require(baseline['baselineJar']['sha256']==q.BASELINE_SHA,'retained actual predecessor')
    command(baseline['commands'][0],1);c.require('method Run in class Task cannot be applied to given types' in Path(baseline['commands'][0]['stderrPath']).read_text(),'real missing overload refusal')
    build=receipt(e['build'],'PASS_BUILD',jar)
    for rec in build['commands']:command(rec)
    for pin in build['sourceClosure']:c.validate_pin(pin)
    cases=fields=0
    for key,suffix in [('paired',''),('pairedSupplement','-SUPPLEMENT')]:
        paired=receipt(e[key],'PASS_PAIRED'+suffix,jar);groups(paired)
        native=receipt(e['native' if not suffix else 'nativeSupplement'],'PASS_NATIVE'+suffix)
        for pin in native['compiledNative']+native['references']+native['bootstrapInputs']:c.validate_pin(pin)
        for rec in native['commands']:command(rec)
        config=c.read(next(x['path'] for x in native['bootstrapInputs'] if x['path'].endswith('runtimeconfig.json')))
        c.require(config['runtimeOptions']['rollForward']=='Disable' and config['runtimeOptions']['framework']['version']=='10.0.12','locked runtime config')
        c.require(Path(native['commands'][0]['stdoutPath']).read_text().strip()=='10.0.401','actual SDK version')
        actual=q.wire(Path(paired['groups'][0]['payloads'][0]['path']).read_bytes());captures=[x for x in native['commands'] if x['label'].startswith('native-pass')]
        c.require(len(captures)==2,'two native passes')
        for rec in captures:c.require(actual==q.wire(Path(rec['stdoutPath']).read_bytes()),'all actual typed native observations')
        cases+=len({key.split('.')[0] for key in actual});fields+=len(actual)
    private=receipt(e['private'],'PASS_PRIVATE',jar);groups(private)
    markers=Path(private['groups'][0]['payloads'][0]['path']).read_text().splitlines()
    c.require(len(markers)==23 and len(set(markers))==23 and all(x.endswith('\tb\ttrue') for x in markers),'23 real private groups')
    historical=[]
    for pin,status in [(e['historicalPartial'],'FAILED_RETAINED'),(e['historicalTail'],'PASS_HISTORICAL')]:
        r=receipt(pin,status,jar);groups(r);historical.extend(r['groups'])
        for rec in r['commands']:command(rec,1 if rec['label']=='compile-task-boundaries' and status=='FAILED_RETAINED' else 0)
    expected=['valuetask-task','valuetask-boundaries','task','task-boundaries','worktask','worktask-boundaries','delegate-action-v1','public-cancellation-v1','public-valuetask-v1','delay','delay-private']
    c.require([x['name'] for x in historical]==expected,'all selected historical groups exactly once')
    c.require([x['actualCount'] for x in historical[:9]]==[1884,8,697,49,612,8,34,48,135],'historical field/control counts retained')
    c.require(historical[9]['actualCases']==113 and historical[9]['actualFields']==3955 and historical[10]['actualControls']==30 and historical[10]['actualGroups']==9,'complete retained delay selected/private corpus')
    preservation=c.read(p.E/'public-task-run-token-preservation-v1.json')
    c.require(preservation['status']=='RETAINED_PREREQUISITES_AND_CHANGED_PREDICATES_CHECKED','explicit predecessor guarantee succession')
    for pin in preservation['retainedMetadata']+preservation['nativeReaderInputs']:c.validate_pin(pin)
    refs={}
    for pin in preservation['nativeObservationLocks']:
        c.validate_pin(pin);lock=c.read(pin['path']);number=next(n for n in [2512,2514,2515] if f'Batch-{n}-' in pin['path'])
        if number==2512:
            old_receipt=c.read(p.resolve(lock['nativeReceipt']));raw=p.resolve(old_receipt['commands'][-1]['streams']['stdout']).read_bytes()
        else:raw=p.resolve(lock['stdout']).read_bytes()
        refs[number]=raw
    old=p.load('run_token_retained_task_parser',p.OLD/'run-comparison.py')
    sys.path.insert(0,str(p.H15))
    c14=p.load('run_token_retained_work_parser',p.H14/'capture_support.py');c15=p.load('run_token_retained_value_parser',p.H15/'capture_support.py')
    by_name={g['name']:g for g in historical}
    for name,n,reader,folder in [('task',2512,old,p.OLD),('worktask',2514,c14,p.H14),('valuetask-task',2515,c15,p.H15)]:
        raw=Path(by_name[name]['payloads'][0]['path']).read_bytes();schema=c.read(folder/'schema.json')
        actual=reader.observations(raw,schema,False) if n==2512 else reader.observations(raw,schema)
        native=reader.observations(refs[n],schema,True) if n==2512 else reader.observations(refs[n],schema,True)
        c.require(actual==native,'reparsed retained native equality '+name)
    c.require(Path(by_name['task-boundaries']['payloads'][0]['path']).read_text().strip()=='PASS Task Java boundary controls: 49','retained Task private assertions')
    prior=c.read(p.B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json')['groups']
    for item in prior:
        raw=Path(by_name[item['name']]['payloads'][0]['path']).read_text()
        c.require(dict(line.split('=',1) for line in raw.splitlines())==item['expected'],'legacy exact observed fields')
    schema=c.read(p.FROZEN/'schema.json');manifest=c.read(p.FROZEN/'fixture-manifest.json')
    old_delay=c.read(p.resolve(c.read(p.E/'public-task-delay-v1.json')['paired']))['groups'][0]
    actual={};original={}
    for current,pin,part in zip(by_name['delay']['payloads'],old_delay['payloads'],['ordinary','async']):
        actual.update(c.wire(Path(current['path']).read_bytes(),schema,manifest,part));original.update(c.wire(p.resolve(pin).read_bytes(),schema,manifest,part))
    c.compare(actual,original,manifest)
    private_delay=[line for pin in by_name['delay-private']['payloads'] for line in Path(pin['path']).read_text().splitlines()]
    c.require(len(private_delay)==30 and set(private_delay)=={f'J{n:02}\tb\ttrue' for n in range(1,31)},'all actual delay private markers')
    sample=receipt(preservation['sameJarSample'],'PASS_SAMPLE',jar);groups(sample)
    c.require(Path(sample['groups'][0]['payloads'][0]['path']).read_text().splitlines()==['sample.success\tb\ttrue','sample.canceled\tb\ttrue'],'same-JAR retained migration sample')
    for pair in c.read(p.resolve(c.read(p.E/'public-task-delay-v1.json')['exports'])):
        export=p.resolve(pair['export']);c.require(pair['original']['sha256']==pair['export']['sha256'] and pair['original']['sizeBytes']==pair['export']['sizeBytes'],'retained verbatim archive/export pair')
    controls=c.read(preservation['changedPredicateControls']['path']);c.validate_pin(preservation['changedPredicateControls'])
    c.require(controls['status']=='PASS' and all(x['passed'] for x in controls['controls']),'actual changed consumed-contract controls')
    successors=c.read(q.HERE/'historical-successors-v1.json')
    for pair in successors:c.validate_pin(pair['original']);c.validate_pin(pair['successor'])
    packet=c.read(p.E/'foundation-e01-review-packet-v1.json')
    c.require(packet['candidateJarSha256']==jar['sha256'] and len(packet['openDecisions'])==3 and all(x['status']=='OPEN' for x in packet['openDecisions']),'same candidate all three E01 OPEN')
    c.require(e['acceptanceCredit']==0,'no bounded-work acceptance credit')
    c.require(cases==e['nativeCases']==25 and fields==e['nativeFields']==300,'complete selected native matrix inventory')
    return dict(cases=cases,fields=fields,nativePassesPerMatrix=2,privateControls=len(markers),historicalGroups=len(historical),jarSha256=jar['sha256'],artifactProvenance=provenance)

def main():
    result=validate(c.read(p.E/'public-task-run-token-v1.json'))
    print('PASS selected Task.Run(Action,token): '+str(result))

if __name__=='__main__':main()
