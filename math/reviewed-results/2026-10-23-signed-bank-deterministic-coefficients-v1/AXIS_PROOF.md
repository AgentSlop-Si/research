# Exact reciprocal axis guard and linear-degree scalar avoidance

23 October 2026 UTC. New candidate for independent review. This changes only the exact coefficient-stage axis guard and its proof of the scalar trial bound. It does not change the original space U, any physical bank, accepted source packet, root-field requirement, or warm application schedule. No historical/supplied program is executed and no historical novelty is claimed.

## 1. Contract and result

Retain the original gate N odd, d >= 4, N >= 8d - 10, m = N - d, and a field k containing a primitive Nth root q, with char(k) not dividing N. Retain the ORIGINAL envelope E and coefficient space U = E^perp from the pinned all-characteristics source, and the accepted two-pencil construction. In particular every g in U satisfies g(1) = 0.

Write n = m - 1. For a monic degree-m candidate g with g(1) = 0 and g(0) != 0, put

    h = g/(t - 1), c = h(0), v = rev_n(h),
    K = (h - c)/t, H_N = 1 + t + ... + t^(N-1).

There is an EXACT axis full-rank test using O(N^2) field additions/multiplications, O(N) inversions, and O(N) temporary field-element storage. It handles the entire reciprocal-gcd locus, not merely a generic subset. Together with the original nonzero-constant and squarefreeness tests it replaces each cubic dense rank test in the final pencil.

Moreover the axis rank condition admits a nonzero scalar guard of degree at most 2d on the existing second pencil. The complete product guard has degree at most

    H_fast = 2d + (2m - 2) + 1 = 2N - 1.

Thus a supplied list of 2N distinct field elements suffices for EVERY scalar choice in the two-pencil coefficient generator. The complete deterministic coefficient stage costs O(N^4) field additions/multiplications, O(N^3) inversions, and O(N^2) live storage. The two coprime-combination loops, not the final scalar stage, dominate this bound. This improves the accepted deterministic O(N^5) coefficient-stage upper bound, not the existing expected O(N^3) Las Vegas bound or the full bank compiler.

## 2. Exact reduction of the ORIGINAL axis matrix

The original matrix X_N(g) has row a equal to (p_a, 1, p_[−a mod N]), where p_i is the coefficient vector of t^i mod g. A left relation beta defines A(t) = sum_(a=0)^(N-1) beta_a t^a. It is exactly a relation when

    g | A, A(1) = 0, g | J_N A,
    J_N A = t^N A(1/t) + A(0)(1 - t^N).

Since g = (t - 1)h, write A = (t - 1)k with deg k <= N - 2. Then A(0) = -k(0), and direct expansion gives, in EVERY characteristic,

    J_N A = (t - 1)[k(0) H_N - t rev_(N-2)(k)].

The first divisibility is equivalent to k = h a, deg a <= d - 1. Put b = rev_(d-1)(a), so a(0) = b_(d-1). Reversal is taken to the stated padded degree, even if a has smaller actual degree. Since n + (d - 1) = N - 2, the second divisibility is exactly

    t v b = c b_(d-1) H_N (mod h), deg b <= d - 1.          (1)

Nonzero A, a and b are equivalent. The scalar-column condition A(1)=0 is automatic, not omitted. No field characteristic, squarefreeness, or nonzero constant was needed for (1).

For c != 0, t is a unit modulo h. The identity h = tK + c gives c/t = -K modulo h. Thus (1) is exactly

    v b = w b_(d-1) (mod h), w = -K H_N.                  (2)

This step explicitly uses c != 0, which the generator checks before invoking the fast test.

## 3. Exact reciprocal-gcd test, including its exceptional locus

Let D = gcd(h,v) be monic, hbar = h/D, vbar = v/D, and ell = deg hbar. Since gcd(vbar,hbar)=1, ordinary extended Euclid can compute the inverse below whenever needed. Set s = d - 1.

The following cases are exhaustive.

1. If ell <= s - 1, rank X_N(g) < N. Indeed choose b = hbar. Its coefficient b_s is zero, and h | vb. This is a nonzero relation, including ell = 0.

2. Suppose ell >= s. Any relation with b_s = 0 would have hbar | b and deg b <= s - 1 < ell, so it would be zero. Therefore every nonzero relation can and must be normalized to b_s = 1.

3. Such a normalized relation can exist only if D | w. Since gcd(K,h)=1 when c != 0, this condition is EXACTLY D | H_N, with all multiplicities retained. If D does not divide H_N, the axis has full row rank.

4. If D | H_N, define the unique residue of degree less than ell

       b0 = [vbar^(-1) (-K (H_N/D))] mod hbar.

   All normalized solutions of the congruence are b = b0 + hbar z.

   - If ell = s, the polynomial b0 + hbar is monic of degree s, so rank drops.
   - If ell > s, only b0 could have degree at most s. Rank drops EXACTLY when b0 has degree s and leading coefficient 1. Otherwise the axis has full row rank.

In the familiar reciprocal-coprime case D = 1, ell = n > s, this reduces to the tentative criterion in the task: rank drops exactly when

    b_* = [(t v)^(-1) c H_N] mod h
        = [-K H_N v^(-1)] mod h

is monic of degree d - 1. Every nonzero relation then has a(0) = b_(d-1) != 0. The excluded locus gcd(h,tv) != 1 has NOT been silently discarded: because c != 0, it is exactly D != 1, and cases 1–4 decide it exactly.

The test can return a relation certificate when it reports a rank defect: use b=hbar in case 1, b=b0+hbar when ell=s, or b=b0 in the last defective case; reverse b to obtain a and return A=(t-1)ha. Multiplication and the two original divisibilities verify it in O(N^2) arithmetic.

## 4. Why the original second pencil avoids the gcd locus generically

Use the accepted witness f, monic of degree r = m - 2 = n - 1, with nonzero constant and gcd(f,rev_r f)=1. The second pencil is

    h_Z = h0 + Z h1, h0 = t f,
    deg h1 < n, gcd(h0,h1)=1,
    g_Z = (t - 1)h_Z.

In particular c_Z = Z h1(0), with h1(0) != 0. At Z = 0,

    v0 = rev_n(h0) = rev_r(f),
    gcd(h0,v0) = gcd(t f,rev_r f) = 1.

The last equality also uses rev_r f(0)=1. Hence S(Z)=Res(h_Z,v_Z) is nonzero, already at Z=0, and has degree at most 2n. Thus this SAME family generically avoids the reciprocal-gcd locus. The resultant Res(h_Z,t v_Z) has the factor (-1)^n c_Z, so it vanishes at Z=0; it must not be inverted there.

There is a safe continuation of the normalized residue:

    B_Z = [-K_Z H_N v_Z^(-1)] mod h_Z.

It is defined at Z=0 because S(0)!=0. At that point K0=f and B0=-f: indeed v0(-f)+f H_N = f(H_N-v0) is divisible by t f because H_N(0)=v0(0)=1, and -f has degree n-1<n. Its coefficient at degree n-1 is -1, nonzero also in characteristic two and above the allowed degree d-1.

For an alternative Sylvester/Cramer polynomial certificate, solve

    v_Z B_Z + h_Z Q_Z = -K_Z H_N,
    deg B_Z < n, deg Q_Z < n+d.

The square coefficient matrix has 2n+d rows and columns and affine entries in Z. Its determinant is, up to sign, S(Z), since elimination of the highest d quotient coefficients leaves the usual Sylvester matrix. The Cramer numerator for B_(n-1) has degree at most 2n+d and is nonzero at zero, equal to -det(M(0)). This proves a degree-O(N) guard without an illegal inverse at the singular original t-resultant boundary. The next section gives a smaller and simpler guard and does not need to exclude S=0 at all.

## 5. A degree-2d axis guard by a truncated Sylvester matrix

Return to (1), without assuming c != 0. Write it as a polynomial equality

    t v b - c b_(d-1) H_N - h q = 0.                    (3)

The nominal top degree is N-1=n+d. Its coefficient cancels identically: the first two terms each have coefficient c b_(d-1). Hence their difference has degree at most N-2. Since h is monic of degree n, its quotient q has degree at most d-1.

Therefore let M(h) be the coefficient matrix of the map

    (b,q), deg b<d, deg q<d
      -> t rev_n(h)b - c b_(d-1)H_N - hq
         in polynomials of degree <=N-2.

It has N-1 rows and 2d columns. Every entry is LINEAR in the coefficients of h; on the accepted affine pencil every entry has degree at most one in Z. A kernel element with b=0 necessarily has q=0. Thus M(h) has full column rank EXACTLY when the ORIGINAL X_N((t-1)h) has full row rank. This equivalence includes c=0.

At the existing auxiliary witness h0=t f, equation (3), after cancelling t, becomes

    rev_r(f)b = f q.

Coprimality forces f|b. But deg f=r>d-1, so b=q=0. Consequently M(h0) has full column rank. Choose for the proof any 2d-row minor nonzero there. On the second pencil it is a nonzero polynomial A(Z) of degree at most 2d. No symbolic minor need be computed by the generator.

The accepted pencil proof already establishes that g_Z is generically squarefree, including in characteristic two, and c_Z is a nonzero linear polynomial. Multiplying A(Z), c_Z, and the monic degree-m discriminant gives a nonzero polynomial of degree at most

    2d + 1 + (2m-2) = 2N-1.

A scalar failing at least one ORIGINAL guard must be a zero of this polynomial. A list of 2N distinct scalars therefore contains a successful scalar. The exact algorithm tests nonzero constant, gcd(g_Z,g_Z')=1, and Section 3, so it may also accept good points where the particular theoretical minor vanishes. It does not compute symbolic resultants, assume genericity of a tested point, or weaken the rank condition.

## 6. Entire coefficient-stage accounting

All arithmetic below is in the supplied coefficient field, with schoolbook dense polynomial operations and separately counted inversions.

- Original E matrix, U basis, endpoint constraints, and bases V0,V1,W: O(N^3) arithmetic, O(N^2) storage, as in the accepted generator.
- Each of the TWO coprime-combination loops processes O(N) basis directions and at most O(N) scalar trials per direction. Each trial costs O(N^2) arithmetic and O(N) inversions, including exact gcd equality, candidate construction and coefficient reads/writes. Together they cost O(N^4) arithmetic and O(N^3) inversions.
- First reciprocal pencil: at most 2r+3=2m-1 trials, each O(N^2) arithmetic and O(N) inversions, hence O(N^3) arithmetic and O(N^2) inversions.
- Final pencil: at most 2N trials. Each forms g/h/v/K in O(N), computes squarefreeness by Euclid, and applies Section 3. Gcds, divisibility of H_N by D, one extended-Euclid inverse and degree-O(N) multiplication/remainders cost O(N^2) arithmetic and O(N) inversions per trial. This includes failures, repeated-factor cases, and reciprocal-gcd specializations. Total O(N^3) arithmetic and O(N^2) inversions.

The single list of 2N distinct elements also supplies every earlier choice: the first pencil needs 2m-1, and both combination lemmas need at most n+2<N+2<=2N. Candidate storage is streamed. The envelope/nullspace data dominate storage at O(N^2); no dense axis matrix is needed for the final guards. Total read/write/address work is bounded by the O(N^4) arithmetic-loop count; final coefficient output is included.

TOTAL: O(N^4) additions/multiplications, O(N^3) inversions, O(N^2) live field-element storage. The dominant loops have not been hidden behind the faster final guard. This does not improve the pre-existing expected O(N^3) Las Vegas coefficient-stage upper bound, whose one-time dense envelope solve still dominates after replacing its rank test.

## 7. Unchanged cold field and physical-bank ledger

Retain the supplied/certified base-field representation and q. In the finite case keep the SAME quadratic coefficient field E0=F_(Q^2); its existing O(Q^3) base-field preparation is still charged. Q>=N+1, so Q^2>2N supplies the needed list. List writes are O(N) field elements, plus representation/counter costs; no constant-cost machine word is presumed. In characteristic zero, 0,...,2N-1 is a list; arbitrary positive-characteristic infinite fields still require the stated effective distinct-element interface. No unqualified bit bound follows.

After coefficient generation retain the entire pinned original ledger, without alteration: construct a genuine splitting field or the paid m!-degree finite overfield; recover actual distinct nonzero roots; solve all Vandermonde and axis amplitude systems; recover all raw weights; prepare every original branch inverse; write every coefficient and output coordinate; and expand extension arithmetic/storage to base-field coordinates. Squarefreeness and nonzero constant are still checked exactly before using roots as banks.

In particular the conservative finite root-field recipe remains O(t^2 R^(t+floor(t/2))) coefficient-field operations for its modulus, plus O(m t^2 R^t) for the root scan, where t=m! and R=Q^2. Subsequent sector/weight/operator preparation remains O(N^3) root-field arithmetic with O(N^2) root-field storage. The literal warm B-bank application is unchanged at 2BN^2 multiplications and 2BN^2-BN-N additions, with B=2m+2 and full read/write costs. There is no end-to-end polynomial-time compiler, smaller bank count, efficient root oracle, or FFT improvement.

The ingredients are classical polynomial gcd, reversal, and truncated Sylvester linear algebra. The candidate contribution is this exact original-axis test and the resulting paid deterministic coefficient-stage contract. Independent acceptance is required before any research-table or repository change.
