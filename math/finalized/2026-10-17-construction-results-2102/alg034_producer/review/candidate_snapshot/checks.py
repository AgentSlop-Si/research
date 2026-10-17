"""Fresh deterministic producer controls; imports only this fresh backend."""
import ast
import copy
from hashlib import sha256
import json
from pathlib import Path
import random
import resource
import time
import structured_producer as P


def must_reject(fn, prefix):
    try:
        fn()
    except P.Failure as exc:
        assert str(exc).startswith(prefix), (prefix,str(exc))
        return str(exc)
    raise AssertionError('unexpected acceptance: '+prefix)


def independent_fourier(raw):
    """Full small N direct transform, using exact quadrant characters only.

    This oracle enumerates all N positions and all N frequencies. It does not
    reuse producer roots, period construction, policy or output arithmetic.
    """
    n=raw['N']
    assert n<=256
    data={row[0]:(row[1],row[2]) for row in raw['entries']}
    output=[]
    for k in range(n):
        real=imag=0
        for j in range(n):
            a,b=data.get(j,(0,0))
            if not a and not b: continue
            angle=(k*j)%n
            assert (4*angle)%n==0
            if angle==0: ar,ai=a,b
            elif angle==n//4: ar,ai=b,-a
            elif angle==n//2: ar,ai=-a,-b
            else:
                assert angle==3*n//4
                ar,ai=-b,a
            real+=ar; imag+=ai
        output.append((real,imag))
    return output


def main():
    started=time.perf_counter()
    source=Path(P.__file__).read_bytes()
    tree=ast.parse(source)
    imports=[]
    for item in ast.walk(tree):
        if isinstance(item,ast.Import): imports.extend(x.name for x in item.names)
        if isinstance(item,ast.ImportFrom): imports.append(item.module)
    assert sorted(imports)==['dataclasses','hashlib','json']
    for item in ast.walk(tree):
        if isinstance(item,ast.Call) and isinstance(item.func,ast.Name):
            assert item.func.id not in {'eval','exec','compile','open','__import__'}
    rng=random.Random(34028)
    exact_cases=0
    for m in (2,4,6,8):
        n=1<<m
        for repeat in range(16):
            entries=[]
            for axis in range(4):
                a,b=rng.randrange(-100,101),rng.randrange(-100,101)
                if axis==0: a=2*(a//2)+1
                if a or b: entries.append([axis*n//4,a,b])
            raw={'schema':P.SCHEMA,'N':n,'F':rng.randrange(-6,7),'entries':entries}
            state={'N':n,'B':n,'a':2*rng.randrange(n//2)+1,'beta':rng.randrange(n)}
            result=P.execute(raw,state,t=repeat,q=m+repeat)
            oracle=independent_fourier(raw)
            assert oracle==[result.period[k%4] for k in range(n)]
            assert result.value_exponent==-raw['F']-m//2
            assert result.kappa+result.pgrid_shift==result.value_exponent
            plan=result.policy['plan']
            assert (1<<plan['c'])==64*n**3*(1<<n)
            assert result.policy['p']>=max(result.policy['W'],plan['c']+repeat+1,
                                         plan['c']+m+repeat+plan['G']+2)
            # Explicit small-domain materialization independently checks the
            # formal p-grid and ordinary exact output dyadic are equal.
            for row in result.period:
                for value in row:
                    numerator=value<<result.pgrid_shift
                    assert abs(numerator).bit_length()<=result.policy['p']+plan['I']
            verification=P.verify(raw,state,repeat,m+repeat,result.packet())
            assert verification['exact_target_certified']
            exact_cases+=1
    # The theorem-scale instance is computed and replayed, not materialized.
    raw,state=P.fixture()
    before=time.perf_counter()
    result=P.execute(raw,state)
    scale_elapsed=time.perf_counter()-before
    verification=P.verify(raw,state,16,464,result.packet())
    assert result.N==268435456
    assert result.period==((1,0),)*4 and result.value_exponent==-14
    assert result.policy['p']==268436013
    assert result.policy['plan']['c']==268435546
    assert result.policy['plan']['accepted_serial_radius_factor']=={'coefficient':1,'scale':-466}
    assert result.pgrid_shift==268435998 and result.kappa==-268436012
    assert result.ledger['max_metered_data_integer_bits']==30
    # p is a large value, but has only 29 bits; no p-bit integer is formed.
    assert result.policy['p'].bit_length()==29
    # Support family, larger metadata and large precision input remain compact.
    n=1<<64
    big={'schema':P.SCHEMA,'N':n,'F':-(1<<100),
         'entries':[[0,(1<<1023)+1,-(1<<1022)],[n//4,-3,5]]}
    bigstate={'N':n,'B':n,'a':n-1,'beta':n-1}
    bigrun=P.execute(big,bigstate,p=1<<120)
    assert bigrun.ledger['max_metered_data_integer_bits']<=1026
    assert bigrun.policy['p']==1<<120
    assert bigrun.kappa+bigrun.pgrid_shift==bigrun.value_exponent
    zero={'schema':P.SCHEMA,'N':raw['N'],'F':0,'entries':[]}
    zr=P.execute(zero,state)
    assert zr.status=='EXACT_INPUT_ZERO' and zr.packet()['payload'] is None
    assert P.verify(zero,state,16,464,zr.packet())['exact_target_certified'] is False
    rejections={}
    def bad_raw(name,mutate,prefix):
        x=copy.deepcopy(raw); mutate(x)
        rejections[name]=must_reject(lambda:P.execute(x,state),prefix)
    bad_raw('bool_coefficient',lambda x:x['entries'][0].__setitem__(1,True),'GRAMMAR:')
    bad_raw('float_exponent',lambda x:x.__setitem__('F',0.0),'GRAMMAR:')
    bad_raw('duplicate_support',lambda x:x['entries'].append([0,1,0]),'GRAMMAR:')
    bad_raw('zero_sparse_entry',lambda x:x['entries'].__setitem__(0,[0,0,0]),'GRAMMAR:')
    bad_raw('noncanonical_common_factor',lambda x:x['entries'].__setitem__(0,[0,2,0]),'GRAMMAR:')
    bad_raw('unsupported_index',lambda x:x['entries'][0].__setitem__(0,1),'UNSUPPORTED_STRUCTURE:')
    bad_raw('overwidth_coefficient',lambda x:x['entries'][0].__setitem__(1,1<<1024),'RESOURCE_LIMIT:')
    bad_raw('extra_raw_key',lambda x:x.__setitem__('proof',True),'GRAMMAR:')
    wrong=dict(state); wrong['B']-=1
    rejections['nonsingleton']=must_reject(lambda:P.execute(raw,wrong),'UNSUPPORTED_STRUCTURE:')
    wrong=dict(state); wrong['a']=2
    rejections['noninvertible_phase']=must_reject(lambda:P.execute(raw,wrong),'DOMAIN:')
    rejections['low_precision']=must_reject(lambda:P.execute(raw,state,p=result.policy['p']-1),'PRECISION:')
    rejections['negative_t']=must_reject(lambda:P.execute(raw,state,t=-1),'DOMAIN:')
    rejections['low_q']=must_reject(lambda:P.execute(raw,state,q=27),'DOMAIN:')
    rejections['bool_q']=must_reject(lambda:P.execute(raw,state,q=True),'GRAMMAR:')
    rejections['zero_with_precision']=must_reject(lambda:P.execute(zero,state,p=100),'DOMAIN:')
    oddn=1<<27
    oddraw={'schema':P.SCHEMA,'N':oddn,'F':0,'entries':[[0,1,0]]}
    oddstate={'N':oddn,'B':oddn,'a':1,'beta':0}
    rejections['nonsquare']=must_reject(lambda:P.execute(oddraw,oddstate),'UNSUPPORTED_STRUCTURE:')
    hugen=1<<66
    hugeraw={'schema':P.SCHEMA,'N':hugen,'F':0,'entries':[[0,1,0]]}
    hugestate={'N':hugen,'B':hugen,'a':1,'beta':0}
    rejections['m_cap']=must_reject(lambda:P.execute(hugeraw,hugestate),'RESOURCE_LIMIT:')
    for field in ('period','value_exponent','formal_p_grid'):
        forged=result.packet()
        if field=='period': forged['payload'][field][0][0]+=1
        elif field=='value_exponent': forged['payload'][field]+=1
        else: forged['payload'][field]['kappa']+=1
        rejections['forged_'+field]=must_reject(lambda:P.verify(raw,state,16,464,forged),'SEMANTIC_MISMATCH:')
    forged=result.packet()
    forged['context']['raw']['entries'][0][1]=3
    forged['policy']['raw_input_sha256']='0'*64
    rejections['rehashed_input_substitution']=must_reject(lambda:P.verify(raw,state,16,464,forged),'SEMANTIC_MISMATCH:')
    # A fully self-consistent alternative packet still fails against ORIGINAL
    # supplied context, even though its own digest and policy were recalculated.
    other=copy.deepcopy(raw); other['entries'][0][1]=3
    forged=P.execute(other,state).packet()
    rejections['fully_recomputed_substitution']=must_reject(lambda:P.verify(raw,state,16,464,forged),'SEMANTIC_MISMATCH:')
    forged=result.packet(); forged['historical_execution_attested']=True
    rejections['extra_attestation']=must_reject(lambda:P.verify(raw,state,16,464,forged),'GRAMMAR:')
    forged=result.packet(); forged['payload']['period']=[[0,0]]*129
    rejections['oversized_packet_list']=must_reject(lambda:P.verify(raw,state,16,464,forged),'RESOURCE_LIMIT:')
    # Copies and decoded views cannot mutate immutable execution context.
    original_bytes=result.context_bytes
    raw['entries'][0][1]=9
    exposed=result.context; exposed['raw']['entries'][0][1]=11
    assert result.context_bytes==original_bytes and result.period==((1,0),)*4
    raw,state=P.fixture()
    summary={
        'status':'PASS','source_sha256':sha256(source).hexdigest(),
        'source_static_imports':imports,'small_direct_transform_cases':exact_cases,
        'rejections':rejections,'theorem_scale':result.packet(),
        'theorem_scale_ledger':result.ledger,'theorem_scale_verification':verification,
        'large_metadata_max_metered_data_bits':bigrun.ledger['max_metered_data_integer_bits'],
        'elapsed_seconds':time.perf_counter()-started,'theorem_scale_execute_seconds':scale_elapsed,
        'process_maxrss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'measurement_scope':'whole fresh checks process including Python, tests and small oracle; not a hardware guarantee',
    }
    here=Path(__file__).resolve().parent
    (here/'CHECK_RESULTS.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    (here/'EXAMPLE.json').write_text(json.dumps(result.packet(),sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('theorem_scale','rejections')},sort_keys=True))


if __name__=='__main__': main()
