"""Independent exact checks for the shared-scan theory. Run: python verify.py.
Dense inversion and direct DFT below are test oracles, not fast algorithms.
"""
from __future__ import annotations
from itertools import combinations, permutations
from math import comb,gcd
from pathlib import Path
import json, random
from shared_scan import (ScanPlan,Counts,root_of_order,direct_dft,projective_key,
                        fourier_two_plan,block_tour_plan,weyl_check,
                        histogram_checks,minimum_equal_degree,capacity,to_prefix,fourier_four_plan)

FIELDS=[(65537,3),(998244353,3)]

def inverse(A,p):
    n=len(A);a=[[v%p for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:raise ValueError('singular')
        a[j],a[k]=a[k],a[j];s=pow(a[j][j],p-2,p)
        a[j]=[v*s%p for v in a[j]]
        for k in range(n):
            if k!=j:
                s=a[k][j]
                a[k]=[(v-s*w)%p for v,w in zip(a[k],a[j])]
    return [row[n:] for row in a]

def matvec(A,x,p):return [sum(a*b for a,b in zip(row,x))%p for row in A]
def matmul(A,B,p):return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def rank(A,p):
    a=[row[:] for row in A];r=0
    for c in range(len(a[0]) if a else 0):
        k=next((k for k in range(r,len(a)) if a[k][c]%p),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];inv=pow(a[r][c]%p,p-2,p)
        a[r]=[v*inv%p for v in a[r]]
        for k in range(r+1,len(a)):
            q=a[k][c]%p;a[k]=[(v-q*w)%p for v,w in zip(a[k],a[r])]
        r+=1
    return r

def dense_sparse(rows,cols,p):
    a=[[0]*cols for _ in rows]
    for i,row in enumerate(rows):
        for j,c in row:a[i][j]=(a[i][j]+c)%p
    return a

def dense_plan(plan):
    n=plan.m;p=plan.p
    Q=[[int(i==j) for j in range(n)] for i in range(n)]
    for i,a in enumerate(plan.a):Q[i][(i-1)%n]=(Q[i][(i-1)%n]-a)%p
    G=inverse(Q,p)
    return matmul(matmul(dense_sparse(plan.R,n,p),G,p),dense_sparse(plan.C,plan.n,p),p)

def random_plan(rng,n,m,r,s,p,zeros):
    while True:
        weights=[rng.randrange(1,p) for _ in range(m)]
        if zeros:
            for i in rng.sample(range(m),max(1,m//4)):weights[i]=0
        C=[[] for _ in range(m)]
        for j in range(n):
            for i in rng.sample(range(m),rng.randrange(s+1)):
                C[i].append((j,rng.randrange(1,p)))
        R=[[(i,rng.randrange(1,p)) for i in rng.sample(range(m),rng.randrange(r+1))] for _ in range(n)]
        try:return ScanPlan(n,p,weights,C,R)
        except ValueError:continue

def run():
    rng=random.Random(20261010)
    result={'status':'No new sub-N-log-N Fourier factorization constructed.',
            'fields':[p for p,_ in FIELDS], 'tests':{}}
    g={'plans':0,'vectors':0,'transpose_vectors':0,'green_basis_vectors':0,'exact_output_entries':0}
    direction={'restrictions':0,'including_zero_forcing':0,'with_zero_rows':0}
    normal={'plans':0,'vectors':0,'nonzero_cycle':0,'broken_cycle':0}
    false={'random_false_fourier':0,'seed_correct_but_phase_wrong':0}
    for p,_ in FIELDS:
        for n in (2,4,8):
            for m in (n,2*n,3*n):
                for zeros in (False,True):
                    plan=random_plan(rng,n,m,min(n,3),min(n,3),p,zeros)
                    A=dense_plan(plan);transpose=plan.transpose_plan();pref=to_prefix(plan)
                    Q=[[int(i==j) for j in range(m)] for i in range(m)]
                    for i,a in enumerate(plan.a):Q[i][(i-1)%m]=(Q[i][(i-1)%m]-a)%p
                    G=inverse(Q,p)
                    for j in range(m):
                        e=[0]*m;e[j]=1
                        assert plan.green(e)==[row[j] for row in G]
                        g['green_basis_vectors']+=1
                    assert pref.input_degrees==plan.input_degrees
                    if zeros:
                        assert all(a<=2*b for a,b in zip(pref.output_degrees,plan.output_degrees));normal['broken_cycle']+=1
                    else:
                        assert all(a<=b+1 for a,b in zip(pref.output_degrees,plan.output_degrees));normal['nonzero_cycle']+=1
                    g['plans']+=1;normal['plans']+=1
                    for _ in range(5):
                        x=[rng.randrange(p) for _ in range(n)]
                        y,c=plan.apply(x);assert y==matvec(A,x,p)
                        assert c.total==4*m+2*(plan.nnz_C+plan.nnz_R)+1
                        assert transpose.apply(x)[0]==matvec(list(zip(*A)),x,p)
                        assert pref.apply(x)[0]==y
                        g['vectors']+=1;g['transpose_vectors']+=1;g['exact_output_entries']+=n;normal['vectors']+=1
                    # Independent inverse computed above validates all applied Green columns.
                    for k in range(1,min(n,4)+1):
                        for cols in list(combinations(range(n),k))[:12]:
                            V=plan.internal_columns(cols)
                            f=sum(any(j in cols for j,c in row) for row in plan.C)
                            keys=[projective_key(v,p) for v in V]
                            D={v for v in keys if v is not None}
                            assert len(D)<=f
                            direction['restrictions']+=1
                            direction['including_zero_forcing']+=int(f==0)
                            direction['with_zero_rows']+=int(None in keys)
                    w=root_of_order(n,p,3)
                    assert not weyl_check(plan,w)['exact_fourier'];false['random_false_fourier']+=1
    result['tests']['scan_and_transpose']=g
    result['tests']['projective_directions']=direction
    result['tests']['prefix_normal_form']=normal
    result['tests']['phase_negative_controls']=false

    # Constructive dyadic Fourier controls. All endpoint weights are generated
    # explicitly from powers of the supplied root, not fitted to a target matrix.
    controls={'plans':0,'basis_vectors':0,'dense_vectors':0,'output_entries':0,'histogram_checks':0,'records':[]}
    for p,gen in FIELDS:
        small=fourier_two_plan(p)
        assert weyl_check(small,p-1)['exact_fourier']
        f4=fourier_four_plan(p,root_of_order(4,p,gen))
        assert max(f4.output_degrees)==2 and max(f4.input_degrees)==2
        assert weyl_check(f4,root_of_order(4,p,gen))['exact_fourier']
        wrongC=[[(j,c*(2 if j==1 else 1)%p) for j,c in row] for row in f4.C]
        wrong=ScanPlan(4,p,f4.a,wrongC,f4.R)
        check=weyl_check(wrong,root_of_order(4,p,gen))
        assert check['seed_ok'] and check['phase_failures']>0
        assert all(c['passes'] for c in histogram_checks(wrong))
        false['seed_correct_but_phase_wrong']+=1
        for n in (4,8,16,32,64,128,256):
            B=4 if n<=16 else 1<<((n.bit_length()-1)//2)
            w=root_of_order(n,p,gen);plan=block_tour_plan(n,B,p,w)
            assert plan.nnz_C==(n//B)*(2*B*B+1)//3
            assert plan.nnz_R==n*(n//B)
            assert capacity(max(plan.output_degrees),max(plan.input_degrees))>=n
            checks=histogram_checks(plan)
            assert all(c['passes'] for c in checks)
            controls['histogram_checks']+=len(checks)
            if n<=64:
                for j in range(n):
                    x=[0]*n;x[j]=1;y,c=plan.apply(x)
                    assert y==direct_dft(x,w,p)
                    controls['basis_vectors']+=1;controls['output_entries']+=n
                assert weyl_check(plan,w)['exact_fourier']
            for _ in range(3):
                x=[rng.randrange(p) for _ in range(n)]
                y,c=plan.apply(x);assert y==direct_dft(x,w,p)
                controls['dense_vectors']+=1;controls['output_entries']+=n
            controls['plans']+=1
            controls['records'].append(dict(p=p,n=n,B=B,M=plan.m,r=max(plan.output_degrees),s=max(plan.input_degrees),
                                            E_in=plan.nnz_C,E_out=plan.nnz_R,apply_field_ops=plan.expected_apply_ops,
                                            cycle_setup_ops=plan.setup.total,
                                            endpoint_setup_status='Explicit construction; not included in cycle_setup_ops. O(N^(3/2)) balanced.'))
    result['tests']['fourier_controls']=controls

    # The actual capacity proof uses ONLY consecutive-column full spark,
    # valid for composite lengths too. Check wrapping columns independently.
    vand={'minors':0,'lengths':[]}
    for p,generator in FIELDS:
        for n in (2,3,4,5,6,7,8,12,16,17):
            if (p-1)%n:continue
            w=root_of_order(n,p,generator);vand['lengths'].append([p,n])
            for k in range(1,min(n,5)+1):
                for start in (0,n-1):
                    for rr in list(combinations(range(n),k))[:24]:
                        A=[[pow(w,r*((start+j)%n),p) for j in range(k)] for r in rr]
                        assert rank(A,p)==k;vand['minors']+=1
    result['tests']['consecutive_vandermonde']=vand

    # Exhaustive finite support check for the abstract union-of-spans count.
    # Each r-dimensional proper subspace in k=r+1 dimensions contains at
    # most r points on the finite Fourier moment curve.
    unions={'subspaces':0,'target_membership_tests':0}
    p=17;n=8;w=2
    for r in (1,2,3):
        k=r+1;D=(r+1)*2
        points=[[rng.randrange(p) for _ in range(k)] for _ in range(D)]
        targets=[[pow(w,i*j,p) for j in range(k)] for i in range(n)]
        for ids in combinations(range(D),r):
            basis=[points[j] for j in ids];rank0=rank(basis,p)
            count=sum(rank(basis+[v],p)==rank0 for v in targets)
            assert count<=rank0<=r;unions['subspaces']+=1;unions['target_membership_tests']+=n
    result['tests']['union_of_spans']=unions

    # Exact tour weight optimum: N<=8 enumerates every output ordering,
    # using the projective freedom optimally edge by edge.
    tours=[]
    for B in (2,4,8):
        max_gcd=0
        for tail in permutations(range(1,B)):
            order=(0,)+tail
            weight=sum(gcd(abs(v-u),B) for u,v in zip(order,order[1:]))
            max_gcd=max(max_gcd,weight)
        assert max_gcd==(B*B-1)//3
        tours.append(dict(B=B,max_total_unchanged=max_gcd,minimum_input_entries=B*B-max_gcd))
    result['tests']['exhaustive_tour_optimum']=tours
    average={'degree_histograms':0,'window_checks':0}
    for n in (8,16,32,64):
        for _ in range(40):
            din=[1+rng.randrange(n) if rng.randrange(5)==0 else 1 for _ in range(n)]
            dout=[1+rng.randrange(n//2) if rng.randrange(4)==0 else 1 for _ in range(n)]
            E=sum(dout);r=2*E//n
            assert sum(d<=r for d in dout)>n/2
            if r<n:
                k=r+1
                wins=[sum(din[(i+j)%n] for j in range(k)) for i in range(n)]
                assert sum(wins)==k*sum(din)
                assert min(wins)<=k*sum(din)//n
                average['window_checks']+=1
            average['degree_histograms']+=1
    result['tests']['uneven_degree_averaging']=average

    rejects=0
    for p,_ in FIELDS:
        for a in ([1],[1,1],[1,1,1,1]):
            try:ScanPlan(1,p,a,[[(0,1)] for _ in a],[[(0,1)]])
            except ValueError:rejects+=1
            else:raise AssertionError('singular cycle accepted')
        for bad in (-1,3):
            try:ScanPlan(2,p,[0,1],[[(bad,1)],[]],[[(0,1)],[(1,1)]])
            except ValueError:rejects+=1
            else:raise AssertionError('bad endpoint index accepted')
        try:root_of_order(8,p,1)
        except ValueError:rejects+=1
        else:raise AssertionError('nonprimitive root accepted')
    result['tests']['invalid_plans_rejected']=rejects

    result['necessary_degree_schedule']=[dict(log2_N=k,min_equal_degree=minimum_equal_degree(1<<k))
                                        for k in (4,8,16,32,64,128,256,512,1024,4096)]
    result['limitations']=[
      'No uniform sub-N-log-N sparse endpoint factorization found.',
      'The target O(N log N / log log N) is a conjecture, not an achieved upper bound.',
      'Fourier-positive controls are an explicit quadratic/3-halves-power mixed-radix construction.',
      'No historical test counts are reused as current execution evidence.',
      'External priority is not established. Proofs are human-readable, not proof-assistant formalized.',
      'Unit-cost field arithmetic; no finite-precision, bit-complexity or practical timing theorem.']
    result['test_group_count']=len(result['tests'])
    return result

if __name__=='__main__':
    result=run()
    out=Path(__file__).with_name('RESULTS.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS:',result['test_group_count'],'exact check groups')
    print(json.dumps(result['necessary_degree_schedule'],indent=2))
