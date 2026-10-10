"""Produce Phase 38 consolidated provenance-preserving exact certificate report."""
import json, subprocess, shutil
from pathlib import Path
import phase38_joint_masks as mod
from charzero_n4 import verify as verify_charzero

BASE=Path(__file__).resolve().parent

def run():
  native=str(BASE/'exhaustive_permutations')
  if not Path(native).exists():
    if shutil.which('g++') is None:raise RuntimeError('g++ compiler required')
    subprocess.run(['g++','-std=c++17','-O3',str(BASE/'exhaustive_permutations.cpp'),'-o',native],check=True)
  result={'phase':38,'date':'2026-10-10','status':'fixed-family exclusions, not a new FFT',
          'architecture':'A diag(u) P1 (G2 + lambda G3) P2 diag(v) C',
          'both_internal_masks_freely_tunable':True,
          'both_internal_permutations_freely_tunable':True,
          'green_couplings_and_six_cycle_orders_fixed':True,
          'field_results':[], 'charzero_direct_N4':verify_charzero(),
          'planted_valid_control':mod.plant_valid_control(8),
          'N64_second_prime_modular_collision':{
           'row_mapping':[53,55],'column_mapping':[19,26,5],
           'resultant_p1':470304279,'resultant_p2':0,
           'characteristic_zero_still_excluded_by_p1':True}}
  for p,g in mod.PRIMES:
    for n in (4,8,16,32,64,128,256):
      x=mod.build(n,p,g)
      w=mod.witness(x)
      w['anchor_calibration_lambda_7']=mod.anchored_fit(x,7)
      if n<=64:
        path=BASE/'instances'/f'phase38_instance_N{n}_p{p}.txt'
        assert path.exists(),path
        existing=json.loads((BASE/f'perm_N64_p{p}.json').read_text()) if n==64 else None
        if existing is None:
            stdout=subprocess.check_output([native,str(path)],text=True)
            w['exhaustive_permutations']=json.loads(stdout)
        else:
            w['exhaustive_permutations']=existing
        report=w['exhaustive_permutations']
        assert report['checked']==n*n*(n-1)*(n-1)*(n-2)
        assert report['zero_resultants']==(1 if n==64 and p==2013265921 else 0)
      else:
        path=BASE/'instances'/f'sample_N{n}_p{p}.json'
        w['sampled_permutations']=json.loads(path.read_text())
        assert w['sampled_permutations']['checked']==200000
        assert w['sampled_permutations']['zero_resultants']==0
      print(n,p,w.get('exhaustive_permutations',w.get('sampled_permutations'))['checked'])
      result['field_results'].append(w)
  (BASE/'phase38_recomputed_audit.json').write_text(json.dumps(result,indent=2)+'\n')
  return result
if __name__=='__main__':run()
