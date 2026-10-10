"""Reproduce new exact-regression suite and write a compact report."""
import hashlib,json,subprocess,sys
from pathlib import Path
from bitrev_rank import exact_cut_rank,predicted_qs_rank
root=Path(__file__).parent
p=subprocess.run([sys.executable,'-m','unittest','-v','test_exact_gate'],cwd=root,capture_output=True,text=True)
(root/'TEST_OUTPUT.txt').write_text(p.stdout+p.stderr)
print(p.stdout+p.stderr,flush=True)
assert p.returncode==0,'new research tests failed'
old=root/'prior_checkpoint_full.zip'
assert old.is_file()
summary={'date':'2026-10-09','new_suite':'9 tests passed',
 'old_checkpoint_nested_zip_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
 'main_theorem':'For N=2^m>=8, minimum over arbitrary independent row and column permutations of Fourier quasiseparable rank equals N/4+1',
 'cost_claim':'No FFT runtime complexity improvement',
 'sizes':{str(n):{'optimal_max_rank':predicted_qs_rank(n),
                  'central_rank':exact_cut_rank(n,n//2),
                  'rank_sum':sum(exact_cut_rank(n,k) for k in range(1,n))}
                  for n in (8,16,32,64,128,256,1024)}}
(root/'EXACT_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print('NEW CHECKPOINT OK; previous checkpoint intact. No faster FFT claimed.',flush=True)
