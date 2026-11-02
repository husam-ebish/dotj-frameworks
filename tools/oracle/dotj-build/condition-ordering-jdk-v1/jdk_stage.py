"""Finite live JDK closure; completed native verification is pinned prior evidence.

Authority: task104-finite-jdk-input-boundary-ruling-v1, cd4a2677. Historical
audit references are discoverable but deliberately not traversed/requalified.
"""
import hashlib
from pathlib import Path
import time
import zipfile
import jdk_contract as c
import jdk_jar


class HistoricalContext:
    """Explicit finite roles, no historical path fallback or recursive walker."""
    def __init__(self,graph):
        c.require(graph['schemaVersion']==2 and graph['boundary']=='FINITE_JDK_INPUTS_PRIOR_COMPLETED_NATIVE_EVIDENCE','finite boundary version')
        self.graph=graph
        self.files=list(graph['references'].values())+graph['baselineFixtureFiles']
        self.files+=[e['original'] for e in graph['additionalArchiveEntries']]
        self.current_lock={'manifest':graph['references']['fixtureManifest']}

    def path_descriptor(self,path):
        matches=[d for d in self.files if str(Path(d['path']))==str(Path(path))]
        unique={c.canonical(d):d for d in matches}
        c.require(len(unique)==1,'one finite named input '+str(path))
        return next(iter(unique.values()))

    def raw(self,d):
        c.require(any(c.same(d,x) for x in self.files),'declared finite input')
        entries=[e for e in self.graph['additionalArchiveEntries'] if c.same(e['original'],d)]
        c.require(len(entries)<=1,'no ambiguous archival mapping')
        path=entries[0]['archived']['path'] if entries else d['path']
        return Path(path).read_bytes()

    def json(self,d):return c.loads(self.raw(d).decode('utf-8-sig'))
    def role(self,name):return self.json(self.graph['references'][name])


def archive_relations(ctx):
    for e in ctx.graph['additionalArchiveEntries']:
        c.pin(e['archived']);c.resolve_historical(e['original'],[e])
        if e['gitBlob']:
            c.pin(e['gitBlob']);raw=Path(e['archived']['path']).read_bytes();git=Path(e['gitBlob']['path']).read_bytes()
            c.require(hashlib.sha1(b'blob '+str(len(git)).encode()+b'\0'+git).hexdigest()==e['gitObjectId'],'exact Git object bytes')
            relation=e['gitRelation']
            if relation=='EXACT_RAW_EQUALS_GIT':c.require(raw==git,'exact raw/Git relation')
            elif relation=='RAW_CRLF_GIT_LF':c.require(raw.replace(b'\r\n',b'\n')==git and b'\r\n' in raw,'explicit CRLF/LF relation')
            elif relation=='RAW_LF_GIT_CRLF':c.require(git.replace(b'\r\n',b'\n')==raw and b'\r\n' in git,'explicit LF/CRLF relation')
            else:c.require(relation=='EXPLICIT_RAW_DIFFERS_FROM_GIT' and raw!=git,'explicit raw/Git difference')
        else:c.require(e['gitRelation']=='UNTRACKED_OR_EXTERNAL_NO_GIT_BLOB' and e['gitObjectId'] is None,'explicit absence of Git provenance, never invented')
    return dict(archivedOriginals=len(ctx.graph['additionalArchiveEntries']),old14='RETAINED_PRIOR_ARCHIVE_AUDIT_REFERENCE_NOT_REQUALIFIED')


def native_contract(ctx):
    refs=ctx.graph['references'];contract=ctx.role('contract');acceptance=ctx.role('acceptance');command=ctx.role('freezeCommand');approval=ctx.role('freezeApproval')
    c.require(refs['contract']['sha256']==c.CONTRACT_SHA and refs['bridge']['sha256']==c.BRIDGE_SHA
              and refs['nativeSourceLock']['sha256']==c.NATIVE_LOCK,'fixed completed native evidence identity')
    c.require(acceptance['status']=='NATIVE_CONTRACT_TWO_PASSES_MATCHED_AND_FROZEN_NOT_PRODUCT_QUALIFICATION'
              and acceptance['executionLockSha256']==contract['executionLockSha256']==c.NATIVE_LOCK,'completed native prerequisite source identity')
    for key in ['contract','bridge','freezeCommand']:c.require(c.same(acceptance[key],refs[key]),'accepted finite reference '+key)
    c.require(acceptance['uniqueCases']==308 and acceptance['completeMatchingPasses']==2 and acceptance['rawCaseObservations']==616
              and acceptance['actualFreezeExitCode']==0 and acceptance['actualFreezeNewNativeCompilerJvmProductExecutions']==0,'prior completed native verification, not new qualification')
    c.require(acceptance['firstOriginalParentExit1Preserved'] is True and acceptance['secondOriginalTimeoutPreserved'] is True
              and c.same(acceptance['historicalAttemptNativeCount'],dict(state='UNKNOWN',value=None)),'original historical failures remain unchanged')
    c.require(command['exitCode']==0 and type(command['exitCode']) is int and command['timedOut'] is False,'actual completed freeze command')
    for field,role in [('source','freezeSource'),('executionLock','nativeSourceLock'),('review','freezeApproval')]:
        c.require(c.same(command[field],refs[role]),'actual freeze command provenance '+field)
    c.require(c.same(command['artifacts'],[refs['contract'],refs['bridge']]) and command['newNativeCompilerJvmProductExecutions']==0,'actual freeze outputs and execution boundary')
    c.require(c.same(contract['review'],refs['freezeApproval']) and approval['executionLockSha256']==c.NATIVE_LOCK
              and approval['contractFreezeApproved'] is True,'actual approved freeze provenance')
    c.require(len(contract['proofs'])==8 and c.same(contract['proofs'],ctx.graph['auditReferences']['nativeProofs']),'eight retained discoverable audit receipt references')
    c.require(len(contract['rows'])==308,'frozen contract row inventory')
    witness=next(v for v in contract['rows'] if v['id']=='ORD-HISTORY-BOOL-BOUND-ordering')
    c.require(witness['evaluation']['success'] is True and witness['evaluation']['properties']==dict(P='yes',Q='taken')
              and witness['evaluation']['imports']==[] and witness['diagnostics']==[],'actual baseline witness in completed contract')
    c.require(ctx.raw(refs['bridge'])==b'ORDERING_NATIVE_SUCCESS_BRIDGE_V1\nORD-HISTORY-BOOL-BOUND-ordering\teWVz\tdGFrZW4=\n','exact native-backed bridge')
    return dict(kind='PRIOR_COMPLETED_NATIVE_FREEZE',rowsPerPass=308,matchingPasses=2,transitiveInputsTraversed=False,
                freshNativeQualification=False,firstParentExit1Preserved=True,historicalSecondNative='UNKNOWN')


def baseline_provenance(ctx):
    refs=ctx.graph['references'];qualified=ctx.role('baselineQualification');original=ctx.role('baselineBuild')
    c.require(refs['baselineJar']['sha256']==c.BASE_JAR_SHA and refs['baselineJar']['sizeBytes']==98307
              and c.same(qualified['candidateJar'],refs['baselineJar']) and c.same(original['candidateJar'],refs['baselineJar'])
              and c.same(qualified['oneBuildReceipt'],refs['baselineBuild']),'exact baseline JAR/original build/qualification chain')
    expected={'c6db113559db4d04dc9034388790c71410a3eade4ab9cca41e4c0da0dc7730d1','4aff79a07ae0f450a31172d78d4a519e405a7372ee4a693b867c4b49a24ed321'}
    c.require({d['sha256'] for d in qualified['sourceInputs']}==expected and c.same(original['sourceInputs'],qualified['sourceInputs']),'original baseline evaluator/module bytes')
    for d in qualified['sourceInputs']:c.resolve_historical(d,ctx.graph['additionalArchiveEntries'])
    c.require(original['status']=='FAILED_STOP_NO_RETRY' and qualified['status']=='PASS_PRIVATE_BOOLEAN_PRODUCT_CANDIDATE','retain original later failure separately from successful compilation/later qualification')
    commands=[v for v in original['commands'] if v['label'] in ('compile-product','compile-consumers')]
    c.require(c.same(commands,qualified['oneBuildCommands']) and [v['label'] for v in commands]==['compile-product','compile-consumers'],'recorded original successful compiler provenance')
    product=commands[0]['process'];argv=product['argv']
    c.require(argv[0]==str(c.JDK/'bin/javac.exe') and argv[-2:]==[d['path'] for d in qualified['sourceInputs']]
              and argv[argv.index('--release')+1]=='21' and '-implicit:none' in argv,'exact original compiler/source relationship')
    for command in commands:
        p=command['process'];c.require(type(p['exitCode']) is int and p['exitCode']==0 and p['launched'] is True
              and p['jobAssigned'] is True and p['resumed'] is True and p['timedOut'] is False
              and p['outputLimitExceeded'] is False and p.get('error') is None and p.get('cleanupError') is None,'recorded successful original compile despite later aggregate failure')
    with zipfile.ZipFile(c.BASE_JAR) as jar:
        names=jar.namelist();c.require(len(names)==len(set(names)),'unique JAR entries')
        jdk_jar.verify_module(jar.read('module-info.class'))
        classes=[n for n in names if n.endswith('.class') and n!='module-info.class']
        c.require(classes and all(n.startswith('org/dotj/internal/build/evaluation/ProjectEvaluationComponent') for n in classes)
                  and not any(n.endswith('.java') for n in names),'baseline class-only product origin inventory')
    return dict(jarSha256=c.BASE_JAR_SHA,productClasses=len(classes),originalBuildLaterFailurePreserved=True)


def full_inputs(source,*,review_descriptor=None):
    start=time.monotonic();lock_path=c.HERE/'source-lock.json';c.require(c.sha(lock_path)==source,'reviewed new source lock')
    lock=c.read(lock_path);c.require(lock['schemaVersion']==1 and lock['status']=='BASELINE_PREPARATION_REQUIRES_SEPARATE_OPERATION_APPROVAL','source lock status/version')
    c.require(c.inventory(c.HERE)==sorted([str(lock_path)]+[d['path'] for d in lock['files']]),'exact current J inventory')
    for d in lock['files']:c.pin(d)
    c.pin(lock['externalBootstrapHost']);c.pin(lock['guard'])
    c.validate_policy(c.read(c.HERE/'jdk-controller-policy-v1.json'))
    c.require(c.same(c.read(c.HERE/'operations.json')['operations'],[c.operation(v) for v in ['baseline-compile','baseline-runtime']]),'fixed reviewed argv/env/operations')
    graph=c.read(c.HERE/'stage-inputs.json');ctx=HistoricalContext(graph)
    c.require(graph['counts']['livePayloadFiles']==520,'finite complete live payload')
    for root,count in [(c.PYTHON,34),(c.JDK,486)]:
        ds=[d for d in graph['selectedLiveFiles'] if Path(d['path']).is_relative_to(root)]
        c.require(len(ds)==count,'complete selected runtime payload count');c.verify_inventory(root,ds)
    active=[line.strip() for line in (c.PYTHON/'python313._pth').read_text().splitlines() if line.strip() and not line.strip().startswith('#')]
    c.require(active==['python313.zip','.'],'isolated Python paths/site disabled')
    for d in graph['references'].values():c.pin(d)
    for d in graph['baselineFixtureFiles']:c.pin(d)
    case=graph['baselineFixtureCase'];manifest=ctx.role('fixtureManifest')
    c.require(case['id']=='ORD-HISTORY-BOOL-BOUND-ordering' and case==next(v for v in manifest['cases'] if v['id']==case['id']),'exact manifest witness fixture')
    c.require(c.inventory(c.H/'fixtures'/case['id'])==sorted(d['path'] for d in graph['baselineFixtureFiles']),'exact baseline fixture inventory')
    archives=archive_relations(ctx);native=native_contract(ctx);baseline=baseline_provenance(ctx)
    if review_descriptor:c.pin(review_descriptor)
    return dict(status='COMPLETE_STAGE_INPUT_CLOSURE',sourceLockSha256=source,stageInputsSha256=c.sha(c.HERE/'stage-inputs.json'),
                policySha256=c.sha(c.HERE/'jdk-controller-policy-v1.json'),counts=graph['counts'],archives=archives,native=native,baseline=baseline,
                seconds=time.monotonic()-start,installedSdkVerified=False,
                compiledOutputValidation='NOT_PART_OF_KNOWN_INPUT_FIT_REQUIRES_ACTUAL_PRODUCER')
