#!/usr/bin/env python3
"""Independent finite-field checks of the v21 packet/line identities."""
from pathlib import Path
from fractions import Fraction
from itertools import permutations
import json
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def block(n,p,w,a,x):
 inv2=pow(2,-1,n)
 return [[pow(a,d*pow(h,-1,n)%n,p)*pow(w,(-x*d*(d-h)*inv2)%n,p)%p for h in range(1,n)] for d in range(1,n)]
def green(n,p,w,a,h,r):
 f=Field(p);mat=f.eye(n)
 for j in range(n):mat[(j+h)%n][j]=(mat[(j+h)%n][j]-a*pow(w,r*j%n,p))%p
 inv=f.inverse(mat);assert f.mul(mat,inv)==f.eye(n);return inv

def case(n,p,w,a,saved=None,full_rank=True):
 assert prime_by_trial_division(n) and n%2 and prime_by_trial_division(p)
 assert w!=1 and pow(w,n,p)==1 and a%p and pow(a,n,p)!=1
 f=Field(p);den=f.inv(1-pow(a,n,p));ivn=f.inv(n);two=pow(2,-1,n)
 blocks=[block(n,p,w,a,x) for x in range(n)];ranks=[f.rank(b) for b in blocks];assert ranks==[n-1]*n
 packets=[];labels=[];greens={};support=[];filtered_entries=0
 for h in range(1,n):
  gs=[green(n,p,w,a,h,r) for r in range(n)]
  for r,g in enumerate(gs):greens[h,r]=g
  for s in range(n):
   mat=[[0]*n for _ in range(n)]
   # Direct filtered geometric powers, with one position for each (m,j).
   for m in range(n):
    for j in range(n):
     if (m*j+h*m*(m-1)//2-s)%n==0:mat[(j+m*h)%n][j]=den*pow(a,m,p)%p
   # Independent resolvent character sum, all entries and all packets.
   for i in range(n):
    for j in range(n):
     rhs=ivn*sum(pow(w,(-r*s)%n,p)*gs[r][i][j] for r in range(n))%p
     assert mat[i][j]==rhs;filtered_entries+=1
   rowmax=max(sum(bool(v) for v in row) for row in mat);colmax=max(sum(bool(mat[i][j]) for i in range(n)) for j in range(n))
   total=sum(bool(v) for row in mat for v in row)
   assert rowmax<=2 and colmax<=2 and total==(2*n-1 if s==0 else n-1)
   packets.append(mat);labels.append((h,s));support.append((h,s,rowmax,colmax,total))
 off=[[mat[i][j] for mat in packets] for i in range(n) for j in range(n) if i!=j]
 offrank=f.rank(off) if full_rank else sum(ranks)
 assert offrank==n*(n-1)
 # Recover an arbitrary constant-diagonal matrix via displacement transforms.
 target=[[(37*i+19*j+11*i*j+7)%p if i!=j else 13%p for j in range(n)] for i in range(n)]
 chat={h:[0]*n for h in range(1,n)}
 for x in range(n):
  rhs=[]
  for d in range(1,n):rhs.append((1-pow(a,n,p))*sum(target[(j+d)%n][j]*pow(w,(x*d*j)%n,p) for j in range(n))%p)
  sol=f.solve(blocks[x],rhs)
  for h,value in zip(range(1,n),sol):chat[h][x*h%n]=value
 coeff={(h,s):ivn*sum(chat[h][ell]*pow(w,(-ell*s)%n,p) for ell in range(n))%p for h in range(1,n) for s in range(n)}
 recon=[[sum(coeff[label]*mat[i][j] for label,mat in zip(labels,packets))%p for j in range(n)] for i in range(n)]
 diag=(target[0][0]-recon[0][0])%p
 assert all((recon[i][j]+diag*int(i==j))%p==target[i][j] for i in range(n) for j in range(n))
 # Fourier line coefficients use only B_1, not a flattened overdetermined solve.
 A=f.solve(blocks[1],[(1-pow(a,n,p))*pow(w,(-d*d)%n,p)%p for d in range(1,n)])
 lam=(1-den*sum(A))%p;fourier=[[pow(w,(i*j-i*i)%n,p) for j in range(n)] for i in range(n)]
 assert all((lam*int(i==j)+sum(A[h-1]*greens[h,(-h)%n][i][j] for h in range(1,n)))%p==fourier[i][j] for i in range(n) for j in range(n))
 # Iteratively generate U^h, independently of the closed phase formula.
 u=[[0]*n for _ in range(n)]
 for j in range(n):u[(j+1)%n][j]=pow(w,(-j)%n,p)
 power=f.eye(n);poly=[[0]*n for _ in range(n)];cc=[]
 for h in range(n):
  c=pow(w,(-h*(h+1)*two)%n,p);cc.append(c)
  for i in range(n):
   for j in range(n):poly[i][j]=(poly[i][j]+c*power[i][j])%p
  if h:
   phase=pow(w,(h*(h-1)*two)%n,p)
   assert all(phase*power[i][j]%p==(pow(w,(-h*j)%n,p) if i==(j+h)%n else 0) for i in range(n) for j in range(n))
  power=f.mul(u,power)
 assert power==f.eye(n) and poly==fourier
 spectrum=[sum(cc[h]*pow(w,k*h%n,p) for h in range(n))%p for k in range(n)];assert all(spectrum)
 assert all(pow(w,i*j%n,p)==pow(w,((i*i-(i-j)**2+j*j)*two)%n,p) for i in range(n) for j in range(n))
 if saved:
  assert ranks==saved['block_ranks'] and offrank==saved['packet_offdiag_rank']
  assert lam==saved['green_line_identity_scalar'] and sum(bool(v) for v in A)==saved['green_line_nonzero_coefficients']
  samples=[next(r[2:] for r in support if r[:2]==pair) for pair in [(1,0),(1,1),(2,0),(2,3%n)]]
  assert [list(t) for t in samples]==saved['packet_degree_samples']
 # Nonpole exceptional controls: alpha=0 and alpha=-1 invalidate completeness.
 assert f.rank(block(n,p,w,0,0))==0
 minus=block(n,p,w,p-1,0)
 assert all(minus[n-d-1]==[(-v)%p for v in minus[d-1]] for d in range(1,n))
 assert f.rank(minus)<= (n-1)//2 and (1-pow(p-1,n,p))%p!=0
 return {'n':n,'field_prime':p,'omega':w,'alpha':a,'block_ranks':ranks,'offdiag_rank':offrank,'full_offdiag_rank_computed':full_rank,'resolvent_character_entries_checked':filtered_entries,'all_packets_checked':len(packets),'line_coefficients':A,'line_scalar':lam,'line_nonzero_coefficients':sum(bool(v) for v in A),'chirp_spectrum':spectrum,'arbitrary_constant_diagonal_reconstruction':True,'exceptional_minus_one_block_rank':f.rank(minus)}

def leading_controls():
 out=[]
 for n in (3,5,7):
  perm=list(permutations(range(1,n)));values=[]
  for pi in perm:values.append((sum(d*pow(h,-1,n)%n for d,h in zip(range(1,n),pi)),pi))
  lo=min(e for e,pi in values);hi=max(e for e,pi in values)
  assert [pi for e,pi in values if e==lo]==[tuple(range(1,n))] and lo==n-1
  assert [pi for e,pi in values if e==hi]==[tuple(n-d for d in range(1,n))] and hi==(n-1)**2
  out.append({'n':n,'permutations':len(perm),'unique_low_degree':lo,'unique_top_degree':hi})
 # Exact rational dominance magnitudes, with no finite-field modulus interpretation.
 dominance=[]
 for n in (3,5,7,11,17,31,127,257,1021):
  for a in (Fraction(1,2),Fraction(1,3)):
   off=sum(a**m for m in range(2,n));gap=a-off
   assert gap>0
   if a==Fraction(1,2):assert gap==Fraction(1,2**(n-1))
   else:assert gap>Fraction(1,6)
   assert all(sorted(d*pow(h,-1,n)%n for h in range(1,n))==list(range(1,n)) for d in (1,2,n-1))
   dominance.append({'n':n,'alpha':str(a),'gap':str(gap)})
 return {'exhaustive_determinant_controls':out,'complex_modulus_dominance_controls':dominance}

if __name__=='__main__':
 source=json.loads((BASE/'sources/results.json').read_text());records=[]
 for r in source['finite_field_cases']:
  records.append(case(r['n'],r['field_prime'],r['omega'],r['alpha'],r));print('Source case',r['n'],'PASS',flush=True)
 for n in (3,5,19):
  found=None
  for p in range(2*n+1,2000,n):
   if not prime_by_trial_division(p):continue
   w=next((pow(g,(p-1)//n,p) for g in range(2,p) if pow(g,(p-1)//n,p)!=1),None)
   if w is None:continue
   for a in range(2,p):
    if pow(a,n,p)!=1 and all(Field(p).rank(block(n,p,w,a,x))==n-1 for x in range(n)):found=(p,w,a);break
   if found:break
  assert found;records.append(case(n,*found,full_rank=n<=5));print('Additional case',n,'PASS',flush=True)
 result={'status':'PASS','cases':records,'formal_guard_controls':leading_controls(),'source_programs_executed':False,'scope':'Odd-prime full matrix identities; conventional chirp convolution and no faster-FFT claim'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('PASS all identities and guards',flush=True)
