"""Owned Batch2520 phases; unchanged predecessor Job/resource guard and profiles."""
import argparse,json,os,shutil,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'public-task-delay-product-v1'))
import product_support as p
c=p.c
prior=p.load('batch2520_retained_phase_runner',HERE.parent/'public-task-run-token-v1/qualify.py')
A=p.B/'agents/batch2520-task-wait-async-implementation-v1'
BASELINE=p.B/'worktrees/dotj-core-task-run-cancellation-v1/dotj-core/dotj-core-public/build/foundation-v1/dotj-core-foundation-v1.jar'
BASELINE_SHA='18f9b3ffb4fe2d8dcbe5a7d036b557b543a61e2a6507bfd51375420ca7017a99'
class Session(prior.Session):
    def __init__(self,out,mode,jar=None):
        self.out=out;p.prepare(out);self.deadline=time.monotonic()+(2100 if mode=='gate' else 1800)
        self.data=dict(status='RUNNING',mode=mode,commands=[],groups=[],inputs=[],acceptanceCredit=0)
        if jar:self.data['candidateJar']=c.descriptor(jar)
        for source in sorted(HERE.iterdir()):
            if not source.is_file():continue
            target=out/'inputs'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target)
            self.data['inputs'].append(dict(original=c.descriptor(source),durable=c.descriptor(target)))
        self.data['guard']=c.descriptor(p.OLD/'owned_process.py')
        self.data['helpers']=[c.descriptor(Path(module.__file__)) for module in [p,c,p.frozen_phases,prior]]
        self.save()
def native(s):
    prior.payload(s,True)
    lock=c.read(A/'matrix-freeze-v3.json')
    for pin in lock['files']:c.validate_pin(pin)
    s.data['matrixFreeze']=c.descriptor(A/'matrix-freeze-v3.json')
    dotnet=p.B/'toolchains/dotnet';refs=sorted((dotnet/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    s.data['references']=[c.descriptor(x) for x in refs]
    for name,value in [('global.json',{'sdk':{'version':'10.0.401','rollForward':'disable'}}),('PublicTaskWaitAsyncOracle.runtimeconfig.json',{'runtimeOptions':{'tfm':'net10.0','framework':{'name':'Microsoft.NETCore.App','version':'10.0.12'},'rollForward':'Disable','configProperties':{'System.GC.Server':False}}})]:p.write(s.out/name,value)
    (s.out/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>\n',encoding='utf-8')
    s.data['bootstrapInputs']=[c.descriptor(s.out/name) for name in ['global.json','NuGet.Config','PublicTaskWaitAsyncOracle.runtimeconfig.json']];s.save()
    s.step('sdk-version',[str(dotnet/'dotnet.exe'),'--version'])
    c.require(Path(s.data['commands'][-1]['stdoutPath']).read_text().strip()=='10.0.401','actual pinned SDK')
    s.step('compile-native',[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(s.out/'PublicTaskWaitAsyncOracle.dll'),*['-r:'+str(x) for x in refs],str(HERE/'PublicTaskWaitAsyncOracle.cs')])
    s.data['compiledNative']=[c.descriptor(s.out/name) for name in ['PublicTaskWaitAsyncOracle.dll','PublicTaskWaitAsyncOracle.runtimeconfig.json']];s.save()
    argv=[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(s.out/'PublicTaskWaitAsyncOracle.runtimeconfig.json'),str(s.out/'PublicTaskWaitAsyncOracle.dll')]
    rec=s.step('installed-metadata',argv+['--metadata'])
    metadata=Path(rec['stdoutPath']).read_text()
    c.require('runtime=10.0.12' in metadata and 'corelib=1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' in metadata and metadata.count(' WaitAsync(')==5,'installed metadata/runtime/CoreLib')
    passes=[]
    for n in [1,2]:
        rec=s.step('native-pass'+str(n),argv+[str(HERE/'matrix-v2.tsv')],timeout=60)
        c.require(Path(rec['stderrPath']).read_bytes()==b'','native stderr');passes.append(prior.wire(Path(rec['stdoutPath']).read_bytes()))
    c.require(passes[0]==passes[1],'two exact native passes')
    validate_schema(passes[0]);s.data.update(cases=lock['rows'],fields=len(passes[0]),nativePasses=2)
def validate_schema(payload):
    matrix=c.read(HERE/'matrix-v2.json');expected={row['id']+'.'+name:kind for row in matrix['rows'] for name,kind in matrix['fields'][row['group']].items()}
    c.require(set(payload)==set(expected),'complete frozen matrix membership')
    c.require(all(payload[key][0]==kind for key,kind in expected.items()),'every frozen typed field')
def baseline(s):
    prior.payload(s);c.require(c.sha(BASELINE)==BASELINE_SHA,'actual frozen predecessor');s.data['baselineJar']=c.descriptor(BASELINE)
    rec=s.step('compile-baseline',[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(s.out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(s.out/'empty-sourcepath'),'-cp',str(BASELINE),'-d',str(s.out/'classes'),str(HERE/'BaselineWaitAsync.java')],expected=1)
    diagnostic=Path(rec['stderrPath']).read_text(encoding='utf-8');c.require(diagnostic.count('symbol:   method WaitAsync')==3 and 'symbol:   class TimeoutException' in diagnostic and '4 errors' in diagnostic,'three genuine overload refusals plus System name-collision diagnostic; class absence is proved by compiled surface')
def surface(jar):
    c.require(c.sha(BASELINE)==BASELINE_SHA,'frozen predecessor identity')
    before=p.surface_lines(BASELINE);after=p.surface_lines(jar)
    additions={
        'System/Threading/Tasks/Task|M|WaitAsync|(LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|1',
        'System/Threading/Tasks/Task|M|WaitAsync|(LSystem/TimeSpan;)LSystem/Threading/Tasks/Task;|1',
        'System/Threading/Tasks/Task|M|WaitAsync|(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|1',
        'System/TimeoutException|C|33',
        'System/TimeoutException|M|<init>|()V|1',
        'System/TimeoutException|M|<init>|(Ljava/lang/String;)V|1',
        'System/TimeoutException|M|<init>|(Ljava/lang/String;LSystem/Exception;)V|1'}
    c.require(after-before==additions and not before-after,'exact selected public delta')
    return dict(before=len(before),after=len(after),added=sorted(additions),removed=[])
def build(s):
    prior.payload(s);builder=p.load('wait_async_explicit_builder',HERE.parent/'build-foundation-product-candidate.py')
    s.data['sourceClosure']=[c.descriptor(x) for x in builder.SOURCES];s.save()
    classes=builder.build_product(s.jdk)
    artifact=dict(schemaVersion=1,productSources=[dict(path=x.relative_to(p.ROOT).as_posix(),sha256=c.sha(x)) for x in builder.SOURCES],jarPath=builder.JAR.relative_to(p.ROOT).as_posix(),jarSha256=c.sha(builder.JAR),licensePath=builder.LICENSE.relative_to(p.ROOT).as_posix(),licenseSha256=c.sha(builder.LICENSE),licenseEntry='META-INF/LICENSE',jarEntries=['META-INF/MANIFEST.MF','META-INF/LICENSE',*classes],classSha256={name:c.sha(builder.CLASSES/name) for name in classes},status='BUILT_STAGED_CANDIDATE; Batch2520 qualification and integration pending')
    p.write(p.E/'foundation-product-candidate-v1.json',artifact)
    s.data.update(candidateJar=c.descriptor(builder.JAR),surface=surface(builder.JAR));s.save()
    mapping=c.read(p.E/'foundation-file-notice-map-v1.json')
    task='dotj-core/dotj-core-public/src/main/java/System/Threading/Tasks/Task.java';timeout='dotj-core/dotj-core-public/src/main/java/System/TimeoutException.java'
    mapping['sourceToClasses'][task]=[name for name in classes if name=='System/Threading/Tasks/Task.class' or name.startswith('System/Threading/Tasks/Task$')]
    mapping['sourceToClasses'][timeout]=['System/TimeoutException.class']
    p.write(p.E/'foundation-file-notice-map-v1.json',mapping)
    p.load('wait_async_bind_map',HERE.parent/'bind-foundation-file-map.py').main()
    p.load('wait_async_distribution',HERE.parent/'verify-foundation-distribution.py').main(s.jdk)
def paired(s):
    native_pin=c.descriptor(A/'native-v2/receipt.json');native=c.read(native_pin['path']);c.require(native['status']=='PASS_NATIVE','actual corrected native capture')
    s.data['nativeReceipt']=native_pin;group,records=s.java_group('paired',[HERE/'PublicTaskWaitAsyncFixtures.java'],'PublicTaskWaitAsyncFixtures',[('PublicTaskWaitAsyncFixtures',[str(s.jar),str(HERE/'matrix-v2.tsv')])],s.jar,module=True)
    payload=prior.wire(Path(records[0]['stdoutPath']).read_bytes());validate_schema(payload)
    for rec in [r for r in native['commands'] if r['label'].startswith('native-pass')]:
        expected=prior.wire(Path(rec['stdoutPath']).read_bytes());differences=[key for key in payload if payload[key]!=expected[key]]
        if differences:p.write(s.out/'differences.json',[dict(field=key,native=expected[key],java=payload[key]) for key in differences])
        c.require(not differences,'exact typed native comparison '+str(len(differences))+' differing fields')
    group.update(cases=390,fields=len(payload),nativePasses=2)
def inherited_run(s,jar):
    evidence=c.read(p.E/'public-task-run-token-v1.json');s.data['retainedRunEvidence']=c.descriptor(p.E/'public-task-run-token-v1.json')
    old=HERE.with_name('public-task-run-token-v1')
    for label,owner,key in [('run-token','PublicTaskRunTokenFixtures','native'),('run-token-supplement','SupplementRunTokenFixtures','nativeSupplement'),('run-token-association','TaskRunTokenAssociationFixtures','nativeAssociation')]:
        native=c.read(evidence[key]['path']);group,records=s.java_group(label,[old/(owner+'.java')],owner,[(owner,[str(jar)])],jar,module=True)
        actual=prior.wire(Path(records[0]['stdoutPath']).read_bytes())
        for rec in [r for r in native['commands'] if r['label'].startswith('native-pass')]:c.require(actual==prior.wire(Path(rec['stdoutPath']).read_bytes()),'retained Run native fields '+label)
        group.update(actualFields=len(actual),nativeReceipt=evidence[key])
    for label,owner,wanted in [('run-token-private','TaskRunTokenControls',23),('run-token-association-private','TaskRunTokenAssociationControls',6)]:
        group,records=s.java_group(label,[old/(owner+'.java')],None,[('System.Threading.Tasks.'+owner,[str(jar)])],jar)
        markers=Path(records[0]['stdoutPath']).read_text().splitlines();c.require(len(markers)==wanted and len(set(markers))==wanted and all(x.endswith('\tb\ttrue') for x in markers),'retained Run controls');group['actualControls']=wanted
def supplement_schema(payload,boundary=False):
    matrix=c.read(HERE/('validation-boundary-schema-v1.json' if boundary else 'supplement-schema-v1.json'))
    expected={row['id']+'.'+name:kind for row in matrix['rows'] for name,kind in matrix['fields'][row['group']].items()} if boundary else {id+'.'+name:kind for id in matrix['rows'] for name,kind in matrix['fields'].items()}
    c.require(set(payload)==set(expected) and all(payload[key][0]==kind for key,kind in expected.items()),'complete exact supplemental typed schema')
def native_supplement(s,boundary=False):
    lock=A/'supplement-freeze-v1.json';c.validate_pin(c.descriptor(lock))
    for pin in c.read(lock)['files']:c.validate_pin(pin)
    s.data['matrixFreeze']=c.descriptor(lock);native=c.read(A/'native-v2/receipt.json');dotnet=p.B/'toolchains/dotnet'
    if boundary:
        for pin in native['compiledNative']:c.validate_pin(pin)
        s.data['importedNativeAssembly']=native['compiledNative'];s.data['nativeProducer']=c.descriptor(A/'native-v2/receipt.json')
        argv=[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(A/'native-v2/PublicTaskWaitAsyncOracle.runtimeconfig.json'),str(A/'native-v2/PublicTaskWaitAsyncOracle.dll'),str(HERE/'validation-boundary-v1.tsv')]
    else:
        refs=native['references'];s.data['references']=refs
        for pin in refs:c.validate_pin(pin)
        target=s.out/'SupplementWaitAsyncOracle.runtimeconfig.json';shutil.copyfile(A/'native-v2/PublicTaskWaitAsyncOracle.runtimeconfig.json',target);s.data['runtimeConfig']=c.descriptor(target);s.save()
        s.step('compile-native',[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(s.out/'SupplementWaitAsyncOracle.dll'),*['-r:'+pin['path'] for pin in refs],str(HERE/'SupplementWaitAsyncOracle.cs')])
        s.data['compiledNative']=c.descriptor(s.out/'SupplementWaitAsyncOracle.dll');argv=[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(target),str(s.out/'SupplementWaitAsyncOracle.dll')]
    s.save();passes=[]
    for n in [1,2]:
        rec=s.step('native-pass'+str(n),argv,timeout=60);c.require(Path(rec['stderrPath']).read_bytes()==b'','supplement native stderr');passes.append(prior.wire(Path(rec['stdoutPath']).read_bytes()))
    supplement_schema(passes[0],boundary);c.require(passes[0]==passes[1],'two exact supplemental native passes');s.data.update(cases=80 if boundary else 17,fields=len(passes[0]),nativePasses=2)
def paired_supplement(s,jar,boundary=False):
    label='paired-validation' if boundary else 'paired-supplement';owner='PublicTaskWaitAsyncFixtures' if boundary else 'SupplementWaitAsyncFixtures';arguments=[str(jar),str(HERE/'validation-boundary-v1.tsv')] if boundary else [str(jar)]
    native_path=A/('native-validation-v1' if boundary else 'native-supplement-v1')/'receipt.json';native=c.read(native_path);c.require(native['status']==('PASS_NATIVE-VALIDATION' if boundary else 'PASS_NATIVE-SUPPLEMENT'),'actual supplemental native phase');s.data['nativeReceipt']=c.descriptor(native_path)
    group,records=s.java_group(label,[HERE/(owner+'.java')],owner,[(owner,arguments)],jar,module=True);actual=prior.wire(Path(records[0]['stdoutPath']).read_bytes());supplement_schema(actual,boundary)
    for rec in [rec for rec in native['commands'] if rec['label'].startswith('native-pass')]:c.require(actual==prior.wire(Path(rec['stdoutPath']).read_bytes()),'exact supplemental native fields')
    group.update(cases=native['cases'],fields=len(actual),nativePasses=2)
def sample(s,jar):
    dotnet=p.B/'toolchains/dotnet';refs=sorted((dotnet/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    source=A/'native-v2/PublicTaskWaitAsyncOracle.runtimeconfig.json';target=s.out/'WaitAsyncSample.runtimeconfig.json';shutil.copyfile(source,target)
    s.data['sampleNativeInputs']=[c.descriptor(x) for x in [HERE/'WaitAsyncSample.cs',target,*refs]];s.save()
    s.step('compile-sample-native',[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(s.out/'WaitAsyncSample.dll'),*['-r:'+str(x) for x in refs],str(HERE/'WaitAsyncSample.cs')])
    s.data['sampleNativeAssembly']=c.descriptor(s.out/'WaitAsyncSample.dll');s.save();captures=[]
    for n in [1,2]:
        rec=s.step('sample-native-pass'+str(n),[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(target),str(s.out/'WaitAsyncSample.dll')]);captures.append(prior.wire(Path(rec['stdoutPath']).read_bytes()))
    group,records=s.java_group('sample',[HERE/'WaitAsyncSample.java'],None,[('WaitAsyncSample',[str(jar)])],jar,module=True)
    actual=prior.wire(Path(records[0]['stdoutPath']).read_bytes());c.require(captures[0]==captures[1]==actual and len(actual)==6 and all(x==('b','true') for x in actual.values()),'paired sample exact six fields')
    s.java_group('retained-delay-sample',[p.HERE/'DelayCancellationSample.java'],None,[('DelayCancellationSample',[str(jar)])],jar)
def inner(args):
    s=Session(args.out,args.mode,args.jar);s.jar=args.jar
    try:
        if args.mode=='native':native(s)
        elif args.mode=='native-supplement':native_supplement(s)
        elif args.mode=='native-validation':native_supplement(s,True)
        elif args.mode=='paired-supplement':paired_supplement(s,args.jar)
        elif args.mode=='paired-validation':paired_supplement(s,args.jar,True)
        elif args.mode=='baseline':baseline(s)
        elif args.mode=='build':build(s)
        elif args.mode=='paired':paired(s)
        elif args.mode=='private':
            group,records=s.java_group('private',[HERE/'TaskWaitAsyncControls.java'],None,[('System.Threading.Tasks.TaskWaitAsyncControls',[str(args.jar)]),('System.Threading.Tasks.TaskWaitAsyncControls',[str(args.jar),'fresh'])],args.jar)
            markers=[line for rec in records for line in Path(rec['stdoutPath']).read_text().splitlines()];c.require(markers and len(markers)==len(set(markers)) and all(line.endswith('\tb\ttrue') for line in markers),'unique passing private groups');group['controls']=len(markers)
        elif args.mode=='historical':
            sys.modules['batch2520_qualify']=sys.modules[__name__]
            p.load('batch2520_historical_replay',HERE/'historical.py').replay(s,args.jar,args.only)
            inherited_run(s,args.jar)
        elif args.mode=='sample':sample(s,args.jar)
        elif args.mode=='audits':
            for name in ['audit-foundation-rights-inputs.py','audit-foundation-source-provenance.py','compare-foundation-upstream-text.py','build-foundation-notice-review-queue.py','audit-throw-site-upstream-adjacency.py','build-foundation-e01-review-packet.py','verify-differential-oracle-provenance.py']:
                if args.only and name not in args.only.split(','):continue
                s.step('audit-'+name,[str(p.PYTHON),'-B',str(HERE.parent/name)])
        elif args.mode=='gate':
            predecessor=c.read(p.E/'public-task-run-token-foundation-v1.json');c.validate_pin(predecessor['phase']);proof=Path(predecessor['phase']['path'])
            c.require(c.read(proof)['status']=='PASS_GATE','actual predecessor complete gate profile')
            s.data['inheritedGateEnvelope']=c.descriptor(proof);prior_gate=c.read(proof)
            for pin in prior_gate['shellPayload']:c.validate_pin(pin)
            s.data['shellPayload']=prior_gate['shellPayload'];gate=p.load('batch2520_complete_gate',HERE.parent/'run-foundation-public-candidate-gate.py');s.data['gateSources']=[c.descriptor(HERE.parent/name) for name in ['run-foundation-public-candidate-gate.py',*gate.CHECKS]]
            s.data['gateEnvelope']=dict(childSeconds=1800,ownedOuterSeconds=2100,checkWorkers=3,builderJavaWorkers=2,sdkHeapMiB=512,jdkHeapMiB=256,metadataRollForward='LatestPatch; actual runtime10.0.12/CoreLib bound; selected native keeps Disable/128MiB')
            s.save();s.step('compile-bootstrap',[str(p.PYTHON),'-B',str(HERE.parent/'build-idisposable-candidate.py')]);s.step('foundation-gate',[str(p.PYTHON),'-B',str(HERE.parent/'run-foundation-public-candidate-gate.py')],timeout=1800)
        elif args.mode=='pure':
            for name in ['verify-public-task-wait-async.py','verify-public-task-run-token.py','verify-public-task-delay.py','verify-public-valuetask-task.py','verify-public-worktask-cancelasync.py']:s.step('pure-'+name,[str(p.PYTHON),'-B',str(HERE.parent/name)])
        elif args.mode=='negative':
            target=s.out/'selected-evidence-at-execution.json';shutil.copyfile(p.E/'public-task-wait-async-v1.json',target);s.data['selectedEvidenceInput']=c.descriptor(target);s.save()
            s.step('negative-controls',[str(p.PYTHON),'-B',str(HERE/'verify-negative-controls.py'),str(s.out/'controls')])
        elif args.mode=='aggregate-controls':s.step('aggregate-controls',[str(p.PYTHON),'-B',str(HERE/'GateTaskEvidenceControls.py'),str(s.out/'controls')])
        else:raise ValueError(args.mode)
        if args.jar:c.require(c.descriptor(args.jar)==s.data['candidateJar'],'actual unchanged final JAR at phase finalization')
        s.data.update(status='PASS_'+args.mode.upper(),finalized=True);s.save()
    except BaseException as error:s.data.update(status='FAILED_RETAINED',failure=repr(error),finalized=True);s.save();raise
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',required=True);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--jar',type=Path);ap.add_argument('--only');ap.add_argument('--inner',action='store_true');args=ap.parse_args()
    if args.inner:inner(args);return
    outer=args.out.with_name(args.out.name+'-outer');p.prepare(outer)
    p.write(outer/'invocation.json',dict(argv=sys.argv,source=c.descriptor(__file__),guard=c.descriptor(p.OLD/'owned_process.py')))
    timeout=2100 if args.mode=='gate' else 1800
    def update(rec):p.write(outer/'controller.json',rec)
    rec=prior.launch([str(p.PYTHON),'-B',str(HERE/'qualify.py'),*sys.argv[1:],'--inner'],outer,'controller',timeout,time.monotonic()+timeout+165,update);update(rec);c.successful(rec)
    print(c.read(args.out/'receipt.json')['status'],c.sha(args.out/'receipt.json'))
if __name__=='__main__':main()
