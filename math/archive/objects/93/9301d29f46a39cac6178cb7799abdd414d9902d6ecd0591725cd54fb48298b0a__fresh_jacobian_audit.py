"""New exact sparse-inverse audit. Supplied Python files are never imported or evaluated."""
from pathlib import Path
import json,random,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'masks'))
from fresh_reconstruct import inverse,rankdet,FIELDS
SOURCE=ROOT/'source/fft_green_phase41_unit_holonomy'

def det(A,p):
 r,ids,v=rankdet(A,p)
 if r<len(A):return 0
 return v*((-1)**sum(ids[i]>ids[j] for i in range(len(ids)) for j in range(i+1,len(ids))))%p

def geometry(n,cycles,weights,p,k,phase,iota):
 count=len(cycles);greens=[];green_dets=[]
 for s,c in enumerate(cycles):
  H=[[int(i==j) for j in range(n)] for i in range(n)]
  for j in range(n):H[c[j]][c[j-1]]=(H[c[j]][c[j-1]]-weights[s*n+j])%p
  G,d=inverse(H,p);greens.append(G);green_dets.append(d)
 M=[[sum(G[i][j] for G in greens)%p for j in range(n)] for i in range(n)]
 _,mdet=inverse(M,p)
 inv=[[pow(M[i][j],-1,p) for j in range(k+1)] for i in range(2)]
 chords=list(range(n-1,count*n));J=[]
 for j in range(1,k+1):
  row=[]
  for e in chords:
   s,t=divmod(e,n);c=cycles[s];v,u=c[t],c[t-1];G=greens[s]
   f=iota*weights[e]%p if phase else 1
   a=G[0][v]*G[u][j]*inv[0][j]+G[1][v]*G[u][0]*inv[1][0]-G[1][v]*G[u][j]*inv[1][j]-G[0][v]*G[u][0]*inv[0][0]
   row.append(f*a%p)
  J.append(row)
 return J,dict(resolvent_determinants=green_dets,middle_sum_determinant=mdet,all_middle_entries_nonzero=all(x for row in M for x in row),all_selected_ratio_entries_nonzero=True)

def gaussian_weights(n,count,spec,p,ii):
 ws=[1]*(count*n)
 for e,(a,b) in zip(range(n-1,count*n),spec):
  assert (a+b*ii)%p and (a-b*ii)%p
  ws[e]=(a+b*ii)*pow((a-b*ii)%p,-1,p)%p
 return ws

def main():
 results=[]
 for kind,filename in [('two_phase','phase41_unit_jacobian_certificates.json'),('three_phase','phase41_three_cycle_certificates.json')]:
  cases=json.loads((SOURCE/filename).read_text())['cases'];count=2 if kind=='two_phase' else 3
  for c in cases:
   n=c['N'];cycles=c['cycle_orders'];spec=c['unit_gain_numerators'] if count==2 else c['gaussian_rational_unit_gain_ab'];k=4 if count==2 else n-1
   # Check explicit input arrays against the declared graph/gain seeds without importing source code.
   rr=random.Random(n+(40040 if count==2 else 41041));expected=[list(range(n))]
   for s in range(count-1):cy=list(range(n));rr.shuffle(cy);expected.append(cy)
   assert expected==cycles
   rr=random.Random(n+(41000 if count==2 else 41003));expected=[(rr.randrange(2,90 if count==2 else 100),rr.randrange(2,90 if count==2 else 100)) for _ in range((count-1)*n+1)];assert expected==[tuple(x) for x in spec]
   for p,g,_ in FIELDS:
    ii=pow(g,(p-1)//4,p);plus=gaussian_weights(n,count,spec,p,ii);minus=gaussian_weights(n,count,spec,p,-ii)
    assert all(a*b%p==1 for a,b in zip(plus,minus))
    Jp,gp=geometry(n,cycles,plus,p,k,True,ii);Jm,gm=geometry(n,cycles,minus,p,k,True,-ii)
    re=[[(a+b)*pow(2,-1,p)%p for a,b in zip(x,y)] for x,y in zip(Jp,Jm)]
    im=[[(a-b)*pow(2*ii%p,-1,p)%p for a,b in zip(x,y)] for x,y in zip(Jp,Jm)];A=re+im
    rank=rankdet(A,p)[0];assert rank==(6 if count==2 else 2*(n-1))
    cols=c['common_minor_chord_positions'] if count==2 else c['common_nonzero_minor_columns']
    rows=c['common_minor_real_imag_rows'] if count==2 else list(range(2*(n-1)))
    d=det([[A[i][j] for j in cols] for i in rows],p);source_dets=c['modular_determinants'] if count==2 else c['nonzero_minor_mod_two_primes'];assert d==source_dets[str(p)] and d
    extra={}
    if count==2:
     for ell in (2,3):
      sub=re[:ell]+im[:ell];rrank=rankdet(sub,p)[0];assert rrank==min(2*ell,ell+2);extra[str(ell)]=rrank
    results.append(dict(family=kind,N=n,prime=p,rank=rank,source_minor_matches=True,minor_determinant=d,minor_rows=rows,minor_columns=cols,smaller_k_ranks=extra,positive_embedding_guards=gp,conjugate_embedding_guards=gm,real_log_jacobian=A,cycles=cycles,gaussian_ab=spec))
    print(kind,n,p,rank,d,flush=True)
 # Reconstruct arbitrary-amplitude full signature using original common integer problem.
 for n in (8,16,32,64,128):
  r=random.Random(40040+n);c=list(range(n));r.shuffle(c);cycles=[list(range(n)),c];r=random.Random(40040+7919+n);raw=[[r.randrange(2,100000) for j in range(n)] for s in range(2)]
  for p,g,_ in FIELDS:
   D=[1]*n
   for j in range(1,n-1):D[j]=D[j-1]*raw[0][j]%p
   D[n-1]=pow(raw[0][0],-1,p);weights=[]
   for cy,ws in zip(cycles,raw):
    h=1
    for w in ws:h=h*w%p
    assert h!=1
    weights.extend([w*D[cy[j-1]]*pow(D[cy[j]],-1,p)%p for j,w in enumerate(ws)])
   J,guards=geometry(n,cycles,weights,p,n-1,False,0);rank=rankdet(J,p)[0];assert rank==n-1
   # Pivot rows of the transpose are independent columns of J.
   _,cols,_=rankdet([list(row) for row in zip(*J)],p);minor=[[row[c] for c in sorted(cols)] for row in J];d=det(minor,p);assert d
   results.append(dict(family='two_complex_amplitude',N=n,prime=p,rank=rank,source_reported_rank_matches=True,minor_determinant=d,minor_columns=sorted(cols),guards=guards,log_jacobian=J,cycles=cycles,integer_weights=raw))
   print('two_complex_amplitude',n,p,rank,d,flush=True)
 (ROOT/'FRESH_JACOBIAN_RESULTS.json').write_text(json.dumps({'supplied_code_executed':False,'records':results},indent=2)+'\n')
if __name__=='__main__':main()
