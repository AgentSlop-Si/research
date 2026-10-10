"""Negative controls for newly authored checker only. No inherited code imported."""
import copy, hashlib, json, subprocess, sys, tempfile, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'CONSEQUENCE_CERTIFICATE.json').read_text())

def wrong_numerator(d):
    old=d['definitions'][0]['numerator'];p=copy.deepcopy(d['polynomials'][old]);p[0][1][0]+=1
    new=hashlib.sha256(json.dumps(p,separators=(',',':')).encode()).hexdigest()
    d['polynomials'][new]=p;d['definitions'][0]['numerator']=new

def missing_original_guard(d):del d['guards']['g48']
def missing_new_guard(d):del d['guards']['D52']
def false_source(d):d['definitions'][0]['source_equation']='36'
def zero_unit(d):d['definitions'][1]['denominator_nonzero']['numerator_nonzero']['constant'][0]=[0]*10
def bad_dependency(d):d['definitions'][2]['dependencies'].remove(88)
def missing_equation(d):del d['equations']['5']

result=[]
with tempfile.TemporaryDirectory() as td:
    for edit in [wrong_numerator,missing_original_guard,missing_new_guard,false_source,zero_unit,bad_dependency,missing_equation]:
        d=copy.deepcopy(D);edit(d);p=Path(td)/(edit.__name__+'.json');p.write_text(json.dumps(d))
        run=subprocess.run([sys.executable,str(HERE/'check_consequence.py'),'--certificate',str(p),'--no-receipt'],capture_output=True,text=True,timeout=30)
        assert run.returncode!=0,edit.__name__+' unexpectedly accepted'
        assert 'AssertionError' in run.stderr,run.stderr
        result.append({'mutation':edit.__name__,'status':'rejected by exact assertion','exit_code':run.returncode})
receipt={'status':'PASS: seven invalid modifications rejected','tests':result,'scope':'Checker negative controls, not an independent mathematical review.'}
(HERE/'MUTATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
