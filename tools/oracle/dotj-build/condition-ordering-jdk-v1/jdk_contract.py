"""Fixed baseline JDK contract. Imports perform no verification or process launch."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import struct
import time
import zipfile

B = Path('D:/AI/Implementation/dotj Frameworks')
W = B/'worktrees/dotj-build-ordering-conditions-v1'
H = W/'tools/oracle/dotj-build/condition-ordering-v1'
HERE = Path(__file__).resolve().parent
A = B/'agents/batch2518-build-ordering-preparation-v1'
WORK = A/'baseline-red-jdk-v1'
TEST_ROOT = A/'task104-jdk-preparation-v1'
PYTHON = B/'toolchains/python-3.13.9'
JDK = B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
GUARD = B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA = 'a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
BASE_JAR = B/'validation/Batch-2516-boolean-product-green-v3/dotj-build-evaluation-candidate.jar'
BASE_JAR_SHA = '97b027c56221716cc748aa03a80d24d65a180e13fb0deb07b059c2bbdd290b1c'
BRIDGE = A/'frozen-native-contract-v3/baseline-success-bridge.tsv'
BRIDGE_SHA = '8a788c21b54c120c089c3ec9fcc863505a6ab7f9bbf138adc8a7372a63436698'
CONTRACT_SHA = '9beb122636b028f01dccbdf4988c517160abcfdfcf06d374fcab470c70732452'
NATIVE_LOCK = 'a5ef29400f90ec8f12667b1611377358343607e5b5a0a712b020970a529ab7a8'
MODULE = 'org.dotj.build.evaluation.candidate'
CLASS_RELATIVE = 'org/dotj/internal/build/evaluation/OrderingBaselineTest.class'
SOURCE_RELATIVE = CLASS_RELATIVE[:-5]+'java'
COMPILE = WORK/'baseline-compile-attempt01'
RUNTIME = WORK/'baseline-runtime-attempt01'
FIXTURE = H/'java'/SOURCE_RELATIVE
POLICY = dict(schemaVersion=1, policyId='batch2518-jdk-baseline-v1', controllerSeconds=900,
              childSeconds=120, cleanupSeconds=5, postVerificationReserveSeconds=300,
              metadataReserveSeconds=60, resourceWaitMaximumSeconds=120, freshnessSeconds=2,
              freePhysicalBytes=536870912, availableSystemCommitBytes=17179869184,
              pollSeconds=0.1, compilerCaps=dict(stdout=2097152, stderr=2097152),
              runtimeCaps=dict(stdout=2097152, stderr=524288))


def require(ok, message):
    if not ok: raise ValueError(message)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def same(a, b):
    return type(a) is type(b) and canonical(a) == canonical(b)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('ascii')


def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def loads(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: require(False, 'nonfinite JSON value'))


def read(path):
    return loads(Path(path).read_text(encoding='utf-8-sig'))


def keys(value, names, label):
    require(type(value) is dict and set(value) == set(names), 'exact '+label+' fields')


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''): digest.update(block)
    return digest.hexdigest()


def regular_attributes(attributes, is_link):
    require(not is_link and not attributes & 0x400, 'symlink/reparse path forbidden')


def safe_path(path, *, directory=False):
    path = Path(path)
    require(path.is_absolute(), 'absolute path required')
    for item in [path, *path.parents]:
        info = item.lstat()
        regular_attributes(getattr(info, 'st_file_attributes', 0), stat.S_ISLNK(info.st_mode))
    require(path.is_dir() if directory else path.is_file(), 'regular file/directory required '+str(path))
    return path


def descriptor(path):
    path = safe_path(path)
    size = path.stat().st_size
    digest = sha(path)
    require(path.stat().st_size == size, 'file size changed while reading')
    return dict(path=str(path), sha256=digest, sizeBytes=size)


def descriptor_schema(d):
    keys(d, ['path','sha256','sizeBytes'], 'descriptor')
    require(type(d['path']) is str and Path(d['path']).is_absolute(), 'absolute descriptor path')
    require(type(d['sha256']) is str and re.fullmatch('[0-9a-f]{64}', d['sha256']), 'SHA256')
    require(type(d['sizeBytes']) is int and d['sizeBytes'] >= 0, 'descriptor size')


def pin(d):
    descriptor_schema(d)
    actual=descriptor(d['path'])
    require(actual['sha256']==d['sha256'] and actual['sizeBytes']==d['sizeBytes'], 'descriptor bytes/size mismatch '+d['path'])
    return d


def inventory(root):
    root = safe_path(root, directory=True)
    found = []
    for path in root.rglob('*'):
        info = path.lstat()
        regular_attributes(getattr(info, 'st_file_attributes', 0), stat.S_ISLNK(info.st_mode))
        require(path.is_file() or path.is_dir(), 'unsupported inventory entry')
        if path.is_file(): found.append(str(path))
    return sorted(found)


def verify_inventory(root, descriptors):
    paths = [d['path'] for d in descriptors]
    require(len(paths) == len(set(os.path.normcase(x) for x in paths)), 'duplicate/ambiguous inventory')
    require(inventory(root) == sorted(paths), 'exact inventory additions/removals '+str(root))
    for d in descriptors: pin(d)


def resolve_historical(d, entries):
    descriptor_schema(d)
    matches = [e for e in entries if same(e['original'], d)]
    require(len(matches) == 1, 'one exact authorized historical relation')
    e = matches[0]; descriptor_schema(e['archived'])
    require(e['relation'] == 'EXACT_RAW' and d['sha256'] == e['archived']['sha256']
            and d['sizeBytes'] == e['archived']['sizeBytes'], 'historical raw identity')
    return e['archived']


def validate_policy(value):
    require(same(value, POLICY), 'fixed JDK policy, no overrides or extra fields')


def wait_cutoff(deadline, now):
    require(finite(deadline) and finite(now), 'finite wait clock')
    return min(now+120, deadline-485)


def admission(deadline, decision, started, finished, sample):
    require(all(finite(x) for x in (deadline,decision,started,finished)), 'finite admission clocks')
    require(started <= finished <= decision and finished-started <= 2 and decision-started <= 2,
            'fresh synchronous query immediately before launch')
    require(decision+485 <= deadline, 'whole child120+cleanup5+post300+metadata60 reserve')
    keys(sample, ['freePhysicalBytes','freeVirtualBytes'], 'resource sample')
    require(all(type(sample[k]) is int and sample[k] >= floor for k, floor in
                [('freePhysicalBytes',536870912), ('freeVirtualBytes',17179869184)]),
            'free physical/AVAILABLE SYSTEM commit floor')


def wait_resources(deadline, query, now=time.monotonic, sleep=time.sleep):
    cutoff = wait_cutoff(deadline, now()); samples = []
    while now() < cutoff:
        start = now(); sample = query(); finish = now(); decision = now()
        require(finite(finish) and 0 <= finish-start <= 2, 'resource query freshness')
        samples.append(dict(queryStartedMonotonic=start, queryFinishedMonotonic=finish,
                            decisionMonotonic=decision, sample=sample))
        try: admission(deadline, decision, start, finish, sample)
        except ValueError:
            if decision >= cutoff: break
        else:
            require(decision < cutoff, 'resource wait cutoff')
            return samples
        sleep(max(0, min(0.1, cutoff-now())))
    raise ValueError('resource floor unavailable within fixed wait/reserve')


def environment(root):
    root = Path(root); home = str(root/'home'); drive, tail = os.path.splitdrive(home)
    return dict(SystemRoot='C:\\Windows', WINDIR='C:\\Windows', ComSpec='C:\\Windows\\System32\\cmd.exe',
                PATH=str(JDK/'bin')+';C:\\Windows\\System32', TEMP=str(root/'tmp'), TMP=str(root/'tmp'),
                HOME=home, USERPROFILE=home, HOMEDRIVE=drive, HOMEPATH=tail,
                APPDATA=str(root/'home/AppData/Roaming'), LOCALAPPDATA=str(root/'home/AppData/Local'),
                JAVA_HOME=str(JDK), VSLANG='1033', PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONUTF8='1')


def operation(name):
    require(name in ('baseline-compile','baseline-runtime'), 'fixed baseline operation allowlist')
    root = COMPILE if name == 'baseline-compile' else RUNTIME
    vm = ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC',
          '-Djava.io.tmpdir='+str(root/'tmp'), '-Duser.home='+str(root/'home'),
          '-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8',
          '-XX:ErrorFile='+str(root/'tmp/hs_err_pid%p.log'), '-XX:HeapDumpPath='+str(root/'tmp')]
    if name == 'baseline-compile':
        argv = [str(JDK/'bin/javac.exe')]+['-J'+v for v in vm]+[
            '--release','21','-encoding','UTF-8','-implicit:none','-sourcepath',str(COMPILE/'empty-sourcepath'),
            '--module-path',str(BASE_JAR),'--add-modules',MODULE,
            '--patch-module',MODULE+'='+str(COMPILE/'consumer-source'),
            '-d',str(COMPILE/'consumer-classes'),str(COMPILE/'consumer-source'/SOURCE_RELATIVE)]
    else:
        argv = [str(JDK/'bin/java.exe')]+vm+['--limit-modules','java.base,java.xml,'+MODULE,
            '--module-path',str(BASE_JAR),'--patch-module',MODULE+'='+str(COMPILE/'consumer-classes'),
            '-m',MODULE+'/org.dotj.internal.build.evaluation.OrderingBaselineTest',str(BASE_JAR),
            str(COMPILE/'fixtures'),str(BRIDGE),BRIDGE_SHA]
    return dict(operation=name, attemptId=name+'-attempt01', cwd=str(root), controllerOutput=str(root/'controller'),
                reviewPath=str(B/'orchestration/two-frameworks'/('batch2518-jdk-'+name+'-attempt01-review-v1.json')),
                argv=argv, environment=environment(root),
                output=dict(kind='DECLARED_SINGLE_CLASS_PRODUCED_BY_COMPILE', relativePath=CLASS_RELATIVE,
                            root=str(COMPILE/'consumer-classes'), maximumBytes=1048576),
                predecessor=None if name=='baseline-compile' else dict(kind='ACTUAL_SUCCESSFUL_COMPILE_PROOF_REQUIRED',
                                  path=str(COMPILE/'receipt.json'), operation='baseline-compile', attemptId='baseline-compile-attempt01'))


def validate_operation(value):
    require(type(value) is dict and value.get('operation') in ('baseline-compile','baseline-runtime'), 'operation')
    require(same(value, operation(value['operation'])), 'exact argv/environment/paths/dependency')


class OneUse:
    def __init__(self): self.used = False
    def take(self):
        require(not self.used, 'one-use capability already consumed')
        self.used = True


def capability_handle(handle):
    require(type(handle) is int and handle > 0, 'inherited pipe capability required; direct inner prohibited')


def validate_envelope(e, *, operation, source, review, policy, parent_pid, child_pid, now):
    keys(e, ['schemaVersion','operation','attemptId','sourceLockSha256','reviewSha256','policySha256',
             'guardSha256','outerStartedMonotonic','actualOuterDeadlineMonotonic','parentPid','childPid','parentJobHandle'], 'ownership envelope')
    require(type(e['schemaVersion']) is int and e['schemaVersion']==1, 'envelope version')
    require(operation in ('baseline-compile','baseline-runtime'), 'envelope operation')
    for k,v in [('operation',operation),('attemptId',operation+'-attempt01'),('sourceLockSha256',source),
                ('reviewSha256',review),('policySha256',policy),('guardSha256',GUARD_SHA)]:
        require(e[k] == v, 'ownership binding '+k)
    for k,v in [('parentPid',parent_pid),('childPid',child_pid)]:
        require(type(e[k]) is int and e[k] == v and v > 0, 'actual OS '+k)
    require(type(e['parentJobHandle']) is int and e['parentJobHandle'] > 0, 'actual Job HANDLE')
    start=e['outerStartedMonotonic']; deadline=e['actualOuterDeadlineMonotonic']
    require(all(finite(v) for v in (start,deadline,now)) and deadline==start+900 and start<=now<deadline,
            'one inherited monotonic start+900 deadline')
    return deadline


def class_output(root):
    root=Path(root); expected=root/CLASS_RELATIVE
    require(inventory(root)==[str(expected)], 'exact sole consumer class, no product/module/resource shadow')
    d=descriptor(expected)
    require(10 <= d['sizeBytes'] <= 1048576, 'bounded class output')
    raw=expected.read_bytes();require(raw[:4] == b'\xca\xfe\xba\xbe', 'classfile magic')
    offset=4
    def take(count):
        nonlocal offset
        require(offset+count<=len(raw),'bounded complete classfile header')
        value=raw[offset:offset+count];offset+=count;return value
    def u2():return struct.unpack('>H',take(2))[0]
    require(u2()==0 and u2()==65,'release21 classfile version')
    count=u2();pool=[None]*count;i=1
    while i<count:
        tag=take(1)[0]
        if tag==1:pool[i]=take(u2()).decode('utf-8')
        elif tag in [7,8,16,19,20]:pool[i]=(tag,u2())
        elif tag in [3,4,9,10,11,12,17,18]:take(4)
        elif tag in [5,6]:take(8);i+=1
        elif tag==15:take(3)
        else:raise ValueError('classfile constant-pool tag')
        i+=1
    u2();this=u2();require(0<this<len(pool) and type(pool[this]) is tuple and pool[this][0]==7,'classfile this_class')
    name=pool[this][1];require(0<name<len(pool) and pool[name]==CLASS_RELATIVE[:-6],'sole output actual internal class identity')
    return d


def process_complete(process, plan, *, compile_success):
    require(type(process) is dict, 'process record')
    require(same(process.get('argv'),plan['argv']) and process.get('cwd')==plan['cwd'], 'actual process argv/cwd')
    for key,value in [('timeoutSeconds',120),('cleanupLimitSeconds',5),('outputPollSeconds',0.1)]:
        require(type(process.get(key)) is type(value) and process[key]==value, 'actual process '+key)
    caps=POLICY['compilerCaps' if compile_success else 'runtimeCaps']
    require(same(process.get('outputLimitsBytes'),caps), 'actual stream caps')
    require(process.get('launched') is True and process.get('jobAssigned') is True and process.get('resumed') is True,
            'actual guarded child started')
    require(type(process.get('processId')) is int and process['processId']>0, 'actual child PID')
    require(process.get('timedOut') is False and process.get('outputLimitExceeded') is False
            and process.get('cleanupError') is None and process.get('error') is None, 'ordinary process termination')
    require(finite(process.get('cleanupSeconds')) and 0<=process['cleanupSeconds']<=5
            and finite(process.get('seconds')) and 0<=process['seconds']<=125, 'child/cleanup durations')
    code=process.get('exitCode')
    require(type(code) is int and (code==0 if compile_success else 0<code<125), 'ordinary compiler/runtime exit')
    keys(process.get('outputSizesBytes'), ['stdout','stderr'], 'actual output sizes')
    require(all(type(process['outputSizesBytes'][s]) is int and 0<=process['outputSizesBytes'][s]<=caps[s]
                for s in caps), 'bounded actual streams')


def classify_red(stdout, stderr, exit_code, complete_postclosure):
    require(type(exit_code) is int and 0<exit_code<125 and complete_postclosure is True, 'ordinary nonzero and complete postclosure')
    lines=stdout.splitlines()
    require(len(lines)==2 and re.fullmatch(re.escape('BASELINE_ORIGIN '+str(BASE_JAR)+' '+BASE_JAR_SHA)+r' classes=[1-9][0-9]*',lines[0])
            and lines[1]=='ORDERING_BASELINE_BEGIN ORD-HISTORY-BOOL-BOUND-ordering', 'exact ordered origin and real witness checkpoint, no END')
    error_lines=stderr.splitlines()
    require(error_lines and error_lines[0]=='Exception in thread "main" org.dotj.internal.build.evaluation.ProjectEvaluationComponent$ProfileRejected: Trailing condition syntax outside selected profile', 'uncaught real product trailing-syntax refusal')
    require(all(re.fullmatch(r'\s+at org\.dotj\.build\.evaluation\.candidate/org\.dotj\.internal\.build\.evaluation\.(ProjectEvaluationComponent(?:\$[A-Za-z0-9_]+)*|OrderingBaselineTest)\.[A-Za-z0-9_$<>]+\([A-Za-z]+\.java:[0-9]+\)',x) for x in error_lines[1:]), 'only exact product/fixture Java stack frames')
    require(any('ProjectEvaluationComponent$State$ConditionParser.parse(' in x for x in error_lines)
            and any('ProjectEvaluationComponent.evaluate(' in x for x in error_lines)
            and any('OrderingBaselineTest.main(' in x for x in error_lines), 'real parse/evaluate/fixture frames')
    return 'GENUINE_BASELINE_PRODUCT_RED'


def validate_compile_link(value, source, *, verify_files=True):
    require(type(value) is dict, 'actual compiler proof required')
    require(value.get('schemaVersion')==1 and type(value.get('schemaVersion')) is int
            and value.get('status')=='COMPILE_COMPLETE_PENDING_ROOT_REVIEW' and value.get('failure') is None,
            'actual successful compile proof')
    require(value.get('operation')=='baseline-compile' and value.get('attemptId')=='baseline-compile-attempt01'
            and value.get('sourceLockSha256')==source, 'actual predecessor operation/source binding')
    require(value.get('preClosure',{}).get('status')=='COMPLETE_STAGE_INPUT_CLOSURE'
            and value.get('postClosure',{}).get('status')=='COMPLETE_STAGE_INPUT_CLOSURE', 'both actual compiler closures')
    process_complete(value.get('process'),operation('baseline-compile'),compile_success=True)
    d=value.get('compiledOutput');descriptor_schema(d)
    require(d['path']==str(COMPILE/'consumer-classes'/CLASS_RELATIVE), 'actual compiler output path')
    require(type(value.get('resourceAdmissions')) is list and len(value['resourceAdmissions'])==1, 'actual compile admission')
    require(value.get('ownershipProof',{}).get('actualJobMembershipVerified') is True, 'actual compiler controller ownership')
    for stream in ['stdout','stderr']:
        descriptor_schema(value.get('raw',{}).get(stream))
        require(value['raw'][stream]['path']==str(COMPILE/('compile.'+stream)), 'actual compiler raw path')
        require(value['raw'][stream]['sizeBytes']==value['process']['outputSizesBytes'][stream], 'compile actual raw size')
    if verify_files:
        require(same(class_output(COMPILE/'consumer-classes'),d), 'immutable linked compiler output')
        for d in value['raw'].values():pin(d)
    return value['compiledOutput']


def validate_fit_times(pre, post, full):
    require(all(finite(x) and x>=0 for x in (pre,post,full)) and full>=pre+post,
            'finite complete measured fit times')
    require(pre<=295 and post<=300 and full+120+120+5+60<=900, 'full input-closure fit envelope')


def validate_review(value, operation_name, source, *, verify_files=True):
    keys(value,['schemaVersion','independentReviewer','operation','attemptId','sourceLockSha256','policySha256',
                'guardSha256','jdkInvocationApproved','invocationCountApproved','fitEvidence',
                'compilerProof','compilerControllerProof','compiledOutput'], 'independent JDK operation review')
    require(type(value['schemaVersion']) is int and value['schemaVersion']==1
            and type(value['independentReviewer']) is str and value['independentReviewer'].strip(), 'independent review identity')
    require(value['operation']==operation_name and value['attemptId']==operation_name+'-attempt01'
            and value['sourceLockSha256']==source and value['policySha256']==sha(HERE/'jdk-controller-policy-v1.json')
            and value['guardSha256']==GUARD_SHA, 'exact reviewed operation/source/policy/guard')
    require(value['jdkInvocationApproved'] is True and type(value['invocationCountApproved']) is int
            and value['invocationCountApproved']==1, 'one separately approved actual JDK invocation')
    d=value['fitEvidence'];descriptor_schema(d)
    require(d['path']==str(TEST_ROOT/'input-fit-fix1/timing.json'),'one authorized actual input-fit path')
    if verify_files:
        pin(d);fit=read(d['path'])
        require(fit['sourceLockSha256']==source and fit['policySha256']==value['policySha256']
                and fit['completeChecks']==2 and fit['status']=='TWO_COMPLETE_STAGE_INPUT_CHECKS_FIT', 'same actual full input-fit source/policy')
        validate_fit_times(fit['preSeconds'],fit['postSeconds'],fit['fullMeasuredSeconds'])
    if operation_name=='baseline-compile':
        require(value['compilerProof'] is None and value['compilerControllerProof'] is None and value['compiledOutput'] is None,
                'compile output is unknown, never preapproved predicted bytes')
    else:
        for name,path in [('compilerProof',COMPILE/'receipt.json'),('compilerControllerProof',COMPILE/'controller/receipt.json'),
                          ('compiledOutput',COMPILE/'consumer-classes'/CLASS_RELATIVE)]:
            descriptor_schema(value[name]);require(value[name]['path']==str(path),'actual linked '+name)
        if verify_files:
            for name in ['compilerProof','compilerControllerProof','compiledOutput']:pin(value[name])
            child=read(value['compilerProof']['path']);parent=read(value['compilerControllerProof']['path'])
            output=validate_compile_link(child,source)
            require(same(output,value['compiledOutput']) and same(parent['innerReceipt'],value['compilerProof'])
                    and parent['sourceLockSha256']==source and parent['operation']=='baseline-compile'
                    and parent['status']=='CONTROLLER_COMPLETE_PENDING_ROOT_REVIEW' and parent['failure'] is None,
                    'actual successful owned compile parent/child/output linkage')
            require(parent['process']['exitCode']==0 and parent['process']['timedOut'] is False
                    and parent['process'].get('cleanupError') is None and parent['process'].get('error') is None
                    and parent['process']['jobAssigned'] is True and parent['process']['resumed'] is True
                    and parent['process']['outputLimitExceeded'] is False, 'complete actual compiler controller')
    return value


def fresh_json(path,value):
    with Path(path).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
