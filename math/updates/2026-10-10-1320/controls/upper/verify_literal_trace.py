#!/usr/bin/env python3
"""Fresh independent N7 eight-bank control. No author/predecessor code loaded.
Arithmetic: exact QQ(q), then cubic quotient. All result files are local.
"""
import argparse, json, hashlib, time, itertools
from pathlib import Path
import sympy as sp

OUT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(); ap.add_argument('--s1',type=int,default=0); ap.add_argument('--source'); args=ap.parse_args()
z=sp.symbols('z'); K=sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(7,z),z),alias='q')
q=K.unit; zero=K.zero; one=K.one

def fk(x): return K.convert(x)
def enc(x):
    a=list(reversed(x.to_list())); return [str(v) for v in a]+['0']*(6-len(a))
def det(M):
    a=[r[:] for r in M]; n=len(a); d=one
    for j in range(n):
        p=next((i for i in range(j,n) if a[i][j]),None)
        if p is None:return zero
        if p!=j: a[p],a[j]=a[j],a[p]; d=-d
        v=a[j][j]; d*=v
        for i in range(j+1,n):
            if not a[i][j]:continue
            c=a[i][j]/v
            for k in range(j+1,n):a[i][k]-=c*a[j][k]
            a[i][j]=zero
    return d

def solve(M,b):
    a=[r[:]+[v] for r,v in zip(M,b)]; n=len(a); cols=len(M[0]); piv=[]; h=0
    for j in range(cols):
        p=next((i for i in range(h,n) if a[i][j]),None)
        if p is None:continue
        a[p],a[h]=a[h],a[p]; c=a[h][j]; a[h]=[x/c for x in a[h]]
        for i in range(n):
            if i!=h and a[i][j]:
                c=a[i][j]; a[i]=[x-c*y for x,y in zip(a[i],a[h])]
        piv.append(j);h+=1
        if h==n:break
    assert all(any(r[:cols]) or not r[-1] for r in a), 'Inconsistent exact row'
    x=[zero]*cols
    for i,j in enumerate(piv):x[j]=a[i][-1]
    assert all(sum((v*w for v,w in zip(r,x)),zero)==t for r,t in zip(M,b))
    return x,piv

def qb(n,k,s):
    if k<0 or k>n:return zero
    row=[one]
    for a in range(1,n+1):
        row=[(row[j] if j<len(row) else zero)+(s**(a-j)*row[j-1] if j else zero) for j in range(a+1)]
    return row[k]
H=q/(one+q); C=sum((q**((-j*j)%7) for j in range(7)),zero)/fk(7)
assert C
m=[one]
for a in range(2,6):
    G=qb(a+1,1,q); B=qb(8-a,1,q**6)
    m.append(q**((2*(a+1)**2)%7)/(H*G)-B/G)
D=m[2]-m[1]**2; assert D
s1=fk(args.s1)
s2=(s1*(m[3]-m[1]*m[2])+m[1]*m[3]-m[4])/D
s3=m[3]-s1*m[2]+s2*m[1]
assert m[4]==s1*m[3]-s2*m[2]+s3*m[1]
assert s3
# t^3=s1*t^2-s2*t+s3.
Z=(zero,zero,zero); E=(one,zero,zero); T=(zero,one,zero)
def ac(x):return (x,zero,zero)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    p=[zero]*5
    for i in range(3):
        for j in range(3):
            if a[i] and b[j]:p[i+j]+=a[i]*b[j]
    for i in (4,3):
        if p[i]:
            v=p[i];p[i-1]+=v*s1;p[i-2]-=v*s2;p[i-3]+=v*s3
    return tuple(p[:3])
def scale(a,v):return tuple(x*v for x in a)
def powa(a,n):
    b=E
    while n:
        if n&1:b=mul(b,a)
        a=mul(a,a);n//=2
    return b
def inva(a):
    cols=[mul(a,powa(T,j)) for j in range(3)]
    sol,piv=solve([[cols[j][i] for j in range(3)] for i in range(3)],[one,zero,zero])
    assert len(piv)==3
    sol=tuple(sol);assert mul(a,sol)==E;return sol
powers=[powa(T,j) for j in range(8)]
traces=[fk(3),s1,s1*s1-2*s2]
for j in range(3,15):traces.append(s1*traces[-1]-s2*traces[-2]+s3*traces[-3])
def trace(a):return sum((a[j]*traces[j] for j in range(3)),zero)
Gram=[[traces[i+j] for j in range(3)] for i in range(3)]
disc=det(Gram);assert disc
# Direct definition of the Fourier trace coefficients, independent of target shortcut.
F=[[q**((-a*b)%7) for b in range(7)] for a in range(7)]
for a in range(7):
    for b in range(7):
        tr=sum((q**((-b*t)%7)*F[(t+a)%7][t] for t in range(7)),zero)/fk(7)
        assert tr==C*q**((2*(a+b)**2)%7)
# Order: three ++ nodes; one -+ singleton; one +- singleton; three -- nodes.
sectors=[[Z for _ in range(7)] for __ in range(4)]
ranks=[]; pivots=[]; minors=[]; solved=[]; matrices=[]
for b in range(7):
    M=[]
    for a in range(7):
        row=[]
        for eps,dlt,typ in [(1,1,'triple'),(-1,1,'single'),(1,-1,'single'),(-1,-1,'triple')]:
            r=(eps*a)%7; ell=(dlt*b)%7
            coeff=qb(r+ell,ell,q**((eps*dlt)%7)) if r+ell<7 else zero
            row.extend([coeff*v for v in powers[r]] if typ=='triple' else [coeff])
        M.append(row)
    target=[q**((2*(a+b)**2)%7) for a in range(7)]
    matrices.append(M)
    sol,piv=solve(M,target);ranks.append(len(piv));pivots.append(piv);solved.append(sol)
    if len(piv)==7:minors.append(enc(det([[row[j] for j in piv] for row in M])))
    else:minors.append(None)
    for idx,eps,dlt,sl in [(0,1,1,slice(0,3)),(3,-1,-1,slice(5,8))]:
        hp,hpiv=solve(Gram,sol[sl]);assert len(hpiv)==3
        sectors[idx][(dlt*b)%7]=tuple(hp)
    sectors[1][b]=ac(sol[3]);sectors[2][(-b)%7]=ac(sol[4])
print('Exact transformed rows:',ranks,flush=True)

source_audit=None
if args.source:
    source_path=Path(args.source); raw=source_path.read_bytes(); author=json.loads(raw)
    def dec(v):return sum((fk(sp.Rational(c))*q**i for i,c in enumerate(v)),zero)
    def da(v):return tuple(dec(c) for c in v)
    assert author['cubic']['s2']==enc(s2) and author['cubic']['s3']==enc(s3)
    assert author['cubic']['discriminant']==enc(disc)
    assert author['edge']['moments']==[enc(v) for v in m]
    assert author['edge']['D']==enc(D) and author['edge']['H']==enc(H)
    assert author['C']==enc(C)
    az=[[dec(v) for v in author['row_results'][str(b)]['transformed_amplitudes']] for b in range(7)]
    reflect=lambda v: v[5:8]+[v[4],v[3]]+v[:3]
    edge=[H*(m[2]+s2)/s3,H,H*m[1],H,q*q-H*(m[2]+s2)/s3-H,zero,zero,zero]
    assert az[1]==edge and az[6]==reflect(edge)
    assert az[4]==reflect(az[3]) and az[5]==reflect(az[2])
    source_minor_rows={}
    for b in range(7):
        assert author['row_results'][str(b)]['rank']==ranks[b]
        cols=author['row_results'][str(b)]['pivot_columns_zero_based']
        assert cols==pivots[b]
        claimed=dec(author['row_results'][str(b)]['pivot_determinant'])
        matches=[list(rr) for rr in itertools.combinations(range(7),ranks[b]) if det([[matrices[b][i][j] for j in cols] for i in rr])==claimed]
        assert matches, 'Reported minor does not match any ordered original row subset'
        source_minor_rows[str(b)]=matches
        assert all(sum((x*y for x,y in zip(row,az[b])),zero)==q**((2*(a+b)**2)%7) for a,row in enumerate(matrices[b]))
        if b in (0,2,3):
            assert az[b]==solved[b]
            assert author['row_results'][str(b)]['pivot_columns_zero_based']==pivots[b]
            assert author['row_results'][str(b)]['pivot_determinant']==minors[b]
    author_sectors=[[da(v) for v in group] for group in author['sector_polynomials_group_order_pp_mp_pm_mm']]
    deriv=add(scale(powa(T,2),fk(3)),ac(s2))
    assert mul(da(author['generic_alpha_inverse']),T)==E
    assert mul(da(author['generic_guard_inverse']),neg(powa(T,7)))==E
    assert mul(da(author['derivative_inverse']),deriv)==E
    assert one+s2-s3==sum((fk(v)*q**i for i,v in enumerate([24,40,41,32,-3,-36])),zero)/fk(29)
    for b in range(7):
        for idx,dlt,part in [(0,1,az[b][:3]),(3,-1,az[b][5:])]:
            poly=author_sectors[idx][(dlt*b)%7]
            assert all(trace(mul(poly,powa(T,d)))==part[d] for d in range(3))
            # Independently check the frozen note's Lagrange expression.
            numerator=add(add(ac(part[2]),scale(T,part[1])),scale(add(powa(T,2),ac(s2)),part[0]))
            assert mul(poly,deriv)==numerator
        assert author_sectors[1][b]==ac(az[b][3])
        assert author_sectors[2][(-b)%7]==ac(az[b][4])
    sectors=author_sectors
    source_audit={'path':str(source_path),'sha256':hashlib.sha256(raw).hexdigest(),
                  'all_transformed_amplitudes_verified':True,'all_sector_polynomials_verified':True,
                  'exact_note_recipe_verified':True,'selected_minors_verified':True,
                  'all_three_saved_quotient_inverses_verified':True,
                  'additional_g_at_1_identity_verified':True,'all_seven_reported_pivot_minors_verified_at_rows':source_minor_rows}
    print('Frozen author literal data and exact recipe verified.',flush=True)

# Direct matrix arithmetic over the cubic algebra. Each triple evaluation gives
# three literal branch inverses, and trace gives their sum in the splitting field.
def ident():return [[E if i==j else Z for j in range(7)] for i in range(7)]
def mm(A,B):
    out=[[Z for j in range(7)] for i in range(7)]
    for i in range(7):
        for k in range(7):
            if A[i][k]==Z:continue
            for j in range(7):
                if B[k][j]!=Z:out[i][j]=add(out[i][j],mul(A[i][k],B[k][j]))
    return out
I=ident(); total=[[zero for j in range(7)] for i in range(7)];checks=[]
for idx,(eps,dlt,typ) in enumerate([(1,1,'triple'),(-1,1,'single'),(1,-1,'single'),(-1,-1,'triple')]):
    alpha=T if typ=='triple' else E; delta=neg(powa(alpha,7)); delta_inv=inva(delta)
    for j in range(7):
        X=[[Z for k in range(7)] for i in range(7)]
        for t in range(7):
            X[(t+eps)%7][t]=add(X[(t+eps)%7][t],alpha)
            X[t][t]=add(X[t][t],ac(q**((eps*dlt*j+dlt*t)%7)))
        pw=I;geom=[[x for x in row] for row in I]
        for n in range(1,7):
            pw=mm(pw,X)
            geom=[[add(geom[a][b],pw[a][b]) for b in range(7)] for a in range(7)]
        x7=mm(pw,X)
        scalar=add(powa(alpha,7),E)
        assert x7==[[scalar if a==b else Z for b in range(7)] for a in range(7)]
        inv=[[mul(x,delta_inv) for x in row] for row in geom]
        den=[[sub(I[a][b],X[a][b]) for b in range(7)] for a in range(7)]
        assert mm(den,inv)==I and mm(inv,den)==I
        w=Z
        for ell in range(7):w=add(w,scale(sectors[idx][ell],q**((-eps*dlt*j*ell)%7)))
        w=scale(mul(delta,w),C/fk(7))
        for a in range(7):
            for b in range(7):
                v=mul(w,inv[a][b])
                if typ=='triple':total[a][b]+=trace(v)
                else:
                    assert not v[1] and not v[2]
                    total[a][b]+=v[0]
        checks.append({'orientation':[eps,dlt], 'phase':j,'covers_branches':3 if typ=='triple' else 1,'two_sided_inverse':True})
    print('Literal orientation checked:',eps,dlt,typ,flush=True)
assert total==F
result={'status':'PASS','scope':'Characteristic-zero construction in splitting field of stated separable cubic. No lower bound conclusion.',
        's1':args.s1,'cubic_t3_minus_s1_t2_plus_s2_t_minus_s3':{'s1':enc(s1),'s2':enc(s2),'s3':enc(s3)},
        'moments':[enc(v) for v in m], 'D':enc(D),'cubic_discriminant':enc(disc), 'Gauss_C':enc(C),
        'ranks':ranks,'pivot_columns_zero_based':pivots,'full_rank_minors':minors,
        'original_literal_branches_covered':sum(v['covers_branches'] for v in checks),'branch_checks':checks,
        'fourier_entries_checked':49,'all_fourier_entries_pass':True,
        'normalized_trace_amplitude_polynomials':[[[enc(x) for x in h] for h in row] for row in sectors],
        'transformed_row_solutions':[[enc(x) for x in row] for row in (az if args.source else solved)], 'frozen_source_audit':source_audit}
(OUT/('AUTHOR_LITERAL_RESULTS.json' if args.source else 'LITERAL_TRACE_RESULTS.json')).write_text(json.dumps(result,indent=2)+'\n')
print('PASS: all 56 literal branches, both inverse products, all 49 Fourier entries.',flush=True)
