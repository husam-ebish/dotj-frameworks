"""Pure selected reader: exact native fields, owned commands and one compiled JAR."""
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q
p=q.p;c=p.c;HERE=Path(__file__).resolve().parent
COMPILED_ROOT=p.B/'worktrees/dotj-core-task-wait-async-v1'

def command(rec,expected=0,outer=False):
    label='controller' if outer else rec['label']
    c.successful(rec,expected)
    c.require(type(rec['processId']) is int and rec['processId']>0,'owned positive process ID')
    c.require(rec['cleanupLimitSeconds']==5 and 0<=rec['cleanupSeconds']<=5 and rec['outputPollSeconds']==0.1,'owned cleanup/output bounds')
    c.require(0<=rec['resourceSampleAgeSeconds']<=2 and p.guard.resource_ready(rec['resources'][-1]),'fresh physical/commit admission')
    policy=dict(physicalFloorBytes=512*1024**2,availableCommitFloorBytes=16*1024**3,availableCommitField='ullAvailPageFile',maximumWaitSeconds=120,maximumSampleAgeSeconds=2)
    c.require(rec['resourcePolicy']==policy,'resource policy')
    timeout=1800 if outer or label=='foundation-gate' else 60 if label.startswith('native-pass') else 120
    c.require(rec['timeoutSeconds']==timeout and rec['outputLimitsBytes']==p.guard.OUTPUT_LIMITS[p.guard.output_profile(label)],'fixed child/output limits')
    out=Path(rec['cwd']);env=p.frozen_phases.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
    if label in ['foundation-gate','compile-bootstrap']:env=q.prior.full_gate_environment(out)
    c.require(rec['environment']==env,'exact explicit D environment')
    for name,pin in rec['streams'].items():
        c.validate_pin(pin);c.require(pin['path']==rec[name+'Path'] and pin['sizeBytes']==rec['outputSizesBytes'][name],'complete actual stream')
        c.require(Path(pin['path'])==out/(label+'.'+name) and pin['sizeBytes']<=rec['outputLimitsBytes'][name],'bounded owned stream path')

def phase(pin,status,jar=None):
    c.validate_pin(pin);r=c.read(pin['path']);c.require(r['status']==status and r['finalized'] is True,'actual finalized phase completion')
    if jar:c.require(r['candidateJar']==jar,'same final JAR descriptor')
    for pair in r['inputs']:
        c.validate_pin(pair['durable']);c.require(all(pair['original'][k]==pair['durable'][k] for k in ['sha256','sizeBytes']),'exact executed input snapshot')
    c.validate_pin(r['guard']);c.require(r['guard']['sha256']=='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125','unchanged owned guard')
    for rec in r['commands']:command(rec,1 if rec['label']=='compile-baseline' else 0)
    out=Path(pin['path']).parent;outer=out.with_name(out.name+'-outer');controller=c.read(outer/'controller.json')
    command(controller,0 if status.startswith('PASS_') else 1,outer=True)
    invocation=c.read(outer/'invocation.json');producer=next(x for x in r['inputs'] if Path(x['original']['path']).name=='qualify.py')
    c.require(invocation['source']['sha256']==producer['durable']['sha256'],'actual outer/inner producer version')
    c.require(controller['argv']==[str(p.PYTHON),'-B',invocation['source']['path'],*invocation['argv'][1:],'--inner'],'actual owned outer argv')
    return r

def compiled_source_inventory(artifact,jar,build_pin):
    c.validate_pin(build_pin);build=c.read(build_pin['path'])
    def inventory(rows,absolute):
        values={}
        for row in rows:
            value=Path(row['path']);c.require(value.is_absolute()==absolute,'compiled source inventory path kind')
            resolved=value.resolve() if absolute else (COMPILED_ROOT/value).resolve()
            c.require(resolved.is_relative_to(COMPILED_ROOT),'compiled source inventory path escape')
            key=resolved.relative_to(COMPILED_ROOT).as_posix().casefold();c.require(key not in values,'duplicate compiled source inventory path '+key);values[key]=row['sha256']
        c.require(values,'empty compiled source inventory');return values
    trusted=inventory(build['sourceClosure'],True);declared=inventory(artifact['productSources'],False)
    c.require(trusted==declared,'compiled source inventory membership/hash mismatch')
    compiler=build['commands'][0];paths=[row['path'] for row in build['sourceClosure']]
    expected=[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(Path(compiler['cwd']))],'-encoding','UTF-8','--release','21','-d',str(COMPILED_ROOT/'dotj-core/dotj-core-public/build/foundation-v1/classes'),*paths]
    c.require(compiler['label'].startswith('compile-javac-') and compiler['argv']==expected,'compiled source inventory exact actual compiler argv')
    phase(build_pin,'PASS_BUILD',jar)
    for pin in build['sourceClosure']:c.validate_pin(pin)
    return trusted

def qualified_artifact(artifact,jar,source_root,build_pin,canonical_root=Path('C:/source/repos/dotj Frameworks')):
    inventory=compiled_source_inventory(artifact,jar,build_pin);root=Path(source_root).resolve();current=root/artifact['jarPath']
    c.require(artifact['jarSha256']==jar['sha256'],'qualified artifact identity')
    for row in artifact['productSources']:c.require(c.sha(root/row['path'])==row['sha256'],'complete current product source closure '+row['path'])
    if current.is_file():
        c.require(c.sha(current)==jar['sha256'],'present current JAR mismatches; no archive fallback');return current,'ACTUAL_CURRENT_D_OR_GATE_ARTIFACT'
    c.require(root==Path(canonical_root).resolve(),'actual D/gate JAR required; no archive fallback')
    c.validate_pin(jar);return Path(jar['path']),'ARCHIVED_QUALIFIED_ARTIFACT_FOR_CANONICAL_SOURCE_PROJECTION'

def input_pin(r,pin):
    try:c.validate_pin(pin);return Path(pin['path'])
    except (ValueError,FileNotFoundError):
        matches=[pair for pair in r['inputs'] if pair['original']==pin]
        c.require(len(matches)==1,'exact consumed fixture archive');c.validate_pin(matches[0]['durable']);return Path(matches[0]['durable']['path'])

def groups(r):
    jar=r['candidateJar']['path']
    for group in r['groups']:
        for pin in group['fixture']:input_pin(r,pin)
        for pin in group['classes']+group['payloads']:c.validate_pin(pin)
        name=group['name'];prefix='run-'+name+'-'
        records=[rec for rec in r['commands'] if rec['label']=='compile-'+name or rec['label'].startswith(prefix) and rec['label'][len(prefix):].isdigit()]
        c.require(records and records[0]['label']=='compile-'+name,'closed consumer command order')
        rec=records[0];out=Path(rec['cwd']);args=rec['argv'];module='--module-path' in args
        c.require(module==(name in ['paired','paired-supplement','paired-validation','sample','run-token','run-token-supplement','run-token-association','delay']),'fixed selected module/classpath mode')
        pathargs=['--module-path',jar,'--add-modules','dotj.core.foundation.v1'] if module else ['-cp',jar]
        expected=[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(out)],'-parameters','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),*pathargs,'-d',str(out/'classes'),*[pin['path'] for pin in group['fixture']]]
        c.require(args==expected and not list((out/'empty-sourcepath').iterdir()),'exact JAR-only consumer compilation argv')
        actual=sorted((out/'classes').rglob('*.class'));c.require({str(x) for x in actual}=={pin['path'] for pin in group['classes']},'exact consumed class inventory')
        c.require(actual and all(x.name.startswith(tuple(Path(pin['path']).stem for pin in group['fixture'])) for x in actual),'fixture-only classes; no product source fallback')
        cp=['--module-path',jar,'--add-modules','dotj.core.foundation.v1','-cp',str(out/'classes')] if module else ['-cp',str(out/'classes')+os.pathsep+jar]
        prefix=[str(p.JDK/'bin/java.exe'),*p.frozen_phases.jvm(out),*cp]
        modes=runtime_modes(name,out,jar,group)
        c.require(len(records)==1+len(modes),'exact closed runtime count')
        for rec,(owner,arguments) in zip(records[1:],modes):
            c.require(rec['argv']==prefix+[owner,*arguments],'exact same-JAR runtime argv')
            c.require(Path(rec['stderrPath']).read_bytes()==b'','no hidden runtime diagnostic')
        if name in ['delegate-action-v1','public-cancellation-v1','public-valuetask-v1']:c.require(group['payloads']==[c.descriptor(out/'observations.txt')],'legacy actual payload output argument')
        else:c.require(group['payloads']==[rec['streams']['stdout'] for rec in records[1:]],'payload binds actual runtime stdout')

def runtime_modes(name,out,jar,group):
    owner=Path(group['fixture'][0]['path']).stem
    expected=str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/expected-public-surface-v1.txt')
    if name=='paired':return [(owner,[jar,str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/matrix-v2.tsv')])]
    if name=='paired-validation':return [(owner,[jar,str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/validation-boundary-v1.tsv')])]
    if name in ['paired-supplement','observation-paired']:return [(owner,[jar])]
    if name=='observation-controls':return [('WaitAsyncObservationControls',[jar])]
    if name=='private':return [('System.Threading.Tasks.TaskWaitAsyncControls',[jar]),('System.Threading.Tasks.TaskWaitAsyncControls',[jar,'fresh'])]
    if name in ['run-token','run-token-supplement','run-token-association','valuetask-task','task','worktask','sample']:return [(owner,[jar])]
    if name in ['run-token-private','run-token-association-private','task-boundaries']:return [('System.Threading.Tasks.'+owner,[jar])]
    if name=='retained-delay-sample':return [('DelayCancellationSample',[jar])]
    if name=='valuetask-boundaries':return [('ValueTaskTaskBoundaryControls',[mode,jar,expected]) for mode in ['controls','task-first','configured-first','conversion-first']]
    if name=='worktask-boundaries':return [('System.Threading.Tasks.WorkTaskBoundaryControls',[jar]),('System.Threading.CancelAsyncBoundaryControls',[jar])]
    if name in ['delegate-action-v1','public-cancellation-v1','public-valuetask-v1']:return [(owner,[str(out/'observations.txt')])]
    if name=='delay':return [('PublicTaskDelayProductFixtures',[str(p.FROZEN/'fixture-manifest.json'),str(p.HERE/'case-inputs.tsv'),part,jar]) for part in ['ordinary','async']]
    if name=='delay-private':return [('System.Threading.Tasks.TaskDelayProductControls',[jar,str(n)]) for n in range(1,10)]
    raise ValueError('unrecognized consumer group '+name)

def native_commands(native):
    records=native['commands'];c.require([rec['label'] for rec in records]==['sdk-version','compile-native','installed-metadata','native-pass1','native-pass2'],'exact closed native command plan')
    out=Path(native['compiledNative'][0]['path']).parent;dotnet=p.B/'toolchains/dotnet';launcher=str(dotnet/'dotnet.exe')
    c.require(records[0]['argv']==[launcher,'--version'],'actual SDK version argv')
    oracle=COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/PublicTaskWaitAsyncOracle.cs'
    expected=[launcher,'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(out/'PublicTaskWaitAsyncOracle.dll'),*['-r:'+pin['path'] for pin in native['references']],str(oracle)]
    c.require(records[1]['argv']==expected,'exact direct native compiler argv and reference inventory')
    pin=next(pair['original'] for pair in native['inputs'] if Path(pair['original']['path']).name==oracle.name);input_pin(native,pin)
    runtime=[launcher,'exec','--runtimeconfig',str(out/'PublicTaskWaitAsyncOracle.runtimeconfig.json'),str(out/'PublicTaskWaitAsyncOracle.dll')]
    c.require(records[2]['argv']==runtime+['--metadata'],'exact installed metadata execution')
    for rec in records[3:]:c.require(rec['argv']==runtime+[str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/matrix-v2.tsv')],'exact native matrix execution')
    for rec in records:c.require(Path(rec['stderrPath']).read_bytes()==b'','native diagnostic not hidden')
    c.validate_pin(native['payloadManifest'])
    consumed=[p.PYTHON,dotnet/'dotnet.exe',dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll',dotnet/'shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll',p.JDK/'bin/java.exe',p.JDK/'bin/javac.exe']
    for path in consumed:
        pins=[pin for pin in native['payload'] if Path(pin['path'])==path];c.require(len(pins)==1,'actual installed consumed tool payload');c.validate_pin(pins[0])

def supplements(e,jar):
    c.validate_pin(e['supplementFreeze']);lock=c.read(e['supplementFreeze']['path'])
    for pin in lock['files']:c.validate_pin(pin)
    fields=cases=0
    for item in e['supplements']:
        boundary=item['kind']=='validation';native=phase(item['native'],'PASS_NATIVE-VALIDATION' if boundary else 'PASS_NATIVE-SUPPLEMENT');paired=phase(item['paired'],'PASS_PAIRED-VALIDATION' if boundary else 'PASS_PAIRED-SUPPLEMENT',jar);groups(paired)
        dotnet=p.B/'toolchains/dotnet';launcher=str(dotnet/'dotnet.exe');out=Path(item['native']['path']).parent
        if boundary:
            c.validate_pin(native['nativeProducer']);c.require(native['nativeProducer']==e['native'],'same frozen primary native compiler producer')
            for pin in native['importedNativeAssembly']:c.validate_pin(pin)
            prefix=[launcher,'exec','--runtimeconfig',str(q.A/'native-v2/PublicTaskWaitAsyncOracle.runtimeconfig.json'),str(q.A/'native-v2/PublicTaskWaitAsyncOracle.dll'),str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/validation-boundary-v1.tsv')]
            c.require([rec['label'] for rec in native['commands']]==['native-pass1','native-pass2'],'closed boundary native execution plan')
        else:
            c.validate_pin(native['runtimeConfig']);c.validate_pin(native['compiledNative'])
            for pin in native['references']:c.validate_pin(pin)
            compile_expected=[launcher,'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(out/'SupplementWaitAsyncOracle.dll'),*['-r:'+pin['path'] for pin in native['references']],str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/SupplementWaitAsyncOracle.cs')]
            c.require([rec['label'] for rec in native['commands']]==['compile-native','native-pass1','native-pass2'] and native['commands'][0]['argv']==compile_expected,'closed supplemental direct native compiler plan')
            prefix=[launcher,'exec','--runtimeconfig',str(out/'SupplementWaitAsyncOracle.runtimeconfig.json'),str(out/'SupplementWaitAsyncOracle.dll')]
        actual=q.prior.wire(Path(paired['groups'][0]['payloads'][0]['path']).read_bytes());q.supplement_schema(actual,boundary)
        captures=[rec for rec in native['commands'] if rec['label'].startswith('native-pass')];c.require(len(captures)==2,'two supplemental native passes')
        for rec in captures:c.require(rec['argv']==prefix and Path(rec['stderrPath']).read_bytes()==b'' and actual==q.prior.wire(Path(rec['stdoutPath']).read_bytes()),'exact supplemental typed native comparison/argv')
        c.require(native['cases']==(80 if boundary else 17) and len(actual)==(1840 if boundary else 340),'complete supplementary cells')
        cases+=native['cases'];fields+=len(actual)
    c.require([row['kind'] for row in e['supplements']]==['source-disposal','validation'],'both required supplemental matrices')
    return cases,fields

def history(e,jar):
    selected=[]
    for item in e['historicalPhases']:
        r=phase(item['receipt'],item['status'],jar);groups(r)
        selected.extend(group for group in r['groups'] if group['name'] in item['acceptedGroups'])
    names=['valuetask-task','valuetask-boundaries','task','task-boundaries','worktask','worktask-boundaries','delegate-action-v1','public-cancellation-v1','public-valuetask-v1','delay','delay-private','run-token','run-token-supplement','run-token-association','run-token-private','run-token-association-private']
    c.require([g['name'] for g in selected]==names,'complete ordered selected historical groups')
    by={g['name']:g for g in selected}
    predecessor=c.read(e['predecessorEvidence']['path']);references={}
    c.validate_pin(predecessor['historicalCurrent']);previous_phase=c.read(predecessor['historicalCurrent']['path'])
    for group in previous_phase['groups']:references[group['name']]=group
    for name in names[:11]:
        current=by[name];old=references[name]
        if name in ['task-boundaries','worktask-boundaries','valuetask-boundaries','delay-private']:
            c.require([Path(x['path']).read_bytes() for x in current['payloads']]==[p.resolve(x).read_bytes() for x in old['payloads']],'retained exact private raw output '+name)
        elif name=='delay':
            schema=c.read(p.FROZEN/'schema.json');manifest=c.read(p.FROZEN/'fixture-manifest.json');actual={};before={}
            for new_pin,old_pin,part in zip(current['payloads'],old['payloads'],['ordinary','async']):
                actual.update(c.wire(Path(new_pin['path']).read_bytes(),schema,manifest,part));before.update(c.wire(p.resolve(old_pin).read_bytes(),schema,manifest,part))
            c.compare(actual,before,manifest)
        else:
            # Frozen successful native-paired producer already establishes the exact
            # typed corpus. Reparse its raw fields without replaying old producers.
            a=Path(current['payloads'][0]['path']).read_text(encoding='utf-8').splitlines();b=p.resolve(old['payloads'][0]).read_text(encoding='utf-8').splitlines();c.require(a==b,'all retained observed fields '+name)
    for name,key in [('run-token','native'),('run-token-supplement','nativeSupplement'),('run-token-association','nativeAssociation')]:
        c.validate_pin(predecessor[key]);native=c.read(predecessor[key]['path']);actual=q.prior.wire(Path(by[name]['payloads'][0]['path']).read_bytes())
        for rec in [r for r in native['commands'] if r['label'].startswith('native-pass')]:
            c.validate_pin(rec['streams']['stdout']);c.require(actual==q.prior.wire(Path(rec['stdoutPath']).read_bytes()),'retained complete Run matrix '+name)
    for name,wanted in [('run-token-private',23),('run-token-association-private',6)]:
        markers=Path(by[name]['payloads'][0]['path']).read_text().splitlines();c.require(len(markers)==wanted and len(set(markers))==wanted and all(x.endswith('\tb\ttrue') for x in markers),'retained Run private controls')
    return len(selected)

def observation_payload(payload):
    q.observation_schema(payload);matrix=c.read(HERE/'observation-matrix-v1.json')
    def field(row,name,kind,value):c.require(payload[row+'.'+name]==(kind,str(value).lower() if type(value) is bool else str(value)),'direct observation '+row+'.'+name)
    for name in ['waitSameThread','waitInCancel','waitInline','waitSawCanceled','sourceSameThread','waitUnaffectedBySource']:field('O001',name,'b',True)
    field('O001','sourceInCancel','b',False)
    for name in ['waitCallbacks','sourceCallbacks']:field('O001',name,'i',1)
    types={'success':'null','fault':'System.InvalidOperationException','source-cancel':'System.Threading.Tasks.TaskCanceledException','caller-cancel':'System.Threading.Tasks.TaskCanceledException','timeout':'System.TimeoutException'}
    for row in matrix['rows'][1:]:
        id=row['id'];outcome=row['outcome'];identity=outcome in ['fault','timeout'];cancel=outcome.endswith('cancel')
        field(id,'receiverAlias','b',row['shape']=='alias')
        for name in ['asTaskIdentity','preserveIdentity']:field(id,name,'b',True)
        for prefix in ['normal','configured']:
            field(id,prefix+'Type','s',types[outcome]);field(id,prefix+'Succeeded','b',outcome=='success')
            field(id,prefix+'StoredIdentity','s','same' if identity else 'not-applicable')
            field(id,prefix+'TokenMatch','s','equal' if cancel else 'not-applicable');field(id,prefix+'TaskMatch','s','same' if cancel else 'not-applicable');field(id,prefix+'Matches','b',True)

def observations(e,jar):
    correction=e['observationCorrection'];c.require(correction['status']=='POST_GATE_EVIDENCE_STRENGTHENING' and correction['productUnchanged'] is True,'explicit post-gate observation correction')
    c.validate_pin(correction['freeze']);lock=c.read(correction['freeze']['path'])
    c.require(lock['candidateJar']==jar,'frozen same product JAR')
    for pin in lock['files']:c.validate_pin(pin)
    native=phase(correction['native'],'PASS_OBSERVATION-NATIVE',jar);paired=phase(correction['paired'],'PASS_OBSERVATION-PAIRED',jar);controls=phase(correction['controls'],'PASS_OBSERVATION-CONTROLS',jar)
    groups(paired);groups(controls)
    for r in [native,paired,controls]:
        c.require(r['matrixFreeze']==correction['freeze'],'executed observation freeze')
        for pin in lock['files']:
            pair=next((pair for pair in r['inputs'] if pair['original']==pin),None);c.require(pair is not None,'frozen fixture was actual executed phase input');c.validate_pin(pair['durable'])
    for pin in native['references']+[native['runtimeConfig'],native['compiledNative'],native['inheritedInstalledPayload']]:c.validate_pin(pin)
    prior=c.read(native['inheritedInstalledPayload']['path']);c.require(native['references']==prior['references'] and native['inheritedInstalledPayload']==e['native'],'same installed selected native references')
    c.require(c.read(native['runtimeConfig']['path'])==c.read(prior['compiledNative'][1]['path']),'unchanged runtime Disable configuration')
    out=Path(correction['native']['path']).parent;dotnet=p.B/'toolchains/dotnet'
    compiler=[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(out/'WaitAsyncObservationOracle.dll'),*['-r:'+pin['path'] for pin in native['references']],str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/WaitAsyncObservationOracle.cs')]
    c.require([r['label'] for r in native['commands']]==['compile-native','native-pass1','native-pass2'] and native['commands'][0]['argv']==compiler,'closed actual observation native compiler')
    runtime=[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(out/'WaitAsyncObservationOracle.runtimeconfig.json'),str(out/'WaitAsyncObservationOracle.dll')]
    actual=q.prior.wire(Path(paired['groups'][0]['payloads'][0]['path']).read_bytes());observation_payload(actual)
    c.require(native['cases']==11 and native['fields']==159 and native['nativePasses']==2,'complete finite observation matrix')
    for rec in native['commands'][1:]:c.require(rec['argv']==runtime and Path(rec['stderrPath']).read_bytes()==b'' and q.prior.wire(Path(rec['stdoutPath']).read_bytes())==actual,'two exact typed observation native captures')
    observed=q.prior.wire(Path(controls['groups'][0]['payloads'][0]['path']).read_bytes());wanted={'actual-positive-shared-observer','queued-published-canceled','queued-before-return-not-inline','source-inline-cannot-overwrite-queued-wait','late-published-before-observation','same-thread-after-return-not-inline','source-cannot-overwrite-late-wait','wrong-token-rejected','wrong-task-rejected','actual-valuetask-stored-fault-accepted','same-class-wrong-fault-object-rejected','wrong-timeout-object-rejected','success-with-error-rejected','nonapplicable-facets-explicit'}
    c.require(set(observed)==wanted|{key for key in actual if key.startswith('O001.')} and all(observed[key]==('b','true') for key in wanted),'actual shared observation controls complete')
    c.require(all(observed[key]==value for key,value in actual.items() if key.startswith('O001.')),'controls use actual positive observer')
    return dict(cases=11,fields=159,sharedControls=14,chronology='POST_GATE_EVIDENCE_STRENGTHENING')

def validate(e,artifact_override=None,source_root=None,canonical_root=Path('C:/source/repos/dotj Frameworks')):
    c.require(e['status']=='SELECTED_BEHAVIOR_CHECKS_PASSED','selected evidence status');jar=e['candidateJar'];c.validate_pin(jar)
    c.validate_pin(e['reader']);c.require(c.sha(HERE/'verify_candidate.py')==e['reader']['sha256'],'actual final reader version')
    for item in e['toolPins']:
        c.validate_pin(item['pin']);c.require(c.sha(p.ROOT/item['relativePath'])==item['pin']['sha256'],'actual current selected tool/schema bytes '+item['relativePath'])
    artifact=artifact_override if artifact_override is not None else c.read(p.E/'foundation-product-candidate-v1.json')
    chosen,provenance=qualified_artifact(artifact,jar,source_root or p.ROOT,e['build'],canonical_root)
    c.require(q.surface(Path(jar['path']))==e['publicSurface'],'exact complete compiled public surface delta')
    c.validate_pin(e['contract']);contract=c.read(e['contract']['path']);c.require(contract['acceptanceCredit']==0 and len(contract['publicSurface']['taskAdditions'])==3,'selected contract scope')
    c.validate_pin(e['sourcePinArchive']);archive=c.read(e['sourcePinArchive']['path'])
    for pair in archive['entries']:c.validate_pin(pair['durable']);c.require(all(pair['original'][k]==pair['durable'][k] for k in ['sha256','sizeBytes']),'source pin original/copy equality')
    c.require({(x['path'],x['sha256'],x['sizeBytes']) for x in contract['sourcePins']}=={(pair['original']['path'],pair['original']['sha256'],pair['original']['sizeBytes']) for pair in archive['entries']},'complete adopted source pin archive')
    baseline=phase(e['baseline'],'PASS_BASELINE');c.require(baseline['baselineJar']['sha256']==q.BASELINE_SHA,'actual retained predecessor')
    rec=baseline['commands'][0];out=Path(rec['cwd'])
    c.require(rec['argv']==[str(p.JDK/'bin/javac.exe'),*['-J'+x for x in p.frozen_phases.jvm(out)],'-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-cp',str(q.BASELINE),'-d',str(out/'classes'),str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/BaselineWaitAsync.java')] and not list((out/'classes').rglob('*.class')),'actual isolated predecessor compiler argv/no fixture classes')
    diagnostic=Path(baseline['commands'][0]['stderrPath']).read_text();c.require(diagnostic.count('symbol:   method WaitAsync')==3 and 'symbol:   class TimeoutException' in diagnostic and '4 errors' in diagnostic,'actual predecessor refusal')
    native=phase(e['native'],'PASS_NATIVE');paired=phase(e['paired'],'PASS_PAIRED',jar);groups(paired)
    native_commands(native)
    for pin in native['compiledNative']+native['references']+native['bootstrapInputs']:c.validate_pin(pin)
    config=c.read(next(pin['path'] for pin in native['bootstrapInputs'] if pin['path'].endswith('runtimeconfig.json')))
    c.require(config['runtimeOptions']['rollForward']=='Disable' and config['runtimeOptions']['framework']['version']=='10.0.12','locked selected runtime')
    c.require(Path(native['commands'][0]['stdoutPath']).read_text().strip()=='10.0.401','actual SDK10.0.401')
    metadata=Path(next(rec for rec in native['commands'] if rec['label']=='installed-metadata')['stdoutPath']).read_text()
    c.require('runtime=10.0.12' in metadata and 'corelib=1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' in metadata and metadata.count(' WaitAsync(')==5 and metadata.count('Void .ctor(')==3,'actual installed metadata and CoreLib pin')
    actual=q.prior.wire(Path(paired['groups'][0]['payloads'][0]['path']).read_bytes());q.validate_schema(actual)
    captures=[rec for rec in native['commands'] if rec['label'].startswith('native-pass')];c.require(len(captures)==2,'two actual native passes')
    for rec in captures:c.require(actual==q.prior.wire(Path(rec['stdoutPath']).read_bytes()),'every exact typed native field')
    c.require(len(actual)==8510 and e['primaryCases']==390 and e['primaryFields']==8510,'complete retained primary matrix counts')
    c.validate_pin(contract['matrix']);c.validate_pin(contract['matrixFreeze'])
    for pin in c.read(contract['matrixFreeze']['path'])['files']:input_pin(native,pin)
    added_cases,added_fields=supplements(e,jar)
    c.require(e['nativeCases']==390+added_cases==487 and e['nativeFields']==8510+added_fields==10690,'complete combined native matrix counts')
    private=phase(e['private'],'PASS_PRIVATE',jar);groups(private);markers=[line for pin in private['groups'][0]['payloads'] for line in Path(pin['path']).read_text().splitlines()]
    wanted={'J01-fresh-context','J02-validation-resource-free',*{'J03-publication-'+str(n) for n in range(6)},'J04-all-20-ordered-pairs','J05-eight-bounded-three-way-races','J06-exact-removal-and-late','J07-after-detach-loser-harmless','J08-mixed-original-order','J09-blocked-first-and-later-user','J10-terminal-before-cleanup','J11-blocking-disposal-no-task-lock','J12-self-disposal','J13-timer-construction-before-after-winner','J14-partial-construction-cleanup-failure','J15-delay-async-source-normal-wrapper','J16-held-run-token-ownership','J17-rejection-handler-finally-context','J18-dispatch-failure-preserves-winner','J19-dispatch-and-cleanup-failure','J20-mixed-runtime-failure-isolation','J21-five-contender-bounded-race','J22-registrar-failure-after-source-or-timeout-winner'}
    c.require(len(markers)==len(wanted) and set(markers)=={name+'\tb\ttrue' for name in wanted},'complete private control inventory')
    c.validate_pin(e['predecessorEvidence']);historical=history(e,jar)
    sample=phase(e['sample'],'PASS_SAMPLE',jar);groups(sample);sample_actual=q.prior.wire(Path(sample['groups'][0]['payloads'][0]['path']).read_bytes())
    for pin in sample['sampleNativeInputs']:c.validate_pin(pin)
    c.validate_pin(sample['sampleNativeAssembly']);sample_out=Path(sample['sampleNativeAssembly']['path']).parent;dotnet=p.B/'toolchains/dotnet'
    sample_refs=sample['sampleNativeInputs'][2:]
    c.require(sample['commands'][0]['argv']==[str(dotnet/'dotnet.exe'),'exec',str(dotnet/'sdk/10.0.401/Roslyn/bincore/csc.dll'),'-nologo','-noconfig','-nostdlib','-target:exe','-deterministic','-nullable:enable','-langversion:14','-warnaserror','-out:'+str(sample_out/'WaitAsyncSample.dll'),*['-r:'+pin['path'] for pin in sample_refs],str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/WaitAsyncSample.cs')],'exact paired sample native compiler argv')
    sample_captures=[rec for rec in sample['commands'] if rec['label'].startswith('sample-native-pass')];c.require(len(sample_captures)==2 and len(sample_actual)==6,'paired sample inventory')
    for rec in sample_captures:
        c.require(rec['argv']==[str(dotnet/'dotnet.exe'),'exec','--runtimeconfig',str(sample_out/'WaitAsyncSample.runtimeconfig.json'),str(sample_out/'WaitAsyncSample.dll')],'exact paired sample native runtime argv')
        c.require(sample_actual==q.prior.wire(Path(rec['stdoutPath']).read_bytes()),'paired sample exact native fields')
    c.require(Path(sample['groups'][1]['payloads'][0]['path']).read_text().splitlines()==['sample.success\tb\ttrue','sample.canceled\tb\ttrue'],'retained same-JAR Delay sample')
    c.validate_pin(e['preservation']);preservation=c.read(e['preservation']['path'])
    for pin in preservation['retainedGuaranteeInputs']:c.validate_pin(pin)
    c.require(len(preservation['guaranteeDispositions'])>=11 and preservation['acceptanceCredit']==0,'explicit inherited guarantee dispositions')
    for key in ['changedPredicateControls','projectionControls']:
        pin=preservation[key];c.validate_pin(pin);control=c.read(pin['path']);c.require(control['status']=='PASS' and all(row['passed'] for row in control['controls']),'retained predecessor negative guarantees '+key)
    c.validate_pin(preservation['verbatimExportManifest'])
    for pair in c.read(preservation['verbatimExportManifest']['path']):
        p.resolve(pair['export']);c.require(all(pair['original'][key]==pair['export'][key] for key in ['sha256','sizeBytes']),'retained exact original/export hash and size pair')
    successor=c.read(e['historicalSuccessors']['path']);c.validate_pin(e['historicalSuccessors'])
    for pair in successor['entries']:c.validate_pin(pair['original']);c.validate_pin(pair['successor'])
    packet=c.read(p.E/'foundation-e01-review-packet-v1.json');c.require(packet['candidateJarSha256']==jar['sha256'] and len(packet['openDecisions'])==3 and all(row['status']=='OPEN' for row in packet['openDecisions']),'same final artifact all three E01 OPEN')
    c.require(e['acceptanceCredit']==0 and e['acceptedTasks']=='0/1092 (0%)' and e['openAcceptanceItems']==1686 and e['qualifiedFrameworks']=='0/66','no invented acceptance credit')
    if 'negativeControls' in e:
        c.validate_pin(e['negativeControls']);controls=c.read(e['negativeControls']['path']);c.require(controls['status']=='PASS' and len(controls['controls'])==47 and all(row['passed'] for row in controls['controls']),'actual new consumed predicate/source/artifact negative controls')
        previous=e['reviewedReader'];c.validate_pin(previous['durable']);c.require(all(previous['original'][k]==previous['durable'][k] for k in ['sha256','sizeBytes']),'actual reviewed reader retained')
        c.require(controls['reader']==previous['original'] and controls['source']['sha256']==c.sha(HERE/'verify-negative-controls.py'),'historical 47 controls retain actual reviewed source/reader version')
        owned=phase(e['negativePhase'],'PASS_NEGATIVE',jar);c.validate_pin(owned['selectedEvidenceInput']);c.require([rec['label'] for rec in owned['commands']]==['negative-controls'],'owned pure-control command plan')
        c.require(owned['commands'][0]['argv']==[str(p.PYTHON),'-B',str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/verify-negative-controls.py'),str(Path(e['negativeControls']['path']).parent)],'actual owned pure-control argv')
    observation=observations(e,jar)
    proof=phase(e['observationCorrection']['proofControlsPhase'],'PASS_OBSERVATION-PROOF-CONTROLS',jar)
    c.require([r['label'] for r in proof['commands']]==['observation-proof-controls'],'owned observation proof control command')
    proof_out=Path(e['observationCorrection']['proofControlsPhase']['path']).parent
    c.require(proof['commands'][0]['argv']==[str(p.PYTHON),'-B',str(COMPILED_ROOT/'tools/oracle/dotj-core/public-task-wait-async-v1/verify_candidate.py'),'--observation-controls',str(proof_out/'controls')],'actual observation proof controls argv')
    c.validate_pin(e['observationCorrection']['proofControls']);proof_result=c.read(e['observationCorrection']['proofControls']['path'])
    c.require(proof_result['status']=='PASS' and proof_result['reader']==e['reader'] and len(proof_result['controls'])==16 and all(row['passed'] for row in proof_result['controls']),'current actual observation proof controls')
    c.require(proof_result['inputs']=={key:e['observationCorrection'][key] for key in ['native','paired','controls']},'proof controls consume these exact current observations')
    executed=proof_result['selectedEvidenceAtExecution'];c.validate_pin(executed['durable']);c.require(all(executed['original'][key]==executed['durable'][key] for key in ['sha256','sizeBytes']),'actual consumed selected evidence preserved')
    return dict(cases=e['nativeCases'],fields=e['nativeFields'],nativePassesPerMatrix=2,observationCorrection=observation,privateControls=len(markers),historicalGroups=historical,jarSha256=jar['sha256'],artifactProvenance=provenance)

def observation_proof_controls(out):
    import copy
    import shutil
    out=Path(out);out.mkdir();selected=p.E/'public-task-wait-async-v1.json';snapshot=out/'selected-evidence-at-execution.json';shutil.copyfile(selected,snapshot);e=c.read(snapshot);rows=[]
    observations(e,e['candidateJar']);rows.append(dict(name='actual-retained-current-proof-accepted',passed=True))
    paired=c.read(e['observationCorrection']['paired']['path']);actual=q.prior.wire(Path(paired['groups'][0]['payloads'][0]['path']).read_bytes())
    mutations=[('O001.waitSameThread',('b','false')),('O001.waitInCancel',('b','false')),('O001.waitSawCanceled',('b','false')),('O001.waitUnaffectedBySource',('b','false')),('O001.waitCallbacks',('i','2')),('O003.normalStoredIdentity',('s','different')),('O006.configuredStoredIdentity',('s','different')),('O004.normalTokenMatch',('s','different')),('O005.configuredTaskMatch',('s','different')),('O002.normalStoredIdentity',('s','same'))]
    def refused(name,fn):
        try:fn()
        except (ValueError,KeyError,FileNotFoundError):rows.append(dict(name=name,passed=True));return
        raise ValueError('control unexpectedly accepted '+name)
    for key,value in mutations:
        changed=dict(actual);changed[key]=value;refused('reject-'+key,lambda changed=changed:observation_payload(changed))
    changed=dict(actual);changed.pop('O001.waitInCancel');refused('missing-direct-boundary-refused',lambda:observation_payload(changed))
    changed=dict(actual);changed['O001.waitInCancel']=('s','true');refused('wrong-typed-boundary-refused',lambda:observation_payload(changed))
    for key,value in [('productUnchanged',False),('status','PASS')]:
        changed=copy.deepcopy(e);changed['observationCorrection'][key]=value;refused('reject-correction-'+key,lambda changed=changed:observations(changed,changed['candidateJar']))
    changed=copy.deepcopy(e);changed['observationCorrection']['freeze']['sha256']='0'*64;refused('changed-frozen-source-proof-refused',lambda:observations(changed,changed['candidateJar']))
    p.write(out/'receipt.json',dict(status='PASS',reader=c.descriptor(__file__),selectedEvidenceAtExecution=dict(original=c.descriptor(selected),durable=c.descriptor(snapshot)),controls=rows,inputs=dict(native=e['observationCorrection']['native'],paired=e['observationCorrection']['paired'],controls=e['observationCorrection']['controls']),acceptanceCredit=0))
    print('PASS current observation proof controls',len(rows))

def main():
    if len(sys.argv)==3 and sys.argv[1]=='--observation-controls':observation_proof_controls(sys.argv[2]);return
    print('PASS selected nongeneric Task.WaitAsync: '+str(validate(c.read(p.E/'public-task-wait-async-v1.json'))))
if __name__=='__main__':main()
