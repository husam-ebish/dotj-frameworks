"""Task130 successor: preserve all prior gates and validate each boundary family on both OSes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import read_proof_fix1 as previous
from read_proof_fix1 import *

def boundary_result(rows,jar_sha,platform):
    require(len(rows)==3 and [r['id'] for r in rows]==['T130-IMPORTANT-01','T130-IMPORTANT-02','T130-IMPORTANT-03'],'Boundary family inventory')
    require(all(r['status']=='PASS' and r['jarSha256']==jar_sha and r['platform']==platform for r in rows),'Boundary provenance')
    prefix,selectors,extension=rows
    sep='\\' if platform=='windows' else '/'
    expected=['a@'+sep+'x.cs','a%40'+sep+'x.cs','a@'+sep+'x.cs']
    require(prefix['identities']==prefix['copy']==expected and prefix['metadata']==['at','percent','at']
        and prefix['exclude']==[expected[1]] and prefix['remove']==[expected[0],expected[2]] and prefix['inlineIdentity'],'Escaped-prefix boundary')
    require(selectors['identities']==['./a.cs','a.cs','d/../a.cs','missing/../a.cs','other.cs','p%40.cs','p@.cs']
        and selectors['metadata']==['updated','updated','updated','updated','','percent','at']
        and selectors['excludeCount']==0 and selectors['remove']==['other.cs']
        and all(selectors[k] for k in ('absolute','mixedSeparators','nonexistentPaths','copyUnchanged','invalidFallback','trailingSeparator')),'Normalized-selector boundary')
    require(extension['identities']==['name.','plain','file.cs','.hidden','multi.part.']
        and extension['direct']==extension['inline']==['','','.cs','.hidden','']
        and extension['definingProject'] and extension['nonexistentLiteral'],'Trailing-dot boundary')

def check(proof_path,proof_sha,jar,source_root):
    result=previous.check(proof_path,proof_sha,jar,source_root)
    proof=json.loads(Path(proof_path).read_text())
    require(set(proof['finalWaveRegression'])=={'windows','linux'},'Both boundary platforms required')
    for platform,value in proof['finalWaveRegression'].items():
        boundary_result([json.loads(line) for line in Path(value['path']).read_text().splitlines()],proof['jar']['sha256'],platform)
    require(Path(proof['finalWaveLinuxCaseProfile']['path']).read_text()=='directoryAlias\tfalse\n','Boundary Linux case capability')
    result['separateFinalWaveFamiliesPerPlatform']=3
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--proof',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--jar',required=True);parser.add_argument('--source-root',required=True)
    args=parser.parse_args();print(json.dumps(check(args.proof,args.sha256,args.jar,args.source_root)))
if __name__=='__main__':main()
