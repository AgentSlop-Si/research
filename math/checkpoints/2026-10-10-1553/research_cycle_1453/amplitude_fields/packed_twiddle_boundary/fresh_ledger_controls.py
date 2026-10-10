#!/usr/bin/env python3
"""New standalone integer/rational ledger checks; no source programs imported."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]

def params(v,t):
    p=t+10+v.bit_length();E=2*v+p+5;k=E.bit_length();b=2*(p+k+1);g=p+10
    assert 64*b<=v
    P=1<<((v//(16*b)).bit_length()-1)
    assert P>=4 and 16*b*P<=v<32*b*P
    R=1<<b;S=1<<(b*P);Q=1<<g;d=P.bit_length()-1
    total=S*S+(Q-1+d)*S+Q*R+R*R
    phase=(Q-1)*S+Q*R
    assert Q<=2**10 * (1<<(b//2))
    assert F(Q,S)<=F(2)**(10-F(7*b,2))
    assert F(phase,total)<F(2*Q,S)
    B=0
    while 3*((1<<(B+1))+1)**2<(Q+9)//10:B+=1
    return {'v':v,'t':t,'p':p,'b':b,'P':P,'g':g,'log2_S':b*P,
            'log2_Q_over_S':g-b*P,'log2_phase_deletion_fraction_upper':1+g-b*P,
            'HP_entries_bit_length':(S*S).bit_length(),
            'full_response_entries_bit_length':total.bit_length(),
            'minimum_bounded_pair_coefficient_bits_from_tuple_count':B,
            'required_distinct_tuples_lower':str((Q+9)//10),
            'leading_bit_chunk_exponent':v//8}

def gap_tests():
    out=[]
    for g in range(3,31):
        Q=1<<g;a=(Q+1)//3;gaps=[a,Q-2*a,a]
        assert all(F(1,4)<=F(x,Q)<=F(3,8) for x in gaps)
        out.append({'g':g,'a':a,'gaps':gaps})
    return out

def bitserial():
    count=0
    zvalues=[F(-3,4),F(-1,8),F(0),F(1,2),F(5,4)]
    for B in range(1,9):
        for n in range((1<<(B+1))+1):
            for z in zvalues:
                terms=[(F(2)**(ell-B))*z for ell in range(B+2) if (n>>ell)&1]
                assert sum(terms,F(0))==F(n,1<<B)*z
                count+=1
    return count

def main():
    rows=[params(v,t) for v,t in [(5120,2),(5888,8),(6912,16),(11904,53)]]
    gaps=gap_tests();binary=bitserial()
    files={'split_construction':ROOT/'packed_improvement/SPLIT_TABLE_CONSTRUCTION.md',
           'split_review':ROOT/'packed_adversarial/SPLIT_TABLE_INDEPENDENT_REVIEW.md',
           'exact_core':OUT.parent/'AMPLITUDE_FIELD_THEOREM_v2.md',
           'approximation':OUT.parent/'approximation_boundary/RATIONAL_APPROXIMATION_BOUNDARY.md'}
    source_hashes={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()}
    assert source_hashes['split_construction']=='be8de35159ed47f2a5d0bad71937d83bb7053ef83ae6ce358c0dfd80add78ded'
    assert source_hashes['exact_core']=='b01e17257b240f6b5d4618270f636f4deaecdb70cf273c13ecce904f551c326d'
    assert source_hashes['approximation']=='f1de8df712476b57a601cfefa2891ba3672190897fac43fa3ccda9bc91ec11d2'
    result={'status':'PASS','source_programs_executed':False,'source_programs_imported':False,
            'source_documents_read_as_bytes_only':True,'threshold_cases':rows,'power_of_two_gap_cases':len(gaps),
            'gap_cases':gaps,'exact_bitserial_identities':binary,'source_sha256':source_hashes,
            'scope':'Exact symbolic ledger and arithmetic-identity controls; no new packed executor or runtime implementation claimed'}
    (OUT/'FRESH_LEDGER_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
