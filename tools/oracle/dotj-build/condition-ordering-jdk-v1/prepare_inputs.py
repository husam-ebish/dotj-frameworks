"""Finite Task104 input preparation under root ruling cd4a2677. No recursive discovery."""
import hashlib
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import jdk_contract as c

ARCHIVE=c.A/'task104-finite-original-input-archive-v1'
RULING=c.B/'orchestration/two-frameworks/task104-finite-jdk-input-boundary-ruling-v1.json'


def git(repo,args):
    return subprocess.run(['git','-c','core.longpaths=true','-C',str(repo)]+args,capture_output=True,check=True,timeout=30).stdout


def preserve(path,entries):
    path=Path(path);d=c.descriptor(path);raw=path.read_bytes()
    c.require(hashlib.sha256(raw).hexdigest()==d['sha256'],'stable source archive bytes')
    target=ARCHIVE/'raw'/d['sha256']/path.name;target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():c.require(target.read_bytes()==raw,'retained exact archive')
    else:target.write_bytes(raw)
    repo=next((parent for parent in path.parents if (parent/'.git').exists()),None)
    blob=None;gd=None;relation='UNTRACKED_OR_EXTERNAL_NO_GIT_BLOB';head=None
    if repo:
        head=git(repo,['rev-parse','HEAD']).decode().strip();relative=path.relative_to(repo).as_posix()
        tree=git(repo,['ls-tree','-z',head,'--',relative]).split(b'\0');records=[r for r in tree if r]
        if records:
            c.require(len(records)==1,'one named source Git object')
            metadata,name=records[0].split(b'\t',1);mode,kind,oid=metadata.split(b' ')
            c.require(kind==b'blob' and name.decode()==relative,'exact source Git path/type')
            blob=oid.decode();content=git(repo,['cat-file','blob',blob])
            c.require(hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()==blob,'Git object identity')
            gp=ARCHIVE/'git'/blob/path.name;gp.parent.mkdir(parents=True,exist_ok=True)
            if gp.exists():c.require(gp.read_bytes()==content,'retained exact Git bytes')
            else:gp.write_bytes(content)
            gd=c.descriptor(gp)
            if raw==content:relation='EXACT_RAW_EQUALS_GIT'
            elif raw.replace(b'\r\n',b'\n')==content and b'\r\n' in raw:relation='RAW_CRLF_GIT_LF'
            elif content.replace(b'\r\n',b'\n')==raw and b'\r\n' in content:relation='RAW_LF_GIT_CRLF'
            else:relation='EXPLICIT_RAW_DIFFERS_FROM_GIT'
        c.require(git(repo,['rev-parse','HEAD']).decode().strip()==head,'named source repository HEAD unchanged')
    entry=dict(original=d,archived=c.descriptor(target),relation='EXACT_RAW',gitBlob=gd,gitObjectId=blob,gitRelation=relation,repositoryHead=head)
    entries.append(entry);return entry


def main():
    c.require(c.sha(RULING)=='cd4a2677986a81e99dd2473a26af3d8b83dadc8970a26ebcd2568f47616d8643','superseding finite boundary authority')
    c.require(c.sha(c.H/'execution-lock.json')==c.NATIVE_LOCK,'native source lock remains immutable')
    payload=c.read(c.H/'payload-lock.json');live=[]
    for root,count in [(c.PYTHON,34),(c.JDK,486)]:
        selected=[d for d in payload['files'] if Path(d['path']).is_relative_to(root)]
        c.require(len(selected)==count and c.inventory(root)==sorted(d['path'] for d in selected),'complete selected live membership')
        live+=selected
    entries=[]
    for base in [Path('C:/source/repos/dotj Frameworks'),c.W]:
        for relative in ['src/module-info.java','src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java','CONTRACT.md']:
            preserve(base/'dotj-build/evaluation-candidate'/relative,entries)
    old_root=c.B/'worktrees/dotj-build-boolean-conditions-v1/dotj-build/evaluation-candidate/src'
    for path in [old_root/'module-info.java',old_root/'org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java',c.FIXTURE]:preserve(path,entries)
    references={}
    def reference(role,path,expected=None):
        d=c.descriptor(path)
        if expected:c.require(d['sha256']==expected,'finite evidence pin '+role)
        references[role]=d;return d
    reference('boundaryRuling',RULING,'cd4a2677986a81e99dd2473a26af3d8b83dadc8970a26ebcd2568f47616d8643')
    reference('contract',c.A/'frozen-native-contract-v3/contract.json',c.CONTRACT_SHA)
    reference('bridge',c.BRIDGE,c.BRIDGE_SHA)
    reference('acceptance',c.B/'orchestration/two-frameworks/batch2518-root-native-contract-freeze-acceptance-v3.json','4efff84aa423ed6a962dfcf78382c07f86c7379989af977fffcd4e35bcba4b43')
    reference('freezeCommand',c.A/'root-native-contract-freeze-v3/command-result.json','0273ea0bff65feaaaae75accec060d21374f0a66b766a4f0fab136e1aa432964')
    reference('freezeApproval',c.B/'orchestration/two-frameworks/batch2518-ordering-contract-freeze-review-v3.json','7bf3a1b61476af793f4bd619c2cc10b742404930fa47ed47b6b14f58922d8edd')
    reference('freezeSource',c.H/'freeze_contract_v3.py','fbd88079cbed5ca39b81007a3d58b8e0242ffaf59f80daea6d2905313a9afc9f')
    reference('nativeSourceLock',c.H/'execution-lock.json',c.NATIVE_LOCK)
    reference('baselineJar',c.BASE_JAR,c.BASE_JAR_SHA)
    reference('baselineFixture',c.FIXTURE,'4aeea9d53cd66da0082becec13cf953abc6e2dfd35e6a2670b50c0c9f22724eb')
    reference('baselineBuild',c.B/'validation/Batch-2516-boolean-product-green-v3/receipt.json','434498438972fc75d238fb0e226f6af6776137abcd68fdbe19f27b6ee070d757')
    reference('baselineQualification',c.B/'validation/Batch-2516-boolean-product-green-v5/receipt.json','dc29b067a67a31a87fa3b81fc40d5c6c49e0c63c375af6f9427520fe81dd0eb8')
    reference('fixtureManifest',c.H/'manifest.json')
    manifest=c.read(references['fixtureManifest']['path'])
    case=next(v for v in manifest['cases'] if v['id']=='ORD-HISTORY-BOOL-BOUND-ordering')
    files=[dict(path=str(c.H/'fixtures'/f['relativePath']),sha256=f['sha256'],sizeBytes=f['sizeBytes']) for f in case['files']]
    for d in files:c.pin(d)
    old_archive=c.descriptor(c.B/'validation/Batch-2516-historical-input-archive-v1/archive-lock.json')
    c.require(old_archive['sha256']=='02b5dd9a08e8db4b4251f212ba32b1c2d0f9e0de5357e0192c82599c43d9a1c0','old14 retained exact archive identity')
    contract=c.read(references['contract']['path'])
    graph=dict(schemaVersion=2,boundary='FINITE_JDK_INPUTS_PRIOR_COMPLETED_NATIVE_EVIDENCE',
               selectedLiveFiles=live,selectedLiveRoots=[str(c.PYTHON),str(c.JDK)],references=references,
               baselineFixtureCase=case,baselineFixtureFiles=files,additionalArchiveEntries=entries,
               auditReferences=dict(kind='DISCOVERABLE_ONLY_NOT_LIVE_TRANSITIVE_INPUTS',nativeProofs=contract['proofs'],
                   old14Archive=old_archive,firstOriginalParentExit1Preserved=True,historicalSecondNative='UNKNOWN',
                   old35='35ef28faf73f6dd31596867f724c37ec5050163ad47ac18775ab362f6901897e',
                   b169='b169ee19d9ab31d67f04d04cc4fc2dcdd48343488374dbe29b794e2fd2e4caa7'),
               excluded=['recursive historical plan/report descriptor traversal','requalification of prior native Windows/.NET evidence','unrelated installed SDK payload'],
               counts=dict(livePayloadFiles=len(live),finiteReferenceFiles=len(references),archivedOriginals=len(entries),fixtureFiles=len(files)))
    c.fresh_json(c.HERE/'stage-inputs.json',graph)
    c.fresh_json(c.HERE/'jdk-controller-policy-v1.json',c.POLICY)
    c.fresh_json(c.HERE/'operations.json',dict(schemaVersion=1,operations=[c.operation(x) for x in ('baseline-compile','baseline-runtime')]))
    c.fresh_json(c.HERE/'python-bootstrap-inputs.json',dict(schemaVersion=1,root=str(c.PYTHON),files=[d for d in live if Path(d['path']).is_relative_to(c.PYTHON)],activePth=['python313.zip','.'],siteEnabled=False))
    print(c.canonical(graph['counts']).decode())


if __name__=='__main__':main()
