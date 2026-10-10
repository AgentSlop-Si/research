#!/usr/bin/env python3
"""Auditor-authored exact circuit and bounded numerical potential controls."""
import json,random,cmath,math
from fractions import Fraction as F
from pathlib import Path

def roots(n,p):
    if (p-1)%n:raise ValueError('unsupported length')
    primes=[q for q in [2,3] if n%q==0]
    for g in range(2,p):
        w=pow(g,(p-1)//n,p)
        if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in primes):break
    else:raise ValueError('root')
    a=[1]
    for _ in range(1,n):a.append(a[-1]*w%p)
    return a

def binary(x,R,p,lift=False,skip_identity=True):
    n=len(x);a=x[:];add=mul=0;h=n//2
    while h:
        step=n//(2*h)
        for start in range(0,n,2*h):
            for j in range(h):
                u=a[start+j];v=a[start+j+h];top=(u+v)%p
                if lift:
                    coeff=-2%p;bottom=(top+coeff*v)%p;mul+=int(not skip_identity or coeff!=1)
                else:bottom=(u-v)%p
                add+=2;w=R[j*step]
                if w!=1:bottom=bottom*w%p;mul+=1
                a[start+j]=top;a[start+j+h]=bottom
        h//=2
    bits=n.bit_length()-1;res=[0]*n
    for i,v in enumerate(a):
        j=0;s=i
        for _ in range(bits):j=2*j+(s&1);s>>=1
        res[j]=v
    return res,(add,mul)

def split(x,R,p):
    n=len(x);counts=[0,0]
    def rec(v,stride):
        m=len(v)
        if m==1:return v[:]
        if m==2:counts[0]+=2;return [(v[0]+v[1])%p,(v[0]-v[1])%p]
        h=m//2;q=m//4;s=[(v[j]+v[j+h])%p for j in range(h)];d=[(v[j]-v[j+h])%p for j in range(h)];counts[0]+=m
        c=[];e=[];imag=R[q*stride]
        for j in range(q):
            z=imag*d[j+q]%p;counts[1]+=int(imag!=1);u=(d[j]+z)%p;v2=(d[j]-z)%p;counts[0]+=2
            for which in [1,3]:
                tw=R[which*j*stride]
                if tw!=1:
                    if which==1:u=u*tw%p
                    else:v2=v2*tw%p
                    counts[1]+=1
            c.append(u);e.append(v2)
        ev=rec(s,2*stride);od1=rec(c,4*stride);od3=rec(e,4*stride);out=[0]*m
        out[::2]=ev;out[1::4]=od1;out[3::4]=od3;return out
    return rec(x,1),tuple(counts)

def gt(x,R,p,method='split',identity_aware=False):
    n=len(x);g=n//3;rg=R[::3];eg=3*pow(3,-1,g);e3=g*pow(g,-1,3);ys=[];adds=muls=0
    for a in range(3):
        row=[x[(j*eg+a*e3)%n] for j in range(g)]
        y,c=split(row,rg,p) if method=='split' else binary(row,rg,p,lift=method=='lift')
        ys.append(y);adds+=c[0];muls+=c[1]
    inv2=pow(2,-1,p);v=-inv2%p;w=(R[g]-R[2*g])*inv2%p;out=[0]*n
    for j in range(g):
        a,b,c=(row[j] for row in ys);t=(b+c)%p;d=(b-c)%p;mid=(a+v*t)%p;z=w*d%p
        out[3*j%n]=(a+t)%p;out[(3*j+g)%n]=(mid+z)%p;out[(3*j+2*g)%n]=(mid-z)%p
        adds+=6;muls+=int(v!=1)+int(w!=1) if identity_aware else 2
    return out,(adds,muls)

def entropy(A):return -sum((abs(z)**2)*math.log2(abs(z)**2) for row in A for z in row if abs(z)>1e-14)
def fourier(n):return [[cmath.exp(2j*math.pi*i*j/n)/math.sqrt(n) for j in range(n)] for i in range(n)]
def apply_gate(A,ids,U):
    B=[r[:] for r in A]
    for i,a in enumerate(ids):B[a]=[sum(U[i][j]*A[ids[j]][k] for j in range(len(ids))) for k in range(len(A))]
    return B

def main():
    out={'policy':'Only independent code executed; numerical controls are not exact analytic proofs','dyadic':[],'mixed':[],'large':[],'entropy_controls':[],'volume_tolls':[]};rng=random.Random(26101026)
    for p in [12289,786433]:
        for n in [2,4,8,16,32,64,128,256]:
            R=roots(n,p);t=n.bit_length()-1;expected=(n*t,(n//2)*t-n+1)
            for j in range(n):
                x=[int(i==j) for i in range(n)];ref=[R[i*j%n] for i in range(n)];a,ca=binary(x,R,p);b,cb=split(x,R,p);c,cc=binary(x,R,p,True)
                assert a==b==c==ref and ca==cb==expected and cc==(ca[0],ca[1]+n*t//2)
            out['dyadic'].append({'n':n,'field':p,'full_basis_entries':n*n,'add_mul':expected,'lift_penalty':n*t//2})
        for g in [2,4,8,16,32,64,128]:
            n=3*g;R=roots(n,p);t=g.bit_length()-1;expected=(3*g*t+6*g,3*(g*t//2-g+1)+2*g)
            for j in range(n):
                x=[int(i==j) for i in range(n)];ref=[R[i*j%n] for i in range(n)]
                a,ca=gt(x,R,p);b,cb=gt(x,R,p,'binary');assert a==b==ref and ca==cb==expected
            out['mixed'].append({'n':n,'field':p,'full_basis_entries':n*n,'add_mul':expected,'cold_table_multiplications':n-1,'extra_table_vs_G':2*g})
        for n in [1024,4096,16384]:
            if (p-1)%n:continue
            R=roots(n,p);x=[rng.randrange(p) for _ in range(n)];a,ca=binary(x,R,p);b,cb=split(x,R,p);c,cc=binary(x,R,p,True);assert a==b==c and ca==cb
            checked=[]
            for k in [0,1,n//3,n-1]:
                val=sum(xx*R[j*k%n] for j,xx in enumerate(x))%p;assert a[k]==val;checked.append(k)
            out['large'].append({'n':n,'field':p,'add_mul':ca,'direct_bins':checked,'lift_penalty':cc[1]-ca[1]})
    # Exact recurrence checks at huge count-only sizes.
    recur={1:(0,0),2:(2,0)}
    for t in range(2,129):
        n=1<<t;a,m=recur[n//2];aa,mm=recur[n//4];recur[n]=(a+2*aa+3*n//2,m+2*mm+3*n//4-2);assert recur[n]==(n*t,n*t//2-n+1)
    out['count_only_dyadic_exponents']=128
    # Characteristic-3 lifting and characteristic-7 triple identity coefficients.
    n=2;p=3;R=[1,2];x=[1,2];a,ca=binary(x,R,p);b,cb=binary(x,R,p,True);literal,cl=binary(x,R,p,True,False)
    assert a==b==literal and ca==cb==(2,0) and cl==(2,1)
    out['characteristic_3_lift_exception']={'n':2,'field':3,'minus_two':1,'optimized_add_mul':cb,'literal_source_add_mul':cl}
    R=[pow(5,j,7) for j in range(6)];x=[1,2,3,4,5,6];a,ca=gt(x,R,7);b,cb=gt(x,R,7,identity_aware=True);assert a==b==[sum(x[j]*R[j*k%6] for j in range(6))%7 for k in range(6)] and sum(ca)==22 and sum(cb)==20
    out['characteristic_7_GT_exception']={'n':6,'field':7,'omega':5,'source_count':22,'identity_aware_count':20}
    # Cubic field Q(c), c^3=1/2: exact counterexample to clamping actual coefficient magnitude at 1.
    def padd(a,b):return [x+y for x,y in zip(a,b)]
    def pmul(a,b):
        r=[F(0)]*5
        for i,x in enumerate(a):
            for j,y in enumerate(b):r[i+j]+=x*y
        for k in [4,3]:r[k-3]+=r[k]/2
        return r[:3]
    def pmm(A,B):return [[padd(pmul(A[i][0],B[0][j]),pmul(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
    H=[[1,1],[1,-1]];C=[[[F(0),F(x),F(0)] for x in row] for row in H];C3=pmm(pmm(C,C),C)
    assert C3==[[[F(x),F(0),F(0)] for x in row] for row in H]
    raw=2**(-1/3);assert raw<1 and abs(2**(2/(2*3*2))/math.sqrt(2)-raw)<1e-14
    out['coefficient_clamp_counterexample']={'N':2,'gate_budget':3,'arity':2,'gate':'c F_2, c positive, c^3=1/2','exact_cube_equals_F2':True,'actual_max_entry':raw,'incorrect_clamp':1,'raw_bound_saturated':True}
    # High-arity entropy bounds under arbitrary preceding unitary gates.
    for n in [8,12,24]:
        A=[[complex(i==j) for j in range(n)] for i in range(n)]
        for trial in range(30):
            b=rng.choice([2,3,4,6]);b=min(b,n);ids=rng.sample(range(n),b);U=fourier(b)
            # Independent unit-modulus row/column phase gauges preserve unitarity.
            rp=[cmath.exp(1j*rng.random()*6) for _ in range(b)];cp=[cmath.exp(1j*rng.random()*6) for _ in range(b)];U=[[rp[i]*U[i][j]*cp[j] for j in range(b)] for i in range(b)]
            old=entropy(A);A=apply_gate(A,ids,U);delta=entropy(A)-old;assert abs(delta)<=b*math.log2(b)+1e-9
            out['entropy_controls'].append({'n':n,'b':b,'change':round(delta,10),'bound':b*math.log2(b)})
    for t in range(1,25):
        g=1<<t;n=3*g;two=3*g*t//2;three=g;vol=two*math.log(2)+three*1.5*math.log(3);ent=two*2+three*3*math.log2(3)
        assert math.isclose(vol,n/2*math.log(n),rel_tol=1e-14) and math.isclose(ent,n*math.log2(n),rel_tol=1e-14)
        out['volume_tolls'].append({'G':g,'N':n,'two_gates':two,'three_gates':three,'volume_entropy_equalities':True})
    out['summary']={'complete_basis_entries':sum(a['full_basis_entries'] for a in out['dyadic']+out['mixed']),'full_matrices':len(out['dyadic'])+len(out['mixed']),'large_vectors':len(out['large']),'entropy_controls':len(out['entropy_controls'])};out['result']='PASS'
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']|{'result':'PASS'}))
if __name__=='__main__':main()
