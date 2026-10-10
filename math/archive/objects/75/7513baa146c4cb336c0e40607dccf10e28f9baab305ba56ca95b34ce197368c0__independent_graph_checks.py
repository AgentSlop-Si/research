#!/usr/bin/env python3
"""Fresh checks for graph-union algebra and output-rank extension.

No uploaded module is imported or executed. Source files are read only for
SHA-256 provenance. All transforms, convolution, rank operations, and fixtures
below were authored for this audit; direct quadratic reference methods are
correctness oracles, not claims about the online fast recognizer's work.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib
import argparse
import json
import random

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'extracted/fft_hero17_tensor_fiber_graph_union_2026-10-10/hero17_tensor_union'
RNG = random.Random(1954100917)
COUNTS = Counter()


def primitive_root_of_order(n, p):
    # Audit fixture setup only; not part of an online algorithm.
    assert p > n and (p-1) % n == 0
    for a in range(1, p):
        w = pow(a, (p-1)//n, p)
        if pow(w,n,p) == 1 and all(pow(w,d,p) != 1 for d in range(1,n) if n%d == 0):
            return w
    raise AssertionError((n,p))


def materialize(rows, q, m, p, w):
    eta = pow(w,q,p)
    return [sum(c*pow(eta,h*u,p) for h,c in rows[t].items()) % p
            for u in range(m) for t in range(q)]


def raw_coefficients(x,q,m,p,w):
    eta=pow(w,q,p)
    inv=pow(m,-1,p)
    return [{h: a for h in range(m)
             if (a := inv*sum(x[t+q*u]*pow(eta,(-h*u)%m,p) for u in range(m))%p)}
            for t in range(q)]


def direct_convolution(x,y,p):
    n=len(x)
    return [sum(x[j]*y[(k-j)%n] for j in range(n))%p for k in range(n)]


def graph_coefficients(xrows,yrows,q,m,p,w):
    # Independent algebra implementation: enumerate row pairs, intersect labels,
    # keep only a dictionary accumulator. Uploaded code uses frequency buckets,
    # a dense array, and an event list instead.
    eta=pow(w,q,p)
    coeff={}
    edges=0
    events=[]
    for a in range(q):
        for b in range(q):
            t=(a+b)%q
            carry=(a+b)//q
            for h in xrows[a].keys() & yrows[b].keys():
                term=m*xrows[a][h]*yrows[b][h]*pow(eta,(-h*carry)%m,p)%p
                idx=(t,h)
                old=coeff.get(idx,0)
                coeff[idx]=(old+term)%p
                events.append((idx,old,coeff[idx]))
                edges+=1
    return {k:v for k,v in coeff.items() if v}, edges, events


def matrix_of_states(states,q,m):
    return [[states.get((t,h),0) for h in range(m)] for t in range(q)]


def reconstruct(states,q,m,p,w):
    return materialize([{h:c for (t0,h),c in states.items() if t0==t} for t in range(q)],q,m,p,w)


def rank_factor(matrix,p,bound=None):
    """Fresh fixed-rank elimination with an explicit reconstruction assertion."""
    q=len(matrix); m=len(matrix[0]) if q else 0
    basis=[]; pivots=[]; coefficients=[]
    for raw in matrix:
        residual=[v%p for v in raw]
        row_factors=[]
        for pivot,base in zip(pivots,basis):
            multiplier=residual[pivot]
            row_factors.append(multiplier)
            residual=[(a-multiplier*b)%p for a,b in zip(residual,base)]
        pivot=next((j for j,a in enumerate(residual) if a),None)
        if pivot is not None:
            if bound is not None and len(basis)==bound:
                return None
            multiplier=residual[pivot]
            inverse=pow(multiplier,-1,p)
            basis.append([inverse*a%p for a in residual])
            pivots.append(pivot)
            row_factors.append(multiplier)
        coefficients.append(row_factors)
    for row in coefficients:
        row.extend([0]*(len(basis)-len(row)))
    assert all(sum(coefficients[t][l]*basis[l][h] for l in range(len(basis)))%p == matrix[t][h]%p
               for t in range(q) for h in range(m))
    return coefficients,basis


def low_rank_reconstruct(matrix,q,m,p,w,bound):
    labels=[h for h in range(m) if any(matrix[t][h] for t in range(q))]
    compressed=[[matrix[t][h] for h in labels] for t in range(q)]
    factor=rank_factor(compressed,p,bound)
    if factor is None:
        return None
    left,right=factor
    eta=pow(w,q,p)
    powers=[1]
    for _ in range(1,m):
        powers.append(powers[-1]*eta%p)
    evaluated=[[sum(row[j]*powers[(h*u)%m] for j,h in enumerate(labels))%p
                for u in range(m)] for row in right]
    return [sum(left[t][l]*evaluated[l][u] for l in range(len(right)))%p
            for u in range(m) for t in range(q)]


def verify_quotient_identity(xrows,yrows,states,q,m,p,w):
    # The quotient gauge turns the carry-twisted length-Q product into a cyclic
    # convolution separately for every h; this does not give a free joint FFT.
    for h in range(m):
        alpha=[row.get(h,0)*pow(w,(-h*t)%(q*m),p)%p for t,row in enumerate(xrows)]
        beta=[row.get(h,0)*pow(w,(-h*t)%(q*m),p)%p for t,row in enumerate(yrows)]
        ordinary=direct_convolution(alpha,beta,p)
        for t in range(q):
            assert states.get((t,h),0)==m*pow(w,h*t,p)*ordinary[t]%p
            COUNTS['quotient_state_comparisons']+=1


def verify_pair(xrows,yrows,q,m,p,w,check_raw=True):
    x=materialize(xrows,q,m,p,w); y=materialize(yrows,q,m,p,w)
    # Recover modes from raw arrays by a separately written full short DFT.
    if check_raw:
        assert raw_coefficients(x,q,m,p,w)==xrows
        assert raw_coefficients(y,q,m,p,w)==yrows
        COUNTS['raw_mode_recoveries']+=2
    states,edges,events=graph_coefficients(xrows,yrows,q,m,p,w)
    expected=direct_convolution(x,y,p)
    actual=reconstruct(states,q,m,p,w)
    assert actual==expected
    COUNTS['all_output_convolution_pairs']+=1
    COUNTS['all_output_convolution_bins']+=q*m
    ax=Counter(h for row in xrows for h in row)
    by=Counter(h for row in yrows for h in row)
    assert edges==sum(ax[h]*by[h] for h in ax)
    kx=sum(map(len,xrows)); ky=sum(map(len,yrows)); s=len(states)
    assert s<=q*m and s<=edges and s*s<=q*kx*ky
    COUNTS['support_bound_cases']+=1
    verify_quotient_identity(xrows,yrows,states,q,m,p,w)
    return states,edges,events,expected


def random_rows(q,m,p,r):
    rows=[]
    for _ in range(q):
        hs=RNG.sample(range(m),RNG.randrange(min(r,m)+1))
        rows.append({h:RNG.randrange(1,p) for h in hs})
    return rows


def boundary_and_random_cases():
    examples=[]
    for q,m,p in [(1,1,3),(1,8,17),(2,1,5),(2,2,17),(2,3,13),
                  (3,2,13),(3,3,19),(3,4,13),(4,4,97),(4,8,97),(8,4,97),(5,5,101),(6,6,109)]:
        w=primitive_root_of_order(q*m,p)
        for r in (1,2,m):
            for trial in range(12):
                x=random_rows(q,m,p,r); y=random_rows(q,m,p,r)
                verify_pair(x,y,q,m,p,w)
        examples.append({'q':q,'m':m,'p':p,'omega':w})
    return examples


def exhaustive_tiny():
    q=m=2; p=5; w=2
    choices=[{}]+[{h:c} for h in range(m) for c in range(1,p)]
    vectors=list(product(choices,repeat=q))
    for x in vectors:
        for y in vectors:
            verify_pair(x,y,q,m,p,w,check_raw=False)
            COUNTS['exhaustive_one_mode_pairs_N4']+=1


def cancellation_controls():
    q=m=3; p=19; w=primitive_root_of_order(9,p)
    x=[{0:1} for _ in range(q)]
    # Written to reproduce the source loop's event order for bookkeeping only.
    y=[{0:1},{0:p-1},{0:2}]
    states,edges,_,expected=verify_pair(x,y,q,m,p,w)
    dense=[0]*(q*m); active=[]
    for b in range(q):
        for a in range(q):
            idx=((a+b)%q)*m
            if dense[idx]==0:
                active.append(idx)
            dense[idx]=(dense[idx]+m*y[b][0])%p
    dedup=[idx for idx in dict.fromkeys(active) if dense[idx]]
    assert len(active)==6 and len(dedup)==3
    assert {(idx//m,idx%m):dense[idx] for idx in dedup}==states
    # Final cancellation, disjoint-label zero product, and zero inputs.
    verify_pair(x,[{0:1},{0:p-1},{}],q,m,p,w)
    assert verify_pair(x,[{1:1} for _ in range(q)],q,m,p,w)[0]=={}
    assert verify_pair([{}]*q,x,q,m,p,w)[0]=={}
    return {'q':q,'m':m,'p':p,'omega':w,'edges':edges,'active_events':len(active),
            'deduplicated_surviving_states':len(dedup),'expected_raw':expected}


def maximum_rank_controls():
    witnesses=[]
    for q,p in [(2,17),(3,19),(4,97),(5,101),(8,257),(16,257)]:
        m=q; w=primitive_root_of_order(q*m,p)
        for trial in range(3):
            h=list(range(q)); g=list(range(q)); RNG.shuffle(h); RNG.shuffle(g)
            x=[{h[t]:RNG.randrange(1,p)} for t in range(q)]
            y=[{g[t]:RNG.randrange(1,p)} for t in range(q)]
            states,edges,_,_=verify_pair(x,y,q,m,p,w)
            xm=[[materialize(x,q,m,p,w)[t+q*u] for u in range(m)] for t in range(q)]
            ym=[[materialize(y,q,m,p,w)[t+q*u] for u in range(m)] for t in range(q)]
            assert len(rank_factor(xm,p)[1])==q
            assert len(rank_factor(ym,p)[1])==q
            assert edges==q and len(states)==q
            COUNTS['full_matrix_rank_pairs']+=1
        witnesses.append({'q':q,'n':q*q,'p':p,'omega':w,'E':q,'S':q})
    return witnesses


def adversarial_controls():
    witnesses=[]
    for s,p in [(2,97),(3,163),(4,257),(5,11251)]:
        q=m=s*s; n=q*m
        # Fixture primality and n-th-root availability are checked directly.
        assert all(p%d for d in range(2,int(p**0.5)+1))
        w=primitive_root_of_order(n,p)
        x=[{t%s:1} for t in range(q)]
        y=[{t//s:1} for t in range(q)]
        states,edges,_,_=verify_pair(x,y,q,m,p,w)
        assert len(states)==edges==s*q
        assert len(states)**2==q*sum(map(len,x))*sum(map(len,y))
        witnesses.append({'s':s,'q':q,'m':m,'p':p,'omega':w,'E':edges,'S':len(states),
                          'reconstruction_contributions':m*len(states),'ratio_2_rejects':len(states)>2*q})
    return witnesses


def rank_fallback_controls():
    witnesses=[]
    for s,m,p in [(2,4,97),(3,9,163),(4,16,257),(5,25,11251),
                  (2,64,257),(3,81,1459),(4,64,12289)]:
        q=s*s; n=q*m; w=primitive_root_of_order(n,p); eta=pow(w,q,p)
        x=[{} for _ in range(q)]; y=[{} for _ in range(q)]
        for h in range(s):
            for v in range(s):
                a=h+s*v
                x[a][h]=pow(eta,h*((v+h)//s),p)
            for b0 in range(s):
                b=(s-1)*h+b0
                y[b][h]=1
        assert max(map(len,x))==1 and max(map(len,y))<=2
        states,edges,_,expected=verify_pair(x,y,q,m,p,w)
        assert states=={(t,h):m%p for t in range(q) for h in range(s)}
        c=matrix_of_states(states,q,m)
        assert len(rank_factor(c,p)[1])==1
        assert low_rank_reconstruct(c,q,m,p,w,1)==expected
        assert len(states)==s*q
        COUNTS['guard_escape_rank_one_families']+=1
        witnesses.append({'s':s,'q':q,'m':m,'n':n,'p':p,'omega':w,'rx':1,'ry':2,
                          'E':edges,'S':len(states),'output_state_matrix_rank':1,
                          'ratio_2_rejects':len(states)>2*q,'rank_1_accepts':True,
                          'active_frequency_columns':s,'rank_1_short_transform_terms':m*s,
                          'rank_1_output_combinations':n})
    # General rectangular rank fixtures, including rank-zero and forced rejection.
    for q,m,p in [(3,4,13),(4,4,97),(4,8,97),(8,4,97),(6,6,109)]:
        w=primitive_root_of_order(q*m,p)
        for d in range(min(q,m)+1):
            for _ in range(4):
                left=[[RNG.randrange(p) for l in range(d)] for t in range(q)]
                right=[[RNG.randrange(p) for h in range(m)] for l in range(d)]
                c=[[sum(left[t][l]*right[l][h] for l in range(d))%p for h in range(m)] for t in range(q)]
                actual=low_rank_reconstruct(c,q,m,p,w,d)
                sparse={(t,h):c[t][h] for t in range(q) for h in range(m) if c[t][h]}
                assert actual==reconstruct(sparse,q,m,p,w)
                rank=len(rank_factor(c,p)[1])
                if rank:
                    assert low_rank_reconstruct(c,q,m,p,w,rank-1) is None
                COUNTS['rank_fallback_matrix_cases']+=1
    return witnesses


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,help='Optional result JSON destination; default is no file writes.')
    args=parser.parse_args()
    provenance=json.loads((HERE/'source_provenance.json').read_text())
    hashes={name:meta['sha256'] for name,meta in provenance['files'].items()}
    if SOURCE.exists():
        assert hashes=={name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in hashes}
    parameters=boundary_and_random_cases()
    exhaustive_tiny()
    cancellation=cancellation_controls()
    full_rank=maximum_rank_controls()
    adversarial=adversarial_controls()
    rank_extension=rank_fallback_controls()
    result={
        'status':'all independent assertions passed',
        'seed':1954100917,
        'uploaded_code_executed_or_imported':False,
        'model':'Exact supplied prime fields; fixture root search is not online work.',
        'counts':dict(sorted(COUNTS.items())),
        'boundary_and_random_parameters':parameters,
        'cancellation_revival':cancellation,
        'full_rank_graph_witnesses':full_rank,
        'tight_state_growth_witnesses':adversarial,
        'output_rank_fallback_witnesses':rank_extension,
        'source_sha256':hashes,
        'scope':'Algebra/independent checks only. Source tests were read as historical evidence and not rerun. Online fiber recognition is audited in the sibling report.'
    }
    if args.output is not None:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counts':result['counts']},indent=2))


if __name__=='__main__':
    main()
