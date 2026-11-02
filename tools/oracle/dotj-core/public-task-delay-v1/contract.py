"""Closed parsing and proof consumption. This module never launches a process."""
import base64
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = Path('D:/AI/Implementation/dotj Frameworks').resolve()

def require(ok, why):
    if not ok:
        raise ValueError(why)

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def descriptor(path):
    path = Path(path).resolve()
    return {'path':str(path),'sha256':sha(path),'sizeBytes':path.stat().st_size}

def keys(obj, expected, label):
    require(type(obj) is dict and set(obj) == set(expected), 'closed keys: ' + label)

def unique_pairs(pairs):
    out = {}
    for k,v in pairs:
        require(k not in out, 'duplicate JSON key: ' + k)
        out[k] = v
    return out

def read(path, limit=16*1024**2):
    path = Path(path)
    require(path.stat().st_size <= limit, 'oversize JSON input')
    with path.open('rb') as stream:
        raw = stream.read(limit+1)
    require(len(raw) <= limit, 'growing input')
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs)

def write_new(path, obj):
    with Path(path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent=2, ensure_ascii=True)
        f.write('\n')

def validate_pin(item):
    keys(item, ['path','sha256','sizeBytes'], 'descriptor')
    require(type(item['sizeBytes']) is int and item['sizeBytes'] >= 0, 'pin size type')
    require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}',item['sha256']) is not None, 'pin hash')
    require(descriptor(item['path']) == item, 'stale input: ' + item['path'])

def confined(path):
    path=Path(path).resolve()
    require(path.is_relative_to(B) and path != B, 'outpath outside D implementation root')
    return path

def fresh_output(path):
    path=confined(path)
    require(not path.exists(), 'output already exists')
    return path

def validate_manifest(manifest):
    keys(manifest, ['version','status','rows','caseCount','coverageGroups','nativePartitions','passes','largeDurationPolicy','caseInputOrder'], 'manifest')
    require(type(manifest['version']) is int and manifest['version']==1, 'manifest version')
    require(type(manifest['caseCount']) is int and manifest['caseCount']==len(manifest['rows']), 'case count')
    require(manifest['status']=='DESIGNED_NOT_OBSERVED' and manifest['passes']==2, 'manifest status')
    ids=set()
    for row in manifest['rows']:
        keys(row,manifest['caseInputOrder'],'case')
        require(all(type(v) is str for v in row.values()),'case input types')
        require(re.fullmatch('D[0-9]{3}',row['id']) is not None and row['id'] not in ids,'duplicate or invalid case ID')
        ids.add(row['id'])
        require(re.fullmatch('0|-?[1-9][0-9]*',row['value']) is not None and -(2**63)<=int(row['value'])<2**63,'canonical Int64 string')
        require(row['partition'] in manifest['nativePartitions'],'case partition')
    return manifest

def wire(raw, schema, manifest, partition):
    validate_manifest(manifest)
    require(type(raw) is bytes and 0 < len(raw) <= 2*1024**2,'wire size')
    require(partition in manifest['nativePartitions'],'partition')
    expected=[r for r in manifest['rows'] if r['partition']==partition]
    lines=raw.decode('utf-8',errors='strict').split('\n')
    require(lines[-1]=='','missing final newline');lines.pop()
    normalized=[]
    for line in lines:
        if line.endswith('\r'):line=line[:-1]
        require(not any(ch in line for ch in '\r\v\f\x00\x1c\x1d\x1e\x85\u2028\u2029'),'illegal line separator')
        normalized.append(line)
    lines=normalized
    identity=schema['globalIdentity']
    require(lines.pop(0)=='META\t'+identity['profile']+'\t'+identity['runtime']+'\t'+identity['manifestSha256'],'global identity')
    result={}; cursor=0
    for case in expected:
        cid=case['id']
        require(cursor<len(lines) and lines[cursor]=='BEGIN\t'+cid,'BEGIN/order/missing case: '+cid);cursor+=1
        row={}
        for unused in range(len(schema['fields'])):
            require(cursor<len(lines),'partial case')
            parts=lines[cursor].split('\t');cursor+=1
            require(len(parts)==3,'scalar framing')
            key,kind,value=parts
            require(key.startswith(cid+'.'),'case identity')
            field=key[len(cid)+1:]
            require(field in schema['fields'] and field not in row,'unknown/duplicate scalar')
            require(kind==schema['fields'][field],'scalar type')
            if kind=='b':
                require(value in ['true','false'],'boolean encoding');decoded=value=='true'
            elif kind=='i':
                require(re.fullmatch('0|-?[1-9][0-9]*',value) is not None,'integer encoding')
                decoded=int(value);require(-(2**31)<=decoded<2**31,'int32 range')
            elif kind=='s':
                data=base64.b64decode(value,validate=True)
                require(base64.b64encode(data).decode()==value,'base64 canonical')
                decoded=data.decode('utf-8',errors='strict')
            else:raise ValueError('unknown schema type')
            row[field]=decoded
        require(cursor<len(lines) and lines[cursor]=='END\t'+cid,'END/partial case: '+cid);cursor+=1
        result[cid]=row
    require(cursor==len(lines),'extra cases/scalars')
    return result

RACE_VARYING_FIELDS=frozenset(['kind','status','successful','canceled','awaitType','awaitTaskIdentity','awaitTokenEqual',
    'repeatType','repeatTaskIdentity','repeatTokenEqual','awaitMessage','awaitHresult','repeatMessage','repeatHresult','winner'])

def race_invariants(row):
    require(row['kind'] in ['success','canceled'],'closed race terminal kind')
    canceled=row['kind']=='canceled'
    require(row['status']==('Canceled' if canceled else 'RanToCompletion') and row['winner']==('cancel' if canceled else 'timer'),'race outcome/status/winner coupling')
    require(row['completed'] is True and row['successful'] is (not canceled) and row['canceled'] is canceled and row['faulted'] is False and row['exceptionNull'] is True,'race terminal flags')
    for prefix in ['await','repeat']:
        require(row[prefix+'Type']==('System.Threading.Tasks.TaskCanceledException' if canceled else 'returned'),'race await kind')
        require(row[prefix+'TaskIdentity'] is canceled and row[prefix+'TokenEqual'] is canceled,'race await identity')
        require(type(row[prefix+'Hresult']) is int and row[prefix+'Hresult']==(-2146233029 if canceled else 0),'race typed HResult')
        require(row[prefix+'Message']==('A task was canceled.' if canceled else ''),'race typed exception message')
    require(row['exceptionType']==row['message']==row['paramName']==row['actualValueKind']==row['actualValue']=='' and row['hresult']==0,'race no top-level error payload')
    require(row['callbackCalls']==1 and row['sameCallStack'] is False,'race callback/affinity')
    require(row['completedTaskIdentity'] is False and row['tokenCanBeCanceled'] is True and row['tokenRequested'] is True,'race producer/token invariants')
    require(row['shape']=='' and row['lateCalls']==0 and row['unsafeCalls']==0 and all(row[k] is False for k in ['stateBeforeReturn','secondWhileBlocked','asyncCompleted']),'race stable observation defaults')

def invariants(payload, manifest):
    cases={r['id']:r for r in manifest['rows']}
    for cid,row in payload.items():
        c=cases[cid];scenario=c['scenario']
        require(row['kind'] not in ['runtimeFault','faulted'],'unexpected runtime fault: '+cid)
        if scenario=='shape':
            require(row['kind']=='shape' and row['shape'].startswith('public static System.Threading.Tasks.Task '),'shape');continue
        if scenario=='invoke':
            require(row['kind']==c['expectedKind'],'source expected branch: '+cid)
            if c['api'].startswith('Delay') and row['kind']!='argument':
                milliseconds=int(int(c['value'])/10000) if c['api'].startswith('DelaySpan') else int(c['value'])
                require(row['completedTaskIdentity'] is (milliseconds==0 and row['kind']=='success'),'zero CompletedTask/precanceled precedence')
        if row['kind']=='argument':
            require(row['exceptionType']=='System.ArgumentOutOfRangeException' and row['paramName']==c['expectedParamName'],'parameter identity')
            require(row['hresult']==-2146233086 and row['actualValueKind']=='null' and row['actualValue']=='','argument typed payload')
            require(bool(row['message']),'exception message retained');continue
        require(not row['faulted'] and row['exceptionNull'],'no-fault state')
        if row['kind']=='canceled':
            require(row['completed'] and row['canceled'] and not row['successful'] and row['status']=='Canceled','canceled flags')
            for prefix in ['await','repeat']:
                require(row[prefix+'Type']=='System.Threading.Tasks.TaskCanceledException' and row[prefix+'TaskIdentity'] and row[prefix+'TokenEqual'],'TCE identity')
                require(type(row[prefix+'Hresult']) is int and bool(row[prefix+'Message']),'typed TCE payload')
        elif row['kind']=='success':
            require(row['completed'] and row['successful'] and not row['canceled'] and row['status']=='RanToCompletion','success flags')
            require(row['awaitType']=='returned' and row['repeatType']=='returned','successful await')
        elif row['kind']=='pending':
            require(not row['completed'] and row['status']=='WaitingForActivation','pending state')
        if scenario=='callbacks':require(row['callbackCalls']==row['lateCalls']==row['unsafeCalls']==1 and row['stateBeforeReturn'],'exactly-once callbacks')
        if scenario=='shared':require(row['callbackCalls']==2,'shared-token count')
        if scenario=='cancelAsync':require(row['callbackCalls']==2 and row['asyncCompleted'],'CancelAsync')
        if scenario=='dispatch':require(row['callbackCalls']==1 and row['stateBeforeReturn'] and row['secondWhileBlocked'] and not row['sameCallStack'],'cancellation dispatch/publication')
        if scenario=='isolation':require(row['secondWhileBlocked'] and row['stateBeforeReturn'],'independent timer')
        if scenario=='race':
            race_invariants(row)

def compare(first, second, manifest):
    require(set(first)==set(second),'comparison manifest completeness')
    invariants(first,manifest);invariants(second,manifest)
    for c in manifest['rows']:
        cid=c['id']
        if cid not in first:continue
        if c['scenario']=='race':
            # Every allowed-varying field is validated against its complete outcome above.
            # All remaining fields compare exactly; raw output is never modified.
            require({k:v for k,v in first[cid].items() if k not in RACE_VARYING_FIELDS}==
                    {k:v for k,v in second[cid].items() if k not in RACE_VARYING_FIELDS},'stable race field difference: '+cid)
            continue
        require(first[cid]==second[cid],'stable ordinary field difference: '+cid)

def validate_approval(approval, phase, lock_sha, command_sha, binding_sha):
    keys(approval,['version','status','phase','inputLockSha256','commandSha256','artifactBindingSha256','reviewer','reviewReceiptSha256','parentTimeoutSeconds'], 'phase approval')
    require(type(approval['version']) is int and approval['version']==1,'approval version')
    require(approval['status']=='APPROVED_FOR_ONE_PHASE' and approval['phase']==phase,'phase approval mismatch')
    require(approval['inputLockSha256']==lock_sha and approval['commandSha256']==command_sha and approval['artifactBindingSha256']==binding_sha,'approval binding mismatch')
    require(approval['reviewer']=='root' and re.fullmatch('[0-9a-f]{64}',approval['reviewReceiptSha256']) is not None,'independent root review receipt')
    require(type(approval['parentTimeoutSeconds']) is int and approval['parentTimeoutSeconds']==180,'parent envelope')

def count_attempt(record):
    require(type(record.get('launched')) is bool,'launch flag')
    return 1 if record['launched'] else 0

def successful(record, exit_code=0):
    require(record.get('launched') is True and type(record.get('exitCode')) is int and record['exitCode']==exit_code and record.get('timedOut') is False and record.get('jobAssigned') is True and record.get('resumed') is True and not any(record.get(k) for k in ['error','cleanupError','outputLimitExceeded']),'failed actual child')

def consumed_capture(receipt_path, expected_receipt_hash, schema, manifest):
    from root_phase import consume_root
    outer=read(receipt_path)
    receipt=consume_root(receipt_path,expected_receipt_hash,'native-capture')
    require(outer['innerReceipt']['sha256']==sha(outer['innerReceipt']['path']),'bound inner capture bytes')
    return consumed_inner_capture(outer['innerReceipt']['path'],outer['innerReceipt']['sha256'],schema,manifest)

def consumed_inner_capture(receipt_path, expected_receipt_hash, schema, manifest):
    require(sha(receipt_path)==expected_receipt_hash,'capture receipt hash')
    receipt=read(receipt_path)
    require(receipt['phase']=='native-capture' and receipt['status']=='CAPTURED_PENDING_ROOT_REVIEW','capture phase/status')
    validate_pin(receipt['artifactBinding']);binding=read(receipt['artifactBinding']['path'])
    validate_pin(binding['dll']);validate_pin(binding['runtimeconfig']);validate_pin(binding['compileReceipt'])
    validate_pin(receipt['inputLock']);validate_pin(receipt['approval']);validate_pin(receipt['commandDescriptor'])
    lock=read(receipt['inputLock']['path']);validate_pin(lock['schema']);validate_pin(lock['manifest'])
    import phase_tools
    phase_tools.verify_binding(binding,lock,receipt['inputLock']['sha256'])
    require(lock['schema']['sha256']==sha(HERE/'schema.json') and lock['manifest']['sha256']==sha(HERE/'fixture-manifest.json'),'capture schema binding')
    command=read(receipt['commandDescriptor']['path'])
    require(command['phase']=='native-capture' and command['inputLockSha256']==receipt['inputLock']['sha256'] and command['artifactBinding']==receipt['artifactBinding'],'consumed native descriptor binding')
    require(command['argv']==phase_tools.command('native-capture',Path(command['cwd']),lock,binding,receipt['partition']),'consumed exact native argv')
    validate_approval(read(receipt['approval']['path']),'native-capture',receipt['inputLock']['sha256'],receipt['commandDescriptor']['sha256'],receipt['artifactBinding']['sha256'])
    require(receipt['command']['argv']==command['argv'],'consumed argv')
    successful(receipt['command'])
    require(receipt['actualLaunches']==1,'actual launch counter')
    for stream in receipt['streams'].values():validate_pin(stream)
    require(receipt['streams']['stdout']['path']==receipt['command']['stdoutPath'],'stdout binding')
    payload=wire(Path(receipt['streams']['stdout']['path']).read_bytes(),schema,manifest,receipt['partition'])
    invariants(payload,manifest)
    return payload
