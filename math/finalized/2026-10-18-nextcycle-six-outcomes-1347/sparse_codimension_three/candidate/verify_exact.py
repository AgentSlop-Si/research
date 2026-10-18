#!/usr/bin/env python3
"""Fresh exact controls for codimension-three masks and quantitative stability.

Requires Python 3 and SymPy. No floating-point tolerances. Does not import or
execute a prior packet's verifier. The exhaustive support search below starts
only from degree-three regularity and the prohibition of singleton overlaps.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import factorial, gcd
from pathlib import Path
import hashlib
import json
import sympy as sp

BASE = Path(__file__).resolve().parent
X = sp.Symbol('X')

@lru_cache(None)
def root_vectors(n):
    phi = sp.Poly(sp.cyclotomic_poly(n, X), X, domain=sp.ZZ)
    degree = phi.degree()
    vectors = []
    for k in range(n):
        rem = sp.Poly(X**k, X, domain=sp.ZZ).rem(phi)
        vectors.append(tuple(int(rem.nth(j)) for j in range(degree)))
    return tuple(vectors)


def roots_sum(n, exponents):
    roots = root_vectors(n)
    out = [0]*len(roots[0])
    for exponent in exponents:
        for i, value in enumerate(roots[exponent % n]):
            out[i] += value
    return tuple(out)


def zero_sum(n, exponents):
    return not any(roots_sum(n, exponents))


def support_components(column_supports):
    n = len(column_supports)
    unseen = set(range(n))
    components = []
    while unseen:
        columns = {min(unseen)}
        rows = set()
        while True:
            next_rows = set().union(*(column_supports[c] for c in columns))
            next_columns = {c for c in range(n) if column_supports[c] & next_rows}
            if next_rows == rows and next_columns == columns:
                break
            rows, columns = next_rows, next_columns
        unseen -= columns
        components.append((tuple(sorted(rows)), tuple(sorted(columns))))
    return components


def enumerate_unlabelled_supports(n):
    """Enumerate every multiset of N column triples on N labelled rows.

    Labels of columns are restored separately. Search conditions are exactly:
    each row has degree 3; each pair of columns avoids intersection size 1.
    No component classification is used to prune the search.
    """
    triples = tuple(frozenset(t) for t in combinations(range(n), 3))
    bitmasks = [sum(1 << r for r in t) for t in triples]
    counts = [0]*n
    answers = []
    nodes = 0
    def visit(chosen, candidates):
        nonlocal nodes
        nodes += 1
        if len(chosen) == n:
            if counts == [3]*n:
                answers.append(tuple(chosen))
            return
        slots = n-len(chosen)
        if any(3-count > slots for count in counts):
            return
        for offset, candidate in enumerate(candidates):
            triple = triples[candidate]
            if any(counts[r] == 3 for r in triple):
                continue
            for r in triple:
                counts[r] += 1
            following = [j for j in candidates[offset:]
                         if len(triple & triples[j]) != 1
                         and all(counts[r] < 3 for r in triples[j])]
            union = 0
            for j in following:
                union |= bitmasks[j]
            if len(chosen)+1 == n or all(count == 3 or (union >> r) & 1
                                         for r, count in enumerate(counts)):
                visit(chosen+[candidate], following)
            for r in triple:
                counts[r] -= 1
    visit([], list(range(len(triples))))
    return triples, answers, nodes


def block_congruences(n, rows, columns):
    if n % 3:
        return False
    r0, r1, r2 = rows
    c0, c1, c2 = columns
    lower = tuple(((r-r0)*(c-c0)) % n
                  for r in (r1, r2) for c in (c1, c2))
    h = n//3
    return lower in ((h,2*h,2*h,h), (2*h,h,h,2*h))


def exact_fourier_assignments(n, triples, multisets):
    """Restore every column ordering, using exact cyclotomic Gram pruning."""
    @lru_cache(None)
    def compatible(first, second, difference):
        return zero_sum(n, (r*difference for r in triples[first] & triples[second]))
    answer_count = 0
    search_nodes = 0
    for multiset in multisets:
        remaining = Counter(multiset)
        chosen = []
        def visit():
            nonlocal answer_count, search_nodes
            search_nodes += 1
            column = len(chosen)
            if column == n:
                supports = [triples[t] for t in chosen]
                for rows, columns in support_components(supports):
                    assert len(rows) == len(columns) == 3
                    assert block_congruences(n, rows, columns)
                answer_count += 1
                return
            for triple in sorted(remaining):
                if remaining[triple] and all(compatible(previous, triple, column-j)
                                            for j, previous in enumerate(chosen)):
                    remaining[triple] -= 1
                    chosen.append(triple)
                    visit()
                    chosen.pop()
                    remaining[triple] += 1
        visit()
    return {'passing_masks': answer_count, 'exact_assignment_nodes': search_nodes,
            'all_passers_have_only_three_by_three_blocks': True,
            'all_passers_satisfy_four_congruences': True}


def exhaustive_support_controls():
    results = []
    expected = {3:1,4:1,5:0,6:10,7:35,8:35,9:280,10:2100,11:5775,12:21175}
    for n in range(3,13):
        triples, multisets, nodes = enumerate_unlabelled_supports(n)
        component_types = Counter()
        labelled_count = 0
        for multiset in multisets:
            supports = [triples[t] for t in multiset]
            assert all(sum(r in t for t in supports) == 3 for r in range(n))
            assert all(len(supports[j] & supports[k]) != 1
                       for j in range(n) for k in range(j))
            sizes = []
            for rows, columns in support_components(supports):
                assert len(rows) == len(columns)
                size = len(rows)
                assert size in (3,4), (n, multiset, rows, columns)
                if size == 3:
                    assert all(supports[c] == set(rows) for c in columns)
                else:
                    omitted = [tuple(set(rows)-supports[c]) for c in columns]
                    assert all(len(t)==1 for t in omitted)
                    assert len(set(omitted))==4
                sizes.append(size)
            component_types['+'.join(map(str, sorted(sizes)))] += 1
            denominator = 1
            for count in Counter(multiset).values():
                denominator *= factorial(count)
            labelled_count += factorial(n)//denominator
        assert len(multisets) == expected[n], (n,len(multisets))
        result = {'N':n, 'unlabelled_column_multisets':len(multisets),
                  'labelled_support_masks':labelled_count,
                  'component_types':dict(sorted(component_types.items())),
                  'support_search_nodes':nodes,
                  'support_decomposition_verified':True}
        if n <= 9:
            result['fourier'] = exact_fourier_assignments(n,triples,multisets)
            assert bool(result['fourier']['passing_masks']) == (n % 3 == 0)
        results.append(result)
        print('support controls', n, len(multisets), result.get('fourier',{}),flush=True)
    return results


def conference_congruence_controls():
    """No valuation argument is used here: test the six congruences directly.

    Translating rows and columns sets r0=c0=0. Simultaneously permuting their
    matched omitted positions lets us sort r1,r2,r3, while c1,c2,c3 stay ordered.
    The first three congruences restrict their finite domains before search.
    """
    results = []
    dimensions = sorted(set(range(2,33,2)) | {40,48,64})
    for n in dimensions:
        h=n//2
        domains={a:tuple(x for x in range(1,n) if a*x % n == h) for a in range(n)}
        row_triples=0
        candidate_column_triples=0
        passing=0
        for a,b,c in combinations(range(1,n),3):
            row_triples+=1
            for x,y,z in product(domains[(b-c)%n], domains[(a-c)%n], domains[(a-b)%n]):
                if len({x,y,z}) != 3:
                    continue
                candidate_column_triples+=1
                if (a*(y-z))%n == h and (b*(x-z))%n == h and (c*(x-y))%n == h:
                    passing+=1
        assert passing==0, (n,passing)
        results.append({'N':n,'normalized_row_triples':row_triples,
                        'candidate_column_triples_after_three_equations':candidate_column_triples,
                        'six_equation_solutions':passing})
    return results


def mask_gram(n, supports, columns=True):
    """Unnormalized Fourier Gram, in the exact root-vector basis."""
    out=[]
    for j in range(n):
        line=[]
        for k in range(n):
            if columns:
                exponents=(r*(k-j) for r in supports[j]&supports[k])
            else:
                exponents=(c*(j-k) for c in range(n) if j in supports[c] and k in supports[c])
            line.append(roots_sum(n,exponents))
        out.append(line)
    return out


def scalar_gram(matrix,scalar):
    return all(value == ((scalar if i==j else 0),)+(0,)*(len(value)-1)
               for i,row in enumerate(matrix) for j,value in enumerate(row))


def divisor_supports(n):
    assert n>=6 and n%3==0
    m=n//3
    return [frozenset(range(3*(c%m),3*(c%m)+3)) for c in range(n)]


def constructive_controls():
    results=[]
    for n in list(range(6,61,3))+[72,81,90]:
        supports=divisor_supports(n)
        assert all(len(t)==3 for t in supports)
        assert all(sum(r in t for t in supports)==3 for r in range(n))
        assert scalar_gram(mask_gram(n,supports),3)
        assert scalar_gram(mask_gram(n,supports,False),3)
        components=support_components(supports)
        assert all(block_congruences(n,r,c) for r,c in components)
        results.append({'N':n,'s':n-3,'both_omitted_grams_equal_3I':True,
                        'both_inverse_support_counts_equal_s':True,
                        'all_block_congruences_pass':True})
    return results


def block_congruence_controls():
    results=[]
    for n in range(4,19):
        tested=passed=0
        for rows in combinations(range(n),3):
            for columns in combinations(range(n),3):
                tested+=1
                exact=all(zero_sum(n,(r*(columns[j]-columns[k]) for r in rows))
                          for j in range(3) for k in range(j))
                congruences=block_congruences(n,rows,columns)
                assert exact==congruences,(n,rows,columns)
                passed+=exact
        assert bool(passed)==(n%3==0)
        results.append({'N':n,'row_column_triple_pairs':tested,
                        'orthogonal_blocks':passed,'four_congruences_equivalent':True})
    return results


def inverse_witness(n):
    phi=sp.Poly(sp.cyclotomic_poly(n,X),X,domain=sp.QQ)
    alpha=sp.CRootOf(phi.as_expr(),0)
    K=sp.QQ.algebraic_field(alpha)
    z=K.convert(alpha)
    powers=[z**i for i in range(n)]
    def conjugate(value):
        result=K.zero
        for coefficient in value.to_list():
            result=result*powers[-1]+K.convert(coefficient)
        return result
    def adjoint(a):
        return [[conjugate(a[j][i]) for j in range(n)] for i in range(n)]
    def multiply(a,b):
        return [[sum((a[i][k]*b[k][j] for k in range(n)),K.zero)
                 for j in range(n)] for i in range(n)]
    def identity(a,gain):
        return all(a[i][j]==(K.convert(gain) if i==j else K.zero)
                   for i in range(n) for j in range(n))
    supports=divisor_supports(n)
    W=[[powers[(r*c)%n] for c in range(n)] for r in range(n)]
    H=[[K.zero if r in supports[c] else W[r][c] for c in range(n)] for r in range(n)]
    Kmat=[[v/K.convert(n-3) for v in row] for row in adjoint(H)]
    augmented=[list(row)+[K.one if i==j else K.zero for j in range(n)]
               for i,row in enumerate(Kmat)]
    for c in range(n):
        pivot=next(r for r in range(c,n) if augmented[r][c]!=K.zero)
        augmented[c],augmented[pivot]=augmented[pivot],augmented[c]
        factor=augmented[c][c]
        augmented[c]=[v/factor for v in augmented[c]]
        for r in range(n):
            if r!=c:
                factor=augmented[r][c]
                augmented[r]=[a-factor*b for a,b in zip(augmented[r],augmented[c])]
    Z=[row[n:] for row in augmented]
    E=[[Z[r][c]-W[r][c] for c in range(n)] for r in range(n)]
    assert identity(multiply(Z,Kmat),1) and identity(multiply(Kmat,Z),1)
    assert identity(multiply(E,adjoint(E)),3) and identity(multiply(adjoint(E),E),3)
    assert all(sum(v!=K.zero for v in row)==n-3 for row in Kmat)
    assert all(sum(Kmat[r][c]!=K.zero for r in range(n))==n-3 for c in range(n))
    # Deliberately move away from equality without changing the inverse support.
    Ktwo=[[2*v for v in row] for row in Kmat]
    Zhalf=[[v/K.convert(2) for v in row] for row in Z]
    Dhalf=[[Zhalf[r][c]-W[r][c] for c in range(n)] for r in range(n)]
    KW=multiply(Ktwo,W)
    KK=multiply(Ktwo,adjoint(Ktwo))
    transformed=multiply(multiply(Ktwo,multiply(Dhalf,adjoint(Dhalf))),adjoint(Ktwo))
    for r in range(n):
        for c in range(n):
            G=(K.one if r==c else K.zero)-KW[r][c]-conjugate(KW[c][r])+(n-3)*KK[r][c]
            assert G==transformed[r][c]-3*KK[r][c]
            if r==c:
                residual=sum((conjugate(Ktwo[r][j]-Kmat[r][j])*(Ktwo[r][j]-Kmat[r][j])
                              for j in range(n)),K.zero)
                assert G==(n-3)*residual
    assert not identity(multiply(Dhalf,adjoint(Dhalf)),3)
    return {'N':n,'normalization':'Z=sqrt(N)M, K=M^(-1)/sqrt(N), W=sqrt(N)F',
            'both_inverse_products_equal_I':True,'both_error_grams_equal_3I':True,
            'both_inverse_support_counts_equal_s':True,
            'nonequality_G_identity_verified':True,
            'nonequality_row_rigidity_identity_verified':True,
            'wrong_gain_fails_floor_error_gram':True}


def resultant_controls():
    """Exact norm identities underpinning the cyclotomic separation bound."""
    results=[]
    for n in range(4,25):
        phi=sp.Poly(sp.cyclotomic_poly(n,X),X,domain=sp.ZZ)
        tested=nonzero=0
        # Repeated powers model collisions caused by non-coprime column gaps.
        for exponents in combinations(range(n+2),3):
            exponents=tuple(k%n for k in exponents)
            polynomial=sp.Poly(sum(X**k for k in exponents),X,domain=sp.ZZ)
            rem=polynomial.rem(phi)
            resultant=int(sp.resultant(phi.as_expr(),polynomial.as_expr(),X))
            assert (rem.is_zero)==(resultant==0)
            if resultant:
                assert abs(resultant)>=1
                nonzero+=1
            tested+=1
        results.append({'N':n,'three_term_polynomials':tested,
                        'nonzero_integer_norms':nonzero,'norm_zero_iff_root_sum_zero':True})
    return results


def gap_constant_controls():
    checks=0
    examples=[]
    for n in range(2,201):
        for s in range(1,n):
            d=n-s;q=Fraction(s,n)
            gain=Fraction(s**6,(2**22)*(n**10)*(d**(2*int(sp.totient(n))-2)))
            # The chosen lower bound is below both excluded easy branches.
            assert 0<gain<=q/8 and gain<Fraction(1,n) and gain<q
            # sqrt(N/q) <= N/q^3, checked after squaring.
            assert Fraction(n,1)/q <= Fraction(n*n,1)/(q**6)
            assert 1024+24+4<=2048
            # Exact equality between final and intermediate expressions.
            gamma=Fraction(1,n*(d**(int(sp.totient(n))-1)))
            assert gain==(gamma*q**3/(2048*n))**2
            checks+=1
        if n in (4,5,7,8,10,14,16,20):
            s=n-3; d=3
            gain=Fraction(s**6,(2**22)*(n**10)*(d**(2*int(sp.totient(n))-2)))
            examples.append({'N':n,'s':s,'squared_floor':str(Fraction(3,n)),
                             'certified_added_squared_gap':str(gain)})
    return {'parameter_pairs':checks,'all_rational_constant_checks_pass':True,
            'codimension_three_nonsharp_examples':examples}


def negative_controls():
    conference=[[0,1,1,1],[1,0,-1,1],[1,1,0,-1],[1,-1,1,0]]
    assert all(sum(conference[i][k]*conference[j][k] for k in range(4)) == (3 if i==j else 0)
               for i in range(4) for j in range(4))
    supports=[frozenset(set(range(4))-{c}) for c in range(4)]
    assert not scalar_gram(mask_gram(4,supports),3)
    arbitrary_blocks=[frozenset(range(0,3))]*3+[frozenset(range(3,6))]*3
    assert not scalar_gram(mask_gram(6,arbitrary_blocks),3)
    corrupt=divisor_supports(6)
    corrupt[0]=frozenset(set(corrupt[0])-{0})
    assert not scalar_gram(mask_gram(6,corrupt),3)
    return {'real_conference_weight_three_unitary_exists':True,
            'same_support_with_Fourier_phases_rejected':True,
            'arbitrary_three_block_partition_rejected':True,
            'deleted_entry_rejected':True}


def main():
    output={'all_checks_passed':True,'arithmetic':'exact integer, rational, and cyclotomic-field',
            'support_controls':exhaustive_support_controls(),
            'conference_congruences':conference_congruence_controls(),
            'constructive_masks':constructive_controls(),
            'three_block_congruences':block_congruence_controls(),
            'inverse_witnesses':[inverse_witness(n) for n in (6,9,12)],
            'cyclotomic_resultants':resultant_controls(),
            'gap_constants':gap_constant_controls(),
            'negative_controls':negative_controls()}
    (BASE/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print('PASS: all exact controls; RESULTS.json written.',flush=True)

if __name__=='__main__':
    main()
