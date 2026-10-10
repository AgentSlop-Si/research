"""Fresh read-only reconstruction of saved numerical candidate parameters, never optimizer execution."""
from pathlib import Path
import numpy as np,json
R=Path(__file__).resolve().parent;S=R/'source/fft_green_phase41_unit_holonomy';out=[]
def form(n,cycles,chords,values):
 weights=np.ones(len(cycles)*n,dtype=complex);weights[chords]=values;M=np.zeros((n,n),dtype=complex)
 for s,c in enumerate(cycles):
  A=np.eye(n,dtype=complex)
  for j in range(n):A[c[j],c[j-1]]-=weights[s*n+j]
  M+=np.linalg.inv(A)
 return M
for n in (8,16,32):
 for family,stem in [('three_unit_cycles','phase41_three_cycle_fit'),('two_complex_amplitude','phase41_nonunit_target')]:
  x=json.loads((S/f'{stem}_N{n}.json').read_text())
  if family=='three_unit_cycles':values=np.exp(1j*np.array(x['angles']))
  else:
   z=np.array(x['theta_logweights']);values=np.exp(z[:n+1]+1j*z[n+1:])
  M=form(n,x['cycles'],x['chords'],values);F=np.exp(2j*np.pi*np.arange(n)[:,None]*np.arange(n)[None,:]/n)
  V=M*M[0,0]/(M[:,0,None]*M[None,0,:]);err=np.abs(V-F)
  assert err[:2].max()<1e-8 and err[2].max()>1
  out.append(dict(N=n,family=family,two_row_max_error=float(err[:2].max()),third_row_max_error=float(err[2].max()),all_rows_max_error=float(err.max()),condition_number=float(np.linalg.cond(M)),classification='ordinary floating reconstruction, not exact target certificate'))
# Evaluate retained high-precision decimal parameters without running the source Newton/optimization code.
import mpmath as mp
mp.mp.dps=110
for n in (8,16):
 x=json.loads((S/f'phase41_highprecision_N{n}.json').read_text());base=json.loads((S/f'phase41_nonunit_target_N{n}.json').read_text())
 gains=[mp.exp(mp.mpc(a,b)) for a,b in zip(x['z_real'],x['z_imag'])];ws=[mp.mpc(1)]*(2*n)
 for e,w in zip(base['chords'],gains):ws[e]=w
 M=mp.zeros(n)
 for s,c in enumerate(base['cycles']):
  H=mp.eye(n)
  for j in range(n):H[c[j],c[j-1]]-=ws[s*n+j]
  M+=H**-1
 residual=max(abs(M[0,j]*M[1,0]/(M[1,j]*M[0,0])-mp.exp(-2j*mp.pi*j/n)) for j in range(1,n))
 third=max(abs(M[2,j]*M[0,0]/(M[2,0]*M[0,j])-mp.exp(4j*mp.pi*j/n)) for j in range(n))
 assert residual<mp.mpf('1e-80') and third>1
 out.append(dict(N=n,family='two_complex_amplitude_retained_decimal_high_precision',evaluation_digits=110,source_reported_residual=x['residual_scientific'],fresh_retained_parameter_residual=mp.nstr(residual,30),third_row_max_error=mp.nstr(third,30),classification='high-precision residual only; no validated interval or exact root proof'))
(R/'FRESH_PARTIAL_FIT_RESULTS.json').write_text(json.dumps({'records':out,'optimizer_rerun':False,'supplied_code_executed':False},indent=2)+'\n');print(json.dumps(out,indent=2))
