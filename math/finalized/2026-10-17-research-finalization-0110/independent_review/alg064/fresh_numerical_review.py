"""Independent exact Q(sqrt(2),i) controls of the numerical contract.
No author or historical program is imported or executed. All comparisons are exact.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import random,json
random.seed(6417)
# Real quadratic number a+b sqrt(2).
def ra(x,y):return (x[0]+y[0],x[1]+y[1])
def rn(x):return (-x[0],-x[1])
def rm(x,y):return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def rr(a=0,b=0):return(F(a),F(b))
def rs(x):
 a,b=x
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if a>0 and b>0:return 1
 if a<0 and b<0:return -1
 d=a*a-2*b*b
 return ((d>0)-(d<0)) if a>0 else ((d<0)-(d>0))
def za(x,y):return(ra(x[0],y[0]),ra(x[1],y[1]))
def zn(x):return(rn(x[0]),rn(x[1]))
def zm(x,y):return(ra(rm(x[0],y[0]),rn(rm(x[1],y[1]))),ra(rm(x[0],y[1]),rm(x[1],y[0])))
def zq(x):return(rr(x[0]),rr(x[1]))
def norm2(x):return ra(rm(x[0],x[0]),rm(x[1],x[1]))
def error_leq(x,y,bound):return rs(ra(norm2(za(x,zn(y))),rr(-bound*bound)))<=0
# Dyadic complex rationals.
zero=(F(0),F(0));one=(F(1),F(0))
def qa(x,y):return(x[0]+y[0],x[1]+y[1])
def qn(x):return(-x[0],-x[1])
def qm(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qd(x,y):
 den=y[0]*y[0]+y[1]*y[1]
 return((x[0]*y[0]+x[1]*y[1])/den,(x[1]*y[0]-x[0]*y[1])/den)
def nu(x):return abs(x[0])+abs(x[1])
def roundreal(x,p):return F((x*(1<<p)+F(1,2)).numerator//(x*(1<<p)+F(1,2)).denominator,1<<p)
def rounded(x,p):return(roundreal(x[0],p),roundreal(x[1],p))
def horner_q(poly,z,p):
 h=poly[-1]
 for a in reversed(poly[:-1]):h=rounded(qa(rounded(qm(h,z),p),a),p)
 return h

def horner_z(poly,z):
 h=zq(poly[-1])
 for a in reversed(poly[:-1]):h=za(zm(h,z),zq(a))
 return h

def roots(n,p):
 z8=[(rr(1),rr()),(rr(0,F(1,2)),rr(0,F(1,2))),(rr(),rr(1)),(rr(0,-F(1,2)),rr(0,F(1,2))),(rr(-1),rr()),(rr(0,-F(1,2)),rr(0,-F(1,2))),(rr(),rr(-1)),(rr(0,F(1,2)),rr(0,-F(1,2)))]
 q=p+4;s=F(isqrt(1<<(2*q-1)),1<<q)
 out=[]
 for t in z8[::8//n]:
  approx=rounded(tuple(a+b*2*s for a,b in t),p)
  assert error_leq(zq(approx),t,F(1,1<<p))
  out.append((t,approx))
 return out

summary={'accepted_vectors':0,'residual_rejections':0,'regular_outputs':0,'suspect_outputs':0,'actual_nonzero_residual_acceptances':0,'untapped_span_cases':0,'exact_all_output_error_checks':0,'exact_node_certificates':0,'defect_identities':0,'precision_inequality_checks':0}
rows=[]
def run(x,c,eps=F(1,32)):
 n=len(x);L=len(c)-1;r=max(i for i,a in enumerate(c) if a!=zero);tau=F(1,(2*n)**r)
 A=[];E=[]
 for j in range(L):
  v=zero
  for i in range(j+1):v=qa(v,qm(c[i],x[j-i]))
  for i in range(j+1,L+1):v=qa(v,qm(c[i],x[n+j-i]))
  A.append(v)
 for j in range(L,n):
  v=zero
  for i in range(L+1):v=qa(v,qm(c[i],x[j-i]))
  E.append(v)
 S=sum(map(nu,x));H=sum(map(nu,c));K=sum(map(nu,A));R=sum(map(nu,E))
 if R>eps*tau/8:
  summary['residual_rejections']+=1;return
 b=max(v.denominator.bit_length()-1 for q in x+c for v in q)
 assert all(v.denominator==(1<<(v.denominator.bit_length()-1)) for q in x+c for v in q)
 p=max(1,2*b)
 while True:
  rho=F(1,1<<p)
  if rho<=F(1,n) and 3*L*(H+2)*rho<=min(tau/4,eps*tau/(8*(S+1))) and 3*L*(K+2)*rho<=eps*tau/8 and 3*n*(S+2)*rho<=eps and rho<=eps/4:break
  p+=1
 summary['precision_inequality_checks']+=1
 suspects=0
 for t,z in roots(n,p):
  summary['exact_node_certificates']+=1
  exactx=horner_z(x,t);exactc=horner_z(c,t);exacta=horner_z(A,t)
  exacte=horner_z([zero]*L+E,t)
  assert zm(exactc,exactx)==za(exacta,exacte)
  summary['defect_identities']+=1
  qhat=horner_q(c,z,p);ahat=horner_q(A,z,p)
  assert error_leq(zq(qhat),exactc,3*L*(H+2)*rho)
  assert error_leq(zq(ahat),exacta,3*L*(K+2)*rho)
  if qhat[0]**2+qhat[1]**2 < (3*tau/4)**2:
   suspects+=1;summary['suspect_outputs']+=1;y=horner_q(x,z,p)
   assert rs(ra(norm2(exactc),rr(-tau*tau)))<0
  else:
   summary['regular_outputs']+=1;y=rounded(qd(ahat,qhat),p)
   assert rs(ra(norm2(exactc),rr(-(tau/2)**2)))>=0
  assert error_leq(zq(y),exactx,eps)
  summary['exact_all_output_error_checks']+=1
 assert suspects<=r
 summary['accepted_vectors']+=1
 summary['actual_nonzero_residual_acceptances']+=bool(R)
 summary['untapped_span_cases']+=r<L
 rows.append({'N':n,'L':L,'degree':r,'p':p,'suspects':suspects,'nonzero_residual':bool(R)})

for n in [2,4,8]:
 for L in range(1,min(4,n)):
  for _ in range(25):
   c=[one]+[(F(random.randint(-2,2),2),F(random.randint(-1,1),2)) for _ in range(L)]
   x=[(F(random.randint(-2,2),2),F(random.randint(-2,2),2)) for _ in range(L)]
   for j in range(L,n):
    v=zero
    for i in range(1,L+1):v=qa(v,qm(c[i],x[j-i]))
    x.append(qn(v))
   run(x,c)
   # Tiny final perturbation is admitted only by the exact residual gate.
   y=x[:];y[-1]=qa(y[-1],(F(1,1<<48),F(0)));run(y,c)
   y=x[:];y[-1]=qa(y[-1],one);run(y,c)
  # Untapped register impulse and exact resonant constant recurrence.
  run([one]+[zero]*(n-1),[one]+[zero]*L)
  run([one]*n,[one,(-F(1),F(0))]+[zero]*(L-1))
# Near-resonance: dyadic C root lies extremely close to t=1.
for n in [2,4,8]:
 c=[one,(-F((1<<20)-1,1<<20),F(0))];x=[one]
 for _ in range(1,n):x.append(qn(qm(c[1],x[-1])))
 run(x,c)
# Direct exact rational small-denominator lemma controls on the four-root grid.
near=0
for ar in range(-8,9):
 for ai in range(-8,9):
  alpha=(F(ar,4),F(ai,4))
  if alpha==zero:continue
  for n in [2,4]:
   eps=F(1,2*n);bad=0
   for t in [one,(F(0),F(1)),(-F(1),F(0)),(F(0),-F(1))][::4//n]:
    u=qa(one,qn(qd(t,alpha)))
    bad+=u[0]*u[0]+u[1]*u[1]<eps*eps
   assert bad<=1;near+=1
summary['exact_single_root_neighborhood_controls']=near
# A fixed threshold has unboundedly many near bins; N/8 is certified for C=1-T,
# |C(t_k)| <= 2*pi*k/N <= 8*k/N, using pi<4, for k<N/8 and threshold 1.
summary['fixed_threshold_countercontrol']='For each N, all 0<=k<N/8 obey |1-exp(2*pi*i*k/N)|<1 using pi<4; no N-independent O(1) suspect bound.'
result={'verdict':'PASS','method':'Fresh exact rational/Q(sqrt(2),i) controls and integer-grid rounding; no author or historical code run','summary':summary,'vectors':rows}
(Path(__file__).parent/'INDEPENDENT_NUMERICAL_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(summary,indent=2))
