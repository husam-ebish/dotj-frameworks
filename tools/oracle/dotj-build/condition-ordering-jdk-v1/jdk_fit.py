"""One externally bounded PURE two-full-known-input-closure timing.
No staged/compiled output is created or asserted successful by this fit.
"""
import argparse
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import jdk_contract as c
import jdk_stage as stage


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--source-lock-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    c.require(args.output==c.TEST_ROOT/'input-fit-fix1','one exact authorized fresh fit output')
    c.require(not (args.output/'timing.json').exists(),'one fit, no retry or overwrite')
    c.require(not c.COMPILE.exists() and not c.RUNTIME.exists(),'fit has no compiler output or runtime attempt')
    started=time.monotonic();pre=stage.full_inputs(args.source_lock_sha256);mid=time.monotonic()
    c.fresh_json(args.output/'pre.json',pre)
    post=stage.full_inputs(args.source_lock_sha256);end=time.monotonic()
    c.fresh_json(args.output/'post.json',post)
    pre_seconds=mid-started;post_seconds=end-mid;full=end-started
    c.validate_fit_times(pre_seconds,post_seconds,full)
    c.require(pre['stageInputsSha256']==post['stageInputsSha256'],'same concrete complete input set')
    result=dict(schemaVersion=1,status='TWO_COMPLETE_STAGE_INPUT_CHECKS_FIT',sourceLockSha256=args.source_lock_sha256,
                policySha256=c.sha(c.HERE/'jdk-controller-policy-v1.json'),stageInputsSha256=pre['stageInputsSha256'],
                completeChecks=2,preSeconds=pre_seconds,postSeconds=post_seconds,fullMeasuredSeconds=full,
                formulaSeconds=full+120+120+5+60,pre=c.descriptor(args.output/'pre.json'),post=c.descriptor(args.output/'post.json'),
                interpretation='KNOWN_STAGE_INPUT_CLOSURE_ONLY_NOT_COMPILE_OUTPUT_OR_OWNED_JDK_SUCCESS',
                compiledOutputPresent=False,compiledOutputValidated=False,newCompilerExecutions=0,newJvmExecutions=0,newNativeExecutions=0)
    c.fresh_json(args.output/'timing.json',result)
    print(c.canonical(result).decode())


if __name__=='__main__':main()
