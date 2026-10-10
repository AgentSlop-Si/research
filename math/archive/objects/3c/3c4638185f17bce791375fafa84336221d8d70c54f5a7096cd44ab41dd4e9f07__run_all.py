"""Reproduce this checkpoint's new audits; every subprocess is isolated."""
from pathlib import Path
import subprocess
import sys
import time
import json

ROOT = Path(__file__).resolve().parent
CHECKS = [
 ('fft_wordram_decoder_research', 'run_audit.py'),
 ('fft_wordram_review_research', 'verify_packing.py'),
 ('fft_wordram_review_research', 'review_decoder.py'),
 ('fft_wordram_integration', 'run_audit.py'),
 ('fft_macro_review_research', 'check_macro_bounds.py'),
 ('fft_bidirectional_extension_research', 'run_audit.py'),
 ('fft_bidirectional_extension_research', 'review_edge_checks.py'),
 ('fft_bidirectional_graph_research', 'run_audit.py'),
 ('fft_bidirectional_graph_research', 'independent_checks.py'),
]

def main():
    records=[]
    for directory,script in CHECKS:
        start=time.perf_counter()
        result=subprocess.run([sys.executable,script],cwd=ROOT/directory,
                              capture_output=True,text=True)
        records.append({'directory':directory,'script':script,
                        'exit_code':result.returncode,'seconds':time.perf_counter()-start,
                        'stdout':result.stdout,'stderr':result.stderr})
        print(('PASS' if result.returncode==0 else 'FAIL')+' '+directory+'/'+script,flush=True)
        if result.returncode:
            print(result.stdout+result.stderr)
            break
    output={'status':'PASS' if len(records)==len(CHECKS) and all(r['exit_code']==0 for r in records) else 'FAIL',
            'runs':records,'note':'Rerunning rewrites audit result/timing files; the original MANIFEST describes the distributed snapshot.'}
    (ROOT/'rerun_results.json').write_text(json.dumps(output,indent=2)+'\n')
    return 0 if output['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
