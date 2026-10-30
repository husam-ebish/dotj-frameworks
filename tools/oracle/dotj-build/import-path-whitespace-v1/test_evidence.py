"""Python-only whitespace transport/input controls; synthetic rows qualify transport only."""
import base64,copy,json,runpy,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
api=runpy.run_path(str(HERE/'verify.py'))
class WhitespaceEvidenceTest(unittest.TestCase):
    def test_immutable_inputs_and_four_new_case_accounting(self):
        api['verify_plan_inputs']()
        p=api['plan']()
        self.assertEqual(4,len(p['cases']))
        self.assertEqual({'prior':90,'priorDispositionChanges':0,'newProjectCases':4,'fullUniqueComparisons':94,'nativePasses':2},p['accounting'])
    def test_synthetic_classifier_and_unicode_transport_shape(self):
        old=json.loads((api['REPO']/'dotj-build/evaluation-candidate/evidence/import-path-observations-v1.json').read_text(encoding='utf-8'))['captures'][0]
        capture=copy.deepcopy(old);template=copy.deepcopy(old['rows'][0]);capture['rows']=[]
        # Deliberately synthetic shape data, never persisted as observations or native outcomes.
        capture['whiteSpaceCodePoints']=[9,32,160]
        for case in api['plan']()['cases']:
            row=copy.deepcopy(template);oldid=row['id'];row['id']=case['id'];row['globals']=case['globals']
            for edge in row['evaluation']['imports']:
                for key in ['owner','project']:edge[key]=edge[key].replace('\\'+oldid+'\\','\\'+case['id']+'\\')
            row['evaluation']['properties']['Q']='\u00a0one.props\u00a0';capture['rows'].append(row)
        text=api['bridge'](capture)
        self.assertTrue(text.startswith('WHITESPACE\t9,32,160\n'))
        self.assertEqual(4,sum(x.startswith('CASE\t') for x in text.splitlines()))
        for line in text.splitlines():
            if line.startswith('CASE\t'):self.assertEqual('\u00a0one.props\u00a0',base64.b64decode(line.split('\t')[5]).decode('utf-8'))
        for points in [[9,True],[32,9],[9,9],[-1],[65536],[]]:
            bad=copy.deepcopy(capture);bad['whiteSpaceCodePoints']=points
            with self.assertRaises(ValueError):api['bridge'](bad)
    def test_actual_native_binding_mutations(self):
        observations=api['BASE']/'evidence/observations.json'
        if not observations.exists():self.skipTest('Native/JVM work is not authorized yet; actual observations pending')
        api['verify_inputs']();data=json.loads(observations.read_text(encoding='utf-8'))
        raw=json.loads(Path(data['raw']['path']).read_text(encoding='utf-8'))
        self.assertIn(160,raw['captures'][0]['whiteSpaceCodePoints'])
        self.assertNotIn(28,raw['captures'][0]['whiteSpaceCodePoints'])
        mutations=[lambda c:c['whiteSpaceCodePoints'].remove(160),lambda c:c['rows'][0].update(globals={'ImportName':'changed'}),lambda c:c['rows'][0]['evaluation'].pop('code'),lambda c:c['rows'][0]['evaluation'].update(column=99),lambda c:c['rows'][0]['evaluation'].update(properties={'P':'fabricated'}),lambda c:c['rows'][0].update(taskMarkerAbsent=1),lambda c:c['rows'][0]['cleanup'].update(afterUnload=True),lambda c:c['rows'].reverse(),lambda c:c['rows'][1]['evaluation']['imports'][0].update(project='foreign')]
        for mutation in mutations:
            forged=copy.deepcopy(raw)
            for capture in forged['captures']:mutation(capture)
            with self.assertRaises(ValueError):api['validate_raw'](forged)
if __name__=='__main__':unittest.main()
