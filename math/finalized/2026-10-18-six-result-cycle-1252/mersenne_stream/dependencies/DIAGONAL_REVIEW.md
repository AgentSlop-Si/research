# Independent review: width-adaptive streamed diagonal maps

18 October 2026 UTC.

## Verdict

PASS for the exact arithmetic construction and its stated complete conversion upper bound, under the explicitly inherited sequential-bit/array arithmetic model and wide-digit interface. No blocking correction is required.

With alpha=log_2(3), a=alpha-1, N=Lm, and m>=cL for fixed c>0, the accepted bound is

O(M(CN) + N B_*^a + N (log(L+1))^a),

where B_*=max(1,min(m,L ceil(log_2(L+1)))). The full diagonal maps, the small inverse, the complete W-bit kernel, coefficient scans, signed guards, carrying and explicit outputs are paid. The convolution backend M is still a separate same-scale cost.

The construction improves the explicit Karatsuba diagonal/inversion upper bound when W/(n log(n+1)) tends to infinity. For admissible supplied parameter families with L=O(log N), its local diagonal/inversion/setup/reconstruction cost is o(N log N). It does not establish a complete sub-N-log-N multiplier, balanced-width diagonal saving, arbitrary-backend superiority, growing Mersenne-prime availability, or a matrix/correlated-product improvement.

There is one minor operation-count wording correction: section 2's phrase "q bounded additions/subtractions" should read "O(q) bounded additions/subtractions". The supplied loop performs three represented-value additions/subtractions per limb: a-carry, product+carry, and the final subtraction of a. The asserted exact 2q local multiplication count is correct, and the displayed complexity is unchanged.

## Exact inspected binding and provenance

The original candidate was read without modification. A separate snapshot is retained in reviewed_candidate/. All 18 entries in the candidate manifest were checked, as were all seven restored sources' SHA-256 and Git-blob SHA-1 identities. Six restored files also matched their entries in the accepted source package manifest; that manifest itself is pinned separately.

- Candidate manifest SHA-256: 5155de0817c61b23cd812bc996e845c6c69592a158ef9b715c3fcbf5b13b175d
- Report SHA-256: 1bdb0ed25a032ab6550ffcdcaf108671c4a7a5e08c13a7c900c6ce9b54441cf1
- Arithmetic core SHA-256: 7e7e8ca33bfa00eeb35547c26eebeefb377d90172ee5b15dfb29145b5f021b8f
- Candidate controls SHA-256: 39065f8b983984e14481c3dcb36a9ae993568e790f09084b1c69397d7f4ba1fa

The pinned setup candidate/review, inherited conversion report, native-negacyclic report and mandatory clarifications were inspected for their applicable interfaces and exclusions. Historical source programs were neither imported nor executed. The new candidate controls were run only in the review snapshot, and their RESULTS.json reproduced the original exactly, including every count and its digest. The preserved initial failure log is consistent with an integer-to-decimal digest serialization failure, not an arithmetic assertion failure.

The external attribution was checked against [GNU MP's exact-division documentation](https://gmplib.org/manual/Exact-Division). It supports the stated established low-digit modular-inverse principle. The candidate's modular-division recurrence and bound are proved independently; ordinary exact divisibility is not imported as an assumption.

## 1. Modular division: carry, prefix, widths and exact products

Set R=2^t, 0<u<R odd, and v=u^-1 modulo R. Given a_j in [0,R), choose b_j=((a_j-c_j) mod R)v mod R. Then u b_j+c_j-a_j is divisible by R. If 0<=c_j<u, its lower bound is -(R-1)>-R and its upper bound is uR-1<uR. As a multiple of R, it is nonnegative and its quotient is strictly less than u. This establishes the nonnegative bounded carry invariant, including u=1.

Multiplying the recurrence by R^j and telescoping gives uY_r=X_r+c_r R^r. At q=ceil(W/t), R^q is divisible by 2^W, so truncating Y_q to W bits gives exactly x u^-1 modulo 2^W. The final carry need not vanish. Zero padding and the last partial limb are valid even for W<t.

Each digit invokes two multiplications with operands of at most t bits. The intermediate product-plus-carry is below R^2, and every retained carry has at most t bits. The pre-multiplication modular subtraction and all subsequent additions, subtractions and masks are bounded-width. Exactly 2q outer products are performed when the microinverse v is supplied. Its construction is separately charged.

The buffer implementation reads bounded windows, writes bounded windows and materializes the whole input/output only a constant number of times. Its arithmetic-core cost is

O(q(K(t)+t)+W+t).

It does not repeatedly shift a W-bit input at each digit or repeatedly add into a growing output. The standalone multiplication/division formula keeps the t^alpha term when W<t; it is absorbed only after applying the chosen factorial width.

## 2. Factorial cap and byte rounding

For n>=2 and 0<=i<n,

1<=u_i<=i!<n^(n-1)<=2^((n-1)ceil(log_2 n)).

The n=1 cap is B_n=1. Let B=min(W,B_n) and t=8ceil(B/8). Then B<=t<B+8, so t=O(B) with B>=1.

If W<=t, U_i=u_i modulo 2^t implies the needed congruence modulo 2^W. If W>t, B cannot be W, because t>=B; therefore B=B_n, and u_i<2^B<=2^t. In this branch U_i equals the ordinary odd factorial exactly. In both branches U_i is an odd unit with the same action modulo 2^W as u_i.

This is the key reason the inverse action may be evaluated by division by a short denominator even though the displayed inverse residue itself occupies W bits. No full-width inverse residue multiplication is silently left behind in the final diagonal.

## 3. Shared inverse and complete kernel preparation

The forward recurrence U_i=U_(i-1)o_i modulo 2^t is exact. One precision-doubling Newton inverse supplies v_(n-1). Since U_i=U_(i-1)o_i, the reverse relation v_(i-1)=v_i o_i modulo 2^t produces all microinverses.

The Newton implementation masks u to the current precision and masks the correction before multiplication. Both argument pairs are bounded by the current precision. The sequence of powers-of-two precisions, with a possibly shorter last step, costs O(K(t)) for the explicitly terminating Karatsuba routine.

For W<=t, truncation of the microinverses supplies all W-bit V_i directly. For W>t, exactly one streamed modular division of 1 by U_(n-1) produces V_(n-1), and n-1 reverse short-factor products produce the entire full-width inverse-factorial kernel. Nothing treats those W-bit outputs or their scans as free.

All table factors o_i have O(log(n+1)) bits. Byte-rounded short-factor streaming therefore charges O(nW(log(n+1))^a) for forward/reverse microtables and the optional full-width reverse table, since t=O(W). The one Newton inverse and optional terminal modular division cost O(WB^a). Constructing odd parts and small indices is absorbed: W>=n and log^2(n+1)=O(n). Microtables, full tables and arrays occupy O(nW) bits, plus the convolution workspace; temporary long carries do not occur.

## 4. Both actual diagonal maps and exact reconstruction

The implementation evaluates

A_i=2^(g-s(i))u_i a_i modulo 2^W

by streamed multiplication with U_i, and it evaluates

R_j=2^s(j)u_j^-1 D_(n-1-j) modulo 2^W

by streamed modular division with U_j followed by the indicated power-of-two shift. The latter is not an unevaluated diagonal rescaling passed to another stage. Signed input reduction by the W-bit mask is exact.

For i<n, s(i)<=g=ceil(log_2 n), so every initial shift is nonnegative. The full kernel is J_i=sigma^i 2^s(i)V_i. Reversing A gives the required correlation orientation, and the accepted valuation identity yields R_j=2^g(T_sigma a)_j modulo 2^(H+g). Its low g bits are therefore zero. Exact division by 2^g retains all H bits; |(T_sigma a)_j|<2^(H-1) gives unique centered recovery. Both signs of sigma, signed coefficients, empty input and the direct n=1 branch are consistent.

The bit work for the n initial streamed products plus n final divisions is O(nW B^a): each input coordinate uses q=ceil(W/t) bounded products, each output coordinate uses 2q, and t=O(B), B<=W. Kernel sign formation, power-of-two shifts, masks, input/output scans and centered reconstruction add O(nW).

## 5. Complete conversion ledger and remaining obstruction

The exact packed convolution has b=8ceil((2W+ceil(log_2 n))/8) and S=nb. Its unreduced coefficients are strictly below n 2^(2W)<=2^b, preventing inter-slot carry. It costs one paid M(S) multiplication plus O(nW) packing/extraction. Combining every term gives

O(M(S)+nW B^a+nW(log(n+1))^a).

For the accepted binary, redundant-p, canonical-p, lazy raw-product and inverse interfaces, n=O(L), W=O(m), nW=O(N), S=O(N), and B=O(B_*), with constants allowed to depend on the fixed c. The inherited signed local quotient/carry and binary-carry streams, including final tails and possible extra p digits, remain O(N). This yields the stated complete conversion upper bound. The new code implements the changed shift core; the older exact carry construction and grouping cost proof are inherited, not falsely represented as newly implemented production stages.

For grouping length d<=L, O(L/d) actual-length shifts give the paid convolution total (L/d)M(Cdm) and local total

O(N min(m,d log(d+1))^a+N(log(d+1))^a).

Under the inherited monotonicity of M(t)/t, the first term aggregates into O(M(CN)); the local terms do not exceed the global L terms. Partial groups, enlarged raw coefficient heights, bounded overlap and the actual-width lone-digit handling preserve the premises. This is not a cost theorem for a newly implemented grouped matrix multiplication.

When L=O(log N), B_*=O(log N log log N), so the dominant local ratio to N log N is bounded by a constant times

(log N)^(a-1)(log log N)^a,

which tends to zero since a<1. This covers the local conversion work only. The convolution remains M(CN). At balanced m=Theta(L), B_*=Theta(m), giving no new Karatsuba diagonal order. The alternative minimum with the old independently supplied diagonal backend remains legitimate; no universal superiority over M is claimed.

For each nontrivial input-shift instance L>=2, W>m and S>=2LW>2N. Consequently, literal replacement of this prescribed-capacity convolution backend by the same nontrivial converter/multiplier at every nonleaf gives a larger recursive child and cannot terminate using only a fixed size cutoff. This argument applies to that particular repeated capacity recipe. Actual-value trimming, a different basecase strategy, fusion or a specialized convolution evaluator would need separate constructions and charges; no multiplication lower bound follows.

Strict-prime availability and selection, same-scale convolution, balanced-width diagonal improvement, matrix transforms, correlated point products and complete recursive composition all remain open exactly as stated by the candidate. Fixed p=3 cannot supply an unbounded L family satisfying m>=cL.

## 6. Fresh independent finite controls

After inspecting the code and proof, independent_checks.py was written with seed 202610181052. It passed:

- 792 signed Karatsuba products, including split/leaf boundaries and up to 4,098-bit operands.
- All 4,194,304 valid 8-bit carry transitions over odd u, all 0<=c<u and all input limbs.
- 200 Newton inversion controls, checking current-precision argument widths and exact iteration/product counts, plus agreement with the explicit arithmetic implementation.
- 690 complete streamed division/product controls up to 65,537 input bits, checking every prefix identity, carry bound, partial limb, exact 2ceil(W/t) local multiplication count and t-bit argument cap.
- 91 odd-factorial tables spanning both width branches and byte-padding boundaries, checking exactly one small inverse and exactly one terminal long division when W>t.
- 120 signed cases separately inspecting both diagonal maps, the complete kernel/convolution orientation, guards, centering and inverse shift against a polynomial-Horner oracle.
- 726 exhaustive signed shift/inverse cases using the original explicit Karatsuba convolution backend, plus the empty input.
- 40 maximum-digit round trips and lazy-product identities, with signed binary carry normalization; 200 grouped actual-length identities.
- 36 conversion parameter/capacity boundary controls.

For larger algebraic cases, the optional convolution backend is explicitly replaced by native multiplication as a paid correctness oracle. Those cases are not represented as explicit-Karatsuba execution or timing evidence. The separate 726 exhaustive cases and the reproduced original harness do execute the candidate's own convolution backend. Likewise, the fresh normalization tests use independent oracle arithmetic; they do not claim to rerun the historical carry implementation.

INDEPENDENT_RESULTS.json records digest f0606cb4fac851079fde15531b1018079aa141ff02acc3ee6017bb40ccf6b243. The finite evidence supports implementation correctness; the explicit proof supplies the asymptotic bounds. No runtime comparison or external write was performed.
