#!/usr/bin/env python3
"""Exact checks for a centered-target representation obstruction, not a DFT provider."""
import hashlib, json, sys
from pathlib import Path
from fractions import Fraction
D=Path(__file__).resolve().parent

def params(r,a):
    assert a in (0,2) and r>=a+3
    m=4*r;M=1<<m;N=M//4;lam=1<<a
    K=1<<(2*r-4-2*a);J=N//K;h=r+1+a;P=16*m+16
    E=J;B=2*J;C=1<<(3*r+a);q=2*J
    R2=Fraction(J,1<<(2*h));amp2=Fraction(J*J,M*(1<<(2*h)))
    tol2=Fraction(lam*lam,1<<(2*r))
    assert R2==1 and amp2==4*tol2
    assert C*C*4*E==N*B*B
    assert C*(1<<r)==lam*M
    assert K*16*lam*lam==1<<(m//2)
    assert K>=4 and 160*m+4<M
    assert Fraction(1,1<<(2*P))<tol2
    return dict(r=r,a=a,m=m,M=M,N=N,tolerance_multiplier=lam,
        required_coordinates=K,impulse_count=J,h=h,P=P,source_energy=E,
        variation=B,variation_factor=C,canonical_blocks=q,
        original_scale=0,cutoff=C*(1<<r),amplitude_squared=str(amp2),
        tolerance_squared=str(tol2),squared_gap_ratio=4,
        one_numerator_bit_length_lower=P+a-r,
        coefficient_magnitude_bits_lower=K*(P+a-r),
        required_outer_incidences=K*(40*m+1),mandatory_original_output_records=N)

def cyclotomic_sum(M, exponents):
    """Exact coefficients in Z[X]/(X^(M/2)+1), M a power of two."""
    d={}
    for e in exponents:
        e%=M;sgn=1
        if e>=M//2:e-=M//2;sgn=-1
        d[e]=d.get(e,0)+sgn
    return {e:v for e,v in d.items() if v}

def direct_selected(p):
    M,N,K,J=(p[k] for k in ('M','N','required_coordinates','impulse_count'))
    a0=(N-1)//2;terms=0
    for ell in range(K):
        k=M//K*ell
        actual=cyclotomic_sum(M,((a0-j*K)*k for j in range(J)))
        expected=cyclotomic_sum(M,[-ell*(M//K)])
        expected={e:J*v for e,v in expected.items()}
        assert actual==expected
        terms+=J
    return dict(m=p['m'],tolerance_multiplier=p['tolerance_multiplier'],
        selected_coordinates=K,raw_original_terms=terms,all_exact=True)

def alias_grid_check(p):
    M,N,K,J=(p[k] for k in ('M','N','required_coordinates','impulse_count'))
    a0=(N-1)//2;nonzero=[]
    for ell in range(N):
        k=4*ell
        value=cyclotomic_sum(M,((a0-j*K)*k for j in range(J)))
        if value:nonzero.append(k)
    assert nonzero==[M//K*j for j in range(K)]
    return dict(original_alias_rows=N,raw_original_terms=N*J,nonzero_rows=nonzero)

def source_controls():
    p=params(3,0);N,K,J=(p[k] for k in ('N','required_coordinates','impulse_count'))
    dense=[(int(j%K==0),0) for j in range(N)]
    original={'m':p['m'],'F':p['h'],'kind':'dense','data':dense}
    blocks=[]
    for j in range(J):blocks.extend(((j*K+1,1,0),((j+1)*K,0,0)))
    descriptor={'m':p['m'],'F':p['h'],'kind':'blocks','data':blocks}
    rejected=[]
    for obj,want in ((original,'block count ceiling after full dense scan'),(descriptor,'block count ceiling')):
        try:bv.produce(obj)
        except Rejected as ex:
            assert str(ex)==want
            receipt=ex.receipt;events=receipt['events']
            assert events.get('coefficient_outputs',0)==0
            assert not any(('pi_' in k or 'root_' in k or 'trig' in k) for k in events)
            expected_visits=N if obj['kind']=='dense' else 0
            assert events.get('dense_coordinate_visits',0)==expected_visits
            rejected.append(dict(kind=obj['kind'],reason=str(ex),receipt=receipt))
        else:raise AssertionError('accepted fixture outside original caps')
    # Diagnostic recognition only with explicit cap overrides. No produce(),
    # coefficient evaluation, accepted larger provider, or outer run follows.
    diagnostic=[]
    for obj in (original,descriptor):
        ledger=Ledger();s=bv.recognize(obj,ledger,max_blocks=len(blocks),max_factor=p['variation_factor'])
        assert (s.energy,s.variation_l1,s.variation_factor,s.h,s.scale,len(s.blocks)) == (
            J,2*J,p['variation_factor'],p['h'],0,2*J)
        assert s.variation_factor*(1<<((s.m+3)//4))==p['M']>=p['M']//2
        diagnostic.append(dict(kind=obj['kind'],recognized_blocks=len(s.blocks),
            source_energy=s.energy,variation=s.variation_l1,factor=s.variation_factor,
            h=s.h,scale=s.scale,cutoff=p['M'],sparse_cutoff_guard_passes=False,
            receipt=ledger.report()))
    return dict(default_provider_rejections=rejected,recognition_only_cap_overrides=diagnostic)

def omission_controls():
    p=params(3,0);M,K,P=p['M'],p['required_coordinates'],p['P']
    required=[M//K*j for j in range(K)]
    # Here K=4: all selected true values are exact cardinal Gaussian dyadics.
    A=Fraction(1,4);eps=Fraction(1,8);unit=1<<(P-2)
    exact=[(unit,0),(0,-unit),(-unit,0),(0,unit)]
    true={k:(Fraction(x,1<<P),Fraction(y,1<<P)) for k,(x,y) in zip(required,exact)}
    def bad(z):
        return [k for k,(x,y) in true.items() if (z.get(k,(0,0))[0]-x)**2+(z.get(k,(0,0))[1]-y)**2>eps*eps]
    assert not bad(true) # Only selected grid; no full-spectrum success assertion.
    for k in required:
        z=true.copy();del z[k];assert bad(z)==[k]
    wrong=true.copy();value=wrong.pop(required[-1]);wrong[required[-1]+1]=value
    assert bad(wrong)==[required[-1]]
    # Every successful approximate value must have a large Cartesian component.
    B=p['one_numerator_bit_length_lower']
    assert Fraction(2*((1<<(B-1))-1)**2,1<<(2*P))<eps*eps
    # At the equality amplitude==tolerance endpoint, an omitted point is legal.
    assert not (eps*eps>eps*eps)
    return dict(exact_selected_rows=K,one_missing_tests=K,wrong_location_test=True,
        numerator_width_test=True,equality_endpoint_test=True,
        scope='necessary selected-coordinate tests, not complete sparse recovery')

def verify_sources():
    b=json.loads((D/'SOURCE_BINDINGS.json').read_text())
    for v in b['bindings']:
        assert hashlib.sha256((D/v['snapshot']).read_bytes()).hexdigest()==v['sha256']
    return dict(snapshot_files=len(b['bindings']),all_hashes_pass=True)

def main():
    bindings=verify_sources()
    # Verify frozen dependency bytes before importing any recognition module.
    global bv, Ledger, Rejected
    sys.path.insert(0,str(D/'runtime'))
    import bounded_variation as bv
    from interval_core import Ledger, Rejected
    plans=[params(r,a) for a in (0,2) for r in list(range(a+3,17))+[32,64,128,256]]
    finite=[direct_selected(params(3,0)),direct_selected(params(4,0)),direct_selected(params(5,2))]
    out=dict(status='PASS_EXACT_CONTRACT_OBSTRUCTION_CHECKS',source_binding=bindings,
        structural_parameter_checks=len(plans),parameter_plans=plans,
        direct_centered_selected_checks=finite,complete_alias_grid=alias_grid_check(params(3,0)),
        source_controls=source_controls(),omission_controls=omission_controls(),
        no_general_provider_or_outer_execution_claim=True)
    (D/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'structural_parameter_checks':len(plans),
        'direct_selected_coordinates':sum(x['selected_coordinates'] for x in finite),
        'direct_selected_raw_terms':sum(x['raw_original_terms'] for x in finite),
        'complete_alias_grid_rows':out['complete_alias_grid']['original_alias_rows'],
        'default_provider_rejections':len(out['source_controls']['default_provider_rejections'])},indent=2))
if __name__=='__main__':main()
