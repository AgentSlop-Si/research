"""Reproduce the extension, regenerate the exact integer certificates, run tests."""
from pathlib import Path
import subprocess,sys,json
from window_gate import enumerate_n8, combinatorial_ceiling,check_windows
from finite_field_audit import run as audit
root=Path(__file__).parent
p16=[8,0,13,4,9,3,15,5,6,1,12,11,10,2,14,7]
report={
  'exact_permutation_screen_n8':enumerate_n8(),
  'combinatorial_ceilings':{str(r):combinatorial_ceiling(r,r,r,r) for r in range(1,5)},
  'N16_window_survivor':{'permutation':p16,'passes_all_window_gates':not check_windows(p16)},
  'interpretation':'All filters are necessary only; no FFT upper-bound improvement.'
}
(root/'SCREEN_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print('PERMUTATION SCREEN:',report,flush=True)
audit()
p=subprocess.run([sys.executable,'-m','unittest','-v','test_window_gate'],cwd=root)
assert p.returncode==0
print('NEW WINDOW TEST SUITE PASSED',flush=True)
