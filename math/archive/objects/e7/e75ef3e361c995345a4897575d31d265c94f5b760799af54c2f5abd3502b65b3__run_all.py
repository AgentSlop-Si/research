from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from weyl_line_basis import finite_field_case

ROOT=Path(__file__).resolve().parent
CASES=[7,11,13,17]

def main():
    records=[finite_field_case(n) for n in CASES]
    results={
      'phase':'v21',
      'title':'Weyl-line Fourier embedding and Bluestein collapse',
      'finite_field_cases':records,
      'theorem_checks':{
        'generic_packet_blocks_checked':sum(r['n'] for r in records),
        'all_block_ranks_full':all(r['block_ranks']==[r['n']-1]*r['n'] for r in records),
        'all_green_line_identities':all(r['green_line_identity'] for r in records),
        'all_chirp_polynomial_identities':all(r['chirp_polynomial_identity'] for r in records),
        'all_chirp_spectra_full_support':all(r['chirp_spectrum_nonzero']==r['n'] for r in records),
      }
    }
    (ROOT/'results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    summary={
      'exact_faster_fft':False,
      'positive_result':'generic multi-h character packets plus I span every constant-diagonal matrix; a gauged Fourier has an exact N-1-resolvent Weyl-line representation',
      'collapse':'the Fourier-compatible line is a full quadratic-chirp polynomial in one monomial Weyl generator, equivalent to Bluestein convolution',
      'tests_expected':11,
      'cases':CASES,
    }
    (ROOT/'RESULT_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    commands=[
      [sys.executable,'-m','unittest','-v','test_checkpoint'],
      [sys.executable,'independent_verifier.py'],
    ]
    logs=[]
    for cmd in commands:
      cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
      logs.append('$ '+' '.join(cmd)+'\n'+cp.stdout+cp.stderr)
      if cp.returncode: raise SystemExit(cp.returncode)
    (ROOT/'run_all.log').write_text('\n'.join(logs))
    print(json.dumps(results['theorem_checks'],sort_keys=True))

if __name__=='__main__':main()
