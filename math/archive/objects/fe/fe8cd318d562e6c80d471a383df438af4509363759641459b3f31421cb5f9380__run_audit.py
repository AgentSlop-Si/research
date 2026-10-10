"""Generate and independently replay all rank certificates; no timing claim."""
import json,time
from pathlib import Path
import numpy as np
import deferred_correction as d


def main():
    start=time.perf_counter();certificates=[]
    for p in (65537,998244353):
        for n in (2,4,8,16,32,64,128,256):
            cert=d.make_certificate(n,p)
            assert d.verify_certificate(cert)
            certificates.append(cert)
            print(f'p={p}, n={n}: rank={cert["rank_mod_p"]}, kernel={cert["kernel_dimension"]}',flush=True)
    rng=np.random.default_rng(9331);cores=[]
    for n in (4,8,16,32,64):
        m=n//2;f,c=d.matrices(m);one=np.ones(m,dtype=np.int64)
        for name,g in [('zero',np.zeros((m,m),dtype=np.int64)),('identity',np.eye(m,dtype=np.int64)),
                       ('sign_butterfly',c),('fourier',f),('random',rng.integers(0,65537,(m,m)))]:
            row=d.shared_core_audit(n,g,one);row['core']=name;cores.append(row)
    f,c,e=d.telescope(8);naive=d.naive_single_corrections(8);difference=(e-naive)%65537
    positions=np.argwhere(difference!=0);i,j=map(int,positions[0])
    record={'n':8,'prime':65537,'input_basis_index':j,'output_index':i,
            'correct_correction':int(e[i,j]),'naive_correction':int(naive[i,j]),
            'missing_mixed_term':int(difference[i,j]),'number_wrong_matrix_entries':len(positions)}
    Path('results/rank_certificates.json').write_text(json.dumps(certificates,indent=2)+'\n')
    Path('results/shared_cores.json').write_text(json.dumps(cores,indent=2)+'\n')
    Path('results/mixed_term_counterexample.json').write_text(json.dumps(record,indent=2)+'\n')
    summary={'certificates_passed':len(certificates),'different_shared_cores_checked':len(cores),
             'largest_certified_n':256,'largest_exact_complex_rank':247,
             'universal_lower_bound':'rank(F_N-C_G,D0) >= number of k with D[k] != D0[k]',
             'sign_only_lower_bound':'N/2 - 1','all_n_exact_rank_formula_proved':False,
             'new_sub_n_log_n_algorithm':False,'audit_elapsed_seconds':time.perf_counter()-start}
    Path('results/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
