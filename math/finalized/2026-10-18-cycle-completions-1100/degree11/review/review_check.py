#!/usr/bin/env python3
"""Fresh independent exact verifier. No supplied program is run or imported.
Input: inert certificate and census JSON, source report byte strings.
The original inverse uses a 13-term literal operator geometric series, rather
than either supplied inversion algorithm. Both multiplication orders are tested.
"""
import json, hashlib, time, sys, math
from pathlib import Path
from collections import Counter
P=53; N=13; Q=16; D=11
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent / 'inputs'
OUT=Path(__file__).resolve().parent
started=time.time()
checks=Counter()
def check(ok, label):
    if not ok: raise AssertionError(label)
    checks[label.split(':')[0]]+=1

def digest(b):return hashlib.sha256(b).hexdigest()
cert_bytes=(ROOT/'DEGREE11_LITERAL_CERTIFICATE.json').read_bytes()
check(digest(cert_bytes)=='8b7264552dbc555fe1ee46359f3e19fd8c74a01a2be17c36f9aa2031eb09a25c','certificate byte pin')
C=json.loads(cert_bytes)
# Generic prime-polynomial arithmetic, including extended Euclid, independent
# of the specialized extension multiplication below.
def trim(a):
    a=[x%P for x in a]
    while a and not a[-1]:a.pop()
    return a

def pa(a,b):
    z=[0]*max(len(a),len(b))
    for i,v in enumerate(a):z[i]+=v
    for i,v in enumerate(b):z[i]+=v
    return trim(z)
def ps(a,b):return pa(a,[-x for x in b])
def pm(a,b):
    z=[0]*(len(a)+len(b)-1) if a and b else []
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return trim(z)
def pd(a,b):
    a=trim(a);b=trim(b);assert b
    quot=[0]*max(0,(len(a)-len(b)+1));inv=pow(b[-1],-1,P)
    while len(a)>=len(b):
        k=len(a)-len(b);s=a[-1]*inv%P;quot[k]=s
        for j,y in enumerate(b):a[k+j]=(a[k+j]-s*y)%P
        a=trim(a)
    return trim(quot),a
def pg(a,b):
    while b:a,b=b,pd(a,b)[1]
    return [(x*pow(a[-1],-1,P))%P for x in a]
def pp(a,e,m):
    r=[1]
    while e:
        if e&1:r=pd(pm(r,a),m)[1]
        a=pd(pm(a,a),m)[1];e//=2
    return r
M=[3,1]+[0]*9+[1]
check(C['field_modulus_ascending']==M and C['degree']==11 and C['characteristic']==53,'field declaration')
x=[0,1];frob=[]
for k in range(11):x=pp(x,53,M);frob.append(x)
check(x==[0,1],'Rabin final Frobenius')
gcd=pg(M,ps(frob[0],[0,1]));check(gcd==[1],'Rabin prime divisor gcd')
# 11 prime, so these two tests prove irreducibility before any inversion.
Z=(0,)*D;O=(1,)+(0,)*(D-1)
def fe(v):
    check(isinstance(v,list) and len(v)==D and all(type(a) is int and 0<=a<P for a in v),'canonical field input')
    return tuple(v)
def sc(a,c):return tuple((x*c)%P for x in a)
def add(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def sub(a,b):return tuple((x-y)%P for x,y in zip(a,b))
def mul(a,b):
    if a==Z or b==Z:return Z
    if not any(a[1:]):return sc(b,a[0])
    if not any(b[1:]):return sc(a,b[0])
    v=[0]*21
    for i,x in enumerate(a):
        for j,y in enumerate(b):v[i+j]+=x*y
    # u^11=-u-3; coefficients may be unreduced until the final pass.
    for k in range(20,10,-1):
        v[k-11]-=3*v[k];v[k-10]-=v[k]
    return tuple(x%P for x in v[:11])
def power(a,e):
    r=O
    while e:
        if e&1:r=mul(r,a)
        a=mul(a,a);e//=2
    return r
def inverse(a):
    assert a!=Z
    r0,r1=M,trim(a);s0,s1=[],[1]
    while r1:
        q,r=pd(r0,r1);r0,r1=r1,r;s0,s1=s1,ps(s0,pm(q,s1))
    assert len(r0)==1
    z=pd([(x*pow(r0[0],-1,P))%P for x in s0],M)[1]
    z=tuple(z+[0]*(D-len(z)));check(mul(z,a)==O,'field inverse product');return z
check(pow(Q,13,P)==1 and all(pow(Q,k,P)!=1 for k in range(1,13)),'q exact order')
source_receipts=[]
for pin in json.loads((ROOT/'SOURCE_PINS.json').read_text()):
    b=(ROOT/pin['local_path']).read_bytes()
    s=digest(b);g=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check(s==pin['sha256'] and len(b)==pin['bytes'] and g==pin['git_blob_sha'],'source byte binding')
    source_receipts.append({**pin,'verified_sha256':s,'verified_git_blob_sha':g})
roots=[fe(v) for v in C['roots']];h=[O]
check(len(roots)==7 and len(set(roots))==7 and Z not in roots,'root cardinality legality')
for r in roots:
    z=[Z]*(len(h)+1)
    for i,v in enumerate(h):z[i]=sub(z[i],mul(r,v));z[i+1]=add(z[i+1],v)
    h=z
check(h==[fe(v) for v in C['H']],'annihilator exact product')
root_frob=[power(v,53) for v in roots]
check(set(root_frob)!=set(roots),'support Frobenius nonstability')
check(any(any(v[1:]) for v in h),'nonbase annihilator')
y,z=fe(C['y']),fe(C['z'])
check(y!=Z and z!=Z and any(y[1:]) and any(z[1:]),'nonbase cross legality')
# Gaussian factors from literal words in S,T: right-appending S creates
# omega^ell, while right-appending T introduces no commutation factor.
gtables={}
for e in (-1,1):
    for d in (-1,1):
        w=pow(Q,e*d%13,P);tab=[[0]*13 for _ in range(13)];tab[0][0]=1
        for n in range(1,13):
            for r in range(n+1):
                l=n-r
                tab[r][l]=((pow(w,l,P)*tab[r-1][l] if r else 0)+(tab[r][l-1] if l else 0))%P
        gtables[e,d]=tab

def G(e,d,a,b):
    r=e*a%13;l=d*b%13
    return gtables[e,d][r][l] if r+l<13 else 0
q=lambda e:pow(Q,e%13,P)
f=lambda a,b:q(10*(a+b)**2)
gamma=sum(q(-t*t) for t in range(13))*pow(13,-1,P)%P
check(gamma==7,'gamma from literal Fourier')
for a in range(13):
    for b in range(13):
        wc=sum(q(-b*t)*q(-(t+a)*t) for t in range(13))*pow(13,-1,P)%P
        check(wc==gamma*f(a,b)%P,'literal normalized Fourier coefficient')
        for e in (-1,1):
            for d in (-1,1):check(G(e,d,a,b)==G(-e,-d,-a,-b),'Gaussian reflection')
# All literal powers of A=alpha*S^epsilon+q^(epsilon*delta*j)*T^delta.
def identity():return [[O if r==c else Z for c in range(13)] for r in range(13)]
def left_A(X,alpha,e,d,j):
    return [[add(mul(alpha,X[(r-e)%13][c]),sc(X[r][c],q(e*d*j+d*r))) for c in range(13)] for r in range(13)]
def literal_inverse(alpha,beta,e,d,j,guard):
    assert beta==1
    term=identity();total=identity()
    for k in range(1,13):
        term=left_A(term,alpha,e,d,j)
        total=[[add(total[r][c],term[r][c]) for c in range(13)] for r in range(13)]
    thirteenth=left_A(term,alpha,e,d,j)
    targetA=add(power(alpha,13),O)
    for r in range(13):
        for c in range(13):check(thirteenth[r][c]==(targetA if r==c else Z),'literal A13 entry')
    gi=inverse(guard)
    V=[[mul(gi,total[r][c]) for c in range(13)] for r in range(13)]
    for r in range(13):
        for c in range(13):
            target=O if r==c else Z
            left=sub(sc(V[r][c],1-q(e*d*j+d*r)),mul(alpha,V[(r-e)%13][c]))
            right=sub(sc(V[r][c],1-q(e*d*j+d*c)),mul(alpha,V[r][(c+e)%13]))
            check(left==target,'left inverse entry');check(right==target,'right inverse entry')
    return V

banks=C['banks'];check(len(banks)==16,'physical bank count')
check(Counter((b['epsilon'],b['delta']) for b in banks)=={(1,1):7,(-1,1):1,(1,-1):1,(-1,-1):7},'orientation allocation')
for orientation in [(1,1),(-1,-1)]:
    check({tuple(b['alpha']) for b in banks if (b['epsilon'],b['delta'])==orientation}==set(roots),'same sign support identity')
all_sum=[[Z]*13 for _ in range(13)];all_amps=[];bank_receipts=[]
inv13=pow(13,-1,P)
for bi,bank in enumerate(banks):
    e,d=bank['epsilon'],bank['delta'];alpha=fe(bank['alpha']);beta=bank['beta']
    check(e in (-1,1) and d in (-1,1) and beta==1 and alpha!=Z,'physical bank legality')
    if e==-1 and d==1:check(alpha==y,'cross y binding')
    if e==1 and d==-1:check(alpha==z,'cross z binding')
    guard=sub(sub(O,power(alpha,13)),O)
    check(guard!=Z and guard==fe(bank['guard']),'nonzero raw guard')
    amps=[fe(v) for v in bank['amplitudes']];weights=[fe(v) for v in bank['weights']]
    check(len(amps)==len(weights)==13,'bank record length');all_amps.append(amps)
    for j in range(13):
        v=Z
        for b in range(13):v=add(v,sc(amps[b],q(-e*b*j)))
        check(weights[j]==sc(mul(guard,v),gamma),'raw weight forward transform')
    recip=inverse(sc(guard,13*gamma))
    for b in range(13):
        v=Z
        for j in range(13):v=add(v,sc(weights[j],q(e*b*j)))
        check(mul(v,recip)==amps[b],'raw weight inverse transform')
    bank_sum=[[Z]*13 for _ in range(13)]
    for j in range(13):
        V=literal_inverse(alpha,beta,e,d,j,guard)
        for r in range(13):
            for c in range(13):bank_sum[r][c]=add(bank_sum[r][c],sc(mul(weights[j],V[r][c]),inv13))
        if bi==15 and j==12:last_inverse=V
    check(any(v!=Z for row in bank_sum for v in row),'nonzero physical bank matrix')
    for r in range(13):
        for c in range(13):all_sum[r][c]=add(all_sum[r][c],bank_sum[r][c])
    # Independent literal Weyl extraction validates all 169 coefficients of
    # each bank against its claimed normalized sector amplitudes.
    for a in range(13):
        for b in range(13):
            extracted=Z
            for t in range(13):extracted=add(extracted,sc(bank_sum[(t+a)%13][t],q(-b*t)*inv13))
            predicted=sc(mul(power(alpha,e*a%13),amps[b]),gamma*G(e,d,a,b))
            check(extracted==predicted,'per bank literal Weyl coefficient')
    bank_receipts.append({'index':bi,'orientation':[e,d],'guard':guard,'nonzero_matrix':True,'branches':13})
    print('literal bank',bi+1,'/ 16 passed',round(time.time()-started,2),'s',flush=True)
for r in range(13):
    for c in range(13):
        check(all_sum[r][c]==sc(O,q(-r*c)),'literal Fourier target entry')
        check(all_sum[r][c]==fe(C['matrix'][r][c]),'claimed matrix entry')
# Recompute the 13 actual-root sector ranks and all 169 sector residuals.
sector_ranks=[]
for b in range(13):
    sector=[[sc(power(tuple(bank['alpha']),bank['epsilon']*a%13),G(bank['epsilon'],bank['delta'],a,b)) for bank in banks] for a in range(13)]
    for a in range(13):
        val=Z
        for i in range(16):val=add(val,mul(sector[a][i],all_amps[i][b]))
        check(val==sc(O,f(a,b)),'actual root sector equality')
    rr=[row[:] for row in sector];row=0
    for col in range(16):
        pivot=next((i for i in range(row,13) if rr[i][col]!=Z),None)
        if pivot is None:continue
        rr[pivot],rr[row]=rr[row],rr[pivot];scale=inverse(rr[row][col]);rr[row]=[mul(scale,v) for v in rr[row]]
        for i in range(row+1,13):
            fac=rr[i][col]
            if fac!=Z:rr[i]=[sub(v,mul(fac,w)) for v,w in zip(rr[i],rr[row])]
        row+=1
        if row==13:break
    sector_ranks.append(row)
check(sector_ranks==[13,9,11,12,13,13,13,13,13,13,12,11,9],'actual root sector ranks')
# Three falsification controls, including direct raw-weight perturbation.
controls={
 'omitted_1_over_13':sum(sc(all_sum[r][c],13)!=sc(O,q(-r*c)) for r in range(13) for c in range(13)),
 'opposite_Fourier_sign':sum(all_sum[r][c]!=sc(O,q(r*c)) for r in range(13) for c in range(13)),
 'last_raw_weight_plus_1':sum(add(all_sum[r][c],sc(last_inverse[r][c],inv13))!=sc(O,q(-r*c)) for r in range(13) for c in range(13))}
check(controls=={'omitted_1_over_13':169,'opposite_Fourier_sign':144,'last_raw_weight_plus_1':91},'falsification controls')
print('Degree 11 literal certificate PASSED',flush=True)
# Fresh base-field arithmetic gate for all 2704 ordered cross pairs.
def rref(A):
    A=[[v%P for v in row] for row in A];piv=[];r=0
    for c in range(len(A[0])):
        k=next((i for i in range(r,len(A)) if A[i][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];s=pow(A[r][c],-1,P);A[r]=[v*s%P for v in A[r]]
        for i in range(len(A)):
            if i!=r:
                s=A[i][c];A[i]=[(u-s*v)%P for u,v in zip(A[i],A[r])]
        piv.append(c);r+=1
        if r==len(A):break
    return A,piv

def forced(y,a,b):
    den=G(1,1,a,b);pivot=G(-1,1,13-b,b)
    assert den and pivot
    return (f(a,b)-pow(y,13-a-b,P)*G(-1,1,a,b)*pow(pivot,-1,P))*pow(den,-1,P)%P
lines={};det_receipts=[];root_hist=Counter();fresh_gates=[];degree_hist=Counter()
census=json.loads((ROOT/'CROSS_GATE_CENSUS.json').read_text())
for yy in range(1,53):
    A=[[forced(yy,a+j,b) for j in range(8)] for b,a in [(1,1),(1,2),(1,3),(1,4),(2,2),(2,3)]]
    R,piv=rref(A)
    check(piv==list(range(6)),'prime cross affine rank')
    cc=[(-R[i][7])%P for i in range(6)]+[0,1];nn=[(-R[i][6])%P for i in range(6)]+[1,0]
    lines[str(yy)]={'c':cc,'n':nn}
    check(lines[str(yy)]==census['lines'][str(yy)],'affine line census binding')
    for lam in range(53):
        hh=[(cc[j]+lam*nn[j])%P for j in range(8)]
        check(all(sum(row[j]*hh[j] for j in range(8))%P==0 for row in A),'all base affine recurrences')
        roots0=[v for v in range(1,53) if sum(hh[j]*pow(v,j,P) for j in range(8))%P==0]
        root_hist[len(roots0)]+=1
        check(len(roots0)<7,'seven base roots excluded')
    UU=[forced(yy,a,3) for a in range(1,10)]
    for zz in range(1,53):
        VV=[pow(zz,a,P)*G(1,-1,a,3)*pow(G(1,1,a,3),-1,P)%P for a in range(1,10)]
        E=[];F=[]
        for s in (0,1):
            E.append([sum(hh[j]*UU[s+j] for j in range(8))%P for hh in (cc,nn)])
            F.append([sum(hh[j]*VV[s+j] for j in range(8))%P for hh in (cc,nn)])
        gate=ps(pm(E[0],F[1]),pm(E[1],F[0]));deg=len(gate)-1;gate=gate+[0]*(3-len(gate))
        degree_hist[deg]+=1
        check(deg>=0,'nonzero cross compatibility polynomial')
        fresh_gates.append({'y':yy,'z':zz,'quadratic':gate,'degree':deg})
        for lam in range(53):
            hh=[(cc[j]+lam*nn[j])%P for j in range(8)]
            ee=[sum(hh[j]*UU[s+j] for j in range(8))%P for s in (0,1)]
            ff=[sum(hh[j]*VV[s+j] for j in range(8))%P for s in (0,1)]
            check((ee[0]*ff[1]-ee[1]*ff[0])%P==sum(gate[j]*pow(lam,j,P) for j in range(3))%P,'all base parameter determinant evaluations')
check(fresh_gates==census['gates'],'full cross census binding')
check(dict(degree_hist)=={2:2655,1:47,0:2},'cross degree histogram')
constants=[x for x in fresh_gates if x['degree']==0]
check(constants==[{'y':25,'z':28,'quadratic':[27,0,0],'degree':0},{'y':46,'z':4,'quadratic':[30,0,0],'degree':0}],'constant obstruction exceptions')
check(dict(root_hist)=={0:1041,1:1006,2:521,3:150,4:32,5:5,6:1},'one side base root histogram')
for b in (1,2,3):
    a=13-b
    check(G(-1,1,a,b)!=0 and all(G(e,d,a,b)==0 for e,d in [(1,1),(1,-1),(-1,-1)]),'isolated cross row')
for a in range(1,10):
    check(G(-1,-1,a,3)==0 and G(1,1,a,3)!=0,'b3 support vanishings')
    check((G(1,-1,a,3)!=0)==(a in (1,2)),'b3 opposite cross support')
# Rebuild a base-field 18-bank witness and check original inverses freshly.
support=[1,2,6,7,12,21,22,26]
records=[(1,1,a) for a in support]+[(-1,1,1),(1,-1,1)]+[(-1,-1,a) for a in support]
baseamps=[[0]*13 for _ in records];baseranks=[]
for b in range(13):
    mat=[[G(e,d,a,b)*pow(alpha,e*a%13,P)%P for e,d,alpha in records]+[f(a,b)] for a in range(13)]
    rr,pivs=rref(mat);check(18 not in pivs,'18 witness sector consistency');baseranks.append(len(pivs))
    sol=[0]*18
    for i,k in enumerate(pivs):sol[k]=rr[i][18]
    check(all(sum(row[k]*sol[k] for k in range(18))%P==row[-1] for row in mat),'18 witness sector residual')
    for i,v in enumerate(sol):baseamps[i][b]=v
basesum=[[0]*13 for _ in range(13)];basecert=[]
for i,(e,d,alpha) in enumerate(records):
    guard=(-pow(alpha,13,P))%P;check(guard!=0,'18 witness nonzero guard')
    weights=[guard*gamma*sum(baseamps[i][b]*q(-e*b*j) for b in range(13))%P for j in range(13)]
    bankmat=[[0]*13 for _ in range(13)]
    for j in range(13):
        mm=[[(int(r==c)*(1-q(e*d*j+d*c))-int(r==(c+e)%13)*alpha)%P for c in range(13)]+[int(r==c) for c in range(13)] for r in range(13)]
        rr,pivs=rref(mm);check(pivs==list(range(13)),'18 witness literal inverse rank')
        vv=[row[13:] for row in rr]
        for r in range(13):
            for c in range(13):
                check(((1-q(e*d*j+d*r))*vv[r][c]-alpha*vv[(r-e)%13][c])%P==int(r==c),'18 witness left inverse')
                check(((1-q(e*d*j+d*c))*vv[r][c]-alpha*vv[r][(c+e)%13])%P==int(r==c),'18 witness right inverse')
                bankmat[r][c]=(bankmat[r][c]+inv13*weights[j]*vv[r][c])%P
    check(any(v for row in bankmat for v in row),'18 witness nonzero matrix')
    for r in range(13):
        for c in range(13):basesum[r][c]=(basesum[r][c]+bankmat[r][c])%P
    basecert.append({'epsilon':e,'delta':d,'alpha':alpha,'beta':1,'guard':guard,'amplitudes':baseamps[i],'weights':weights})
for r in range(13):
    for c in range(13):check(basesum[r][c]==q(-r*c),'18 witness literal Fourier target')
# Degrees already attained under scalar extension of 2,3,5,7,11.
residual=[d for d in range(2,232) if math.gcd(d,2310)==1]
check(residual[0]==13,'first residual degree')
result={'verdict':'ACCEPT_SCOPE_LIMITED','certificate_sha256':digest(cert_bytes),'field_irreducible':True,
 'frobenius_remainders':frob,'frobenius_linear_gcd':gcd,'checks':dict(checks),'literal_banks':bank_receipts,
 'inverse_algorithm':'13-term geometric series of the literal operator A, followed by both original matrix products',
 'field_inverse_algorithm':'prime-polynomial extended Euclid', 'falsification_controls':controls,'actual_root_sector_ranks':sector_ranks,
 'cross_gate_counts':dict(degree_hist),'constant_cross_gates':constants,'basefield_root_histogram':dict(root_hist),
 'source_receipts':source_receipts,'support_53rd_powers':root_frob,'base_18_sector_ranks':baseranks,
 'residual_degrees_up_to_231':residual,'inherited_lower_bound':'At least seven effective nonzero same-sign nodes on each side, plus two nonzero cross singletons, from pinned ACCEPTED_LOWER_REVIEW.md section 1; large original lower-minor computation not replayed.',
 'scope':'Exactly one effective nonzero alpha node per cross orientation. Explicit 16-bank minimum at d=11 and 11|d; prime-field-cross restricted minimum 18 for gcd(d,210)=1. No complete unrestricted degree classification or priority claim.',
 'runtime_seconds':time.time()-started}
(OUT/'ARITHMETIC.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'FRESH_BASE18_CERTIFICATE.json').write_text(json.dumps({'banks':basecert,'matrix':basesum},indent=2)+'\n')
(OUT/'FRESH_CROSS_CENSUS.json').write_text(json.dumps({'lines':lines,'gates':fresh_gates,'counts':dict(degree_hist)},indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'runtime_seconds':result['runtime_seconds'],'checks':dict(checks)},indent=2),flush=True)
