# Independent review of the order-2q Fourier equality-mask theorem

Date: 2026-10-19 UTC.

## Verdict and exact binding

PASS for the complete order-2q theorem, the two supplementary pq exclusion results, and the retained exact witness data, within the scopes stated below. The proof requires no repair. This is an independent mathematical review with freshly written exact checks; the candidate checker was neither imported nor executed.

Reviewed frozen candidate:

- Directory: `/workspace/shared/sparse_mixedprime_2q_classification_20261019_1002`
- Manifest SHA-256: `e4fbbf3512c5093ae10247c74ba74fd0badb783af2a192945c4d3a3e435f0879`
- Report SHA-256: `a54b703ddab52ae93050b1c732c8f288e1b007b7378e4b6e3185ceeeb9e63708`

The independent checker verifies the seal, all 16 manifest entries, and the five source copies against both their recorded hashes and their original local source files. It repeats the integrity check after mathematical checks, establishing that the reviewed bytes did not change during the run.

The principal conclusion is exactly this: for every odd prime q, a binary matrix R of order N=2q with D[r,c]=R[r,c] zeta^(rc), zeta primitive of order N, and D*D=dI with d>0 exists if and only if d is 1, 2, q, or 2q. The diagonal Gram already makes d an integer. The theorem classifies possible weights, not every support pattern at an allowed weight.

## Independent proof audit: both Grams and all degree cases

Because D is square and D*D=dI with d>0, D is invertible and DD*=dI. Thus every row and every column of R has exactly d ones. This implication supplies row orthogonality without adding a hypothesis. The roles of row and column norms are kept separate below.

For distinct rows of the same parity, r-s=2h where h is nonzero modulo q. Consequently zeta^(r-s) is primitive of order q. Group the common support by the q fibers F_t={t,t+q}. The row inner product has integer coefficients b_t=|S_r intersect S_s intersect F_t| in {0,1,2}. The minimal polynomial 1+X+...+X^(q-1) forces all b_t equal. This conclusion concerns the exact individual fiber counts and includes zero coefficients; it is stronger than a divisibility claim about total overlap alone.

### The case 1<=d<q

Every same-parity pair has overlap size a multiple of q, bounded above by d<q, so the overlap is empty. The q even-row supports are pairwise disjoint subsets of 2q columns, each of size d. Hence qd<=2q and d<=2. As d is positive integral, precisely d=1 or 2 remains. There is no hidden exception at q=3.

### The case d=q

This value is an allowed divisor and is supplied by the explicit construction. No classification or reduction of all d=q masks is needed for a theorem about possible weights. In particular the upper-branch argument must not be applied with its strict positivity inequality weakened to equality; the candidate correctly does not do that.

### The case q<d<2q

Every two d-element row supports overlap, because 2d-2q>0. The common fiber coefficient is therefore nonzero. It cannot equal 2, since that would give a 2q-element intersection although d<2q. Thus every same-parity pair has exactly one common column in every fiber F_t.

Fix a parity group and a fiber. The q support restrictions are subsets of a two-element set, any two having intersection size one. None is empty; at most one is the full pair; and the two different singleton subsets cannot both occur. Since q>=3, at least two rows are singleton restrictions. Their common singleton is the unique baseline column, present in every row of the group. At most one row contains the other column.

This is a classification of q local binary restrictions, not a full-support-block assumption. Applying it independently to all q fibers gives q baseline entries in each row. A row needs d-q additional entries. There are at most q extra incidences in the entire parity group, so q(d-q)<=q. Since d>q, d=q+1. Equality in this count forces every row to have exactly one extra and every fiber to have exactly one extra incidence. Thus the map from the q rows to their extra-fiber labels is a bijection.

Now use the original column norms, an essential use of the other Gram. Within either parity group, the two column degrees of a fiber are q and 1. If both groups chose the same baseline column, the full column degrees would be 2q and 2, neither equal to q+1 for q>=3. The baseline choices must therefore be complementary.

Write A_t for the even baseline and B_t for the odd baseline, with {A_t,B_t}=F_t. If f(e) is the exceptional fiber of an even row and g(o) that of an odd row, their intersection is exactly {B_(f(e)), A_(g(o))}. The two displayed columns are distinct whether or not f(e)=g(o), and no further common column is omitted from this calculation.

Fix an even row e. Exactly one odd row, e+q modulo 2q, has row difference divisible by q. Every other odd row has a difference h coprime to 2q. For such a pair, the zero two-term inner product requires zeta^(h(c_1-c_2))=-1=zeta^q. Since h is a unit and every unit modulo 2q is odd, this is equivalent to c_1-c_2=q modulo 2q. Thus the two columns must be in the same fiber, requiring g(o)=f(e).

There are q-1>=2 such primitive odd partners, whereas g is injective. This is impossible. This step does not impose a primitive-character condition on the exceptional row e+q; that row is correctly excluded. It also does not assume cancellation merely from two columns having opposite ordinary parity. The actual phase requirement is antipodality modulo 2q.

For q=3 there are exactly two primitive odd partners, already enough for the contradiction. The entire open interval q<d<2q is excluded.

### The full boundary and sufficiency

For d=2q the full Fourier mask works. For each divisor d of N, put m=N/d and R[r,c]=1 exactly when floor(r/d) is congruent to c modulo m. Each row block consists of d consecutive row labels and uses one residue class of columns modulo m. Distinct row blocks have disjoint support. In a single row block, any nonzero row-label difference has magnitude less than d, and the row inner product is a scalar phase times a complete nontrivial d-th-root sum. Thus DD*=dI, and squareness gives D*D=dI. This verifies the construction in the original fixed phases and supplies all four allowed weights.

No induced square object, quotient, weighted matching class, or full-block decomposition of an arbitrary mask is used anywhere in necessity. In particular the accepted connected (8,4) example poses no conflict with this proof.

## Supplementary pq results

The frozen report also proves two additional statements for distinct primes p<q: weights d<q are exactly 1 and p, and no weight lies in (p-1)q<d<pq. Both proofs pass independent analytic review.

The auxiliary binary vanishing-sum lemma is valid. In product coordinates for the primitive pq character, reduction in the standard cyclotomic basis gives beta_ab=u_a+v_b. If both coordinate functions vary, each has a nonzero integer difference and hence range at least one. The range of their sums is then at least two, contradicting beta_ab in {0,1}. Thus the binary coefficient set is a union of complete parallel p-lines or complete parallel q-lines. Passing from product coordinates to the fixed primitive root only permutes labels by units in each prime coordinate, preserving these line families. This does not justify the same statement for weighted coefficients.

For d<q, the q rows in one residue class modulo p have disjoint supports and force d<=p. If 1<d<p, no pair of distinct rows can have a nonempty vanishing overlap: the character order is p, q, or pq, and in every case a nonempty binary vanishing sum has at least p terms. All N row supports would then be disjoint, forcing d<=1. The divisor construction realizes 1 and p.

For the upper interval, p=2 is already covered. Let p>=3. Same-group row overlaps are multiples of q, strictly larger than (p-2)q and smaller than pq, so they equal (p-1)q, with p-1 common entries in every p-element column fiber. In one fiber, all q restrictions share the same (p-1)-element baseline and at most one row is full. Counting extras forces d=(p-1)q+1 and exactly one extra per row and fiber. Full column degrees force every column to be omitted by exactly one of the p groups' baselines. Distinct groups therefore omit distinct columns in every fiber.

A pair of rows whose difference is primitive then has p-2 common baseline entries in every fiber, plus two distinct extra entries in at most two fibers. Such a pair exists. Since q>p>=3, an untouched fiber has a count strictly between zero and p, excluding a union of full p-lines. Touched and untouched fiber counts differ, excluding a union of full q-lines. The binary vanishing-sum lemma contradicts row orthogonality. This proves exactly the stated strict upper interval, without claiming its lower endpoint or the remaining odd-p interior.

The order-six weighted grid in Section 8 is a valid obstruction only to the naive coefficient-matching inference. Its ordinary-exponent coefficient vector (1,3,2,2,2,3) reduces to zero modulo Phi_6. It is not an equality mask and does not refute divisibility.

## Fresh exact checks

`independent_checks.py` was written specifically for this review. It uses only the Python standard library and reads the candidate's JSON as data. It generates cyclotomic polynomials by exact divisions of X^n-1, computes exact integer or rational residues, and independently evaluates both Gram orders. No candidate or historical module is imported or executed.

Completed checks, with full machine-readable results in `INDEPENDENT_RESULTS.json`:

1. All 38 retained positive masks pass both complete Grams, including every retained divisor case, the connected (8,4) mask, and its retained order-24 lift.
2. All eight retained upper-branch countercontrols have the stated regular degrees and zero same-group row Grams, but fail a primitive cross-group Gram. These include five q+1 examples at q=3,5,7,11,13 and three general-pq examples at (p,q)=(3,5),(3,7),(5,7).
3. All seven original-model matrix witnesses pass both inverse products, both error Grams, the exact relation B_tilde=(H-D)*/(N-d), the exact error relation E=M_tilde-H, and all inverse row and column support counts N-d. The checks use the supplied rational matrices but independently perform every product and compare each matrix entry. This verifies the original invertible simultaneous inverse-row model and its stated normalization, rather than only a mask surrogate.
4. A full labeled N=6 census, with no quotient by symmetry, gives numbers of equality masks for d=1,2,3,4,5,6 equal to 720,66,14,0,0,1. The search exhausts all constant-weight row supports, prunes only necessary exact row-orthogonality and final column-degree conditions, and verifies both complete Grams for every accepted mask. The census is an independent finite corroboration, not the infinite proof.
5. All 288 upper-branch q=3 configurations formed from arbitrary complementary baseline choices and both exceptional-fiber bijections satisfy all degree and same-parity conditions but fail a primitive cross-parity Gram.
6. Exhaustive local two-column checks at q=3,5,7 test 64,1,024,16,384 vectors-with-multiplicity configurations and accept respectively 8,12,16, exactly the claimed baseline form.
7. Exhaustive binary primitive vanishing-sum checks at pq=6,10,15 test all 64,1,024,32,768 supports. Every zero sum has one of the two parallel-line forms. The counts are respectively 10,34,38, agreeing with 2^p+2^q-2.
8. The weighted order-six cancellation is verified exactly.

The final run has empty standard error and all assertions pass. The candidate packet remains byte-identical to its seal.

## Original-model consequence and limits

Composing the reviewed mask theorem with the separately accepted equality criterion gives Delta_(2q,2q-d)=sqrt(d/(2q)) exactly for d in {1,2,q}, within 1<=d<2q. The full-mask d=2q case is not an inverse-row problem at s=0; its admissible invertible class would be empty. The report preserves this boundary correctly.

The displayed quantitative exclusion bound is a correct substitution into the inherited bound: phi(2q)=q-1, so 1/[10 N d^(phi(N)-1)] becomes 1/[20 q d^(q-2)]. This review verifies that substitution and the new no-mask hypotheses. It does not claim to reprove or improve the inherited gap estimate.

General mixed-prime divisibility is still open outside the proved scopes. In particular no conclusion for all p^a q, all odd-p semiprime interior weights, or all N follows. The owner remains TO RESEARCH, priority 42; no owner status, registry, spreadsheet, or repository was modified. No novelty or historical-priority claim is made.

No external state was changed. All writes were confined to this independent local review directory.
