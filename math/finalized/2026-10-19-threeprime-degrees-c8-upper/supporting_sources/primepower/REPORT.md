# Prime-power classification of binary Fourier equality masks

Date: 19 October 2026 (UTC). Owner M-SPARSE-DEFECT; priority 42.
Status: new proof candidate, pending independent review. Do not self-close the owner.

## 1. Result and exact scope

**Theorem.** Let p be prime, a >= 1, N = p^a, and let zeta be any primitive N-th complex root. If R is a binary N by N matrix and

    D[r,c] = R[r,c] zeta^(rc),       D* D = d I_N,

where 1 <= d <= N, then d = p^b for an integer 0 <= b <= a.
Conversely every such d has a mask. In the proper range d < N, necessarily b < a.

The proof below is uniform in both p and a. It does not assume that R is a union of full square support blocks, and retains the original character phases. It explicitly accommodates the accepted connected (N,d) = (8,4) counterexample to that proposed block reduction.

Together with the accepted necessary-and-sufficient equality criterion and divisor construction, this proves exactly

    Delta_(p^a, p^a-d) = sqrt(d/p^a)   iff   d = p^b, 0 <= b < a.

For every other integer 1 <= d < p^a, the strict inequality

    Delta_(p^a, p^a-d) > sqrt(d/p^a)

follows from the accepted compactness/attainment argument. No quantitative strict gap, exact nonsharp optimum, mixed-prime necessity, runtime claim, or whole-owner closure follows.

The new ingredient is a weighted character-filtration descent. Its auxiliary square matrices can have repeated row labels, repeated column labels, varying row amplitudes, and dimensions unrelated to their character order. These freedoms are essential to justify the induced objects.

## 2. Cyclotomic coefficient lemma

For a >= 1 write L = p^a and n = p^(a-1). If rational numbers beta_x, 0 <= x < L, satisfy

    sum_x beta_x zeta^(h x) = 0,       gcd(h,p) = 1,

then, for each u in {0,...,n-1},

    beta_u = beta_(u+n) = ... = beta_(u+(p-1)n).                 (2.1)

Indeed zeta^h is primitive and its minimal polynomial is

    Phi_L(X) = 1 + X^n + ... + X^((p-1)n).

A polynomial of degree less than L that vanishes there is Phi_L times a polynomial of degree less than n. Comparing coefficients proves (2.1), including zero coefficients. Conversely (2.1) gives the vanishing sum. The standard prime-power cyclotomic formula follows from (X^L-1)/(X^n-1); irreducibility follows by Eisenstein after X -> X+1. Equivalently, modulo p this substituted polynomial is X^((p-1)n), and its constant term is p, not a multiple of p^2.

This is a statement about exact rational coefficients, not a numerical cancellation test.

## 3. The closed class used for descent

Fix p. At character level a >= 0 consider a nonempty square matrix A of size m, with arbitrary labels

    x_i, y_j in Z/(p^a),          1 <= i,j <= m,

arbitrary integers k_i >= 0, and a binary support matrix T, such that

    A[i,j] = p^(k_i/2) T[i,j] zeta_a^(x_i y_j),
    A* A = A A* = d I_m.                                      (3.1)

At a = 0, the cyclic group is trivial and zeta_0 = 1. Repeated labels are expressly allowed. The common d is the same throughout the descent. The initial Fourier mask is in this class with m = N, k_i = 0, x_i = i, y_j = j. Its second Gram follows from the first because the matrix is square and d > 0.

Each row is nonzero. Its support S_i has

    p^k_i |S_i| = d.                                          (3.2)

Two different rows with the same label x have disjoint supports: their inner product is the positive scalar p^((k_i+k_l)/2) times |S_i intersect S_l|, so (3.1) forces that intersection to be empty. Therefore, for any fixed pair of columns, at most one row of any given label can meet both columns.

These observations are also valid when the row amplitudes differ.

## 4. Support-matching lemma at one character level

Assume a >= 1, L = p^a, n = L/p. Partition columns by y_j modulo p. Call a row pure if all its neighbors lie in one such residue class; call it mixed otherwise.

**Lemma.** Every mixed row belongs to a unique p-tuple of rows with:

- labels u, u+n, ..., u+(p-1)n for some 0 <= u < n;
- precisely the same support S;
- precisely the same amplitude p^(k/2).

Distinct such p-tuples are disjoint as sets of rows. Moreover S contains the same positive number of columns in each residue class modulo p.

**Proof of matching, without a degree or quotient assumption.** Let i be a mixed row. Choose two columns j_0,j_1 in its support whose labels have different residues modulo p. For any such pair j,l, its column inner product is

    sum_r p^k_r T[r,j] T[r,l] zeta_a^(x_r (y_l-y_j)) = 0.

The difference y_l-y_j is a unit modulo p. Aggregate by the exact row label x:

    beta_x = sum_(r:x_r=x) p^k_r T[r,j] T[r,l].

The same-label disjointness from Section 3 means beta_x is either zero or exactly one row weight p^k_r. The cyclotomic lemma says these coefficients are equal across each p-element lifted label fiber. Thus, if one row contains j and l, there is exactly one row at every sibling label containing both, and all these rows have equal weight.

Apply this to the two anchor columns j_0,j_1. For each sibling label obtain a unique row i_q containing both anchors. To see that i_q contains every j in S_i, choose one anchor whose residue differs from that of j. Applying the pair argument to j and that anchor produces a row at the sibling label. It must be i_q, since two rows with that same label cannot both contain the anchor. Hence S_i is contained in S_(i_q).

Conversely, for any l in S_(i_q), choose an anchor of different residue. Apply the same argument back at the original label. The resulting row must be i, again by same-label disjointness. Hence l belongs to S_i. The supports are therefore exactly equal. The anchor-pair coefficients already gave equality of their weights. Uniqueness at each label gives a partition of all mixed rows into disjoint p-tuples.

Finally, let b_t be the number of columns of this common support whose label is t modulo p. Orthogonality of two tuple rows with distinct lifted labels gives

    sum_(t=0)^(p-1) b_t omega^((q-q')t) = 0,
    omega = zeta_a^n.

Taking q-q' = 1 already forces all b_t equal by the degree-(p-1) cyclotomic relation. The common value is positive because the support is nonempty. Thus the support has size p b_0. This finishes the lemma.

In particular, the matching is deduced from BOTH Gram identities. A proof based only on column intersections would lack the same-label disjointness and could not infer the matching rows.

## 5. Legitimate weighted descent, including dimensions

For each matched p-tuple, order its rows by q = 0,...,p-1. Their common weight is p^k and their entries are

    p^(k/2) T[j] zeta_a^(u y_j) omega^(q y_j).

Apply the unitary p-point row Fourier transform with entries

    p^(-1/2) omega^(-t q),       0 <= t,q < p.

The new row indexed t has entries

    p^((k+1)/2) T[j] zeta_a^(u y_j) 1_(y_j = t mod p).        (5.1)

It is nonzero by the support-matching lemma. All these transformations act on disjoint row tuples. Leave pure rows unchanged. The resulting entire matrix still has both Grams dI. Every resulting row is supported in exactly one column residue class modulo p.

Permute rows and columns to group these residue classes. The matrix becomes a direct sum of possibly initially rectangular blocks, with r_t rows and c_t columns. Each block B_t satisfies

    B_t B_t* = d I_(r_t),       B_t* B_t = d I_(c_t).

Consequently r_t <= c_t and c_t <= r_t, so r_t = c_t. Empty blocks may be discarded; every remaining block is square. No dimension equality has been assumed from the mask alone.

For a block t write every column label as y_j = t + p y'_j with 0 <= y'_j < n. A pure original row of label x_i has entries

    p^(k_i/2) T[i,j] zeta_a^(x_i t) (zeta_a^p)^(x_i y'_j).

Multiply this row by the unit scalar zeta_a^(-x_i t). It now has precisely the character form at order n with row label x_i mod n and unchanged exponent k_i.

A transformed row from (5.1) has the same form after multiplication by zeta_a^(-u t), with row label u and new exponent k+1. Therefore each nonempty square block is again in the class (3.1), at level a-1, using the primitive root zeta_(a-1) = zeta_a^p. Row labels or column labels may coincide after descent, and that is permitted by Section 3. The masks remain binary. Squared row amplitudes remain integer powers of p. The common d is unchanged.

This proves the claimed induced subspaces, their dimensions, their character phases, and their integral weight exponents. It is a unitary change of row basis followed by an exact direct-sum decomposition; it is not a quotient of the original binary mask into full blocks.

## 6. Termination and the necessity theorem

Iterate the descent on every nonempty block until character level zero. Exactly one character level is removed at every step, so this ends after a levels, regardless of the block sizes.

At level zero every matrix entry is nonnegative real, of the form p^(k_i/2) T[i,j]. Its different rows are orthogonal, hence have disjoint supports. It is a nonempty square invertible matrix, so there are as many disjoint nonempty row supports as columns. Each row support must therefore be a singleton. Equation (3.2) becomes

    d = p^k_i.

For an original unweighted Fourier mask all initial exponents are zero, and each level either leaves an exponent unchanged or increments it once. Thus every terminal exponent lies between 0 and a. At least one terminal row exists, and the common d gives d = p^b with 0 <= b <= a. If d < p^a, then b < a.

This proves the uniform necessity theorem. Divisor sufficiency is the accepted construction from the pinned equality-criterion report. Combining necessity and sufficiency gives Section 1.

An equivalent structural description is a finite character-splitting tree with p-point Fourier transforms on precisely matched row tuples. Every terminal row arising from an initial exponent-zero matrix has accumulated exactly b weight increments. This permits connected support graphs and genuinely nonrectangular initial masks.

## 7. Exact checks and retained positive control

`verify_primepower.py` is newly written for this packet, imports no historical program, uses the Python standard library, and performs exact integer cyclotomic reduction for both Gram orders at every stage of the descent. Its coefficient checker uses the direct exponent formula separately for rows and columns. Its descent implementation verifies the matching lemma, balance, new square-block dimensions, every new Gram, and singleton terminal supports. It additionally checks the original inverse minimizer by exact rational field arithmetic on the connected order-eight control.

The literal connected order-eight mask is copied as data from the accepted source report, not imported from historical code. Its original support graph remains connected; the checker verifies all 128 original Gram entries, then its weighted descent. It is explicitly NOT forced into two full 4 by 4 support components. Positive-control divisor masks at several prime-power orders exercise pure and mixed levels, different primes, nontrivial depths, d=1, intermediate powers, and the full d=N boundary. These checks corroborate the formulas and implementation; the all-size proof is Sections 2-6, not a finite census.

Negative controls alter the connected mask by a degree-preserving switch and corrupt an induced row weight. Both must fail the complete exact Gram validator. The checker also verifies the cyclotomic coefficient lemma against freshly generated exact vanishing-coefficient examples and rejects an intentionally unbalanced fiber.

The passing run checks 55 positive divisor controls, the connected (8,4) control, and a 16-by-16 direct-sum control at character order 8 with repeated row and column labels. It verifies 275,704 full Gram entries across all descent states, 89 cyclotomic vanishing controls, the direct p-point transformation and dephasing identities, and the original connected inverse witness. The actual test counts and descent records are retained in `RESULTS.json` and `DESCENT_CERTIFICATES.json`. The inverse witness is retained in `CONNECTED_INVERSE_WITNESS.json`.

## 8. Remaining obligation, scope, and source binding

There is no further mathematical lemma required for the prime-power conclusion if the matching lemma and weighted induction above pass independent review. The remaining acceptance obligation is independent verification of those arguments and the fresh exact artifacts. This packet does not self-accept or update any owner, status, priority, registry, spreadsheet, or repository.

The next unresolved arithmetic question is mixed-prime necessity: whether any mask exists with d not dividing N when N has at least two distinct prime factors. The prime-power coefficient matching used here is not asserted at mixed-prime order. All nonsharp exact optimum values and quantitative strict gaps also remain open.

Pinned source copies and their SHA-256 bindings are in `sources/` and `SOURCE_BINDINGS.json`. The accepted connected-control report and independent review remain unchanged. The immutable accepted latest report is
https://github.com/AgentSlop-Si/research/blob/7769fb444edb0b63ebbce7e31dc52966ba08f4f0/math/finalized/2026-10-18-sixth-cycle-six-results/sparse_divisibility/candidate/REPORT.md .

No external state was changed. No historical checker, solver, or historical research program was executed. Run the new checker with `python verify_primepower.py` from this directory. `MANIFEST.json` binds all frozen packet files except itself and the final seal.
