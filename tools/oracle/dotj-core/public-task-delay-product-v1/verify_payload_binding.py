"""Focused changed-contract forgery controls; no prior mock or runtime replay."""
import sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import product_support as p
import verify_product as v

if __name__=='__main__':
    e=p.c.read(p.E/'public-task-delay-v1.json');paired=p.c.read(e['paired']['path']);group=paired['groups'][0]
    passed=[]
    other=e['contract']
    for name,mutation in [('runtime-stdout-redirection',lambda x:x['payloads'].__setitem__(0,other)),('missing-compiled-fixture-class',lambda x:x['classes'].pop())]:
        forged=copy.deepcopy(group);mutation(forged)
        try:v.actual_group(forged,paired['commands'],e['candidateJar']['path'])
        except ValueError:passed.append(name)
        else:raise AssertionError('accepted group forgery '+name)
    legacy=p.c.read(e['historicalTail']['path']);group=next(x for x in legacy['groups'] if x['name']=='delegate-action-v1');forged=copy.deepcopy(group);forged['payloads']=[other]
    try:v.actual_group(forged,legacy['commands'],e['candidateJar']['path'])
    except ValueError:passed.append('legacy-output-argument-redirection')
    else:raise AssertionError('accepted legacy output redirection')
    p.write(p.A/'payload-class-binding-controls-v1.json',dict(status='PASS_FOCUSED_PAYLOAD_AND_CLASS_BINDING',actualControls=len(passed),passed=passed,workloadChildren=0,
        original17Controls=p.c.descriptor(p.A/'changed-consumed-contract-controls-v1.json'),canonical3Controls=p.c.descriptor(p.A/'archive-resolution-controls-v1/receipt.json'),unchangedControlsRerun=False))
    print('PASS focused payload/class binding',len(passed))
