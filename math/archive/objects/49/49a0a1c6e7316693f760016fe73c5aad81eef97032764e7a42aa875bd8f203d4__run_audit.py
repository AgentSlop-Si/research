import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'fft_bidirectional_graph_research'))
from exact_fields import PrimeField,CyclotomicField,fourier,mv
from affine_cycle import ordinary_fft
from green_bridge import FourierPathGreen


class Traced:
    def __init__(self,field):self.field=field;self.calls=Counter()
    def __getattr__(self,name):
        value=getattr(self.field,name)
        if name not in ('add','sub','mul','inv','integer'):return value
        def called(*args):
            self.calls[{'inv':'inverse','integer':'integer_embed'}.get(name,name)]+=1
            return value(*args)
        return called


def main():
    rng=random.Random(105739)
    results={'status':'PASS','exact_conjugacy_checks':0,'exact_inverse_checks':0,
             'cyclotomic_conjugacy_checks':0,'unsupported_modular_pivots':[],
             'large_exact_conjugacy_checks':0,'invalid_length_checks':0,'operation_counts':[]}
    configurations=[(PrimeField(p),n) for p in (65537,786433) for n in (4,8,16,32)]
    configurations += [(CyclotomicField(n),n) for n in (4,8)]
    for field,n in configurations:
        q=field.root(n);traced=Traced(field)
        try:plan=FourierPathGreen(traced,n,q)
        except ValueError as error:
            if isinstance(field,CyclotomicField):raise
            results['unsupported_modular_pivots'].append({'p':field.p,'N':n,'reason':str(error)})
            continue
        assert dict(traced.calls)==dict(plan.c.count)
        matrix=fourier(field,n)
        pairs=[(plan.source_t,plan.target_h),(plan.source_solve,plan.target_solve),
               (lambda x:plan.source_solve(x,'one'),lambda x:plan.target_solve(x,'one')),
               (lambda x:plan.source_solve(x,'half'),lambda x:plan.target_solve(x,'half')),
               (plan.source_s,plan.target_s),(plan.source_s_inverse,plan.target_s_inverse)]
        vectors=[]
        for j in range(n):
            basis=[field.zero]*n;basis[j]=field.one;vectors.append(basis)
        vectors.append([field.integer(rng.randrange(-7,8)) for _ in range(n)])
        for x in vectors:
            fx=mv(field,matrix,x)
            for source,target in pairs:
                assert mv(field,matrix,source(x))==target(fx)
                results['exact_conjugacy_checks']+=1
                results['cyclotomic_conjugacy_checks']+=isinstance(field,CyclotomicField)
            assert plan.source_s_inverse(plan.source_s(x))==x
            assert plan.target_s_inverse(plan.target_s(fx))==fx
            assert plan.source_t(plan.source_solve(x))==x
            assert plan.target_h(plan.target_solve(fx))==fx
            results['exact_inverse_checks']+=4
        assert dict(traced.calls)==dict(plan.c.count)
    field=PrimeField(65537)
    for n in (64,256,1024):
        q=field.root(n);plan=FourierPathGreen(field,n,q)
        x=[field.integer(rng.randrange(field.p)) for _ in range(n)]
        fx,_=ordinary_fft(field,x,q)
        entry={'N':n,'preparation':sum(plan.preparation_operations.values())}
        for label,source,target in [('S',plan.source_s,plan.target_s),
                                    ('S_inverse',plan.source_s_inverse,plan.target_s_inverse)]:
            before=sum(plan.c.count.values());sx=source(x)
            entry['source_'+label]=sum(plan.c.count.values())-before
            before=sum(plan.c.count.values());tfx=target(fx)
            entry['target_'+label]=sum(plan.c.count.values())-before
            fsx,_=ordinary_fft(field,sx,q)
            assert fsx==tfx;results['large_exact_conjugacy_checks']+=1
        results['operation_counts'].append(entry)
    for method in (plan.source_t,plan.target_h,plan.source_solve,plan.target_solve,
                   plan.source_s,plan.target_s,plan.source_s_inverse,plan.target_s_inverse):
        for size in (n-1,n+1):
            try:method([field.zero]*size)
            except ValueError:results['invalid_length_checks']+=1
            else:raise AssertionError('invalid length accepted')
    results['source_sha256']=hashlib.sha256(Path('green_bridge.py').read_bytes()).hexdigest()
    Path('results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
