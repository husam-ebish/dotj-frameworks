"""Focused deterministic controls for the final launch boundary; no child launch."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import qualify as q

def main():
    good={'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3}
    results=[]
    for name,times,sample,deadline,allowed in [
        ('fresh',[10.0,10.25],good,200,True),
        ('stale',[10.0,12.01],good,200,False),
        ('physical-refused',[10.0,10.25],dict(good,freePhysicalBytes=512*1024**2-1),200,False),
        ('commit-refused',[10.0,10.25],dict(good,freeVirtualBytes=16*1024**3-1),200,False),
        ('deadline-exhausted',[10.0,10.25],good,135.25,False),
        ('finalization-reserve',[10.0,10.25],good,136.25,False),
        ('backward-clock',[10.0,9.99],good,200,False)]:
        values=iter(times);actual=True
        try:q.final_admission(deadline,120,lambda:next(values),lambda:sample)
        except ValueError:actual=False
        q.c.require(actual==allowed,'launch admission '+name);results.append(dict(control=name,passed=True,allowed=actual))
    print(json.dumps(dict(status='PASS',actualChildLaunches=0,controls=results)))

if __name__=='__main__':main()
