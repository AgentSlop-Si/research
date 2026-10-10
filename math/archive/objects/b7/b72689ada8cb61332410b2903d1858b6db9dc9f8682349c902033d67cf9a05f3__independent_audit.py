"""Independent Phase 17 audit: independently evaluate support cuts, finite-field
Vandermonde minors, matrix ranks and Green/feedback residuals. No NumPy FFT.
The audit is a verification of stated restricted identities, not a speed claim
for an arbitrary-input full Fourier transform.
"""
from __future__ import annotations
import json,itertools,random,sys,os
from pathlib import Path
from phase17 import (nth_root, graph_certificate,local_band_certificate,
    MagneticGreenPlan,RankOneFeedbackPlan,FieldCount,mixed_feedback_residual,
    mixed_green_denominator,covariance_defect_rank_via_denominator)

HERE=Path(__file__).resolve().parent

# Deliberately distinct rank elimination from the production implementation.
def ref_rank(M,p):
    if not M:return 0
    A=[x.copy() for x in M]; r=0
    for j in range(len(A[0])):
        pivot=-1
        for i in range(r,len(A)):
            if A[i][j]%p:pivot=i;break
        if pivot<0:continue
        A[r],A[pivot]=A[pivot],A[r]
        v=pow(A[r][j],-1,p)
        for k in range(j,len(A[0])):A[r][k]=(A[r][k]*v)%p
        for i in range(len(A)):
            if i==r:continue
            f=A[i][j]%p
            if f:
                for k in range(j,len(A[0])):A[i][k]=(A[i][k]-f*A[r][k])%p
        r+=1
        if r==len(A):break
    return r


def direct_fourier(n,p,w):
    return [[pow(w,(-i*j)%n,p) for j in range(n)] for i in range(n)]


def matmul(A,B,p):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p
            for j in range(len(B[0]))] for i in range(len(A))]


def manual_support_cert(P,Q,cert,w,p):
    n=len(P);I=cert['rows'];B=cert['columns'];J=cert['neighbors']
    assert len(B)==cert['bound']
    assert len(I)>=len(J)
    assert len(I)==len(set(I))
    assert all(I[i]==(I[0]+i)%n for i in range(len(I)))
    assert all(all(P[i][j]%p==0 for i in I) for j in B)
    assert sorted({i for j in B for i in range(n) if Q[i][j]%p})==J
    assert ref_rank([[pow(w,(-i*j)%n,p) for j in J] for i in I],p)==len(J)


def sparse_random(n,t,p,rng):
    A=[[0]*n for _ in range(n)]
    for j in range(n):
        for i in rng.sample(range(n),rng.randrange(1,t+1)):
            A[i][j]=rng.randrange(1,p)
    return A


def choose_green_params(n,p):
    for alpha in range(1,min(p,15)):
        for beta in range(1,min(p,15)):
            if pow(beta,n,p)!=1 and (1-pow(alpha,n,p)-pow(beta,n,p))%p:
                return alpha,beta
    raise AssertionError('no admissible parameters in candidate range')


def reference_solve(Q,b,p):
    A=[[(q%p) for q in row]+[b[i]%p] for i,row in enumerate(Q)]
    n=len(A)
    for j in range(n):
        i=next((i for i in range(j,n) if A[i][j]%p),None)
        if i is None:raise ValueError('singular')
        A[j],A[i]=A[i],A[j]
        inv=pow(A[j][j],-1,p)
        A[j]=[(x*inv)%p for x in A[j]]
        for i in range(n):
            if i==j:continue
            v=A[i][j]
            if v:A[i]=[(x-v*y)%p for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]


def main():
    rng=random.Random(2026101017)
    out={'project':'Hero #17 Phase 17','method':'Independent finite-prime-field exact arithmetic',
         'source':'Executable recurrence / graph certificates; no universal FFT speedup',
         'exhaustive_permutation_pair_cases':0,'irregular_graph_certificate_cases':0,
         'local_band_certificate_cases':0,'vandermonde_minor_checks':0,
         'arbitrary_endpoint_permutation_certificates':0,
         'exhaustive_magnetic_parameter_cases':0,
         'feedback_dense_reference_solves':0,'feedback_exact_vector_residuals':0,
         'covariance_defect_rank_cases':0,'full_fourier_intertwining_checks':0,
         'large_executions':[],'field_defect_distributions':{}}
    # Exhaust all permutation support pairs (n=4,5); no field values are used
    # in the support selection, so the theorem covers any nonzero weights.
    for n,p in [(4,17),(5,31)]:
        w=nth_root(n,p)
        for ap in itertools.permutations(range(n)):
            P=[[int(i==ap[j]) for j in range(n)] for i in range(n)]
            for aq in itertools.permutations(range(n)):
                Q=[[int(i==aq[j]) for j in range(n)] for i in range(n)]
                cert=graph_certificate(P,Q,1,1)
                manual_support_cert(P,Q,cert,w,p)
                out['exhaustive_permutation_pair_cases']+=1
                out['vandermonde_minor_checks']+=1
    print('PASS exhaustive permutation-support certificates',out['exhaustive_permutation_pair_cases'])
    # Random arbitrary long-range support, no band restrictions.
    for n,p,t,s in [(9,19,2,2),(16,17,3,3),(17,103,2,3),(24,73,3,3),(31,311,3,2),(64,257,3,3)]:
        w=nth_root(n,p)
        for _ in range(30):
            P=sparse_random(n,t,p,rng)
            Q=sparse_random(n,s,p,rng)
            cert=graph_certificate(P,Q,t,s)
            manual_support_cert(P,Q,cert,w,p)
            assert cert['bound']==n//(1+s*t)
            out['irregular_graph_certificate_cases']+=1
            out['vandermonde_minor_checks']+=1
    print('PASS arbitrary sparse-graph cuts',out['irregular_graph_certificate_cases'])
    for n,p in [(16,17),(17,103),(24,73),(31,311),(32,97),(64,257)]:
        w=nth_root(n,p)
        for a,b in [(0,0),(1,0),(0,1),(1,2),(2,2),(3,3),(4,2)]:
            cert=local_band_certificate(n,a,b)
            assert cert['bound']==max(0,n//2-a-b)
            if cert['bound']:
                P=[[int(min((i-j)%n,(j-i)%n)<=a) for j in range(n)] for i in range(n)]
                Q=[[int(min((i-j)%n,(j-i)%n)<=b) for j in range(n)] for i in range(n)]
                manual_support_cert(P,Q,cert,w,p)
                out['vandermonde_minor_checks']+=1
            out['local_band_certificate_cases']+=1
    print('PASS stronger banded cut theorem',out['local_band_certificate_cases'])
    # Independently permute both Fourier endpoints: the Vandermonde gate must
    # remain valid because rows are selected consecutive in frequency order.
    for n,p,t,s in [(16,17,2,2),(17,103,3,2),(24,73,3,3),(31,311,3,3)]:
        w=nth_root(n,p)
        for _ in range(25):
            P=sparse_random(n,t,p,rng);Q=sparse_random(n,s,p,rng)
            row_order=rng.sample(range(n),n)
            input_order=rng.sample(range(n),n)
            phys_to_frequency=[0]*n
            for freq,physical in enumerate(row_order):phys_to_frequency[physical]=freq
            cert=graph_certificate(P,Q,t,s,row_order=row_order)
            I=cert['rows'];J=cert['neighbors']
            assert len(I)>=len(J)
            assert all(P[i][j]==0 for i in I for j in cert['columns'])
            assert ref_rank([[pow(w,(-phys_to_frequency[i]*input_order[j])%n,p)
                                for j in J] for i in I],p)==len(J)
            out['arbitrary_endpoint_permutation_certificates']+=1
            out['vandermonde_minor_checks']+=1
    print('PASS arbitrary Fourier endpoint permutation cuts',out['arbitrary_endpoint_permutation_certificates'])
    # Prove the production Green evaluator matches independent dense
    # Gaussian elimination for all basis directions, then random feedback.
    for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(11,23),(17,103),(24,73)]:
        w=nth_root(n,p)
        alpha,beta=choose_green_params(n,p)
        green=MagneticGreenPlan(n,p,w,alpha,beta)
        Q=mixed_green_denominator(n,p,w,alpha,beta)
        for _ in range(4):
            x=[rng.randrange(p) for _ in range(n)]
            a=green.solve(x)
            b=reference_solve(Q,x,p)
            assert a==b
            out['feedback_dense_reference_solves']+=1
            for _ in range(3):
                u=[rng.randrange(p) for _ in range(n)]
                v=[rng.randrange(p) for _ in range(n)]
                try:f=RankOneFeedbackPlan(green,u,v)
                except ZeroDivisionError:continue
                y=f.solve(x)
                R=[[((Q[i][j]+u[i]*v[j])%p) for j in range(n)] for i in range(n)]
                yy=reference_solve(R,x,p)
                assert y==yy
                assert not any(mixed_feedback_residual(y,x,n,p,w,alpha,beta,u,v))
                out['feedback_dense_reference_solves']+=1
                out['feedback_exact_vector_residuals']+=1
    print('PASS independent Gaussian Green/feedback solves',out['feedback_dense_reference_solves'])
    for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(11,23),(12,37),(16,17),(17,103),(24,73),(32,97)]:
        w=nth_root(n,p)
        F=direct_fourier(n,p,w)
        assert all(F[i][(j+1)%n]==(pow(w,-i%n,p)*F[i][j])%p
                   for i in range(n) for j in range(n))
        out['full_fourier_intertwining_checks']+=n*n
        ranks={}
        for alpha,beta in [(1,1),(2,3),(3,5),(1,0),(0,1),(5,7),(1,2),(2,1)]:
            Q=mixed_green_denominator(n,p,w,alpha,beta)
            if ref_rank(Q,p)<n:continue
            # Independent construction of B = S Q - Q T^-1.
            B=[[(Q[(i-1)%n][j]-Q[i][j]*pow(w,-j%n,p))%p for j in range(n)]
               for i in range(n)]
            k=ref_rank(B,p)
            assert k==covariance_defect_rank_via_denominator(Q,p,w)
            assert k>=n-2
            if alpha==0:assert k>=n-1
            ranks[str(k)]=ranks.get(str(k),0)+1
            out['covariance_defect_rank_cases']+=1
        out['field_defect_distributions'][str(n)]={'modulus':p,'ranks':ranks}
    print('PASS covariance defect rank and Fourier identity',out['covariance_defect_rank_cases'])
    for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(12,37),(16,17)]:
        w=nth_root(n,p)
        histogram={}
        for alpha in range(1,p):
            for beta in range(1,p):
                if (1-pow(alpha,n,p)-pow(beta,n,p))%p==0:continue
                Q=mixed_green_denominator(n,p,w,alpha,beta)
                B=[[(Q[(i-1)%n][j]-Q[i][j]*pow(w,-j%n,p))%p for j in range(n)]
                   for i in range(n)]
                k=ref_rank(B,p)
                assert k>=n-2
                histogram[str(k)]=histogram.get(str(k),0)+1
                out['exhaustive_magnetic_parameter_cases']+=1
        out['field_defect_distributions'][str(n)]['exhaustive_nonzero_parameter_rank_histogram']=histogram
    print('PASS exhaustive magnetic-parameter defect ranks',out['exhaustive_magnetic_parameter_cases'])

    # Charge the complete execution of the O(N) *Green* operator, not the DFT.
    p=2013265921
    for n in (256,1024,4096,65536):
        w=nth_root(n,p)
        c=FieldCount()
        alpha,beta=2,3
        G=MagneticGreenPlan(n,p,w,alpha,beta,c)
        init=c.report().copy()
        x=[rng.randrange(p) for _ in range(n)]
        u=[(j*71+13)%p for j in range(n)]
        v=[(j*53+19)%p for j in range(n)]
        plan=RankOneFeedbackPlan(G,u,v,c)
        prep=c.report().copy()
        y=plan.solve(x,c)
        total=c.report().copy()
        assert all(z==0 for z in mixed_feedback_residual(y,x,n,p,w,alpha,beta,u,v))
        out['feedback_exact_vector_residuals']+=1
        run={key:total[key]-prep[key] for key in ('add_sub','multiply','invert','total_field_ops')}
        out['large_executions'].append({'n':n,'field':p,
            'green_preparation':init,'feedback_preparation_cumulative':prep,
            'feedback_online':run,'total_preparation_plus_one_online':total,
            'all_output_residuals_zero':True})
    print('PASS large fully charged Green feedback executions',[(x['n'],x['feedback_online']['total_field_ops']) for x in out['large_executions']])
    path=HERE/'AUDIT_RESULTS.json'
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('Wrote',path)
    return out

if __name__=='__main__':main()
