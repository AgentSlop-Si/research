"""All-basis finite-field F_N audit of *nonstationary* full-rank chirp frames.

Unlike stationary Phase14, W_r varies with the input block. Verifies each
V_{r}=D_r W_r, exact W_r inverse, q=M complete cyclic Green decoders,
odd-factor Cooley-Tukey fusion, and all N^2 direct Fourier entries.
Decoder impulse caching is used ONLY by the verifier, not counted as an
actual fresh-input FFT algorithm. The literal runtime still uses M scans.
"""
import sys,json
from pathlib import Path
from field_gram_audit import primitive_root,tri,decode_chirp_unscaled_mod
from field_stationary_audit import invert_matrix
from slope_tradeoff import triangular_nodes


def verify_case(N,p,M,d):
    G=N&-N;m=N//G;K=G//M;L=K//d
    assert G>=M*M and d<K and (p-1)%N==0
    z=primitive_root(N,p)
    zg=pow(z,m,p);zm=pow(z,G,p)
    nodes=[[triangular_nodes(M,K,d,r)[u] for u in range(M)] for r in range(K)]
    # The actual exponents modulo G are d times nodes modulo LM=G/d.
    WI=[]
    for r in range(K):
        W=[[pow(zg,(-d*i*nodes[r][u])%G,p) for i in range(M)] for u in range(M)]
        invW=invert_matrix(W,p)
        for u in range(M):
            for v in range(M):
                assert sum(W[u][i]*invW[i][v] for i in range(M))%p==int(u==v)
        WI.append(invW)
    assert nodes[0]!=nodes[1]
    # Build the complete signed chirp decoder response for each basis stream.
    # This is verifier-only caching of known impulse responses.
    kernels=[]
    for s in range(m):
        by_i=[]
        for i in range(M):
            state=(1+d*i,(3*s+d*i)%G)
            by_r=[]
            for r in range(K):
                unit=[int(t==r) for t in range(K)]
                by_r.append(decode_chirp_unscaled_mod(unit,G,M,state,zg,p))
            by_i.append(by_r)
        kernels.append(by_i)
    count=0;drop_mismatch=0
    for n in range(N):
        s=n%m;r=(n//m)//M;u=(n//m)%M
        dinv=pow(zg,(tri(u)+(M*r+3*s)*u)%G,p)
        c=[WI[r][i][u]*dinv%p for i in range(M)]
        stage=[sum(c[i]*kernels[s][i][r][k1] for i in range(M))%p
               for k1 in range(G)]
        # Dropping the last chirp channel cannot preserve all basis columns.
        drop=[sum(c[i]*kernels[s][i][r][k1] for i in range(M-1))%p
              for k1 in range(G)]
        if stage!=drop:drop_mismatch+=1
        for k2 in range(m):
            odd=pow(zm,(-k2*s)%m,p)
            for k1 in range(G):
                k=k1+G*k2
                got=stage[k1]*pow(z,(-k1*s)%N,p)*odd%p
                expected=pow(z,(-k*n)%N,p)
                assert got==expected,(N,p,M,d,n,k,got,expected)
                count+=1
    assert drop_mismatch>0
    return {'N':N,'p':p,'M':M,'d':d,'L':L,'G':G,
            'all_basis_exact_fourier_entries':count,
            'all_blocks_invertible':True,
            'dropped_channel_basis_failures':drop_mismatch,
            'full_length_DFT_used_in_verifier':False,
            'complete_chirp_decoder_cached_in_verifier_only':True}


def main():
    cases=[(48,97,4,2),(80,641,4,2),(96,97,4,2),
           (192,193,8,2),(384,769,8,2),(384,769,8,4)]
    rows=[verify_case(*c) for c in cases]
    data={'scope':'exact all-basis verification of genuinely block-dependent W_r; does not imply a faster arbitrary-input FFT',
          'cases':rows,'exact_matrix_entries':sum(r['all_basis_exact_fourier_entries'] for r in rows),
          'not_a_sub_nlogn_FFT':True}
    (Path(__file__).parent/'FIELD_SLOPE_RESULTS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'cases':[(c['N'],c['d']) for c in rows],
                      'exact_matrix_entries':data['exact_matrix_entries'],
                      'mutation_count':[c['dropped_channel_basis_failures'] for c in rows]},indent=2))

if __name__=='__main__':main()
