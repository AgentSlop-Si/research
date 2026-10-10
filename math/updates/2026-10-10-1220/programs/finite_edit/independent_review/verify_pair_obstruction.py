#!/usr/bin/env python3
"""Independent reviewer implementation. No author/source module imported or executed.

Uses cycle-orbit geometric sums rather than author dense inversion. Coefficient
sign convention is the negative of the author's row convention, so 4x4
minor determinants agree while entire minor matrices are entrywise negatives.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, itertools, json, math
import numpy as np

P=65537
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def maps(n):
    s=math.isqrt(n); assert s*s==n
    return [np.array([((x+2*y+d)%s)*s+y for x in range(s) for y in range(s)],dtype=np.int64) for d in (0,1)] + [np.array([x*s+(y+2*x+d)%s for x in range(s) for y in range(s)],dtype=np.int64) for d in (0,1)]


def orbits(q):
    unvisited=set(range(len(q))); ans=[]
    while unvisited:
        start=min(unvisited); cyc=[]; i=start
        while i not in cyc:
            cyc.append(i); unvisited.remove(i); i=int(q[i])
        assert i==start
        ans.append(cyc)
    return ans


def denominators(q,w):
    return [1-math.prod(int(w[i]) for i in cyc) for cyc in orbits(q)]


def green(q,w):
    n=len(q); g=np.zeros((n,n),dtype=np.int64)
    for cyc in orbits(q):
        den=(1-math.prod(int(w[k]) for k in cyc))%P
        if den==0: raise ValueError('Singular Green factor')
        for i in cyc:
            j=i; coeff=pow(den,-1,P)
            for _ in cyc:
                g[i,j]=coeff
                coeff=coeff*int(w[j])%P; j=int(q[j])
            assert j==i
    pencil=np.eye(n,dtype=np.int64)
    pencil[np.arange(n),q]-=w
    assert np.array_equal(mul(pencil%P,g),np.eye(n,dtype=np.int64))
    assert np.array_equal(mul(g,pencil%P),np.eye(n,dtype=np.int64))
    return g


def mul(a,b):
    # n<=256 and each input residue <65537; sums fit signed int64.
    return (np.asarray(a,dtype=np.int64)%P @ (np.asarray(b,dtype=np.int64)%P))%P


def rank(m):
    m=np.array(m,dtype=np.int64,copy=True)%P; rows,cols=m.shape; r=0
    for c in range(cols):
        pivot=next((j for j in range(r,rows) if m[j,c]),None)
        if pivot is None: continue
        m[[r,pivot]]=m[[pivot,r]]
        m[r]=m[r]*pow(int(m[r,c]),-1,P)%P
        for j in range(r+1,rows):
            m[j]=(m[j]-int(m[j,c])*m[r])%P
        r+=1
        if r==rows: break
    return r


def determinant4(m):
    # Leibniz expansion is deliberately independent of rank elimination.
    ret=0
    for p in itertools.permutations(range(4)):
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        ret+=(-1 if inversions%2 else 1)*math.prod(int(m[i,p[i]]) for i in range(4))
    return ret%P


def pin(n):
    ps=maps(n); rng=np.random.default_rng(19); weights=[]; greens=[]; denom=[]
    for stage in range(2):
        ws=[]; gs=[]; ds=[]
        for q in ps:
            while True:
                w=rng.integers(2,1024,n,dtype=np.int64)
                d=denominators(q,w)
                if all(t%P for t in d): break
            ws.append(w); gs.append(green(q,w)); ds.append(d)
        weights.append(ws); greens.append(gs); denom.append(ds)
    a=pow(4,-1,P)
    A=a*(greens[1][0]+greens[1][1]+greens[1][2])%P
    B=a*(greens[0][0]+greens[0][2]+greens[0][3])%P
    return ps,weights,greens,denom,A,B


def coeffs(F,A,B,qh,qv):
    n=len(F); alpha=pow(4,-1,P); I=np.eye(n,dtype=np.int64)
    ph=I[qh]; pv=I[qv]
    X=(F-mul(A,B))%P
    R=mul(X-alpha*A-alpha*B-(alpha*alpha%P)*I,ph.T)
    U=mul(mul(pv,X-alpha*A),ph.T)
    W=(X-alpha*B)%P
    Z=mul(pv,X)
    return R,U,W,Z


def resultant_rows(c,i,k):
    r,u,w,z=c
    return np.array([[int(r[i,j])*int(w[k,j])-int(r[k,j])*int(w[i,j]),
                      -int(u[i,j])*int(w[k,j])+int(r[k,j])*int(z[i,j]),
                      -int(r[i,j])*int(z[k,j])+int(u[k,j])*int(w[i,j]),
                      int(u[i,j])*int(z[k,j])-int(u[k,j])*int(z[i,j])]
                     for j in range(len(r))],dtype=np.int64)%P


def test_control(n,kind):
    ps,weights,gs,ds,A,B=pin(n); qh,qv=ps[1],ps[3]
    # Reviewer's deterministic choices, distinct from submitted controls.
    h=np.array([2+(7*j+3)%41 for j in range(n)],dtype=np.int64)
    v=np.array([2+(11*j+5)%43 for j in range(n)],dtype=np.int64)
    if kind in ('zero_horizontal','both_zero'): h[:]=0
    if kind in ('zero_vertical','both_zero'): v[:]=0
    if kind=='sparse':
        h[::2]=0; v[1::2]=0
    # No random retry may hide singular cases: deterministic controls must pass.
    H=green(qh,h); V=green(qv,v); a=pow(4,-1,P)
    F=mul(A+a*V,B+a*H)
    R,U,W,Z=coeffs(F,A,B,qh,qv)
    equations=(R-v[:,None]*U-W*h[None,:]+(v[:,None]*h[None,:]%P)*Z)%P
    assert not np.any(equations)
    I=np.eye(n,dtype=np.int64); Sv=(I-v[:,None]*I[qv])%P; Sh=(I-h[:,None]*I[qh])%P
    assert np.array_equal(mul(mul(Sv,F),Sh),mul(mul(Sv,A)+a*I,mul(B,Sh)+a*I))
    maxrank=0; count=0
    for i in range(n):
        for k in range(i+1,n):
            rows=resultant_rows((R,U,W,Z),i,k)
            kernel=np.array([1,v[i],v[k],int(v[i])*int(v[k])%P],dtype=np.int64)
            assert not np.any(mul(rows,kernel))
            rr=rank(rows); assert rr<=3
            maxrank=max(maxrank,rr); count+=1
    bridge=mul(mul(I[qv],gs[1][3]),H)
    return dict(N=n,kind=kind,selected_horizontal_zero_count=int(np.sum(h==0)),
                selected_vertical_zero_count=int(np.sum(v==0)),
                old_vertical_new_horizontal_bridge_zero_count=int(np.sum(bridge==0)),
                full_matrix_equality_constructed=True,two_sided_pencil_identity=True,
                all_bilinear_equations_zero=True,all_row_pairs_checked=count,
                all_row_pair_kernel_identities_pass=True,maximum_row_pair_rank=maxrank)


# Exact rational complex arithmetic in Q(i) for an extra characteristic-zero N=4 check.
def ca(a,b): return (a[0]+b[0],a[1]+b[1])
def cn(a): return (-a[0],-a[1])
def cm(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cs(a,b): return ca(a,cn(b))
def cq(x): return (Q(x),Q(0))
def matrix_product(a,b): return [[sum_pairs(cm(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def sum_pairs(it):
    ans=cq(0)
    for item in it: ans=ca(ans,item)
    return ans

def exact_four(weights):
    n=4; ps=maps(4); gs=[]
    for layer in range(2):
        local=[]
        for term,q in enumerate(ps):
            g=[[cq(0) for _ in range(n)] for _ in range(n)]
            w=weights[layer][term]
            for cyc in orbits(q):
                den=1-math.prod(int(w[j]) for j in cyc)
                for i in cyc:
                    j=i; prod=1
                    for _ in cyc:
                        g[i][j]=cq(Q(prod,den)); prod*=int(w[j]);j=int(q[j])
            local.append(g)
        gs.append(local)
    A=[[cm(cq(Q(1,4)),sum_pairs(gs[1][t][i][j] for t in [0,1,2])) for j in range(n)] for i in range(n)]
    B=[[cm(cq(Q(1,4)),sum_pairs(gs[0][t][i][j] for t in [0,2,3])) for j in range(n)] for i in range(n)]
    phases=[cq(1),(Q(0),Q(1)),cq(-1),(Q(0),Q(-1))]
    F=[[phases[i*j%4] for j in range(n)] for i in range(n)]
    AB=matrix_product(A,B);X=[[cs(F[i][j],AB[i][j]) for j in range(n)] for i in range(n)]
    # Explicit right Q_H^{-1}: column j equals old column q_H[j].
    qh,qv=ps[1],ps[3]; a=cq(Q(1,4));aa=cq(Q(1,16))
    R=[[cs(cs(cs(X[i][int(qh[j])],cm(a,A[i][int(qh[j])])),cm(a,B[i][int(qh[j])])),aa if i==int(qh[j]) else cq(0)) for j in range(n)] for i in range(n)]
    U=[[cs(X[int(qv[i])][int(qh[j])],cm(a,A[int(qv[i])][int(qh[j])])) for j in range(n)] for i in range(n)]
    W=[[cs(X[i][j],cm(a,B[i][j])) for j in range(n)] for i in range(n)]
    Z=[[X[int(qv[i])][j] for j in range(n)] for i in range(n)]
    i,k=0,1
    m=[[cs(cm(R[i][j],W[k][j]),cm(R[k][j],W[i][j])),
        ca(cn(cm(U[i][j],W[k][j])),cm(R[k][j],Z[i][j])),
        ca(cn(cm(R[i][j],Z[k][j])),cm(U[k][j],W[i][j])),
        cs(cm(U[i][j],Z[k][j]),cm(U[k][j],Z[i][j]))] for j in range(n)]
    det=cq(0)
    for p in itertools.permutations(range(4)):
        prod=cq(1)
        for i in range(4): prod=cm(prod,m[i][p[i]])
        inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        det=ca(det,cn(prod) if inv%2 else prod)
    assert det!=cq(0)
    def reduce_q(q):
        assert q.denominator%P
        return q.numerator*pow(q.denominator,-1,P)%P
    omega=pow(3,(P-1)//4,P)
    reduced=(reduce_q(det[0])+omega*reduce_q(det[1]))%P
    assert reduced==27524
    return dict(field='Q(i)',real_numerator=str(det[0].numerator),real_denominator=str(det[0].denominator),
                imaginary_numerator=str(det[1].numerator),imaginary_denominator=str(det[1].denominator),
                exact_nonzero=True,reduction_at_i_equals_omega=reduced,omega=omega)


def main():
    submitted=json.loads((ROOT/'FRESH_PAIR_OBSTRUCTION_RESULTS.json').read_text())
    answers=[]; all_denoms=[]; n4_weights=None
    for n,claimed in zip([4,16,64,256],submitted['fourier_certificates']):
        ps,weights,gs,ds,A,B=pin(n)
        if n==4:n4_weights=weights
        assert [[w.tolist() for w in layer] for layer in weights]==claimed['integer_weight_arrays']
        omega=pow(3,(P-1)//n,P)
        assert pow(omega,n,P)==1 and pow(omega,n//2,P)==P-1
        F=np.array([[pow(omega,i*j,P) for j in range(n)] for i in range(n)],dtype=np.int64)
        allrows=resultant_rows(coeffs(F,A,B,ps[1],ps[3]),0,1)
        minor=allrows[:4];det=determinant4(minor)
        assert det==claimed['certificate']['determinant_mod_p']
        assert np.array_equal(minor,(-np.array(claimed['certificate']['minor_matrix'],dtype=np.int64))%P)
        assert det!=0 and rank(minor)==4
        frozen=[ds[stage][term] for stage in range(2) for term in range(4) if (stage,term) not in [(0,1),(1,3)]]
        assert all(d!=0 and d%P for block in frozen for d in block)
        item=dict(N=n,omega=omega,primitive_root_checked=True,weights_match_explicit_arrays=True,
                  row_pair=[0,1],target_columns=[0,1,2,3],reviewer_signed_minor=minor.tolist(),
                  determinant_mod_65537=det,rank=4,author_signed_minor_is_negative=True,
                  frozen_cycle_denominator_count=sum(len(block) for block in frozen),
                  all_frozen_denominators_nonzero_over_Q_and_mod_p=True,
                  all_green_two_sided_inverse_checks_pass=True)
        answers.append(item);print(json.dumps(item),flush=True)
        all_denoms.append(dict(N=n,all_eight_term_cycle_denominators=[[[str(d) for d in block] for block in layer] for layer in ds]))
    controls=[]
    for n in [4,16,64]:
        for kind in ['dense','zero_horizontal','zero_vertical','both_zero','sparse']:
            c=test_control(n,kind); controls.append(c);print(json.dumps(c),flush=True)
    exact=exact_four(n4_weights);print(json.dumps(exact),flush=True)
    result=dict(prime=P,input_results_sha256=hashlib.sha256((ROOT/'FRESH_PAIR_OBSTRUCTION_RESULTS.json').read_bytes()).hexdigest(),
                source_or_author_programs_executed_or_imported=False,
                green_construction='Cycle-orbit geometric sum; both inverse identities checked',
                determinant_construction='Independent 24-term Leibniz expansion',
                coefficient_convention='Negative of author resultant rows; same 4x4 determinant',
                fourier_certificates=answers,reachable_controls=controls,exact_N4_cyclotomic_check=exact,
                denominator_audit=all_denoms)
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
