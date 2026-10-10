#!/usr/bin/env python3
"""Fresh review of the prose lemma and its explicit coefficient table.
Imports only our independently authored literal field/matrix control, stdlib,
and installed SymPy. No author/predecessor implementation is executed/imported.
"""
import importlib.util
import itertools
import json
import re
from pathlib import Path
from hashlib import sha256
import sympy as sp

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_literal',HERE/'verify_witness.py')
f=importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
checks=[]
def check(name,truth):
    assert truth,name
    checks.append(name)

q,x,z,y,u,v=sp.symbols('q x z y u v')
Phi=q**4+q**3+q**2+q+1
K=sp.QQ.frac_field(x,z,y,u,v)
def reduce(expr):
    num,den=sp.fraction(sp.cancel(expr))
    a=sp.Poly(num,q,domain=K)
    b=sp.Poly(den,q,domain=K)
    p=sp.Poly(Phi,q,domain=K)
    return (a*sp.invert(b,p)).rem(p).as_expr()
def same(name,a,b):check(name,reduce(a-b)==0)
def sym(a):return sum(sp.Rational(c.numerator,c.denominator)*q**i for i,c in enumerate(a))
S=[[f.O if r==(c+1)%5 else f.Z for c in range(5)] for r in range(5)]
T=[[f.power(f.Q,c) if r==c else f.Z for c in range(5)] for r in range(5)]
# Enumerate all noncommutative words of length <=4 in literal S,T matrices.
# This generates sector columns without using a Gaussian recurrence.
g={}
for eps,ds in ((1,1),(-1,1),(1,-1),(-1,-1)):
    Se,Td=f.mpow(S,eps%5),f.mpow(T,ds%5)
    for length in range(5):
        for r in range(length+1):
            ell=length-r
            A=f.zeros(5)
            for word in itertools.product((0,1),repeat=length):
                if word.count(0)!=r:continue
                B=f.identity(5)
                for letter in word:B=f.mm(B,Se if letter==0 else Td)
                A=f.ma(A,B)
            a,b=(eps*r)%5,(ds*ell)%5
            coeff=f.times(f.elt('1/5'),f.total(f.times(f.power(f.Q,-b*j),A[(j+a)%5][j]) for j in range(5)))
            W=f.mm(f.mpow(S,a),f.mpow(T,b))
            check(f'word_sum_is_Weyl_{eps}_{ds}_{r}_{ell}',A==f.ms(coeff,W))
            g[eps,ds,r,ell]=sym(coeff)
parameters=[x,z,y,v,u]
signs=[(1,1),(1,1),(-1,1),(1,-1),(-1,-1)]
M={}
for b in range(5):
    rows=[]
    for a in range(5):
        row=[]
        for p,(eps,ds) in zip(parameters,signs):
            r=(eps*a)%5
            ell=(ds*b)%5
            row.append(g[eps,ds,r,ell]*p**r if r+ell<=4 else sp.Integer(0))
        rows.append(row)
    M[b]=sp.Matrix(rows)
G=1+q+q**2
P=1+q**4+q**3
c=q+q**4
H=q/(1+q)
claimed={0:sp.Matrix([[1,1,1,1,1],[x,z,y**4,v,u**4],[x**2,z**2,y**3,v**2,u**3],[x**3,z**3,y**2,v**3,u**2],[x**4,z**4,y,v**4,u]]),2:sp.Matrix([[1,1,1,1,1],[G*x,G*z,0,-q*v,0],[q**2*x**2,q**2*z**2,0,0,0],[0,0,q**3*y**2,0,0],[0,0,P*y,0,-q**4*u]]),3:sp.Matrix([[1,1,1,1,1],[-q**4*x,-q**4*z,0,P*v,0],[0,0,0,q**3*v**2,0],[0,0,0,0,q**2*u**2],[0,0,-q*y,0,G*u]])}
for b in (0,2,3):
    for a in range(5):
        for j in range(5):same(f'literal_M{b}_{a}_{j}',M[b][a,j],claimed[b][a,j])
# Literal generic determinant identities, with all scalar factors displayed.
same('M2_generic_determinant_factor',M[2].det(),u*v*y**2*(z-x)*(x+z+(G/(q*v))*x*z))
same('M3_generic_determinant_factor',M[3].det(),(z-x)*y*u**2*v**2)
My=c*y**2-q**2
Ny=(y+q**2)/c
hx=H*(z-My)/(x*(z-x))
hz=H*(My-x)/(z*(z-x))
hy=H/y
same('H_identity',H,1+q+q**3)
same('b1_first_moment',hx*x+hz*z,H)
same('b1_second_moment',hx*x**2+hz*z**2,H*My)
same('b1_third_moment_recurrence',hx*x**3+hz*z**3,H*((x+z)*My-x*z))
# b1 endpoint and first two equations vanish; final one is precisely moment condition.
amplitudes=sp.Matrix([hx,hz,hy,0,0])
for a in (1,2,4):same(f'b1_nonaxis_{a}',(M[1]*amplitudes)[a],q**((4*(a+1)**2)%5))
same('b1_last_residual_is_moment_constraint',(M[1]*amplitudes)[3]-q**4,-q**4*H*((x+z)*My-x*z-Ny))
# b4 two endpoints determine amplitudes; the interior equations match (1).
a4=sp.Matrix([0,0,0,H/v,H/u])
for a in (1,4):same(f'b4_endpoint_{a}',(M[4]*a4)[a],q**((4*(a+4)**2)%5))
# Use primitive-root reduction to compare polynomial proportionality exactly.
r2=reduce((M[4]*a4)[2]-q**((4*6**2)%5))
r3=reduce((M[4]*a4)[3]-q**((4*7**2)%5))
same('b4_interior_equation_a2',r2,-q**2*(v-c*u**2+q**2))
same('b4_interior_equation_a3',r3,-q**4*(u-c*v**2+q**2))
# Specialization and nonsingular row determinants.
z0=-2-3*q-3*q**2-q**3
t=1+q
subs={x:1,z:z0,y:q,u:t,v:t}
same('z_specialization',z0,(Ny-My).subs(y,q)/(My.subs(y,q)-1))
same('negative_row_specialization',c*t*t-t-q*q,0)
same('M2_short_nonsing_factor',(x+z+(G/(q*v))*x*z).subs(subs),-3-6*q-4*q*q-q**3)
D={0:[-1093,-5351,-6894,-3592],2:[31,21,-17,-30],3:[6,19,21,9]}
for b in range(5):
    numeric=[]
    for a in range(5):
        row=[]
        for j in range(5):
            p=sp.Poly(reduce(M[b][a,j].subs(subs)),q)
            row.append(f.elt([str(p.nth(k)) for k in range(4)]))
        numeric.append(row)
    if b in D:
        _,det=f.inverse_and_det(numeric)
        check(f'specialized_M{b}_determinant',det==f.elt(D[b]))
    # Exact rank by field Gaussian elimination, allowing rectangular rank deficient rows.
    A=[r[:] for r in numeric]
    rank=0
    for j in range(5):
        pivots=[i for i in range(rank,5) if A[i][j]!=f.Z]
        if not pivots:continue
        p=pivots[0]
        A[rank],A[p]=A[p],A[rank]
        div=f.reciprocal(A[rank][j])
        A[rank]=[f.times(vv,div) for vv in A[rank]]
        for i in range(5):
            if i!=rank:
                c0=A[i][j]
                A[i]=[f.minus(aa,f.times(c0,bb)) for aa,bb in zip(A[i],A[rank])]
        rank+=1
    check(f'row{b}_rank',rank==[5,4,5,5,3][b])
# Read the submitted proof table as data and compare every number to frozen witness.
proof=(HERE/'N5_FIVE_BANK_CONSTRUCTION.md').read_text()
witness=json.loads((HERE/'WITNESS.json').read_text())
entries=[]
for line in proof.splitlines():
    m=re.fullmatch(r'\| ([1-5]) \| ([0-4]) \| \(([^)]+)\) \| (\d+) \|',line)
    if not m:continue
    bank,ell=int(m[1])-1,int(m[2])
    den=int(m[4])
    nums=[int(s.strip().replace('−','-')) for s in m[3].split(',')]
    check(f'prose_amplitude_table_{bank+1}_{ell}',f.elt([f.Fr(a,den) for a in nums])==f.elt(witness['banks'][bank]['normalized_h'][ell]))
    entries.append((bank,ell))
check('all_25_prose_amplitudes_present_once',len(entries)==25 and len(set(entries))==25)
result={'verdict':'PASS','checks_passed':len(checks),'proof_sha256':sha256((HERE/'N5_FIVE_BANK_CONSTRUCTION.md').read_bytes()).hexdigest(),'control_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'generic_lemma':'Accepted on its explicitly stated nonzero/distinct/nonsingular locus.','method':'Literal noncommutative S/T word sums, exact symbolic cyclotomic reduction, direct determinants/ranks, and full prose-table/witness comparison.','checks':checks}
(HERE/'lemma_verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
