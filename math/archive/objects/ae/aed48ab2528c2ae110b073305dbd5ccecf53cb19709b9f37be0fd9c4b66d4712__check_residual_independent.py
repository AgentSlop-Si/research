"""Audit-authored checks. No imports or execution from the uploaded archive."""
from pathlib import Path
from fractions import Fraction
from math import gcd
from itertools import product
import json, random, hashlib, ast
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,help='Optional extracted source root containing MANIFEST.json; only read as data')
args=parser.parse_args()
R=Path(__file__).resolve().parent
src=args.source
if src is None and (R/'extracted').is_dir():
    src=next((R/'extracted').iterdir())
manifest={}; mismatches=[];parse_count=0
if src is not None:
    manifest=json.loads((src/'MANIFEST.json').read_text())
    for rel,m in manifest.items():
        p=src/rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=m['sha256'] or p.stat().st_size!=m['bytes']: mismatches.append(rel)
    for p in src.rglob('*.py'):
        ast.parse(p.read_text());parse_count+=1

def f(coords):
 N=len(coords);q=gcd(N,4);n=N//q
 S=[[sum(coords[j][c] for j in range(s,N,q)) for c in range(2)] for s in range(q)]
 chosen=[[S[s][c] if sum(abs(n*coords[j][c]-S[s][c]) for j in range(s,N,q))<=n*sum(abs(coords[j][c]) for j in range(s,N,q)) else 0 for c in range(2)] for s in range(q)]
 rho=[tuple(n*x[c]-chosen[j%q][c] for c in range(2)) for j,x in enumerate(coords)]
 mass=lambda a:sum(abs(t) for v in a for t in v)
 assert mass(rho)<=n*mass(coords)
 for j,x in enumerate(coords):
  for c in range(2):assert Fraction(chosen[j%q][c]+rho[j][c],n)==x[c]
 # Independent rational reference spectrum at q exact frequencies.
 roots=[(1,0),(0,-1),(-1,0),(0,1)]
 def short(sums,t):
  real=imag=0
  for s,(a,b) in enumerate(sums):
   u,v=roots[(4*s*t//q)%4];real+=a*u-b*v;imag+=a*v+b*u
  return (real,imag)
 for t in range(q):
  raw=(0,0)
  for j,(a,b) in enumerate(coords):
   u,v=roots[(4*j*t//q)%4];raw=(raw[0]+a*u-b*v,raw[1]+a*v+b*u)
  assert raw==short(S,t)
 # Medians independently minimize L1 cluster mass among all integer candidates.
 med=[[sorted(coords[j][c] for j in range(s,N,q))[(n-1)//2] for c in range(2)] for s in range(q)]
 rmass=sum(abs(x[c]-med[j%q][c]) for j,x in enumerate(coords) for c in range(2))
 assert rmass*n<=mass(rho)
 return {'input_mass':mass(coords),'mean_residual_mass':str(Fraction(mass(rho),n)),'median_residual_mass':rmass}

rng=random.Random(72410); cases=0
for N in [1,2,3,4,5,6,7,8,9,12,16,20,24,31,32]:
 q=gcd(N,4);n=N//q
 for _ in range(100):
  coords=[(rng.randint(-100,100),rng.randint(-100,100)) for j in range(N)];f(coords);cases+=1
  comparison=[(Fraction(rng.randint(-20,20),3),Fraction(rng.randint(-20,20),7)) for _ in range(q)]
  means=[[Fraction(sum(coords[j][c] for j in range(s,N,q)),n) for c in range(2)] for s in range(q)]
  meanmass=sum(abs(x[c]-means[j%q][c]) for j,x in enumerate(coords) for c in range(2))
  emass=sum(abs(x[c]-comparison[j%q][c]) for j,x in enumerate(coords) for c in range(2))
  assert meanmass<=2*emass
  baseline=[(rng.randint(-10,10),rng.randint(-10,10)) for _ in range(q)]
  assert f([baseline[j%q] for j in range(N)])['mean_residual_mass']=='0';cases+=1
worst=f([(1,0)]*4+[(-1,0)]*4)
assert worst['input_mass']==int(worst['mean_residual_mass'])==worst['median_residual_mass']
# A one-cluster inlier-heavy example approaching the factor-two mean loss.
example=f([(100,0)]*20+[(101,0)])
result={'source_manifest_supplied':src is not None,'manifest_entries_verified':len(manifest),'manifest_mismatches':mismatches,'uploaded_python_ast_parsed':parse_count,'uploaded_code_executed':False,'independent_rational_cases':cases,'worst_case_N8':worst,'near_periodic_N21':example,'status':'PASS' if not mismatches else 'FAIL'}
(R/'independent_residual_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
