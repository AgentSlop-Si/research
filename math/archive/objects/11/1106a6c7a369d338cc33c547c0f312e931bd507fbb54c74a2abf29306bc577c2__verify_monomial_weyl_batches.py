#!/usr/bin/env python3
"""Independent promised sparse-action recovery and explicit FFT-family controls."""
import json
from pathlib import Path


def zero(n): return [[0] * n for _ in range(n)]
def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def tr(a): return [list(row) for row in zip(*a)]
def add(a,b,p): return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]


def mm(a,b,p):
    n=len(a); c=zero(n)
    sb=[[(j,v) for j,v in enumerate(row) if v] for row in b]
    for i,row in enumerate(a):
        for k,v in enumerate(row):
            if v:
                for j,w in sb[k]: c[i][j]+=v*w
        c[i]=[v%p for v in c[i]]
    return c


def primitive_root(p):
    t=p-1; factors=[]; d=2
    while d*d<=t:
        if t%d==0:
            factors.append(d)
            while t%d==0:t//=d
        d+=1
    if t>1:factors.append(t)
    return next(g for g in range(2,p) if all(pow(g,(p-1)//r,p)!=1 for r in factors))


def root(n,p): return pow(primitive_root(p),(p-1)//n,p)
def fourier(n,p,inverse=False):
    w=root(n,p); norm=1
    if inverse:w=pow(w,-1,p);norm=pow(n,-1,p)
    return [[norm*pow(w,i*j,p)%p for j in range(n)] for i in range(n)]


def kron(a,b):
    na,nb=len(a),len(b);out=zero(na*nb)
    for i in range(na):
        for j in range(na):
            if a[i][j]:
                for r in range(nb):
                    for s in range(nb):out[i*nb+r][j*nb+s]=a[i][j]*b[r][s]
    return out


def diag(values):
    out=zero(len(values))
    for i,v in enumerate(values):out[i][i]=v
    return out


def shift(n,step=1):
    out=zero(n)
    for j in range(n):out[(j+step)%n][j]=1
    return out


def mono_arrays(a):
    n=len(a);perm=[];weights=[]
    for j in range(n):
        entries=[(i,a[i][j]) for i in range(n) if a[i][j]]
        assert len(entries)==1
        perm.append(entries[0][0]);weights.append(entries[0][1])
    assert len(set(perm))==n
    return perm,weights


def recover(alpha,uw,beta,vw,omega,p,seed_entry):
    """Only sparse arrays, root and one scalar callback; no H matrix access."""
    n=len(alpha);cycles=[];which=[-1]*n;position=[-1]*n;products=[]
    for v in range(n):
        if which[v]>=0:continue
        cycle=[];product=1;t=v
        while which[t]<0:
            which[t]=len(cycles);position[t]=len(cycle);cycle.append(t)
            product=product*vw[t]%p;t=beta[t]
        assert t==v
        cycles.append(cycle);products.append(product)
    d=len(cycles[0]);c=len(cycles)
    assert c*d==n and all(len(row)==d for row in cycles)
    starts=[i for i,x in enumerate(products) if x==1]
    assert len(starts)==1
    labeled=[];current=starts[0]
    for r in range(c):
        assert current not in labeled
        labeled.append(current)
        assert products[current]==pow(omega,d*r,p)
        current=which[alpha[cycles[current][0]]]
    assert current==starts[0]
    verts=[cycles[i] for i in labeled]
    h=[]
    for row in verts:
        prefixes=[1]
        for v in row[:-1]:prefixes.append(prefixes[-1]*vw[v]%p)
        h.append(prefixes)
    ia=[0]*n
    for v,w in enumerate(alpha):ia[w]=v
    ks=[];us=[]
    for r in range(c):
        u=ia[verts[(r+1)%c][0]]
        assert which[u]==labeled[r]
        ks.append(position[u]);us.append(u)
    powers=[1]
    for j in range(1,n):powers.append(powers[-1]*omega%p)
    gamma=[seed_entry(verts[0][0],0)]
    assert gamma[0]
    for j in range(n):
        r=j%c;k=ks[r];u=us[r]
        value=uw[u]*gamma[j]*h[r][k]*powers[(-j*k)%n]%p
        if j+1<n:gamma.append(value)
        else:assert value==gamma[0]
    input_route=[0]*n;output_route=[0]*n;output_scale=[0]*n
    for r in range(c):
        for k in range(d):
            output_route[r*d+k]=verts[r][k]
            output_scale[r*d+k]=h[r][k]*powers[(-r*k)%n]%p
        for ell in range(d):input_route[r+c*ell]=r*d+ell
    return {'d':d,'c':c,'input_route':input_route,'input_scale':gamma,
            'output_route':output_route,'output_scale':output_scale,
            'linear_pass_counts':{'clock_edges':n,'gamma_updates':n,'root_table_entries':n}}


def materialize_normal_form(data,omega,p):
    n=len(data['input_route']);d=data['d'];c=data['c'];out=zero(n)
    for j in range(n):
        r,ell=divmod(data['input_route'][j],d)
        for k in range(d):
            t=r*d+k;i=data['output_route'][t]
            out[i][j]=data['output_scale'][t]*pow(omega,(-c*k*ell)%n,p)*data['input_scale'][j]%p
    return out


def recovery_controls():
    results=[]
    for n,p in ((4,17),(8,97),(12,97),(16,65537),(9,109),(25,101),(64,65537)):
        omega=root(n,p)
        for d in (x for x in range(1,n+1) if n%x==0):
            c=n//d;r=zero(n)
            for b in range(c):
                for s in range(d):r[b*d+s][b+c*s]=1
            bank=kron(eye(c),fourier(d,p)) if d>1 else eye(n)
            bi=kron(eye(c),fourier(d,p,True)) if d>1 else eye(n)
            ordering=list(range(0,n,2))+list(range(1,n,2))[::-1]
            left,li=zero(n),zero(n)
            for j,i in enumerate(ordering):
                weight=j+2
                left[i][j]=weight;li[j][i]=pow(weight,-1,p)
            h=mm(left,mm(bank,r,p),p)
            hi=mm(tr(r),mm(bi,li,p),p)
            u=mm(h,mm(shift(n),hi,p),p)
            v=mm(h,mm(diag([pow(omega,j,p) for j in range(n)]),hi,p),p)
            alpha,uw=mono_arrays(u);beta,vw=mono_arrays(v)
            queries=[]
            def seed(i,j):queries.append([i,j]);return h[i][j]
            data=recover(alpha,uw,beta,vw,omega,p,seed)
            assert data['d']==d and len(queries)==1
            assert materialize_normal_form(data,omega,p)==h
            assert all(sum(bool(x) for x in row)==d for row in h)
            results.append({'N':n,'field':p,'d':d,'batches':c,'seed_queries':queries,
                            'exact_reconstruction':True,**data['linear_pass_counts']})
    return results


def bank_family(a,m,b,p):
    n=a*m*b;omega=root(n,p);pmat,qmat,pi,qi=zero(n),zero(n),zero(n),zero(n)
    up,vp,uq,vq=zero(n),zero(n),zero(n),zero(n)
    for r0 in range(a):
        for r1 in range(m):
            for r2 in range(b):
                j=r0+a*r1+a*m*r2
                vq[(r0*m+r1)*b+r2][j]=1
            for t2 in range(b):
                row=(r0*b+t2)*m+r1
                phase=pow(root(m*b,p),r1*t2,p) if m*b>1 else 1
                uq[row][(r0*m+r1)*b+t2]=phase
                for r2 in range(b):
                    j=r0+a*r1+a*m*r2
                    qmat[row][j]=phase*pow(root(b,p),r2*t2,p)%p if b>1 else phase
                    qi[j][row]=pow(b,-1,p)*pow(phase,-1,p)*(pow(root(b,p),(-r2*t2)%b,p) if b>1 else 1)%p
        for t2 in range(b):
            for t1 in range(m):
                col=(r0*b+t2)*m+t1;group=t2*m+t1
                phase=pow(omega,r0*(t2+b*t1),p)
                vp[group*a+r0][col]=phase
                for t0 in range(a):
                    row=t2+b*t1+b*m*t0
                    up[row][group*a+t0]=1
                    pmat[row][col]=phase*(pow(root(a,p),r0*t0,p) if a>1 else 1)%p
                    pi[col][row]=pow(a,-1,p)*pow(phase,-1,p)*(pow(root(a,p),(-r0*t0)%a,p) if a>1 else 1)%p
    bank=kron(eye(a*b),fourier(m,p))
    assert mm(pmat,mm(bank,qmat,p),p)==fourier(n,p)
    assert mm(pmat,pi,p)==mm(qmat,qi,p)==eye(n)
    assert all(sum(bool(x) for x in row)==a for row in pmat)
    assert all(sum(bool(x) for x in row)==b for row in qmat)
    for x,y in ((shift(n),diag([pow(omega,j,p) for j in range(n)])),(diag([pow(omega,j,p) for j in range(n)]),shift(n,-1))):
        amat=mm(pi,mm(y,pmat,p),p);tmat=mm(qmat,mm(x,qi,p),p)
        mono_arrays(amat);mono_arrays(tmat)
        assert mm(amat,bank,p)==mm(bank,tmat,p)
    detail={'N':n,'a':a,'m':m,'b':b,'d_P':a,'d_Q':b,'support_product':a*m*b,'all_four_actions_monomial':True}
    if a==b==4:
        ehi=diag([1,1,p-1,p-1]);elo=diag([1,p-1,1,p-1]);ph,pl,k2=zero(4),zero(4),zero(4)
        for j in range(4):ph[j^2][j]=1;pl[j^1][j]=1;k2[(j%2)*2+j//2][j]=1
        d4=diag([1,1,1,root(4,p)])
        at=[mm(term,d4,p) for term in (ehi,ph)];ct=[mm(term,k2,p) for term in (elo,pl)]
        pterms4=[mm(up,kron(eye(n//4),term),p) for term in at]
        pterms3=[mm(kron(eye(n//4),term),vp,p) for term in ct]
        qterms2=[mm(uq,kron(eye(n//4),term),p) for term in at]
        qterms1=[mm(kron(eye(n//4),term),vq,p) for term in ct]
        for pair in (pterms4,pterms3,qterms2,qterms1):
            for term in pair:mono_arrays(term)
        h4,h3,h2,h1=[add(*pair,p) for pair in (pterms4,pterms3,qterms2,qterms1)]
        assert mm(h4,h3,p)==pmat and mm(h2,h1,p)==qmat
        assert mm(h4,mm(h3,mm(bank,mm(h2,h1,p),p),p),p)==fourier(n,p)
        detail['explicit_paired_green_layers']=4;detail['zero_mask_guards']=[1]*8
    return detail


def main():
    recovery=recovery_controls()
    family=[bank_family(a,m,b,p) for a,m,b,p in ((2,4,2,65537),(4,8,2,65537),(4,16,4,65537),(4,8,4,65537),(3,3,1,109),(1,3,3,109),(3,3,3,109))]
    result={'recovery_cases':len(recovery),'recovery':recovery,'bank_family_cases':family,
            'all_exact_assertions_passed':True,
            'scope':'Necessary normal form and known mixed-radix constructions only; no new Fourier speedup.'}
    Path(__file__).with_name('MONOMIAL_WEYL_CLASSIFICATION_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'recovery_cases':len(recovery),'bank_family_cases':family,'all_exact_assertions_passed':True},indent=2))


if __name__=='__main__':main()
