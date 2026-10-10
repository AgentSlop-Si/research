"""Compare *locally fitted* Green circuits with all-entry Fourier coherence.
Fitting rows 0,1 does NOT certify the transform on all rows.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from phase41_three_cycle import graph, apply_matrices
from phase41_actual_target_fit import calculate as amplitude_calculate
from phase41_unit_holonomy import model

BASE=Path(__file__).parent

def compare(n,kind):
    if kind=='three_unit_cycles':
        rec=json.loads((BASE/f'phase41_three_cycle_fit_N{n}.json').read_text())
        c,e,ch=graph(n)
        M,G,w=apply_matrices(n,np.asarray(rec['angles']),e,ch)
        assert np.allclose(abs(w),1,atol=1e-12)
    elif kind=='two_arbitrary_gain_cycles':
        rec=json.loads((BASE/f'phase41_nonunit_target_N{n}.json').read_text())
        c,e,ch=model(n)
        w,G,M=amplitude_calculate(n,np.asarray(rec['theta_logweights']),e,ch)
    else:raise ValueError(kind)
    root=np.exp(2j*np.pi/n)
    F=root**np.outer(np.arange(n),np.arange(n))
    # Exact projective dephasing, matching row 0 and column 0.
    Q=(M*M[0,0])/(M[:,[0]]*M[[0],:])
    two_error=float(np.max(abs(Q[:2]-F[:2])))
    third_error=float(np.max(abs(Q[2]-F[2])))
    max_other_error=float(np.max(abs(Q[2:]-F[2:])))
    return {'N':n,'kind':kind,'two_row_max_entry_error':two_error,
            'third_row_max_entry_error':third_error,'other_rows_max_error':max_other_error,
            'max_abs_gain':float(np.max(abs(w))),
            'min_abs_gain':float(np.min(abs(w))),
            'matrix_condition_2':float(np.linalg.cond(M)),
            'first_two_rows_fit':two_error<1e-9,
            'full_fft_not_reproduced':third_error>.1,
            'only_online_apply_is_linear_given_parameters':True}

if __name__=='__main__':
    data=[]
    for n in (8,16,32):
        for kind in ('two_arbitrary_gain_cycles','three_unit_cycles'):
            record=compare(n,kind)
            assert record['first_two_rows_fit'] and record['full_fft_not_reproduced']
            data.append(record)
            print(record,flush=True)
    (BASE/'phase41_full_audit.json').write_text(json.dumps(data,indent=2))
