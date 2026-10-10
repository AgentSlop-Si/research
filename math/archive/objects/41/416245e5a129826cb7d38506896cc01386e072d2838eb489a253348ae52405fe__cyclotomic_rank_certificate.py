"""Phase 30: reproducible exact-integer cyclotomic-projection rank witnesses.

For n, zeta primitive n-th root, let L be Q-linear on Q(zeta), specified
in the integral power basis (1,zeta,...,zeta^(phi(n)-1)). M[j,k]=L(zeta^(jk)).
All entries of M are exact integers. A nonzero minor after reduction modulo
998244353 certifies a characteristic-zero rank lower bound. The matching
rank upper bound n-tau(n) is established symbolically via Ramanujan sums.

The trace branch uses integer Ramanujan sum c_n(j*k) = Tr(zeta^(jk)),
which has rank tau(n) exactly by the Galois-orbit argument in THEOREM.md.
"""
from __future__ import annotations
import argparse,hashlib,json,math
import numpy as np
from sympy import Poly, Symbol, cyclotomic_poly, divisor_count, totient, mobius, divisors
P=998244353

def residues(n):
    x=Symbol('x'); phi=Poly(cyclotomic_poly(n,x),x,domain='ZZ')
    z=Poly(1,x,domain='ZZ'); xx=Poly(x,x,domain='ZZ')
    out=[]
    for k in range(n):
        out.append(tuple(int(z.nth(j)) for j in range(phi.degree())))
        z=(z*xx).rem(phi)
    return out

def rank_minor_mod(a,p=P):
    a=np.asarray(a,dtype=np.int64)%p
    m,k=a.shape
    x=a.copy()
    rowids=list(range(m)); row=0; cols=[]; rows=[]
    for col in range(k):
        if row>=m:break
        nz=np.flatnonzero(x[row:,col])
        if len(nz)==0:continue
        j=row+int(nz[0]);x[[row,j]]=x[[j,row]]
        rowids[row],rowids[j]=rowids[j],rowids[row]
        inverse=pow(int(x[row,col]),-1,p)
        x[row,col:]=(x[row,col:]*inverse)%p
        rr=np.flatnonzero(x[row+1:,col])+row+1
        if len(rr):x[rr,col:]=(x[rr,col:]-x[rr,col,None]*x[row,col:])%p
        cols.append(col);rows.append(rowids[row]);row+=1
    return row,rows,cols

def det_mod(a,p=P):
    m=np.asarray(a,dtype=np.int64).copy()%p
    n=m.shape[0]; val=1
    for i in range(n):
        nz=np.flatnonzero(m[i:,i])
        if len(nz)==0:return 0
        j=i+int(nz[0]);
        if j!=i:
            m[[i,j]]=m[[j,i]]
            val=(-val)%p
        u=int(m[i,i]);val=(val*u)%p
        inv=pow(u,-1,p)
        rr=np.flatnonzero(m[i+1:,i])+i+1
        if len(rr):
            coefficients=(m[rr,i]*inv)%p
            m[rr,i:]=(m[rr,i:]-coefficients[:,None]*m[i,i:])%p
    return int(val)

def ramanujan(n,k):
    # c_n(k) = sum_{d|gcd(n,k)} d*mu(n/d) is an exact integer.
    return sum(int(d*mobius(n//d)) for d in divisors(math.gcd(n,k)))

def result(n,with_det=True):
    rs=residues(n);degree=len(rs[0]);t=int(divisor_count(n))
    lam0=[0]+list(range(1,degree))
    lamgen=[1]+list(range(1,degree))
    records={}
    for name,lam in [('traceless',lam0),('unrestricted',lamgen)]:
        samples=[sum(a*b for a,b in zip(lam,r))%P for r in rs]
        A=np.fromfunction(lambda j,k: 0,(1,1)) # avoid vectorized overflow
        A=np.array([[samples[(j*k)%n] for k in range(n)] for j in range(n)],dtype=np.int64)
        rank,rows,cols=rank_minor_mod(A)
        det=det_mod(A[np.ix_(rows,cols)]) if with_det and rank else (1 if rank==0 else None)
        records[name]={'basis_functional':lam, 'rank_mod_p':rank,
                       'minor_determinant_mod_p':det,
                       'pivot_rows_sha256':hashlib.sha256(json.dumps(rows).encode()).hexdigest(),
                       'pivot_columns_sha256':hashlib.sha256(json.dumps(cols).encode()).hexdigest()}
        if name=='traceless':
            assert rank==n-t,(n,'traceless',rank,n-t)
            assert lam[0]==0
            # The gcd-orbit indicators are exact kernel vectors for all L(1)=0.
            for d in divisors(n):
                for j in range(n):
                    assert sum(samples[(j*k)%n] for k in range(n) if math.gcd(k,n)==d)%P==0,(n,d,j)
        else:assert rank==n,(n,'unrestricted',rank)
        assert det is None or det%P !=0,(name,det)
    trace_vals=[ramanujan(n,k)%P for k in range(n)]
    A=np.array([[trace_vals[(j*k)%n] for k in range(n)] for j in range(n)],dtype=np.int64)
    rank,rows,cols=rank_minor_mod(A)
    det=det_mod(A[np.ix_(rows,cols)]) if with_det and rank else (1 if rank==0 else None)
    assert rank==t,(n,rank,t)
    assert det is None or det%P!=0
    records['trace']={'rank_mod_p':rank, 'minor_determinant_mod_p':det,
                      'pivot_rows_sha256':hashlib.sha256(json.dumps(rows).encode()).hexdigest(),
                      'pivot_columns_sha256':hashlib.sha256(json.dumps(cols).encode()).hexdigest()}
    return {'n':n,'degree_Q_zeta':degree,'divisor_count':t,'traceless_expected':n-t,
            'field_prime':P,'witnesses':records}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--n',nargs='*',type=int)
    parser.add_argument('--output',type=str)
    args=parser.parse_args()
    ns=args.n or [1,2,3,4,5,6,8,9,10,12,15,16,20,24,30,32,48,60,64,96,120,240]
    data={'scheme':'exact-integer matrices with mod-p nonzero determinant rank witnesses',
          'theorem':'trace=tau(n); traceless generic=n-tau(n); full functional generic=n',
          'fields':[P],'results':[]}
    for n in ns:
        r=result(n)
        data['results'].append(r)
        print('n',n,'phi',r['degree_Q_zeta'],'tau',r['divisor_count'],
              'ranks',(r['witnesses']['trace']['rank_mod_p'],r['witnesses']['traceless']['rank_mod_p'],r['witnesses']['unrestricted']['rank_mod_p']),flush=True)
    if args.output:
        with open(args.output,'w') as f:json.dump(data,f,indent=2)
    return data

if __name__=='__main__':main()
