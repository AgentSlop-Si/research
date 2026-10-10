"""POSITIVE Fourier phase-coherence control: 2 masks, 3 K8-defined mixers.

This is NOT a faster FFT. It combines the explicit field-descent factors
F_a=B_a Q_a A_a (a=16,32,64) with the classical Cooley-Tukey split
N=8*a:
  F_N=(B_a tensor I_8) (Q_a tensor I_8) (A_a tensor I_8)
        T_N (I_a tensor F_8) P_in.
All non-diagonal operators are defined over K8=Q(zeta_8). The two
non-K8 diagonal phase masks are Q_a and T_N. O(NlogN) work is NOT
beaten; this is a correctness/feasibility control for Phase 14 gates.

The program verifies ALL 128 Fourier columns, and sampled columns for
N=256,512, using a genuinely different direct Fourier oracle.
"""
from field_descent import cycles
from galois_gate import MOD


def power_root(n):
    assert (MOD-1)%n==0
    return pow(3,(MOD-1)//n,MOD)


def base_factor(n):
    """Construct exact F_n=B Q A over finite prime field, B,A in K8.

    Returns B as [k][e], A as [e][j], q[e] in Fourier root field.
    """
    assert n in (16,32,64)
    L=n//8
    omega8=power_root(8)
    omegaL=power_root(L)
    omegaN=power_root(n)
    B=[[0]*n for _ in range(n)]
    A=[]; q=[]
    eid=0
    for orbit in cycles(n):
        d=len(orbit)
        for e in range(d):
            r=e*(L//d)
            lam=pow(omegaL,r,MOD)
            for t,k in enumerate(orbit):B[k][eid]=pow(lam,t,MOD)
            q.append(pow(omegaN,r,MOD))
            row=[];k0=orbit[0]
            for j in range(n):
                row.append(pow(omega8,(k0*j-r)//L,MOD)
                           if k0*j%L==r else 0)
            A.append(row)
            eid+=1
    assert eid==n
    return B,q,A


def two_mask_fft(n,x,fac=None):
    assert n in (128,256,512)
    a=n//8
    assert len(x)==n
    B,q,A=fac if fac is not None else base_factor(a)
    omega8=power_root(8);omegaN=power_root(n)
    # P_in and (I_a tensor F_8): gather stride-a sequences.
    work=[[0]*8 for _ in range(a)]
    for j1 in range(a):
        for k2 in range(8):
            work[j1][k2]=sum(pow(omega8,k2*j2,MOD)*x[j1+a*j2]
                              for j2 in range(8))%MOD
    # First high-order phase mask T_N.
    for j1 in range(a):
        for k2 in range(8):
            work[j1][k2]=work[j1][k2]*pow(omegaN,j1*k2,MOD)%MOD
    # K8-valued middle factor A_a tensor I_8.
    middle=[[0]*8 for _ in range(a)]
    for e in range(a):
        for k2 in range(8):
            middle[e][k2]=sum(A[e][j1]*work[j1][k2]
                               for j1 in range(a) if A[e][j1])%MOD
    # Second high-order phase mask Q_a tensor I_8.
    for e in range(a):
        for k2 in range(8):middle[e][k2]=middle[e][k2]*q[e]%MOD
    # Final orbit-eigenbasis factor B_a tensor I_8.
    out=[0]*n
    for k1 in range(a):
        for k2 in range(8):
            out[8*k1+k2]=sum(B[k1][e]*middle[e][k2] for e in range(a)
                                  if B[k1][e])%MOD
    return out


def direct_dft(n,x):
    omega=power_root(n)
    return [sum(x[j]*pow(omega,k*j,MOD) for j in range(n))%MOD
            for k in range(n)]


def verify(n,all_basis=False):
    fac=base_factor(n//8)
    probes=[0,1,2,3,n//3,n-1]
    if all_basis:probes=list(range(n))
    omega=power_root(n)
    for j in probes:
        inp=[0]*n;inp[j]=1
        expected=[pow(omega,k*j,MOD) for k in range(n)]
        got=two_mask_fft(n,inp,fac)
        assert got==expected,(n,j,next((k for k in range(n) if got[k]!=expected[k]),None))
    x=[((j*97+11)**2+23*j+7)%MOD for j in range(n)]
    assert two_mask_fft(n,x,fac)==direct_dft(n,x)
    return dict(n=n,all_basis=all_basis,basis_checked=len(probes),
                dense_input_direct_DFT_match=True,
                interstage_nonbase_phase_masks=2,
                other_stages_defined_over_zeta8=True,
                asymptotic_speedup=False)

if __name__=='__main__':
    for n in (128,256,512):
        print(verify(n,all_basis=(n==128)))
