#!/usr/bin/env python3
"""Audit frozen candidate bytes and witnesses; execute no candidate code."""
import hashlib,json,math
from pathlib import Path
from sympy import QQ,Poly,Symbol,cyclotomic_poly
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parent
P=Path('/workspace/shared/sparse_threeq_endpoint_20261019_1054')
EXPECTED='918a8048cf86741e1e58b070f2d96147be53732fb89b53d0274382b3af807b49'
x=Symbol('x')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def integrity():
    assert sha(P/'MANIFEST.json')==EXPECTED
    assert (P/'SEAL.sha256').read_text().split()[0]==EXPECTED
    manifest=json.loads((P/'MANIFEST.json').read_text())
    for f in manifest['files']:
        p=P/f['path']; assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
    sources=json.loads((P/'SOURCE_BINDINGS.json').read_text())
    for f in sources:
        for p in (P/f['copy'],Path(f['source'])):
            assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
    return {'manifest_sha256':EXPECTED,'report_sha256':sha(P/'REPORT.md'),'manifest_files':len(manifest['files']),'source_bindings':len(sources)}

class Field:
    def __init__(self,n):
        self.n=n; p=Poly(cyclotomic_poly(n,x),x); self.poly=list(map(int,reversed(p.all_coeffs())))
        self.F=QQ.alg_field_from_poly(p,alias='zeta'); F=self.F
        self.powers=[F.one]
        for j in range(1,n): self.powers.append(self.powers[-1]*F.unit)
        assert self.powers[-1]*F.unit==F.one
        self.I=self.matrix([[F.one if r==c else F.zero for c in range(n)] for r in range(n)])
        self.H=self.matrix([[self.powers[r*c%n] for c in range(n)] for r in range(n)])
    def matrix(self,rows): return DomainMatrix(rows,(self.n,self.n),self.F)
    def conj(self,a):
        val=self.F.zero
        for j,c in enumerate(reversed(a.to_list())): val+=self.F.convert(c)*self.powers[-j%self.n]
        return val
    def adj(self,A):
        rows=A.to_list(); return self.matrix([[self.conj(rows[c][r]) for c in range(self.n)] for r in range(self.n)])
    def decode_element(self,cs):
        v=self.F.zero
        for j,c in enumerate(cs): v+=self.F.convert(QQ(str(c)))*self.powers[j%self.n]
        return v
    def decode(self,A): return self.matrix([[self.decode_element(a) for a in row] for row in A])
    def mask(self,R): return self.matrix([[self.powers[r*c%self.n] if R[r][c] else self.F.zero for c in range(self.n)] for r in range(self.n)])
    def target(self,d): return self.I.scalarmul(self.F.convert(d)).to_list()

before=integrity(); fields={}
def fld(n):
    if n not in fields: fields[n]=Field(n)
    return fields[n]

positive=[]; negative=[]; gram_entries=0
for filename,store,expect in [('POSITIVE_CONTROLS.json',positive,True),('NEGATIVE_CONTROLS.json',negative,False)]:
    for w in json.loads((P/filename).read_text()):
        n,d=w['n'],w['d']; f=fld(n); R=w['R']; F=f.F
        assert w['cyclotomic_polynomial']==f.poly
        assert all(v in (0,1) for row in R for v in row)
        assert all(sum(row)==d for row in R)
        assert all(sum(R[r][c] for r in range(n))==d for c in range(n))
        D=f.mask(R); counts={}
        for side,G in [('row',D*f.adj(D)),('column',f.adj(D)*D)]:
            entries=G.to_list(); supplied={tuple(a['indices']):a for a in w[side+'_failures']}; actual={}; zero_counts={}
            for r in range(n):
                for s in range(n):
                    gram_entries+=1; val=entries[r][s]; order=n//math.gcd(r-s,n)
                    if r==s: assert val==F.convert(d); continue
                    if not val:
                        zero_counts[str(order)]=zero_counts.get(str(order),0)+1
                    else:
                        actual[(r,s)]=val
                        assert (r,s) in supplied
                        a=supplied[(r,s)]
                        assert a['difference_character_order']==order
                        assert f.decode_element(a['residue'])==val
                        assert f.decode_element(a['squared_modulus'])==val*f.conj(val)
            assert set(actual)==set(supplied)
            assert zero_counts==w['offdiagonal_zeros_by_character_order'][side]
            assert (not actual)==expect
            counts[side]=len(actual)
        store.append({'n':n,'d':d,'label':w['label'],'failure_counts':counts})

original=[]; inverse_entries=error_entries=0
for w in json.loads((P/'ORIGINAL_MODEL_CONTROLS.json').read_text()):
    n,d=w['n'],w['d']; s=n-d; f=fld(n); F=f.F
    assert w['cyclotomic_polynomial']==f.poly
    R=w['R']; D=f.mask(R); B=f.decode(w['B_tilde']); M=f.decode(w['M_tilde']); E=f.decode(w['E_tilde'])
    assert B.to_list()==f.adj(f.H-D).scalarmul(F.convert(QQ(1,s))).to_list()
    assert E.to_list()==(M-f.H).to_list()
    assert (B*M).to_list()==f.I.to_list()==(M*B).to_list()
    assert (f.adj(E)*E).to_list()==f.target(d)==(E*f.adj(E)).to_list()
    # Also check each retained mask's full Grams, regardless of any declared status.
    assert (f.adj(D)*D).to_list()==f.target(d)==(D*f.adj(D)).to_list()
    Bdata=B.to_list()
    assert all(sum(bool(a) for a in row)==s for row in Bdata)
    assert all(sum(bool(Bdata[r][c]) for r in range(n))==s for c in range(n))
    assert w['inverse_support_budget']==s
    assert str(QQ(w['normalized_squared_spectral_error']))==str(QQ(d,n))
    inverse_entries+=2*n*n; error_entries+=2*n*n
    original.append({'n':n,'d':d,'s':s,'all_matrix_identities_verified':True})
assert integrity()==before
out={'status':'PASS','candidate_integrity_before_and_after':before,'positive_witnesses':positive,'negative_witnesses':negative,'original_model_witnesses':original,'both_gram_entries_verified':gram_entries,'both_inverse_product_entries_verified':inverse_entries,'both_error_gram_entries_verified':error_entries,'candidate_or_historical_code_executed':False,'external_writes':False}
(ROOT/'CANDIDATE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
