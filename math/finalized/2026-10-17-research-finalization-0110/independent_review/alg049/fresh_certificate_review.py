"""Safe data-only proof review of published author polynomial strings."""
import ast, json, hashlib, sys
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).parent
source=Path(sys.argv[1] if len(sys.argv)>1 else 'CUT_CERTIFICATES.json')
author=json.loads(source.read_text())
fresh=json.loads((P/'FRESH_ALL_MINORS.json').read_text())
grams=json.loads((P/'FRESH_GRAMS.json').read_text())

def add(a,b):
 c=a.copy()
 for k,v in b.items():
  c[k]=c.get(k,F(0))+v
  if not c[k]:del c[k]
 return c

def scale(a,x):return {k:v*x for k,v in a.items() if v*x}
def mul(a,b):
 c={}
 for k,v in a.items():
  for l,w in b.items():c[k+l]=c.get(k+l,F(0))+v*w
 return {k:v for k,v in c.items() if v}
def parse(s):
 def walk(n):
  if isinstance(n,ast.Constant) and type(n.value) is int:return {0:F(n.value)} if n.value else {}
  if isinstance(n,ast.Name) and n.id=='z':return {1:F(1)}
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return scale(walk(n.operand),-1)
  if isinstance(n,ast.BinOp):
   a,b=walk(n.left),walk(n.right)
   if isinstance(n.op,ast.Add):return add(a,b)
   if isinstance(n.op,ast.Sub):return add(a,scale(b,-1))
   if isinstance(n.op,ast.Mult):return mul(a,b)
   if isinstance(n.op,ast.Div) and set(b)=={0} and b[0]:return scale(a,1/b[0])
   if isinstance(n.op,ast.Pow) and set(b)=={0} and b[0].denominator==1 and 0<=b[0]<=30:
    r={0:F(1)}
    for _ in range(int(b[0])):r=mul(r,a)
    return r
  raise ValueError('Unrecognized polynomial expression')
 return walk(ast.parse(s,mode='eval').body)

expected={(s1,s2,tuple((0,)+e)) for s1,s2 in [(-1,-1),(-1,1),(1,-1),(1,1)] for e in __import__('itertools').combinations(range(2,8),3)}
seen=set();rows=[];bad=0
for c in author['certificates']:
 s1,s2=c['signs'];A=tuple(c['A']);B=tuple(c['B']);key=f'{s1},{s2}/{A}'
 assert set(A).isdisjoint(B) and set(A)|set(B)==set(range(8))
 assert (s1,s2,A) in expected and (s1,s2,A) not in seen
 seen.add((s1,s2,A))
 assert c['scale_z']==2
 g=grams[f'{s1},{s2}']
 # Verify stated scaled Gram is a polynomial matrix, including no negative powers.
 for row in g['entries']:
  for e in row:
   assert all(int(k)+2>=0 and (F(v)*c['scale_den']/g['denominator']).denominator==1 for k,v in e.items())
 ps=[]
 for m in c['minors']:
  f=next(e for e in fresh[key] if e['rows']==m['R'] and e['cols']==m['C'])
  q={int(k):F(v) for k,v in f['polynomial'].items()};lo=min(q);hi=max(q)
  normalized={k-lo:v/q[hi] for k,v in q.items()}
  assert m['valuation']==lo+6
  assert normalized==parse(m['p'])
  ps.append(normalized)
 assert len(ps)==len(c['bezout'])
 bez={}
 for poly,coef in zip(ps,c['bezout']):bez=add(bez,mul(poly,parse(coef)))
 assert bez=={0:F(1)} and c['gcd']=='1'
 # A change of +1 to one witness coefficient must break the identity.
 corrupted=add(parse(c['bezout'][0]),{0:F(1)})
 corrupt_sum={}
 for idx,(poly,coef) in enumerate(zip(ps,c['bezout'])):corrupt_sum=add(corrupt_sum,mul(poly,corrupted if idx==0 else parse(coef)))
 assert corrupt_sum!={0:F(1)}
 bad+=1
 rows.append({'signs':[s1,s2],'cut':A,'minor_count':len(ps),'exact_bezout_identity':'PASS','fresh_reconstruction':'PASS'})
assert seen==expected
result={'verdict':'PASS','author_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cuts':len(rows),'independently_reconstructed_minors':sum(r['minor_count'] for r in rows),'exact_bezout_identities':len(rows),'corruption_controls_rejected':bad,'method':'Fresh integer Laurent matrices and data-only restricted AST polynomial parser; no author or historical program executed','results':rows}
(P/'INDEPENDENT_CERTIFICATE_ACCEPTANCE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
