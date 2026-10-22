# ALG-042: a growing obstruction to affine covers of the marker set

Status: independently verified within the stated scope on 22 October 2026. See INDEPENDENT_REVIEW.md; no historical novelty claim.

## Result

For the exact marker frequency set E retained in ALG-042, let tau_aff(E) be the least number of sets a_i E+c_i needed to cover Z/(2^n), where every a_i is odd. Then

    tau_aff(E) >= 2^floor((b+1)/2) >= sqrt(2L),   L=2^(b-1).

In particular, no uniform constant-size affine cover exists at the accepted asymptotic marker choice b=floor(log2(n/(4 ln n))). Translation-only covers are a subclass, so the same lower bound applies to them. Together with the previously proved O(L) translation cover, this leaves

    Omega(sqrt L) <= tau_aff(E) <= tau_trans(E) <= O(L).

This resolves only the constant-cover question negatively. It does not prove an operation lower bound for computing the selected Fourier outputs, a generic FFT lower bound, or failure of other reductions. The accepted orthonormal frontier, paid O(NL) interconversion, and selected-chirp-convolution target remain intact. The exponent in the displayed lower bound is not claimed optimal. Historical novelty is not assessed.

## 1. Exact inherited target and permitted maps

The immutable source is NORMALIZED_PACKET_ESCAPE.md at repository commit ac6418587047464926c436ba21ce54d388f77616, sections 1, 3, 4, and 7. Its independent audit is INDEPENDENT_NORMALIZED_FRONTIER_AUDIT.md, especially section 6. Full verified locators and Git-object hashes appear in SOURCES.json.

The parameters are N=2^n, L=2^(b-1), b>=7, L+2b<=n. E is the union of frequency cylinders C(h,f)={ell: ell=f modulo 2^h} for n-L<=h<=n and selected h-bit labels f. A selected label has MSB-first pattern

    0^b rev_t(k) 0^b [free bits],

where 1<=t<=L, h>=2b+t, and k starts and ends in 1 and contains no 0^b. The reversal does not matter to the proof below.

The precise containment needed is elementary: every ell in E has a consecutive block of b zero digits in its ordinary, padded n-bit representation. Indeed, membership in C(h,f) fixes the lower h bits, and their highest b bits, at positions h-b through h-1 counted from the least significant bit, are zero. Extending to n bits adds positions above h-1 and cannot destroy this run.

Define Z_b(n) as all residues whose padded n-bit expansion contains b consecutive zeros at any position wholly inside positions 0,...,n-1. Thus

    E subset Z_b(n).

The source's affine frequency maps realized by source permutations and modulations are ell -> a ell+c modulo N, with a a unit modulo N, equivalently odd. For example, setting z_s=omega^(cs) x_(a^(-1)s) gives (Fz)_ell=(Fx)_(a ell+ac). Since c ranges over all residues and a is invertible, this realizes all affine translates aE+d. Scalar phases and input-index translations do not enlarge this output-index group. The source explicitly warns in section 7: "Arbitrary bit permutations of frequency labels are not free source permutations in the Fourier transform". Thus its affine question is not a question about arbitrary affine transformations of the vector space F_2^n. No arbitrary frequency-bit permutation, noninvertible dilation, or independently chosen local map is smuggled into this scope.

The inherited computational model is exact scalar arithmetic over a field containing the supplied Nth root and 1/sqrt(2), with word-address routing and coefficient preparation charged. The new statement is a combinatorial covering obstruction, independent of operation costs. It does not convert a count of covers into an unrestricted circuit lower bound.

## 2. Block-avoidance lemma

Lemma. Let n>=b>=1, d=floor((b+1)/2), and let f_1,...,f_k be arbitrary affine permutations of Z/(2^n), f_i(x)=a_i x+c_i with a_i odd. If k<2^d, there exists x such that every padded n-bit expansion f_i(x) contains no b consecutive zero digits.

The maps and their coefficients may depend arbitrarily on n and b. The quantifier is for every family of fewer than 2^d maps, not for a fixed map family followed by a size limit.

Proof. Partition the bit positions starting at position zero into complete aligned d-bit blocks

    J_j={jd,...,(j+1)d-1},  0<=j<floor(n/d),

and, if necessary, one final shorter block. We select x from least significant bits upward, requiring that every complete J_j be nonzero in every f_i(x).

Suppose positions below m=jd of x have already been chosen, with lower residue P in [0,2^m). Write the next chosen d-bit block as v in [0,2^d), so the new lower residue is P+2^m v. Arbitrary later, higher input bits cannot affect output bits below m+d. Integer division gives the output block exactly as

    B_i(v) = (a_i v + floor((a_i P+c_i)/2^m)) modulo 2^d.

This remains valid when the representative a_i P+c_i exceeds N, since reduction modulo N changes the quotient by a multiple of 2^(n-m), which is divisible by 2^d for a complete block. Equivalently, compute modulo 2^(m+d) from the start.

Because a_i is odd, multiplication by a_i permutes residues modulo 2^d. Thus B_i(v)=0 has exactly one solution v. There are at most k forbidden choices across all k maps. Since k<2^d, at least one safe v exists. Choose one and proceed to the next block. Previously secured output blocks remain unchanged. After all complete blocks, choose any remaining high input bits.

It remains to exclude a b-zero run not aligned with the partition. Take any b consecutive bit positions {s,...,s+b-1} inside {0,...,n-1}. The first aligned block start m=d ceil(s/d) obeys s<=m<=s+d-1, so its block end satisfies

    m+d-1 <= s+2d-2 <= s+b-1,

because 2d-1<=b. Therefore this interval contains a complete aligned d-block J_j. The block is wholly within n positions, including when n is not divisible by d. That block was made nonzero in every output. No f_i(x) can have the alleged b-zero run. QED.

Witness count. At every complete block there are at least 2^d-k choices, and the final n mod d bits can be chosen freely. Therefore at least

    (2^d-k)^floor(n/d) * 2^(n mod d)

different x simultaneously avoid all k transformed zero-run sets. This is also a lower bound on the number of frequencies missed by k affine images of E, by applying the statement to the inverse maps. The count is not needed to exclude a constant cover.

Remark. The proof actually works for any permutations compatible with reduction modulo powers of two: conditioned on a lower prefix, the next output block must permute the 2^d extensions. The affine specialization above is sufficient and is the only transformation class used in the cover conclusion. This remark is a proved extension of the block argument, not an assertion that the original computational model authorizes arbitrary bit permutations.

## 3. Cover lower bound and asymptotics

Suppose k<2^d affine images g_i(E) covered Z/(2^n). Each inverse g_i^(-1) is again odd-affine. Apply the lemma to f_i=g_i^(-1) and obtain x with all f_i(x) outside Z_b(n), hence outside E. Then x is outside every g_i(E), a contradiction.

Thus tau_aff(E)>=2^d. Translations are the case a_i=1, yielding tau_trans(E)>=tau_aff(E). Since 2floor((b+1)/2)>=b and L=2^(b-1),

    (2^d)^2 >= 2^b = 2L.

Consequently the covering number diverges at least as Omega(sqrt L). Merely fixing b and letting n grow would not give divergence, and that is not the asymptotic claim. Under the explicit accepted choice b=floor(log2(n/(4 ln n))), n/ln n tends to infinity, so b tends to infinity and L=Theta(n/ln n). The lower bound is then Omega(sqrt(n/ln n)), or Omega(sqrt(log N/log log N)). In particular, the constant-cover question posed in the source has a negative answer even when arbitrary odd multipliers and shifts, depending on size, are allowed.

## 4. Explicit witness construction and scope of cost claims

For an actual proposed k-map cover with k<2^d, the proof gives a missing-frequency witness. At block m, invert each a_i modulo 2^d and compute its single forbidden digit

    v_i = -a_i^(-1) floor((a_i P+c_i)/2^m) modulo 2^d.

Choose a digit outside {v_1,...,v_k}; such a digit exists. Repeat for every complete block and set the final short block to zero. This is an exact finite-integer witness method, not an FFT algorithm. A straightforward implementation may search the 2^d possible digits and use growing-precision integer products; no unproved constant-time bit-complexity bound is asserted. The theorem is constructive without relying on executing repository programs or on a feasibility extrapolation from finite checks.

The count is solely about covering frequency sets. It does not exclude recovery through additional algebraic operations or non-affine preconditioning. In particular, multiplying the cover lower bound by an implementation upper bound would not produce a valid universal operation lower bound.

## 5. Verification and disposition

The mathematical proof is all-size. Independently authored finite controls in fresh_controls.py check the block map formula, inverse-map convention, partial final blocks, all possible forbidden-window placements, literal marker containment on small toy instances, and exact witness avoidance for admissible b>=7 instances. These controls corroborate the proof but do not replace it. They do not execute or import supplied repository code.

The research catalogue identifies ALG-042 as a broader open programme, including faster selected convolution, early-time outputs, causal/full recovery, and numerical/bit qualifications. Its overall TO RESEARCH status and priority 34 are unaffected by closing the constant-cover question.

The independently verified disposition is: close the constant-size odd-affine/translation-cover gate negatively, while preserving ALG-042's accepted reductions and its separate unresolved selected-transform/algorithmic obligations. No external table or repository was changed by this research task.
