"""Pure Python CLI boundary tests; no SDK, JDK, native or owned process launch."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parent))
import operations as op

VERIFY = ['--lock=L', '--lock-sha256=LH', '--checkpoint=C', '--checkpoint-sha256=CH', '--receipt=R', '--receipt-sha256=RH']
BOUNDARIES = ['--out=O', '--candidate-jar=J', '--candidate-sha256=JH', '--java-lock=K', '--java-lock-sha256=KH', '--execute-reviewed']


class CliTests(unittest.TestCase):
    def rejects(self, function, args):
        loader = Mock(side_effect=AssertionError('malformed input reached library'))
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                function(args, loader=loader)
        self.assertEqual(result.exception.code, 2)
        loader.assert_not_called()

    def test_all_selectors_modes_and_placement(self):
        for function, valid in [(op.verify, VERIFY), (op.boundaries, BOUNDARIES), (op.child_main, BOUNDARIES)]:
            for mode in ['static', 'capture', 'compare', 'baseline-red', 'boundaries', 'verify']:
                for flag in ['--mode', '--mod', '--mo', '--m']:
                    for selector in [[flag, mode], [flag + '=' + mode]]:
                        for position in [0, 2, len(valid)]:
                            with self.subTest(function=function.__name__, mode=mode, flag=selector, position=position):
                                args = valid[:position] + selector + valid[position:]
                                self.rejects(function, args)

    def test_conflicts_delimiter_unknown_and_inner(self):
        attacks = [['--mode=verify', '--mode=capture'], ['--mode', 'boundaries', '--mo=static'],
                   ['--', '--mode=capture'], ['--'], ['--inner'], ['--inner=true'],
                   ['--execute-reviewed=false'], ['--only=valuetask-task'], ['capture'], ['--', 'capture'], ['--unknown'], ['--outlandish=1'], ['--exe']]
        for function, valid in [(op.verify, VERIFY), (op.boundaries, BOUNDARIES), (op.child_main, BOUNDARIES)]:
            for attack in attacks:
                for args in [attack + valid, valid + attack]:
                    with self.subTest(function=function.__name__, attack=attack, args=args):
                        self.rejects(function, args)
        self.rejects(op.verify, VERIFY + ['--execute-reviewed'])
        self.rejects(op.verify, VERIFY + ['--out=unused'])
        self.rejects(op.boundaries, BOUNDARIES[:-1])

    def test_positive_verify_is_receipt_dispatch_only(self):
        library = SimpleNamespace(verify_receipt=Mock(return_value={'status': 'VERIFIED_ONLY_NO_LAUNCH'}),
                                  main=Mock(side_effect=AssertionError('CLI')), execute=Mock(side_effect=AssertionError('execute')),
                                  controller=Mock(side_effect=AssertionError('controller')))
        result = op.verify(VERIFY, loader=lambda: library)
        self.assertEqual(result['status'], 'VERIFIED_ONLY_NO_LAUNCH')
        a = library.verify_receipt.call_args.args[0]
        self.assertEqual(a.mode, 'verify')
        self.assertEqual(a.receipt, Path('R'))
        for name in ['main', 'execute', 'controller']:
            getattr(library, name).assert_not_called()

    def test_missing_receipt_and_hash_failure_propagate(self):
        # Use the actual frozen receipt function: both failures occur before native
        # validation, so these controls do not rescan the SDK or execute anything.
        library = op.frozen_library()
        with tempfile.TemporaryDirectory(dir=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2515-whole-branch-fix1-v1')) as tmp:
            receipt = Path(tmp) / 'receipt.json'
            argv = VERIFY[:-2] + ['--receipt=' + str(receipt), '--receipt-sha256=' + '0' * 64]
            for expected in [FileNotFoundError, ValueError]:
                with self.assertRaises(expected):
                    op.verify(argv, loader=lambda: library)
                receipt.write_text('{}', encoding='utf-8')

    def test_selector_like_values_survive_without_dispatch(self):
        values = {'out': Path('D:/a space/--mode=capture'), 'candidate_jar': Path('D:/x/--inner.jar'),
                  'java_lock': Path('D:/x/--mo=static.json'), 'candidate_sha256': '--mode=static',
                  'java_lock_sha256': '--inner', 'execute_reviewed': True, 'mode': 'boundaries'}
        a = SimpleNamespace(**values)
        argv = op.boundary_child_argv(a, Path('D:/Python/python.exe'))
        self.assertEqual(argv[:3], ['D:\\Python\\python.exe', '-B', '-c'])
        self.assertIn('operations.child_main()', argv[3])
        parsed = op.parse_boundaries(argv[4:])
        self.assertEqual(vars(parsed), values)
        library = SimpleNamespace(verify_receipt=Mock(return_value={'status': 'sentinel'}))
        op.verify(VERIFY[:-2] + ['--receipt=--mode=capture', '--receipt-sha256=--mo=static'], loader=lambda: library)
        a = library.verify_receipt.call_args.args[0]
        self.assertEqual(a.receipt, Path('--mode=capture'))
        self.assertEqual(a.receipt_sha256, '--mo=static')
        self.assertEqual(a.mode, 'verify')

    def fake_backend(self, out):
        qualified = op.PRODUCT / 'ValueTaskTaskBoundaryControls.java'
        pins = [{'path': str(qualified), 'sha256': 'FIXTURE'}]
        lock = {'candidateJar': {'path': 'J', 'sha256': 'JH'}, 'pins': pins}
        records = {Path('K'): lock, out / 'receipt.json': {'status': 'PASS_STAGED_GROUPS', 'groups': [{'name': 'valuetask-boundaries'}]}}
        def require(ok, message):
            if not ok:
                raise ValueError(message)
        c = SimpleNamespace(require=require, sha=lambda p: 'KH' if p == Path('K') else 'FIXTURE' if p == qualified else 'JH',
                            read=lambda p: records[p], pin=Mock(), descriptor=lambda p: {'path': 'J', 'sha256': 'JH'} if p == Path('J') else {'path': str(p)},
                            confined=lambda p: p, write=lambda p, v: records.__setitem__(p, v), successful=Mock(), PYTHON=Path('D:/Python/python.exe'))
        backend = SimpleNamespace(c=c, prepare=Mock(), inputs=Mock(return_value=pins), launch=Mock(return_value={'exitCode': 0}),
                                  inner=Mock(return_value={'status': 'PASS_STAGED_GROUPS'}))
        return backend, records

    def test_parent_and_child_only_qualified_boundaries(self):
        with tempfile.TemporaryDirectory(dir=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2515-whole-branch-fix1-v1')) as tmp:
            out = Path(tmp)
            backend, records = self.fake_backend(out)
            args = ['--out=' + str(out), *BOUNDARIES[1:]]
            result = op.boundaries(args, loader=lambda: backend)
            self.assertEqual(result['status'], 'PASS_STAGED_GROUPS')
            backend.inner.assert_not_called()
            call = backend.launch.call_args
            self.assertEqual(call.args[1:4], (out, 'controller', 600))
            parsed = op.parse_boundaries(call.args[0][4:])
            self.assertEqual(parsed.mode, 'boundaries')
            (out / 'controller.json').write_text('{}', encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                op.child_main(call.args[0][4:], loader=lambda: backend)
            request = backend.inner.call_args.args[0]
            self.assertEqual(vars(request), {'mode': 'groups', 'only': 'valuetask-boundaries', 'out': out,
                                             'jar': Path('J'), 'jar_sha256': 'JH'})
            self.assertEqual(backend.launch.call_count, 1)
            self.assertEqual(records[out / 'inputs.json'], backend.inputs.return_value)

    def test_bad_lock_and_missing_qualified_fixture_stop_before_launch(self):
        for mutation in ['hash', 'fixture']:
            backend, records = self.fake_backend(Path('O'))
            if mutation == 'hash':
                records[Path('K')]['candidateJar']['sha256'] = 'wrong'
            else:
                records[Path('K')]['pins'] = []
            with self.assertRaises(ValueError):
                op.boundaries(BOUNDARIES, loader=lambda: backend)
            backend.prepare.assert_not_called()
            backend.launch.assert_not_called()
            backend.inner.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)