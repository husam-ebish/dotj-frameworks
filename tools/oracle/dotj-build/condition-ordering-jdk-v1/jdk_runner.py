"""Fixed baseline compile/runtime; no actual launch without separate exact review.

External PowerShell closes Python and launcher identity first. The owned900
controller begins before complete input hashing. No arbitrary argv/deadline.
"""
import argparse
import importlib.util
import os
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import jdk_contract as c
import jdk_stage as stage
import jdk_ownership as ownership


def guard_module():
    c.require(c.sha(c.GUARD)==c.GUARD_SHA,'unchanged qualified guard')
    spec=importlib.util.spec_from_file_location('jdk_qualified_owned_guard',c.GUARD)
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard);return guard


def approval(plan,source,review_sha):
    d=c.descriptor(plan['reviewPath']);c.require(d['sha256']==review_sha,'external independent operation review digest')
    review=c.read(d['path']);c.validate_review(review,plan['operation'],source)
    return d,review


def bootstrap(plan,source,review_sha,bootstrap_sha):
    path=c.WORK/'bootstrap'/(plan['attemptId']+'.json')
    d=c.descriptor(path);c.require(d['sha256']==bootstrap_sha,'actual external bootstrap record digest')
    value=c.read(path)
    c.require(value['status']=='EXTERNAL_PYTHON_BOOTSTRAP_VERIFIED' and value['sourceLockSha256']==source
              and value['reviewSha256']==review_sha and value['operation']==plan['operation']
              and value['pythonFiles']==34 and value['activePth']==['python313.zip','.']
              and value['siteEnabled'] is False and value['ownershipTimingIncludesBootstrap'] is False,
              'separate minimum external bootstrap before Python')
    c.require(c.finite(value['seconds']) and value['seconds']>=0,'measured bootstrap time')
    return d


def additional_inputs(review,review_descriptor,bootstrap_descriptor):
    ds=[review_descriptor,bootstrap_descriptor,review['fitEvidence']]
    if review['compilerProof']:
        ds += [review[k] for k in ['compilerProof','compilerControllerProof','compiledOutput']]
        child=c.read(review['compilerProof']['path']);parent=c.read(review['compilerControllerProof']['path'])
        ds += list(child['raw'].values())+list(parent['raw'].values())
        ds += [child['review'],child['bootstrap']]
    for d in ds:c.pin(d)
    return ds


def fixture_inventory(ctx,folder):
    descriptors=[]
    for case in [ctx.graph['baselineFixtureCase']]:
        for f in case['files']:
            descriptors.append(dict(path=str(folder/f['relativePath']),sha256=f['sha256'],sizeBytes=f['sizeBytes']))
    c.verify_inventory(folder,descriptors)


def stage_compile_sources(ctx):
    root=c.COMPILE
    for name in ['consumer-source','consumer-classes','empty-sourcepath','fixtures']:(root/name).mkdir()
    fixture=c.FIXTURE;d=ctx.path_descriptor(fixture)
    c.require(d['sha256']=='4aeea9d53cd66da0082becec13cf953abc6e2dfd35e6a2670b50c0c9f22724eb','unchanged baseline fixture')
    target=root/'consumer-source'/c.SOURCE_RELATIVE;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(ctx.raw(d))
    for case in [ctx.graph['baselineFixtureCase']]:
        for f in case['files']:
            source=ctx.path_descriptor(c.H/'fixtures'/f['relativePath'])
            target=root/'fixtures'/f['relativePath'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(ctx.raw(source))


def validate_staging(ctx, *, output_required):
    c.require(c.inventory(c.COMPILE/'empty-sourcepath')==[],'empty sourcepath, no implicit class shadow')
    source=c.COMPILE/'consumer-source'/c.SOURCE_RELATIVE
    c.require(c.inventory(c.COMPILE/'consumer-source')==[str(source)]
              and c.sha(source)=='4aeea9d53cd66da0082becec13cf953abc6e2dfd35e6a2670b50c0c9f22724eb','exact fixture-only source inventory')
    fixture_inventory(ctx,c.COMPILE/'fixtures')
    if output_required:return c.class_output(c.COMPILE/'consumer-classes')
    c.require(c.inventory(c.COMPILE/'consumer-classes')==[],'fresh compile output initially empty')


def inner(args):
    plan=c.operation(args.operation);source=args.source_lock_sha256
    policy=c.sha(c.HERE/'jdk-controller-policy-v1.json')
    envelope,ownership_proof,deadline=ownership.consume(args.ownership_handle,args.operation,source,args.review_sha256,policy)
    started=time.monotonic();root=Path(plan['cwd']);guard=guard_module()
    record=dict(schemaVersion=1,status='INCOMPLETE',operation=args.operation,attemptId=plan['attemptId'],sourceLockSha256=source,
                ownershipEnvelope=envelope,ownershipProof=ownership_proof,actualOuterDeadlineMonotonic=deadline,
                resourceAdmissions=[],failure=None,newJdkExecutions=dict(state='KNOWN',value=0),newNativeExecutions=0)
    code=1;process=None;pre=None;post=None
    try:
        review_d,review=approval(plan,source,args.review_sha256);boot=bootstrap(plan,source,args.review_sha256,args.bootstrap_sha256)
        record.update(review=review_d,bootstrap=boot,environment=plan['environment'])
        additional=additional_inputs(review,review_d,boot)
        pre=stage.full_inputs(source,review_descriptor=review_d);record['preClosure']=pre
        graph=c.read(c.HERE/'stage-inputs.json');ctx=stage.HistoricalContext(graph)
        if args.operation=='baseline-compile':stage_compile_sources(ctx)
        validate_staging(ctx,output_required=args.operation=='baseline-runtime')
        record['resourceSamples']=c.wait_resources(deadline,guard.memory)
        def admit():
            begin=time.monotonic();sample=guard.memory();end=time.monotonic();decision=time.monotonic()
            c.admission(deadline,decision,begin,end,sample)
            record['resourceAdmissions'].append(dict(queryStartedMonotonic=begin,queryFinishedMonotonic=end,
                decisionMonotonic=decision,actualOuterDeadlineMonotonic=deadline,sample=sample,childSeconds=120))
        is_compile=args.operation=='baseline-compile';label='compile' if is_compile else 'runtime'
        process=guard.run(plan['argv'],root,plan['environment'],label,120,prelaunch=admit,
                          stream_limits=c.POLICY['compilerCaps' if is_compile else 'runtimeCaps'])
        record['process']=process;record['newJdkExecutions']=dict(state='KNOWN',value=1 if process['launched'] else 0)
        # Always complete postclosure even if the actual product/tool process failed.
        post_start=time.monotonic();post=stage.full_inputs(source,review_descriptor=review_d)
        for d in additional:c.pin(d)
        output=validate_staging(ctx,output_required=True)
        c.require(time.monotonic()-post_start<=300,'actual postcheck within reserved300')
        record['postClosure']=post
        c.require(pre['stageInputsSha256']==post['stageInputsSha256'],'same full pre/post inputs')
        c.process_complete(process,plan,compile_success=is_compile)
        record['raw']={stream:c.descriptor(root/(label+'.'+stream)) for stream in ['stdout','stderr']}
        if is_compile:
            record.update(compiledOutput=output,status='COMPILE_COMPLETE_PENDING_ROOT_REVIEW')
        else:
            c.require(c.same(output,review['compiledOutput']),'actual runtime predecessor class unchanged')
            stdout=(root/'runtime.stdout').read_text(encoding='utf-8');stderr=(root/'runtime.stderr').read_text(encoding='utf-8')
            c.require(stdout.splitlines()[0].endswith(' classes='+str(pre['baseline']['productClasses'])),'all actual baseline product classes checked')
            record['classification']=c.classify_red(stdout,stderr,process['exitCode'],True)
            record.update(status='GENUINE_BASELINE_RED_PENDING_ROOT_REVIEW',compiledOutput=output)
        c.require(time.monotonic()+60<=deadline,'receipt metadata reserve remains')
        code=0
    except BaseException as error:
        record.update(status='FATAL_OR_CLEANUP_FAILURE',failure=dict(type=type(error).__name__,message=str(error)))
    finally:
        record['innerSeconds']=time.monotonic()-started
        if process:
            label='compile' if args.operation=='baseline-compile' else 'runtime'
            record['raw']={s:c.descriptor(root/(label+'.'+s)) for s in ['stdout','stderr'] if (root/(label+'.'+s)).exists()}
        c.fresh_json(root/'receipt.json',record)
    return code


def outer(args):
    plan=c.operation(args.operation);source=args.source_lock_sha256
    review_d,review=approval(plan,source,args.review_sha256);boot=bootstrap(plan,source,args.review_sha256,args.bootstrap_sha256)
    c.require(c.sha(c.HERE/'source-lock.json')==source,'new source lock identity before owned launch')
    root=Path(plan['cwd']);c.require(not root.exists(),'fresh fixed operation attempt, no retry')
    root.mkdir(parents=True);controller=root/'controller';controller.mkdir()
    for name in ['tmp','home/AppData/Roaming','home/AppData/Local']:(root/name).mkdir(parents=True,exist_ok=True)
    guard=guard_module();policy=c.sha(c.HERE/'jdk-controller-policy-v1.json')
    # This is the owned900 timing boundary; external bootstrap was independently measured.
    started=time.monotonic();cap=ownership.LaunchCapability(guard,args.operation,source,args.review_sha256,policy,started)
    argv=[str(c.PYTHON/'python.exe'),'-B',str(c.HERE/'jdk_runner.py'),'--inner',
          '--operation='+args.operation,'--source-lock-sha256='+source,'--review-sha256='+args.review_sha256,
          '--bootstrap-sha256='+args.bootstrap_sha256,'--ownership-handle='+str(cap.handle)]
    record=dict(schemaVersion=1,status='INCOMPLETE',operation=args.operation,attemptId=plan['attemptId'],sourceLockSha256=source,
                review=review_d,bootstrap=boot,outerStartedMonotonic=started,actualOuterDeadlineMonotonic=started+900,
                failure=None,innerReceipt=None,environment=c.environment(root),ownershipPipeHandle=cap.handle)
    code=1
    try:
        process=guard.run(argv,controller,c.environment(root),'controller',max(0,started+900-time.monotonic()),
                          launch=cap.launch,job_factory=cap.job_factory,stream_limits=c.POLICY['runtimeCaps'])
        record.update(process=process,ownershipEnvelope=cap.record)
        c.require(process['launched'] is True and process['jobAssigned'] is True and process['resumed'] is True
                  and process['exitCode']==0 and process['timedOut'] is False and process['outputLimitExceeded'] is False
                  and process.get('error') is None and process.get('cleanupError') is None and process['cleanupSeconds']<=5,'actual owned controller complete')
        record['innerReceipt']=c.descriptor(root/'receipt.json');child=c.read(root/'receipt.json')
        c.require(child['failure'] is None and child['status'] in ('COMPILE_COMPLETE_PENDING_ROOT_REVIEW','GENUINE_BASELINE_RED_PENDING_ROOT_REVIEW')
                  and child['sourceLockSha256']==source and c.same(child['ownershipEnvelope'],cap.record),'same actual child receipt')
        record['status']='CONTROLLER_COMPLETE_PENDING_ROOT_REVIEW';code=0
    except BaseException as error:record.update(status='FATAL_OR_CLEANUP_FAILURE',failure=dict(type=type(error).__name__,message=str(error)))
    finally:
        cap.close();record['raw']={s:c.descriptor(controller/('controller.'+s)) for s in ['stdout','stderr'] if (controller/('controller.'+s)).exists()}
        record['seconds']=time.monotonic()-started;c.fresh_json(controller/'receipt.json',record)
    return code


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--operation',choices=['baseline-compile','baseline-runtime'],required=True)
    for name in ['source-lock-sha256','review-sha256','bootstrap-sha256']:parser.add_argument('--'+name,required=True)
    parser.add_argument('--inner',action='store_true');parser.add_argument('--ownership-handle',type=int)
    args=parser.parse_args()
    for value in [args.source_lock_sha256,args.review_sha256,args.bootstrap_sha256]:c.require(type(value) is str and __import__('re').fullmatch('[0-9a-f]{64}',value),'exact required digest')
    if args.inner:c.capability_handle(args.ownership_handle)
    else:c.require(args.ownership_handle is None,'no caller ownership override')
    return inner(args) if args.inner else outer(args)


if __name__=='__main__':sys.exit(main())
