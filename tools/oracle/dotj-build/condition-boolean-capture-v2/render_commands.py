"""Closed typed descriptor rendering only. Never executes or substitutes paths."""
import argparse
import importlib.util
import json
from pathlib import Path
s = importlib.util.spec_from_file_location('recovery_protocol', Path(__file__).with_name('protocol.py'))
p = importlib.util.module_from_spec(s)
s.loader.exec_module(p)

def fill(proposal, original_sha, execution_sha, review_sha):
    """Pure fixed-slot renderer; caller supplies only pinned proposal and digests."""
    for value in [original_sha, execution_sha, review_sha]:
        p.digest(value)
    p.require(original_sha == p.ORIGINAL_LOCK_SHA, 'fixed original lock')
    p.require(proposal['executionLock'] == {'path': str(p.HERE / 'execution-lock.json'),
                                          'sha256': '{executionLockSha256}'}, 'typed execution lock slot')
    replacements = {'--original-lock-sha256={originalNativeLockSha256}': '--original-lock-sha256=' + original_sha,
                    '--execution-lock-sha256={executionLockSha256}': '--execution-lock-sha256=' + execution_sha,
                    '--review-sha256={rootReviewSha256}': '--review-sha256=' + review_sha}
    for command in proposal['commands']:
        p.require(all(command['outerArgv'].count(token) == 1 for token in replacements), 'three exact digest slots')
        command['outerArgv'] = [replacements.get(token, token) for token in command['outerArgv']]
        p.require(not any('{' in token or '}' in token for token in command['outerArgv']), 'unknown placeholder')
    proposal['executionLock']['sha256'] = execution_sha
    return proposal

def render(original_sha, execution_sha, review_sha):
    for value in [original_sha, execution_sha, review_sha]:
        p.digest(value)
    p.require(original_sha == p.ORIGINAL_LOCK_SHA, 'fixed original lock')
    p.verify_execution(execution_sha)
    p.review_authorization(p.REVIEW, review_sha, execution_sha)
    return fill(p.read(p.HERE / 'proposed-commands.json'), original_sha, execution_sha, review_sha)

def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--original-lock-sha256', required=True)
    parser.add_argument('--execution-lock-sha256', required=True)
    parser.add_argument('--review-sha256', required=True)
    a = parser.parse_args()
    print(json.dumps(render(a.original_lock_sha256, a.execution_lock_sha256, a.review_sha256), indent=2))

if __name__ == '__main__':
    main()
