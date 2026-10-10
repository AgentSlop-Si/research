"""Construct explicit local + interstage diagonal gauge tangent directions.
Demonstrates they explain every generic tangent null vector before saturation.
"""
import random,tempfile,subprocess,json
from pathlib import Path
import numpy as np
from multistage_jacobian import materialize
HERE=Path(__file__).resolve().parent

def bitrev(n):
  m=(n-1).bit_length();return [int(format(i,f'0{m}b')[::-1],2) for i in range(n)]

def stage_idx(stage,term,i,n):
  offsets={'d':0,'L':1,'V':2,'U':3,'W':4}
  return stage*(5*n)+offsets[term]*n+i

def gauges(n,t,par,perms,p):
  params=t*5*n
  allcols=[]
  for s in range(t):
    # inactive scalar generator coordinates
    for term,i in [('L',0),('V',n-1),('U',n-1),('W',0)]:
      v=np.zeros(params,dtype=np.int64)
      v[stage_idx(s,term,i,n)]=1
      allcols.append(v)
    # internal scale of rank-one lower and upper generator pairs
    for plus,minus in [('L','V'),('U','W')]:
      v=np.zeros(params,dtype=np.int64)
      for i in range(n):
        v[stage_idx(s,plus,i,n)]=int(par[s][plus][i,0])
        v[stage_idx(s,minus,i,n)]=-int(par[s][minus][i,0])
      allcols.append(v)
  # interstage diagonal gauge: row scale in stage s,
  # paired with inverse column scale in stage s+1 after permutation.
  for s in range(t-1):
    inv=[0]*n
    for row,prior in enumerate(perms[s]):inv[prior]=row
    for i in range(n):
      j=inv[i]
      v=np.zeros(params,dtype=np.int64)
      for term in ('d','L','U'):
        val=int(par[s][term][i] if term=='d' else par[s][term][i,0])
        v[stage_idx(s,term,i,n)]+=val
      for term in ('d','V','W'):
        val=int(par[s+1][term][j] if term=='d' else par[s+1][term][j,0])
        v[stage_idx(s+1,term,j,n)]-=val
      allcols.append(v)
  return np.array(allcols,dtype=np.int64).T%p

def rank_cpp(M,p):
  with tempfile.TemporaryDirectory() as tmp:
    file=Path(tmp)/'matrix.dat';M.astype(np.int32).tofile(file)
    out=subprocess.check_output([str(HERE/'rankmod'),str(file),str(M.shape[0]),str(M.shape[1]),str(p)],text=True)
  return int(out.split('rank=')[1].split()[0])

def run(n,t,p=12289,seed=99017):
  perms=[bitrev(n)]*(t-1)
  _,J,pars,mats=materialize(n,t,perms,seed,p)
  G=gauges(n,t,pars,perms,p)
  expected=6*t+(t-1)*n
  assert G.shape==(5*n*t,expected)
  killed=(J@G)%p
  assert not np.any(killed), ('nonzero gauge tangent',int(np.count_nonzero(killed)))
  rg=rank_cpp(G,p);rj=rank_cpp(J,p)
  assert rg==expected
  nullity=J.shape[1]-rj
  return {'n':n,'t':t,'field':p,'jacobian_rank':rj,'jacobian_nullity':nullity,
          'gauge_directions':expected,'independent_gauges':rg,
          'all_gauges_killed_by_jacobian':True,
          'gauge_complete':expected==nullity}

if __name__=='__main__':
  results=[]
  for n,t in [(8,2),(8,3),(16,4),(16,5),(32,8),(32,9)]:
    for p in (12289,65537):
      item=run(n,t,p)
      results.append(item)
      print(json.dumps(item),flush=True)
  (HERE/'GAUGE_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
