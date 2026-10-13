#!/usr/bin/env python3
"""Fresh exact finite PREFIX compatibility-graph and direct group checks.
No candidate or historical code imported. Definitions from published p7/p11 reviews.
"""
import json,math,time,argparse
from pathlib import Path

def graph(p,r):
 n=8*p*r
 types=[d for d in range(2,n) if n%d==0 and d not in (4*p*r,8*r,8*p)]
 vertices=sorted((i,d) for d in types for i in range(d,n,d))
 size=len(vertices); masks=[0]*size;edges=0
 for a,(i,d) in enumerate(vertices):
  mask=0
  for b in range(a+1,size):
   j,e=vertices[b]
   L=math.lcm(d,e)
   lo=i if L==d else i+1
   hi=j if L==e else j-1
   conflict=(i==j or ((lo+L-1)//L)>hi//L)
   enumerated_conflict = i==j or not any(
    (m>i or L==d) and (m<j or L==e)
    for m in range(((i+L-1)//L)*L,j+1,L))
   assert conflict==enumerated_conflict
   if conflict: mask|=1<<(b-a-1);edges+=1
  masks[a]=mask
 states={0:0};peak=1;transitions=0
 for a,(i,d) in enumerate(vertices):
  next_states={}
  def put(k,v):
   if v>next_states.get(k,-1):next_states[k]=v
  for blocked,value in states.items():
   transitions+=1; tail=blocked>>1;put(tail,value)
   if not blocked&1:put(tail|masks[a],value+d-1)
  states=next_states;peak=max(peak,len(states))
  if a%200==0: print('graph',p,r,a,size,'states',len(states),flush=True)
 assert list(states)==[0]
 return {'p':p,'r':r,'N':n,'types':types,'vertices':size,'pair_checks':size*(size-1)//2,'edges':edges,'maximum':states[0],'target':(18*p-8)*r-8*p+1,'states_peak':peak,'transitions':transitions}

def group(p,r,escape):
 n=8*p*r
 # Tuple encoding: d + 8*c + 8*p*t, d=i+4*b in D8.
 decode=[(a%4,(a//4)%2,(a//8)%p,a//(8*p)) for a in range(n)]
 def mul(a,b):
  i,j,c,t=decode[a];k,l,e,u=decode[b]
  return ((i+(-1 if j else 1)*k)%4)+4*(j^l)+8*((c+e)%p)+8*p*((t+u)%r)
 def inv(a):
  i,j,c,t=decode[a]
  return ((i if j else -i)%4)+4*j+8*((-c)%p)+8*p*((-t)%r)
 inverses=[inv(a) for a in range(n)]
 d_order=[0,4,1,5,2,6,3,7] if escape else [0,4,2,6,1,5,7,3]
 order=[d+8*c+8*p*t for d in d_order for c in range(p) for t in range(r)]
 assert len(set(order))==n
 seen=[];hits=[0]*n;generators=set();score=0;profiles=[]
 for j,y in enumerate(order,1):
  for x in seen:hits[mul(y,inverses[x])]+=1
  seen.append(y)
  for x in seen:hits[mul(x,inverses[y])]+=1
  stab=[g for g in range(n) if hits[g]==j]
  assert j%len(stab)==0
  score+=len(stab)-1
  if j<n:generators.update(stab)
  profiles.append(len(stab))
 # Explicit subgroup closure by successively adding currently outside generators.
 B={0};basis=[]
 for g in sorted(generators):
  if g in B:continue
  basis.append(g);front=list(B)
  while front:
   h=front.pop()
   for b in basis:
    k=mul(h,b)
    if k not in B:B.add(k);front.append(k)
 expected=(26*p-8 if escape else 28*p-8)*r-8*p
 assert score==expected
 assert len(B)==(n if escape else n//2)
 return {'p':p,'r':r,'N':n,'escape':escape,'D8_encoding':'i+4*b','D8_order':d_order,'score':score,'expected_score':expected,'B_order':len(B),'expected_B_order':n if escape else n//2,'stabilizer_profile':profiles,'translation_prefix_checks':n*n}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,required=True);ap.add_argument('--r',type=int,required=True);ap.add_argument('--out',required=True);ap.add_argument('--no-group',action='store_true');a=ap.parse_args()
 assert a.p>=3 and a.r>a.p and all(a.p%d for d in range(2,math.isqrt(a.p)+1)) and all(a.r%d for d in range(2,math.isqrt(a.r)+1))
 t=time.monotonic();result={'graph':graph(a.p,a.r)}
 if not a.no_group:result['group_witnesses']=[group(a.p,a.r,False),group(a.p,a.r,True)]
 result['elapsed_seconds']=time.monotonic()-t
 Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='group_witnesses'},indent=2));print('SAVED',a.out)
if __name__=='__main__':main()
