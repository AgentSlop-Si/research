import json
from pathlib import Path
p=Path(__file__).resolve().parent
z=json.loads((p/'results.json').read_text())
lines=['# Repeated chirp-block reference experiment','',
'Independent NumPy code written from the algebra; no uploaded code was run. This is a bounded numerical test, not a concentration theorem or a fast implementation.','',
'## Setup','',
'- Seed: 20261009; 12 trials per family/K/scheme; R = 1, 2, 4, 8, 16, 32; K = 4, 16, 32.',
'- Dyadic: M=256, independent uniform odd a, uniform b, and either d=0 or independent uniform odd d.',
'- Prime: M=251, independent uniform a,b and either d=0 or independent uniform d. Zero a and zero d are included; do not conflate this with a nonzero-a ensemble.',
'- N=KM, maximum N=8192. Within each condition, the same first R independent sketches serve both aggregators and all five test signals. Different K/family/scheme conditions use different seed draws.',
'- Signals: all ones; identical local mode exp(2πi·7t/M) in each block; a fixed random-phase array per family/K; one spike; and three nonzero coherent blocks equal to the conjugate chirp with fixed seed (a,b,d)=(1,0,1). That last input is fixed before drawing sketches, not adaptive to the tested random seeds.',
'- Sketch: σ[r,t]=exp(2πi(a t²+(b+dr)t)/M), y[r]=sum_t σ[r,t]x[r,t]. Reference decoder: unitary full N-point FFT of the flattened array conjugate(σ[r,t])y[r].',
'- Aggregation: arithmetic complex mean, or separate coordinatewise medians of real and imaginary parts. Even R uses NumPy’s average-of-two-middle-values convention. This is NOT median of means.',
'- Primary error: max_m |estimate_m−FFT(x)_m| / (||x||₁/√N). RMS is sqrt(mean_m |error_m|²) divided by the same scale. Relative L2 is ||error||₂/||x||₂. All summary table entries below are medians across 12 trials.',
'', '## Exact dyadic resonance verification','',
f"Checked 27 combinations of M in {{16,64,256}}, even K in {{2,4,8}}, and three odd-a/odd-d seeds. For h=d⁻¹ mod M and q=2ah mod M, both the full complex formula and magnitude 2 sin(πK/M)/(K sin(2π/M)) agree with the reference. Maximum complex discrepancy: {max(v['complex_error'] for v in z['resonance_checks']):.3g}. The checked formula is from the prior AFFINE_RESONANCE.md checkpoint.",
'', '## Main results at K=16, R=32','',
'| Family | Scheme | Input | Mean max | Median max | Mean RMS | Median RMS |','|---|---|---|---:|---:|---:|---:|']
for fam in ['dyadic_odd_a_odd_affine_d','prime_uniform_a_b_d_including_zero']:
 for scheme in ['shared_d_zero','affine_d_random']:
  for inp in ['flat','repeated_local_mode','random_phase','spike','fixed_coherent_three_blocks']:
   rs=[r for r in z['results'] if r['family']==fam and r['scheme']==scheme and r['input']==inp and r['K']==16 and r['repetitions']==32]
   a=next(r for r in rs if r['aggregation']=='complex_mean'); b=next(r for r in rs if r['aggregation']=='coordinate_median')
   lines.append(f"| {'dyadic' if fam.startswith('dyadic') else 'prime'} | {'shared' if scheme.startswith('shared') else 'affine'} | {inp} | {a['normalized_max_error']['median']:.4f} | {b['normalized_max_error']['median']:.4f} | {a['normalized_rms_error_median']:.4f} | {b['normalized_rms_error_median']:.4f} |")
lines+=['','## Affine complex-mean scaling','', '| Family | K | Input | R=1 | R=2 | R=4 | R=8 | R=16 | R=32 |','|---|---:|---|---:|---:|---:|---:|---:|---:|']
for fam in ['dyadic_odd_a_odd_affine_d','prime_uniform_a_b_d_including_zero']:
 for K in [4,16,32]:
  for inp in ['flat','spike']:
   rs=sorted([r for r in z['results'] if r['family']==fam and r['scheme']=='affine_d_random' and r['input']==inp and r['K']==K and r['aggregation']=='complex_mean'],key=lambda r:r['repetitions'])
   lines.append('| '+('dyadic' if fam.startswith('dyadic') else 'prime')+' | '+str(K)+' | '+inp+' | '+' | '.join(f"{r['normalized_max_error']['median']:.4f}" for r in rs)+' |')
lines+=['','## Interpretation and limits','',
'- Independent averaging reduces the visible moving resonances for dense inputs in these finite tests. At K=16, affine flat max error drops from about 1 to 0.199 (dyadic) or 0.143 (prime) after 32 sketches. This neither proves an all-input result nor establishes asymptotic polylogarithmic repetition suffices.',
'- A spike remains far from a small normalized maximum-error target: approximately 7.24 dyadic or 7.26 prime at K=16,R=32. Its normalized RMS is about 2.79, versus about 15.97/15.81 with one sketch, broadly consistent with a 1/sqrt(R) scale. Increasing K while holding M fixed does not resolve within-block spike interference.',
'- Plain coordinatewise median is not interchangeable with mean or median-of-means. It performs poorly for dyadic flat/local-mode inputs here, and shared-slope dyadic medians can return essentially zero (max error 1). The fixed coherent three-block dyadic input also exposes misleadingly small normalized max errors from near-zero estimates: relative L2 error 1 is recorded in JSON.',
'- Small normalized maximum error and small relative RMS/L2 are different criteria. For example dyadic affine flat R=32 has normalized max 0.199 yet relative L2 about 2.82.',
'- Every repetition makes K measurements, thus RK total stored scalar sketches; direct sketch formation here costs O(RN), and this reference decoding costs O(RN log N). Coordinatewise median also needs aggregation work/storage. These tests do not establish an O(N log log N) end-to-end algorithm or a cheaper decoder.',
'- Twelve trials provide only descriptive finite-sample evidence. JSON contains all trial metrics, min/max, and empirical p90, which must not be interpreted as a proved tail bound. Tests do not optimize sparse recovery or use an alternative nonlinear decoder.',
'', '## Files and rerun','',
'- repetition_reference.py: standalone algebraic experiment; requires NumPy.',
'- results.json: complete 720 condition summaries, raw trial metrics, exact checks, seed, and runtime.',
'- run_summary.txt: selected console results.',
'- Run: OPENBLAS_NUM_THREADS=1 python repetition_reference.py',
f"- Recorded experiment runtime: {z['runtime_seconds']:.2f} seconds."]
(p/'README.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[40:64]))
