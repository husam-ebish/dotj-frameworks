"""Round1 successor: retain the base gate and add the separately counted raw-glob regression."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import read_proof as base
from read_proof import *

def sort_result(value,jar_sha):
    require(value['id']=='T129-IMPORTANT-01' and value['status']=='PASS','Raw-sort disposition')
    require(value['pair']==['a0.cs','a@.cs'],'Raw-sort pair order')
    expected=['a@.cs','a%40.cs','a0.cs','a@.cs','a%40.cs','a0.cs','a@.cs']
    require(value['fragmentsAndDuplicates']==expected and value['vectorOrder']==expected,'Raw-sort fragment/vector order')
    require(value['identityEscaping'] and value['retainedSnapshot'] and value['jarSha256']==jar_sha,'Raw-sort identity/provenance')

def check(proof_path,proof_sha,jar,source_root):
    result=base.check(proof_path,proof_sha,jar,source_root)
    proof=json.loads(Path(proof_path).read_text())
    require(set(proof['rawSortRegression'])=={'windows','linux'},'Both raw-sort platforms required')
    for value in proof['rawSortRegression'].values():
        sort_result(json.loads(Path(value['path']).read_text()),proof['jar']['sha256'])
    require(Path(proof['rawSortLinuxCaseProfile']['path']).read_text()=='fileAlias\tfalse\n','Raw-sort Linux case capability')
    result['separateRawSortRegressions']=2
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--proof',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--jar',required=True);parser.add_argument('--source-root',required=True)
    args=parser.parse_args();print(json.dumps(check(args.proof,args.sha256,args.jar,args.source_root)))
if __name__=='__main__':main()
