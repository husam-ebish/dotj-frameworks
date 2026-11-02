"""Ordering v1 closed data protocol. Importing this file never launches a process.

Only fixture-root prefixes in path/message fields may normalize. Fault stacks
and all raw streams remain exact. ProjectError stack is UNAVAILABLE in reused
observer v3; absence of a process receipt means UNKNOWN execution count.
"""
import copy
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
B=Path('D:/AI/Implementation/dotj Frameworks')
A=B/'agents/batch2518-build-ordering-preparation-v1'
W=B/'worktrees/dotj-build-ordering-conditions-v1'
COMPILED=B/'agents/batch2516-observer-fault-preparation-v1/compiled-observer'
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
BASE_JAR=B/'validation/Batch-2516-boolean-product-green-v3/dotj-build-evaluation-candidate.jar'
BASE_JAR_SHA='97b027c56221716cc748aa03a80d24d65a180e13fb0deb07b059c2bbdd290b1c'
ID=re.compile(r'[A-Za-z0-9_-]{1,96}\Z',re.ASCII)
HEX=re.compile(r'[0-9a-f]{64}\Z',re.ASCII)
MODULE='org.dotj.build.evaluation.candidate'

def require(ok,message):
    if not ok:raise ValueError(message)
def keys(v,expected,label):
    require(type(v) is dict and set(v)==set(expected),label+' exact fields')
def string(v,label):require(type(v) is str,label+' string')
def integer(v,label,low=None):
    require(type(v) is int and (low is None or v>=low),label+' integer')
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def pairs(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON field '+k);out[k]=v
    return out
def loads(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON number '+x)))
def read(path):return loads(Path(path).read_text(encoding='utf-8'))
def bounded(path,limit):
    path=Path(path);require(path.stat().st_size<=limit,'bounded raw file')
    raw=path.read_bytes();require(len(raw)<=limit,'bounded growing raw file');return raw
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()
def descriptor(path):
    path=Path(path);require(path.is_file() and not path.is_symlink(),'regular nonlink file '+str(path))
    return dict(path=str(path),sha256=sha(path),sizeBytes=path.stat().st_size)
def check_descriptor(d):
    keys(d,['path','sha256','sizeBytes'],'descriptor');string(d['path'],'path')
    require(type(d['sha256']) is str and HEX.fullmatch(d['sha256']),'sha256');integer(d['sizeBytes'],'size',0)
def pin(d):
    check_descriptor(d);require(same(d,descriptor(d['path'])),'file binding '+d['path']);return d
def resolve_history(d,entries):
    check_descriptor(d)
    matches=[x['archived'] for x in entries if same(x['original'],d)]
    require(len(matches)==1,'exact explicit historical descriptor required')
    check_descriptor(matches[0]);require(matches[0]['sha256']==d['sha256'] and matches[0]['sizeBytes']==d['sizeBytes'],'archive bytes')
    return matches[0]

def manifest(m):
    keys(m,['schemaVersion','status','groups','cases','javaOnlyControls'],'manifest')
    require(type(m['schemaVersion']) is int and m['schemaVersion']==1 and m['status']=='DESIGNED_NOT_OBSERVED','manifest version/status')
    require(type(m['groups']) is list and len(m['groups'])==12 and len(set(m['groups']))==12,'twelve groups')
    require(type(m['cases']) is list and m['cases'],'nonempty cases')
    seen=set()
    for c in m['cases']:
        keys(c,['id','group','globals','condition','site','purpose','sourceAnchor','nativeStatus','productScope','files','historicalId'],'case')
        require(type(c['id']) is str and ID.fullmatch(c['id']) and c['id'] not in seen,'unique ASCII case ID');seen.add(c['id'])
        require(c['group'] in m['groups'] and c['site'] in ['Property','PropertyGroup','Import','ImportGroup'],'group/site')
        for k in ['condition','purpose','sourceAnchor','productScope']:string(c[k],k)
        require(c['nativeStatus']=='NOT_LAUNCHED_NOT_OBSERVED','unobserved case')
        require(c['historicalId'] is None or type(c['historicalId']) is str,'history ID')
        require(type(c['globals']) is dict and all(type(k) is str and type(v) is str for k,v in c['globals'].items()),'globals string map')
        require(len({k.upper() for k in c['globals']})==len(c['globals']),'global name collision')
        require(type(c['files']) is list and c['files'],'case files')
        file_names=[]
        for f in c['files']:
            keys(f,['relativePath','sha256','sizeBytes'],'fixture descriptor');integer(f['sizeBytes'],'fixture size',0)
            require(type(f['sha256']) is str and HEX.fullmatch(f['sha256']),'fixture digest')
            string(f['relativePath'],'fixture relative path');path=Path(f['relativePath']);require(not path.is_absolute() and path.parts[0]==c['id'] and '..' not in path.parts,'fixture containment')
            file_names.append(f['relativePath'])
        require(len(file_names)==len(set(file_names)),'unique fixture paths')
        require(c['id']+'/main.proj' in [f['relativePath'] for f in c['files']],'main.proj required')
    require(set(c['group'] for c in m['cases'])==set(m['groups']),'all groups populated')
    require(type(m['javaOnlyControls']) is list,'Java-only controls')
    return m

def fixtures(m,root):
    manifest(m);root=Path(root).resolve();expected=set()
    for c in m['cases']:
        for f in c['files']:
            path=root/f['relativePath'];require(path.resolve().is_relative_to(root) and not path.is_symlink(),'fixture path')
            require(path.stat().st_size==f['sizeBytes'] and sha(path)==f['sha256'],'fixture byte binding')
            raw=path.read_bytes();require(b'\0' not in raw and b'<!DOCTYPE' not in raw.upper(),'secured XML input')
            ET.fromstring(raw);expected.add(path.resolve())
    require(expected=={x.resolve() for x in root.rglob('*') if x.is_file()},'exact fixture inventory')

def imports(v):
    require(type(v) is list,'imports array')
    for e in v:
        keys(e,['owner','project','line','column'],'import')
        for k in ['owner','project']:string(e[k],k)
        for k in ['line','column']:integer(e[k],k,0)
def diagnostics(v):
    require(type(v) is list,'diagnostics array')
    for d in v:
        keys(d,['kind','code','file','line','column','endLine','endColumn','message'],'diagnostic')
        require(d['kind'] in ['warning','error'],'diagnostic kind')
        for k in ['code','file','message']:string(d[k],k)
        for k in ['line','column','endLine','endColumn']:integer(d[k],k,0)
def row(r,case_id,globals):
    keys(r,['id','globals','profile','evaluation','diagnostics','cleanup','taskMarkerAbsent'],'row')
    require(r['id']==case_id and same(r['globals'],globals) and r['profile']=='Default','row identity/globals/profile')
    diagnostics(r['diagnostics']);keys(r['cleanup'],['before','loaded','afterUnload','disposed'],'cleanup')
    for k in ['before','loaded','afterUnload']:integer(r['cleanup'][k],k,0)
    require(r['cleanup']['before']==0 and r['cleanup']['afterUnload']==0 and r['cleanup']['disposed'] is True and r['taskMarkerAbsent'] is True,'cleanup/lifecycle/marker')
    ev=r['evaluation'];require(type(ev) is dict,'evaluation object')
    if ev.get('outcome')=='runtime-fault-v3':
        keys(ev,['outcome','type','message','hresult','stack'],'runtime fault')
        for k in ['type','message']:string(ev[k],k)
        require(ev['type'] not in ['System.OutOfMemoryException','System.StackOverflowException','System.AccessViolationException','System.Runtime.InteropServices.SEHException','System.Threading.ThreadAbortException','Microsoft.Build.Exceptions.InvalidProjectFileException'],'fatal/ProjectError cannot be nonfatal fault')
        require(ev['stack'] is None or type(ev['stack']) is str,'runtime-fault stack nullable emitted field required')
        integer(ev['hresult'],'hresult');return 'UNEXPECTED_NONFATAL_RUNTIME_FAULT'
    require(type(ev.get('success')) is bool,'success boolean')
    if ev['success']:
        keys(ev,['success','properties','imports','duplicateImports','duplicateGetterFailure'],'success')
        keys(ev['properties'],['P','Q'],'properties')
        for k in ['P','Q']:string(ev['properties'][k],k)
        imports(ev['imports'])
        require(ev['duplicateImports'] is None or type(ev['duplicateImports']) is list,'nullable duplicate imports')
        if ev['duplicateImports'] is not None:imports(ev['duplicateImports'])
        if ev['duplicateGetterFailure'] is not None:
            keys(ev['duplicateGetterFailure'],['type','message'],'duplicate getter')
            for k in ['type','message']:string(ev['duplicateGetterFailure'][k],k)
        require(not (ev['duplicateImports'] is not None and ev['duplicateGetterFailure'] is not None),'getter success/failure exclusive')
        return 'SUCCESS'
    keys(ev,['success','type','code','file','line','column','endLine','endColumn','message','hresult'],'ProjectError: stack UNAVAILABLE')
    for k in ['type','code','file','message']:string(ev[k],k)
    for k in ['line','column','endLine','endColumn']:integer(ev[k],k,0)
    integer(ev['hresult'],'hresult');return 'PROJECT_ERROR'

def observation(v,cases,fingerprint):
    keys(v,['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile','rows'],'observation')
    for k in ['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath','profile']:
        require(type(v[k]) is str and v[k]==fingerprint[k],'native assembly/runtime binding '+k)
    require(type(v['rows']) is list and len(v['rows'])==len(cases),'exact row count')
    return [row(r,c['id'],c['globals']) for r,c in zip(v['rows'],cases)]
def progress(raw,ids,complete):
    require(type(raw) is str,'stderr text');expected=[(phase,i) for i in ids for phase in ['BEGIN','END']];got=[]
    for line in raw.splitlines():
        if line.startswith('DOTJ_OBSERVER_V3'):
            m=re.fullmatch(r'DOTJ_OBSERVER_V3 (BEGIN|END) ([A-Za-z0-9_-]{1,96})',line)
            require(m is not None,'malformed progress');got.append(m.groups())
    require(got==expected if complete else got==expected[:len(got)],'ordered complete/prefix progress')
    return got
def normalize(v,root):
    require(type(root) is str and root,'explicit fixture root')
    def walk(x,key=''):
        if type(x) is dict:return {k:walk(value,k) for k,value in x.items()}
        if type(x) is list:return [walk(i,key) for i in x]
        if type(x) is str and key in ['file','owner','project','message']:
            return x.replace(root+'/', '<fixture-root>/').replace(root+'\\','<fixture-root>\\')
        return x
    return walk(copy.deepcopy(v))
def execution_count(process):
    if process is None:return dict(state='UNKNOWN',value=None)
    require(type(process.get('launched')) is bool,'typed launch state')
    return dict(state='KNOWN',value=1 if process['launched'] else 0)
def process_outcome(process):
    if process is None:return 'FATAL_OR_CLEANUP_FAILURE'
    if process.get('launched') is True and type(process.get('exitCode')) is int and process['exitCode']==0 and process.get('jobAssigned') is True and process.get('resumed') is True and process.get('cleanupError') is None and process.get('error') is None and process.get('timedOut') is False and process.get('outputLimitExceeded') is False and type(process.get('cleanupSeconds')) in [int,float] and 0<=process['cleanupSeconds']<=5:return 'PROCESS_COMPLETE'
    return 'FATAL_OR_CLEANUP_FAILURE'
def process_receipt(process,argv,cwd,timeout,profile):
    require(type(process) is dict,'process receipt required')
    require(same(process.get('argv'),argv) and process.get('cwd')==str(cwd),'process exact argv/cwd')
    require(type(process.get('timeoutSeconds')) is int and process['timeoutSeconds']==timeout,'process timeout')
    require(type(process.get('cleanupLimitSeconds')) is int and process['cleanupLimitSeconds']==5,'cleanup reserve')
    require(type(process.get('outputPollSeconds')) in [int,float] and process['outputPollSeconds']==0.1,'output poll')
    require(process.get('outputProfile')==profile,'stream profile')
    limits={'stdout':2097152,'stderr':2097152 if profile=='compiler' else 524288}
    require(same(process.get('outputLimitsBytes'),limits),'fixed stream caps')
    require(process_outcome(process)=='PROCESS_COMPLETE','process complete/cleanup')
    integer(process.get('processId'),'actual process PID',1)
    keys(process.get('outputSizesBytes'),['stdout','stderr'],'output sizes')
    for stream in ['stdout','stderr']:
        integer(process['outputSizesBytes'][stream],stream+' bytes',0)
        require(process['outputSizesBytes'][stream]<=limits[stream],'stream cap '+stream)
    require(type(process.get('seconds')) in [int,float] and 0<=process['seconds']<=timeout+5,'process wall duration')
    return process
def admission(deadline,now,sampled,sample,child_seconds):
    require(type(deadline) in [int,float] and type(now) in [int,float] and type(sampled) in [int,float],'monotonic times')
    require(0<=now-sampled<=2,'fresh admission sample')
    require(child_seconds in [30,120] and type(child_seconds) is int and now+child_seconds+5<=deadline,'whole child and cleanup reserve against actual outer deadline')
    require(type(sample) is dict and all(type(sample.get(k)) is int and sample[k]>=floor for k,floor in [('freePhysicalBytes',512*1024**2),('freeVirtualBytes',16*1024**3)]),'physical and AVAILABLE commit floor')
def approval(v,execution,phase):
    keys(v,['schemaVersion','independentReviewer','executionLockSha256','phase','nativeApproved','reuseObserverApproved','newCompilerExecutions','invocationCountApproved'],'independent approval')
    require(type(v['schemaVersion']) is int and v['schemaVersion']==1 and type(v['independentReviewer']) is str and v['independentReviewer'].strip(),'review identity/version')
    require(v['executionLockSha256']==execution and v['phase']==phase and v['nativeApproved'] is True and v['reuseObserverApproved'] is True,'new profile/phase/reuse approval')
    require(type(v['newCompilerExecutions']) is int and v['newCompilerExecutions']==0 and type(v['invocationCountApproved']) is int and v['invocationCountApproved']>0,'review execution bounds')
def example_approval(execution,phase):
    return dict(schemaVersion=1,independentReviewer='PURE_CONTROL_ONLY',executionLockSha256=execution,phase=phase,nativeApproved=True,reuseObserverApproved=True,newCompilerExecutions=0,invocationCountApproved=1)
def example_row(kind):
    # Artificial protocol controls, never native observations.
    r=dict(id='ORD-TEST',globals={},profile='Default',diagnostics=[],cleanup=dict(before=0,loaded=1,afterUnload=0,disposed=True),taskMarkerAbsent=True)
    if kind=='SUCCESS':ev=dict(success=True,properties=dict(P='yes',Q='taken'),imports=[],duplicateImports=None,duplicateGetterFailure=dict(type='System.InvalidOperationException',message='control'))
    elif kind=='PROJECT_ERROR':ev=dict(success=False,type='Microsoft.Build.Exceptions.InvalidProjectFileException',code='MSB4086',file='main.proj',line=2,column=1,endLine=0,endColumn=0,message='pure control',hresult=-1)
    else:ev=dict(outcome='runtime-fault-v3',type='System.NullReferenceException',message='pure control',hresult=-1,stack='pure control stack')
    r['evaluation']=ev;return r
