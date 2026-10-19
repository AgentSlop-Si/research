# Independent analytic check: orders 2q and the small-degree pq range

Date: 2026-10-19 (UTC).

## Verdict

The parent-proposed proof for N = 2q, q an odd prime, is valid. It proves that a binary Fourier equality mask can have degree only 1, 2, q, or 2q. Together with divisor constructions this is exactly d | 2q. The argument uses both row and column regularity and fixed Fourier phases; it makes no full-block-support assumption.

The same elementary method proves a smaller-degree result for every N = pq with distinct primes p < q: if d < q, then d is 1 or p. General p > 2 with q < d < pq is not resolved here. These results do not close the full mixed-prime problem.

## Hypotheses and elementary cancellation fact

Let R be binary of size N by N, let D[r,c] = R[r,c] zeta_N^(rc), and assume DD* = D*D = dI with d > 0. Every row and column of R has exactly d entries equal to one.

For N = pq, two different rows congruent modulo p differ by pk with q not dividing k. Their scalar product is a positive-coefficient sum of q-th roots. Grouping common supported columns according to c modulo q, its vanishing says that all q multiplicities are equal. Consequently their common support has cardinality tq for an integer t between 0 and p. This follows from the minimal polynomial 1 + X + ... + X^(q-1) of a primitive q-th root. In particular, if their overlap has size q, it contains exactly one common column in every residue class modulo q.

## Complete necessity proof for N = 2q

Here q >= 3 is odd.

### Case 1: d < q

The q rows of either parity have pairwise disjoint supports: their overlaps are multiples of q and less than q. They occupy qd entries among 2q columns, so d <= 2. Thus d is 1 or 2.

### Case 2: q < d < 2q

Two rows of the same parity have overlap at least 2d - 2q > 0. By the cancellation fact their overlap is exactly q and contains one common column in each fiber F_v = {v, v+q}, v modulo q.

Fix one parity group and one fiber. Record the restrictions of its q rows to the two columns of the fiber as q vectors in {00,10,01,11}. Any two distinct vectors, counted with row multiplicity, have scalar product one. Since q >= 3:

- 00 cannot occur;
- 11 occurs at most once;
- 10 and 01 cannot both occur.

Therefore every row contains a common baseline column of this fiber, and at most one row also contains the other column. The baseline is unique. Repeat over all q fibers. Every row has the q baseline columns, plus d-q extra columns. Extras are disjoint across the q rows, and there are at most q of them, so q(d-q) <= q. Since d>q is integral, d=q+1.

Equality forces exactly one extra in each fiber and exactly one extra in each row. Thus, in each parity group, the map sending a row to its extra fiber is a bijection onto the q fibers. Denote these bijections by f on even rows and g on odd rows.

The two parity groups must use opposite baseline columns in every fiber. If they used the same baseline there, that column would have degree 2q, while the other would have degree 2, contrary to common degree q+1 (q>=3).

Take an even row e and odd row o. Because baselines are opposite, their common support contains exactly two columns. If f(e) and g(o) are distinct fibers, there is one common column in each of these two fibers. If the fibers coincide, both columns of that fiber are common.

There is exactly one odd row o with o congruent to e modulo q, namely o=e+q modulo 2q. For every other odd row, o-e is coprime to 2q. The vanishing sum on the two common columns c_1,c_2 then gives

    zeta_(2q)^((o-e)(c_1-c_2)) = -1,

so c_1-c_2=q modulo 2q. Hence the common columns belong to the same fiber and g(o)=f(e).

For fixed e this equality is required for q-1 >= 2 different odd rows. It contradicts injectivity of g. Therefore the entire case q<d<2q is impossible.

The only remaining degrees are 1,2,q,2q, all divisors. The argument did not need to classify masks at d=q.

## General pq small-degree result

Suppose p<q and d<q. The q rows in any fixed residue class modulo p have pairwise disjoint supports, so qd <= pq and d<=p.

If 1<d<p, every pair of distinct rows has overlap less than p. No nonempty overlap can have zero Fourier sum:

- if the row difference is divisible by p, a nonempty overlap has at least q terms;
- if it is divisible by q, a nonempty overlap has at least p terms;
- if the row difference is coprime to pq, a nonempty binary vanishing sum of pq-th roots is a union of full p-cycles or full q-cycles, so has at least p terms.

Thus all N row supports would be pairwise disjoint, requiring Nd<=N, a contradiction to d>1. Consequently d is 1 or p.

For completeness, the binary primitive-character statement has a direct proof. In CRT coordinates, a rational coefficient grid beta_ab has primitive-character sum zero exactly when beta_ab=u_a+v_b. One can see this by taking the tensor product of the prime cyclotomic quotient maps: the quotient has dimension (p-1)(q-1), and its kernel is the sum of the subspaces constant along either coordinate. If beta is binary and u takes two different values, then their difference must be 1 or -1; a nonconstant v would force at least three distinct grid values. Hence one coordinate is constant. A nonempty grid therefore consists of complete parallel p-lines or complete parallel q-lines.

## Exact boundary of this check

The local binary two-coordinate lemma is not a weighted matching lemma. At N=6 the positive coefficient grid

    1 2 2
    2 3 3

is of the form u_a+v_b with u=(0,1), v=(1,2,2), so its primitive-character sum vanishes, yet neither coordinate direction is constant. All coefficients are 2,3-smooth. It is not asserted to be a square equality mask or a counterexample to d|N. It only obstructs replacing binary overlap coefficients by arbitrary smooth integer weights in a mixed-prime descent.

No historical program was executed, no external service was changed, and no owner status or repository state was modified. This review is an analytic argument, not a finite-search inference.

## Additional general-pq theorem: exclusion near full degree

For every pair of distinct primes p<q, no binary Fourier equality mask has

    (p-1)q < d < pq.

For p=2 this is already the high-degree part proved above. Suppose p>=3.

Rows in the same residue class modulo p have overlaps divisible by q. In the stated interval, two such rows overlap in more than (p-2)q columns and in fewer than pq columns. Thus their overlap is exactly (p-1)q, with exactly p-1 common entries in every p-element column fiber F_v = {c : c=v modulo q}.

Fix one row-residue group and one fiber. The q binary vectors of length p have pairwise dot product p-1. Every vector has weight at least p-1. At most one vector can have weight p, and all the weight-(p-1) vectors must be equal (otherwise their intersection has size p-2). Hence all q rows share the same baseline (p-1)-subset of that fiber, and at most one row also contains its omitted column.

There are q baseline fibers. Every row has (p-1)q baseline entries and d-(p-1)q extras. Extras are disjoint among the q rows and at most q in total. Integrality and d>(p-1)q imply

    d=(p-1)q+1.

Moreover each row has exactly one extra and each fiber has exactly one extra.

There are p row-residue groups. For a fixed column in a fixed fiber, let t be the number of groups omitting it from their baseline. A group containing it in the baseline contributes q to the column degree; a group omitting it contributes exactly one, from its unique extra. Its degree is therefore

    (p-t)q+t = pq-t(q-1).

The common degree pq-(q-1) forces t=1. Consequently different row groups omit different baseline columns in every fiber.

Choose rows in two different residue groups modulo p and with different residues modulo q; their difference is primitive modulo pq. Their baseline supports intersect in exactly p-2 columns in every fiber. Each of the two rows has one extra, and that extra belongs to the other row's baseline in its fiber. Thus their common support has p-2 entries in every fiber, plus two additional entries distributed over at most two fibers.

Since q>p>=3, at least one fiber is untouched. Its common-support count p-2 is strictly between 0 and p, so the overlap cannot be a union of full p-lines. The counts are unequal between touched and untouched fibers, so it cannot be a union of full q-lines either. This contradicts the binary primitive-character cancellation lemma.

The result is an additional uniform excluded range, not the full pq classification. Together with the small-degree result it leaves only q <= d <= (p-1)q for a proper unresolved degree when p>=3 (and the allowed degree p below q).
