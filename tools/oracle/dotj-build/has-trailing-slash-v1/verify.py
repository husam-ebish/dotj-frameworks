"""Strict native pair comparison; fixture roots are the sole normalization."""
import argparse, copy
from pathlib import Path
import capture as c
def normalize(payload,root):
    result=copy.deepcopy(payload)
    def replace(value):return value.replace(root,'<OWNED_FIXTURE_ROOT>') if type(value) is str else value
    for row in result['rows']:
        ev=row['evaluation']
        if ev['success']:
            for field in ['imports','duplicateImports']:
                if ev[field] is not None:
                    for edge in ev[field]:
                        for key in ['owner','project']:edge[key]=replace(edge[key])
            if ev['duplicateGetterFailure'] is not None:ev['duplicateGetterFailure']['message']=replace(ev['duplicateGetterFailure']['message'])
        else:
            for key in ['file','message']:ev[key]=replace(ev[key])
        for event in row['diagnostics']:
            for key in ['file','message']:event[key]=replace(event[key])
    return result
def receipt(path,digest):
    c.require(c.sha(path)==digest,'receipt pin mismatch');r=c.read(path)
    c.require(r['status']=='CAPTURED_PENDING_ROOT_REVIEW' and len(r['commands'])==1,'capture receipt status/count')
    c.successful(r['commands'][0]);obs=r['observation'];c.require(c.sha(obs['path'])==obs['sha256'],'raw observation changed')
    payload=c.parse_observation(obs['path']);c.require(payload==r['payload'],'receipt/raw mismatch');c.metadata(payload)
    actual=c.verify_fixture_copy(Path(r['fixtureRoot']));c.require(actual==r['fixtureInputs'],'fixture receipt changed')
    for item in r['retainedRaw']:c.require(c.descriptor(item['path'])==item,'retained raw evidence changed')
    controller=c.read(Path(path).parent/'controller-receipt.json');c.successful(controller['process'])
    c.require(controller['inputLockSha256']==r['inputLockSha256'] and controller['checkpointSha256']==r['checkpointSha256'],'controller/native identity mismatch')
    c.require(c.read(Path(path).parent/'native-process.json')==r['commands'][0],'native process receipt mismatch')
    return r
def compare(a,ash,b,bsh):
    left=receipt(a,ash);right=receipt(b,bsh)
    c.require(left['inputLockSha256']==right['inputLockSha256'] and left['checkpointSha256']==right['checkpointSha256'],'different capture identities')
    c.require(left['fixtureRoot']!=right['fixtureRoot'],'fresh fixture roots required')
    c.require(left['commands'][0]['processId']!=right['commands'][0]['processId'],'two distinct native process IDs required')
    c.require(normalize(left['payload'],left['fixtureRoot'])==normalize(right['payload'],right['fixtureRoot']),'full typed native payload pair differs')
    # stderr retained byte-for-byte; root prefix only, no whitespace/line/event suppression.
    ls=c.bounded(left['stderr']['path'],512*1024);rs=c.bounded(right['stderr']['path'],512*1024)
    c.require(c.sha(left['stderr']['path'])==left['stderr']['sha256'] and c.sha(right['stderr']['path'])==right['stderr']['sha256'],'stderr pin mismatch')
    c.require(ls.replace(left['fixtureRoot'].encode(),b'<OWNED_FIXTURE_ROOT>')==rs.replace(right['fixtureRoot'].encode(),b'<OWNED_FIXTURE_ROOT>'),'stderr pair differs')
    return {'status':'PAIR_EQUAL_PENDING_ROOT_REVIEW','uniqueCases':38,'semanticCases':32,'boundaryCases':6,'freshProcesses':2,'acceptedTasksAdded':0,'leftReceipt':c.descriptor(a),'rightReceipt':c.descriptor(b),'leftController':c.descriptor(Path(a).parent/'controller-receipt.json'),'rightController':c.descriptor(Path(b).parent/'controller-receipt.json'),'inputLockSha256':left['inputLockSha256']}
def main():
    p=argparse.ArgumentParser()
    for name in ['left','right','out']:p.add_argument('--'+name,type=Path,required=True)
    for name in ['left-sha256','right-sha256']:p.add_argument('--'+name,required=True)
    a=p.parse_args();out=c.confined(a.out);c.require(not out.exists(),'fresh pair receipt required');c.write(out,compare(a.left,a.left_sha256,a.right,a.right_sha256))
if __name__=='__main__':main()
