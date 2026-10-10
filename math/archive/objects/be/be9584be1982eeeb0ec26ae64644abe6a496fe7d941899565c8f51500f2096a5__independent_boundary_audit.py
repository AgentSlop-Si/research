#!/usr/bin/env python3
"""Fresh audit. Reads JSON certificates only; never imports/executes source programs.
Exact SymPy algebraic-domain polynomial arithmetic; no floating point or solver.
"""
import json, hashlib, itertools, time
from pathlib import Path
import sympy as sy
from sympy.polys.fields import field
from sympy.polys.rings import ring

OUT=Path(__file__).resolve().parent
SRC=Path('boundary_factorization_escape_0328')
START=time.monotonic()
CHECKS=[]; GUARDS=[]; CERTS=[]; NEGATIVE=[]
def ok(label, condition=True, **data):
    if not condition: raise AssertionError(label)
    CHECKS.append({'check':label,**data})
def exact_equal(a,b):
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):
        return len(a)==len(b) and all(exact_equal(x,y) for x,y in zip(a,b))
    if isinstance(a,sy.MatrixBase) and isinstance(b,sy.MatrixBase): return a==b
    if type(a) in (dict,str) or type(b) in (dict,str): return a==b
    try: return not bool(a-b)
    except TypeError: return a==b
def equal(label,a,b): ok(label,exact_equal(a,b))
zsymbol=sy.Symbol('z')
K=sy.QQ.algebraic_field(sy.CRootOf(zsymbol**4+1,0))
F,w=field('w',K)
z=F(K.unit)
S,a,b,c,d=ring('a,b,c,d',F.to_domain())
free=[a,b,c,d]
PI=[(i+1)%8 for i in range(8)]
SIG=[2,7,5,0,6,1,3,4]
J=[j for j in range(8) if 0 not in {j,PI[j],SIG[j]}]
allowed=lambda r,j: r not in {j,PI[j],SIG[j]}

def poly(data):
    p=F.ring.zero; seen=set()
    for ex, coeff in data:
        assert len(ex)==1 and isinstance(ex[0],int) and ex[0]>=0 and ex[0] not in seen
        seen.add(ex[0]); assert 1<=len(coeff)<=4
        v=K.zero
        for i,q in enumerate(coeff): v+=K.convert(sy.Rational(q))*K.unit**i
        assert v
        p[(ex[0],)]=v
    return p

def frac(data):
    n,de=poly(data['numer']),poly(data['denom']); assert de
    return F(n)/F(de)

def den_guard(label, denominator, guards):
    rem=denominator.monic()
    used=[]
    for name,g in guards:
        g=F(g).numer
        assert g
        count=0
        while rem.degree()>0:
            h=rem.gcd(g)
            if h.degree()<=0: break
            rem=rem.exquo(h); count+=1
        if count: used.append({'guard':name,'gcd_rounds':count})
    ok(label+' denominator allowed',rem.degree()==0)
    rogue=(w-137).numer
    for name,g in guards:
        ok(label+' forbidden pole distinct from '+name,rogue.gcd(F(g).numer).degree()==0)
    # If this extraneous pole were appended to the stored denominator, no legal
    # guard could remove it. This is a rejection test of denominator coverage.
    poisoned=denominator*rogue
    for name,g in guards:
        while poisoned.degree()>0:
            h=poisoned.gcd(F(g).numer)
            if h.degree()<=0: break
            poisoned=poisoned.exquo(h)
    ok(label+' extraneous pole rejected',poisoned.degree()==1 and exact_equal(poisoned.monic(),rogue))
    GUARDS.append({'fraction':label,'denominator_degree':int(denominator.degree()),'guards_used':used,'extraneous_w_minus_137_pole_rejected':True})

def check_frac(C,key,value,guards,case):
    stored=C[key]
    f=frac(stored)
    equal(case+': '+key+' reconstructed',f,value)
    den_guard(case+': '+key,poly(stored['denom']),guards)
    den_guard(case+': '+key+' regenerated',F(value).denom,guards)
    # Deliberately change each stored fraction by a nonzero rational.
    ok(case+': '+key+' perturbation rejected',not exact_equal(f+F(sy.Rational(1,103)),value))
    NEGATIVE.append(case+':'+key+':numerator-value')
    return f

def bezout(C,key,left,right,rhs,case):
    B=C[key]
    equal(case+': '+key+' left tied',poly(B['left']),left)
    equal(case+': '+key+' right tied',poly(B['right']),right)
    s,t=poly(B['s']),poly(B['t'])
    want=F(rhs).numer
    if 'gcd' in B: equal(case+': '+key+' stored gcd',poly(B['gcd']),want)
    equal(case+': '+key+' exact identity',s*left+t*right,want)
    ok(case+': '+key+' wrong target rejected',not exact_equal(s*left+t*right,want+1))
    ok(case+': '+key+' changed multiplier rejected',not exact_equal((s+1)*left+t*right,want))
    NEGATIVE.extend([case+':'+key+':target',case+':'+key+':multiplier'])

def constant(label,p):
    p=S(p)
    ok(label+' no hidden free ratio',all(m==(0,0,0,0) for m in p))
    return p.get((0,0,0,0),F.zero)

def affine(label,p,var):
    p=S(p); i=free.index(var); m=tuple(int(j==i) for j in range(4)); zero=(0,0,0,0)
    ok(label+' exact affine support',all(e in (zero,m) for e in p))
    A=p.get(m,F.zero); D=p.get(zero,F.zero)
    equal(label+' polynomial identity',p,S(A)*var+S(D))
    return A,D

class MatrixModel:
    def __init__(self,t,ww=w):
        self.w=S(ww); self.t=list(map(S,t))
        self.M=[[S(z**(r*(2*k))) + (-1 if j%2 else 1)*self.t[k]*S(z**(r*(2*k+1)))
                 for j in range(8) for k in [j//2]] for r in range(8)]
        self.B=[self.M[0][j]+self.w*self.M[7][j] for j in range(8)]
    def bc(self,r,j):
        assert j in J and 1<=r<8 and allowed(r,j)
        k=SIG[j]; M=self.M; B=self.B
        return B[k]*M[r][j]-B[j]*M[r][k], B[k]*M[r-1][j]-B[j]*M[r-1][k]
    def R(self,r,j,k):
        bj,cj=self.bc(r,j); bk,ck=self.bc(r,k)
        return bj*ck-bk*cj
    def L(self,r,j,k,l):
        assert SIG[j]==k and SIG[k]==l and allowed(r,j) and allowed(r,k)
        M=self.M; B=self.B
        det=lambda i,j: M[r][i]*M[r-1][j]-M[r][j]*M[r-1][i]
        return B[l]*det(j,k)-B[k]*det(j,l)+B[j]*det(k,l)
    def E(self,l,r,j):
        assert allowed(r,l)
        bj,cj=self.bc(r,j)
        return bj*self.M[r-1][l]-cj*self.M[r][l]

def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),0) for j in range(len(B[0]))] for i in range(len(A))]

def foundational_checks():
    equal('cyclotomic defining modulus',K.mod.to_list(),[sy.QQ(1),sy.QQ(0),sy.QQ(0),sy.QQ(0),sy.QQ(1)])
    for seed in [17,23,41,59]:
        aa=sum(sy.Rational(seed+i,seed+2*i+1)*zsymbol**i for i in range(4))
        bb=sum(sy.Rational(2*seed+i,seed+3*i+2)*zsymbol**i for i in range(4))
        toK=lambda expr:sum((K.convert(q)*K.unit**monom[0] for monom,q in sy.Poly(expr,zsymbol).terms()),K.zero)
        for title,expr,value in [('product',aa*bb,toK(aa)*toK(bb)),('cube',aa**3,toK(aa)**3)]:
            remainder=sy.rem(sy.Poly(expr,zsymbol),sy.Poly(zsymbol**4+1,zsymbol)).as_expr()
            equal(f'independent formal-z remainder {seed} {title}',value,toK(remainder))
    equal('z fourth power',z**4,F(-1)); equal('z eighth power',z**8,F(1))
    ok('primitive eighth root',all(not exact_equal(z**i,1) for i in [1,2,4]))
    equal('Eisenstein translated coefficients',sy.Poly((zsymbol+1)**4+1,zsymbol).all_coeffs(),[1,4,6,4,2])
    equal('row zero eligible columns',J,[1,2,4,5,6])
    for name,m in [('pi',PI),('sigma',SIG)]:
        order=[0]
        for i in range(7): order.append(m[order[-1]])
        ok(name+' Hamiltonian',len(set(order))==8 and m[order[-1]]==0)
    ok('disjoint directed support cycles',all(PI[j]!=SIG[j] for j in range(8)))
    T=[[S.zero for j in range(8)] for i in range(8)]
    H=[[S.zero for j in range(8)] for i in range(8)]
    FF=[[S(z**(i*j)) for j in range(8)] for i in range(8)]
    for i in range(8): T[i][i]=S.one if i%2==0 else free[i//2]
    for k in range(4):
        p=2*k; H[p][p]=H[p][p+1]=H[p+1][p]=S.one; H[p+1][p+1]=-S.one
    M=MatrixModel(free)
    equal('all 64 Fourier entries independently multiplied',matmul(matmul(FF,T),H),M.M)
    equal('actual Fourier scale reconstruction',matmul(M.M,H),[[2*q for q in row] for row in matmul(FF,T)])
    equal('anchor square is twice identity',matmul(H,H),[[S(2 if i==j else 0) for j in range(8)] for i in range(8)])
    for i in range(4):
        N=1+w*z**(-2*i); D=1+w*z**(-(2*i+1))
        equal('pair '+str(i)+' even B',M.B[2*i],S(N)+free[i]*S(D))
        equal('pair '+str(i)+' odd B',M.B[2*i+1],S(N)-free[i]*S(D))
        equal('pair '+str(i)+' D zero forces nonzero N',1+(-z**(2*i+1))*z**(-2*i),1-z)
    ok('1-z is nonzero',not exact_equal(1-z,0))
    for r in range(1,8):
        cols=[j for j in J if allowed(r,j)]
        for j,k in itertools.combinations(cols,2):
            bj,cj=M.bc(r,j); bk,ck=M.bc(r,k)
            # u_r is represented by a new outer polynomial indeterminate.
            U,uu=ring('u',S.to_domain())
            equal(f'row {r} columns {j},{k} raw resultant necessity',U(M.R(r,j,k)),U(ck)*(U(bj)+uu*U(cj))-U(cj)*(U(bk)+uu*U(ck)))
    for r,j,k,l in [(1,4,6,3),(2,4,6,3),(3,5,1,7),(4,2,5,1),(7,2,5,1)]:
        equal(f'chain quotient polynomial identity {r},{j},{k},{l}',M.R(r,j,k),M.B[k]*M.L(r,j,k,l))
    # Universal no-division identities from the full off-support equations.
    G,br,bk,mr,mk,pr,pk,ur,v=ring('br,bk,mr,mk,pr,pk,ur,v',sy.QQ)
    h=bk*(mr+ur*pr)-br*(mk+ur*pk)
    equal('full equation to pivot minor without division',h,bk*(mr+ur*pr+v*(mk+ur*pk))-(mk+ur*pk)*(br+v*bk))
    Ge,B,C,L,P,U=ring('B,C,L,P,U',sy.QQ)
    equal('zero edge eliminant necessity without division',B*P-C*L,P*(B+U*C)-C*(L+U*P))
    # Partition is evaluated on all Boolean zero/nonzero patterns.
    n=0
    for zw,z1,z5,z6,z3 in itertools.product([False,True],repeat=5):
        if not (zw or z1 or z5 or z6): continue
        cats=[zw,not zw and z1,not zw and not z1 and z5,not zw and not z1 and not z5 and z6 and z3,not zw and not z1 and not z5 and z6 and not z3]
        assert sum(cats)==1; n+=1
    ok('boundary ordered partition exhaustive and disjoint',n==30,zero_patterns=n)
    # Full normalized RHS support, with generic coefficients.
    G,*q=ring(','.join(f'q{i}' for i in range(32)),sy.QQ)
    u,v,x,y=[q[8*i:8*i+8] for i in range(4)]
    U=[[G(int(i==j)) for j in range(8)] for i in range(8)]
    V=[[G(int(i==j)) for j in range(8)] for i in range(8)]
    DX=[[x[i] if i==j else G.zero for j in range(8)] for i in range(8)]
    DY=[[y[i] if i==j else G.zero for j in range(8)] for i in range(8)]
    for j in range(8): U[PI[j]][j]=u[PI[j]]; V[SIG[j]][j]=v[j]
    L=matmul(U,DY); R=matmul(DX,V)
    for i in range(8):
        for j in range(8):
            expected=(x[i]+y[i] if i==j else (u[i]*y[j] if i==PI[j] else (x[i]*v[j] if i==SIG[j] else G.zero)))
            equal(f'normalized RHS ({i},{j})',L[i][j]+R[i][j],expected)

def finish_pair(C,case,Q,H,q,h,guards):
    fq=check_frac(C,'q_fraction',q,guards,case); fh=check_frac(C,'h_fraction',h,guards,case)
    Qs,Hs=poly(C['Q']),poly(C['H'])
    equal(case+': Q monic normalization',Qs,poly(C['q_fraction']['numer']).monic())
    equal(case+': H monic normalization',Hs,poly(C['h_fraction']['numer']).monic())
    bezout(C,'Q_H_bezout',Qs,Hs,1,case)
    CERTS.append({'case':case,'final_degrees':[int(Qs.degree()),int(Hs.degree())],'final_identity':'1'})

def audit_wzero():
    case='w=0'; C=json.loads((SRC/'WZERO_CERTIFICATE.json').read_text()); guards=[]
    M=MatrixModel([a,b,c,w],0)
    for j in [2,4,6]: equal(case+f': c[1,{j}] identically zero',M.bc(1,j)[1],S.zero)
    A6,D6=affine(case+': b16',M.bc(1,6)[0],b)
    A4,D4=affine(case+': b14',M.bc(1,4)[0],c)
    for k,val in [('A6',A6),('D6',D6),('A4',A4),('D4',D4)]: check_frac(C,k,val,guards,case)
    bezout(C,'A6_D6_bezout',poly(C['A6']['numer']),poly(C['D6']['numer']),1,case)
    bezout(C,'A4_D4_bezout',poly(C['A4']['numer']),poly(C['D4']['numer']),1,case)
    guards += [('num A6',F(poly(C['A6']['numer']))),('num A4',F(poly(C['A4']['numer'])))]
    t1=check_frac(C,'t1',-D6/A6,guards,case); t2=check_frac(C,'t2',-D4/A4,guards,case)
    M=MatrixModel([a,t1,t2,w],0)
    q=constant(case+': b12',M.bc(1,2)[0]); check_frac(C,'q_fraction',q,guards,case)
    Q=poly(C['Q']); equal(case+': Q derived monic',Q,poly(C['q_fraction']['numer']).monic())
    A0,P0=affine(case+': R245',M.R(2,4,5),a)
    check_frac(C,'A0',A0,guards,case); check_frac(C,'P0',P0,guards,case)
    bezout(C,'Q_A0_bezout',Q,poly(C['A0']['numer']),1,case)
    guards += [('num A0 (given Q=0)',F(poly(C['A0']['numer'])))]
    t0=check_frac(C,'t0',-P0/A0,guards,case)
    M=MatrixModel([t0,t1,t2,w],0)
    h=constant(case+': R314',M.R(3,1,4))
    finish_pair(C,case,Q,None,q,h,guards)

def ND(): return ([1+w*z**(-2*i) for i in range(4)],[1+w*z**(-(2*i+1)) for i in range(4)])
def pair_guards(indices,nonzero_w=True):
    N,D=ND(); return ([('w',w)] if nonzero_w else [])+[(f'{letter}{i}',values[i]) for i in indices for letter,values in [('N',N),('D',D)]]

def audit_b1_b5(which):
    case=which; C=json.loads((SRC/(case+'_CERTIFICATE.json')).read_text()); N,D=ND()
    indices=[0,1,2] if which=='B1' else [1,2]; guards=pair_guards(indices)
    t0=N[0]/D[0] if which=='B1' else a
    M=MatrixModel([t0,-N[1]/D[1],N[2]/D[2],d])
    for j in ([1,2,5] if which=='B1' else [2,5]): equal(case+f': B{j}=0',M.B[j],S.zero)
    equal(case+': B4=2N2',M.B[4],S(2*N[2]))
    A,Dd=affine(case+': L461/w',M.L(1,4,6,3)*S(1/w),d)
    check_frac(C,'A',A,guards,case); check_frac(C,'D',Dd,guards,case)
    bezout(C,'A_D_bezout',poly(C['A']['numer']),poly(C['D']['numer']),1,case)
    guards += [('num A',F(poly(C['A']['numer'])))]
    t3=check_frac(C,'t3',-Dd/A,guards,case)
    M=MatrixModel([t0,-N[1]/D[1],N[2]/D[2],t3])
    q=constant(case+': L462',M.L(2,4,6,3))
    h=constant(case+(': R314' if which=='B1' else ': E5_24'),M.R(3,1,4) if which=='B1' else M.E(5,2,4))
    finish_pair(C,case,None,None,q,h,guards)

def audit_b6_b3():
    case='B6_B3'; C=json.loads((SRC/(case+'_CERTIFICATE.json')).read_text()); N,D=ND(); guards=pair_guards([1,2,3],False)
    M=MatrixModel([a,N[1]/D[1],-N[2]/D[2],-N[3]/D[3]])
    for j in [3,4,6]: equal(case+f': B{j}=0',M.B[j],S.zero)
    equal(case+': B5=2N2',M.B[5],S(2*N[2]))
    A,Dd=affine(case+': L153',-M.L(3,5,1,7),a)
    check_frac(C,'A',A,guards,case); check_frac(C,'D',Dd,guards,case)
    bezout(C,'A_D_bezout',poly(C['A']['numer']),poly(C['D']['numer']),1,case)
    guards += [('num A',F(poly(C['A']['numer'])))]
    t0=check_frac(C,'t0',-Dd/A,guards,case)
    M=MatrixModel([t0,N[1]/D[1],-N[2]/D[2],-N[3]/D[3]])
    q=constant(case+': L254',M.L(4,2,5,1)); h=constant(case+': L257',M.L(7,2,5,1))
    finish_pair(C,case,None,None,q,h,guards)

def audit_b6_edge():
    case='B6_ZEROEDGE'; C=json.loads((SRC/(case+'_CERTIFICATE.json')).read_text()); N,D=ND(); guards=pair_guards([2,3])
    M=MatrixModel([a,b,-N[2]/D[2],-N[3]/D[3]])
    for j in [4,6]: equal(case+f': B{j}=0',M.B[j],S.zero)
    A1,D1=affine(case+': E6_12',M.E(6,1,2),b)
    check_frac(C,'A1',A1,guards,case); check_frac(C,'D1',D1,guards,case)
    bezout(C,'A1_D1_bezout',poly(C['A1']['numer']),poly(C['D1']['numer']),w,case)
    guards += [('num A1 (w nonzero)',F(poly(C['A1']['numer'])))]
    t1=check_frac(C,'t1',-D1/A1,guards,case)
    M=MatrixModel([a,t1,-N[2]/D[2],-N[3]/D[3]])
    A0,D0=affine(case+': E6_25',M.E(6,2,5),a)
    check_frac(C,'A0',A0,guards,case); check_frac(C,'D0',D0,guards,case)
    bezout(C,'A0_D0_bezout',poly(C['A0']['numer']),poly(C['D0']['numer']),1,case)
    guards += [('num A0',F(poly(C['A0']['numer'])))]
    t0=check_frac(C,'t0',-D0/A0,guards,case)
    M=MatrixModel([t0,t1,-N[2]/D[2],-N[3]/D[3]])
    numer=[]
    for j,ex in zip([1,2],C['equations']):
        assert ex['name']=='E4'+str(j)
        val=constant(case+': '+ex['name'],M.E(6,4,j))
        check_frac(ex,'fraction',val,guards,case+':'+ex['name'])
        numer.append(poly(ex['fraction']['numer']))
    bezout(C,'final_bezout',*numer,1,case)
    CERTS.append({'case':case,'final_degrees':[int(p.degree()) for p in numer],'final_identity':'1'})

def snapshot():
    old=json.loads((OUT/'SOURCE_SEALS_BEFORE.json').read_text())
    now={p:{'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest(),'bytes':Path(p).stat().st_size} for p in old}
    equal('all original bytes unchanged',now,old)
    (OUT/'SOURCE_SEALS_AFTER.json').write_text(json.dumps(now,indent=2)+'\n')
    return len(now)

def manifests():
    files=[]
    for root in [SRC,Path('adjacent_obstruction_independent_audit_0323'),Path('adjacent_anchor_construction_0304'),Path('fourier8_orbit_independent_audit_0312')]:
        path=root/'SHA256SUMS.txt'
        if not path.exists(): continue
        for line in path.read_text().splitlines():
            if not line.strip(): continue
            sha,name=line.split(None,1); name=name.strip().lstrip('*')
            p=root/name
            ok('source manifest '+str(p),hashlib.sha256(p.read_bytes()).hexdigest()==sha)
            files.append(str(p))
    return len(files)

# Fresh rational inverse sums; sources are not used for control construction.
def controls():
    records=[]
    scenarios=[('u0_zero', [0], []),('v1_zero',[],[1]),('v5_v6_zero',[],[5,6]),('v3_zero',[],[3]),('v6_zero',[],[6]),('all_edges_zero',list(range(8)),list(range(8))),('mixed_zero_pivots',[0,2,5],[1,3,6])]
    for idx,(name,zu,zv) in enumerate(scenarios):
        u=[sy.Rational(i+2+idx,37+i) for i in range(8)]
        v=[sy.Rational(i+3+idx,53+i) for i in range(8)]
        x=[sy.Rational(11+2*i+idx,71+i) for i in range(8)]
        y=[sy.Rational(19+3*i+idx,97+i) for i in range(8)]
        for i in zu:u[i]=sy.S.Zero
        for i in zv:v[i]=sy.S.Zero
        U=sy.eye(8);V=sy.eye(8)
        for j in range(8):U[PI[j],j]=u[PI[j]];V[SIG[j],j]=v[j]
        assert U.det()!=0 and V.det()!=0 and all(x) and all(y)
        M=U.inv()*sy.diag(*x)+sy.diag(*y)*V.inv()
        Q0=sy.diag(*(1/q for q in x))*U; Q1=V*sy.diag(*(1/q for q in y))
        equal(name+': exact inverse sum',M,Q0.inv()+Q1.inv())
        equal(name+': full matrix equation',U*M*V,U*sy.diag(*y)+sy.diag(*x)*V)
        equal(name+': actual second factor scale',(2*Q0).inv()+(2*Q1).inv(),M/2)
        def quantities(A):
            B=list((U*A)[0,:]); hs=[]; rs=[]; es=[]; zeros=[]
            UMV=U*A*V
            full=[UMV[r,j] for r in range(8) for j in range(8) if allowed(r,j)]
            for j in J: hs.append(B[j]+v[j]*B[SIG[j]])
            for r in range(1,8):
                bc={}
                for j in J:
                    if not allowed(r,j):continue
                    bj=B[SIG[j]]*A[r,j]-B[j]*A[r,SIG[j]]
                    cj=B[SIG[j]]*A[r-1,j]-B[j]*A[r-1,SIG[j]]
                    bc[j]=(bj,cj); hs.append(bj+u[r]*cj)
                for j,k in itertools.combinations(bc,2):
                    bj,cj=bc[j];bk,ck=bc[k];rs.append(bj*ck-bk*cj)
                for l in zv:
                    if allowed(r,l):
                        zeros.append(A[r,l]+u[r]*A[r-1,l])
                        for j,(bj,cj) in bc.items():es.append(bj*A[r-1,l]-cj*A[r,l])
            return B,hs,rs,es,zeros,full
        B,hs,rs,es,zeros,full=quantities(M)
        ok(name+': all 40 full off-support equations',all(q==0 for q in full) and len(full)==40)
        ok(name+': all necessary minors',all(q==0 for q in hs),count=len(hs))
        ok(name+': all raw row resultants',all(q==0 for q in rs),count=len(rs))
        ok(name+': all applicable zero-edge equations',all(q==0 for q in zeros),count=len(zeros))
        ok(name+': all applicable zero-edge eliminants',all(q==0 for q in es),count=len(es))
        boundary=u[0]*B[1]*B[5]*B[6]==0
        ok(name+': truly on boundary',boundary)
        branch=('w=0' if u[0]==0 else ('B1' if B[1]==0 else ('B5' if B[5]==0 else ('B6_B3' if B[3]==0 else 'B6_ZEROEDGE'))))
        expected=['w=0','B1','B5','B6_B3','B6_ZEROEDGE','w=0','w=0'][idx]
        equal(name+': expected ordered boundary branch',branch,expected)
        rec={'name':name,'branch':branch,'u':list(map(str,u)),'v':list(map(str,v)),'x':list(map(str,x)),'y':list(map(str,y)),
             'det_U':str(U.det()),'det_V':str(V.det()),'zero_B':[j for j,bj in enumerate(B) if bj==0],
             'pivot_pairs_zero':[j for j in J if B[j]==0 and B[SIG[j]]==0], 'minor_count':len(hs),'resultant_count':len(rs),'zero_edge_equations':len(zeros),'zero_edge_eliminants':len(es),'negative_controls':[]}
        # Perturb off-support entries away from rows 0 and 7 so B stays fixed.
        for r,j in [(2,4),(3,1),(4,2),(6,1)]:
            P=M.copy();P[r,j]+=sy.Rational(1,149)
            Bp,hp,rp,ep,zp,fp=quantities(P)
            equal(name+f': perturb ({r},{j}) preserves all B pivots',Bp,B)
            ok(name+f': perturb ({r},{j}) retains boundary',u[0]*Bp[1]*Bp[5]*Bp[6]==0)
            fail_full=U*P*V!=U*sy.diag(*y)+sy.diag(*x)*V
            fail_eq=any(q!=0 for q in hp+rp+ep+zp+fp)
            ok(name+f': perturb ({r},{j}) rejected by full equation',fail_full)
            # All-zero pivots can make h and R vacuous; zero-edge equations still reject.
            ok(name+f': perturb ({r},{j}) rejected by necessary equations',fail_eq)
            rec['negative_controls'].append({'entry':[r,j],'boundary_preserved':True,'full_equation_rejected':True,'necessary_system_rejected':True,'nonzero_full_offsupport_equations':sum(q!=0 for q in fp),'nonzero_minors':sum(q!=0 for q in hp),'nonzero_resultants':sum(q!=0 for q in rp),'nonzero_edge_eliminants':sum(q!=0 for q in ep),'nonzero_edge_equations':sum(q!=0 for q in zp)})
        records.append(rec)
    return records

def main():
    manifest_n=manifests(); foundational_checks(); print('Foundational identities and partition passed.',flush=True)
    for f in [audit_wzero,lambda:audit_b1_b5('B1'),lambda:audit_b1_b5('B5'),audit_b6_b3,audit_b6_edge]:
        f(); print('Passed',CERTS[-1],flush=True)
    ctrls=controls(); frozen=snapshot()
    results={'verdict':'PASS','arithmetic':'SymPy exact algebraic field with modulus z^4+1 and rational-function / polynomial domains','sympy_version':sy.__version__,'checks':len(CHECKS),'certificates':CERTS,'denominator_checks':len(GUARDS),'perturbation_checks':len(NEGATIVE),'manifest_entries':manifest_n,'preserved_original_files':frozen,'seconds':time.monotonic()-START,'scope':'Complete legal boundary and, using accepted nonboundary theorem, full adjacent-anchor nonsingular diagonal orbit for the fixed support pair; characteristic zero only.'}
    for name,data in [('AUDIT_RESULTS.json',results),('EXACT_CHECK_EVIDENCE.json',CHECKS),('DENOMINATOR_EVIDENCE.json',GUARDS),('CERTIFICATE_PERTURBATIONS.json',NEGATIVE),('FRESH_BOUNDARY_CONTROLS.json',ctrls)]:
        (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(results,indent=2),flush=True)
if __name__=='__main__':main()
