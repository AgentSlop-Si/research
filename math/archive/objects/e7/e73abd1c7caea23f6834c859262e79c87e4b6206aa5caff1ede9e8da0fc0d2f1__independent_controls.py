#!/usr/bin/env python3
"""Independent audit controls. Supplied programs are never imported or executed.
Input packages are read-only. Uses Python stdlib and installed SymPy 1.14.
Polynomial coefficient lists in this file are ascending.
"""
import hashlib, json, math, time
from pathlib import Path
import sympy as sp
from sympy import QQ, GF
HERE=Path(__file__).resolve().parent
SOURCE=Path('diagonal_chirp_classification_0246')
START=time.time()

def write(name, value):
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot():
    paths=list(SOURCE.iterdir())
    paths += [Path(p) for p in json.loads((SOURCE/'SOURCE_HASHES_BEFORE.json').read_text())]
    return {str(p):digest(p) for p in sorted(set(paths)) if p.is_file()}
BEFORE=snapshot();write('SOURCE_HASHES_BEFORE.json',BEFORE)
manifest_checks=[]
for directory in [SOURCE,Path('global_chirp_bank_audit_0235'),Path('joint_chirp_bank_0200')]:
    entries=[]
    for line in (directory/'MANIFEST.sha256').read_text().splitlines():
        want,name=line.split(maxsplit=1);path=directory/name.lstrip('*');got=digest(path)
        assert want==got,(path,want,got);entries.append(name)
    manifest_checks.append({'directory':str(directory),'entries':len(entries),'all_valid':True})
old_before=json.loads((SOURCE/'SOURCE_HASHES_BEFORE.json').read_text())
old_after=json.loads((SOURCE/'SOURCE_HASHES_AFTER.json').read_text())
assert old_before==old_after
assert all(digest(Path(p))==d for p,d in old_before.items())

def cut(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a

def plus(a,b):
    zero=a[0]*0
    return cut([(a[i] if i<len(a) else zero)+(b[i] if i<len(b) else zero) for i in range(max(len(a),len(b)))])
def times(a,b):
    out=[a[0]*0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return cut(out)
def divide(a,b):
    r=cut(a);z=a[0]*0;q=[z]*max(1,len(a)-len(b)+1)
    while any(r) and len(r)>=len(b):
        pos=len(r)-len(b);v=r[-1]/b[-1];q[pos]=v
        for j,y in enumerate(b):r[pos+j]-=v*y
        r=cut(r)
    return cut(q),r
def gcd(a,b):
    while any(b):a,b=b,divide(a,b)[1]
    return [v/a[-1] for v in a]
def evaluate(a,x):
    r=x*0
    for v in a[::-1]:r=r*x+v
    return r
def slope(a):return [j*a[j] for j in range(1,len(a))]
def gaussian(m,q):
    b=q*0+1;row=[]
    for j in range(m+1):
        if j:b=b*(1-q**(m-j+1))/(1-q**j)
        row.append((-1)**(m-j)*b)
    return row

def prime(p):
    return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def distinct_factors(N):return [d for d in range(2,N+1) if N%d==0 and prime(d)]
def raw_remainder(a,b,p):
    a=cut([v%p for v in a]);b=cut([v%p for v in b])
    inv=pow(b[-1],-1,p)
    while any(a) and len(a)>=len(b):
        i=len(a)-len(b);v=a[-1]*inv%p
        for j,c in enumerate(b):a[i+j]=(a[i+j]-v*c)%p
        a=cut(a)
    return a

def raw_gcd(a,b,p):
    while any(b):a,b=b,raw_remainder(a,b,p)
    return [v*pow(a[-1],-1,p)%p for v in a]
def raw_gaussian(m,q,p):
    row=[];value=1
    for j in range(m+1):
        if j:value=value*(1-pow(q,m-j+1,p))*pow(1-pow(q,j,p),-1,p)%p
        row.append((-1)**(m-j)*value%p)
    return row

def trial_guards(N,p,q):
    assert prime(p) and (p-1)%N==0
    assert pow(q,N,p)==1 and all(pow(q,N//d,p)!=1 for d in distinct_factors(N))
    t=raw_gaussian((N-1)//2,q,p);dt=[j*t[j]%p for j in range(1,len(t))]
    return t,len(raw_gcd(t,dt,p))-1,len(raw_gcd(t,[-1]+[0]*(N-1)+[1],p))-1

rows=json.loads((SOURCE/'MODULAR_CERTIFICATES.json').read_text())
assert [row['N'] for row in rows]==list(range(5,1002,4))
cert_results=[];bad=[]
for row in rows:
    N,p,q=row['N'],row['prime_p'],row['primitive_q'];m=(N-1)//2
    t,gs,gr=trial_guards(N,p,q)
    assert row['minimum']==m and t==row['T'] and gs==gr==0
    dt=[j*t[j]%p for j in range(1,m+1)]
    lhs=[0]*(2*m+1)
    for a,b in [(row['squarefree_bezout_u'],t),(row['squarefree_bezout_v'],dt)]:
        for i,x in enumerate(a):
            for j,y in enumerate(b):lhs[i+j]=(lhs[i+j]+x*y)%p
    assert lhs[0]==1 and not any(lhs[1:])
    for trial in row['trials']:
        tt,gst,grt=trial_guards(N,trial['p'],trial['q'])
        assert (gst,grt)==(trial['squarefree_gcd_degree'],trial['resonance_gcd_degree'])
        if gst or grt:bad.append({'N':N,**trial})
    assert (row['trials'][-1]['p'],row['trials'][-1]['q'])==(p,q)
    cert_results.append({'N':N,'p':p,'q':q,'squarefree_gcd_degree':gs,'resonance_gcd_degree':gr,'bezout_identity':True})
write('CERTIFICATE_AUDIT.json',{'verified':len(rows),'exact_coverage':'N=5,9,...,1001','independent_T_method':'multiplicative Gaussian binomial formula','independent_resonance_method':'Euclidean gcd with z^N-1','bad_reductions':bad,'certificates':cert_results})
print('All 250 certificates and all saved trial guards verified.',flush=True)

def solve(A,b):
    n=len(b);M=[list(row)+[v] for row,v in zip(A,b)]
    for k in range(n):
        j=next(j for j in range(k,n) if M[j][k])
        M[k],M[j]=M[j],M[k]
        fac=M[k][k];M[k]=[v/fac for v in M[k]]
        for j in range(n):
            if j==k:continue
            fac=M[j][k]
            if fac:M[j]=[x-fac*y for x,y in zip(M[j],M[k])]
    return [row[-1] for row in M]
def determinant(A):
    n=len(A);A=[list(row) for row in A];det=A[0][0]*0+1
    for k in range(n):
        nonzero=[j for j in range(k,n) if A[j][k]]
        if not nonzero:return det*0
        j=nonzero[0]
        if j!=k:A[k],A[j]=A[j],A[k];det=-det
        fac=A[k][k];det*=fac
        for j in range(k+1,n):
            mul=A[j][k]/fac
            for l in range(k+1,n):A[j][l]-=mul*A[k][l]
    return det

def bank_control(N,q,field,all_basis):
    m=(N-1)//2;z=q*0;o=z+1;h=(N+1)//2
    f=[q**((h*k*k)%N) for k in range(2*N)]
    H=[[f[i+j+1] for j in range(m)] for i in range(m)]
    t=solve(H,[-f[i+m+1] for i in range(m)])+[o]
    assert t==gaussian(m,q)
    expected_resonance=[-o,o] if m%2 else [o]
    assert gcd(t,[-o]+[z]*(N-1)+[o])==expected_resonance
    squarefree=gcd(t,slope(t))==[o]
    ans={'N':N,'field':field,'T_from_independent_Hankel_solve':True,'resonance_gcd_degree':len(expected_resonance)-1,'squarefree':squarefree}
    if m%2:return ans
    assert squarefree
    R=[sum((t[j+l+1]*f[l+1] for l in range(m-j)),z) for j in range(m)]
    delta=o+R[0]/t[0]
    product=(-1)**m*q**(-m*(m+1)//2)
    for j in range(1,m+1):product*=o-q**j
    assert delta==product and delta
    ratio=determinant([[f[i+j] for j in range(m+1)] for i in range(m+1)])/determinant([[f[i+j+2] for j in range(m)] for i in range(m)])
    assert ratio==delta
    def mod(v):return divide(v,t)[1]
    def mult(v,w):return mod(times(v,w))
    def matrix(v):
        cols=[mod([z]*j+v)+[z]*m for j in range(m)]
        return [[cols[j][i] for j in range(m)] for i in range(m)]
    def inverse(v):return cut(solve(matrix(v),[o]+[z]*(m-1)))
    def trace(v):
        mat=matrix(v)
        return sum((mat[i][i] for i in range(m)),z)
    variable=[z,o]
    b=mult(mult(R,inverse(variable)),inverse(slope(t)))
    zn=mod([z]*N+[o]);closure=plus([o],[-v for v in zn]);a=mult(closure,b)
    inverse_closure=inverse(closure)
    def ell(y):return trace(mult(a,y))
    moments=[trace(mult(b,mod([z]*k+[o]))) for k in range(N)]
    assert moments==[o-delta]+f[1:N]
    xs=([[o if i==j else z for i in range(N)] for j in range(N)] if all_basis else [[z+i*i+2*i+3 for i in range(N)],[z+(i%3)-1 for i in range(N)]])
    for x in xs:
        y0=mult(mod(x),inverse_closure)
        out=[ell(y0)+delta*x[0]]+[z]*(N-1);y=y0
        for i in range(N-1,0,-1):
            y=plus([x[i]],mult(variable,y));out[i]=ell(y)+delta*x[i]
        wanted=[sum((f[(j-i)%N]*x[j] for j in range(N)),z) for i in range(N)]
        assert out==wanted
    ans.update({'forced_delta_and_determinant_ratio':True,'moment_checks':N,'all_basis_vectors':all_basis,'scan_entry_checks':N*len(xs),'quotient_inverse_method':'Gaussian solve of multiplication matrix','trace_method':'literal multiplication matrix trace'})
    return ans

bank=[];qvar=sp.Symbol('q')
for N in [3,5,7,9,11,13]:
    K=QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(N,qvar),qvar),alias='q')
    for sign in [1,-1]:
        bank.append(bank_control(N,K.unit**sign,'Q(zeta_%d), sign %d'%(N,sign),True))
    print('Exact cyclotomic controls completed for N='+str(N),flush=True)
for N in [17,21,25,45]:
    row=next(v for v in rows if v['N']==N);p=row['prime_p'];K=GF(p)
    for sign in [1,-1]:
        q=K(pow(row['primitive_q'],sign,p));bank.append(bank_control(N,q,'F_%d, sign %d'%(p,sign),N<=25))
    print('Finite bank controls completed for N='+str(N),flush=True)
write('BANK_AUDIT.json',{'cases':bank,'moment_checks':sum(v.get('moment_checks',0) for v in bank),'scan_entry_checks':sum(v.get('scan_entry_checks',0) for v in bank)})

x=sp.Symbol('x');T0=sp.Integer(1);T1=x-1;discs=[]
for n in range(1,9):
    if n==1:T=T1
    else:T0,T1=T1,sp.expand((x-1)*T1+(1-qvar**(n-1))*x*T0);T=T1
    D=sp.Poly(sp.discriminant(T,x),qvar)
    E,remainder=sp.div(D,sp.Poly((qvar-1)**(n*(n-1)//2),qvar))
    assert remainder.is_zero
    expected=math.prod(j**j for j in range(1,n+1))
    assert E.eval(1)==expected
    discs.append({'degree':n,'disc_degree_in_q':D.degree(),'E_at_1':expected,'integer_quotient':all(c.q==1 for c in E.all_coeffs())})
hermite=[]
for n in range(1,17):
    got=int(sp.discriminant(sp.hermite_prob(n,x),x));want=math.prod(j**j for j in range(1,n+1));assert got==want
    hermite.append({'degree':n,'discriminant':str(got)})
write('DISCRIMINANT_AUDIT.json',{'ordinary_discriminants':discs,'hermite_discriminants':hermite})
AFTER=snapshot();assert BEFORE==AFTER;write('SOURCE_HASHES_AFTER.json',AFTER)
summary={'verdict':'PASS within the stated model and finite range','verified_modular_certificates':len(rows),'bad_reduction_trials_rechecked':len(bad),'bank_cases':len(bank),'moment_checks':sum(v.get('moment_checks',0) for v in bank),'scan_entry_checks':sum(v.get('scan_entry_checks',0) for v in bank),'ordinary_discriminant_degrees':list(range(1,9)),'hermite_discriminant_degrees':list(range(1,17)),'protected_files_unchanged':len(BEFORE),'manifest_checks':manifest_checks,'supplied_code_executed_or_imported':False,'sympy_version':sp.__version__,'elapsed_seconds':time.time()-START}
write('AUDIT_RESULTS.json',summary);print(json.dumps(summary,indent=2),flush=True)
