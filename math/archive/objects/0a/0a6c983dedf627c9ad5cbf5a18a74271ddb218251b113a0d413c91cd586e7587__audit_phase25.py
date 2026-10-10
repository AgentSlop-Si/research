"""Independent exact matrix audit; oracle is the DFT definition, not an FFT."""
from pathlib import Path
import json,random
from gt3_deferred import DeferredGT3,ct3_baseline,primitive_roots,direct_dft
from entropy_gate import entropy_trajectory
from gt3_green import transform_deferred_conjugate_gt3
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects

field_entries=0;basis_vectors=0;preview_entries=0;tested_lengths=[]

# Evaluate every basis column of the complete Fourier matrix at all lengths.
for p,g,lengths in [(2013265921,31,(6,12,24,48,96,192,384,768)),
                    (97,5,(6,12,24,48,96))]:
    for n in lengths:
        w=primitive_roots(n,p,g)
        powers=[1]*n
        for j in range(1,n):powers[j]=powers[j-1]*w%p
        for j in range(n):
            x=[0]*n;x[j]=1
            e=DeferredGT3(x,p,g)
            keys=sorted(set(list(range(min(10,n)))+[n-1]))
            pre=e.preview(keys)
            v=1;z=powers[j];ref=[]
            for k in range(n):ref.append(v);v=v*z%p
            for k,value in pre.items():
                if value!=ref[k]:raise AssertionError(f'preview mismatch p={p} N={n} j={j} k={k}')
            preview_entries+=len(pre)
            if e.full()!=ref:raise AssertionError(f'full mismatch p={p} N={n} j={j}')
            if e.stats()['arithmetic']!=e.predicted_full_arithmetic():raise AssertionError('miscount')
            field_entries+=n;basis_vectors+=1
        tested_lengths.append({'field_p':p,'N':n,'columns':n,'matrix_entries':n*n})

# Compare two algebraically different all-input implementations on dense data.
dense_checks=[]
for n in (96,384,1536,6144):
    rng=random.Random(25111+n)
    x=[rng.randrange(2013265921) for _ in range(n)]
    e=DeferredGT3(x);out=e.full()
    alt,count=ct3_baseline(x)
    assert out==alt
    if n<=384:assert out==direct_dft(x,e.omega,e.p)
    dense_checks.append(n)
    field_entries+=n

# Check the unitary-model entropy potential; separate complex domain from Fp.
entropy_checks=[]
for n in (2,4,8,16,32,64):
    info=entropy_trajectory(n)
    assert info['gate_count']==info['known_unitary_lower_bound']
    assert all(abs(v-n*ell)<1e-8 for ell,v in enumerate(info['entropies']))
    assert info['max_column_l2_deviation']<1e-12
    entropy_checks.append({'N':n,'gates':info['gate_count'],
              'entropy_increase_per_stage':n,
              'entropy_end':round(info['entropies'][-1],10)})

report={'phase':25,'audit':'complete finite-field Fourier basis matrices plus independent dense samples',
  'basis_columns_tested':basis_vectors,'matrix_entries_compared':field_entries-96-384-1536-6144,
  'total_exact_output_comparisons':field_entries,
  'preview_output_comparisons':preview_entries,
  'fields_and_lengths':tested_lengths,'dense_input_lengths':dense_checks,
  'entropy_checks':entropy_checks,
  'claims_not_established':['unrestricted exact o(NlogN)',
     'complex numerical stability','historical priority','bit-time sub-NlogN']}
Path('PHASE25_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"Independent exact finite-field outputs checked: {field_entries:,}")
print(f"Complete Fourier matrix columns checked: {basis_vectors:,}")
print(f"Preview coefficient comparisons: {preview_entries:,}")
print('Complex unitary entropy audits:',entropy_checks)
