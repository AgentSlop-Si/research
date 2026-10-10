"""Fresh author control; only imports this packet's fresh arithmetic helper."""
from fresh_probe import *
import argparse

def run(N,literal=True):
 t0=time.time();K,q,G0,f,H,s=setup(N);d=N-3;m=N-4;zero=K.zero;one=K.one
 table={(a,b,e,j):G0(a,b,e,j) for a in range(N) for b in range(N) for e,j in ((1,1),(-1,1),(1,-1),(-1,-1))}
 G=lambda a,b,e,j:table[a,b,e,j]
 nodes=[q**i for i in range(1,m+1)]; p=[one]
 for y in nodes:p=mult(p,[-y,one],K)
 D=sum((p[k]*s[k] for k in range(m+1)),zero);U=sum((p[k]*s[k+1] for k in range(m+1)),zero)
 assert D and U
 x=U/D;assert x not in nodes;nodes.append(x)
 g=mult(p,[-x,one],K);assert not sum((g[k]*s[k] for k in range(d+1)),zero)
 assert s[2]==q
 def moments(values,start=0):
  l=len(values);a=solve([[v**r for v in nodes[:l]] for r in range(start,start+l)],values,K)
  assert a is not None and len(a[1])==l
  return a[0]+[zero]*(d-l)
 Z=[]
 cols=list(range(m))+[d]+list(range(d+2,d+5))
 M=[[G(a,0,1,1)*v**a for v in nodes]+[G(a,0,-1,1),G(a,0,1,-1)]+[G(a,0,-1,-1)*v**((-a)%N) for v in nodes] for a in range(N)]
 a=solve([[r[c] for c in cols] for r in M],[f(r,0) for r in range(N)],K);assert a and len(a[1])==N
 z=[zero]*(2*d+2)
 for c,v in zip(cols,a[0]):z[c]=v
 Z.append(z)
 A=moments([H*s[r] for r in range(d)],1)
 Z.append(A+[H,f(0,1)-H-sum(A,zero)]+[zero]*d)
 for b in range(2,(N-1)//2+1):
  T=f(N-b,b)/G(N-b,b,-1,1)
  A=moments([(f(a,b)-T*G(a,b,-1,1))/G(a,b,1,1) for a in range(1,N-b)],1)
  vals=[f(0,b)-T-sum(A,zero)]+[(f(N-r,b)-T*G(N-r,b,-1,1))/G(N-r,b,-1,-1) for r in range(1,b)]
  B=moments(vals)
  Z.append(A+[T,zero]+B)
 def reflect(z):return z[d+2:]+[z[d+1],z[d]]+z[:d]
 for b in range((N+1)//2,N):Z.append(reflect(Z[N-b]))
 configs=[(1,1,v) for v in nodes]+[(-1,1,one),(1,-1,one)]+[(-1,-1,v) for v in nodes]
 for b,z in enumerate(Z):
  for a in range(N):
   actual=sum((z[i]*v**(e*a%N)*G(a,b,e,j) for i,(e,j,v) in enumerate(configs)),zero)
   assert actual==f(a,b),(N,a,b)
 C=sum((q**((-t*t)%N) for t in range(N)),zero)/K(N);assert C
 weights=[]
 for i,(e,j,v) in enumerate(configs):
  h=[zero]*N
  for b in range(N):h[j*b%N]=Z[b][i]
  delta=-v**N;assert delta
  w=[C*delta*sum((h[l]*q**((-e*j*r*l)%N) for l in range(N)),zero) for r in range(N)]
  for l in range(N):assert sum((w[r]*q**((e*j*r*l)%N) for r in range(N)),zero)/K(N)==C*delta*h[l]
  weights.append(w)
 # Independent literal target Weyl traces; no assumed chirp formula in this check.
 for a in range(N):
  for b in range(N):
   direct=sum((q**((-t*(t+a)-b*t)%N) for t in range(N)),zero)/K(N)
   assert direct==C*f(a,b)
 receipt={'N':N,'field_degree':K.mod.degree(),'banks':len(configs),'branches':len(configs)*N,'last_node':enc(x,N),'edge_denominator':enc(D,N),'axis_columns':cols,'normalized_coefficient_equations':N*N,'literal_target_weyl_traces':N*N,'raw_weight_character_checks':len(configs)*N,'all_nodes_and_weights_in_base_field':True,'literal_branches_checked':0,'literal_original_matrix_entries_checked':0}
 if literal:
  total=[[zero for t in range(N)] for k in range(N)]
  eye=[[one if k==t else zero for t in range(N)] for k in range(N)]
  for i,(e,j,v) in enumerate(configs):
   delta=-v**N
   for phase in range(N):
    z=q**(e*j*phase%N); diag=[z*q**(j*k%N) for k in range(N)]
    def left(A):return [[v*A[(k-e)%N][t]+diag[k]*A[k][t] for t in range(N)] for k in range(N)]
    P=[r[:] for r in eye];B=[r[:] for r in eye]
    for power in range(1,N):
     P=left(P);B=[[a+b for a,b in zip(r,sr)] for r,sr in zip(B,P)]
    V=[[u/delta for u in r] for r in B];LV=left(V)
    for k in range(N):
     for t in range(N):
      assert V[k][t]-LV[k][t]==eye[k][t]
      assert V[k][t]-v*V[k][(t+e)%N]-diag[t]*V[k][t]==eye[k][t]
      total[k][t]+=weights[i][phase]*V[k][t]/K(N)
    receipt['literal_branches_checked']+=1
   print('literal bank',N,i+1,'/',len(configs),flush=True)
  for k in range(N):
   for t in range(N):assert total[k][t]==q**((-k*t)%N)
  receipt['literal_original_matrix_entries_checked']=N*N
 receipt['seconds']=time.time()-t0
 witness={'N':N,'nodes':[enc(v,N) for v in nodes],'edge_annihilator':[enc(v,N) for v in g],'row_sector_amplitudes':[[enc(v,N) for v in z] for z in Z],'raw_weights':[[enc(v,N) for v in w] for w in weights]}
 (OUT/f'N{N}_BASEFIELD_WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
 (OUT/f'N{N}_CONTROL_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print('PASS',json.dumps(receipt),flush=True)
 return receipt
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('N',nargs='+',type=int);a.add_argument('--skip-literal',action='store_true');p=a.parse_args()
 for N in p.N:run(N,not p.skip_literal)
