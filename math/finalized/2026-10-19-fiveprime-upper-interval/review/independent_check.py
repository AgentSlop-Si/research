#!/usr/bin/env python3
"""Independent exact checks for the open interval 3q < d < 4q.
Integer polynomial remainders in original indices; no candidate code imported.
Finite corroboration only. The proof is reviewed separately in REVIEW.md.
"""
from itertools import combinations
from pathlib import Path
from math import gcd
import json

ROOT=Path(__file__).resolve().parent

def cyclotomic(q):
    # Phi_(5q)(X) = (1 + X^q + X^(2q) + X^(3q) + X^(4q)) /
    #                (1 + X + X^2 + X^3 + X^4), since q is prime and q != 5.
    work=[int(k%q==0) for k in range(4*q+1)]
    quotient=[0]*(4*q-3)
    for k in range(4*q,3,-1):
        quotient[k-4]=work[k]
        for j in range(5): work[k-4+j]-=quotient[k-4]
    assert work==[0]*len(work)
    assert len(quotient)==4*(q-1)+1 and quotient[-1]==1
    return quotient

class ExactRoots:
    def __init__(self,q):
        self.n=5*q; self.phi=cyclotomic(q); self.dimension=len(self.phi)-1
        self.monomials=[]
        for k in range(self.n):
            work=[0]*self.n; work[k]=1
            for j in range(self.n-1,self.dimension-1,-1):
                coefficient=work[j]
                if coefficient:
                    for a,value in enumerate(self.phi):
                        work[j-self.dimension+a]-=coefficient*value
            self.monomials.append(tuple(work[:self.dimension]))
    def remainder(self,columns,difference):
        result=[0]*self.dimension
        for c in columns:
            for j,value in enumerate(self.monomials[(difference*c)%self.n]):
                result[j]+=value
        return result
    def zero(self,columns,difference):
        return not any(self.remainder(columns,difference))

def run(q,all_primitive):
    n=5*q; exact=ExactRoots(q)
    e5=q*pow(q,-1,5); eq=5*pow(5,-1,q)
    index=lambda a,b:(e5*a+eq*b)%n
    coordinates={index(a,b):(a,b) for a in range(5) for b in range(q)}
    assert len(coordinates)==n
    assert (e5*e5-e5)%n==(eq*eq-eq)%n==(e5*eq)%n==0
    assert (e5+eq)%n==1
    phase_checks=0
    for r in range(n):
        a,b=coordinates[r]
        assert (r%5,r%q)==(a,b)
        for c in range(n):
            u,v=coordinates[c]
            assert (r*c-e5*a*u-eq*b*v)%n==0
            phase_checks+=1

    # The coverage bound includes the row under consideration.
    coverage=[]
    reduction=[]
    for d in range(3*q+1,4*q):
        assert d>q+4
        coverage.append([d,d-(q+4)])
        representations=[[ell,f] for ell in range(4) for f in range(1,q)
                         if ell*q+(5-ell)*f==d]
        singleton=[ell for ell,f in representations if f==1]
        assert singleton==([3] if d==3*q+2 else [])
        reduction.append({'d':d,'mixed_cycle_counts':representations,
                          'singleton_line_counts':singleton})

    triples=list(combinations(range(5),3))
    support={(A,f):frozenset(index(u,v) for u in range(5) for v in range(q)
                            if u in A or v==f)
             for A in triples for f in range(q)}
    chars=[h for h in range(1,n) if gcd(h,n)==1] if all_primitive else [1]
    local_checks=local_zeros=0
    cross_witness=None
    for A in triples:
        for B in triples:
            h=len(set(A)&set(B))
            assert 1<=h<=3
            for f in range(q):
                for g in range(q):
                    overlap=support[A,f]&support[B,g]
                    sizes=[sum(index(u,v) in overlap for u in range(5)) for v in range(q)]
                    if f!=g:
                        assert all(sizes[v]==(3 if v in (f,g) else h) for v in range(q))
                    expected_zero=(A==B and f!=g)
                    for char in chars:
                        actual=exact.zero(overlap,char)
                        assert actual==expected_zero,(q,A,B,f,g,char)
                        local_checks+=1; local_zeros+=actual
                        if A!=B and f!=g and cross_witness is None:
                            cross_witness={'A':A,'B':B,'f':f,'g':g,'original_difference':char,
                                           'original_columns':sorted(overlap),
                                           'remainder':exact.remainder(overlap,char)}

    # Exhaustively verify the at-most-two exclusions for arbitrary target fibers
    # and affine permutations; all q! permutations obey the same bijection proof.
    partners=0
    for coefficient in range(1,q):
        for offset in range(q):
            for b in range(q):
                for f in range(q):
                    eligible=[c for c in range(q) if c!=b and
                              (coefficient*c+offset)%q!=f]
                    assert len(eligible)>=q-2
                    partners+=1

    # Full-square negative control with unrelated within-group permutations.
    rows=[]
    for r in range(n):
        a,b=coordinates[r]
        A=tuple(sorted({a,(a+1)%5,(a+2)%5}))
        f=((a+1)*b+2*a)%q
        rows.append(support[A,f])
    columns=[frozenset(r for r in range(n) if c in rows[r]) for c in range(n)]
    degree=3*q+2
    assert all(len(S)==degree for S in rows+columns)
    row_bad=column_bad=same_group=0
    square_witness=None
    for r in range(n):
        for s in range(n):
            if r==s: continue
            rem=exact.remainder(rows[r]&rows[s],r-s)
            row_bad+=bool(any(rem))
            column_bad+=not exact.zero(columns[r]&columns[s],s-r)
            if coordinates[r][0]==coordinates[s][0]:
                assert not any(rem)
                same_group+=1
            if any(rem) and gcd(r-s,n)==1 and square_witness is None:
                square_witness={'rows':[r,s],'crt_rows':[coordinates[r],coordinates[s]],
                                'columns':sorted(rows[r]&rows[s]),'remainder':rem}
    assert row_bad and column_bad and square_witness

    # Positive controls span monomial, both CRT divisor supports, and full mask.
    positives=[]
    for kind,expected in [('diagonal',1),('q_lines',q),('five_fibers',5),('full',n)]:
        pos=[]
        for r in range(n):
            a,b=coordinates[r]
            pos.append(frozenset(c for c in range(n) if
                (kind=='diagonal' and r==c) or
                (kind=='q_lines' and coordinates[c][0]==a) or
                (kind=='five_fibers' and coordinates[c][1]==b) or
                kind=='full'))
        poscols=[frozenset(r for r in range(n) if c in pos[r]) for c in range(n)]
        assert all(len(S)==expected for S in pos+poscols)
        entries=0
        for r in range(n):
            for s in range(n):
                if r!=s:
                    assert exact.zero(pos[r]&pos[s],r-s)
                    assert exact.zero(poscols[r]&poscols[s],s-r)
                entries+=2
        positives.append({'kind':kind,'degree':expected,'both_gram_entries':entries})
    return {'q':q,'cyclotomic':exact.phi,'crt_phase_checks':phase_checks,
            'coverage_margins':coverage,'degree_reductions':reduction,
            'primitive_overlap_checks':local_checks,'primitive_overlap_zeros':local_zeros,
            'cross_overlap_witness':cross_witness,'partner_selection_checks':partners,
            'negative_degree':degree,'negative_row_nonzero_offdiagonals':row_bad,
            'negative_column_nonzero_offdiagonals':column_bad,
            'negative_same_group_zero_checks':same_group,
            'negative_both_gram_entries':2*n*n,'negative_square_witness':square_witness,
            'positive_controls':positives}

if __name__=='__main__':
    result={'scope':'Original arbitrary binary fixed-Fourier masks; finite exact controls supplement symbolic audit only.',
            'results':[run(7,True),run(11,True),run(13,False)]}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={'status':'PASS','q_values':[7,11,13],
             'crt_phase_checks':sum(r['crt_phase_checks'] for r in result['results']),
             'primitive_overlap_checks':sum(r['primitive_overlap_checks'] for r in result['results']),
             'partner_selection_checks':sum(r['partner_selection_checks'] for r in result['results']),
             'positive_both_gram_entries':sum(c['both_gram_entries'] for r in result['results'] for c in r['positive_controls']),
             'negative_both_gram_entries':sum(r['negative_both_gram_entries'] for r in result['results'])}
    print(json.dumps(summary,indent=2))
