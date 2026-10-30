"""Import-path input/transport guards catch forged envelopes before Java runs."""
import copy,json,runpy,unittest,subprocess,sys,shutil,uuid,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
api=runpy.run_path(str(HERE/'verify-import-paths-v1.py'))
class ImportPathEvidenceTest(unittest.TestCase):
    def test_copied_native_fixture_bytes_are_still_pinned(self):
        observed=api['BASE']/'evidence/import-path-observations-v1.json'
        if not observed.exists():self.skipTest('Native observations are not captured yet')
        source=Path(json.loads(observed.read_text())['raw']['path']);raw=json.loads(source.read_text())
        private=api['ROOT']/'validation'/('import-paths-fixture-control-v1-'+uuid.uuid4().hex);private.mkdir()
        shutil.copytree(source.parent/'fixtures',private/'fixtures')
        shutil.copyfile(source.parent/'import-path-plan-v1.json',private/'import-path-plan-v1.json')
        (private/'fixtures/NEG-dynamic-import/one.props').write_bytes(b'<Project>changed</Project>')
        for command in raw['commands'][1:]:command['argv'][-2:]=[str(private/'fixtures'),str(private/'import-path-plan-v1.json')]
        with self.assertRaisesRegex(ValueError,'fixture'):api['validate_raw'](raw)
    def test_embedded_rows_must_equal_exact_native_stdout(self):
        observed=api['BASE']/'evidence/import-path-observations-v1.json'
        if not observed.exists():self.skipTest('Native observations are not captured yet')
        source=Path(json.loads(observed.read_text())['raw']['path'])
        raw=json.loads(source.read_text());private=api['ROOT']/'validation'/('import-paths-transport-control-v1-'+uuid.uuid4().hex)
        private.mkdir();shutil.copytree(source.parent/'fixtures',private/'fixtures')
        # Mutate only private copies. The exact original logs remain untouched and hashed.
        raw['captures']=json.loads(json.dumps(raw['captures']).replace(str(source.parent/'fixtures').replace('\\','\\\\'),str(private/'fixtures').replace('\\','\\\\')))
        for capture in raw['captures']:capture['rows'][0]['evaluation']['properties']['P']='forged-but-shape-valid'
        native=private/'verification.json';native.write_bytes((json.dumps(raw,indent=2)+'\n').encode())
        env=os.environ.copy();env.update(TEMP=str(private),TMP=str(private),PYTHONPYCACHEPREFIX=str(private/'cache'))
        command=[sys.executable,'-B',str(HERE/'verify-import-paths-v1.py'),str(native),'--out',str(private/'bridge')]
        result=subprocess.run(command,capture_output=True,env=env,timeout=30)
        (private/'stdout').write_bytes(result.stdout);(private/'stderr').write_bytes(result.stderr)
        (private/'result.json').write_text(json.dumps({'argv':command,'exitCode':result.returncode,'mutation':'Both embedded native passes changed; original stdout logs unchanged','expected':'Nonzero refusal'},indent=2)+'\n')
        self.assertNotEqual(0,result.returncode,'Forged duplicated rows passed while exact native stdout stayed unchanged: '+str(private))
    def test_immutable_inputs_and_legacy_bytes(self):
        api['verify_plan_inputs']()
        rows=api['plan']()['fixtures']
        self.assertEqual([(90,'752761ce6eedf56cb4042798dd8175f46f88a67f2dac8d26786b304af57c2e3e'),(10,'4fd24be83f7dd636f6e2e8f456dfa559f1ca9c7346e1d10a5358db346b1300b9')],[(r['bytes'],r['sha256']) for r in rows if r['path'].startswith('NEG-')])
    def test_native_transport_mutations(self):
        path=api['BASE']/'evidence/import-path-observations-v1.json'
        if not path.exists():self.skipTest('Native observations are not captured yet')
        capture=json.loads(path.read_text())['captures'][0]
        raw=json.loads(Path(json.loads(path.read_text())['raw']['path']).read_text())
        original=api['bridge'](capture)
        self.assertEqual(8,sum(x.startswith('CASE\t') for x in original.splitlines()))
        mutations=[lambda c:c['rows'][0].update(globals={'P':'injected'}),lambda c:c['rows'][0]['cleanup'].update(afterUnload=True),lambda c:c['rows'][0].update(taskMarkerAbsent=1),lambda c:c['rows'][0]['evaluation']['imports'][0].update(owner='foreign'),lambda c:c['rows'][-1]['evaluation'].pop('code'),lambda c:c['rows'][-1]['evaluation'].update(properties={'P':'fabricated'}),lambda c:c['rows'][-1]['evaluation'].update(endColumn='0'),lambda c:c['rows'].reverse()]
        for mutation in mutations:
            bad=copy.deepcopy(capture);mutation(bad)
            with self.assertRaises((ValueError,KeyError,TypeError)):api['bridge'](bad)
            forged=copy.deepcopy(raw)
            for c in forged['captures']:mutation(c)
            with self.assertRaises(ValueError):api['validate_raw'](forged)
        for mutation in [lambda c:c['rows'][0]['evaluation']['imports'][0].update(column=99),lambda c:c['rows'][0]['evaluation'].update(properties={'P':'forged','Q':''}),lambda c:c['rows'][-1]['evaluation'].update(column=99)]:
            bad=copy.deepcopy(capture);mutation(bad)
            self.assertNotEqual(original,api['bridge'](bad),'Native identity/coordinate must survive transport')
            forged=copy.deepcopy(raw)
            for c in forged['captures']:mutation(c)
            with self.assertRaises(ValueError):api['validate_raw'](forged)
        for field in ['file','message']:
            bad=copy.deepcopy(capture);ev=next(r['evaluation'] for r in bad['rows'] if not r['evaluation']['success']);ev[field]+='foreign'
            if field=='message':self.assertNotEqual(capture,bad,'Raw messages stay evidence')
            else:
                self.assertNotEqual(original,api['bridge'](bad),'Changed local filename must alter the comparison bridge')
if __name__=='__main__':unittest.main()
