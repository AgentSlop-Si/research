# ALG-FIXED-PENCIL-CERTS: bounded primary comparison

Date: 2026-10-17. Status: completed author comparison; recommendation awaits independent review. No external write, theorem replay, new proof acceptance, or priority claim.

## Decision

The owner's final bounded comparison gate is exhausted by the named matches and qualified nonmatches below. Recommend **activity-only archival of the existing finite-certificate/comparison task, after independent acceptance of this comparison**. Retain the accepted six-size theorem as supporting finite evidence, at its existing rank and qualifications. This is neither worldwide novelty clearance nor standalone promotion.

The current stopping condition expressly allows an exact primary-theorem mapping **or a qualified nonmatch**. Both are now supplied: the individual Green kernel/cost and cross-ratio mechanism have explicit primary matches; broad factorization and modular algorithms have precisely delimited relations; none of the inspected primary results states the particular six-size, fixed-data exclusion. A reusable theorem increment remains necessary only if someone later proposes standalone novelty promotion. It is not an unfinished requirement of this finite certificate's accepted proof or its bounded comparison.

## 1. Exact target and identity

The target is **Theorem 37B**, not the neighboring all-length single-Green curvature Theorem 37A. Its accepted statement is inherited from the [fixed theorem](https://github.com/AgentSlop-Si/research/blob/5b49695e3d8b7b12ad841ad7b773d50088d30571/math/archive/objects/41/41e33de3d9eccd79df4ae2ff04f851eb52b0df0e584f36a3d83a08ae096b1bc4__THEOREM_1_.md) and [independent proof review](https://github.com/AgentSlop-Si/research/blob/5b49695e3d8b7b12ad841ad7b773d50088d30571/math/archive/objects/20/206c0390037a3185b57049d815524ca21d52ec7cacb7bed58e080958f649fcc4__REVIEW.md). Both source bodies were read and their recorded SHA-256 identities rechecked as text; historical certificate programs were not executed.

For each N in {4,8,16,32,64,128}, the circuit is

M_N(λ) = (G_0+w_A G_1) D_1 (G_2+λG_3) D_2 (G_4+w_C G_5),

G_s=(I−α_s W_s)^{-1},

α=((1+i)/4,(2+i)/7,(1+2i)/8,(1−i)/5,(2+i)/9,(1+i)/6),
w_A=(1+i)/3, w_C=(1−i)/4,
D_1[j]=i^{(3j+1) mod 4}, D_2[j]=i^{(j²+j+1) mod 4}.

The six W_s are the serialized, fixed Hamiltonian cycle orders identified in the source by seeded_cycles(N,37037). The source's immutable certificate data, not an arbitrary cycle with similar statistics, determine the instance. Every constant, cycle, and internal mask is fixed; only λ varies. External row/column permutations and arbitrary nonzero complex diagonal scalings are allowed.

Writing m_ab(λ) for an entry gives affine polynomials over Q(i). The two necessary equations are

f_j(λ)=(m_00 m_1j)^N−(m_0j m_10)^N=0, j=1,2.

Accepted certificates, in each of p=998244353 and p=2013265921, verify legal coefficient reduction, all Green denominator guards, deg(f_j)=deg(φ(f_j))=2N, and explicit polynomial identities uφ(f_1)+vφ(f_2)=1. The twelve checks exclude every complex λ at the six stated sizes. One good reduction suffices; two are corroboration. The accepted review reconstructs 2,040 f-coefficients. This comparison does not repeat that reconstruction.

## 2. Primary comparison: cyclic inverse and execution cost

**Huhtanen–Perämäki (2015), Proposition 2.5 and Theorem 2.9**, author manuscript pp.4 and 6, give O(n) factorization/storage for a nonsingular sum of two scaled permutations and the explicit inverse of I+DS. [Primary paper](https://math.aalto.fi/~mhuhtane/manu.pdf); [publication record, DOI 10.1007/s00041-015-9395-0](https://research.aalto.fi/fi/publications/factoring-matrices-into-the-product-of-circulant-and-diagonal-mat/).

Exact substitution: n=N, W_s=Q_s S Q_s^{-1}, D=−α_s I. Their formula becomes

G_s = Q_s [Σ_{k=0}^{N−1} α_s^k S^k /(1−α_s^N)] Q_s^{-1}.

This is the source Green kernel, with the same nonsingularity guard. Proposition 2.5 supplies the same linear-arithmetic primitive. This is an exact primitive/cost match, not an equivalence to the entire exclusion theorem.

**Theorem 4.3**, manuscript p.10, instead factors generic n×n matrices as (S−E_1)…(S−E_{n−1})E_n with freely chosen diagonal E_j; equation (1.2) converts to at most 2n−1 alternating diagonal/circulant factors. Its growing depth and free diagonals differ from six fixed resolvents, two fixed masks, and one λ. Generic existence neither guarantees this grammar contains Fourier nor proves it excludes Fourier. This is a qualified whole-theorem nonmatch.

## 3. Primary comparison: invariant, gauges, and necessary equations

**Ikuta–Munemasa (2015), introduction and §5**, arXiv v3 pp.1–2 and 18, define type-II equivalence using arbitrary invertible complex diagonal matrices and independent permutations, and the rational Haagerup set

H(W)={W_ab W_cd/(W_ad W_cb)}.

Equivalent matrices have identical H. Thus the denominator-ratio form and external gauge group match exactly. Their construction/classification concerns association-scheme matrices, not this Green pencil. [Primary paper](https://arxiv.org/pdf/1411.0057v3).

For the target, set (a,b,c,d)=(0,0,1,j). Direct substitution into the Fourier entries ω^{rc} gives the ratio ω^{(r_0−r_1)(c_0−c_j)}. Its Nth power is one regardless of the unknown permutations. Diagonal factors cancel. Clearing the denominator gives exactly f_j. This deduction does not require pencil members themselves to be type-II: every candidate equivalent to Fourier necessarily is. Zero-entry candidates cannot be Fourier-equivalent; clearing denominators cannot create a false exclusion. The invariant supplies a necessary condition only, never a sufficient Fourier-recognition test.

The paper attributes this invariant to Haagerup. This pass uses the fully accessible primary application above; it does not claim to have read Haagerup's 1997 original chapter or settled earliest priority.

## 4. Primary comparison: modular inference and certificate type

**Van Hoeij–Monagan (2002), Theorem 1 and modular algorithm step 4**, pp.5 and 7, establish a modular-GCD degree bound over number fields under their good-reduction/no-failure hypotheses. In particular, a modular output of 1 terminates the algorithm with characteristic-zero gcd 1. [Primary paper](https://www.cecm.sfu.ca/CAG/papers/hoeijmon.pdf); [author's publication list](https://www.math.fsu.edu/~hoeij/papers.html).

Map L=Q(i), x=λ, f_1,f_2 to the source's two degree-2N equations. The logical use of an exact modular gcd-one witness is classical. **Do not identify their algorithm with the stored certificates:** their reduction uses the full algebra F_p[z]/(z²+1), which splits for these primes; the source chooses a single root i↦j in F_p. Hence this is a related correctness-mechanism comparison, not a literal invocation of their Theorem 1 for that single component.

**Collins (1971)** supplies earlier primary evidence for exact modular resultant computation, using finite-field resultants and reconstruction. Only its publisher abstract was accessible here; no numbered theorem or full proof from Collins is claimed. [Publisher abstract](https://doi.org/10.1145/800204.806289).

### Exact bridge used by this target

The following is an explicit algebraic mapping of the already accepted proof, not a new priority claim. Let A be the finitely generated coefficient localization Z[i,S^{-1}] obtained by inverting the actual rational and Green denominators. The checks establish φ:A→F_p with i sent to a root of z²+1. There is no field homomorphism Q(i)→F_p; the localization and surviving denominators matter.

Because both degrees survive, the Sylvester matrix has the same size before and after φ. Determinants commute with a ring homomorphism, so

φ(Res_λ(f_1,f_2))=Res_λ(φ(f_1),φ(f_2)).

The stored Bézout identity makes the right side nonzero. Therefore the original resultant is nonzero in A and Q(i), so f_1 and f_2 have no common root over C. This is why one split residue component suffices despite the different ring used by van Hoeij–Monagan. The proof does not infer complex exclusion from merely finding no F_p-valued roots.

Distinguish three objects:

1. **Generic/existential algebra:** gcd 1 over Q(i) implies that some Q(i)[λ] Bézout coefficients exist by Euclidean algebra. This is not an exported rational coefficient array.
2. **Actual explicit evidence:** the retained finite-field coefficient arrays u,v and f_j, plus legal degree-preserving reduction, prove a characteristic-zero exclusion for the fixed rational-Gaussian input. Calling these explicit Q(i) Bézout arrays would overstate what is supplied.
3. **Restricted-grammar conclusion:** the certificate decides this particular one-parameter circuit at six sizes. It supplies no statement for all seeds, free masks, variable α_s, arbitrary sums of Greens, or all N.

## 5. Costs, reusable content, and final boundary

Per application, the accepted graph has six Green solves, two masks and **three** vector sums, with supplied cycle lists/constants. Its arithmetic cost is O(N); unknown λ does not change that count. This is a cost statement about evaluating the excluded candidate, not a DFT algorithm.

A constant number of basis-column applications produces the needed affine entries. Polynomial powering, gcd/Bézout construction and certificate checking are additional work on degree-2N polynomials. Neither the primitive O(N) count nor generic factorization grants O(N) certification, bit complexity, stable numerical implementation, or uniform parameter generation. Ordinary explicit application of n−1 sparse factors would already cost O(n²); the broad factorization theorem cannot be substituted as a constant-stage transform construction.

The reusable certificate recipe is: extract necessary monomial invariants, clear denominators, and certify gcd one in a good finite specialization with degree guards. The source-specific retained content is the fixed constants/orders, choice of two plaquettes, and successful six-size exact certificates. The inspected literature matches the ingredients but does not reproduce those six instance outcomes. No nonroutine reusable theorem increment beyond this finite application has been established in this comparison.

**What closes:** the finite instance's bounded model-matched comparison, keeping the previously accepted exclusion intact. **What does not close:** the source's wider Phase38 research direction concerning jointly tunable masks and noncommuting Green weights with a uniform, fully charged Fourier realization; other N/seeds/parameters remain excluded extensions. This report neither transfers those questions to a new owner nor claims they were solved. It recommends no new task merely to search indefinitely for priority. The finite owner can be archived as supporting evidence after comparison acceptance; any later standalone promotion would require a separately justified reusable increment and renewed scoped literature comparison.

## Inspection and access limits

Read in this pass: the complete retained theorem/review; relevant statements and proof passages of Huhtanen–Perämäki; Ikuta–Munemasa's equivalence definition and §5 invariant; van Hoeij–Monagan's Theorem 1 proof and stopping algorithm. Collins was abstract-only. Targeted phrase searches did not locate the exact six-instance result, but negative searches are not absence evidence and carry no novelty credit. No historical scripts, original certificate replay, full bibliography census, external editing, or global closure count was performed.
