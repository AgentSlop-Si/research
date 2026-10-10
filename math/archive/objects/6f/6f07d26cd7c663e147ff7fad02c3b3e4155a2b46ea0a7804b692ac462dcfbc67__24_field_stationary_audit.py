"""Prime-field all-basis test of the stationary full-rank Toeplitz chirp chart.

Verifies W is a Vandermonde with pairwise distinct nodes, that W*W is
Toeplitz, independent of the input block, and that q=M different slopes,
parsed through K-FFT and exact G-step Green recurrences, reproduce the
entire N-point Fourier matrix over a finite field. Basis-response caching
in this *verifier* is solely to make all-N^2 tests fast: it is NOT counted
as or claimed to be a fast runtime Fourier algorithm on fresh inputs.
"""
import json
from pathlib import Path
from field_gram_audit import primitive_root,decode_chirp_unscaled_mod,tri


def invert_matrix(A,p):
    N=len(A)
    B=[[A[i][j]%p for j in range(N)]+[int(i==j) for j in range(N)]
       for i in range(N)]
    for k in range(N):
        pivot=next((i for i in range(k,N) if B[i][k]%p),None)
        if pivot is None:raise ValueError('Singular Vandermonde')
        B[k],B[pivot]=B[pivot],B[k]
        t=pow(B[k][k],-1,p)
        B[k]=[t*z%p for z in B[k]]
        for i in range(N):
            if i==k:continue
            fac=B[i][k]
            if fac:
                B[i]=[(B[i][j]-fac*B[k][j])%p for j in range(2*N)]
    return [row[N:] for row in B]


def verify_case(N,p,M):
    G=N&-N;m=N//G;K=G//M
    assert G>=M*M and M>=2 and (p-1)%N==0
    z=primitive_root(N,p); zg=pow(z,m,p); zm=pow(z,G,p)
    zeta=zg
    exponents=[(K*tri(u)+(K+1)*u)%G for u in range(M)]
    assert len(set(exponents))==M
    assert len(set(t%K for t in exponents))==M
    W=[[pow(zeta,(-i*exponents[u])%G,p) for i in range(M)] for u in range(M)]
    wi=invert_matrix(W,p)
    for u in range(M):
        for v in range(M):
            assert sum(W[u][i]*wi[i][v] for i in range(M))%p==int(u==v)
    # Gram = W^* W under the formal involution zeta -> zeta^{-1}
    # (not the ordinary complex norm or a field automorphism of Fp).
    gram=[[sum(pow(zeta,((i-j)*exponents[u])%G,p) for u in range(M))%p
           for j in range(M)] for i in range(M)]
    for i in range(M-1):
        for j in range(M-1):
            assert gram[i][j]==gram[i+1][j+1]
    # Independent exact Green decoder impulse kernels, *verifier-only* cache.
    kernels=[]
    for s in range(m):
        all_i=[]
        for i in range(M):
            state=(1+i*K,(3*s+i*(K+1))%G)
            basis=[]
            for r in range(K):
                d=[int(z==r) for z in range(K)]
                basis.append(decode_chirp_unscaled_mod(d,G,M,state,zeta,p))
            all_i.append(basis)
        kernels.append(all_i)
    # Check N^2 Fourier entries on ALL N source basis vectors.
    matches=0
    for n in range(N):
        s=n%m
        rg=(n//m)//M
        u=(n//m)%M
        base_phase=pow(zeta,(tri(u)+(M*rg+3*s)*u)%G,p)
        coeff=[wi[i][u]*base_phase%p for i in range(M)]
        stage=[sum(coeff[i]*kernels[s][i][rg][k1] for i in range(M))%p
               for k1 in range(G)]
        for k2 in range(m):
            modm=pow(zm,(-k2*s)%m,p)
            for k1 in range(G):
                k=k1+G*k2
                val=stage[k1]*pow(z,(-k1*s)%N,p)*modm%p
                goal=pow(z,(-k*n)%N,p)
                assert val==goal,(N,p,M,n,k,val,goal)
                matches+=1
    # Wrong Toeplitz phase step in preconditioner: decoder states unchanged.
    wrong_nodes=[(K*tri(u)+K*u)%G for u in range(M)]
    wrongW=[[pow(zeta,(-i*wrong_nodes[u])%G,p) for i in range(M)] for u in range(M)]
    wrongInv=invert_matrix(wrongW,p)
    wrong_count=0
    for u in range(M):
        if any(wrongInv[i][u]!=wi[i][u] for i in range(M)):
            wrong_count+=1
    assert wrong_count>0
    return {'N':N,'prime':p,'G':G,'M':M,'odd_m':m,'exact_fourier_entries':matches,
            'stationary_gram_toeplitz_checked':True,
            'all_nodes_distinct':True,'wrong_phase_inversion_rejected':wrong_count,
            'decoder_basis_response_cache_is_verifier_only':True}


def main():
    cases=[(48,97,4),(80,641,4),(96,97,4),(192,193,8),(384,769,8)]
    results=[verify_case(*arg) for arg in cases]
    summary={'scope':'full-rank q=M stationary noncommuting Toeplitz frame: exact all-basis finite fields, no faster algorithm',
             'cases':results,
             'total_full_fourier_entries':sum(r['exact_fourier_entries'] for r in results)}
    path=Path(__file__).parent/'FIELD_STATIONARY_RESULTS.json'
    path.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'cases':[r['N'] for r in results],
                      'total_exact_Fourier_entries':summary['total_full_fourier_entries'],
                      'verified':'FULL-RANK EXACT, not sub-FFT'},indent=2))

if __name__=='__main__':main()
