# Publication adaptation of reviewer-authored checker.
# Original SHA-256: 2a5f305a532fab6c7674e45cd09c837a807e78436d08862889a0a6ab5e06e84e
# Changes: Removed only original ZIP manifest/report-identity audit; all numerical controls retained. Frozen input verification is performed by the replay runner.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
"""Independent floating-point cross-checks and negative controls.
No uploaded code imported or executed. This is supplementary, not a proof.
"""
from pathlib import Path
import hashlib,json,random,zipfile
import numpy as np

root=Path(__file__).resolve().parent
cert=json.loads((root/'extracted/phase44_full_N8_box.json').read_text())
x=np.array([float(s) for s in cert['center_decimals']]);n=8
cycles=[]
for stage in range(4):
    rng=random.Random(44321+997*stage+n);orders=[list(range(n))]
    for _ in range(2):
        p=list(range(n));rng.shuffle(p);orders.append(p)
    cycles.append(orders)

def network(params):
    weights=[];layers=[]
    for stage in range(4):
        w=np.ones(24,dtype=complex);w[7:]=np.exp(1j*params[17*stage:17*(stage+1)])
        weights.append(w.reshape(3,8))
        S=np.zeros((n,n),dtype=complex)
        for t,order in enumerate(cycles[stage]):
            W=np.zeros((n,n),dtype=complex)
            for j in range(n):W[order[j],order[j-1]]=w[8*t+j]
            S+=np.linalg.solve(np.eye(n)-W,np.eye(n))
        layers.append(S)
    Ds=[]
    for stage in range(3):
        pos=68+14*stage
        Ds.append(np.r_[1,np.exp(params[pos+7:pos+14]+1j*params[pos:pos+7])])
    M=layers[0]
    for stage in range(1,4):M=layers[stage]@(Ds[stage-1][:,None]*M)
    return M,weights,Ds

def normalize(M):return M*M[0,0]/(M[0,:][None,:]*M[:,0][:,None])
F=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)
M,weights,Ds=network(x);Q=normalize(M)
L=M[0,0]/M[:,0];R=1/M[0,:]

def cyclic_solve(order,w,v):
    # Solve y[j]-w[j]y[j-1]=v[j] by closing one scalar recurrence.
    b=0j;a=1+0j
    for j in range(1,n):b=v[order[j]]+w[j]*b;a=w[j]*a
    y=np.zeros(n,dtype=complex)
    y[order[0]]=(v[order[0]]+w[0]*b)/(1-w[0]*a)
    for j in range(1,n):y[order[j]]=v[order[j]]+w[j]*y[order[j-1]]
    return y
def apply(v):
    out=R*v
    for stage in range(4):
        out=sum((cyclic_solve(order,weights[stage][t],out) for t,order in enumerate(cycles[stage])),np.zeros(n,dtype=complex))
        if stage<3:out=Ds[stage]*out
    return L*out

rng=np.random.default_rng(234044)
samples=[np.eye(n,dtype=complex)[:,i] for i in range(n)]
samples += [rng.normal(size=n)+1j*rng.normal(size=n) for _ in range(24)]
perturbed=x.copy();perturbed[cert['selected_variable_indices'][0]]+=1e-3
phase_only=x.copy()
for stage in range(3):phase_only[68+stage*14+7:68+stage*14+14]=0
controls={
 'dense_direct_inverse_all64_F8_max_error':float(np.max(abs(Q-F))),
 'matrix_free_all8_basis_F8_max_error':float(np.max(abs(np.column_stack([apply(v) for v in samples[:8]])-F))),
 'matrix_free_24_random_FFT_max_error':max(float(np.max(abs(apply(v)-np.fft.fft(v)))) for v in samples[8:]),
 'matrix_free_vs_calibrated_dense_max_error':max(float(np.max(abs(apply(v)-Q@v))) for v in samples),
 'wrong_sign_Fourier_control_error':float(np.max(abs(Q-F.conj()))),
 'selected_parameter_plus_0_001_control_error':float(np.max(abs(normalize(network(perturbed)[0])-F))),
 'zero_all_log_amplitudes_control_error':float(np.max(abs(normalize(network(phase_only)[0])-F))),
 'negative_controls_meaning':'Parameter/model changes do not preserve this witness; this does not prove impossibility of separately synthesizing a phase-only network.',
 'uploaded_programs_executed':False,
}
assert controls['dense_direct_inverse_all64_F8_max_error']<1e-9
assert controls['matrix_free_all8_basis_F8_max_error']<1e-9
assert controls['matrix_free_24_random_FFT_max_error']<1e-9
assert controls['wrong_sign_Fourier_control_error']>1
assert controls['selected_parameter_plus_0_001_control_error']>1e-6
assert controls['zero_all_log_amplitudes_control_error']>1

controls['publication_archive_audit']='omitted; historical hashes recorded separately'
(root/'fresh_controls_results.json').write_text(json.dumps(controls,indent=2)+'\n')
print(json.dumps(controls,indent=2))
