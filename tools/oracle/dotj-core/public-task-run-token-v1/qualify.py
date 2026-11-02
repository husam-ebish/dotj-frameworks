"""Fixed selected Run(Action,token) phases using the unchanged owned Job guard."""
import argparse, hashlib, json, os, shutil, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent/'public-task-delay-product-v1'))
import product_support as p
c=p.c
A=p.B/'agents/batch2519-task-run-cancellation-implementation-v1'
BASELINE=p.B/'worktrees/dotj-core-task-delay-v1/dotj-core/dotj-core-public/build/foundation-v1/dotj-core-foundation-v1.jar'
BASELINE_SHA='7528c565d2242ad5ab50700ad554e1561e71ba78ed40ed48b9a834cf58934099'
ADDITION='System/Threading/Tasks/Task|M|Run|(LSystem/Action;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|9'

def final_admission(deadline,timeout,now=time.monotonic,memory=p.guard.memory):
    started=now();sample=memory();finished=now();age=finished-started
    c.require(0<=age<=2 and p.guard.resource_ready(sample),'fresh final physical/commit admission')
    c.require(finished+timeout+5+1<deadline,'full remaining child/cleanup/finalization budget')
    return sample,age

def full_gate_environment(out):
    env=p.frozen_phases.environment(out)
    env.update({'ProgramFiles(x86)':r'C:\Program Files (x86)','DOTNET_GCHeapHardLimit':'20000000','DOTNET_ROLL_FORWARD':'LatestPatch',
        'DOTJ_JAVA_WORKERS':'2','MSBUILDDISABLENODEREUSE':'1','DOTNET_CLI_DO_NOT_USE_MSBUILD_SERVER':'1','PYTHONUNBUFFERED':'1',
        'PATHEXT':'.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC',
        'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'core.longpaths','GIT_CONFIG_VALUE_0':'true'})
    env['PATH']=str(p.PYTHON.parent)+';'+env['PATH']+r';C:\Program Files\Git\cmd;C:\Windows\System32\WindowsPowerShell\v1.0'
    env['JAVA_TOOL_OPTIONS']='-Xms16m -Xmx256m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC -XX:ReservedCodeCacheSize=64m '+ ' '.join('-D'+key+'="'+str(value)+'"' for key,value in [('java.io.tmpdir',out/'tmp'),('user.home',out/'home')])+ ' -XX:ErrorFile="'+str(out/'tmp/hs_err_pid%p.log')+'" -XX:HeapDumpPath="'+str(out/'tmp')+'"'
    return env

def launch(argv,out,label,timeout,deadline,update):
    # Receipt/stream creation can take >2s on this disk. Sample inside the
    # unchanged guard's final prelaunch boundary, after those writes and Job setup.
    sampled,samples=p.guard.wait_resources(min(deadline,time.monotonic()+160))
    env=p.frozen_phases.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
    if label in ['foundation-gate','metadata-corrected','compile-bootstrap']:env=full_gate_environment(out)
    age=[None]
    def prelaunch():
        sample,age[0]=final_admission(deadline,timeout)
        samples.append(sample)
    rec=p.guard.run(argv,out,env,label,timeout,on_update=update,prelaunch=prelaunch)
    rec.update(resources=samples,resourceSampleAgeSeconds=age[0],environment=env,
        streams={name:c.descriptor(rec[name+'Path']) for name in ['stdout','stderr']},
        resourcePolicy=dict(physicalFloorBytes=512*1024**2,availableCommitFloorBytes=16*1024**3,availableCommitField='ullAvailPageFile',maximumWaitSeconds=120,maximumSampleAgeSeconds=2))
    return rec

def wire(raw):
    result={}
    for line in raw.decode('utf-8').splitlines():
        key,kind,value=line.split('\t')
        c.require(key not in result and kind in ['b','i','s'],'unique typed field')
        c.require(kind!='b' or value in ['true','false'],'typed Boolean')
        if kind=='i':int(value)
        result[key]=(kind,value)
    return result

def surface(jar):
    c.require(c.sha(BASELINE)==BASELINE_SHA,'actual retained predecessor JAR')
    before=p.surface_lines(BASELINE);after=p.surface_lines(jar)
    c.require(after-before=={ADDITION} and not before-after,'exact one-overload public delta')
    return dict(before=len(before),after=len(after),added=sorted(after-before),removed=[])

class Session:
    def __init__(self,out,mode,jar=None):
        self.out=out;p.prepare(out);self.deadline=time.monotonic()+(2100 if mode=='gate' else 1800)
        self.data=dict(status='RUNNING',mode=mode,commands=[],groups=[],inputs=[],acceptanceCredit=0)
        if jar:self.data['candidateJar']=c.descriptor(jar)
        # Freeze the actual authored phase inputs, not predecessor provenance graphs.
        for source in sorted(HERE.iterdir()):
            if not source.is_file():continue
            target=out/'inputs'/source.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(source,target)
            self.data['inputs'].append(dict(original=c.descriptor(source),durable=c.descriptor(target)))
        self.data['guard']=c.descriptor(p.OLD/'owned_process.py')
        self.data['helpers']=[c.descriptor(Path(module.__file__)) for module in [p,c,p.frozen_phases]]
        self.save()
    def save(self):p.write(self.out/'receipt.json',self.data)
    def step(self,label,argv,out=None,timeout=120,expected=0):
        out=out or self.out;entry={'label':label};self.data['commands'].append(entry);self.save()
        def update(value):entry.update(value);self.save()
        entry.update(launch(argv,out,label,timeout,self.deadline,update));self.save()
        c.successful(entry,expected)
        return entry
    def jdk(self,tool,*args):
        flags=p.frozen_phases.jvm(self.out) if tool=='java' else ['-J'+x for x in p.frozen_phases.jvm(self.out)]
        rec=self.step(('compile-' if tool=='javac' else 'run-')+tool+'-'+str(len(self.data['commands'])),[str(p.JDK/'bin'/(tool+'.exe')),*flags,*args])
        return Path(rec['stdoutPath']).read_text(encoding='utf-8')
    def java_group(self,name,fixtures,main,modes,jar,module=False):
        out=self.out/name;p.prepare(out)
        args=['--module-path',str(jar),'--add-modules','dotj.core.foundation.v1'] if module else ['-cp',str(jar)]
        self.step('compile-'+name,[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(out)],'-parameters','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),*args,'-d',str(out/'classes'),*map(str,fixtures)],out)
        classes=sorted((out/'classes').rglob('*.class'))
        c.require(classes and not list((out/'empty-sourcepath').iterdir()),'empty sourcepath')
        c.require(all(x.name.startswith(tuple(f.stem for f in fixtures)) for x in classes),'fixture-only class inventory')
        records=[]
        for n,(owner,arguments) in enumerate(modes or [(main,[])]):
            cp=['--module-path',str(jar),'--add-modules','dotj.core.foundation.v1','-cp',str(out/'classes')] if module else ['-cp',str(out/'classes')+os.pathsep+str(jar)]
            rec=self.step('run-'+name+'-'+str(n),[str(p.JDK/'bin/java.exe'),*p.frozen_phases.jvm(out),*cp,owner,*arguments],out)
            c.require(Path(rec['stderrPath']).read_bytes()==b'','clean runtime stderr '+name);records.append(rec)
        group=dict(name=name,fixture=[c.descriptor(x) for x in fixtures],classes=[c.descriptor(x) for x in classes],payloads=[x['streams']['stdout'] for x in records])
        self.data['groups'].append(group);self.save();return group,records

def payload(s,native=False):
    lock=c.read(p.FROZEN/'toolchain-payload-lock.json')
    names=['python','jdk']+(['dotnet'] if native else [])
    # The frozen manifest is reused. Only actual executable/runtime payloads are
    # consumed; no SDK oracle or old baseline producer graph is reexecuted.
    pins=[]
    for name,item in lock['payloads'].items():
        if name in names:
            for pin in item['files']:c.validate_pin(pin);pins.append(pin)
    c.require(any(Path(x['path'])==p.PYTHON for x in pins),'actual Python executable pin')
    s.data['payloadManifest']=c.descriptor(p.FROZEN/'toolchain-payload-lock.json');s.data['payload']=pins;s.save()

def native(s,supplement=False):
    payload(s,True)
    dotnet=p.B/'toolchains/dotnet';refs=sorted((dotnet/'packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    c.require(refs,'locked reference assemblies')
    s.data['references']=[c.descriptor(x) for x in refs]
    for name,value in [('global.json',{'sdk':{'version':'10.0.401','rollForward':'disable'}}),('PublicTaskRunTokenOracle.runtimeconfig.json',{'runtimeOptions':{'tfm':'net10.0','framework':{'name':'Microsoft.NETCore.App','version':'10.0.12'},'rollForward':'Disable','configProperties':{'System.GC.Server':False}}})]:p.write(s.out/name,value)
    (s.out/'NuGet.Config').write_text('<configuration><packageSources><clear /></packageSources></configuration>\n',encoding='utf-8')
    s.data['bootstrapInputs']=[c.descriptor(s.out/name) for name in ['global.json','NuGet.Config','PublicTaskRunTokenOracle.runtimeconfig.json']]
    s.save()
    s.step('sdk-version',[str(dotnet/'dotnet.exe'),'--version'])
    c.require(Path(s.data['commands'][-1]['stdoutPath']).read_text().strip()=='10.0.401','actual pinned SDK')
    s.step('compile-native',[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(s.out/'PublicTaskRunTokenOracle.dll'),*['-r:'+str(x) for x in refs],str(HERE/('SupplementRunTokenOracle.cs' if supplement else 'PublicTaskRunTokenOracle.cs'))])
    s.data['compiledNative']=[c.descriptor(s.out/name) for name in ['PublicTaskRunTokenOracle.dll','PublicTaskRunTokenOracle.runtimeconfig.json']];s.save()
    passes=[]
    for n in [1,2]:
        rec=s.step('native-pass'+str(n),[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(s.out/'PublicTaskRunTokenOracle.runtimeconfig.json'),str(s.out/'PublicTaskRunTokenOracle.dll')],timeout=30)
        c.require(Path(rec['stderrPath']).read_bytes()==b'','native stderr')
        passes.append(wire(Path(rec['stdoutPath']).read_bytes()))
    c.require(passes[0]==passes[1],'two native passes')
    s.data.update(cases=len({key.split('.')[0] for key in passes[0]}),fields=len(passes[0]),nativePasses=2)

def baseline(s):
    payload(s);c.require(c.sha(BASELINE)==BASELINE_SHA,'baseline identity');s.data['baselineJar']=c.descriptor(BASELINE)
    rec=s.step('compile-baseline',[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(s.out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(s.out/'empty-sourcepath'),'-cp',str(BASELINE),'-d',str(s.out/'classes'),str(HERE/'BaselineRunToken.java')],expected=1)
    diagnostic=Path(rec['stderrPath']).read_text(encoding='utf-8')
    c.require('method Run in class Task cannot be applied to given types' in diagnostic and 'required: Action' in diagnostic and 'found:' in diagnostic and '1 error' in diagnostic,'genuine overload compilation refusal')
    c.require(not list((s.out/'classes').rglob('*.class')),'no baseline fixture class')

def build(s):
    payload(s);builder=p.load('run_token_explicit_builder',HERE.parent/'build-foundation-product-candidate.py')
    s.data['sourceClosure']=[c.descriptor(x) for x in builder.SOURCES];s.save()
    classes=builder.build_product(s.jdk)
    artifact=dict(schemaVersion=1,productSources=[dict(path=x.relative_to(ROOT).as_posix(),sha256=c.sha(x)) for x in builder.SOURCES],jarPath=builder.JAR.relative_to(ROOT).as_posix(),jarSha256=c.sha(builder.JAR),licensePath=builder.LICENSE.relative_to(ROOT).as_posix(),licenseSha256=c.sha(builder.LICENSE),licenseEntry='META-INF/LICENSE',jarEntries=['META-INF/MANIFEST.MF','META-INF/LICENSE',*classes],classSha256={name:c.sha(builder.CLASSES/name) for name in classes},status='BUILT_STAGED_CANDIDATE; Batch2519 qualification and integration pending')
    p.write(p.E/'foundation-product-candidate-v1.json',artifact)
    s.data.update(candidateJar=c.descriptor(builder.JAR),surface=surface(builder.JAR));s.save()
    p.load('run_token_bind_map',HERE.parent/'bind-foundation-file-map.py').main()
    p.load('run_token_distribution',HERE.parent/'verify-foundation-distribution.py').main(s.jdk)

def paired(s,jar,native_receipt,supplement=False):
    payload(s);s.data['surface']=surface(jar);native_data=c.read(native_receipt)
    c.require(native_data['status']==('PASS_NATIVE-SUPPLEMENT' if supplement else 'PASS_NATIVE'),'qualified actual native phase')
    native_runs=[x for x in native_data['commands'] if x['label'].startswith('native-pass')]
    owner='SupplementRunTokenFixtures' if supplement else 'PublicTaskRunTokenFixtures'
    group,records=s.java_group('paired',[HERE/(owner+'.java')],owner,[(owner,[str(jar)])],jar,module=True)
    actual=wire(Path(records[0]['stdoutPath']).read_bytes())
    for rec in native_runs:
        for pin in rec['streams'].values():c.validate_pin(pin)
        c.require(actual==wire(Path(rec['stdoutPath']).read_bytes()),'complete typed native match')
    group.update(cases=native_data['cases'],fields=len(actual),nativePasses=len(native_runs));s.data['nativeReceipt']=c.descriptor(native_receipt)

def inner(args):
    s=Session(args.out,args.mode,args.jar)
    try:
        if args.mode=='baseline':baseline(s)
        elif args.mode=='native':native(s)
        elif args.mode=='native-supplement':native(s,True)
        elif args.mode=='build':build(s)
        elif args.mode=='paired':paired(s,args.jar,args.native_receipt)
        elif args.mode=='paired-supplement':paired(s,args.jar,args.native_receipt,True)
        elif args.mode=='private':
            payload(s);group,records=s.java_group('private',[HERE/'TaskRunTokenControls.java'],'System.Threading.Tasks.TaskRunTokenControls',[('System.Threading.Tasks.TaskRunTokenControls',[str(args.jar)])],args.jar)
            markers=Path(records[0]['stdoutPath']).read_text().splitlines();c.require(markers and all(line.endswith('\tb\ttrue') for line in markers) and len(markers)==len(set(markers)),'unique private controls');group['controls']=len(markers)
        elif args.mode=='sample':
            payload(s);s.java_group('sample',[p.HERE/'DelayCancellationSample.java'],'DelayCancellationSample',[('DelayCancellationSample',[str(args.jar)])],args.jar)
        elif args.mode=='pure-verifiers':
            for name in ['verify-public-worktask-cancelasync.py','verify-public-valuetask-task.py','verify-public-task-delay.py','verify-public-task-run-token.py']:
                s.step('pure-'+name,[str(p.PYTHON),'-B',str(HERE.parent/name)])
        elif args.mode=='historical':
            payload(s)
            from historical import replay
            replay(s,args.jar,args.only)
        elif args.mode=='audits':
            for name in ['audit-foundation-rights-inputs.py','audit-foundation-source-provenance.py','compare-foundation-upstream-text.py','build-foundation-notice-review-queue.py','audit-throw-site-upstream-adjacency.py','build-foundation-e01-review-packet.py','verify-differential-oracle-provenance.py']:s.step('audit-'+name,[str(p.PYTHON),'-B',str(HERE.parent/name)])
        elif args.mode=='metadata-diagnostic':
            s.data['inheritedPayloadVerification']=c.descriptor(A/'native-v1/receipt.json')
            s.data['diagnosticInputs']=[c.descriptor(HERE.parent/name) for name in ['capture-foundation-public-metadata.py','global.json','NuGet.Config','OracleBootstrap.csproj','foundation-public-metadata/FoundationPublicMetadata.csproj']]
            s.save()
            s.step('metadata-direct',[str(p.B/'toolchains/dotnet/dotnet.exe'),'run','--project',str(HERE.parent/'foundation-public-metadata/FoundationPublicMetadata.csproj'),'--configuration','Release','--no-launch-profile'],expected=1)
        elif args.mode=='metadata-corrected':
            s.step('metadata-corrected',[str(p.B/'toolchains/dotnet/dotnet.exe'),'run','--project',str(HERE.parent/'foundation-public-metadata/FoundationPublicMetadata.csproj'),'--configuration','Release','--no-launch-profile'])
            rec=s.data['commands'][-1];raw=Path(rec['stdoutPath']).read_text();value=__import__('json').loads(raw[raw.index('{'):])
            expected=c.read(p.E/'api-shapes-v10.0.12/system-type.json')
            c.require(value['runtimeVersion']=='10.0.12' and value['coreLibSha256']==expected['assemblySha256'],'actual full-SDK metadata runtime/CoreLib pin')
            s.data['actualMetadataBinding']=dict(runtimeVersion=value['runtimeVersion'],coreLibSha256=value['coreLibSha256'],types=len(value['types']))
        elif args.mode=='gate':
            payload(s)
            prior=p.B/'agents/batch2517-task-delay-product-implementation-v1/full-foundation-gate-v6/receipt.json'
            proof=p.O/'batch2517-root-full-gate6-verification-v1.json'
            c.require(c.sha(prior)=='b126b39458bd4ec1275833b6a6b17fb84a62ed61f7f64988c062732a0c9c08b2' and c.sha(proof)=='8369f08fd12e4d3b8daf5937d256f79ac2cda500e895dcc1ba9b8ad6cd24a04d','actual inherited full-gate envelope receipts')
            prior_data=c.read(prior)
            for pin in prior_data['WindowsPowerShellPayload']+prior_data['PowerShell7FullPayload']:c.validate_pin(pin)
            s.data['inheritedGateEnvelopeEvidence']=[c.descriptor(prior),c.descriptor(proof)]
            s.data['shellPayload']=prior_data['WindowsPowerShellPayload']+prior_data['PowerShell7FullPayload']
            gate=p.load('run_token_actual_foundation_gate',HERE.parent/'run-foundation-public-candidate-gate.py')
            s.data['gateSources']=[c.descriptor(HERE.parent/name) for name in ['run-foundation-public-candidate-gate.py',*gate.CHECKS]]
            s.data['gateEnvelope']=dict(childSeconds=1800,ownedOuterSeconds=2100,checkWorkers=3,builderJavaWorkers=2,sdkHeapMiB=512,jdkHeapMiB=256,metadataRollForward='LatestPatch with actual runtime/CoreLib assertion10.0.12; selected Run producers remain Disable/128MiB',scope='Complete inherited public foundation gate; no checks narrowed',resourceFloor='512MiB physical / 16GiB available commit; final sample <=2s; cleanup5s plus finalization1s')
            s.save()
            s.step('compile-bootstrap',[str(p.PYTHON),'-B',str(HERE.parent/'build-idisposable-candidate.py')])
            s.step('foundation-gate',[str(p.PYTHON),'-B',str(HERE.parent/'run-foundation-public-candidate-gate.py')],timeout=1800)
        else:raise ValueError(args.mode)
        if args.jar:c.require(c.descriptor(args.jar)==s.data['candidateJar'],'identical phase JAR')
        s.data.update(status='PASS_'+args.mode.upper(),finalized=True);s.save()
    except BaseException as error:s.data.update(status='FAILED_RETAINED',failure=repr(error),finalized=True);s.save();raise

def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--mode',choices=['baseline','native','native-supplement','build','paired','paired-supplement','private','sample','pure-verifiers','historical','audits','metadata-diagnostic','metadata-corrected','gate'],required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--jar',type=Path);parser.add_argument('--native-receipt',type=Path);parser.add_argument('--inner',action='store_true')
    parser.add_argument('--only')
    args=parser.parse_args();c.confined(args.out)
    if args.inner:inner(args);return
    outer=args.out.with_name(args.out.name+'-outer');p.prepare(outer)
    p.write(outer/'invocation.json',dict(argv=sys.argv,source=c.descriptor(__file__),guard=c.descriptor(p.OLD/'owned_process.py')))
    argv=[str(p.PYTHON),'-B',str(HERE/'qualify.py'),*sys.argv[1:],'--inner']
    # The inherited full foundation gate may consume 1800s. Its owned outer
    # envelope must include that budget plus setup/admission/cleanup overhead.
    timeout=2100 if args.mode=='gate' else 1800
    def update(record):p.write(outer/'controller.json',record)
    rec=launch(argv,outer,'controller',timeout,time.monotonic()+timeout+165,update);update(rec);c.successful(rec)
    result=c.read(args.out/'receipt.json');c.require(result['status']=='PASS_'+args.mode.upper(),'phase completion')
    print(result['status'],c.sha(args.out/'receipt.json'))

if __name__=='__main__':main()
