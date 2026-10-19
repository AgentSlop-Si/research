"""Audit frozen candidate as data only; execute only the new review checker."""
from pathlib import Path
import hashlib
import json
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from independent_checks import grams, Roots, write

P=Path('/workspace/shared/sparse_threeq_interior_20261019_1220')
EXPECTED_MANIFEST='597d0de53a54cdc28f8d3d4130ce0df5acfd790b51c11cbcbf10956214ebb8ed'
EXPECTED_REPORT='adb4b382dad3de602d802214b5b548a107683158777c1421156b21be4965c3d8'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def integrity():
    assert sha(P/'MANIFEST.json')==EXPECTED_MANIFEST
    assert sha(P/'REPORT.md')==EXPECTED_REPORT
    assert (P/'SEAL.sha256').read_text().split()[0]==EXPECTED_MANIFEST
    manifest=json.loads((P/'MANIFEST.json').read_text())
    for f in manifest['files']:
        path=P/f['path']
        assert path.stat().st_size==f['bytes'] and sha(path)==f['sha256']
    sources=json.loads((P/'SOURCE_BINDINGS.json').read_text())
    for s in sources:
        assert sha(P/s['copy'])==sha(Path(s['source']))==s['sha256']
        assert (P/s['copy']).stat().st_size==s['bytes']
    return {'manifest_sha256':EXPECTED_MANIFEST,'report_sha256':EXPECTED_REPORT,
            'manifest_files_checked':len(manifest['files']),'source_bindings_checked':len(sources)}

def audit_grams(filename,positive):
    records=json.loads((P/filename).read_text());audits=[]
    for rec in records:
        n,d,R=rec['n'],rec['d'],rec['R']
        result=grams(R,d)
        assert rec['row_degrees']==list(map(sum,R))
        assert rec['column_degrees']==[sum(R[r][c] for r in range(n)) for c in range(n)]
        assert [int(v) for v in rec['cyclotomic_polynomial']]==Roots(n).phi
        for order in ('row','column'):
            recomputed={tuple(f['indices']):f['residue'] for f in result[order]['failures']}
            retained={tuple(f['pair']):[int(v) for v in f['value']] for f in rec['failures'][order]}
            assert recomputed==retained
            assert result[order]['zero_off_diagonal_by_order']==rec['offdiagonal_zeros_by_order'][order]
            assert bool(recomputed) != positive
        audits.append({'label':rec['label'],'N':n,'d':d,'both_Grams_recomputed':True,
                       'row_nonzeros':len(result['row']['failures']),'column_nonzeros':len(result['column']['failures'])})
    return audits

def audit_original(rec):
    n,d,R=rec['n'],rec['d'],rec['R'];X=sp.Symbol('X')
    field=sp.QQ.algebraic_field(sp.CRootOf(sp.cyclotomic_poly(n,X),0))
    z=field.unit;zero=field.zero;one=field.one;power=[z**e for e in range(n)]
    def dm(rows):return DomainMatrix(rows,(n,n),field)
    def decode(A):
        return dm([[sum((field.convert(sp.Rational(c))*power[j] for j,c in enumerate(v)),zero)
                    for v in row] for row in A])
    def star(A):
        values=A.to_list()
        def conj(v):
            ans=zero
            for c in v.to_list():ans=ans*power[-1]+field.convert(c)
            return ans
        return dm([[conj(values[c][r]) for c in range(n)] for r in range(n)])
    H=dm([[power[r*c%n] for c in range(n)] for r in range(n)])
    D=dm([[power[r*c%n] if R[r][c] else zero for c in range(n)] for r in range(n)])
    I=dm([[one if r==c else zero for c in range(n)] for r in range(n)])
    B=decode(rec['B_tilde']);M=decode(rec['M_tilde']);E=decode(rec['E'])
    assert B==star(H-D).scalarmul(field.convert(sp.Rational(1,n-d)))
    assert E==M-H
    assert D*star(D)==star(D)*D==I.scalarmul(field.convert(d))
    assert B*M==M*B==I
    assert E*star(E)==star(E)*E==I.scalarmul(field.convert(d))
    rows=B.to_list()
    assert {sum(v!=zero for v in row) for row in rows}=={n-d}
    assert {sum(rows[r][c]!=zero for r in range(n)) for c in range(n)}=={n-d}
    assert rec['inverse_support_budget']==n-d
    return {'N':n,'d':d,'both_mask_Grams':True,'B_definition':True,'E_definition':True,
            'both_inverse_products':True,'both_error_Grams':True,'all_inverse_supports':n-d}

def main():
    result={'candidate_path':str(P),'before':integrity(),'candidate_code_executed':False}
    result['positive_masks']=audit_grams('POSITIVE_CONTROLS.json',True)
    result['negative_masks']=audit_grams('NEGATIVE_CONTROLS.json',False)
    result['original_models']=[audit_original(r) for r in json.loads((P/'ORIGINAL_MODEL_CONTROLS.json').read_text())]
    result['after']=integrity()
    result['both_integrity_checks_identical']=result['before']==result['after']
    result['full_Gram_entries_each_order']=sum(r['N']**2 for r in result['positive_masks']+result['negative_masks'])
    result['inverse_product_entries_each_order']=sum(r['N']**2 for r in result['original_models'])
    write('CANDIDATE_AUDIT.json',result)
    print(json.dumps({k:result[k] for k in ('before','full_Gram_entries_each_order','inverse_product_entries_each_order')},indent=2))

if __name__=='__main__':main()
