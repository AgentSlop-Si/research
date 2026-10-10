#!/usr/bin/env python3
"""Fresh standard-library exact construction/verification of the F8 anchor-orbit interface.

No research program is imported.  This does NOT solve the generated polynomial
systems and does NOT claim that either system has a guarded solution.
"""
import json, hashlib
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
N=8
ORDER0=[0,1,2,3,4,5,6,7]
ORDER1=[0,2,5,1,7,4,6,3]
PAIRS={'adjacent':[(0,1),(2,3),(4,5),(6,7)],
       'half':[(0,4),(1,5),(2,6),(3,7)]}
def cycle(order): return {order[i]:order[(i+1)%N] for i in range(N)}
pi,sigma=cycle(ORDER0),cycle(ORDER1)
ip={v:k for k,v in pi.items()}; iss={v:k for k,v in sigma.items()}
pivot={j:min(set(range(N))-{j,pi[j],sigma[j]}) for j in range(N)}
assert all(pi[j]!=sigma[j] for j in range(N))
assert any(pi[sigma[j]]!=sigma[pi[j]] for j in range(N))

# Q[zeta_8] coefficients, zeta_8^4=-1; integer coefficients suffice.
Z=(0,0,0,0); ONE=(1,0,0,0)
def ca(a,b):return tuple(a[i]+b[i] for i in range(4))
def cn(a):return tuple(-x for x in a)
def cm(a,b):
    c=[0]*4
    for i in range(4):
      for j in range(4):
        k=i+j;c[k%4]+=a[i]*b[j]*(1 if k<4 else -1)
    return tuple(c)
def zp(k):
    k%=8;c=[0]*4;c[k%4]=1 if k<4 else -1;return tuple(c)

# Sparse polynomials in t0,...,t3,u0,...,u7.
E0=(0,)*12
def con(c):return {} if c==Z else {E0:c}
def var(k):
    e=list(E0);e[k]=1;return {tuple(e):ONE}
def add(a,b):
    d=dict(a)
    for e,c in b.items():
      d[e]=ca(d.get(e,Z),c)
      if d[e]==Z:del d[e]
    return d
def neg(a):return {e:cn(c) for e,c in a.items()}
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    d={}
    for ea,ca0 in a.items():
      for eb,cb0 in b.items():
        e=tuple(x+y for x,y in zip(ea,eb));d[e]=ca(d.get(e,Z),cm(ca0,cb0))
        if d[e]==Z:del d[e]
    return d
T=[var(k) for k in range(4)];U=[var(4+i) for i in range(N)]
def encode(p):return [[list(e),list(c)] for e,c in sorted(p.items())]

def build(name,pairs):
    M=[[None]*N for _ in range(N)]
    for k,(a,b) in enumerate(pairs):
      for i in range(N):
        left=con(zp(i*a));right=mul(T[k],con(zp(i*b)))
        M[i][a]=add(left,right);M[i][b]=sub(left,right)
    A=[[add(M[i][j],mul(U[i],M[ip[i]][j])) for j in range(N)] for i in range(N)]
    C=[[A[i][sigma[j]] for j in range(N)] for i in range(N)]
    a=[A[pivot[j]][j] for j in range(N)]
    c=[C[pivot[j]][j] for j in range(N)]
    h=[[sub(mul(c[j],A[i][j]),mul(a[j],C[i][j])) for j in range(N)] for i in range(N)]
    d=[]
    for i in range(N):
      k=iss[i]
      d.append(sub(add(mul(mul(U[pi[i]],a[k]),h[i][i]),
                       mul(mul(c[i],U[pi[i]]),h[i][k])),
                   mul(a[k],h[pi[i]][i])))
    polys={}
    for j in range(N):polys[f'a_{j}']=a[j];polys[f'c_{j}']=c[j]
    for i in range(N):
      for j in range(N):polys[f'h_{i}_{j}']=h[i][j]
    for i in range(N):polys[f'diag_{i}']=d[i]
    offs=[f'h_{i}_{j}' for j in range(N) for i in range(N) if i not in {j,pi[j],sigma[j],pivot[j]}]
    eqs=offs+[f'diag_{i}' for i in range(N)]
    assert len(eqs)==40 and all(not h[pivot[j]][j] for j in range(N))
    data={'status':('Exact iff open-chart interface; excluded by companion whole-orbit certificate' if name=='half' else 'Exact iff open-chart interface; solvability not established'),
      'field':'Q(zeta_8), zeta_8^4=-1; coefficients in basis 1,zeta_8,zeta_8^2,zeta_8^3',
      'variables':[f't{k}' for k in range(4)]+[f'u{i}' for i in range(N)],
      'anchor_pairs':pairs,'order_0':ORDER0,'order_1':ORDER1,
      'pi':pi,'sigma':sigma,'pivot_rows':pivot,
      'target':'M=F8*T*K, where T[a_k]=1 and T[b_k]=t_k; actual second factor is M/2',
      'polynomials':{k:encode(v) for k,v in polys.items()},'zero_equations':eqs,
      'nonzero_polynomial_guards':[f'a_{j}' for j in range(N)]+[f'c_{j}' for j in range(N)]+
          [f'h_{pi[j]}_{j}' for j in range(N)]+[f'h_{sigma[j]}_{j}' for j in range(N)],
      'nonzero_variable_guards':[f't{k}' for k in range(4)]+[f'u{i}' for i in range(N)],
      'additional_nonzero_guards':['1-product_i(u_i)','product_j(c_j)-product_j(a_j)'],
      'reconstruction':{'v_j':'-a_j/c_j','x_i':'-h_{i,sigma_inverse(i)}/a_{sigma_inverse(i)}',
        'y_j':'h_{pi(j),j}/(c_j*u_{pi(j)})','U':'I+diag(u)*P_pi',
        'V':'I+P_sigma*diag(v)','Q_0':'diag(1/x)*U','Q_1':'V*diag(1/y)',
        'factor_1':'K*T^(-1)','factor_2':'(Q_0^(-1)+Q_1^(-1))/2',
        'actual_second_inverse_branches':['2*Q_0','2*Q_1']},
      'stats':{'number_variables':12,'number_zero_equations':40,
        'maximum_equation_total_degree':max((sum(e) for k in eqs for e in polys[k]),default=0),
        'total_equation_monomials':sum(len(polys[k]) for k in eqs)}}
    (ROOT/f'{name.upper()}_ANCHOR_ORBIT_SYSTEM.json').write_text(json.dumps(data,indent=2)+'\n')
    return data

def eye():return [[F(i==j) for j in range(N)] for i in range(N)]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
def madd(a,b):return [[a[i][j]+b[i][j] for j in range(N)] for i in range(N)]
def inv(a):
    z=[a[i][:]+eye()[i] for i in range(N)]
    for j in range(N):
      k=next(i for i in range(j,N) if z[i][j]);z[j],z[k]=z[k],z[j]
      q=z[j][j];z[j]=[x/q for x in z[j]]
      for i in range(N):
        if i!=j:
          q=z[i][j];z[i]=[x-q*y for x,y in zip(z[i],z[j])]
    return [row[N:] for row in z]
def diag(x):return [[F(x[i]) if i==j else F(0) for j in range(N)] for i in range(N)]
def product(x):
    a=1
    for b in x:a*=b
    return a

def recover_numeric(B,u):
    A=[[B[i][j]+u[i]*B[ip[i]][j] for j in range(N)] for i in range(N)]
    C=[[A[i][sigma[j]] for j in range(N)] for i in range(N)]
    a=[A[pivot[j]][j] for j in range(N)];c=[C[pivot[j]][j] for j in range(N)]
    assert all(a) and all(c)
    h=[[c[j]*A[i][j]-a[j]*C[i][j] for j in range(N)] for i in range(N)]
    v=[-a[j]/c[j] for j in range(N)]
    x=[-h[i][iss[i]]/a[iss[i]] for i in range(N)]
    y=[h[pi[j]][j]/(c[j]*u[pi[j]]) for j in range(N)]
    equations=[h[i][j] for j in range(N) for i in range(N) if i not in {j,pi[j],sigma[j],pivot[j]}]
    equations += [u[pi[i]]*a[iss[i]]*h[i][i]+c[i]*u[pi[i]]*h[i][iss[i]]-a[iss[i]]*h[pi[i]][i] for i in range(N)]
    return a,c,h,v,x,y,equations

def rational_controls():
    out=[]
    for seed in range(1,5):
      u=[F(seed+i+1) for i in range(N)]
      v=[F(seed+2*i+3) for i in range(N)]
      x=[F(seed+3*i+2) for i in range(N)]
      y=[F(seed+5*i+4) for i in range(N)]
      Um=eye();Vm=eye()
      for i in range(N):Um[i][ip[i]]=u[i]
      for j in range(N):Vm[sigma[j]][j]=v[j]
      B=madd(mm(inv(Um),diag(x)),mm(diag(y),inv(Vm)))
      a,c,h,v2,x2,y2,equations=recover_numeric(B,u)
      assert v==v2 and x==x2 and y==y2 and not any(equations)
      assert product(u)!=1 and product(v)!=1 and all(x2) and all(y2)
      Q0=mm(diag([1/z for z in x2]),Um);Q1=mm(Vm,diag([1/z for z in y2]))
      assert madd(inv(Q0),inv(Q1))==B
      bad=[row[:] for row in B];bad[4][0]+=1
      try:rejected=any(recover_numeric(bad,u)[-1])
      except AssertionError:rejected=True
      assert rejected
      out.append({'seed':seed,'exact_rational_positive_control':'PASS',
        'all_40_equations_zero':True,'direction_and_scale_recovery_exact':True,
        'full_inverse_sum_verified':True,'one_entry_negative_control_rejected':True})
    return out

def ev(poly,values,z,p):
    ans=0
    for e,c in poly:
      term=sum(c[k]*pow(z,k,p) for k in range(4))%p
      for a,b in zip(values,e):term=term*pow(a,b,p)%p
      ans=(ans+term)%p
    return ans
def modular_symbolic_controls(data):
    result=[]
    pairs=data['anchor_pairs']
    for p in [17,97,113,193]:
      z=next(z for z in range(2,p) if pow(z,4,p)==p-1)
      values=[(3*i+2)%p for i in range(12)]
      t,u=values[:4],values[4:]
      M=[[0]*N for _ in range(N)]
      for k,(a,b) in enumerate(pairs):
        for i in range(N):
          M[i][a]=(pow(z,i*a,p)+t[k]*pow(z,i*b,p))%p
          M[i][b]=(pow(z,i*a,p)-t[k]*pow(z,i*b,p))%p
      A=[[(M[i][j]+u[i]*M[ip[i]][j])%p for j in range(N)] for i in range(N)]
      C=[[A[i][sigma[j]] for j in range(N)] for i in range(N)]
      a=[A[pivot[j]][j] for j in range(N)];c=[C[pivot[j]][j] for j in range(N)]
      h=[[(c[j]*A[i][j]-a[j]*C[i][j])%p for j in range(N)] for i in range(N)]
      expected={**{f'a_{j}':a[j] for j in range(N)},**{f'c_{j}':c[j] for j in range(N)}}
      expected.update({f'h_{i}_{j}':h[i][j] for i in range(N) for j in range(N)})
      expected.update({f'diag_{i}':(u[pi[i]]*a[iss[i]]*h[i][i]+c[i]*u[pi[i]]*h[i][iss[i]]-a[iss[i]]*h[pi[i]][i])%p for i in range(N)})
      assert all(ev(poly,values,z,p)==expected[name] for name,poly in data['polynomials'].items())
      # Independently verify M/2 * K*T^-1 = F8 in each splitting prime field.
      assert all(t)
      K=[[0]*N for _ in range(N)];Ti=[1]*N
      for k,(aa,bb) in enumerate(pairs):
        K[aa][aa]=K[aa][bb]=K[bb][aa]=1;K[bb][bb]=-1;Ti[bb]=pow(t[k],-1,p)
      for i in range(N):
        for j in range(N):
          assert sum(M[i][k]*K[k][j]*Ti[j] for k in range(N))*pow(2,-1,p)%p==pow(z,i*j,p)
      result.append({'prime':p,'zeta8':z,'all_88_stored_polynomials_match_direct_formulas':True,'anchor_identity_verified':True})
    return result

def exact_half_orbit_obstruction(data):
    """Verify every polynomial identity in the short whole-orbit rejection proof.

    The minors are necessary even when the selected column pivots vanish, so
    this obstruction is stronger than the 12-variable open-chart interface.
    """
    polys={name:{tuple(e):tuple(c) for e,c in rows} for name,rows in data['polynomials'].items()}
    one=con(ONE);ii=con(zp(2));zz=con(zp(1));w=U[0];aa=T[0];bb=T[2];tt=T[1]
    def sc(n,p):return mul(con((n,0,0,0)),p)
    def direction_sub(p):
      out={}
      for e,c in p.items():
        e=list(e);power=e[7]+e[11]
        e[4]+=e[6]+e[8]-power
        for k in [6,7,8,11]:e[k]=0
        term={tuple(e):cm(c,zp(2*power))};out=add(out,term)
      return out
    def b_minus_a(p):
      out={}
      for e,c in p.items():
        e=list(e);power=e[2];e[0]+=power;e[2]=0
        out=add(out,{tuple(e):c if power%2==0 else cn(c)})
      return out
    # First four necessary minors force u2=u4=w and u3=u7=i/w.
    assert polys['h_2_5']==sc(-4,mul(mul(tt,zz),sub(w,U[2])))
    assert polys['h_3_5']==sc(4,mul(mul(tt,zz),sub(ii,mul(w,U[3]))))
    assert polys['h_4_5']==sc(-4,mul(mul(tt,con(zp(3))),sub(w,U[4])))
    assert polys['h_7_5']==sc(-4,mul(mul(tt,zz),sub(ii,mul(w,U[7]))))
    # Multiplication by w is legitimate because w*u3=i forces w != 0.
    q40=mul(w,direction_sub(polys['h_4_0']))
    q34=mul(w,direction_sub(polys['h_3_4']))
    assert add(q40,q34)==sc(-4,mul(ii,add(aa,bb)))
    E=add(mul(mul(add(mul(aa,aa),one),add(one,ii)),w),mul(ii,sub(one,mul(aa,aa))))
    assert b_minus_a(q40)==sc(-2,E)
    R=sub(mul(add(aa,one),w),sub(aa,one))
    S=sub(neg(mul(mul(ii,sub(aa,one)),w)),add(aa,one))
    assert b_minus_a(direction_sub(polys['h_2_4']))==sc(-2,mul(R,S))
    q=add(sub(mul(aa,aa),sc(2,mul(ii,aa))),one)
    coefficient=mul(add(mul(aa,aa),one),add(one,ii))
    assert mul(add(aa,one),E)==add(mul(coefficient,R),mul(sub(aa,one),q))
    assert add(mul(mul(ii,sub(aa,one)),E),mul(coefficient,S))==neg(mul(mul(ii,add(aa,one)),q))
    # E rules out a=+/-1; either R=0 or S=0 therefore forces q=0.
    # q=0 and a!=0 give coefficient!=0, hence R=0 and w^2=i.
    assert sub(mul(mul(add(aa,one),add(aa,one)),sub(mul(w,w),ii)),mul(sub(one,ii),q))==mul(R,add(mul(add(aa,one),w),sub(aa,one)))
    L=con(ca(zp(3),cn(zp(1))))
    term1=mul(mul(add(tt,one),w),L)
    term2=mul(sub(tt,one),add(one,ii))
    J=add(term1,term2)
    assert b_minus_a(mul(w,direction_sub(polys['h_7_2'])))==mul(sub(one,aa),J)
    assert mul(J,sub(term1,term2))==add(sc(2,mul(mul(add(tt,one),add(tt,one)),sub(mul(w,w),ii))),sc(8,mul(ii,tt)))
    cert={'status':'PASS: exact whole diagonal-orbit obstruction',
      'scope':'Half-pair anchor X1=A*K*B with arbitrary nonsingular diagonal A,B; second factor uses the two stipulated inverse-branch support cycles and nonsingular diagonal endpoints. Edge coefficients may be zero. This is not a universal F8 obstruction.',
      'field':'Any field containing a primitive eighth root zeta, with characteristic !=2',
      'source_minors':['h_2_5','h_3_5','h_4_5','h_7_5','h_4_0','h_3_4','h_2_4','h_7_2'],
      'number_exact_polynomial_assertions':12,
      'conclusion':'The eight necessary minors imply 8*i*t1=0; i=zeta^2 and t1 is a required nonzero diagonal ratio.',
      'pivot_nonvanishing_used':False,'nonzero_edge_assumption_used':False,
      'green_determinant_guard_used':False}
    (ROOT/'HALF_ORBIT_EXACT_REJECTION.json').write_text(json.dumps(cert,indent=2)+'\n')
    return cert

def main():
    data=[build(name,pairs) for name,pairs in PAIRS.items()]
    controls={'status':'PASS; interface correctness only, no F8 solution claimed',
      'cycle_pair_disjoint_edges':True,'cycle_pair_noncommuting':True,'pivot_rows':pivot,
      'rational_controls':rational_controls(),
      'symbolic_controls':{name:modular_symbolic_controls(d) for name,d in zip(PAIRS,data)},
      'system_stats':{name:d['stats'] for name,d in zip(PAIRS,data)},
      'half_orbit_rejection':exact_half_orbit_obstruction(data[1])}
    (ROOT/'EXACT_INTERFACE_CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n')
    print(json.dumps(controls,indent=2))
if __name__=='__main__':main()
