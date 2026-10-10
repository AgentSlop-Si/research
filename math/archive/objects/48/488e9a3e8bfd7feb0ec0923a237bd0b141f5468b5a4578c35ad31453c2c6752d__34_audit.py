"""Independent deterministic audit for Phase 28 algebraic Green certificates."""
import json
from pathlib import Path
from phase28_synthesis import (
    P,green_triple_trace_certificate,green_triple_fourier_test,
    green_sum,green_components,matmul,invert,fft_matrix,
    trace2_from_row_moments,inverse)
from phase28_polynomial import (trace_poly,eval_poly,product_affines)

def main():
    rows=[]
    for n in (4,8,16,32,64,128):
        seed=2800+n
        cert=green_triple_trace_certificate(n,seed)
        out=green_triple_fourier_test(n,seed)
        cert['full_signature_status']=out.status
        if n in (4,8):
            A=green_sum(n,seed*3+1)
            B0,B1=green_components(n,seed*3+2)
            C=green_sum(n,seed*3+3)
            T=matmul(matmul(invert(A),fft_matrix(n)),invert(C))
            poly=trace_poly(trace2_from_row_moments(T),B0,B1)
            z=3*inverse(2)%P
            cert['scalar_coupling_degree']=len(poly)-1
            cert['scalar_coupling_specialization']=eval_poly(poly,z)
            cert['expected_specialization']=eval_poly(product_affines(B0,B1),z)*(-cert['nonzero_difference'])%P
            assert cert['scalar_coupling_specialization']==cert['expected_specialization']
        assert out.status=='excluded' and cert['nonzero_difference']!=0
        rows.append(cert)
    data={'phase':28,'date':'2026-10-10','field_prime':P,
          'note':'Mod p values are reductions of exactly specified cyclotomic-rational matrices. Nonzero polynomial numerator with good denominators also certifies the corresponding characteristic-0 algebraic expressions are nonzero.',
          'certificates':rows}
    dest=Path(__file__).with_name('audit.json')
    dest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
