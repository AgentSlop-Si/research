"""Verify completed packet bytes and exact summary claims without rerunning production."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,argparse
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((HERE/n).read_text())
def frac(x):return F(*x)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fresh',action='store_true');args=parser.parse_args()
    R=load('RESULTS.json');O=load('OUTPUT.json');T=load('TARGET_CHECKS.json');P=load('PROVIDER_CHECKS.json');C=load('FRESH_CHECKS.json')
    assert R['full_outer_executed'] and R['source_replay_executed']
    assert R['dense_coordinates_read']==1024 and R['provider_runs']==2
    assert R['sparse_records']==49 and R['provider_records']==98 and R['cutoff']==24
    assert R['coefficients']==21609 and R['output_rows']==512
    assert O['source']==R['source'] and O['source']['blocks']==[[173,1,0],[384,2,0],[512,-1,0]]
    assert O['source']['energy']==1145 and O['source']['variation_l1']==6 and O['source']['variation_factor']==3
    assert O['source']['h']==6 and O['source']['scale']==44
    assert O['output']['bits']==0 and O['output']['normalized_bits']==25 and O['output']['incidences']==21609
    assert len(O['output']['pairs'])==512 and len(O['estimates']['pairs'])==49
    assert T['all_original_outputs_checked']==512 and T['direct_sum_terms']==512**2
    assert frac(T['squared_relative_error_upper'])<=frac(T['relative_error_upper_rational'])**2
    assert max(map(frac,T['row_squared_error_upper']))==frac(T['maximum_squared_error_upper'])
    assert P['all_centered_coefficients_checked']==2048 and P['retained']==49 and P['omitted']==1999
    assert P['all_retained_complex_radii_at_most_rho'] and P['all_global_premise_checks_passed']
    assert len(C['rejection_controls'])==11 and all(x['rejected'] for x in C['rejection_controls'])
    assert len(C['complex_coefficient_checks'])==7 and C['same_original_dense_and_blocks']
    assert len(R['controls'])==4 and all(x['rejected'] for x in R['controls'])
    rec=R['receipts'];assert rec['front_production']['events']['dense_coordinate_visits']==512
    assert rec['source_replay']['replay_production']['events']['dense_coordinate_visits']==512
    assert rec['front_production']['events']['coefficient_outputs']==49
    assert rec['source_replay']['replay_production']['events']['coefficient_outputs']==49
    o=rec['outer_transfer'];assert o['state']=='COMPLETE' and o['coefficients_evaluated']==21609
    assert o['scalar']['operations']['coefficient_call']==o['scalar']['operations']['certificate_pass']==21609
    assert o['scalar']['operations']['pi_setup']==o['scalar']['operations']['sqrt_setup']==1
    for rel,binding in load('SOURCE_BINDINGS.json').items():assert sha(HERE/rel)==binding['sha256']
    if not args.fresh:
        manifest=load('MANIFEST.json');seal=load('SEAL.json')
        assert sha(HERE/'MANIFEST.json')==seal['manifest_sha256']
        for rel,want in manifest.items():assert sha(HERE/rel)==want,rel
    print(json.dumps({'accepted_byte_and_result_checks':True,'fresh_mode':args.fresh,'source_members':len(load('SOURCE_BINDINGS.json'))}))
if __name__=='__main__':main()
