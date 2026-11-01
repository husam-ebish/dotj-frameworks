"""Versioned packaged cache qualification. Never launches native observers."""
import argparse, datetime, importlib.util, json, os, shutil, subprocess, time, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parents[3]
B = Path(r'D:\AI\Implementation\dotj Frameworks')
BASE = R/'dotj-build/evaluation-candidate'
DATA = BASE/'condition-cache-product-v1'
NATIVE = BASE/'condition-cache-v1'
LOCK = B/'validation/Batch-2511-cache-native-pair-v1/observation-lock.json'
LOCK_PIN = '9612d662aa80501614b04475236169d7bb839ef5e0d41b932e2964bd0d2d688c'
BASELINE = B/'validation/Batch-2510-build-condition-packaged-v3-run3/packaged94/dotj-build-evaluation-candidate.jar'
BASELINE_PIN = '253a22a247695295fe6eea07d34fbb71f9b5f059715fde75ac75eb4a2ceba941'
PROBE = BASE/'tests/org/dotj/internal/build/evaluation/ConditionCachePackagedTest.java'
NATIVE_CHECKPOINT = B/'agents/validation-performance/condition-cache-native-preparation-20261101/checkpoint.json'
MODULE = 'org.dotj.build.evaluation.candidate'
PACKAGE = 'org.dotj.internal.build.evaluation'

def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

v3=load('cache_product_frozen_v3_primitives',HERE.parent/'condition-product-v3/verify.py')
native=load('cache_product_frozen_native_validator',HERE.parent/'condition-cache-v1/verify.py')
sha,read,require,info,dump=v3.sha,v3.read,v3.require,v3.info,v3.dump

def observations():
    lock=v3.read_pinned(LOCK,LOCK_PIN)
    _,plan,fp=native.verify_inputs(lock['inputLockSha256'])
    native.verify_checkpoint(NATIVE_CHECKPOINT,lock['checkpointSha256'],lock['inputLockSha256'])
    for key in ['nativeFingerprint','manifest','pairReceipt','independentEvidenceReview']:
        item=lock[key]; require(sha(Path(item['path']))==item['sha256'],'native reference descriptor changed: '+key)
    for item in lock['captures']:
        v3.read_pinned(item['path'],item['sha256'])
        capture=native.validate_capture(item['path'],lock['inputLockSha256'],NATIVE_CHECKPOINT,lock['checkpointSha256'])
        native.bind_stdout(capture['commands'][0]['stdout'],capture['payload'],Path(item['path']).parent)
        native.validate_payload(capture['payload'],plan,fp,capture['fixtureRoot'])
        native.verify_fixtures(Path(capture['fixtureRoot']),plan)
        normalized=v3.old.normalize(capture['payload'],capture['fixtureRoot'])
        require(native.equal(normalized,lock['normalizedPayload']),'raw native payload differs from root reference')
    rows=lock['normalizedPayload']['rows']
    require([len(r['diagnostics']) for r in rows]==[1,0,0,1,1,1,0,1],'observed warning vector differs')
    native.verify_fixtures(NATIVE/'fixtures',plan)
    return rows

def inputs():
    paths=[Path(x['path']) for x in v3.closure()]
    paths += [LOCK,BASELINE,NATIVE_CHECKPOINT]
    return [info(p) for p in sorted(set(paths))]

def checkpoint(path,pin):
    cp=v3.read_pinned(path,pin)
    require(cp['kind']=='CACHE_PRODUCT_V1' and cp['inputs']==inputs(),'candidate checkpoint closure differs')
    require(sha(BASE/'verify.py')==v3.RUNNER_PIN,'canonical94 runner changed')
    require(sha(BASELINE)==BASELINE_PIN,'actual baseline JAR changed')
    return cp

def vm(out):
    return ['-Xms16m','-Xmx128m','-XX:+UseSerialGC','-XX:ActiveProcessorCount=2','-Dfile.encoding=UTF-8','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-XX:HeapDumpPath='+str(out/'logs'),'-XX:ErrorFile='+str(out/'logs/hs_err_pid%p.log')]

def run(label,args,cwd,env,record,save,allow_failure=False):
    # Frozen guarded primitive applies 120 s memory wait, 20 s query and fresh20 Popen.
    try: v3.guarded(label,args,cwd,env,record,save)
    except ValueError:
        command=record['commands'][-1]
        if not allow_failure or type(command.get('exitCode')) is not int or command['exitCode']==0 or command.get('timedOut'): raise
    return record['commands'][-1]

def compile_consumers(out,candidate,tests,record,save):
    originals=[PROBE]
    if tests: originals.append(BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java')
    sources=[]
    for original in originals:
        target=out/'fixture-sources'/original.relative_to(BASE/'tests');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target);sources.append(str(target))
    patch=str(out/'fixture-sources')+(';' + str(tests) if tests else '')
    args=[str(v3.JDK/'bin/javac.exe'),*['-J'+x for x in vm(out)],'--release','21','-encoding','UTF-8','--module-path',str(candidate),'--patch-module',MODULE+'='+patch,'-sourcepath',str(out/'empty-sourcepath'),'-implicit:none','-d',str(out/'consumer-classes'),*sources]
    run('compile-fixture-consumers',args,out/'unrelated-cwd',v3.environment(out),record,save)
    classes={p.relative_to(out/'consumer-classes').as_posix():p.read_bytes() for p in (out/'consumer-classes').rglob('*.class')}
    prefix=PACKAGE.replace('.','/')+'/'
    wanted={prefix+'ConditionCachePackagedTest.class'}
    if tests: wanted|={prefix+'AndConditionTest.class',prefix+'AndConditionTest$Edge.class'}
    require(set(classes)==wanted,'fixture-only compiler emitted unexpected/product classes')
    if tests:
        with zipfile.ZipFile(tests) as archive:
            for name in archive.namelist(): classes.setdefault(name,archive.read(name))
    jar=out/'fixture-tests.jar'
    with zipfile.ZipFile(jar,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(classes.items()): archive.writestr(name,data)
    record['fixtureTestsJar']=info(jar); save();return jar

def verify_consumers(out,tests):
    classes={p.relative_to(out/'consumer-classes').as_posix():p.read_bytes() for p in (out/'consumer-classes').rglob('*.class')}
    prefix=PACKAGE.replace('.','/')+'/'
    wanted={prefix+'ConditionCachePackagedTest.class'}
    if tests:wanted|={prefix+'AndConditionTest.class',prefix+'AndConditionTest$Edge.class'}
    require(set(classes)==wanted,'consumer compilation membership differs')
    if tests:
        with zipfile.ZipFile(tests) as archive:
            for name in archive.namelist():classes.setdefault(name,archive.read(name))
    with zipfile.ZipFile(out/'fixture-tests.jar') as archive:
        require(len(archive.namelist())==len(set(archive.namelist())) and set(archive.namelist())==set(classes),'fixture JAR membership differs')
        require(all(archive.read(name)==value for name,value in classes.items()),'fixture JAR/helper bytes differ')

def consume(name,rows,fixtures,out,candidate,patch,record,save,red=False):
    bridge=out/(name+'-bridge.tsv');bridge.write_bytes(v3.logic_bridge(rows).encode())
    result=out/(name+'-results.tsv')
    argv=[str(v3.JDK/'bin/java.exe'),*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(patch),'-m',MODULE+'/'+PACKAGE+'.ConditionCachePackagedTest',str(bridge),str(fixtures),str(result),str(candidate),name]
    cmd=run('packaged-'+name,argv,out/'unrelated-cwd',v3.environment(out),record,save,red)
    actual=result.read_text().splitlines(); expected=v3.logic_results(rows)
    record[name]={'bridge':info(bridge),'results':info(result),'expected':expected,'actual':actual,'match':actual==expected}
    if red:
        require(cmd['exitCode']!=0 and actual!=expected,'baseline did not exhibit genuine behavioral RED')
        require(len(actual)==len(expected)==8,'RED did not retain all eight results')
        for a,e in zip(actual,expected): require(a.split('\t')[:5]==e.split('\t')[:5],'RED was not isolated to warning behavior')
        require('warning mismatch:' in Path(cmd['stderr']['path']).read_text(),'RED assertion not warning mismatch')
    else: require(cmd['exitCode']==0 and actual==expected,'packaged comparison differs: '+name)
    save()

def validate_result_lines(lines,rows):
    require(type(lines) is list and lines==v3.logic_results(rows),'ordered values/imports/warnings differ')

def validate_commands(record,out):
    commands=[c for c in record['commands'] if c['label']!='unchanged-current94-runner']
    v3.verify_resource_evidence(dict(commands=commands,resources=record['resources'],resourceWaits=record['resourceWaits']))
    for c in record['commands']:
        require(type(c.get('exitCode')) is int,'typed process completion missing')
        for stream in ['stdout','stderr']: v3.validate_descriptor(c[stream],out)
        if c['label']=='unchanged-current94-runner':
            require(c['exitCode']==0 and c['outerTimeoutSeconds']==600,'canonical runner failed')
            require(c['argv']==[str(v3.PYTHON),'-B',str(BASE/'verify.py'),'--out',str(out/'packaged94')] and c['cwd']==str(R),'canonical runner provenance differs')
            require(Path(c['stderr']['path']).read_bytes()==b'' and 'PASS_INTERNAL_PACKAGED_CONTRACT' in Path(c['stdout']['path']).read_text(),'canonical runner raw success missing')
            continue
        require(c['timeoutSeconds']==120 and 0<=c['resourceSampleAgeSeconds']<20 and not c.get('timedOut'),'JVM resource/timeout evidence differs')
        args=c['argv'];require(v3.option(args,'--module-path')==record['candidateJar']['path'],'actual JAR differs')
        compile=c['label'].startswith('compile-');prefix='-J' if compile else ''
        require({prefix+'-Xmx128m',prefix+'-XX:ActiveProcessorCount=2',prefix+'-XX:+UseSerialGC'}.issubset(args),'JVM limits differ')
        require(args[0]==str(v3.JDK/'bin'/('javac.exe' if compile else 'java.exe')) and c['cwd']==str(out/'unrelated-cwd'),'tool/cwd identity differs')
        require(type(c['processId']) is int and c['processId']>0 and 0<=c['seconds']<120,'bounded actual process evidence missing')
        age=(datetime.datetime.fromisoformat(c['launchUtc'])-datetime.datetime.fromisoformat(c['resourceSampleUtc'])).total_seconds()
        require(0<=age<20,'stale resource eligibility')
        if c['label'].startswith('compile-'):
            require(v3.option(args,'-sourcepath')==str(out/'empty-sourcepath') and '-implicit:none' in args,'source fallback allowed')
            require(not list((out/'empty-sourcepath').iterdir()),'source fallback directory is not empty')
        require(not any(x in args for x in ['-cp','-classpath','--add-exports','--add-opens']),'exposure or fallback arguments')
        for key in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','XDG_CACHE_HOME']:
            require(Path(c['environmentOverrides'][key]).is_relative_to(out),'temporary directory outside owned output')

def verify_receipt(file,lockfile,pin):
    lock=v3.read_pinned(lockfile,pin);require(lock['receipt']==info(file),'receipt binding differs')
    for item in lock['inputs']: v3.validate_descriptor(item)
    record=read(file);out=Path(file).parent
    for key,value in receipt_fields().items():require(key in record and native.equal(record[key],value),'qualification count/type differs: '+key)
    checkpoint(record['checkpoint']['path'],record['checkpoint']['sha256'])
    rows=observations();validate_commands(record,out)
    require(record['status'] in ['GENUINE_PACKAGED_BASELINE_RED','PASS_PACKAGED_CACHE_PRODUCT_V1'],'qualification status differs')
    if record['status'].startswith('PASS'):
        require([c['label'] for c in record['commands']]==['unchanged-current94-runner','compile-fixture-consumers','packaged-cache','packaged-condition','packaged-and','packaged-cache-controls'],'command coverage differs')
        candidate,tests=v3.packaged_artifacts(out/'packaged94')
        require(record['candidateJar']==info(candidate),'new JAR identity differs')
        verify_consumers(out,tests)
        validate_result_lines(Path(record['cache']['results']['path']).read_text().splitlines(),rows)
        and_rows,logic_rows=v3.native_sets()
        validate_result_lines(Path(record['condition']['results']['path']).read_text().splitlines(),logic_rows)
        v3.and_product.verify_probe_results(record['andResults']['path'],and_rows)
        v3.and_product.verify94(out/'packaged94/outputs/all-comparisons.tsv',v3.GOLDEN94)
        require(Path(record['cacheControls']['path']).read_text().splitlines()==control_rows(),'private cache controls differ')
    else:
        require([c['label'] for c in record['commands']]==['compile-fixture-consumers','packaged-cache'],'RED command coverage differs')
        require(record['candidateJar']==info(BASELINE) and sha(BASELINE)==BASELINE_PIN,'baseline JAR identity differs')
        verify_consumers(out,None)
    for name in ['cache']+(['condition'] if record['status'].startswith('PASS') else []):
        expected_rows=rows if name=='cache' else logic_rows
        require(Path(record[name]['bridge']['path']).read_text()==v3.logic_bridge(expected_rows),'bridge not derived from pinned observations')
        native_plan=read((NATIVE if name=='cache' else BASE/'condition-logic-v2')/'evidence/manifest.json')
        v3.old.verify_fixtures(out/(name+'-fixtures'),native_plan['fixtures'])
    compile=next(c for c in record['commands'] if c['label'].startswith('compile-'))
    originals=[PROBE]+([BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java'] if record['status'].startswith('PASS') else [])
    sources=[out/'fixture-sources'/p.relative_to(BASE/'tests') for p in originals]
    require([x for x in compile['argv'] if x.endswith('.java')]==list(map(str,sources)),'explicit consumer input set differs')
    for source,original in zip(sources,originals):require(source.read_bytes()==original.read_bytes(),'staged consumer source changed')
    for command in record['commands']:
        if command['label'].startswith('packaged-'):
            args=command['argv'];stdout=Path(command['stdout']['path']).read_text()
            require(v3.option(args,'--patch-module')==MODULE+'='+str(out/'fixture-tests.jar'),'runtime patch differs')
            require('jar='+record['candidateJar']['path']+' module='+MODULE+' exports=0 opens=0' in stdout,'actual packaged class/module identity missing')
            if record['status'].startswith('PASS'):require(command['exitCode']==0 and Path(command['stderr']['path']).read_bytes()==b'','packaged consumer failure')
    require(not list(out.rglob('must-not-exist.txt')),'task marker created')
    return {'status':record['status'],'candidateJar':record['candidateJar'],'acceptedTasksAdded':0}

def control_rows():
    return ['CC-OWNER-AND-VALUE-FRESHNESS\tPRIVATE_CONTROL\tTRUE_FALSE_TRUE_FALSE','CC-IMMUTABLE-SNAPSHOTS\tPRIVATE_CONTROL\tUNCHANGED','CC-WARM-SCALAR-INJECTION\tPRIVATE_CONTROL\tREJECTED','CC-WARM-SKIPPED-MALFORMED\tPRIVATE_CONTROL\tREJECTED']

def receipt_fields():
    return dict(schemaVersion=1,nativeCacheRows=8,nativeWarningEvents=5,current94Rows=94,andNativeSuccesses=9,andMalformedBoundary=1,andPrivateControls=24,conditionEvaluations=26,conditionNativeParseBoundaries=5,conditionDeclaredBoundaries=4,conditionWarningEvents=4,privateCacheControls=4,acceptedTasksAdded=0,numberedBatchCredit=0)

def python_controls(out,record,save):
    record['pythonControls']=[]
    for name,args,count in [('native29',['-m','unittest','discover','-s',str(HERE.parent/'condition-cache-v1'),'-p','test_*.py'],29),('qualification10',[str(HERE/'test_verify.py')],10)]:
        argv=[str(v3.PYTHON),'-B',*args];entry=dict(label=name,argv=argv,cwd=str(out),timeoutSeconds=120)
        record['pythonControls'].append(entry);save();process=subprocess.Popen(argv,cwd=out,env=v3.environment(out),stdout=subprocess.PIPE,stderr=subprocess.PIPE);entry['processId']=process.pid
        try: stdout,stderr=process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill();stdout,stderr=process.communicate(timeout=5);entry['timedOut']=True;raise
        finally:
            entry['exitCode']=process.returncode
            for stream,data in [('stdout',locals().get('stdout',b'')),('stderr',locals().get('stderr',b''))]:
                file=out/'logs'/(name+'.'+stream);file.write_bytes(data);entry[stream]=info(file)
            save()
        require(entry['exitCode']==0 and ('Ran '+str(count)+' tests') in stderr.decode() and '\nOK' in stderr.decode(),'pure Python controls failed')

def main():
    p=argparse.ArgumentParser();p.add_argument('--freeze-checkpoint',type=Path);p.add_argument('--checkpoint',type=Path);p.add_argument('--checkpoint-sha256');p.add_argument('--out',type=Path);p.add_argument('--red',action='store_true');p.add_argument('--check-receipt',type=Path);p.add_argument('--candidate-lock',type=Path);p.add_argument('--candidate-lock-sha256');a=p.parse_args()
    if a.freeze_checkpoint:
        require(not a.freeze_checkpoint.exists() and a.freeze_checkpoint.resolve().is_relative_to(B),'fresh owned checkpoint required');a.freeze_checkpoint.parent.mkdir(parents=True,exist_ok=True);dump(a.freeze_checkpoint,dict(kind='CACHE_PRODUCT_V1',inputs=inputs()));print(json.dumps(info(a.freeze_checkpoint)));return
    if a.check_receipt: print(json.dumps(verify_receipt(a.check_receipt,a.candidate_lock,a.candidate_lock_sha256)));return
    cp=checkpoint(a.checkpoint,a.checkpoint_sha256);rows=observations();out=a.out.resolve()
    require(out.is_relative_to(B) and out!=B and not out.exists(),'fresh owned output required')
    for folder in ['tmp','home','cache','logs','unrelated-cwd/logs','empty-sourcepath','consumer-classes']:(out/folder).mkdir(parents=True)
    record=dict(receipt_fields(),status='RUNNING',checkpoint=info(a.checkpoint),commands=[],resources=[])
    def save():dump(out/'verification.json',record)
    save()
    try:
        shutil.copytree(NATIVE/'fixtures',out/'cache-fixtures')
        if a.red:candidate,tests=BASELINE,None
        else:
            helper=load('cache_product_owned_tree_helper',B/'orchestration/two-frameworks/task-19-capture-phase-v4.py')
            require(sha(B/'orchestration/two-frameworks/task-19-capture-phase-v4.py')==v3.HELPER_PIN,'owned helper changed')
            entry=dict(label='unchanged-current94-runner',argv=[str(v3.PYTHON),'-B',str(BASE/'verify.py'),'--out',str(out/'packaged94')],cwd=str(R),outerTimeoutSeconds=600);record['commands'].append(entry);save()
            adapter=load('cache_product_owned_cleanup_adapter',HERE.parent/'condition-cache-v1/outer_cleanup_adapter.py')
            env=v3.environment(out);stdout=stderr=b''
            fingerprint=read(NATIVE/'evidence/native-input-lock.json')
            taskkill=Path(os.environ['SystemRoot'])/'System32/taskkill.exe'
            require(any(Path(x['path'])==taskkill and x['sha256']==sha(taskkill) for x in fingerprint['executionPins']),'cleanup executable is not independently pinned')
            try:
                stdout,stderr=adapter.run_capture_process(helper,entry['argv'],R,env,entry,cleanup_cwd=out,taskkill=taskkill,environment_overrides={k:env[k] for k in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','XDG_CACHE_HOME']},timeout=600)
            except subprocess.TimeoutExpired as error:
                stdout=error.stdout or b'';stderr=error.stderr or b'';raise
            finally:
                for stream,data in [('stdout',stdout),('stderr',stderr)]:
                    path=out/'logs'/('runner.'+stream);path.write_bytes(data);entry[stream]=info(path)
                save()
            require(type(entry.get('exitCode')) is int and entry['exitCode']==0,'canonical94 runner failed')
            candidate,tests=v3.packaged_artifacts(out/'packaged94')
        record['candidateJar']=info(candidate);save()
        patch=compile_consumers(out,candidate,tests,record,save)
        consume('cache',rows,out/'cache-fixtures',out,candidate,patch,record,save,a.red)
        if not a.red:
            and_rows,logic_rows=v3.native_sets()
            for target,source in [('and-fixtures','and-conditions-v1'),('exists-fixtures','exists-site-directories-v1'),('condition-fixtures','condition-logic-v2')]:shutil.copytree(BASE/source/'fixtures',out/target)
            for case in (out/'exists-fixtures').iterdir():shutil.copytree(case,out/'and-fixtures'/case.name)
            shutil.copyfile(BASE/'exists-site-directories-v1/cwd/cwd-only.marker',out/'unrelated-cwd/cwd-only.marker')
            consume('condition',logic_rows,out/'condition-fixtures',out,candidate,patch,record,save)
            bridge=out/'and-bridge.tsv';bridge.write_bytes(v3.and_product.bridge(and_rows).encode())
            argv=[str(v3.JDK/'bin/java.exe'),*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(patch),'-m',MODULE+'/'+PACKAGE+'.AndConditionTest','green',str(bridge),str(out/'and-fixtures'),str(out/'and-results.tsv'),str(out/'controls'),str(candidate)]
            run('packaged-and',argv,out/'unrelated-cwd',v3.environment(out),record,save)
            v3.and_product.verify_probe_results(out/'and-results.tsv',and_rows);record['andResults']=info(out/'and-results.tsv')
            controls=out/'cache-controls.tsv'
            argv=[str(v3.JDK/'bin/java.exe'),*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(patch),'-m',MODULE+'/'+PACKAGE+'.ConditionCachePackagedTest',str(out/'cache-bridge.tsv'),str(out/'cache-controls'),str(controls),str(candidate),'controls']
            run('packaged-cache-controls',argv,out/'unrelated-cwd',v3.environment(out),record,save)
            require(controls.read_text().splitlines()==control_rows(),'private cache controls failed');record['cacheControls']=info(controls)
            python_controls(out,record,save)
        checkpoint(a.checkpoint,a.checkpoint_sha256)
        record['status']='GENUINE_PACKAGED_BASELINE_RED' if a.red else 'PASS_PACKAGED_CACHE_PRODUCT_V1';save()
        artifacts=[info(x) for x in sorted(out.rglob('*')) if x.is_file() and x.name!='candidate-lock.json']
        dump(out/'candidate-lock.json',dict(receipt=info(out/'verification.json'),inputs=cp['inputs']+artifacts))
        verify_receipt(out/'verification.json',out/'candidate-lock.json',sha(out/'candidate-lock.json'))
        print(json.dumps({'status':record['status'],'receipt':info(out/'verification.json'),'candidateLock':info(out/'candidate-lock.json')}))
    except Exception as error:
        record.update(status='FAILED',error=str(error));save();raise

if __name__=='__main__': main()
