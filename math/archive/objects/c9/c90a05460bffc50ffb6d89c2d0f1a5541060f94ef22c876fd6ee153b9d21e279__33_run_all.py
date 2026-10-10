#!/usr/bin/env python3
"""Run independent Hero #0 Phase 5 checks, no hidden FFT oracle in engine."""
import subprocess,sys,json,pathlib,time
root=pathlib.Path(__file__).resolve().parent
scripts=['joint_phase_collapse.py','cross_lineage_check.py','finite_field_certificate.py',
         'phase_transfer_gate.py','measurement_rank_barrier.py',
         'bounded_coefficient_gate.py']
results=[]
for script in scripts:
    begin=time.perf_counter()
    print('RUN',script,flush=True)
    p=subprocess.run([sys.executable,str(root/script)],cwd=root,
                     stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    results.append({'script':script,'returncode':p.returncode,
                    'elapsed_s':round(time.perf_counter()-begin,3),
                    'stdout_tail':p.stdout[-650:],
                    'stderr_tail':p.stderr[-1200:]})
    if p.returncode:
        print('FAIL',script,'\n',p.stderr,flush=True)
        break
    print('PASS',script,'s=',results[-1]['elapsed_s'],flush=True)
(root/'suite_results.json').write_text(json.dumps(results,indent=2))
if any(x['returncode'] for x in results):sys.exit(1)
print('ALL PASSED:',len(results),'independent research scripts')
