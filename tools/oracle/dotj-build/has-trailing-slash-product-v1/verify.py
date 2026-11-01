"""Predicate successor: unchanged historical assertions, one JAR, W12 execution.

The pinned original coordinator snapshot adapted canonical94.run_command.
This continuation binds that one build and its eight successful commands, then
runs the remaining consumers. No historical pin/source or native input changes.
"""
import argparse, datetime, importlib.util, json, sys, time, shutil, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
W=HERE.parents[3]
B=Path('D:/AI/Implementation/dotj Frameworks')
BASE=W/'dotj-build/evaluation-candidate'
H=HERE.parent/'has-trailing-slash-v1'
sys.path.insert(0,str(H)) # Embeddable Python excludes the script directory.
import capture as c
import packaged

MODULE=packaged.MODULE
PACKAGE=packaged.PACKAGE
JDK=packaged.JDK
RUNNER_SHA='b9fd187bae555ea4ccbfe96dfb36823540209f064c066b683531748e76c981da'
NATIVE=B/'validation/Batch-2513-has-trailing-slash-native-pass1-v1/receipt.json'
NATIVE_SHA='ac62a91d7814228e9c6dda129fff6d5fb7f00d6a3ad39add332bddcb81ab00f2'
NATIVE_LOCK=B/'agents/batch2513-has-trailing-slash-native-preparation-v1/native-input-lock-v2.json'
NATIVE_LOCK_SHA='1e6259da405ab05310afbc3384df227f1498880ea208f85d6f0062e9baaaf5ec'
RED=B/'validation/Batch-2513-has-trailing-slash-behavioral-red-v1/receipt.json'
RED_SHA='bdf4ce618cd2b24a1c10750aff1c67fd98626c4d9f5f82fa573c697f6c2aa1cb'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

cache=load('predicate_frozen_cache_primitives',HERE.parent/'condition-cache-product-v1/verify.py')
v3=cache.v3

def environment(out):
    return {'SystemRoot':r'C:\Windows','WINDIR':r'C:\Windows','ComSpec':r'C:\Windows\System32\cmd.exe',
      'PATH':str(JDK/'bin')+r';C:\Windows\System32;C:\Windows\System32\WindowsPowerShell\v1.0','TEMP':str(out/'tmp'),'TMP':str(out/'tmp'),
      'HOME':str(out/'home'),'USERPROFILE':str(out/'home'),'HOMEDRIVE':'D:','HOMEPATH':str(out/'home')[2:],
      'APPDATA':str(out/'home/AppData/Roaming'),'LOCALAPPDATA':str(out/'home/AppData/Local'),
      'XDG_CACHE_HOME':str(out/'cache'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1',
      'PYTHONUTF8':'1','LANG':'en_US.UTF-8','LC_ALL':'en_US.UTF-8'}

def frozen_inputs():
    c.require(c.sha(NATIVE_LOCK)==NATIVE_LOCK_SHA,'native input lock changed')
    pins=c.read(NATIVE_LOCK)['pins']
    for pin in pins:
        c.require(c.sha(pin['path'])==pin['sha256'] and Path(pin['path']).stat().st_size==pin['sizeBytes'],'frozen native input changed: '+pin['path'])
    c.require(c.sha(BASE/'verify.py')==RUNNER_SHA,'canonical94 changed')
    c.require(c.sha(RED)==RED_SHA,'actual behavioral RED changed')
    return [c.descriptor(pin['path']) for pin in pins]

def validate_classes(actual,expected):
    c.require(set(actual)==set(expected),'unexpected/missing consumer output class membership')
    c.require(not any(Path(x).name=='ProjectEvaluationComponent.class' or Path(x).name.startswith('ProjectEvaluationComponent$') or x=='module-info.class' for x in actual),'hidden product class in consumer output')

def validate_lines(actual,expected):
    c.require(actual==expected,'ordered result fields or category membership differ')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--inner',action='store_true')
    p.add_argument('--built-receipt',type=Path,required=True);p.add_argument('--built-receipt-sha256',required=True);a=p.parse_args()
    out=c.confined(a.out)
    if not a.inner:
        c.require(not out.exists(),'new output directory required');out.mkdir(parents=True)
        for d in ['tmp','home','cache']:(out/d).mkdir()
        guard=c.owned();env=environment(out)
        argv=[str(c.PYTHON),'-B',str(HERE/'verify.py'),'--out',str(out),'--built-receipt',str(a.built_receipt),'--built-receipt-sha256',a.built_receipt_sha256,'--inner']
        record=guard.run(argv,out,env,'controller',600,on_update=lambda r:c.write(out/'controller-process.json',r))
        c.write(out/'controller-receipt.json',{'process':record,'environment':env,'coordinator':c.descriptor(HERE/'verify.py'),'ownedGuard':c.descriptor(c.GUARD)})
        c.successful(record)
        print(json.dumps({'status':c.read(out/'receipt.json')['status'],'receipt':c.descriptor(out/'receipt.json')}));return
    deadline=time.monotonic()+540
    guard=c.owned();env=environment(out)
    for d in ['logs','unrelated-cwd','empty-sourcepath','consumer-classes','consumer-source']:(out/d).mkdir()
    record={'schemaVersion':1,'status':'RUNNING','commands':[],'resourceSamples':[],
      'nativeLaunches':0,'acceptedTasksAdded':0,'numberedBatchCredit':0,'environment':env,
      'ownedGuard':c.descriptor(c.GUARD),'coordinator':c.descriptor(HERE/'verify.py'),
      'behavioralRed':c.descriptor(RED),'nativeReceipt':c.descriptor(NATIVE),
      'executionAdapter':{'originalRunnerSha256':RUNNER_SHA,'replacedBoundary':'canonical94.run_command',
       'changes':['W12 guard; wait_resources before run; fresh <=2s prelaunch resource query',
        'explicit environment whitelist and D storage','compile-tests adds empty -sourcepath and -implicit:none'],
       'historicalAssertionCodeChanged':False,'historicalSourcePinsChanged':False},
      'counts':{'current94':94,'andSemantic':9,'andNativeParseBoundary':1,'andPrivateControls':24,
       'conditionSemantic':26,'conditionNativeParseBoundaries':5,'conditionDeclaredBoundaries':4,'conditionWarnings':4,
       'cacheSemantic':8,'cacheWarningVector':[1,0,0,1,1,1,0,1],'cachePrivateControls':4,
       'predicateRows':38,'predicateSemantic':32,'predicateBoundaries':6,'predicateWarnings':4,'predicatePrivateGroups':4}}
    def save():c.write(out/'receipt.json',record)
    def run(label,argv,cwd,foreign_env=None,foreign_record=None,foreign_save=None):
        c.require(time.monotonic()<deadline,'aggregate deadline exceeded')
        c.require(Path(argv[0]) in [JDK/'bin/java.exe',JDK/'bin/javac.exe'],'unapproved executable')
        _,samples=guard.wait_resources(deadline);record['resourceSamples'].extend(samples)
        entry=guard.run(argv,cwd,env,label,120,
          prelaunch=lambda:c.resource_check(guard,deadline,record['resourceSamples']),
          stream_limits={'stdout':2097152,'stderr':524288},
          on_update=lambda r:c.write(out/(label+'-process.json'),r))
        entry['label']=label;entry['stdout']=c.descriptor(entry['stdoutPath']);entry['stderr']=c.descriptor(entry['stderrPath'])
        record['commands'].append(entry);save()
        if foreign_record is not None:foreign_record['commands'].append(entry);foreign_save()
        c.successful(entry)
        c.require(Path(entry['stderrPath']).read_bytes()==b'','unexpected compiler/runtime stderr')
        return entry
    save()
    try:
        record['frozenInputsBefore']=frozen_inputs()
        record['toolchain']=[c.descriptor(x) for x in [c.PYTHON,c.PYTHON.parent/'python313.dll',JDK/'bin/java.exe',JDK/'bin/javac.exe',JDK/'lib/modules',JDK/'release']]
        record['sourceInputs']=[c.descriptor(p) for folder in ['src','tests'] for p in sorted((BASE/folder).rglob('*.java'))]
        native=packaged.pair.receipt(NATIVE,NATIVE_SHA)
        # Native locks bind the original W11 byte spellings (including CRLF).
        # Revalidate there; this successor never rewrites historical files/pins.
        historical_cache_path=B/'worktrees/dotj-build-condition-cache-v1/tools/oracle/dotj-build/condition-cache-product-v1/verify.py'
        c.require(c.sha(historical_cache_path)==c.sha(HERE.parent/'condition-cache-product-v1/verify.py'),'historical cache validator source differs')
        historical_cache=load('predicate_immutable_w11_native_validation',historical_cache_path)
        record['historicalCacheValidator']=c.descriptor(historical_cache_path)
        record['historicalCacheNativeLock']=c.descriptor(historical_cache.BASE/'condition-cache-v1/evidence/native-input-lock.json')
        record['checkoutCacheNativeLock']=c.descriptor(BASE/'condition-cache-v1/evidence/native-input-lock.json')
        record['historicalCacheLocationRuling']='Root approved original W11 CRLF native identity; checkout LF copy is preserved unchanged.'
        cache_rows=historical_cache.observations();and_rows,logic_rows=v3.native_sets()
        # Resume after a bookkeeping-only membership failure: never rebuild product.
        c.require(c.sha(a.built_receipt)==a.built_receipt_sha256,'one-build receipt changed')
        built=c.read(a.built_receipt);builtout=a.built_receipt.parent;builddir=builtout/'packaged94'
        c.require(built['status']=='FAILED_OR_DEFERRED' and built['failure']=={'type':'ValueError','message':'hidden product class in consumer output'},'unexpected resume reason')
        c.require(c.sha(builtout/'coordinator-source.py')==built['coordinator']['sha256'],'original build coordinator snapshot changed')
        c.require(built['sourceInputs']==record['sourceInputs'],'product/consumer source changed since one build')
        expected_labels=['compile-candidate','compile-tests','packaged-contract','packaged-locations','packaged-default-cycles','packaged-import-profiles','packaged-import-paths','packaged-import-path-whitespace']
        c.require([x['label'] for x in built['commands']]==expected_labels,'one-build command coverage differs')
        for command in built['commands']:
            c.successful(command)
            for stream in ['stdout','stderr']:
                c.require(c.descriptor(command[stream]['path'])==command[stream],'one-build raw log changed')
        candidate=builddir/'dotj-build-evaluation-candidate.jar';tests=builddir/'evaluation-contract-tests.jar'
        record['oneBuildReceipt']=c.descriptor(a.built_receipt)
        record['oneBuildCoordinatorSnapshot']=c.descriptor(builtout/'coordinator-source.py')
        record['oneBuildCommands']=built['commands'];record['oneBuildResourceSamples']=built['resourceSamples']
        record['candidateJar']=c.descriptor(candidate);record['canonical94Receipt']=c.descriptor(builddir/'verification.json')
        c.require(record['candidateJar']==built['candidateJar'],'one-build JAR changed')
        c.require(c.read(builddir/'verification.json')['status']=='PASS_INTERNAL_PACKAGED_CONTRACT','current94 did not pass')
        v3.and_product.verify94(builddir/'outputs/all-comparisons.tsv',v3.GOLDEN94)
        with zipfile.ZipFile(candidate) as z:
            expected={p.relative_to(builddir/'classes').as_posix():p.read_bytes() for p in (builddir/'classes').rglob('*.class')}
            c.require(set(z.namelist())==set(expected) and all(z.read(k)==v for k,v in expected.items()),'candidate JAR/class closure differs')
        with zipfile.ZipFile(tests) as z:
            # Baseline helper and new consumer classes only; product classes forbidden.
            oldtests=B/'validation/Batch-2511-cache-product-final-green-run3/packaged94/evaluation-contract-tests.jar'
            with zipfile.ZipFile(oldtests) as old:expected_test_names=set(old.namelist())|{PACKAGE.replace('.','/')+'/HasTrailingSlashPackagedTest.class'}
            validate_classes(z.namelist(),expected_test_names)
        originals=[cache.PROBE,BASE/'tests/org/dotj/internal/build/evaluation/AndConditionTest.java',packaged.CONSUMER]
        sources=[]
        for src in originals:
            staged=out/'consumer-source'/src.relative_to(BASE/'tests');staged.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,staged);sources.append(str(staged))
        args=[str(JDK/'bin/javac.exe'),*['-J'+x for x in cache.vm(out)],'--release','21','-encoding','UTF-8','--module-path',str(candidate),'--patch-module',MODULE+'='+str(out/'consumer-source')+';'+str(tests),'-sourcepath',str(out/'empty-sourcepath'),'-implicit:none','-d',str(out/'consumer-classes'),*sources]
        run('compile-successor-consumers',args,out/'unrelated-cwd')
        prefix=PACKAGE.replace('.','/')+'/'
        expected_classes={prefix+x for x in ['ConditionCachePackagedTest.class','AndConditionTest.class','AndConditionTest$Edge.class','HasTrailingSlashPackagedTest.class']}
        actual={p.relative_to(out/'consumer-classes').as_posix() for p in (out/'consumer-classes').rglob('*') if p.is_file()}
        validate_classes(actual,expected_classes);c.require(not list((out/'empty-sourcepath').iterdir()),'nonempty sourcepath')
        record['consumerOutputClasses']=sorted(actual);record['stagedConsumers']=[c.descriptor(x) for x in sources]
        patch=out/'fixture-tests.jar'
        with zipfile.ZipFile(tests) as z:entries={n:z.read(n) for n in z.namelist()}
        for pth in (out/'consumer-classes').rglob('*.class'):entries[pth.relative_to(out/'consumer-classes').as_posix()]=pth.read_bytes()
        validate_classes(entries,expected_test_names)
        with zipfile.ZipFile(patch,'x',zipfile.ZIP_STORED) as z:
            for name,data in sorted(entries.items()):z.writestr(name,data)
        record['fixtureTestsJar']=c.descriptor(patch)
        for target,source in [('cache','condition-cache-v1'),('condition','condition-logic-v2'),('and','and-conditions-v1')]:shutil.copytree(BASE/source/'fixtures',out/(target+'-fixtures'))
        for case in (BASE/'exists-site-directories-v1/fixtures').iterdir():shutil.copytree(case,out/'and-fixtures'/case.name)
        shutil.copyfile(BASE/'exists-site-directories-v1/cwd/cwd-only.marker',out/'unrelated-cwd/cwd-only.marker')
        def java(label,cls,args):
            return run(label,[str(JDK/'bin/java.exe'),*cache.vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(candidate),'--patch-module',MODULE+'='+str(patch),'-m',MODULE+'/'+PACKAGE+'.'+cls,*map(str,args)],out/'unrelated-cwd')
        for name,rows in [('cache',cache_rows),('condition',logic_rows)]:
            bridge=out/(name+'-bridge.tsv');bridge.write_text(v3.logic_bridge(rows),encoding='utf-8',newline='\n')
            result=out/(name+'-results.tsv');java('packaged-'+name,'ConditionCachePackagedTest',[bridge,out/(name+'-fixtures'),result,candidate,name])
            validate_lines(result.read_text().splitlines(),v3.logic_results(rows))
        bridge=out/'and-bridge.tsv';bridge.write_text(v3.and_product.bridge(and_rows),encoding='utf-8',newline='\n')
        java('packaged-and','AndConditionTest',['green',bridge,out/'and-fixtures',out/'and-results.tsv',out/'and-controls',candidate])
        v3.and_product.verify_probe_results(out/'and-results.tsv',and_rows)
        java('packaged-cache-controls','ConditionCachePackagedTest',[out/'cache-bridge.tsv',out/'cache-controls',out/'cache-controls.tsv',candidate,'controls'])
        validate_lines((out/'cache-controls.tsv').read_text().splitlines(),cache.control_rows())
        shutil.copytree(c.C/'fixtures',out/'predicate-fixtures')
        text=packaged.bridge(native);bridge=out/'predicate-bridge.tsv';bridge.write_text(text,encoding='utf-8',newline='\n')
        java('packaged-predicate','HasTrailingSlashPackagedTest',[bridge,out/'predicate-fixtures',out/'predicate-results.tsv',candidate,'corpus'])
        expected=[line[5:] for line in text.splitlines() if line.startswith('CASE\t')]
        validate_lines((out/'predicate-results.tsv').read_text().splitlines(),expected)
        java('packaged-predicate-controls','HasTrailingSlashPackagedTest',[bridge,out/'predicate-controls',out/'predicate-controls.tsv',candidate,'controls'])
        validate_lines((out/'predicate-controls.tsv').read_text().splitlines(),[
          'HT-STATIC-SYNTAX-AND-SKIPPED\tPRIVATE_CONTROL\t22_REFUSALS',
          'HT-WARM-LITERAL-DATA-AND-LAZY-TOKENIZATION\tPRIVATE_CONTROL\t17_SCALARS_2_LIST_REFUSALS',
          'HT-STATIC-ITEM-METADATA-FUNCTION\tPRIVATE_CONTROL\t3_REFUSALS',
          'HT-EXISTING-GROUP-NODE-BUDGETS\tPRIVATE_CONTROL\t64_65_255_257'])
        c.require(record['candidateJar']==c.descriptor(candidate),'candidate JAR changed between datasets')
        record['frozenInputsAfter']=frozen_inputs();c.require(record['frozenInputsBefore']==record['frozenInputsAfter'],'frozen inputs changed during qualification')
        for target,source in [('cache','condition-cache-v1'),('condition','condition-logic-v2'),('predicate','has-trailing-slash-v1')]:
            original=c.fixture_inventory(BASE/source/'fixtures');copied=c.fixture_inventory(out/(target+'-fixtures'))
            c.require({k:v['sha256'] for k,v in original.items()}=={k:v['sha256'] for k,v in copied.items()},'runtime fixture mutation')
        c.require(not list(out.rglob('must-not-exist.txt')),'task marker created')
        record['resultFiles']=[c.descriptor(p) for p in sorted(out.rglob('*results.tsv'))]+[c.descriptor(p) for p in sorted(out.glob('*controls.tsv'))]
        c.require(time.monotonic()<deadline,'aggregate deadline exceeded');record['status']='PASS_HAS_TRAILING_SLASH_PRODUCT_V1';save()
        artifacts=[c.descriptor(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name not in ['artifact-lock.json','controller-process.json','controller-receipt.json','controller.stdout','controller.stderr']]
        c.write(out/'artifact-lock.json',{'status':record['status'],'receipt':c.descriptor(out/'receipt.json'),'artifacts':artifacts})
    except BaseException as error:
        record['status']='FAILED_OR_DEFERRED';record['failure']={'type':type(error).__name__,'message':str(error)};save();raise

if __name__=='__main__':main()
