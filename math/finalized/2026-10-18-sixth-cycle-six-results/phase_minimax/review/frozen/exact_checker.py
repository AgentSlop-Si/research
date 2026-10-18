#!/usr/bin/env python3
"""Fresh characteristic-zero checks; no candidate or historical code is imported.
Field Q[z]/(z^16+1), with intended embedding z=exp(i*pi/16).
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, json
import sympy as sp

D = Path(__file__).resolve().parent
class K:
    def __init__(self, v=0):
        if isinstance(v,K): self.d=v.d.copy()
        elif isinstance(v,dict): self.d={i:Q(x) for i,x in v.items() if x}
        else: self.d={} if not v else {0:Q(v)}
    def __add__(self,o):
        o=K(o); d=self.d.copy()
        for j,v in o.d.items():d[j]=d.get(j,Q(0))+v
        return K(d)
    __radd__=__add__
    def __neg__(self):return K({j:-v for j,v in self.d.items()})
    def __sub__(self,o):return self+-K(o)
    def __rsub__(self,o):return K(o)+-self
    def __mul__(self,o):
        o=K(o);d={}
        for j,v in self.d.items():
            for k,w in o.d.items():
                h=j+k;sgn=(-1)**(h//16);h%=16
                d[h]=d.get(h,Q(0))+sgn*v*w
        return K(d)
    __rmul__=__mul__
    def __pow__(self,n):
        assert n>=0
        x=K(1);b=self
        while n:
            if n&1:x=x*b
            b=b*b;n//=2
        return x
    def __eq__(self,o):return self.d==K(o).d
    def conj(self):return sum((v*root(-j) for j,v in self.d.items()),K())
    def serial(self):return {str(j):str(v) for j,v in sorted(self.d.items())}
def root(n):
    q,r=divmod(n,16);return K({r:Q(1 if q%2==0 else -1)})
I=root(8);sqrt2=root(4)+root(-4);s=(root(1)-root(-1))*(-I)*Q(1,2);c=(root(1)+root(-1))*Q(1,2);t=s*s
n=8
zero=lambda: [[K() for j in range(n)] for i in range(n)]
def eye():return [[K(int(i==j)) for j in range(n)] for i in range(n)]
def tr(A):return [list(a) for a in zip(*A)]
def conj(A):return [[x.conj() for x in a] for a in A]
def adj(A):return tr(conj(A))
def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def sub(A,B):return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(A,k):return [[k*x for x in a] for a in A]
def mul(A,B):return [[sum((x*y for x,y in zip(a,b)),K()) for b in tr(B)] for a in A]
def outer(a,b):return [[x*y for y in b] for x in a]
def re(A):return scale(add(A,conj(A)),Q(1,2))
def im(A):return scale(sub(A,conj(A)),-I*Q(1,2))
def phases(A,p,q):return [[root(p[j]+q[k])*A[j][k] for k in range(n)] for j in range(n)]
def serial(A):return [[x.serial() for x in a] for a in A]
results={}
def check(name,truth):
    assert truth,name
    results[name]=True
F=[[sqrt2*Q(1,4)*root(-4*j*k) for k in range(n)] for j in range(n)]
qe=[0,2,0,10,0,2,0,10];pe=[x+1 for x in qe]
V=phases(F,pe,qe);X=re(V);Y=im(V)
a=[K(Q(x,2)) for x in [1,0,-1,0,-1,0,1,0]]
b=[K(Q(x,2)) for x in [0,1,0,1,0,1,0,1]]
R=add(outer(a,a),outer(b,b));H=scale(add(outer(a,b),outer(b,a)),c);Y0=sub(Y,H)
w=[x+I*y for x,y in zip(a,b)];E=scale(outer(w,w),c);B=sub(X,re(E))
check('root_i_squared',I*I==-1)
check('sqrt_two_squared',sqrt2*sqrt2==2)
check('s_squared_plus_c_squared',s*s+c*c==1)
check('F_negative_sign_unitary_all_64',mul(adj(F),F)==eye())
check('V_symmetric_all_64',V==tr(V))
check('a_b_orthonormal',sum((x*x for x in a),K())==1 and sum((x*x for x in b),K())==1 and sum((x*y for x,y in zip(a,b)),K())==0)
check('Y_a_equals_c_b',all(sum((Y[j][k]*a[k] for k in range(n)),K())==c*b[j] for j in range(n)))
check('Y_b_equals_c_a',all(sum((Y[j][k]*b[k] for k in range(n)),K())==c*a[j] for j in range(n)))
check('Y_square_spectral_identity_all_64',mul(Y,Y)==add(scale(eye(),t),scale(R,1-2*t)))
check('residual_square_identity_all_64',mul(Y0,Y0)==scale(sub(eye(),R),t))
check('E_all_784_two_by_two_minors_zero',all(E[i][j]*E[k][l]-E[i][l]*E[k][j]==0 for i in range(n) for k in range(i+1,n) for j in range(n) for l in range(j+1,n)))
check('E_nonzero',E[0][0]!=0)
check('B_real_all_64',B==conj(B))
check('Im_E_is_high_rank_two_part_all_64',im(E)==H)
check('inner_residual_all_64',sub(V,add(B,E))==scale(Y0,I))
check('original_outer_gauge_residual_all_64',sub(F,phases(add(B,E),[-x for x in pe],[-x for x in qe]))==phases(scale(Y0,I),[-x for x in pe],[-x for x in qe]))
# Explicit real-orthogonal paired-index transforms, ordered (c,d,u).
U=zero();W=zero();halfsqrt2=sqrt2*Q(1,2)
for cc in range(2):
 for dd in range(2):
  for u in range(2):
   idx=4*cc+2*dd+u;r=cc+2*u;k=dd+2*u
   U[r][idx]=halfsqrt2;U[r+4][idx]=((-1)**dd)*halfsqrt2
   W[k][idx]=halfsqrt2;W[k+4][idx]=((-1)**cc)*halfsqrt2
check('real_left_transform_orthogonal',mul(tr(U),U)==eye() and U==conj(U))
check('real_right_transform_orthogonal',mul(tr(W),W)==eye() and W==conj(W))
C=mul(mul(tr(U),V),W);expected=zero()
for cc in range(2):
 for dd in range(2):
  for u in range(2):
   for v in range(2):
    row=4*cc+2*dd+u;col=4*cc+2*dd+v
    expected[row][col]=halfsqrt2*root(pe[cc+2*u]+qe[dd+2*v]-4*(cc+2*u)*(dd+2*v))
check('four_block_transform_all_64',C==expected)
check('algebraic_squared_error_polynomial',128*t**4-256*t**3+160*t**2-32*t+1==0)
check('algebraic_error_polynomial',128*s**8-256*s**6+160*s**4-32*s**2+1==0)
x=sp.Symbol('x');poly=sp.Poly(128*x**8-256*x**6+160*x**4-32*x**2+1,x)
lo=sp.Rational(1950903220161282678,10**19);hi=sp.Rational(1950903220161282679,10**19)
check('unique_polynomial_root_in_error_interval',poly.count_roots(lo,hi)==1)
check('interval_within_positive_smallest_root_region',poly.count_roots(0,lo)==0 and hi<sp.Rational(1,4))
# Mutation controls must fail the exact witness certificate.
Fplus=[[sqrt2*Q(1,4)*root(4*j*k) for k in range(n)] for j in range(n)]
wrongY=im(phases(Fplus,pe,qe))
check('reject_reversed_Fourier_sign',mul(wrongY,wrongY)!=add(scale(eye(),t),scale(R,1-2*t)))
pbad=pe.copy();pbad[3]-=1;badY=im(phases(F,pbad,qe))
check('reject_single_phase_exponent_error',mul(badY,badY)!=add(scale(eye(),t),scale(R,1-2*t)))
wbad=[x-I*y for x,y in zip(a,b)];badE=scale(outer(wbad,wbad),c)
check('reject_conjugated_rank_one_vector',im(badE)!=H)
check('reject_wrong_normalization',mul(adj(scale(F,Q(1,2))),scale(F,Q(1,2)))!=eye())
source=(D/'SOURCE_ACCEPTED_C8.md').read_bytes()
check('pinned_source_git_blob',hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()=='11b2f499b004f62686a8584488e57022e970ebf2')
results['arithmetic']='Exact Q[z]/(z^16+1), no floating-point arithmetic in witness checks.'
results['error_root_interval']=[str(lo),str(hi)]
results['scope']='Upper bound and exact witness verified; this checker does not prove the unrestricted continuous-phase lower bound.'
(D/'EXACT_CHECKS.json').write_text(json.dumps(results,indent=2)+'\n')
witness={'field':'Q[z]/(z^16+1), intended z=exp(i*pi/16)','matrix_order':8,'coefficient_encoding':'Map exponent 0..15 to exact rational coefficient','P_inner_exponents':pe,'Q_inner_exponents':qe,'P_outer_exponents':[-x for x in pe],'Q_outer_exponents':[-x for x in qe],'a':[x.serial() for x in a],'b':[x.serial() for x in b],'s':s.serial(),'c':c.serial(),'F':serial(F),'V':serial(V),'B':serial(B),'E':serial(E),'residual_inner':serial(scale(Y0,I))}
(D/'WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
print(json.dumps(results,indent=2))
