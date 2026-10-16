"""New independent checks of the proof's finite combinatorial ceilings.

No historical/candidate module is imported, parsed, compiled or executed.
These finite controls support, and do not replace, the all-input written proof.
"""
import json
import math
from pathlib import Path

def D(k):
    return 2*k**3+k*k+3*k

def determinant_max(k):
    # Every pivot and possible sign swap, every lower-row factor,
    # and every possible trailing-matrix update.
    return 3*k+sum(h+2*h*h for h in range(k))

def interpolation_fixed(q):
    return q+2*sum(range(1,q+1))+2*sum(range(1,q+2))+3*sum(range(1,q+1))

def interpolation_arbitrary(n):
    h=n*(n-1)//2
    return 9*h+n*(n+1)+(1 if h else 0)

def gcd_loose(d):
    return (d+1)*(1+(d+1)*(1+2*(d+1)))+(d+2)

def bound(s,n,p):
    m=s+1; ell=2*s+2
    b=s*(s+1)*(2*s+1)//6
    v=s*(s+1)*(4*s+5)//6
    r=b+4
    Z=2*s+1+6*m*(m+1)+2*(m+1)*D(m)+12*(m+2)**2+D(2*m)
    C=r*(Z+2*(v+b).bit_length()+2*(m*m).bit_length()+10)+1+8*(b+2)**2+6*(b+1)+(b+1)*(b+2)
    T=4*(b+2)**3+3*(b+2)**2+(4*b*b+1)*(n.bit_length()-1)+20
    h=p.bit_length()
    S=2*h*(p+2)+2*h*h+3*h+1
    mu=math.isqrt(n)+1
    gamma=(n+mu-1)//mu+1
    E=(2*b+3)*(n//2)+S+7+mu+2*gamma+10*n.bit_length()
    P=4*s+1+6*(s+2)*(2*s+1)+2*(s+2)*D(s+1)+12*(s+3)**2+4*(s+3)**3+1+4*ell+16*(s+1)**2+s*s+4*(s+2)**3+3*ell*s
    value=n*(2*ell-1)+(3*ell+1)+C+T+E+2*b*(P+(6*s+1)*n)
    return dict(s=s,n=n,p_upper_envelope=p,b=b,compressed_samples=r,candidate_ceiling=2*b,
                Z=Z,C=C,T=T,S=S,E=E,P=P,field_operation_upper_bound=value)

def isprime(p):
    return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))

def prime_controls():
    records=[]
    total=0
    for p in range(3,502,2):
        if not isprime(p): continue
        # Direct residue enumeration, not Tonelli-Shanks or source execution.
        squares={x*x%p for x in range(1,p)}
        assert len(squares)==(p-1)//2
        z=next(x for x in range(2,p) if x not in squares)
        assert 2<=z<=p-1
        traces={}
        for w in range(2,p):
            t=(w+pow(w,-1,p))%p
            traces.setdefault(t,[]).append(w)
        assert max(map(len,traces.values()))<=2
        assert len(traces)==(p-1)//2
        for s in range(1,9):
            b=s*(s+1)*(2*s+1)//6
            if p<=4*b+20: continue
            seen=set(); trials=0
            for w in range(2,p):
                trials+=1
                seen.add((w+pow(w,-1,p))%p)
                if len(seen)==b+4: break
            assert len(seen)==b+4 and trials<=2*(b+4)
            total+=1
        records.append(dict(p=p,least_nonresidue=z,trace_count=len(traces)))
    return records,total

def main():
    primitive_cases=0
    for k in range(1,410):
        assert determinant_max(k)<=D(k)
        assert interpolation_fixed(k)<=6*(k+2)**2
        assert interpolation_arbitrary(k)<=8*(k+1)**2
        assert gcd_loose(k)<=4*(k+2)**3
        primitive_cases+=4
    valuations=[]
    for s in range(1,9):
        m=s+1;b=sum(j*j for j in range(1,s+1))
        v=s*(s+1)*(4*s+5)//6
        grade=m*m*(2*m-1)
        root_sum=sum(max(2*i,2*j+1) for i in range(s+1) for j in range(s+1))
        assert grade-root_sum==v
        assert grade-2*v-m*m==2*b
        valuations.append(dict(s=s,grade=grade,v=v,b=b))
    primes,sample_cases=prime_controls()
    # Endpoint rectangle provides monotone upper envelopes. In particular,
    # p=2^31-1 and n=4096 are NOT claimed to be an admitted root-field pair.
    envelopes=[bound(s,4096,2**31-1) for s in range(1,9)]
    result={
        'status':'PASS',
        'method':'Self-authored combinatorial and small-prime controls only; no supplied source execution.',
        'not_an_all_input_execution_test':True,
        'primitive_ceiling_checks':primitive_cases,
        'resultant_degree_identity_checks':valuations,
        'prime_controls':primes,
        'admitted_reciprocal_sampling_cases':sample_cases,
        'upper_envelopes_not_admitted_fixtures':envelopes,
    }
    Path(__file__).with_name('BOUND_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'primitive_ceiling_checks':primitive_cases,
                      'prime_count':len(primes),'sampling_cases':sample_cases,
                      'largest_envelope':max(x['field_operation_upper_bound'] for x in envelopes)}))

if __name__=='__main__':main()
