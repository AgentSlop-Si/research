# Review of the generic FFT fusion barrier

Review date: 2026-10-12 UTC. The author labels the source 2026-10-13; this is its document date, not the retrieval or review date.

## Decision

ACCEPT the two restricted generic-input support obstructions and the WDRR exact-row implication, with the hypotheses and wording corrections below. The supplied finite certificate also passes a fresh independent exact check. REFUTE any promotion of these results to an unrestricted Fourier lower bound, an impossibility of a cheap WDRR base, or a construction of a faster all-input FFT. Existing implementation, uniform scalar-DAG, and whole-target resource gates remain open.

The proof review is self-contained. The underlying review did not execute an imported author program. This publication derivative contains prose and verification metadata only.

## Source citations

The reviewed source is RESEARCH(1).md and its byte-identical RESEARCH.md member of FFT_Generic_Fusion_Gate_2026-10-13.zip. The note and archive are bound by exact names, byte counts and SHA-256 in [Source citations](SOURCE_CITATIONS.json). The source's future-dated filename is retained verbatim; the review date is 12 October 2026.

## Definitions that must accompany the accepted claims

Work over the complex numbers. For an integer N >= 1, let X be the cyclic shift defined by X e_j = e_(j+1 mod N), and let C_x[i,j] = x[(i-j) mod N]. In the Weyl result N >= 2, omega is a primitive Nth root, and Z e_j = omega^j e_j. Take an integer divisor m of N with 1 <= m < N, and an integer ell >= 0.

The t-tap vector is p in C^N with precisely t nonzero entries, 1 <= t <= N. P(X) means sum from j=0 to N-1 of p_j X^j. If a polynomial is initially supplied with other exponents, its coefficients must first be combined modulo X^N-1; t counts the nonzero resulting residues. A formally nonzero polynomial is not enough: P(T)=T^N-1 has two formal terms but P(X)=0 and would invalidate the claim. The source's explicit nonzero vector p excludes this counterexample.

Each Weyl coefficient triple (a_i,b_i,c_i) must be nonzero, with equivalent triples differing by a nonzero scalar identified. The parameters therefore lie in (P^2(C))^ell. Coefficients can depend arbitrarily on x. No regularity, continuity, computability, or algebraicity of that adaptive selection rule is assumed.

## Circulant theorem and adaptive support bound

ACCEPT for every positive integer N, including composite N.

Fix a complex number u with |u|>1 and take x_j=1/(u-omega^j). For row indices i and column indices j,

C_x[i,j] = omega^j / (u omega^j - omega^i).

Every square submatrix is a column-scaled Cauchy matrix. Its row points omega^i are distinct, its column points u omega^j are distinct, and no row point equals a column point because their magnitudes differ. The Cauchy determinant has nonzero pairwise-difference factors in its numerator and nonzero cross-difference factors in its denominator. Hence every square minor is nonzero for this single x.

Every fixed minor is a polynomial in x_0,...,x_(N-1). The product of all the finitely many nonempty square-minor polynomials is nonzero at this witness. Its nonvanishing set U_N is consequently a nonempty Zariski-open dense set. This proves the claimed simultaneous total nonsingularity, not just nonsingularity of C_x itself.

For x in U_N, let A be the support of a nonzero p, |A|=t. If C_x p had t zero coordinates, select t such rows R. The invertible square matrix C_x[R,A] would annihilate the nonzero vector p_A, a contradiction. Thus

nnz(P(X)x) + t >= N+1.

This quantifier is uniform over every p once x is in U_N. Adaptive, discontinuous, or nonconstructive choices of p do not escape it. The exceptional set depends only on N, not on the selection rule.

Sharpness also holds as stated. For any t columns A and any t-1 prescribed zero rows R, the (t-1)-by-t submatrix has rank t-1 and a one-dimensional kernel. A generator cannot have a zero coordinate: the remaining t-1 coordinates would then be killed by an invertible (t-1)-square minor. An additional output zero would contradict an invertible t-square minor. For t=1 this uses the empty determinant 1; for t=N it gives exactly one nonzero output. Both endpoints are valid.

Necessary source wording correction: the sentence saying t=polylog(N) "forces nnz(P(X)x)=N-polylog(N)+1" must use a lower bound. What follows is nnz(P(X)x)>=N-t+1=N-O(polylog(N)); equality holds for the separately constructed sharp filters, not for every t-tap filter.

## Multistage Weyl rank and incidence bound

ACCEPT for the exact operator family

B(theta)=(I-X^m)(a_1 I+b_1 Z-c_1 X)...(a_ell I+b_ell Z-c_ell X).

The written order is fixed by the tuple; allowing adaptive order does not add parameters because the tuple is already ordered. A finite union over other named order conventions gives the same bound.

For a factor L=aI+bZ-cX with c!=0, Ly=0 reads

(a+b omega^j)y_j-c y_(j-1)=0.

Since c is nonzero, one coordinate determines preceding coordinates cyclically. The closure equation may eliminate that one freedom, but cannot create a second: nullity(L)<=1. This remains true when a+b omega^j vanishes at some j. If c=0, L is diagonal. When b!=0 its diagonal entries a+b omega^j can vanish at at most one index; when b=0 the nonzero triple forces a!=0, so it is invertible. Thus the nullity bound is uniform over all allowed triples, including singular parameter strata.

For linear maps A and D, nullity(AD)<=nullity(A)+nullity(D): the inverse image under D of ker(A) has dimension at most dim ker(D)+dim ker(A). Repeating this and using dim ker(I-X^m)=m, the number of cycles of the shift by m, gives

nullity(B(theta))<=m+ell for every theta.

For a fixed output set S of size s, let Q delete its s rows. Deleting s rows decreases rank by at most s, so

rank(Q B(theta)) >= N-m-ell-s.

Therefore the linear x-fiber satisfying B(theta)x in C^S has dimension at most m+ell+s. The parameter space has complex dimension 2ell. The incidence set in (P^2)^ell x C^N consequently has dimension at most m+s+3ell. Its equations are polynomial in x and multihomogeneous in the coefficient triples, so they are well-defined on the whole projective parameter space. Projection to x is closed because the parameter space is projective. If m+s+3ell<N, its image is a proper algebraic subset. A finite union over S remains proper.

This proves, outside one proper algebraic set depending on N,m,ell,

nnz(B(theta)x)>=max(0,N-m-3ell) for every theta.

The maximum with zero only makes the vacuous range explicit. The source's weaker-looking untruncated inequality is also valid. Set s=N-m-3ell-1 when this is nonnegative to obtain exactly the stated integer lower bound. A +1 improvement is not supplied by this dimension calculation and should not be added automatically.

This generic set need not equal the circulant theorem's U_N. Their finite intersection is still nonempty open if both conclusions are wanted together. At each fixed N, one may also intersect over its finitely many permitted m and a finite range of ell. There is no need to assert a single exceptional subset of a common input space for all dimensions N.

### Zero operators and exceptional parameters

- If a zero triple were allowed, B could vanish identically and the claimed generic support lower bound would fail in its positive range. The source excludes it.
- For N>=2 the matrices I, Z, X are linearly independent, so a nonzero triple really defines a nonzero factor. The excluded N=1 Weyl case would require separate treatment.
- Products of nonzero factors can be zero when enough factors are present. For example, multiplying the X-eigenvalue factors missing from I-X^m produces a scalar multiple of I-X^N=0 using ell=N-m factors. This does not contradict the theorem: its support lower bound is already nonpositive there.
- In the informative regime m+3ell<N, the uniform rank bound gives rank(B)>=N-m-ell>0, excluding a zero product automatically.
- If m is not a divisor of N, the appropriate left-factor nullity is gcd(m,N), not m. That extension is possible but is outside the source's stated hypothesis. If m is a multiple of N, I-X^m=0; 1<=m<N prevents that case.
- Primitivity of omega matters. Repeated diagonal eigenvalues can give a diagonal Weyl factor a much larger kernel. No finite-field transfer is inferred from the complex incidence theorem.

The general rational-family principle is likewise sound when the parameter space is a finite-type algebraic family of dimension at most d, the maps are regular on the allowed loci, and the nullity bound holds at every allowed point. For a merely rational parametrization, exclude poles and take the algebraic closure of the constructible image. Its dimension still bounds the exceptional set. A bound that holds only for generic parameters cannot control arbitrary adaptive choices at exceptional parameters.

## WDRR row-defect consequence

ACCEPT the exact row identity under the source's positive-sign convention. Let M be an N-by-N matrix, E=MX-ZM, g=1-Me_0, with 1 the all-ones vector. The equality E[k,:]=0 says

M[k,j+1]=omega^k M[k,j]

with cyclic indices. The seed equality g_k=0 says M[k,0]=1. Induction gives M[k,j]=omega^(kj), exactly the kth row of the unnormalized positive-sign Fourier matrix. Conversely that Fourier row has both defects zero.

If the union of the nonzero row supports of E and g is contained in one set T, then M agrees with F on every row outside T. Thus |T|<=s already requires N-s exact Fourier output rows in the base operator. If E and g have separate supports of size at most s each, the union may have size 2s; the guaranteed count is N-2s, not N-s. State the common-union assumption explicitly.

The accepted criticism is an unprovided construction obligation: the correction formula does not construct a cheap base M with these defects. Defining M=F-correction without separately implementing M can hide the very Fourier computation being sought. The row identity does not prove that such a cheap M is impossible, and calling every use of a conditional small-defect theorem logically circular would be too strong. A proved low-cost base would make the reduction valid and useful. The original Phase 49 correction formula was not independently reconstructed here; this review accepts the new note's exact-row implication, not every other theorem in Phase 49.

## What the obstruction does and does not exclude

With ell=O(log log N) and m=polylog(N), the Weyl lower bound is N-o(N). With t=polylog(N), the cyclic-filter lower bound is N-O(polylog(N)). These results exclude the proposed uniformly tiny residual support for generic dense inputs in these exact families, even with input-adaptive coefficients. This is sufficient to reject an all-input algorithm whose advertised saving requires that sparsity premise.

The source's Theta(N log N) conclusion for a dense residual is accepted only for a specified conventional all-output radix-two FFT pruned by input support on power-of-two lengths. Near-full support does not imply a lower bound for every residual executor, an algorithm using other structural relations, or arbitrary arithmetic circuits. An executor that uses algebraic cancellation or non-support structure requires separate analysis. The obstruction gives no coefficient-selection or recovery algorithm and no claim about charged preprocessing, precision, stability, or finite-word execution.

Structured exceptional inputs may admit short annihilators; x=1 has (I-X)x=0. The generic theorem deliberately excludes such inputs. Preserved special-input or explicitly certified algorithms are not refuted by this example or by the generic barrier.

The note's additional external-comparator, historical-priority, determinant-bound, and proposed-recursion statements are outside this assigned fusion-gate review. No worldwide novelty finding is made.

## Independent finite certificate

A fresh reviewer-authored program uses memoized exact integer Laplace determinants, rather than the author's modular-elimination implementation. It reads only the supplied certificate data.

For x=(10000,7490,3169,9419,5373,7760,1589,6799), it verified all 12,869 nonempty square minors are nonzero over the integers and modulo 2013265921, and independently verified that integer is prime. Exact signed-cofactor filters were then formed for every support and prescribed zero set for every t=1,...,8. All 11,440 cases have all taps nonzero and exactly the prescribed t-1 output zeros, both as integer equalities and modulo the prime. This reproduces the author's 9,640 cases for t<=5 and also checks t=6,7,8. The retained reviewer result is summarized in [Verification scope](VERIFICATION_SCOPE.json). The reviewer program is not distributed in this prose packet.

The all-N proof above is mathematical. The finite check is corroborating evidence and source-certificate verification, not a substitute for that proof.

## Relationship to other research scopes

The obstruction applies to the stated adaptive cyclic-filter and bounded-depth Weyl families. A use of these families that needs a uniformly sparse residual on every dense input fails on the generic set established above. A conditional correction based on a cheap matrix with few common defective rows retains its separate base-construction obligation.

ALG-022 concerns fixed q-Pascal identities in nilpotent or truncated rings. The present cyclic theorem does not automatically transfer to those kernels or supply a faster arbitrary-input evaluator. SPARSE-PREFIX concerns a fixed-coefficient preconditioner and endpoint grammar in a totally nonsingular or prime-Fourier model; similarity of full-spark terminology is insufficient to identify the two grammars.

The accepted executors and promised-input interfaces associated with Q07, Q16, Q30 and ALG-079 are neither constructed nor refuted by this support theorem. Broader weighted-DAG, joint-macro, whole-target-resource, legal-network and all-dimension feasibility problems also require their own constructions and cost analysis. No unrestricted arithmetic-circuit lower bound, cheap-base impossibility, worldwide novelty claim or faster all-input FFT follows.
