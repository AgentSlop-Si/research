"""Exact full-register, scalar-gate, and closed-cycle residual checks."""
import json
import random
from pathlib import Path
from feedback import prepare_feedback,feedback_word,gain_update_word,rank_one_add
from prior_affine_reuse import prepare,execute,execute_scalar,expand_scalar,inverse,apply_t,apply_j,charge


def increment(plan,fb,injections,initial):
    n,p,R=plan['n'],plan['p'],fb['batches']
    forcing=[[0]*n for _ in range(R)]
    for vertex,source in injections:
        value=apply_t(plan,initial[source*n:(source+1)*n])
        forcing[vertex]=[(a+b)%p for a,b in zip(forcing[vertex],value)]
    chain=[forcing[0][:]]
    for r in range(1,R):
        chain.append([(a+b)%p for a,b in zip(forcing[r],apply_j(plan,chain[-1]))])
    scalar=chain[-1][fb['observed']]*pow(fb['kappa'],-1,p)%p
    correction=[scalar*u%p for u in fb['u']]
    out=[]
    for r in range(R):
        out.append([(a+b)%p for a,b in zip(chain[r],correction)])
        correction=apply_j(plan,correction)
    assert out[0]==[(a+u*out[-1][fb['observed']])%p for a,u in zip(forcing[0],fb['u'])]
    for r in range(1,R):
        assert out[r]==[(a+b)%p for a,b in zip(forcing[r],apply_j(plan,out[r-1]))]
    return out


def main():
    rows=[]
    rng=random.Random(731009)
    basis_count=random_count=0
    # Focused independent-review cases: reject invalid register sources before
    # Python's negative indexing can alias them to a target bank.
    edge_plan=prepare(4,65537)
    zero_feedback=prepare_feedback(edge_plan,3,[0]*4,0)
    invalid_injections=([],[(-1,0)],[(3,0)],[(0,-1)])
    for injections in invalid_injections:
        for compiler in (
                lambda: feedback_word(edge_plan,zero_feedback,injections),
                lambda: gain_update_word(edge_plan,zero_feedback,injections,0,1)):
            try:
                compiler()
            except ValueError:
                pass
            else:
                raise AssertionError('invalid injection accepted')
    focused_valid_cases=0
    # Coordinate zero, zero closing edge, repeated source bank, non-root
    # injections, equal gains, and arbitrary preexisting target/workspace state.
    injections=[(0,0),(2,0),(1,1)]
    word,cost=feedback_word(edge_plan,zero_feedback,injections)
    size=cost['target_base']+12
    initial=[(17*i+3)%65537 for i in range(size)]
    initial[0]=0
    expected=initial[:]
    inc=increment(edge_plan,zero_feedback,injections,initial)
    for r in range(3):
        for i in range(4):
            index=cost['target_base']+4*r+i
            expected[index]=(expected[index]+inc[r][i])%65537
    assert execute_scalar(expand_scalar(word,65537),initial,65537)==expected
    zero_update,_=gain_update_word(edge_plan,zero_feedback,injections,0,5)
    assert zero_update==[]
    focused_valid_cases+=1
    nonzero_feedback=prepare_feedback(edge_plan,3,[2,4,6,8],0)
    update,_=gain_update_word(edge_plan,nonzero_feedback,injections,0,1)
    new_expected=initial[:]
    new_inc=increment(edge_plan,nonzero_feedback,injections,initial)
    for r in range(3):
        for i in range(4):
            index=cost['target_base']+4*r+i
            new_expected[index]=(new_expected[index]+new_inc[r][i])%65537
    assert execute_scalar(expand_scalar(update,65537),expected,65537)==new_expected
    equal_update,_=gain_update_word(edge_plan,nonzero_feedback,injections,1,1)
    assert equal_update==[]
    focused_valid_cases+=1
    # A zero-valued source pivot is legal: only its nonzero coefficient is inverted.
    pivot_word,pivot_cost=rank_one_add(65537,{0:3,1:5},3,[2,0])
    pivot_initial=[0,7,99,11,13]
    pivot_expected=[0,7,99,81,13]
    assert execute_scalar(expand_scalar(pivot_word,65537),pivot_initial,65537)==pivot_expected
    assert len(expand_scalar(pivot_word,65537))==pivot_cost['scalar_instructions']
    assert execute(inverse(pivot_word,65537),pivot_expected,65537)==pivot_initial
    assert rank_one_add(65537,{0:0},3,[2,0])[0]==[]
    assert rank_one_add(65537,{0:3},3,[0,0])[0]==[]
    focused_valid_cases+=3
    # Both endpoints of a gain correction must remain nonsingular.
    singular_gain_feedback=prepare_feedback(edge_plan,1,[2,0,0,0],0)
    singular_gain=pow(2,-1,65537)
    for old,new in ((singular_gain,0),(0,singular_gain)):
        try:
            gain_update_word(edge_plan,singular_gain_feedback,[(0,0)],old,new)
        except ValueError as error:
            assert 'singular' in str(error)
        else:
            raise AssertionError('singular gain endpoint accepted')
    for p in (65537,998244353):
        for n in (2,4,8):
            plan=prepare(n,p)
            for R in (1,2,4):
                observed=n-1
                for factor in (2,3,5,7):
                    u=[factor*(i+1)%p for i in range(n)]
                    try:
                        fb=prepare_feedback(plan,R,u,observed)
                        break
                    except ValueError:
                        continue
                else:
                    raise AssertionError('test did not find nonsingular feedback')
                assert fb['coefficient_preparation']=={
                    'mul':(R-1)*(3*n-1)+2*n,
                    'add':(R-1)*(2*n-1)+n-1,
                    'sub':1,'constant_inverse':1}
                modes=[('one_root',[(0,0)]),('independent_roots',[(r,r) for r in range(R)])]
                for mode,injections in modes:
                    word,cost=feedback_word(plan,fb,injections)
                    scalar=expand_scalar(word,p)
                    backwards=inverse(word,p)
                    beta=(1-fb['kappa'])%p
                    new_gain=next(g for g in (2,3,5,7) if (1-g*beta)%p)
                    new_fb=prepare_feedback(plan,R,[new_gain*value%p for value in u],observed)
                    update,update_cost=gain_update_word(plan,fb,injections,1,new_gain)
                    update_scalar=expand_scalar(update,p)
                    assert len(update_scalar)==update_cost['rank_one_correction']['scalar_instructions']
                    assert update_cost['coefficient_preparation']=={
                        'mul':(3*R-2)*n+4,'sub':4,'constant_inverse':1,
                        **({'add':(R-1)*n} if R>1 else {})}
                    assert len(scalar)==cost['scalar_instructions']==charge(word)['expanded_scalar_instructions']
                    size=cost['target_base']+R*n
                    for coordinate in range(size):
                        initial=[int(i==coordinate) for i in range(size)]
                        inc=increment(plan,fb,injections,initial)
                        expected=initial[:]
                        for r in range(R):
                            for i in range(n):
                                k=cost['target_base']+r*n+i
                                expected[k]=(expected[k]+inc[r][i])%p
                        got=execute(word,initial,p)
                        assert got==expected
                        assert execute_scalar(scalar,initial,p)==expected
                        assert execute(backwards,got,p)==initial
                        assert got[:cost['target_base']]==initial[:cost['target_base']]
                        new_inc=increment(plan,new_fb,injections,initial)
                        new_expected=initial[:]
                        for r in range(R):
                            for i in range(n):
                                k=cost['target_base']+r*n+i
                                new_expected[k]=(new_expected[k]+new_inc[r][i])%p
                        assert execute(update,got,p)==new_expected
                        assert execute_scalar(update_scalar,got,p)==new_expected
                        basis_count+=1
                    for _ in range(4):
                        initial=[rng.randrange(p) for _ in range(size)]
                        inc=increment(plan,fb,injections,initial)
                        expected=initial[:]
                        for r in range(R):
                            for i in range(n):
                                k=cost['target_base']+r*n+i
                                expected[k]=(expected[k]+inc[r][i])%p
                        assert execute_scalar(scalar,initial,p)==expected
                        new_inc=increment(plan,new_fb,injections,initial)
                        new_expected=initial[:]
                        for r in range(R):
                            for i in range(n):
                                k=cost['target_base']+r*n+i
                                new_expected[k]=(new_expected[k]+new_inc[r][i])%p
                        assert execute_scalar(update_scalar,expected,p)==new_expected
                        random_count+=1
                    rows.append({'p':p,'n':n,'R':R,'mode':mode,'kappa':fb['kappa'],
                                 'coefficient_preparation':fb['coefficient_preparation'],
                                 'cost':cost,'gain_update':update_cost,'basis_vectors':size})
                pivot=next(i for i,a in enumerate(fb['a']) if a)
                singular=[0]*n
                singular[pivot]=pow(fb['a'][pivot],-1,p)
                try:
                    prepare_feedback(plan,R,singular,observed)
                except ValueError as error:
                    assert 'singular feedback' in str(error)
                else:
                    raise AssertionError('singular feedback accepted')
    examples=[]
    for n,R in ((32,4),(64,4),(128,8)):
        plan=prepare(n)
        fb=prepare_feedback(plan,R,[2*(i+1) for i in range(n)],n-1)
        for mode,injections in [('one_root',[(0,0)]),('independent_roots',[(r,r) for r in range(R)])]:
            word,cost=feedback_word(plan,fb,injections)
            assert charge(word)['expanded_scalar_instructions']==cost['scalar_instructions']
            update,update_cost=gain_update_word(plan,fb,injections,1,2)
            assert charge(update)['expanded_scalar_instructions']==update_cost['rank_one_correction']['scalar_instructions']
            examples.append({'n':n,'R':R,'mode':mode,'cost':cost,
                             'gain_update':update_cost,
                             'coefficient_preparation':fb['coefficient_preparation']})
    report={'status':'PASS','cases':len(rows),'full_state_basis_vectors':basis_count,
            'gain_update_full_state_basis_vectors':basis_count,
            'random_full_states':random_count,'singular_feedback_rejections':18,
            'focused_invalid_injection_rejections':8,
            'focused_singular_gain_rejections':2,
            'focused_valid_edge_cases':focused_valid_cases,
            'scope':'Exact rank-one cyclic feedback; every first transform and preparation is charged; no fresh FFT speed claim.',
            'examples':examples,'cases_detail':rows}
    Path(__file__).with_name('results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases_detail','examples')},indent=2))


if __name__=='__main__':
    main()
