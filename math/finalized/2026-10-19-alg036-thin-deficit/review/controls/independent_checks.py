#!/usr/bin/env python3
"""New independent diagnostic only. No historical code, network, or external writes."""
import sys, json, hashlib, math
from pathlib import Path
import sympy as s
import mpmath as mp
I=s.I
counts={}
def count(k): counts[k]=counts.get(k,0)+1
def eqzero(M):
    assert all(s.expand(x)==0 for x in M), M

def realify_row(row):
    re=[s.re(z) for z in row]; im=[s.im(z) for z in row]
    return s.Matrix([re+[-z for z in im],im+re])

def householder(n,seed):
    w=s.Matrix([s.Rational((j+seed)%5-2) + I*s.Rational((j*seed+1)%3-1) for j in range(n)])
    if w==s.zeros(n,1): w[0]=1
    return s.eye(n)-2*w*w.conjugate().T/(w.conjugate().T*w)[0]

# Exact nontrivial complex rational isometries, including zero leverages.
for n in range(1,8):
    for d in range(1,n+1):
        for seed in range(3):
            U=s.eye(n) if seed==0 else householder(n,seed)*householder(n,seed+3)
            V=U[:,:d]
            eqzero(V.conjugate().T*V-s.eye(d))
            P=(V*V.conjugate().T).applyfunc(s.expand)
            eqzero(P*P-P)
            eqzero(P.conjugate().T-P)
            assert s.trace(P)==d
            total=s.zeros(2*d); leverage=s.Integer(0)
            for j in range(n):
                row=list(V[j,:]); p=s.expand(sum(z*s.conjugate(z) for z in row))
                assert p>=0 and p<=1
                assert p==s.expand(P[j,j])
                T=realify_row(row)
                eqzero(T*T.T-p*s.eye(2))
                total+=T.T*T; leverage+=p
                # With B=T/sqrt(p), these exact identities give BB*=I_2.
                if p: count('positive_rank_two_rows')
                else: count('zero_leverage_rows')
            eqzero(total-s.eye(2*d))
            assert leverage==d
            count('complex_real_frame_data')
            # Fresh posterior update checks, including redundant measurements.
            for seed2 in [1,2]:
                a=s.Matrix([s.Integer((j+seed2)%4-1)+I*s.Integer((2*j+seed2)%3-1) for j in range(n)])
                v=s.expand((a.conjugate().T*P*a)[0])
                if v:
                    Q=P-P*a*a.conjugate().T*P/v
                    Q=Q.applyfunc(s.expand)
                    eqzero(Q*Q-Q); eqzero(Q.conjugate().T-Q)
                    eqzero(Q*a); assert s.trace(Q)==d-1
                    count('posterior_positive_variance_updates')
                else:
                    eqzero(P*a); count('posterior_redundant_updates')

# Symbolic exact scalar derivatives, not finite sample concavity evidence.
p,a=s.symbols('p a',positive=True)
phi=p*s.log(1-s.exp(-a/p))
first=s.log(1-s.exp(-a/p))-(a/p)/(s.exp(a/p)-1)
second=-(a/p)**2*s.exp(a/p)/(p*(s.exp(a/p)-1)**2)
assert s.simplify(s.diff(phi,p)-first)==0
assert s.simplify(s.diff(phi,p,2)-second)==0
count('symbolic_concavity_identities'); count('symbolic_monotonicity_identities')

# Exact equal-block frames without square-root arithmetic: normalized row outer
# products are p times an elementary coordinate projector, p=1/k.
for d in range(1,7):
    for k in range(1,8):
        n=k*d
        leverages=[s.Rational(1,k)]*n
        assert sum(leverages)==d
        assert all(leverages[j]==s.Rational(d,n) for j in range(n))
        exponents=[sum(leverages[q*k:(q+1)*k]) for q in range(d)]
        assert exponents==[1]*d
        assert n*s.Rational(1,k)==d
        count('exact_equal_block_exponent_checks')

# High-precision diagnostics for scalar envelope, rank monotonicity, and window.
mp.mp.dps=90
max_envelope_gap=mp.mpf(0)
for n in range(1,30):
    for d in range(1,n+1):
        for r2 in [mp.mpf('0.01'),mp.mpf('0.5'),mp.mpf(2),mp.mpf(10)]:
            F=mp.power(-mp.expm1(-n*r2/d),d)
            coord=mp.power(-mp.expm1(-r2),d)
            assert coord<=F+mp.mpf('1e-85')
            if d<n:
                nxt=mp.power(-mp.expm1(-n*r2/(d+1)),d+1)
                assert nxt<=F
            count('rank_envelope_diagnostics')

windows=[]
for shift in [-2,0,2]:
    rows=[]
    target=mp.exp(-mp.exp(-shift))
    for k in [8,12,18,24,36]:
        # C=1; N=k*d ensures exact equality construction, while d≈exp(k-shift).
        d=int(mp.nint(mp.exp(k-shift))); n=k*d
        actual_shift=mp.mpf(k)-mp.log(d)
        gaussian=mp.power(-mp.expm1(-k),d)
        eps=mp.mpf(n)**(-mp.mpf(1)/4)
        Flo=mp.power(-mp.expm1(-k*(1-eps)),d)
        Fhi=mp.power(-mp.expm1(-k*(1+eps)),d)
        tail_lo=mp.exp(-n*(-eps-mp.log(1-eps)))
        tail_hi=mp.exp(-n*(eps-mp.log(1+eps)))
        assert gaussian>=Flo and gaussian<=Fhi
        rows.append({'k':k,'N':n,'d':d,'shift':str(actual_shift),'gaussian':str(gaussian),'limiting_value':str(target),'relative_norm_lower':str(max(0,Flo-tail_lo)),'relative_norm_upper':str(min(1,Fhi+tail_hi)),'epsilon_times_k':str(eps*k)})
        count('critical_window_diagnostics')
    assert abs(mp.mpf(rows[-1]['gaussian'])-target)<mp.mpf('1e-12')
    windows.append({'specified_shift':shift,'rows':rows})

out={'status':'PASS','python':sys.version.split()[0],'sympy':s.__version__,'mpmath':mp.__version__,'historical_program_execution':False,'network_access':False,'counts':counts,'critical_window':windows,'qualification':'Exact finite algebra checks support transcription only; the all-dimensional proof and source audit establish the theorem. Floating diagnostics do not prove probability bounds.'}
print(json.dumps(out,indent=2,sort_keys=True))
