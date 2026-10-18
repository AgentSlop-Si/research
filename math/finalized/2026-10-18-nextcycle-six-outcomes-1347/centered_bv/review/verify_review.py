"""Verify the frozen independent review and retained exact conclusions."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
HERE=Path(__file__).resolve().parent
def load(name):return json.loads((HERE/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest=load('MANIFEST.json');seal=load('SEAL.json')
    assert sha(HERE/'MANIFEST.json')==seal['manifest_sha256']
    assert len(manifest)==seal['members']
    for rel,expected in manifest.items():assert sha(HERE/rel)==expected,rel
    r=load('FRESH_SOURCE_REPRODUCTION.json');o=load('INDEPENDENT_OUTPUT_CHECKS.json')
    assert r['replay_passed'] and o['fresh_source_pairs_identical']
    assert r['production']['events']['dense_coordinate_visits']==512
    assert r['semantic_source_replay']['replay_production']['events']['dense_coordinate_visits']==512
    assert o['all_original_rows_checked']==512 and o['all_centered_coefficients_checked']==2048
    assert o['retained_complex_rho_checks']==49 and o['global_beta_one_quarter_checks']==2048
    assert Fraction(*o['relative_error_upper_rational'])==Fraction(53,1000)
    a=load('INDEPENDENT_RETAINED_CHECKS.json')
    assert a['all_retained_operator_rows_checked']==512 and a['independently_enumerated_incidences']==21609
    for row in a['rows']:assert Fraction(*row['squared_error_upper'])<=Fraction(*row['squared_allowed'])
    c=load('INDEPENDENT_CONTROLS.json')
    assert c['all_eleven_rejection_prefixes_identical'] and len(c['rejections'])==11
    assert len(c['complex_coefficients_independently_checked'])==7
    s=load('REPRODUCTION_COMPARISON.json')
    assert s['estimates_exactly_identical'] and s['front_production_receipt_exactly_identical'] and s['complete_source_replay_receipt_exactly_identical']
    assert s['candidate_manifest_sha256']==seal['candidate_manifest_sha256']
    print(json.dumps({'accepted':True,'members':len(manifest),'candidate_manifest_sha256':seal['candidate_manifest_sha256']}))
if __name__=='__main__':main()
