import hashlib
import json
import math
from pathlib import Path
import numpy as np
from head_energy import head_energy_fft, adversary_prefix_certificate


def main():
    exact = []
    for m in range(1,15):
        certificates = [adversary_prefix_certificate(m,h) for h in range(2**m+1)]
        assert all(c['certified_total_lower_bound'] >= c['universal_hybrid_lower_bound']
                   for c in certificates)
        best = min(certificates, key=lambda c: c['certified_total_lower_bound'])
        exact.append({'m':m, 'n':4**m, 'head_sizes_checked':len(certificates),
                      'minimum_certified_butterflies':best['certified_total_lower_bound'],
                      'universal_lower_bound':best['universal_hybrid_lower_bound']})
    numeric = []
    rng = np.random.default_rng(901)
    for n in [64,256,1024,4096]:
        s = math.isqrt(n)
        families = {}
        prefix = np.zeros(n, dtype=complex)
        prefix[:s] = rng.choice([-1.0,1.0],s)
        families['prefix_sqrt_support'] = prefix
        diffuse = rng.choice([-1.0,1.0],n).astype(complex)/n
        diffuse[0] = 1
        families['spike_diffuse_tail'] = diffuse
        families['flat_signs'] = rng.choice([-1.0,1.0],n).astype(complex)
        for name,x in families.items():
            reference = np.fft.fft(x,norm='ortho')
            for h in sorted({0,1,s//2,s}):
                output, stats = head_energy_fft(x,0.25,h)
                error = float(np.max(np.abs(output-reference)))
                assert error <= stats['requested_threshold']+1e-10*max(1,np.linalg.norm(x))
                numeric.append({'n':n,'family':name,'head':h,
                                'observed_max_error':error,
                                'threshold':stats['requested_threshold'],
                                'head_butterflies':stats['head_fft_butterflies'],
                                'tail_split_volume':stats['tail'].get('split_value_volume',0),
                                'total_butterflies':stats['total_butterflies']})
    report = {'status':'PASS', 'exact_adversary_sizes':len(exact),
              'exact_head_sizes_checked':sum(r['head_sizes_checked'] for r in exact),
              'numeric_cases':len(numeric), 'exact_certificates':exact,
              'numerical_checks':numeric,
              'prior_energy_sha256':hashlib.sha256(Path(__file__).with_name('prior_energy_pruned.py').read_bytes()).hexdigest(),
              'scope':'Exact integer work certificates; floating prototype checks, not a numerical error certificate.'}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ('exact_certificates','numerical_checks')},indent=2))


if __name__ == '__main__':
    main()
