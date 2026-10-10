#!/usr/bin/env python3
"""New bounded corollary: global nonzero matching-mask layers for a=b=4.
Imports only this audit's newly authored arithmetic helpers, never source programs.
"""
import json,hashlib
from pathlib import Path
from independent_audit import smm,sadd,SI,mono,diago,root,lift_small
OUT=Path(__file__).resolve().parent

def check(m):
 a=b=4;n=16*m;p=65537;w=root(p,n);ii=pow(w,n//4,p);alpha=ii
 pw=[pow(w,k,p) for k in range(n)]
 assert alpha not in (0,1,p-1)
 gp=[[((r0*b+t2)*m+t1) for r0 in range(a)] for t2 in range(b) for t1 in range(m)]
 gq=[[((r0*b+r2)*m+r1) for r2 in range(b)] for r0 in range(a) for r1 in range(m)]
 Dp=diago([pw[(r0*(t2+b*t1))%n] for r0 in range(a) for t2 in range(b) for t1 in range(m)])
 Dq=diago([pw[(a*r1*t2)%n] for r0 in range(a) for t2 in range(b) for r1 in range(m)])
 Rq=[{} for _ in range(n)];Rp=[{} for _ in range(n)]
 for r0 in range(a):
  for r2 in range(b):
   for r1 in range(m):Rq[(r0*b+r2)*m+r1]={r0+a*r1+a*m*r2:1}
 for t0 in range(a):
  for t2 in range(b):
   for t1 in range(m):Rp[t2+b*t1+b*m*t0]={(t0*b+t2)*m+t1:1}
 Rsmall=[{0:1},{2:1},{1:1},{3:1}];Dsmall=diago([1,1,1,ii])
 layers=[];certificates=[]
 for label,groups,stage,L,R in [
   ('P1',gp,1,SI(n),smm(lift_small(Rsmall,gp,n),Dp,p)),
   ('P2',gp,2,Rp,lift_small(Dsmall,gp,n)),
   ('Q1',gq,1,SI(n),smm(lift_small(Rsmall,gq,n),Rq,p)),
   ('Q2',gq,2,Dq,lift_small(Dsmall,gq,n))]:
  pairs=[(g[x],g[y]) for g in groups for x,y in ([(0,1),(2,3)] if stage==1 else [(0,2),(1,3)])]
  assert len(pairs)==n//2 and sorted([x for pair in pairs for x in pair])==list(range(n))
  order0=[x for aa,bb in pairs for x in (bb,aa)];order1=[x for aa,bb in pairs for x in (aa,bb)]
  W0=[{} for _ in range(n)];W1=[{} for _ in range(n)];diag=[None]*n;H=[{} for _ in range(n)]
  for aa,bb in pairs:
   W0[aa][bb]=pow(alpha,-1,p);W1[bb][aa]=pow((-1-alpha)%p,-1,p)
   diag[aa]=(1-alpha)%p;diag[bb]=(-1-alpha)%p
   H[aa]={aa:1,bb:1};H[bb]={aa:1,bb:p-1}
  assert all(not row for row in smm(W0,W0,p)) and all(not row for row in smm(W1,W1,p))
  for order,W in [(order0,W0),(order1,W1)]:
   succ=dict(zip(order,order[1:]+order[:1]));assert len(succ)==n
   assert all(succ[col]==row for row in range(n) for col in W[row])
  Left0=smm(L,diago([alpha]*n),p);Left1=smm(L,diago(diag),p)
  assert mono(Left0) and mono(Left1) and mono(R)
  G0=sadd(SI(n),W0,p);G1=sadd(SI(n),W1,p)
  T0=smm(smm(Left0,G0,p),R,p);T1=smm(smm(Left1,G1,p),R,p)
  layer=sadd(T0,T1,p);assert layer==smm(smm(L,H,p),R,p);layers.append(layer)
  def monoarr(A):return [[next(iter(row)),next(iter(row.values()))] for row in A]
  certificates.append({'layer':label,'pairs':pairs,'branch0':{'Hamiltonian_visit_order':order0,'nonzero_mask_edges':[[r,c,x] for r in range(n) for c,x in W0[r].items()],'left_endpoint_row_col_weight':monoarr(Left0),'right_endpoint_row_col_weight':monoarr(R),'guard':1},'branch1':{'Hamiltonian_visit_order':order1,'nonzero_mask_edges':[[r,c,x] for r in range(n) for c,x in W1[r].items()],'left_endpoint_row_col_weight':monoarr(Left1),'right_endpoint_row_col_weight':monoarr(R),'guard':1},'all_other_mask_edges':0})
 P=smm(layers[1],layers[0],p);Q=smm(layers[3],layers[2],p)
 B=[{block*m+j:pw[(16*i*j)%n] for j in range(m)} for block in range(16) for i in range(m)]
 F=[{j:pw[(i*j)%n] for j in range(n)} for i in range(n)]
 assert smm(smm(P,B,p),Q,p)==F
 return {'N':n,'a':4,'m':m,'b':4,'q':16,'field_prime':p,'omega':w,'alpha':alpha,'full_four_layer_bank_identity':True,'global_Hamiltonian_cycles':8,'genuinely_nonzero_edges_per_branch':n//2,'all_cycle_product_guards':1,'certificates':certificates}
if __name__=='__main__':
 results=[check(m) for m in [8,16]]
 (OUT/'CONSTRUCTIVE_MATCHING_CONTROLS.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps([{k:v for k,v in r.items() if k!='certificates'} for r in results]))
