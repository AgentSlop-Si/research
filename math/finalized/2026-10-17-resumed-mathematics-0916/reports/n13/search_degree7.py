#!/usr/bin/env python3
"""Fresh exact census of a declared symmetric prime-parameter N13 family.

No historical checker or discovery program is imported. Python stdlib only.
"""
import json
from pathlib import Path
from collections import Counter

P=53
Q=16
ROOT=Path(__file__).resolve().parent

def trim(a):
    a=[x%P for x in a]
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def sub(a,b):
    return trim([(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%P
    return trim(c)

def mod(a,b):
    a=trim(a[:]); b=trim(b[:]); inv=pow(b[-1],-1,P)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b); c=a[-1]*inv%P
        for j,x in enumerate(b): a[k+j]=(a[k+j]-c*x)%P
        a=trim(a)
    return a

def gcd(a,b):
    while b!=[0]: a,b=b,mod(a,b)
    return trim([x*pow(a[-1],-1,P) for x in a])

def power(a,n,h):
    out=[1]
    while n:
        if n&1: out=mod(mul(out,a),h)
        n//=2
        if n: a=mod(mul(a,a),h)
    return out

def solve(A,b):
    M=[[x%P for x in row]+[v%P] for row,v in zip(A,b)]
    nr=len(M); nc=len(A[0]); piv=[]; row=0
    for col in range(nc):
        where=next((i for i in range(row,nr) if M[i][col]),None)
        if where is None: continue
        M[row],M[where]=M[where],M[row]
        z=pow(M[row][col],-1,P); M[row]=[x*z%P for x in M[row]]
        for i in range(nr):
            if i!=row and M[i][col]:
                z=M[i][col]; M[i]=[(x-z*y)%P for x,y in zip(M[i],M[row])]
        piv.append(col); row+=1
        if row==nr: break
    if any(not any(r[:nc]) and r[nc] for r in M): return None,len(piv)
    out=[0]*nc
    for i,j in enumerate(piv): out[j]=M[i][-1]
    assert all(sum(x*y for x,y in zip(a,out))%P==v%P for a,v in zip(A,b))
    return out,len(piv)

def gauss(e,d,a,b):
    r=e*a%13; ell=d*b%13
    if r+ell>=13: return 0
    w=pow(Q,e*d%13,P); val=1
    for i in range(1,ell+1):
        val=val*(1-pow(w,r+i,P))*pow((1-pow(w,i,P))%P,-1,P)%P
    return val

G={(e,d,a,b):gauss(e,d,a,b) for e in (1,-1) for d in (1,-1) for a in range(13) for b in range(13)}
def target(a,b): return pow(Q,10*(a+b)**2%13,P)

def moment(y,a,b):
    return (target(a,b)-pow(y,13-a-b,P)*G[-1,1,a,b]*pow(G[-1,1,13-b,b],-1,P))*pow(G[1,1,a,b],-1,P)%P

def family(y):
    rows=[[moment(y,a+j,b) for j in range(8)] for b,a in [(1,1),(1,2),(1,3),(1,4),(2,2),(2,3)]]
    h0,r=solve([r[:6] for r in rows],[-r[7] for r in rows]); assert r==6
    h1,r=solve([r[:6] for r in rows],[-r[6] for r in rows]); assert r==6
    return h0+[0],h1+[1]

def sector3_gate(h,y,z):
    U={a:moment(y,a,3) for a in range(1,10)}
    V={a:pow(z,a,P)*G[1,-1,a,3]*pow(G[1,1,a,3],-1,P)%P for a in range(1,10)}
    E=[sum(h[j]*U[s+j] for j in range(8))%P for s in (1,2)]
    F=[sum(h[j]*V[s+j] for j in range(8))%P for s in (1,2)]
    return E[0]*F[1]%P==E[1]*F[0]%P and (any(F) or not any(E))

def powers_mod(h):
    rs=[]; r=[1]
    for i in range(13):
        rs.append(r+[0]*(7-len(r))); r=mod([0]+r,h)
    return rs

def sectors(h,y,z):
    R=powers_mod(h); out=[]
    for b in range(13):
        A=[]; f=[]
        for a in range(13):
            A.append([G[1,1,a,b]*v%P for v in R[a]]+[G[-1,1,a,b]*pow(y,-a%13,P)%P,G[1,-1,a,b]*pow(z,a,P)%P]+[G[-1,-1,a,b]*v%P for v in R[-a%13]])
            f.append(target(a,b))
        sol,r=solve(A,f)
        if sol is None: return None,b
        out.append({'b':b,'rank':r,'solution':sol})
    return out,None

def main():
    counts=Counter(); census=[]; witnesses=[]
    for y in range(1,53):
        c,n=family(y)
        for lam in range(53):
            h=[(a+lam*b)%P for a,b in zip(c,n)]+[1]
            row={'y':y,'lambda':lam,'H':h}
            if not sector3_gate(h,y,y): status='sector3_necessary_failure'
            elif h[0]==0: status='zero_support_root'
            elif gcd(h,[(i*h[i])%P for i in range(1,8)])!=[1]: status='repeated_support_root'
            else:
                frob=[0,1]
                for _ in range(7): frob=power(frob,53,h)
                row['frobenius7_remainder']=frob
                if frob!=[0,1]: status='does_not_split_degree7'
                else:
                    sol,failed=sectors(h,y,y)
                    if sol is None: status='full_sector_failure'; row['failed_b']=failed
                    else:
                        status='witness'; row['sectors']=sol
                        witnesses.append(row.copy())
            row['status']=status; counts[status]+=1; census.append(row)
    assert len(census)==52*53
    data={'scope':{'characteristic':53,'degree':7,'y_equals_z':True,'y_in':'F53*','lambda_in':'F53','Hplus_equals_Hminus':True,'beta':1,'allocation':[7,1,1,7]},'counts':dict(counts),'total':len(census),'census':census,'witnesses':witnesses}
    (ROOT/'DEGREE7_CENSUS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'total':len(census),'counts':dict(counts),'witnesses':[{k:v for k,v in w.items() if k!='sectors'} for w in witnesses]},indent=2))
    if witnesses: (ROOT/'DEGREE7_WITNESS.json').write_text(json.dumps(witnesses[0],indent=2)+'\n')

if __name__=='__main__': main()
