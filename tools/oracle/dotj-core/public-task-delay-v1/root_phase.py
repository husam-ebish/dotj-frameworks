"""Root-owned 180s parent. Full payload/admission work runs only in its owned child.

No function runs at import. Dedicated root entrypoints select a fixed phase.
"""
import importlib.util
import hashlib
import json
import os
import time
from pathlib import Path
import contract as c
import phase_tools as phase

CONTEXT_KEYS=['version','phase','outerDirectory','phaseDirectory','inputLockSha256','descriptorSha256','approvalSha256',
    'assessmentSha256','artifactBindingSha256','startedMonotonic','deadlineMonotonic','timeoutSeconds','rootLauncher','outerImplementation','ownerProcessId']

def bootstrap_pin(path,limit=16*1024**2):
    """Bound the small bootstrap-document reads; heavy transitively pinned work is owned."""
    path=Path(path).resolve()
    with path.open('rb') as stream:raw=stream.read(limit+1)
    c.require(len(raw)<=limit,'bootstrap document cap')
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'sizeBytes':len(raw)}

def context_check(context,expected_phase,lock_sha,descriptor_sha,approval_sha,phase_directory,now):
    c.keys(context,CONTEXT_KEYS,'outer context')
    c.require(type(context['version']) is int and context['version']==1 and context['phase']==expected_phase,'outer phase')
    c.require(context['inputLockSha256']==lock_sha and context['descriptorSha256']==descriptor_sha and context['approvalSha256']==approval_sha,'outer input/approval binding')
    c.require(Path(context['phaseDirectory']).resolve()==Path(phase_directory).resolve(),'outer output binding')
    c.require(type(context['timeoutSeconds']) is int and context['timeoutSeconds']==180,'outer timeout')
    c.require(type(context['startedMonotonic']) is float and type(context['deadlineMonotonic']) is float and context['deadlineMonotonic']==context['startedMonotonic']+180,'outer deadline identity')
    c.require(context['startedMonotonic']<=now<context['deadlineMonotonic'],'expired/future outer context')
    c.require(type(context['ownerProcessId']) is int and context['ownerProcessId']>0,'outer owner PID metadata')

def reserve(deadline,now,child_seconds):
    c.require(type(child_seconds) is int and child_seconds in [30,120],'child ceiling')
    c.require(now+child_seconds+5<=deadline,'NO_CHILD: actual outer deadline cannot fit child ceiling plus cleanup5')

def workload_count(inner,outer_context_sha):
    # On an outer timeout or interrupted inner receipt, zero is not knowable.
    if type(inner) is not dict or type(inner.get('outerContext')) is not dict or inner['outerContext'].get('sha256')!=outer_context_sha:return None
    count=inner.get('actualLaunches')
    if type(count) is not int or count not in [0,1]:return None
    if count==1:return 1
    return 0 if inner.get('finalized') is True and inner.get('status')=='DEFERRED_NO_CHILD' else None

def run(fixed_phase):
    parser=phase.parser('root-'+fixed_phase)
    for name in ['descriptor','descriptor-sha256','approval','approval-sha256','assessment','assessment-sha256','outer-out']:
        parser.add_argument('--'+name,required=True)
    args=parser.parse_args()
    for name in ['input_lock','descriptor','approval','assessment']:setattr(args,name,str(Path(getattr(args,name)).resolve()))
    # Only bounded small admission documents are read in the root controller.
    c.require(bootstrap_pin(args.input_lock)['sha256']==args.input_lock_sha256 and bootstrap_pin(args.descriptor)['sha256']==args.descriptor_sha256 and bootstrap_pin(args.approval)['sha256']==args.approval_sha256 and bootstrap_pin(args.assessment)['sha256']==args.assessment_sha256,'root supplied hashes')
    lock=c.read(args.input_lock);descriptor=c.read(args.descriptor);approval=c.read(args.approval);assessment=c.read(args.assessment)
    c.require(descriptor['phase']==fixed_phase and descriptor['inputLockSha256']==args.input_lock_sha256,'root fixed phase')
    binding=descriptor['artifactBinding'];binding_sha=binding['sha256'] if binding else None
    c.validate_approval(approval,fixed_phase,args.input_lock_sha256,args.descriptor_sha256,binding_sha)
    c.require(approval['reviewReceiptSha256']==args.assessment_sha256,'root assessment/approval coupling')
    readiness='conditionalNativeReady' if fixed_phase=='native-capture' else 'readyForSourceCompile' if fixed_phase=='source-compile' else 'readyForBaselineCompile'
    c.require(assessment.get(readiness) is True,'independent review not ready for phase')
    out=c.fresh_output(args.outer_out);phase_out=c.fresh_output(descriptor['cwd'])
    c.require(out!=phase_out and not out.is_relative_to(phase_out) and not phase_out.is_relative_to(out),'separate outer/inner outputs')
    c.validate_pin(lock['guard'])
    c.require(lock['guard']['sha256']=='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125','unchanged original guard')
    executable=c.B/'toolchains/python-3.13.9/python.exe'
    entry=c.HERE/(fixed_phase+'.py');root_entry=c.HERE/('root-'+fixed_phase+'.py')
    producer_pins={x['path']:x for x in lock['producerFiles']}
    for path in [entry,root_entry,Path(__file__).resolve()]:c.validate_pin(producer_pins[str(path.resolve())])
    out.mkdir(parents=True)
    for name in ['tmp','home/AppData/Roaming','home/AppData/Local','cache/nuget','cache/http']:(out/name).mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('batch2517_root_owned_guard',lock['guard']['path']);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    env=phase.environment(out)
    # This timestamp is the guard's actual first clock sample. Context/argv construction consumes it.
    started=time.monotonic()
    context={'version':1,'phase':fixed_phase,'outerDirectory':str(out),'phaseDirectory':str(phase_out),
        'inputLockSha256':args.input_lock_sha256,'descriptorSha256':args.descriptor_sha256,'approvalSha256':args.approval_sha256,
        'assessmentSha256':args.assessment_sha256,'artifactBindingSha256':binding_sha,'startedMonotonic':started,
        'deadlineMonotonic':started+180,'timeoutSeconds':180,'rootLauncher':c.descriptor(root_entry),'outerImplementation':c.descriptor(__file__),'ownerProcessId':os.getpid()}
    c.write_new(out/'outer-context.json',context);context_pin=c.descriptor(out/'outer-context.json')
    argv=[str(executable),'-B',str(entry),'--input-lock',args.input_lock,'--input-lock-sha256',args.input_lock_sha256,
        '--descriptor',args.descriptor,'--descriptor-sha256',args.descriptor_sha256,'--approval',args.approval,'--approval-sha256',args.approval_sha256,
        '--outer-context',context_pin['path'],'--outer-context-sha256',context_pin['sha256']]
    receipt={'version':1,'status':'ROOT_PARENT_PREPARING','phase':fixed_phase,'passNumber':descriptor['passNumber'],'partition':descriptor['partition'],
        'outerPythonLaunches':0,'innerWorkloadLaunches':None,'innerCountState':'UNKNOWN_UNTIL_BOUND_INNER_RECEIPT',
        'rootLauncher':context['rootLauncher'],'outerImplementation':context['outerImplementation'],'guard':lock['guard'],
        'inputLock':c.descriptor(args.input_lock),'descriptor':c.descriptor(args.descriptor),'approval':c.descriptor(args.approval),'assessment':c.descriptor(args.assessment),
        'artifactBinding':binding,'outerContext':context_pin,'argv':argv,'environment':env,'command':None,'streams':{},'innerReceipt':None,'finalized':False}
    def save():(out/'root-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    def update(record):
        receipt['command']=dict(record);receipt['outerPythonLaunches']=c.count_attempt(record)
        inner_path=phase_out/'receipt.json'
        if inner_path.is_file():
            try:
                inner=c.read(inner_path);count=workload_count(inner,context_pin['sha256'])
                if count is not None:receipt['innerWorkloadLaunches']=count;receipt['innerCountState']='BOUND_INNER_EVIDENCE'
            except (ValueError,OSError):pass
        save()
    first=[True]
    def guard_clock():
        if first[0]:first[0]=False;return started
        return time.monotonic()
    save()
    try:
        record=guard.run(argv,out,env,'controller',180,on_update=update,now=guard_clock)
        for stream in ['stdout','stderr']:receipt['streams'][stream]=c.descriptor(record[stream+'Path'])
        inner_path=phase_out/'receipt.json'
        if inner_path.is_file():receipt['innerReceipt']=c.descriptor(inner_path)
        c.successful(record)
        c.require(receipt['innerReceipt'] is not None,'missing final inner receipt')
        inner=c.read(inner_path)
        c.require(inner.get('finalized') is True and inner['outerContext']==context_pin,'inner completion binding')
        c.require(inner['status'] in ['COMPILED_PENDING_ARTIFACT_BINDING','CAPTURED_PENDING_ROOT_REVIEW','GENUINE_PACKAGED_API_RED_PENDING_ROOT_REVIEW'],'inner phase did not qualify')
        c.require(inner['actualLaunches']==1 and type(inner['actualLaunches']) is int,'inner actual workload count')
        receipt['innerWorkloadLaunches']=1;receipt['innerCountState']='BOUND_FINAL_INNER_EVIDENCE'
        receipt['status']='ROOT_PHASE_COMPLETED_PENDING_REVIEW'
    except BaseException as error:
        receipt['status']='ROOT_PHASE_FAILED_RETAINED';receipt['failure']=str(error);raise
    finally:receipt['finalized']=True;save()

def consume_root(path,digest,expected_phase):
    c.require(c.sha(path)==digest,'root receipt supplied hash')
    receipt=c.read(path)
    c.require(receipt['status']=='ROOT_PHASE_COMPLETED_PENDING_REVIEW' and receipt['phase']==expected_phase and receipt['finalized'] is True,'root phase completion')
    c.successful(receipt['command'])
    c.require(type(receipt['outerPythonLaunches']) is int and receipt['outerPythonLaunches']==1 and type(receipt['innerWorkloadLaunches']) is int and receipt['innerWorkloadLaunches']==1,'root actual counters')
    for key in ['rootLauncher','outerImplementation','guard','inputLock','descriptor','approval','assessment','outerContext','innerReceipt']:c.validate_pin(receipt[key])
    for pin in receipt['streams'].values():c.validate_pin(pin)
    c.require(receipt['command']['argv']==receipt['argv'] and receipt['command']['timeoutSeconds']==180,'owned outer argv/timeout')
    inner=c.read(receipt['innerReceipt']['path']);context=c.read(receipt['outerContext']['path'])
    expected_argv=[str(c.B/'toolchains/python-3.13.9/python.exe'),'-B',str(c.HERE/(expected_phase+'.py')),
        '--input-lock',receipt['inputLock']['path'],'--input-lock-sha256',receipt['inputLock']['sha256'],
        '--descriptor',receipt['descriptor']['path'],'--descriptor-sha256',receipt['descriptor']['sha256'],
        '--approval',receipt['approval']['path'],'--approval-sha256',receipt['approval']['sha256'],
        '--outer-context',receipt['outerContext']['path'],'--outer-context-sha256',receipt['outerContext']['sha256']]
    c.require(receipt['argv']==expected_argv and Path(receipt['command']['cwd']).resolve()==Path(context['outerDirectory']).resolve() and receipt['environment']==phase.environment(Path(context['outerDirectory'])),'consumed fixed outer invocation')
    for stream in ['stdout','stderr']:c.require(receipt['streams'][stream]['path']==receipt['command'][stream+'Path'],'outer stream binding')
    c.require(inner['finalized'] is True and inner['outerContext']==receipt['outerContext'] and inner['phase']==expected_phase,'bound final inner evidence')
    c.require(type(inner['actualLaunches']) is int and inner['actualLaunches']==1,'consumed actual inner count')
    c.require(inner['inputLock']==receipt['inputLock'] and inner['approval']==receipt['approval'] and inner['commandDescriptor']==receipt['descriptor'],'root/inner source inputs')
    c.validate_pin(inner['payloadAdmission']);admission=c.read(inner['payloadAdmission']['path'])
    c.require(admission['outerContext']==receipt['outerContext'] and admission['inputLock']==receipt['inputLock'] and admission['descriptor']==receipt['descriptor'] and admission['status']=='FULL_PAYLOAD_VERIFIED_FOR_THIS_OUTER_PHASE','full payload admission binding')
    c.require(admission['finishedMonotonic']<=inner['childAdmissionMonotonic']<context['deadlineMonotonic'],'payload/admission order')
    lock=c.read(receipt['inputLock']['path']);c.require(admission['payload']==lock['payload'],'payload manifest admission binding')
    payload=c.read(lock['payload']['path']);c.require(admission['counts']=={name:item['count'] for name,item in payload['payloads'].items()},'full payload count closure')
    reserve(context['deadlineMonotonic'],inner['childAdmissionMonotonic'],inner['command']['timeoutSeconds'])
    c.require(receipt['approval']['sha256']==context['approvalSha256'] and receipt['assessment']['sha256']==context['assessmentSha256'],'outer review binding')
    binding_sha=receipt['artifactBinding']['sha256'] if receipt['artifactBinding'] else None
    approval=c.read(receipt['approval']['path'])
    c.validate_approval(approval,expected_phase,receipt['inputLock']['sha256'],receipt['descriptor']['sha256'],binding_sha)
    c.require(approval['reviewReceiptSha256']==receipt['assessment']['sha256'] and context['artifactBindingSha256']==binding_sha,'consumed review/artifact binding')
    return inner
