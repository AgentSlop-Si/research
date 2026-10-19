# Mixed-prime Fourier equality masks: complete order 2q classification

Date: 2026-10-19 UTC. Owner: M-SPARSE-DEFECT, priority 42.
Status: proof candidate, pending independent review. The owner remains TO RESEARCH.

## 1. Exact new result

**Theorem.** Let q be any odd prime, N=2q, and zeta any primitive N-th root of unity. Let R be a binary N-by-N matrix and set

    D[r,c] = R[r,c] zeta^(rc),  0 <= r,c < N.

If D*D=d I_N, where 1<=d<=N, then

    d is one of 1, 2, q, 2q.

Conversely each of these four values is realized. Thus the divisibility necessity d|N is proved for the infinite mixed-prime family N=2q. This is a direct argument in the original fixed Fourier phases. It neither asserts a CRT extension of prime-power descent nor assumes full square support components.

The accepted equality-mask criterion and complementary-divisor construction imply, in the proper inverse-row range 1<=d<2q,

    Delta_(2q,2q-d) = sqrt(d/(2q)) iff d belongs to {1,2,q}.

The other proper d have the inherited strict separation and existing quantitative no-mask bound. The d=N boundary concerns masks only; s=0 is not an admissible invertible inverse-row problem.

A supplementary theorem proved in Section 7 says that, for any distinct primes p<q and N=pq, a weight d<q is possible exactly when d is 1 or p. Section 7b also excludes (p-1)q<d<pq. The unresolved nondivisor range at odd squarefree semiprime orders is therefore q<d<=(p-1)q. General orders p^a q and orders with more prime factors remain open except their previously accepted scopes.

## 2. Both Grams and the prime-order overlap lemma

Because D is square and d>0, D*D=dI implies DD*=dI. Every row and every column of R has exactly d ones. Write S_r for the support of row r.

For two different rows r,s of the same parity, r-s=2h with h nonzero modulo q. Thus omega=zeta^(r-s) is a primitive q-th root. Set

    b_t = |S_r intersect S_s intersect {t,t+q}|,  0<=t<q.

Their row Gram vanishes exactly when sum_t b_t omega^t=0. Since Phi_q(X)=1+X+...+X^(q-1), a rational polynomial of degree at most q-1 vanishing at omega has all coefficients equal. Consequently

    b_0=...=b_(q-1)=b,   b in {0,1,2},
    |S_r intersect S_s|=q b.                         (2.1)

This coefficient equality includes zeros and uses the actual phase difference, not just the overlap cardinality. If d<2q, b=2 is impossible because the overlap has at most d elements.

## 3. Weights below q

Suppose 1<=d<q. Equation (2.1) forces distinct rows of the same parity to have disjoint supports. There are q even rows, each with d neighbors, all in 2q columns. Hence qd<=2q, or d<=2.

Thus every d<q is either 1 or 2. This includes the boundary q=3 without exception.

## 4. A complete description of the only possible weight above q

Suppose q<d<2q. Any two d-element subsets of a 2q-element set intersect, since their intersection has size at least 2d-2q>0. Thus (2.1) gives b=1 for every pair of distinct same-parity rows:

    Each two such rows meet in exactly one column of every pair {t,t+q}. (4.1)

Fix one parity group G and one column pair {t,t+q}. The q rows yield q binary vectors v_r in {00,10,01,11}. Equation (4.1) says

    v_r dot v_s = 1 for all distinct r,s in G.         (4.2)

The following elementary classification uses q>=3:

- No vector is 00.
- At most one vector is 11.
- Vectors 10 and 01 cannot both occur.
- At least q-1>=2 vectors are singletons, so they are all the same singleton.

It follows that one column of {t,t+q} is present in every row of G. Call this the baseline column. The other column is present in at most one row. This conclusion holds separately for every column pair and for each parity group.

Therefore every row of G contains q baseline columns plus d-q extra columns. Across the q rows, the extras are disjoint within each column pair, so there are at most q extras in total. Hence

    q(d-q) <= q.

Because d>q is integral, necessarily

    d=q+1.                                           (4.3)

Moreover equality holds in the incidence count: every column pair has exactly one extra incidence, and every row has exactly one extra. The function f_G taking a row to the residue t of its extra column is consequently a bijection from G to Z/q.

## 5. Column norms and primitive cross-parity phases rule out q+1

Continue under the necessary configuration (4.3). For each column pair, its two column degrees within the even group are q and 1, and the same is true within the odd group. The full column degrees must both equal d=q+1 by D*D=dI.

If both parity groups had the same baseline column, those full degrees would be 2q and 2, impossible for q>=3. Thus the parity-group baseline columns are opposite in every pair. Let A_t be the even baseline and B_t the odd baseline in pair t. They are its two distinct columns.

Let f be the even-row extra-fiber bijection, and g the odd-row extra-fiber bijection. An even row e and an odd row o have exactly the two common columns

    B_(f(e)) and A_(g(o)).                            (5.1)

This assertion remains true when f(e)=g(o): in that case the two common columns are the two different columns in the same pair. If f(e)!=g(o), they lie in different pairs and remain distinct.

Fix an even row e. Of the q odd rows, exactly one, o=e+q modulo 2q, has row difference divisible by q. For each of the other q-1 odd rows, e-o is odd and not divisible by q, hence is a unit modulo 2q. The zero row Gram from (5.1) is a sum of two powers of the primitive root zeta^(e-o). Two such terms cancel if and only if their exponents differ by q modulo 2q. Since e-o is a unit, the two column indices themselves must differ by q. They must therefore belong to the same column pair, giving

    g(o)=f(e) for all q-1 of these odd rows.            (5.2)

But g is a bijection and q-1>=2. Equation (5.2) is impossible. This excludes d=q+1, and Section 4 already excluded every other q<d<2q.

Combining Sections 3-5 leaves only d=1,2,q,2q. This proves necessity for every odd prime q. Every use of the second Gram is explicit: row orthogonality and row norms come from DD*, while the critical complementary-baseline step uses all column norms from D*D. No induced object, quotient dimension, weighting assumption, or support-block premise is used.

## 6. Sufficiency in the original phases

For any divisor d of N, put m=N/d and define

    R[r,c]=1 iff floor(r/d)=c modulo m.

Every row and column has d entries. Within a row block, the supported columns have the form a+m k, 0<=k<d, and the row inner product is a unit scalar times a complete d-point character sum. It vanishes for distinct rows in that block; rows in different blocks have disjoint supports. Thus DD*=dI, and the square matrix also has D*D=dI. This is the already accepted complementary-divisor construction, restated to make the phase normalization explicit. It supplies d=1,2,q,2q.

## 7. Supplementary small-density theorem for every N=pq

**Lemma (binary two-prime vanishing sums).** Let p<q be primes. Index coefficients beta_ab in {0,1}, 0<=a<p and 0<=b<q, by the root chi(a,b)=zeta_p^a zeta_q^b. If

    sum_(a,b) beta_ab chi(a,b)=0,

then beta is a union of complete parallel p-lines or a union of complete parallel q-lines. In particular a nonempty vanishing binary sum has at least p terms.

For completeness, take the standard rational basis zeta_p^a zeta_q^b with a<p-1 and b<q-1 for Q(zeta_(pq)); its size is phi(pq)=(p-1)(q-1). Reducing the last row and column by 1+zeta_p+...+zeta_p^(p-1)=0 and its q analogue gives, for all a<p-1,b<q-1,

    beta_ab-beta_(a,q-1)-beta_(p-1,b)+beta_(p-1,q-1)=0.

Thus beta_ab=u_a+v_b for rational u_a,v_b, with suitable choices also on the last row and column. If both u and v were nonconstant, their differences would be nonzero integer differences of binary coefficients; each would have range at least one. The range of their sums would be at least two, contrary to beta being binary. Thus one coordinate function is constant, proving the parallel-line description. The standard cyclotomic degree statement is the only general cyclotomic-field fact used here; this supplementary lemma is not needed for the main 2q theorem.

Now let D be an original binary equality mask of order N=pq and 1<=d<q. In a group of q rows with the same residue modulo p, a nontrivial row difference has character order q. Its overlap coefficients in each residue modulo q are all equal. Since the overlap has fewer than q terms, it is empty. Those q rows therefore have disjoint supports, implying qd<=pq and d<=p.

If 1<d<p, take any two distinct rows. A nonzero difference has order p, q, or pq. Prime-order coefficient balance, or the binary two-prime lemma for order pq, shows that a nonempty vanishing overlap has at least p terms. Since every overlap has at most d<p terms, every pair of rows has disjoint supports. The N nonempty supports lie in N columns, so d=1, a contradiction. Thus d<q permits exactly d=1 or d=p, both supplied by Section 6.

This supplementary theorem does not settle any d>q at odd p. No claim that pairwise parallel directions synchronize globally is made.

## 7b. Supplementary upper-range theorem for every N=pq

**Theorem.** For any primes p<q, no binary Fourier equality mask has (p-1)q<d<pq.

For p=2 this was proved in Sections 4-5. Suppose p>=3. Partition rows by their residue modulo p. Each group has q rows. Two different rows in the same group have overlaps whose counts in the p-element column fibers

    F_t={c: c=t modulo q},  0<=t<q,

are equal, by prime-order q cancellation. Their overlap is greater than (p-2)q because 2d-pq>(p-2)q, and less than pq because d<pq. Hence it is exactly (p-1)q, with p-1 common columns in every fiber.

Fix a group and a fiber. Its q binary vectors of length p have pairwise dot product p-1. Every vector has weight at least p-1; at most one has weight p. All vectors of weight p-1 are identical, since two different (p-1)-subsets intersect in p-2 positions. Therefore all q rows contain a common (p-1)-element baseline in this fiber, with at most one extra occurrence of its omitted column.

Across all q fibers, each row has (p-1)q baseline entries and d-(p-1)q extras, and at most q extras are available across the group. Consequently

    q[d-(p-1)q] <= q,

so d=(p-1)q+1. Every row has exactly one extra, every fiber exactly one extra, and the row-to-extra-fiber map is a bijection in each group.

There are p row groups. In any fixed fiber and fixed column, let m be the number of groups whose baseline omits this column. Its total degree is

    (p-m)q+m = pq-m(q-1).

The required degree is d=pq-(q-1), forcing m=1. Thus the p groups omit distinct columns in every fiber.

Choose rows r,s from different groups and different residues modulo q. Such a pair exists: for any fixed row and another group, exactly one of the q rows is congruent to it modulo q. The difference r-s is a unit modulo pq. Their baseline supports intersect in exactly p-2 columns in every fiber. Each row's one extra column belongs to the other row's baseline in that fiber, since the omitted columns differ. Therefore the full common support has p-2 entries in every fiber, plus two distinct extra entries distributed over one or two fibers.

Since q>p>=3, at least one fiber receives no extra. Its count p-2 is strictly between 0 and p. The overlap cannot be a union of full p-lines, which would require every fiber count to be 0 or p. Nor can it be a union of full q-lines, since those have constant counts in all fibers while the extra entries make these counts unequal. The binary primitive-character lemma in Section 7 rules out its zero Gram. This contradiction proves the upper-range theorem.

This proves a second uniform exclusion interval; it does not resolve q<d<=(p-1)q for odd p.

## 8. Why naive weighted CRT descent remains unjustified

The accepted prime-power descent uses equal coefficients across a single lifted prime fiber. At a mixed order, even nonnegative smooth integer weights can cancel without being equal along either prime direction.

At order 6, under chi(a,b)=zeta_2^a zeta_3^b, take the coefficient grid

    beta = [[1,2,2], [2,3,3]]
         = u_a+v_b,  u=(0,1), v=(1,2,2).

Its primitive-character sum is exactly zero. Every nonzero coefficient is 2^k 3^l, but neither coordinate direction has equal coefficients on all its fibers. In ordinary exponent order the coefficients are (1,3,2,2,2,3). This invalidates a direct replacement of the prime-power coefficient-matching lemma by a prime-by-prime CRT assertion for the same weighted class.

This is a precise obstruction to that local inference, not a binary equality-mask counterexample, not a square two-Gram realization, and not a proof that a more refined mixed-prime descent is impossible. The row-norm integrality and both Grams may impose further structure. Any proposed extension must supply that additional argument, prove matched supports and equal amplitudes, verify square induced blocks, and retain all phases and permitted row weights. The 2q proof above avoids this obstruction by working entirely in the original unweighted class.

## 9. Fresh exact controls and original inverse model

The newly written standard-library checker `verify_mixedprime.py` imports or executes no historical code. It implements exact cyclotomic polynomial reduction, both full Gram orders, exact rational cyclotomic-field matrix inversion, the two-column classification, and degree-preserving negative controls. The accepted connected order-eight mask is copied literally as data and remains connected; its accepted odd CRT lift at N=24 is also retained. It is not forced into full square support components.

Positive masks include every divisor weight for selected N=2q and several odd pq orders. They corroborate phase normalization; they do not prove the infinite theorem. The q+1 baseline countercontrols pass every same-parity off-diagonal row Gram and all row/column degree conditions, yet fail a primitive cross-parity Gram exactly. General-pq upper-range countercontrols likewise pass every same-group row Gram and all degree conditions, while failing primitive cross-group Grams. They isolate the last essential obstruction in Section 5 instead of merely reporting a failed search.

For proper divisor controls and the connected (8,4) mask, the checker reconstructs the original minimizer. Write H[r,c]=zeta^(rc), A=H-D, B_tilde=A*/(N-d), and M_tilde=B_tilde^(-1). It verifies both inverse products, every inverse-row and inverse-column support count N-d, and both error Grams

    (M_tilde-H)*(M_tilde-H) = (M_tilde-H)(M_tilde-H)* = d I_N.

Thus M=M_tilde/sqrt(N), M^(-1)=sqrt(N) B_tilde, and the normalized squared spectral error is d/N in the original invertible, simultaneous inverse-row-sparsity model. No one-row relaxation, conditioning restriction, or modified target is substituted. Full exact matrices are retained for these original-model controls.

The generated `RESULTS.json`, `POSITIVE_MASKS.json`, `NEGATIVE_CONTROLS.json`, and `ORIGINAL_MODEL_CONTROLS.json` report the actual completed checks. The completed run passed 38 positive full-mask controls, 7 original-model inverse reconstructions, 5 two-prime q+1 countercontrols, 3 general-pq upper-branch countercontrols, and 5,440 elementary binary-vector configurations. It evaluated 22,215 row-Gram and 22,215 column-Gram entries, 14 full inverse products and 14 full error Grams. The proof is Sections 2-6, with the supplementary proofs in Sections 7 and 7b.

## 10. Scope and preserved accepted results

This candidate does not self-accept, change the owner, edit a registry/table/repository, or assert historical priority. M-SPARSE-DEFECT stays TO RESEARCH, priority 42. General mixed-prime divisibility remains open beyond the proved 2q and supplementary small-density/upper-range scopes. In particular no theorem for all p^a q, all odd pq at d>q, or all N follows.

Retain the accepted prime-power classification, connected (8,4) mask and (8m,4m) odd CRT family, necessary-and-sufficient equality criterion, all complementary-divisor cases, codimension-two and codimension-three classifications, even half-density optimum, strict singleton nonsharpness, and exact Delta_(3,1)=sqrt(3)/2. Retain the accepted general bound

    Delta_(N,N-d)^2 >= d/N + 1/[10 N d^(phi(N)-1)]

whenever no mask exists, and its accepted specialized refinements. Applying that existing bound at the newly excluded 2q weights gives

    Delta_(2q,2q-d)^2 >= d/(2q) + 1/[20 q d^(q-2)].

This is an inherited bound composed with the new exclusion, not a new gap formula or optimal rate. Remaining exact nonsharp optima, sharper/optimal gap rates, costs, stability, implementation and historical-priority questions remain open at their accepted scopes.

All input sources were read as data only and copied with SHA-256 bindings. No external writes or historical program execution occurred. Run `python verify_mixedprime.py` in this packet directory to reproduce its new exact outputs. `MANIFEST.json` binds the packet; `SEAL.sha256` binds its manifest.
