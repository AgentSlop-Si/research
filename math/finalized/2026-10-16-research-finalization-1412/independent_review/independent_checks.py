"""New reviewer-authored, bounded algebra controls; imports no project program."""
from fractions import Fraction
from itertools import product
import json

def rev(x,t):
 return int(format(x,'0%db'%t)[::-1],2)
def rows(b,d,L):
 r=2**d; out=[]
 for t in range(1,L+1):
  for k in range(2**(t-1),2**t):
   if not k&1 or '0'*b in format(k,'0%db'%t):continue
   R=2**(d-b-t)
   for q in range(R):out.append((t,q,k,R,rev(k,t)))
 return out
checks=0; pairings=0; norms=0; outputs=0
for b in range(1,4):
 L=2**(b-1);d=b+L;r=2**d
 rr=rows(b,d,L)
 dest=set()
 for t,q,k,R,f in rr:
  ix=2**(b+t)*q+k
  assert ix not in dest;dest.add(ix);outputs+=1
  assert len(range(q,r,R))==2**(b+t);norms+=1
 for ia,a in enumerate(rr):
  ta,qa,ka,Ra,fa=a
  for bb in rr[ia+1:]:
   tb,qb,kb,Rb,fb=bb
   v={}
   for j in range(qa,r,Ra):
    if j%Rb!=qb:continue
    e=(j*(fa-fb))%r
    sign=1 if e<r//2 else -1
    e%=r//2
    v[e]=v.get(e,0)+sign
   assert all(x==0 for x in v.values());pairings+=1
 assert len(rr)<=r
 checks+=1
# Avoiding-word counts and sharpened constant in the stated asymptotic domain.
count_cases=[]
for b in range(7,13):
 L=2**(b-1)
 states=[1]+[0]*(b-1)
 avoid=[1]
 for k in range(1,L-1):
  states=[sum(states)]+states[:-1]
  avoid.append(sum(states))
 m=Fraction(1,2**(b+1));S=Fraction(b+1,2**(b+1))
 for t in range(2,L+1):
  a=avoid[t-2]
  mt=Fraction(a,2**(b+t))
  assert a>=2**(t-3) if t>=3 else a>=Fraction(1,2)
  m+=mt;S+=(b+t)*mt
 assert m<=1
 assert S/2>=Fraction(L,64)
 count_cases.append({'b':b,'L':L,'row_fraction_le_one':True,'S_over_2r_ge_L_over_64':True})
# General boundary-polynomial identity using declared recurrence SPAN, including
# cases where connection-polynomial degree is smaller than the span.
boundary_cases=0
for p in (5,7):
 for N in range(2,8):
  for L in range(min(3,N)+1):
   for coeff in product(range(p), repeat=L):
    C=[1]+list(coeff)
    # All initial seeds would be excessive; deterministic seeds include impulses.
    seeds=[tuple(0 for _ in range(L)),tuple(1 for _ in range(L))]
    seeds += [tuple(int(i==j) for i in range(L)) for j in range(L)]
    for seed in seeds:
     a=list(seed)
     for n in range(L,N):
      a.append(-sum(C[j]*a[n-j] for j in range(1,L+1))%p)
     full=[0]*(N+L)
     for n,x in enumerate(a):
      for j,c in enumerate(C):full[n+j]=(full[n+j]+x*c)%p
     assert all(full[n]==0 for n in range(L,N))
     boundary=full[:L]
     for j in range(L):boundary[j]=(boundary[j]+full[N+j])%p
     reduced=[0]*N
     for n,x in enumerate(full):reduced[n%N]=(reduced[n%N]+x)%p
     assert reduced==boundary+[0]*(N-L)
     boundary_cases+=1
print(json.dumps({'young_packet_small_cases':checks,'orthogonality_pairings':pairings,'row_norms':norms,'disjoint_outputs':outputs,'young_count_cases':count_cases,'recurrence_boundary_cases':boundary_cases,'supplied_programs_executed':False,'scope':'Finite transcription controls only; universal conclusions rest on proofs.'},indent=2))
