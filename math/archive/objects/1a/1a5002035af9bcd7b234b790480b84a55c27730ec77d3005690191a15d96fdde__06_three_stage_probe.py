"""Independent exact-field black-box Fourier-covariance and Galois-covariance probes.

Q_j are quadratic or linear Fourier phases. Stage matrices are fixed over
K=Q(zeta_8) and reduced into F_998244353. In these finite examples the
Galois action zeta_N -> zeta_N^9 is simulated exactly by replacing only
phase exponents; this is a necessary characteristic-zero identity.
"""
import json
from collections import Counter
from galois_gate import MOD, rank_mod, stage_kind, n_power_of_two


def direct_fourier(n, x, a=1):
    omega=pow(3,(MOD-1)//n,MOD)
    return [sum(pow(omega,a*k*j,MOD)*x[j] for j in range(n))%MOD
            for k in range(n)]


def make_exponents(n, mode):
    if mode=='linear':return [j for j in range(n)]
    if mode=='quadratic':return [j*j for j in range(n)]
    if mode=='neg_quadratic':return [-j*j for j in range(n)]
    if mode=='shift_quadratic':return [j*j+j for j in range(n)]
    raise ValueError(mode)


def candidate_apply(stages,masks,x,automorphism=1):
    n=len(x)
    omega=pow(3,(MOD-1)//n,MOD)
    y=list(x)
    for i,stage in enumerate(stages):
        y=stage.apply(y)
        if i<len(masks):
            y=[val*pow(omega,automorphism*exponent,MOD)%MOD
               for val,exponent in zip(y,masks[i])]
    return y


def candidate_rank_gates(n,types,mask_types,seed=1400):
    assert n_power_of_two(n) and len(types)==len(mask_types)+1
    stages=[stage_kind(n,s,seed+31*i+n) for i,s in enumerate(types)]
    masks=[make_exponents(n, name) for name in mask_types]
    cols=[];sigcols=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        cols.append(candidate_apply(stages,masks,e,1))
        sigcols.append(candidate_apply(stages,masks,e,9))
    omega=pow(3,(MOD-1)//n,MOD)
    d=[pow(omega,k,MOD) for k in range(n)]
    cov=[[ (cols[(j+1)%n][k]-d[k]*cols[j][k])%MOD for j in range(n)]
         for k in range(n)]
    gal=[[ (sigcols[j][k]-cols[j][9*k%n])%MOD for j in range(n)]
         for k in range(n)]
    return dict(n=n,stage_types=types,mask_types=mask_types,
                covariance_rank=rank_mod(cov),galois_defect_rank=rank_mod(gal),
                exact_fourier=False)


def control_fourier(n):
    assert n_power_of_two(n)
    omega=pow(3,(MOD-1)//n,MOD)
    f=[[pow(omega,k*j,MOD) for j in range(n)] for k in range(n)]
    return dict(n=n,
                covariance_zero=all(f[k][(j+1)%n]==pow(omega,k,MOD)*f[k][j]%MOD
                                    for k in range(n) for j in range(n)),
                galois_zero=all(pow(f[k][j],9,MOD)==f[9*k%n][j]
                                for k in range(n) for j in range(n)))


def run_probes():
    r=[]
    for n in (16,32,64):
        for types,masks in ((('tree','tree','tree'),('linear','quadratic')),
                            (('haar','haar','haar'),('quadratic','neg_quadratic')),
                            (('strong','haar','strong'),('linear','linear')),
                            (('strong','strong','strong'),('shift_quadratic','neg_quadratic'))):
            r.append(candidate_rank_gates(n,types,masks))
    return r

if __name__=='__main__':
    print(json.dumps(dict(control=[control_fourier(n) for n in (16,32,64)],
                          candidates=run_probes()),indent=2))


def sparse_phase_rank_control(n,counts=(3,4)):
    """Exact rank telescoping check with 2 sparse nonbase phase masks."""
    assert n_power_of_two(n)
    types=('tree','haar','strong')
    stages=[stage_kind(n,s,2003+31*i+n) for i,s in enumerate(types)]
    masks=[]
    for k,cnt in enumerate(counts):
        ar=[0]*n
        for j in range(cnt):
            ar[(7*j+5*k+3)%n]=(j+1)*(k+1)
        masks.append(ar)
    cols=[];sigcols=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        cols.append(candidate_apply(stages,masks,e,1))
        sigcols.append(candidate_apply(stages,masks,e,9))
    diff=[[(sigcols[j][k]-cols[j][k])%MOD for j in range(n)] for k in range(n)]
    rank=rank_mod(diff)
    assert rank<=sum(counts)
    return dict(n=n,phase_positions=sum(counts),galois_difference_rank=rank,
                rank_budget_holds=rank<=sum(counts))
