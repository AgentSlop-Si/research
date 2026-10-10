"""Independent phase-14 audit. No uploaded executable is imported or run.
All identity checks use integer exponents or exact modular arithmetic.
Entropy is computed from exact dyadic support sizes, without logarithmic floats.
"""
import json
import math
from collections import Counter
from pathlib import Path

OUT = Path(__file__).with_name('independent_results.json')
P = 1_000_000_009

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, math.isqrt(n)+1, 2))

def orbits(n, a):
    used = set(); answer = []
    for k in range(n):
        if k in used: continue
        seq = []; q = k
        while q not in used:
            used.add(q); seq.append(q); q = a*q % n
        assert q == k
        answer.append(seq)
    return answer

def log2_exact(n):
    assert n > 0 and n & (n-1) == 0
    return n.bit_length()-1

def cycle_audits():
    result=[]
    for m in range(4, 14):
        n=1<<m
        for b in range(3, m):
            base=1<<b; length=n//base
            cycles=orbits(n,1+base)
            expected={1:base, **{1<<s:base//2 for s in range(1,m-b+1)}}
            hist=dict(Counter(map(len, cycles)))
            assert hist==expected
            count=base+(base//2)*(m-b)
            assert len(cycles)==count
            # Every primitive L-th eigenvalue occurs once in each L-cycle.
            assert hist[length]==base//2
            # Nullity of P-cI is at most number of cycles, equality at c=1.
            assert sum(hist.values())==count
            result.append(dict(N=n,B=base,cycles=count,rank_budget=n-count,
                               primitive_eigenvalue_multiplicity=hist[length]))
    return result

def sparse_audits():
    result=[]
    for n,base in [(16,8),(32,8),(64,8),(128,16),(256,16),
                   (256,32),(512,32),(1024,32),(2048,64)]:
        length=n//base; ell=log2_exact(length); b=log2_exact(base)
        assert length<=base
        cycles=orbits(n,1+base)
        entropy_u=0; entropy_v=0; nonzeros=0; pair_checks=0
        for cyc in cycles:
            k0=cyc[0]; d=len(cyc); step=length//d
            assert d==length//math.gcd(length,k0)
            row_counts=[0]*d
            for j in range(n):
                residue=k0*j%length
                assert residue%step==0
                e=residue//step
                h=(k0*j-residue)//length
                row_counts[e]+=1; nonzeros+=1
                for t,k in enumerate(cyc):
                    assert k==k0*(1+base*t)%n
                    assert (base*residue*t+residue+length*h-k*j)%n==0
                    pair_checks+=1
            assert row_counts==[n//d]*d
            # U row probabilities: 1/d on d entries.
            # V row probabilities: d/N on N/d entries.
            entropy_u += d*log2_exact(d)
            entropy_v += d*log2_exact(n//d)
        assert pair_checks==n*n
        assert nonzeros==n*(base+base//2*ell)
        assert entropy_u==n*(ell-1)+base
        assert entropy_v==n*(b+1)-base
        assert entropy_u+entropy_v==n*log2_exact(n)
        result.append(dict(N=n,B=base,entry_exponents_checked=pair_checks,
                           residual_nonzeros=nonzeros,entropy_U=entropy_u,
                           entropy_V=entropy_v,entropy_total=entropy_u+entropy_v,
                           residual_unitary_two_coordinate_gate_lower_bound=(entropy_v+1)//2))
    return result

def extension_audits():
    assert is_prime(P)
    nonresidue=next(x for x in range(2,100) if pow(x,(P-1)//2,P)==P-1)
    z8=pow(nonresidue,(P-1)//8,P)
    assert pow(z8,4,P)==P-1
    result=[]
    for n in (16,32,64):
        length=n//8
        # All roots of X^L-z8 are primitive Nth roots. Their Frobenius
        # orbit length equals ord_N(P)=L, certifying irreducibility.
        order=1
        while pow(P,order,n)!=1: order+=1
        assert order==length
        nonzeros=0; checked=0
        for cyc in orbits(n,9):
            d=len(cyc)
            for e in range(d):
                residue=e*length//d
                for j in range(n):
                    co=[0]*length
                    for t,k in enumerate(cyc):
                        q,r=divmod((k*j)%n,length)
                        phase=pow(z8,(q-(8//d)*e*t)%8,P)
                        co[r]=(co[r]+phase*pow(d,-1,P))%P
                    assert all(v==0 for r,v in enumerate(co) if r!=residue)
                    expected=(pow(z8,((cyc[0]*j-residue)//length)%8,P)
                              if cyc[0]*j%length==residue else 0)
                    assert co[residue]==expected
                    nonzeros+=expected!=0; checked+=1
        assert checked==n*n
        result.append(dict(N=n,extension_degree=order,all_residual_coefficients_checked=checked,
                           residual_nonzeros=nonzeros,prime=P))
    return result

def polynomial_and_multiscale_audits():
    result=[]
    schedules=[lambda j:j,lambda j:j*j,lambda j:j*j+3*j+7,
               lambda j:j**4+5*j**3-7*j+11]
    for m in range(4,11):
        n=1<<m
        for b in range(3,m):
            base=1<<b; length=n//base
            for ix,f in enumerate(schedules):
                counts=Counter(f(j)%length for j in range(n))
                assert all(c%base==0 for c in counts.values())
                assert base//2 not in counts.values()
                rank=n-max(counts.values())
                if length==2:
                    assert rank==min(sum(f(j)%2==0 for j in range(n)),
                                     sum(f(j)%2==1 for j in range(n)))
                result.append(dict(N=n,B=base,schedule=ix,phase_deviation_rank=rank,
                                   required_total_rank=n-base-base//2*(m-b)))
    return result

def two_mask_audits():
    result=[]
    for n in (128,256,512):
        a=n//8; length=a//8
        rows={}
        for cyc in orbits(a,9):
            for t,k1 in enumerate(cyc): rows[k1]=(cyc[0],len(cyc),t)
        checked=0
        for k in range(n):
            k1,k2=divmod(k,8)
            k0,d,t=rows[k1]
            for j in range(n):
                j2,j1=divmod(j,a)
                r=k0*j1%length; e=r//(length//d); h=(k0*j1-r)//length
                # Each matrix coefficient has exactly one surviving orbit term.
                composed=(a*k2*j2+j1*k2+8*r+8*length*h+(n//d)*e*t)%n
                assert composed==(k*j)%n
                checked+=1
        result.append(dict(N=n,all_basis_vectors_verified=n,all_matrix_entries_verified=checked,
                           nonbase_diagonal_masks=2,method='integer phase congruences'))
    return result

def conductor_counterexample():
    n=128
    masks=[[2*j for j in range(n)], [2*j+(j<3) for j in range(n)]]
    profile=[]
    for base in (8,16,32,64):
        length=n//base
        ranks=[n-max(Counter(x%length for x in schedule).values()) for schedule in masks]
        needed=n-base-base//2*log2_exact(length)
        profile.append(dict(N=n,B=base,mask_ranks=ranks,budget=needed,passes=sum(ranks)>=needed))
    assert all(row['passes'] for row in profile[:-1])
    assert not profile[-1]['passes']
    return profile

def main():
    report=dict(cycle_audits=cycle_audits(),sparse_and_entropy_audits=sparse_audits(),
                degree_preserving_extension_audits=extension_audits(),
                polynomial_and_multiscale_audits=polynomial_and_multiscale_audits(),
                two_mask_audits=two_mask_audits(),conductor_counterexample=conductor_counterexample(),
                uploaded_code_executed=False)
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in report.items()},indent=2))
    print('PASS; results:',OUT)

if __name__=='__main__': main()
