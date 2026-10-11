# Publication adaptation of reviewer-authored checker.
# Original SHA-256: 7835ba7bc5fbda1f273bea836af0037741ccd95df86d7aea6b7f7daba56895e8
# Changes: Runs the explicitly adapted fresh preparation/scope/receipt files; final status names the mathematical replay rather than an unavailable original receipt.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
"""Reproduce this review. Execute fresh review code only; packet code stays inert."""
import pathlib,subprocess,sys,json,hashlib,platform
R=pathlib.Path(__file__).resolve().parent

def run(args,log,err=None):
 with (R/log).open('w') as out:
  if err:
   with (R/err).open('w') as e:subprocess.run(args,cwd=R,stdout=out,stderr=e,check=True)
  else:subprocess.run(args,cwd=R,stdout=out,stderr=subprocess.STDOUT,check=True)
run([sys.executable,str(R/'prepare_inert_review.py')],'prepare.log')
run([sys.executable,str(R/'fresh_selected_prepare.py')],'selected_preparation.log')
run([sys.executable,str(R/'review_scope_checks.py')],'scope_checks.log')
for stem in ['fresh_global_rank','fresh_selected_pivots']:
 run(['g++','-O3','-std=c++17','-Wall','-Wextra','-o',str(R/stem),str(R/(stem+'.cpp'))],stem+'_compile.log')
for prime in [1000003,1000033]:
 run([str(R/'fresh_global_rank'),str(prime),str(R/f'samples_{prime}.txt')],f'global_{prime}.log',f'global_{prime}.progress')
run([str(R/'fresh_global_rank'),'1000003',str(R/'samples_1000003.txt'),'degenerate'],'negative_control.log','negative_control.progress')
run([str(R/'fresh_selected_pivots'),str(R)],'selected_pivots.log','selected_pivots.progress')
run([sys.executable,str(R/'assemble_receipt.py')],'assemble.log')
print('Complete publication mathematical replay passed. Historical archive replay excluded. See independent_replay_results.json.')
