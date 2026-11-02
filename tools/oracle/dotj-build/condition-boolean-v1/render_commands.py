"""Pure rendering of closed typed root command descriptors; never executes."""
import argparse, importlib.util, json, re
from pathlib import Path
s=importlib.util.spec_from_file_location('boolean_v1_protocol',Path(__file__).with_name('protocol.py'));p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def render(lock_sha,review_sha):
    for digest in [lock_sha,review_sha]:p.require(type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest) is not None,'64 lowercase hex digest required')
    p.verify_lock(lock_sha);proposal=p.read(p.HERE/'proposed-commands.json')
    for command in proposal['commands']:
        command['outerArgv']=[a.replace('{nativeLockSha256}',lock_sha).replace('{rootReviewSha256}',review_sha) for a in command['outerArgv']]
    return proposal
def main():
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument('--lock-sha256',required=True);parser.add_argument('--review-sha256',required=True);a=parser.parse_args()
    print(json.dumps(render(a.lock_sha256,a.review_sha256),indent=2))
if __name__=='__main__':main()
