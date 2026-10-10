"""Independent exact recheck via the finite geometric series, and Leibniz determinant.

No imports from verify.py. GF(65537), no floating point.
"""
import itertools, json
from pathlib import Path
P=65537
SRC=Path(__file__).with_name('RESULTS.json')

def mul(A,B):
    C=[[0]*len(B[0]) for _ in A]
    for i in range(len(A)):
        for t in range(len(B)):
            for j in range(len(B[0])):
                C[i][j]=(C[i][j]+A[i][t]*B[t][j])%P
    return C

def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def inverse_green_by_series(par):
    n=len(par['sigma']);T=[[0]*n for _ in range(n)]
    for i in range(n): T[i][par['sigma'][i]]=par['weights'][i]
    q=1
    for w in par['weights']: q=q*w%P
    assert q!=1
    cur=identity(n);total=[[0]*n for _ in range(n)]
    for _ in range(n):
        for i in range(n):
            for j in range(n):total[i][j]=(total[i][j]+cur[i][j])%P
        cur=mul(cur,T)
    assert cur==[[int(i==j)*q for j in range(n)] for i in range(n)]
    den=pow((1-q)%P,P-2,P)
    total=[[(x*den)%P for x in row] for row in total]
    return [[par['row_scale'][i]*total[par['row_perm'][i]][par['col_perm'][j]]*par['col_scale'][j]%P for j in range(n)] for i in range(n)]

def det_leibniz(A):
    n=len(A);s=0
    for order in itertools.permutations(range(n)):
        v=1
        for i,j in enumerate(order):v=v*A[i][j]%P
        inv=0
        for i in range(n):
            for j in range(i+1,n):
                if order[i]>order[j]:inv+=1
        s=(s-v if inv%2 else s+v)%P
    return s

def main():
    inp=json.load(open(SRC))
    fw=inp['four_green_witness']; n=inp['N']; w=inp['primitive_8th_root']
    assert n==8 and pow(w,8,P)==1 and pow(w,4,P)==P-1
    pars=fw['green_parameters'];assert len(pars)==2 and all(len(s)==2 for s in pars)
    a1,a2=[inverse_green_by_series(p) for p in pars[0]]
    b1,b2=[inverse_green_by_series(p) for p in pars[1]]
    A=[[(a1[i][j]+a2[i][j])%P for j in range(n)] for i in range(n)]
    B=[[(b1[i][j]+b2[i][j])%P for j in range(n)] for i in range(n)]
    assert A==fw['A'] and B==fw['B'], 'four Green branches do not reconstruct saved A/B'
    K=[[A[k][i]*(B[i][1]-pow(w,k,P)*B[i][0])%P for i in range(n)] for k in range(n)]
    val=det_leibniz(K)
    assert val!=0
    # Directly check no Fourier first-pair relation with any diagonal: det(K) nonzero.
    # Read saved test diagonal and verify it fails a Fourier phase relation.
    d=fw['d'];M=mul(mul(A,[[int(i==j)*d[i] for j in range(n)] for i in range(n)]),B)
    assert any(M[k][1]!=(pow(w,k,P)*M[k][0])%P for k in range(n))
    cert={'prime':P,'N':n,'omega':w,'four_green_reconstructed':True,
          'two_column_pencil_det_GF65537':val,
          'pencil_matrix':K,
          'certificate':'det K != 0 over GF(65537) proves no nonzero interface diagonal, for these stage parameters, can satisfy even the first two Fourier columns. The given Green parameter lifts also give a valid algebraic nonzero certificate in Q(zeta_8), by reduction modulo a prime lying above 65537.'}
    target=Path(__file__).with_name('CERTIFICATE.json');target.write_text(json.dumps(cert,indent=2))
    print(json.dumps({'four_green_reconstructed':True,'N':n,'two_column_pencil_determinant':val, 'valid_root':pow(w,4,P)==P-1}, indent=2))
if __name__=='__main__':main()
