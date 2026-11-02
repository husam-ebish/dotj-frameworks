"""One product build; guarded JAR-only qualification and retained input/output proof."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contract as c
import argparse,copy,json,shutil,time,zipfile
HERE=c.HERE;BASE=c.BASE;B=c.B;W=c.W;MODULE=c.MODULE;PACKAGE=c.PACKAGE

def environment(out):
    return {'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe','PATH':str(c.JDK/'bin')+r';C:\Windows\System32;C:\Windows\System32\WindowsPowerShell\v1.0','TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONUTF8':'1'}
def vm(out):return ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8','-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]
def success(r):
    c.require(r.get('launched') is True and r.get('jobAssigned') is True and r.get('resumed') is True,'ownership')
    c.require(r.get('timedOut') is False and r.get('outputLimitExceeded') is False and 'cleanupError' not in r and 'error' not in r,'bounded process/cleanup')
    c.require(type(r['exitCode']) is int and r['exitCode']==0,'command exit '+str(r['exitCode']))
def jar(root,out):
    with zipfile.ZipFile(out,'x',zipfile.ZIP_STORED) as z:
        for p in sorted(root.rglob('*.class')):
            e=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2000,1,1,0,0,0));e.create_system=0;z.writestr(e,p.read_bytes())
def validate_jar(path,classes):
    expected={x.relative_to(classes).as_posix():x.read_bytes() for x in classes.rglob('*.class')}
    with zipfile.ZipFile(path) as z:c.require(set(z.namelist())==set(expected) and all(z.read(k)==v for k,v in expected.items()),'JAR class closure')
def static_inputs():
    paths=set()
    for folder in [BASE/'src',BASE/'tests',HERE,c.H,HERE.parent/'condition-boolean-capture-v2',HERE.parent/'condition-boolean-observer-v3']:
        paths.update(p for p in folder.rglob('*') if p.is_file() and p.name not in ['input-lock.json'] and '__pycache__' not in p.parts)
    paths.update(Path(x['path']) for x in c.read(c.H/'predecessor-preservation-lock.json')['files'])
    paths.update(Path(x['path']) for x in c.read(c.H/'python-runtime-manifest.json')['files'])
    paths.update(Path(x['path']) for x in c.read(HERE/'CONTRACT.json')['runtimeNumericSource'])
    paths.update(p for p in c.ARCHIVE.parent.rglob('*') if p.is_file())
    paths.update([c.JDK/'bin/java.exe',c.JDK/'bin/javac.exe',c.JDK/'lib/modules',c.JDK/'release',c.GUARD,c.LOCK,c.LOCK.parent/'observations.json',c.LOCK.parent/'numeric-resolution.json',c.LOCK.parent/'runtime-faults.json'])
    return [c.descriptor(p) for p in sorted(paths)]
def foreign():
    # Use original immutable validators at their original newline-bound roots.
    historical=B/'worktrees/dotj-build-condition-cache-v1/tools/oracle/dotj-build/condition-cache-product-v1/verify.py'
    cache=c.load('boolean_original_cache_validator',historical)
    cache_rows=cache.observations();and_rows,logic_rows=cache.v3.native_sets()
    hts=B/'worktrees/dotj-build-has-trailing-slash-v1/tools/oracle/dotj-build/has-trailing-slash-v1'
    sys.path.insert(0,str(hts));p=c.load('boolean_original_predicate_validation',hts/'verify.py')
    receipt=B/'validation/Batch-2513-has-trailing-slash-native-pass1-v1/receipt.json'
    native=p.receipt(receipt,'ac62a91d7814228e9c6dda129fff6d5fb7f00d6a3ad39add332bddcb81ab00f2')
    return cache,cache_rows,and_rows,logic_rows,p,native

def prepare(out,record):
    for name in ['classes','consumer-classes','consumer-source','empty-sourcepath','outputs','unrelated-cwd']:(out/name).mkdir()
    # Original fixtures remain immutable; only BE19's known absolute task marker is relocated.
    for dst,src in [('fixtures','fixtures'),('import-fixtures','import-fixtures'),('import-path-fixtures','import-path-fixtures'),('whitespace-fixtures','import-path-whitespace-v1/fixtures'),('cache-fixtures','condition-cache-v1/fixtures'),('condition-fixtures','condition-logic-v2/fixtures'),('and-fixtures','and-conditions-v1/fixtures'),('predicate-fixtures','has-trailing-slash-v1/fixtures')]:shutil.copytree(BASE/src,out/dst)
    for src in (BASE/'location-fixtures').iterdir():shutil.copytree(src,out/'import-fixtures'/src.name)
    for src in (BASE/'exists-site-directories-v1/fixtures').iterdir():shutil.copytree(src,out/'and-fixtures'/src.name)
    shutil.copyfile(BASE/'exists-site-directories-v1/cwd/cwd-only.marker',out/'unrelated-cwd/cwd-only.marker')
    for dst,src in [('native-import','native-import-comparison-v1.tsv'),('location','location-comparison-v1.tsv'),('cycle','cycle-comparison-v1.tsv'),('profile','profile-comparison-v1.tsv'),('import-path','import-path-comparison-v1.tsv')]:shutil.copyfile(BASE/'evidence'/src,out/(dst+'-bridge.tsv'))
    shutil.copyfile(BASE/'import-path-whitespace-v1/evidence/comparison.tsv',out/'whitespace-bridge.tsv')
    original=B/'agents/validation-performance/build-evaluation-reference/fixtures'
    sentinel=out/'fixtures/BE19-no-target-execution/main.proj';raw=sentinel.read_bytes();old=str(original).encode();c.require(raw.count(old)==1,'BE19 replacement cardinality');sentinel.write_bytes(raw.replace(old,str(out/'fixtures').encode()))
    record['BE19PathOnlyNormalization']={'original':c.descriptor(BASE/'fixtures/BE19-no-target-execution/main.proj'),'relocated':c.descriptor(sentinel),'occurrences':1}
    shutil.copytree(c.H/'fixtures',out/'boolean-fixtures');shutil.copytree(c.H/'private-fixtures',out/'boolean-private-fixtures')
    value=c.read(HERE/'CONTRACT.json');rows=c.frozen();c.validate_contract(value,rows)
    (out/'boolean-bridge.tsv').write_text(c.bridge(value['nativeRecords']),encoding='utf-8',newline='\n');(out/'boolean-private-bridge.tsv').write_text(c.bridge(value['privateRecords']),encoding='utf-8',newline='\n')
    cache,cache_rows,and_rows,logic_rows,p,native=foreign()
    record['historicalValidators']=[c.descriptor(x) for x in [Path(cache.__file__),cache.v3.REVISION/'verify.py',Path(p.__file__)]]
    record['historicalVsCheckoutNativeLock']={'original':c.descriptor(cache.BASE/'condition-cache-v1/evidence/native-input-lock.json'),'checkout':c.descriptor(BASE/'condition-cache-v1/evidence/native-input-lock.json'),'ruling':'Validate original retained CRLF proof at original root. Checkout is a preserved LF copy, not rewritten or repinned.'}
    # Two CL05 scalar cases transition from private refusal to actual native false.
    lines=cache.v3.logic_results(logic_rows)
    for i,r in enumerate(logic_rows):
        if r['id'] in ['CL05-scalar-2','CL05-scalar-4']:lines[i]='\t'.join([r['id'],'MATCHED_EVALUATION',*c.successful_fields(r,'<FIXTURE_ROOT>')])
    def logic_bridge(rows,lines):
        result=[]
        for r,line in zip(rows,lines):
            result.append('CASE\t'+line)
            result.extend('GLOBAL\t'+c.enc(k)+'\t'+c.enc(v) for k,v in r['globals'].items());result.append('END')
        return '\n'.join(result)+'\n'
    (out/'condition-bridge.tsv').write_text(logic_bridge(logic_rows,lines),encoding='utf-8',newline='\n')
    (out/'cache-bridge.tsv').write_text(cache.v3.logic_bridge(cache_rows),encoding='utf-8',newline='\n')
    (out/'and-bridge.tsv').write_text(cache.v3.and_product.bridge(and_rows),encoding='utf-8',newline='\n')
    pred=[]
    classes=c.read(BASE/'has-trailing-slash-v1/case-classifications.json')['cases']
    for r,d in zip(native['payload']['rows'],classes):
        if d['category']=='semantic':fields=[r['id'],'MATCHED_EVALUATION',*c.successful_fields(r,str(Path(native['fixtureRoot'])))]
        else:fields=[r['id'],d['privateDisposition'],','.join(d['privateErrorCodes'])]
        pred.append('CASE\t'+'\t'.join(fields));pred.extend('GLOBAL\t'+c.enc(k)+'\t'+c.enc(v) for k,v in r['globals'].items());pred.append('END')
    (out/'predicate-bridge.tsv').write_text('\n'.join(pred)+'\n',encoding='utf-8',newline='\n')
    record['expectedConditionRows']=lines;record['expectedCacheRows']=cache.v3.logic_results(cache_rows)
    record['fixtureInputs']=[c.descriptor(p) for folder in ['fixtures','import-fixtures','import-path-fixtures','whitespace-fixtures','cache-fixtures','condition-fixtures','and-fixtures','predicate-fixtures','boolean-fixtures','boolean-private-fixtures'] for p in sorted((out/folder).rglob('*')) if p.is_file()]
    record['bridges']=[c.descriptor(p) for p in sorted(out.glob('*bridge.tsv'))]
    staged=[]
    for src in [*sorted((BASE/'tests').rglob('*.java')),*sorted((HERE/'java').rglob('*.java'))]:
        relative=src.relative_to(BASE/'tests') if src.is_relative_to(BASE/'tests') else src.relative_to(HERE/'java')
        dst=out/'consumer-source'/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);staged.append(dst)
    record['stagedSources']=[c.descriptor(p) for p in staged]
    return staged

def qualify(out,record,run):
    sources=prepare(out,record);record['sourceInputs']=[c.descriptor(p) for p in sorted((BASE/'src').rglob('*.java'))]
    def check():
        for pin in [*record['inputPins'],*record['fixtureInputs'],*record['bridges'],*record['stagedSources']]:c.pin(pin)
    compiler=[str(c.JDK/'bin/javac.exe'),*['-J'+x for x in vm(out)],'--release','21','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'-d',str(out/'classes'),*[x['path'] for x in record['sourceInputs']]]
    check();run('compile-product',compiler,out/'unrelated-cwd')
    candidate=out/'dotj-build-evaluation-candidate.jar';jar(out/'classes',candidate);validate_jar(candidate,out/'classes');record['candidateJar']=c.descriptor(candidate)
    compiler=[str(c.JDK/'bin/javac.exe'),*['-J'+x for x in vm(out)],'--release','21','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),'--module-path',str(candidate),'--patch-module',MODULE+'='+str(out/'consumer-source'),'-d',str(out/'consumer-classes'),*map(str,sources)]
    run('compile-consumers',compiler,out/'unrelated-cwd')
    oldtests=B/'validation/Batch-2513-has-trailing-slash-product-green-v3/packaged94/evaluation-contract-tests.jar'
    with zipfile.ZipFile(oldtests) as z:expected=set(z.namelist())
    prefix=PACKAGE.replace('.','/')+'/'
    expected|={prefix+x+'.class' for x in ['EvaluationBooleanProductTest','AndBooleanProductTest','AndBooleanProductTest$Edge','TrailingSlashBooleanProductTest','CacheBooleanProductTest','BooleanSuiteLauncher','ConditionBooleanProductTest']}
    actual={p.relative_to(out/'consumer-classes').as_posix() for p in (out/'consumer-classes').rglob('*') if p.is_file()}
    c.require(actual==expected,'explicit consumer class inventory '+str(actual^expected))
    c.require(not any(Path(x).name=='module-info.class' or Path(x).name.startswith('ProjectEvaluationComponent$') or Path(x).name=='ProjectEvaluationComponent.class' for x in actual),'product class emitted by consumer compiler')
    c.require(not list((out/'empty-sourcepath').iterdir()),'sourcepath not empty');record['consumerOutputClasses']=sorted(actual)
    tests=out/'fixture-tests.jar';jar(out/'consumer-classes',tests);validate_jar(tests,out/'consumer-classes');record['consumerJar']=c.descriptor(tests)
    def java(label,cls,args):
        check();c.pin(record['candidateJar']);c.pin(record['consumerJar'])
        cmd=[str(c.JDK/'bin/java.exe'),*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(tests),'-m',MODULE+'/'+PACKAGE+'.BooleanSuiteLauncher',str(candidate),cls,*map(str,args)]
        run(label,cmd,out/'unrelated-cwd');c.pin(record['candidateJar']);c.pin(record['consumerJar']);check()
    # New coherent vertical first, then every predecessor obligation on this exact JAR.
    java('packaged-boolean','ConditionBooleanProductTest',[out/'boolean-bridge.tsv',out/'boolean-fixtures',out/'boolean-private-bridge.tsv',out/'boolean-private-fixtures',out/'boolean-controls',out/'boolean-results.tsv',candidate])
    original=B/'agents/validation-performance/build-evaluation-reference/fixtures'
    java('packaged-current-base','EvaluationBooleanProductTest',[out/'fixtures/native-comparison.tsv',out/'fixtures',out/'outputs',original/'BE19-no-target-execution/must-not-exist.txt',candidate,out/'native-import-bridge.tsv',out/'import-fixtures',out/'import-path-fixtures'])
    for label,cls,args in [
      ('locations','ImportLocationTest',[out/'location-bridge.tsv',out/'import-fixtures',out/'outputs/location-results.tsv']),
      ('cycles','DefaultCycleTest',[out/'cycle-bridge.tsv',out/'import-fixtures',out/'outputs/cycle-results.tsv']),
      ('profiles','ImportProfileTest',[out/'profile-bridge.tsv',out/'import-fixtures',out/'outputs/profile-results.tsv']),
      ('paths','ImportPathExpansionTest',[out/'import-path-bridge.tsv',out/'import-path-fixtures',out/'outputs/import-path-results.tsv',out/'outputs/path-controls']),
      ('whitespace','ImportPathWhitespaceTest',[out/'whitespace-bridge.tsv',out/'whitespace-fixtures',out/'outputs/whitespace-results.tsv',out/'outputs/whitespace-controls'])]:java('packaged-current-'+label,cls,args)
    base=(out/'outputs/case-results.tsv').read_text().splitlines();paths=(out/'outputs/import-path-results.tsv').read_text().splitlines()
    all94=base+(out/'outputs/location-results.tsv').read_text().splitlines()+(out/'outputs/cycle-results.tsv').read_text().splitlines()+(out/'outputs/profile-results.tsv').read_text().splitlines()+[x for x in paths if not x.startswith('NEG-dynamic-import\t')]+(out/'outputs/whitespace-results.tsv').read_text().splitlines()
    golden=Path(c.read(c.H/'predecessor-preservation-lock.json')['current94']['path']).read_text().splitlines();expected=[]
    for row in golden:
        ident=row.split('\t')[0];expected.append(ident+'\tNATIVE_TYPED_EQUALITY_MATCH\tvalue' if ident in ['NEG-numeric-comparison','NEG-bool-coercion'] else row)
    c.require(all94==expected and len(all94)==94,'94 stable IDs/fields with exact two transitions');(out/'outputs/all-comparisons.tsv').write_text('\n'.join(all94)+'\n',encoding='utf-8',newline='\n')
    for name in ['condition','cache']:
        java('packaged-'+name,'CacheBooleanProductTest',[out/(name+'-bridge.tsv'),out/(name+'-fixtures'),out/(name+'-results.tsv'),candidate,name])
        c.require((out/(name+'-results.tsv')).read_text().splitlines()==record['expected'+name.capitalize()+'Rows'],'ordered '+name+' fields')
    java('packaged-and','AndBooleanProductTest',['green',out/'and-bridge.tsv',out/'and-fixtures',out/'and-results.tsv',out/'and-controls',candidate])
    c.require(len((out/'and-results.tsv').read_text().splitlines())==34,'9+1+24 And coverage')
    java('packaged-cache-controls','CacheBooleanProductTest',[out/'cache-bridge.tsv',out/'cache-controls',out/'cache-controls.tsv',candidate,'controls'])
    c.require(len((out/'cache-controls.tsv').read_text().splitlines())==4,'cache4 groups')
    java('packaged-predicate','TrailingSlashBooleanProductTest',[out/'predicate-bridge.tsv',out/'predicate-fixtures',out/'predicate-results.tsv',candidate,'corpus'])
    c.require((out/'predicate-results.tsv').read_text().splitlines()==[x[5:] for x in (out/'predicate-bridge.tsv').read_text().splitlines() if x.startswith('CASE\t')],'38 predicate fields')
    java('packaged-predicate-controls','TrailingSlashBooleanProductTest',[out/'predicate-bridge.tsv',out/'predicate-controls',out/'predicate-controls.tsv',candidate,'controls'])
    c.require(len((out/'predicate-controls.tsv').read_text().splitlines())==4,'HT4 groups')
    c.require(not list(out.rglob('must-not-exist.txt')),'task marker appeared');check();c.frozen()
    # Exact18 native-backed successor IDs were consumed in Boolean corpus and original successor suites.
    value=c.read(HERE/'CONTRACT.json');got={x.split('\t')[0]:x for x in (out/'boolean-results.tsv').read_text().splitlines()}
    record['transitions']=[{'id':t['id'],'nativeCase':t['nativeCase'],'nativeResult':got[t['nativeCase']],'status':'QUALIFIED_SUCCESSOR'} for t in value['transitions']];c.require(len(record['transitions'])==18,'18 transitions')
    record['counts']={'newNativeIds':297,'nativeSuccessObservableMatches':239,'nativeProjectErrorMappings':46,'inheritedProfileRestrictions':9,'sourceBasedFaultAdaptations':3,'privateInputs':16,'privateGroups':14,'current94':94,'current94Unchanged':92,'current94Transitions':2,'and':[9,1,24],'condition':[28,5,2],'conditionWarnings':4,'cache':8,'cacheWarningVector':[1,0,0,1,1,1,0,1],'cachePrivateGroups':4,'hasTrailingSlash':[32,6],'hasTrailingSlashWarnings':4,'hasTrailingSlashPrivateGroups':4,'hasTrailingSlashSyntax':[18,4],'preservedFiles':391,'predecessorCaseControlInventory':223,'transitionIds':18,'acceptedTasksAdded':0}
    record['resultFiles']=[c.descriptor(p) for p in sorted(out.rglob('*.tsv'))]
    validate_jar(candidate,out/'classes');validate_jar(tests,out/'consumer-classes')
    record['status']='PASS_PRIVATE_BOOLEAN_PRODUCT_CANDIDATE'

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--inner',action='store_true');a=p.parse_args();out=a.out.resolve()
    c.require(out.is_relative_to(B) and out!=B,'D scratch required')
    c.require(c.sha(c.GUARD)==c.GUARD_SHA,'guard pin');guard=c.load('boolean_owned_guard',c.GUARD);env=environment(out)
    if not a.inner:
        c.require(not out.exists(),'fresh output required');c.frozen();c.validate_contract(c.read(HERE/'CONTRACT.json'),c.frozen());out.mkdir()
        for d in ['tmp','home','home/AppData/Local','home/AppData/Roaming']:(out/d).mkdir(parents=True,exist_ok=True)
        pins=static_inputs();c.write(out/'input-lock.json',{'pins':pins});c.write(out/'coordinator-identity.json',{'source':c.descriptor(__file__),'guard':c.descriptor(c.GUARD),'environment':env})
        resource=[];_,resource=guard.wait_resources(time.monotonic()+160)
        def prelaunch():
            t=time.monotonic();m=guard.memory();dt=time.monotonic()-t;c.require(dt<=2 and guard.resource_ready(m),'fresh resources');resource.append({'prelaunch':m,'durationSeconds':dt})
        r=guard.run([str(c.PYTHON),'-B',str(HERE/'verify.py'),'--out',str(out),'--inner'],out,env,'controller',600,prelaunch=prelaunch,on_update=lambda r:c.write(out/'controller-process.json',r))
        c.write(out/'controller-receipt.json',{'process':r,'resources':resource,'environment':env,'source':c.descriptor(__file__),'guard':c.descriptor(c.GUARD)});success(r)
        record=c.read(out/'receipt.json');c.require(record['status']=='PASS_PRIVATE_BOOLEAN_PRODUCT_CANDIDATE','qualification incomplete');print(json.dumps({'status':record['status'],'receipt':c.descriptor(out/'receipt.json'),'jar':record['candidateJar']}));return
    record={'status':'RUNNING','commands':[],'environment':env,'inputPins':c.read(out/'input-lock.json')['pins'],'sourceCoordinator':c.descriptor(__file__),'ownedGuard':c.descriptor(c.GUARD),'nativeLaunches':0,'baselineRed':c.descriptor(B/'validation/Batch-2516-baseline-red-v1/behavior-red.json'),'nativeLock':c.descriptor(c.LOCK)}
    deadline=time.monotonic()+540
    def save():c.write(out/'receipt.json',record)
    def run(label,argv,cwd):
        c.require(time.monotonic()<deadline,'aggregate deadline');c.require(Path(argv[0]) in [c.JDK/'bin/java.exe',c.JDK/'bin/javac.exe'],'JDK executable')
        for pin in record['inputPins']:c.pin(pin)
        _,samples=guard.wait_resources(time.monotonic()+160);entry={'label':label,'resources':samples}
        def prelaunch():
            t=time.monotonic();m=guard.memory();dt=time.monotonic()-t;c.require(dt<=2 and guard.resource_ready(m),'fresh resources');entry['resources'].append({'prelaunch':m,'durationSeconds':dt})
        entry['process']=guard.run(argv,cwd,env,label,120,prelaunch=prelaunch,on_update=lambda r:c.write(out/(label+'-process.json'),r));entry['stdout']=c.descriptor(entry['process']['stdoutPath']);entry['stderr']=c.descriptor(entry['process']['stderrPath']);record['commands'].append(entry);save();success(entry['process']);c.require(Path(entry['stderr']['path']).read_bytes()==b'','unexpected stderr '+label)
    save()
    try:qualify(out,record,run);save()
    except BaseException as e:record.update(status='FAILED_STOP_NO_RETRY',failure={'type':type(e).__name__,'message':str(e)});save();raise
if __name__=='__main__':main()
