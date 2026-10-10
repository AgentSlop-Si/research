"""Independent exact finite-field matrix audit and lazy fallback invariants."""
import json,random
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from deferred_dif import DeferredDIF,transform_deferred_conjugate
from rational_forcing import direct_dft_any

entries=0;cases=0;certified=0;fallback=0
for p,g in ((2013265921,31),(998244353,3)):
    for n in (32,64,128,256):
        e=RecurrenceGreen(n,p,g)
        for j in range(n):
            x=[0]*n;x[j]=1
            out,meta=transform_deferred_conjugate(e,x)
            omega=e.powers[j]
            cur=1
            for k in range(n):
                assert out[k]==cur,(p,n,j,k)
                cur=cur*omega%p
            if meta['selected']=='deferred-conjugate-fallback':
                assert meta['final_fft']['arithmetic']==3*n//2*(n.bit_length()-1)
                assert not meta['residual_computed']
                fallback+=1
            else:
                assert meta['selected']=='deferred-conjugate-certified'
                assert meta['residual_computed']
                certified+=1
            entries+=n;cases+=1
        rng=random.Random(p+n)
        for _ in range(8):
            x=[rng.randrange(p) for _ in range(n)]
            out,meta=transform_deferred_conjugate(e,x)
            assert out==direct_dft_any(x,e.omega,p),(p,n,'generic')
            entries+=n;cases+=1
            if meta['selected']=='deferred-conjugate-fallback':
                fallback+=1
                assert not meta['residual_computed']
                assert meta['final_fft']['arithmetic']==3*n//2*(n.bit_length()-1)
            else:certified+=1
        for _ in range(8):
            d,z=rng.sample(range(1,n),2)
            h=[0]*n;h[4]=7;h[n-9]=11
            r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),z,29,p)
            x=e.P.solve(r)
            out,meta=transform_deferred_conjugate(e,x)
            assert out==direct_dft_any(x,e.omega,p),(p,n,d,z)
            entries+=n;cases+=1
            if meta['selected']=='deferred-conjugate-certified':certified+=1
            else:fallback+=1
result=dict(exact_output_checks=entries,instances=cases,certified=certified,
            safe_fallbacks=fallback,primes=[2013265921,998244353],
            lengths=[32,64,128,256],
            theorem='all-input exact, no recomputed radix2 butterflies on fallback')
with open('PHASE24_AUDIT.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
