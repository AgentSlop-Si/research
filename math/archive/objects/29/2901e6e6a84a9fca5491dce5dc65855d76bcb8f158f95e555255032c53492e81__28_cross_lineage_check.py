#!/usr/bin/env python3
"""Cross-check phase-5 joint aggregate AGAINST original phase-4 Green decoder.

Reads the archived Phase-4 source from prior_phase4_bundle.zip; no external
file dependency. Neither side uses a full length-Q NumPy FFT as its executor.
"""
import tempfile,zipfile,pathlib,sys,math,json
import numpy as np
from joint_phase_collapse import chirp_base, all_phase_summaries,joint_exact_from_summaries
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    rng=np.random.default_rng(1510)
    records=[]
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(ROOT/'prior_phase4_bundle.zip') as z:z.extractall(tmp)
        sys.path.insert(0,str(pathlib.Path(tmp)/'fft_hero0_phase4_coprime_green'))
        from composite_cycle_core import ChirpState,local_phase_matrix,decode_balanced_scan
        from exact_batch import batch_summaries
        for q,m in [(55,5),(517,11),(1067,11),(2057,11)]:
            a=1;beta0=2
            x=rng.standard_normal(q)+1j*rng.standard_normal(q)
            base0=local_phase_matrix(q,m,ChirpState(a,beta0))
            base1=chirp_base(q,m,a,beta0)
            assert np.max(abs(base0-base1))<1e-12
            d0=batch_summaries(x,m,a,beta0).T  # K by M
            d1=all_phase_summaries(x,base1)
            assert np.max(abs(d0-d1))<1e-10
            slow=np.zeros(q,dtype=complex)
            for r in range(m):
                slow+=decode_balanced_scan(d0[:,r],q,m,
                    ChirpState(a,(beta0+r*(q//m))%q))
            slow/=m
            joint=joint_exact_from_summaries(d1,base1)
            delta=float(np.max(abs(slow-joint)))
            assert delta<5e-10,delta
            records.append({'Q':q,'M':m,'previous_M_green_scans_vs_joint_fft':delta,
                'passes':True})
    (ROOT/'cross_lineage_check.json').write_text(json.dumps(records,indent=2))
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
