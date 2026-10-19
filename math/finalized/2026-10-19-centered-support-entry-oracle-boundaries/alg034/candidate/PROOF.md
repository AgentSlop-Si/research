# ALG-034: a sharp-order centered sparse-output obstruction

19 October 2026 UTC. Source-bound author result; independent review not yet performed.

## 1. Selected remaining gate and its exact boundary

The current owner record asks for a broader centered-source supplier or a quantitatively stronger variation-to-energy supplier, with all recognition, precision, replay, median and outer charges. Its latest accepted source is the nonconstant bounded-variation construction. That construction's fixed working precision, q-dependent costs, full nonconstant fixture, source replay and finite implementation ceilings are already accepted. They are not new results here.

This note tests the following particular proposed extension, rather than attributing it to the accepted theorem:

> Extend the same centered-target error contract to every canonical Gaussian-dyadic original, while retaining the bounded-variation family's O(M^(1/4)) explicit candidate-list size (or that size times a fixed polynomial in log M).

This extension is impossible. A normalized, exactly dyadic comb family needs Omega(M^(1/2)) retained coordinates. The same obstruction holds for the outer theorem's weaker constant-four tolerance. Parseval supplies the matching order as a representation-existence bound; it supplies no efficient heavy-coordinate discovery algorithm.

The comb transform identity is the classical roots-of-unity/geometric-sum mechanism, and the representation upper bound is the classical Parseval/energy-counting argument. Neither mechanism is new. The contribution here is their exact, source-bound specialization to this accepted centered-target interface, finite-grid representation and complete cost boundary; no historical novelty is claimed.

The bound concerns explicit retained Fourier coordinates under the specified approximation contract. It is not a lower bound on general Fourier algorithms, original-target approximation without this intermediate contract, all-length transform existence, or the accepted outer reconstruction. The accepted all-length source hypothesis allows O(M^(1/2+beta)) candidates, which is O(M^(3/4)) at beta=1/4 and is not contradicted. ALG-034 remains open.

### Source binding and prior completed work

`sources/OWNER_RECORD.json` preserves the current ALG-034 row recovered from the local verified index response used by the parent. `SOURCE_BINDINGS.json` binds the response and the source snapshots. All 37 members of the accepted BV candidate manifest were verified before copying dependencies; its manifest SHA-256 is

    34cb8b6977c3c5b9ce89ad786628e5cf97a2be49a3d11312fccf5433335c0ac6.

The accepted provider SHA-256 is

    c74c9aaa400f182b381897e80ea74724e6843720b1e44d8572554508fa1c3715.

Primary accepted source and independent review:

- https://github.com/AgentSlop-Si/research/blob/081a311d3e3486071ff89502a412974001a78ae1/math/finalized/2026-10-18-nextcycle-six-outcomes-1347/centered_bv/candidate/PROOF.md
- https://github.com/AgentSlop-Si/research/blob/081a311d3e3486071ff89502a412974001a78ae1/math/finalized/2026-10-18-nextcycle-six-outcomes-1347/centered_bv/review/REVIEW.md

This is distinct from the earlier exact-centered-support lower bound M-N+1: that result concerns exact support and the mismatch with the original sparse supplier. Here the returned approximation may discard most exact coefficients, and the lower bound follows from coefficients strictly above a positive error tolerance. It also does not repeat the accepted Q=P+2m+ceil(log2(q+1))+20 precision proof or the existing q=N warning. The latter are preserved as dependencies.

## 2. Computational and target model

Keep the accepted negative unitary transform

    (U_L x)_k = L^(-1/2) sum_j x_j exp(-2 pi i j k/L).

Let M=2^m, N=M/4, a0=floor((N-1)/2), and let J_N place original coordinate j at residue j-a0 modulo M. The actual original is c_j 2^(-F), with canonical Gaussian-integer c_j. Its accepted normalization uses E=sum |c_j|^2, h=ceil(log2 sqrt(E)), u=c/2^h, R=||u||_2, and sigma=h-F. The required centered target remains

    z=U_M J_N u.

The output is a finite explicit list of distinct candidate locations with Cartesian P-grid coefficients, P=16m+16; unspecified coordinates are zero. Zero-valued retained records are permitted but remain charged. This is the existing sparse-output interface, not a compressed formula for a whole Fourier vector.

Write lambda for the tolerance multiplier, unrelated to the normalization scale. We treat lambda=1 for the accepted BV supplier and lambda=4 for the accepted outer premise:

    ||Z-z||_infinity <= lambda R M^(-1/4).                 (1)

The lower bound permits arbitrarily accurate real or complex retained values and arbitrary choice of support. Consequently it also applies at the accepted finite grid, under randomized choices, and regardless of arithmetic implementation.

## 3. Exact dyadic-comb construction

Let lambda=2^a, where a=0 or 2. For any integer r>=a+3, put

    m=4r, M=2^(4r), N=2^(4r-2),
    K=2^(2r-4-2a) = sqrt(M)/(16 lambda^2),
    J=N/K=2^(2r+2+2a), h=r+1+a.

The letter K here counts required coordinates; it is not the inherited low-frequency cutoff. K>=4, J is a square, and sqrt(J)=2^h. Define the actual original by

    c_j=1 when j is a multiple of K; c_j=0 otherwise,
    F=h, u0_j=c_j 2^(-h).

There are exactly J ones at j=0,K,...,(J-1)K. This is canonical common-grid input, since it has odd nonzero integer coefficients. Its exact energy is E=J, normalization is the accepted h, R=1, and sigma=h-F=0. No irrational original, unbounded amplitude, large scale shift or unstated input oracle is used.

For each ell=0,...,K-1, select

    k_ell=(M/K)ell.

Directly from the centered transform definition,

    z_(k_ell)
       = 2^(-h) M^(-1/2)
           sum_(b=0)^(J-1) exp(2 pi i (a0-bK)k_ell/M)
       = J 2^(-h) M^(-1/2) exp(2 pi i a0 ell/K).

Every summand's b-dependent phase is one. N/2 is divisible by K, so a0=N/2-1 is congruent to -1 modulo K. Therefore

    z_(k_ell)=A exp(-2 pi i ell/K),
    A=sqrt(J/M)=2^(1+a-r)=2 lambda M^(-1/4).            (2)

These are K distinct centered-target coordinates, all strictly twice the allowed error in (1).

### Theorem: mandatory retained coordinates

Every Z satisfying (1) must retain every k_ell and assign it a nonzero value. If a coordinate is omitted, Z_(k_ell)=0 and (2) gives error exactly 2 lambda M^(-1/4), which is larger than the permitted lambda M^(-1/4). A retained zero fails in the same way. Hence

    |supp(Z)| >= K = sqrt(M)/(16 lambda^2).             (3)

In particular, the original supplier tolerance forces at least sqrt(M)/16 coordinates; the weaker outer tolerance forces at least sqrt(M)/256. This statement holds along the explicit infinite family M=2^(4r), which is sufficient to refute a uniform O(M^(1/4) poly(log M)) size guarantee for arbitrary originals.

The bound is deterministic and information-theoretic within this output interface. If every tape emits fewer than K distinct nonzero coordinates, the simultaneous event (1) has probability zero on this input. Independent reruns cannot justify amplification of a nonexistent single-run event. A new scheme combining r_run lists could only succeed if their effective retained union contains all K required coordinates; it would need its own correctness theorem and all r_run runs, union construction, comparisons, median and replay costs. No blanket impossibility of such a larger scheme is asserted.

Strict inequality matters. A coefficient equal to the error threshold need not be retained. The construction uses a factor-two gap, and the checks include the equality endpoint to prevent a spurious greater-than-or-equal counting argument.

## 4. Sharp order as a representation result, not a recovery algorithm

For every normalized source u, unitarity gives sum_k |z_k|^2=R^2. For epsilon=lambda R M^(-1/4), define H={k:|z_k|>epsilon}. Then

    |H| epsilon^2 < R^2,
    |H| < sqrt(M)/lambda^2.

Keep H and round each retained real and imaginary component to the nearest P-grid point. The complex rounding error is at most 2^(-P)/sqrt(2), smaller than epsilon in the admitted domain R>1/2, m>=11. Omitted values have magnitude at most epsilon; thus (1) holds. The rounded retained amplitudes also satisfy the accepted every-tape cap, since |z_k|<=R<=1 and the rounding perturbation is tiny.

Together with (3), this proves sharp worst-case order Theta(sqrt(M)) for the size of an explicit P-grid approximation under the fixed-lambda centered contract, along the displayed length family. The upper bound is an existence argument using the true z and its exact heavy set. It neither computes z nor gives a comparison algorithm at the threshold. It must not be advertised as an efficient supplier or as free preprocessing.

The original-source transform of this particular comb has a simple explicit form. Exploiting that special form would be a different supplier or a special-case algorithm, not an implementation of the existing bounded-variation evaluator or a resolution of arbitrary-original recovery.

## 5. Why merely lifting the existing BV caps fails

The original has q=2J maximal constant blocks: a unit-length one block followed by a K-1 zero block, repeated J times. Its zero-extended Cartesian variation and energy are

    B=2J, E=J.

The accepted variation factor is exactly

    C=ceil sqrt(N B^2/(4E))=sqrt(NJ)=2^(3r+a).

This is much larger than the accepted fixed budget C<=8; q also exceeds the finite q<=64 ceiling. Thus this family does not refute or contradict the accepted BV theorem.

If one only raises those engineering/family caps and retains the same variation-based cutoff formula, T=2^ceil(m/4)=2^r gives

    K_BV=C T=lambda M.

The inherited sparse guard requires K_BV<M/2, which fails even for lambda=1. This failure precedes pi/root setup and coefficient construction in the source path. It cannot be repaired by increasing working precision or widening a numerical radius certificate. A different support selector, a different source premise, or a correctly paid same-target fallback is needed.

The retained executable evidence demonstrates exactly this boundary. On the M=4096, N=1024, lambda=1 example, the unmodified default dense provider reads every original coordinate and rejects its block-count ceiling; the default block-input provider rejects the descriptor count. Separate explicitly labeled recognition-only calls raise the two relevant caps and recover E=256, B=512, C=512, q=512, h=4 and sigma=0. The unchanged cutoff formula is then 4096, violating the strict Nyquist guard. Those diagnostic calls do not modify the source, run a larger producer, or claim an extended accepted numerical domain.

## 6. Precision, setup, replay and full reconstruction ledger

The following counts stay in the accepted binary arithmetic/control model and explicit record representation. They do not convert an inherited conservative upper bound into a new lower bound or a measured speed statement.

### Required coefficient representation

On the comb, every retained required value obeys

    |Z_(k_ell)| >= |z_(k_ell)|-epsilon = lambda 2^(-r).

Writing Z=(x+iy)/2^P, at least one Cartesian numerator satisfies

    max(|x|,|y|) >= 2^(P+a-r)/sqrt(2).

Its ordinary magnitude bit length is at least P+a-r. Since P=64r+16, this is 63r+16+a=Theta(m). Thus the required nonzero coefficient magnitudes alone need at least

    K(P+a-r)=Omega(sqrt(M) m)

bits in this explicit integer-list representation. Location records, signs, other Cartesian components, list structure and source association are additional. A compressed symbolic comb descriptor is not this interface. The count does not assume every stored field has its maximum possible width.

### Recognition and original binding

A supplied dense original entails the existing full N-coordinate recognition and binding pass; this is a source-association requirement, not a new lower bound on every conceivable approximation method. In the comb the raw Cartesian values are 0 or 1, the exponent h is O(m), and all address/count widths must still be paid. The canonical supplied block descriptor has q=2J records and is separately charged without pretending to read N entries. Any new shorter comb grammar would be a changed input interface and require its own recognition/binding contract.

The default-provider failed prefix in the finite check includes all N=1024 dense visits and no scalar preparation or outputs. Its complete receipt is retained in CHECK_RESULTS.json. A rejected prefix followed by dense fallback adds the complete same-target dense cost; it is never reset.

### Source preparation and replay

For a hypothetical successful replacement supplier, its full source reading, normalization, coefficient-selection work, pi/root or other scalar preparation, retained values, certificates and output records must be charged. No lower bound here supplies these algorithms or receipts. The existing BV cost remains O(N L^6+q S L^7) for a dense source and O(q L^6+q S L^7) for a supplied block source, with its actual L, history restrictions and guarded domain. We do not plug the rejected comb into that success bound as if production had occurred.

An actual full source replay adds the entire replacement production cost again and its strict structural/numerical comparisons. The source/row adapter, median construction and mandatory median replay retain their original-row storage and actual H-dependent charges from OUTER_COST_ERRATUM.md. Arbitrary earlier history cannot be replaced by an m-only shorthand. The finite diagnostic program performs no successful provider replay, median or outer execution, and claims none.

### Unchanged outer reconstruction

For D=5 and m=4r the accepted values are

    t=160m+4, eta=2^(-8m), p=8m+3,
    b=ceil(9m/4)=9r, P=16m+16, sigma=0.

The t<M guard holds for our r. Because N=M/4 and t is a multiple of four, every retained column has exactly Nt/M=t/4=40m+1 distinct row incidences in the accepted iterator. Therefore any list meeting (1) on the comb would force at least

    E_outer=K(40m+1)=Omega(sqrt(M) m)

coefficient evaluations in that unchanged complete iterator. Extra retained positions add their incidences. This is an exact algorithm-specific count; no FFT-wide operation lower bound follows. Zero-valued retained records cannot avoid its charged coefficient loop.

The inherited scalar implementation pays one lazy pi/root preparation when E_outer>0, each coefficient evaluation and complex certificate, exact scatter, all N initializations, all N final rounds and all N output records. Its fixed-parameter complete bound, additional to producer/replay prefixes, remains

    O((N+S+E_outer+1)m^2
       + 1_(E_outer>0)m^5 + E_outer m^5),

with actual H replacing the m-only control shorthand when the accepted width/history hypotheses do not hold. Its peak data include N accumulators, N output records, retained median rows/candidate records, endpoint state and scalar scratch. The inherited bound is not a new saving or a claim that the hypothetical supplier exists.

The new support lower bound is sublinear in N up to fixed powers of m, while the reconstruction already writes N outputs. Accordingly it does not rule out the intended linear-word asymptotic outer stage, near-linear algorithms by other routes, or the larger O(M^(3/4)) source support allowance. It only rules out retaining the special BV O(M^(1/4)) candidate budget for arbitrary originals at this same intermediate accuracy.

## 7. Reproducible exact checks and stopping point

Run `python check_obstruction.py` from this directory. It uses integer and Fraction arithmetic only and verifies all copied source hashes before importing the unchanged recognition code.

The fresh run performs:

- 34 exact parameter/precision/cutoff plans, with largest m=1024; these are symbolic integer plans, not numerical transforms at those lengths.
- 24 selected centered-target coefficients across three finite fixtures, by literal summation of 279,552 original-coordinate terms in the exact cyclotomic quotient Z[X]/(X^(M/2)+1). This includes the lambda=4 fixture.
- Every row of the original alias grid k=4 ell for the M=4096 example: 1024 rows and 262,144 original-coordinate terms, identifying exactly the four necessary selected nonzero alias rows.
- Four single-coordinate omissions, a wrong-location substitution, an exact numerator-width inequality, and the strict-threshold equality control.
- Two original default-provider rejection paths with complete paid-prefix receipts, and two explicitly labeled recognition-only cap-override diagnostics. No coefficient construction or new full outer run is claimed.

Cyclotomic reduction is exact for powers of two. The direct sums include the original centering offset; they do not calculate an unrelated uncentered transform or reuse the production block formula. The checked selected-coordinate success of an exact sparse test list is not asserted to be a complete centered-spectrum recovery success. Analytic proofs, rather than finite checks alone, establish the infinite-family lower and representation upper bounds.

This closes the chosen impossibility test for an arbitrary-original extension retaining O(M^(1/4) poly(log M)) explicit candidates. It leaves open an efficiently constructed general centered supplier with a larger support budget, full same-source measurements/recovery, independently justified amplification, complete bit/setup/replay costs and a same-target all-length dispatcher. It leaves structured families with additional hypotheses open. It neither closes ALG-034 nor changes the accepted BV result, scores, tables or repository. No external write was performed.
