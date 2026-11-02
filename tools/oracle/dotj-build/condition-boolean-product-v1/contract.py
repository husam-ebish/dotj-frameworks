"""Java-only successor contract. Frozen native outcomes are never rewritten."""
import base64,hashlib,importlib.util,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
W=HERE.parents[3];B=Path('D:/AI/Implementation/dotj Frameworks');BASE=W/'dotj-build/evaluation-candidate';H=HERE.parent/'condition-boolean-v1'
LOCK=B/'validation/Batch-2516-native-observation-v1/observation-lock.json'
LOCK_SHA='55e6ce90a9fb85991d216ffc8f2611de54565b13201a4af561053b3b8cabf0e0'
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
JDK=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1';PYTHON=B/'toolchains/python-3.13.9/python.exe'
MODULE='org.dotj.build.evaluation.candidate';PACKAGE='org.dotj.internal.build.evaluation'
def require(ok,why):
    if not ok:raise ValueError(why)
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def descriptor(p):
    p=Path(p);return {'path':str(p.resolve()),'sha256':sha(p),'sizeBytes':p.stat().st_size}
def pairs(items):
    d={}
    for k,v in items:require(k.casefold() not in {x.casefold() for x in d},'duplicate/case-distinct key');d[k]=v
    return d
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs)
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=True)+'\n',encoding='utf-8',newline='\n')
def pin(d):
    require(sha(d['path'])==d['sha256'],'hash mismatch '+d['path'])
    if 'sizeBytes' in d:require(Path(d['path']).stat().st_size==d['sizeBytes'],'size mismatch '+d['path'])
def descriptors(v):
    if type(v) is dict:
        if 'path'in v and 'sha256'in v:pin(v)
        for x in v.values():descriptors(x)
    elif type(v)is list:
        for x in v:descriptors(x)
def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
ARCHIVE=B/'validation/Batch-2516-historical-input-archive-v1/archive-lock.json'
ARCHIVE_SHA='02b5dd9a08e8db4b4251f212ba32b1c2d0f9e0de5357e0192c82599c43d9a1c0'
def historical_resolution():
    require(sha(ARCHIVE)==ARCHIVE_SHA,'archive identity');a=read(ARCHIVE);pin(a['originalNativeInputLock'])
    require(a['canonicalBaseCommit']=='2b659b4d581e8925e4386846015356244e7fbfe7','archive Git base')
    pins=read(a['originalNativeInputLock']['path'])['pins']
    canonical={str(Path(x['path']).resolve()):x for x in pins if Path(x['path']).is_relative_to(Path(a['canonicalRepository']))}
    entries={str(Path(x['original']['path']).resolve()):x for x in a['entries']}
    require(len(canonical)==14 and len(entries)==len(a['entries'])==14 and set(entries)==set(canonical),'archive exact14 bijection')
    for path,e in entries.items():
        original=canonical[path];require(e['original']==original,'archive original pin')
        pin(e['archived']);pin(e['gitBlob']);require(e['archived']['sha256']==original['sha256'] and e['archived']['sizeBytes']==original['sizeBytes'],'archive exact raw bytes')
        blob=Path(e['gitBlob']['path']).read_bytes();oid=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()
        require(oid==e['gitObjectId'],'archived Git object bytes/OID')
        raw=Path(e['archived']['path']).read_bytes()
        require((raw==blob and e['workingVsGitRelation']=='EXACT_RAW') or (raw.replace(b'\r\n',b'\n')==blob and e['workingVsGitRelation']=='WORKTREE_CRLF_VS_GIT_LF'),'explicit Git/worktree relation')
    for item in pins:
        if str(Path(item['path']).resolve()) not in entries:pin(item)
    return a
def frozen():
    historical_resolution()
    require(sha(LOCK)==LOCK_SHA,'native lock pin');descriptors(read(LOCK))
    require(sha(B/'orchestration/two-frameworks/task71-next-build-condition-scope-plan-v1.json')=='d6c4e91c739d7727fe05daf8645dadf6a93ad20aa8e75f3499baa543300f76cf','plan changed')
    review=B/'orchestration/two-frameworks/task84-build-boolean-fault-contract-review-v1.json'
    require(sha(review)=='72bc60ef0270a260d9155e9800579311d5bf8337978a7ad7ae8cb4874d741500','fault review pin')
    ruling=read(B/'orchestration/two-frameworks/batch2516-root-fault-contract-ruling-v1.json');require(ruling['status']=='ROOT_ADOPTED_PRIVATE_FAULT_CONTRACT','fault ruling approval')
    red=B/'validation/Batch-2516-baseline-red-v1/behavior-red.json';require(sha(red)=='4b21b681f26137e29c444814f493a58e4f85baf784ebbfe19bf13008c062d366','RED changed')
    for x in read(H/'predecessor-preservation-lock.json')['files']:pin(x)
    require(len(read(H/'predecessor-preservation-lock.json')['files'])==391,'391 predecessors')
    require(len(read(H/'predecessor-transitions.json')['inventory'])==223,'223 case/control inventory')
    for profile in ['condition-boolean-v1','condition-boolean-capture-v2','condition-boolean-observer-v3']:
        # All frozen files remain locked by the exported pre-implementation closure.
        require((HERE.parent/profile).is_dir(),'frozen profile missing')
    for x in read(H/'python-runtime-manifest.json')['files']:pin(x)
    require(sha(GUARD)==GUARD_SHA,'guard changed')
    return read(LOCK.parent/'observations.json')['rows']
def enc(s):require(type(s)is str,'scalar type');return base64.b64encode(s.encode()).decode()
def rel(s,ident,prefix='<fixture-root>'):
    before=prefix+'\\'+ident+'\\';require(s.startswith(before),'native path outside exact fixture case '+s)
    out=s[len(before):].replace('\\','/');require(all(x not in ['.','..',''] for x in out.split('/')),'native relative path');return out
def successful_fields(row,prefix='<fixture-root>'):
    ident=row['id'];ev=row['evaluation'];require(ev['success'] is True,'success type')
    imports='|'.join(rel(e['owner'],ident,prefix)+'>'+rel(e['project'],ident,prefix)+'@'+str(e['line'])+':'+str(e['column']) for e in ev['imports'])
    warnings=[]
    for d in row['diagnostics']:
        require(d['kind']=='warning' and d['code']=='MSB4130' and d['endLine']==0 and d['endColumn']==0,'warning schema/mapping')
        match=re.fullmatch(r'The condition "(.*)" may have been evaluated incorrectly in an earlier version of MSBuild\. Please verify that the order of the AND and OR clauses is written as intended\. To avoid this warning, add parentheses to make the evaluation order explicit\.',d['message']);require(match is not None,'warning message grammar')
        warnings.append(d['code']+':'+rel(d['file'],ident,prefix)+'@'+str(d['line'])+':'+str(d['column'])+':'+match[1])
    return [enc(ev['properties']['P']),enc(ev['properties']['Q']),enc(imports),enc('|'.join(warnings))]
def native_records(rows):
    manifest=read(H/'manifest.json')['cases'];require([r['id'] for r in rows]==[d['id'] for d in manifest],'297 IDs/order')
    require(len(rows)==297,'full297')
    maps={'MSB4113':'CONDITION_NOT_BOOLEAN','MSB4100':'CONDITION_NOT_BOOLEAN_CHILD','MSB4088':'CONDITION_ILL_FORMED','MSB4092':'CONDITION_PROFILE','MSB4101':'CONDITION_PROFILE','MSB4115':'CONDITION_PROFILE','MSB4019':'MSB4019'}
    records=[]
    for row,d in zip(rows,manifest):
        require(row['globals']==d['globals'] and row['taskMarkerAbsent'] is True,'globals/marker')
        ev=row['evaluation'];ident=row['id'];kind='MATCHED_EVALUATION';reason='Selected native P/Q, ordered imports and available private warning fields; Default duplicate unavailable mapped to null.'
        if ev.get('outcome')=='runtime-fault-v3':
            require(ident in ['BOOL-EMPTY-06','BOOL-EMPTY-07','BOOL-EMPTY-08'] and ev['type']=='System.NullReferenceException','unapproved fault')
            kind='SOURCE_BASED_PRIVATE_ADAPTATION_NO_CONDITIONED_PROPERTIES';fields=['','','',''];reason='Root-adopted Task84 source no-inventory empty-side false; operator not executed; native NRE unchanged; excluded from paired parity.'
        elif ident.startswith('BOOL-BAD-') and ident.endswith('-skipped'):
            kind='DECLARED_PRIVATE_PROFILE_RESTRICTION';fields=['CONDITION_PROFILE'];reason='Inherited static XML condition syntax validation includes skipped XML; native skips this site.'
        elif ident=='BOOL-LAZY-09':
            kind='DECLARED_PRIVATE_PROFILE_RESTRICTION';fields=['IMPORT_PATH_PROFILE'];reason='Inherited reached Exists empty relative path refusal; native predicate returns false.'
        elif ev['success'] is False:
            kind='MATCHED_PRIVATE_FAILURE';fields=[maps[ev['code']]];reason='Explicit native error-to-private category mapping, not exact exception ABI/message/location parity. Failure-time warning fields retained in native evidence but private thrown failure exposes no warning list.'
        else:fields=successful_fields(row)
        records.append({'id':ident,'disposition':kind,'expectedFields':fields,'globals':row['globals'],'condition':d['condition'],'nativeEvaluation':ev,'nativeDiagnostics':row['diagnostics'],'reason':reason,'nativePairedParityEligible':kind=='MATCHED_EVALUATION'})
    return records
def private_records():
    out=[]
    for d in read(H/'private-cases.json')['cases']:
        prediction=d['prediction'];ident=d['id']
        if prediction=='accepted':
            fields=['','','',''] if ident=='BOOL-BOUND-not256' else [enc('yes'),enc('taken'),'',''];kind='PRIVATE_DESIGN_SUCCESS'
        else:fields=['PROPERTY_FUNCTION' if ident in ['BOOL-BOUND-item','BOOL-BOUND-metadata'] else prediction];kind='PRIVATE_DESIGN_REFUSAL'
        out.append({'id':ident,'disposition':kind,'expectedFields':fields,'globals':{},'condition':d['condition'],'reason':'Private parser/profile design; raw item/metadata maps to existing static PROPERTY_FUNCTION category; no native parity.'})
    require(len(out)==16,'16 private inputs');return out
def bridge(records):
    lines=[]
    for r in records:
        lines.append('\t'.join(['CASE',r['id'],r['disposition'],*r['expectedFields']]))
        for k,v in r['globals'].items():lines.append('\t'.join(['GLOBAL',enc(k),enc(v)]))
        lines.append('END')
    return '\n'.join(lines)+'\n'
def validate_contract(value,rows):
    require(type(value)is dict and value.get('schemaVersion')==1 and type(value['schemaVersion'])is int,'contract schema')
    require(value['nativeLock']==descriptor(LOCK) and value['historicalInputArchive']==descriptor(ARCHIVE),'native/archive descriptors')
    require(value['nativeRecords']==native_records(rows),'consumed native records differ from immutable observed source')
    require(value['privateRecords']==private_records(),'private design inputs changed')
    require(value['transitions']==read(H/'predecessor-transitions.json')['transitions'],'18 exact transitions/provenance')
    require(value['groups']==read(H/'java-controls.json')['groups'],'14 control group assertions changed')
    require(value['counts']=={'nativeIds':297,'nativeSuccess':248,'nativeProjectErrors':46,'nativeFaults':3,'privateInputs':16,'privateGroups':14,'predecessorFiles':391,'predecessorInventory':223,'transitionIds':18,'conditionSuccessor':[28,5,2],'htSyntaxSuccessor':[18,4]},'typed count contract')
    require(value['normalization']=='Exact <fixture-root> case-relative paths only; no value/error/warning suppression.','normalization widened')
    return True
def make_contract(rows):
    result={'schemaVersion':1,'status':'PRIVATE_CANDIDATE_QUALIFICATION_CONTRACT','nativeLock':descriptor(LOCK),'historicalInputArchive':descriptor(ARCHIVE),'runtimeNumericSource':[descriptor(B/'reference/upstream/runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6'/x) for x in ['src/libraries/System.Private.CoreLib/src/System/Number.Parsing.cs','src/libraries/Common/src/System/Number.Parsing.Common.cs']],'nativeRecords':native_records(rows),'privateRecords':private_records(),'transitions':read(H/'predecessor-transitions.json')['transitions'],'groups':read(H/'java-controls.json')['groups'],'counts':{'nativeIds':297,'nativeSuccess':248,'nativeProjectErrors':46,'nativeFaults':3,'privateInputs':16,'privateGroups':14,'predecessorFiles':391,'predecessorInventory':223,'transitionIds':18,'conditionSuccessor':[28,5,2],'htSyntaxSuccessor':[18,4]},'normalization':'Exact <fixture-root> case-relative paths only; no value/error/warning suppression.','privateErrors':'New Boolean/illformed categories map named source failures, no exact exception ABI. Existing syntax/import/profile boundaries retained.','ASCII':'Scalar Boolean/numeric/text conversion refuses non-ASCII expanded values when reached. Static scalar syntax boundary retained, including skipped raw literals. HasTrailingSlash remains ordinary Unicode data with separate conversion.','numeric':'Invariant signed decimal point grammar, NaN variants, finite binary64; then prefixed Int32 hex with leading zeros and two-s-complement; no exponent/suffix/hex-float/whitespace; source/native selected72 predicates only.','acceptanceCredit':0}
    validate_contract(result,rows);return result
if __name__=='__main__':
    rows=frozen();value=make_contract(rows);write(HERE/'CONTRACT.json',value);print('PREPARED',len(value['nativeRecords']),len(value['privateRecords']))
