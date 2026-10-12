Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: baf6ce0c48a556626c1caa691ad8f7ee3f3dd821b91da815cdd6adcb5fd9e355.

# Independent review: complete Phase43/44 even-chirp membership certificates

Review date: 12 October 2026 UTC.
Gate: CHIRP-PHASE43-44::certificate-api.
Verdict: ACCEPT SCOPED, bound only to the sealed candidate below.

## Exact accepted delta

The stronger primitive-order-2N common-chirp family now has a complete mathematical positive/negative membership-certificate contract for every N>=1 and r>=0. The fresh reference implements that contract over its explicitly bounded supplied prime-field interface, with resource-limited decisions and an independently checkable certificate. Every MEMBER includes its phase, support, amplitudes and all N transform values. Every NONMEMBER includes an exhaustive exclusion certificate. Direct transform output by itself is never membership evidence.

This closes the specific certificate-API obligation. It does not close higher-rank acquisition for the distinct baseline Q13 family, alter the already accepted Q13 rank-one integration, or imply an unrestricted FFT improvement. It does not establish an optimized growing-r kernel, extension-field implementation, numerical stability, historical priority, or a new discovery count. Original source and earlier review programs remained inert throughout this review.

Candidate archive: CHIRP_Phase44_Complete_Certificate_CANDIDATE_2026-10-12.zip.
Archive SHA-256: 2298e49da4bd0d75acc4b24ef2f3e38360a6922f3188661bee26119c2b6e8a0c.
Archive length: 115,952 bytes.
Implementation SHA-256: a4f9da9ea4bf70984b82823894cd0f33e9a2b2839a82672ff0cd4ed68cd96151.
CONTRACT.md SHA-256: b3e9eba5f6ed1cb2ca797c8952799bc6babbe37f1497826daceba0788d0129c9.
MANIFEST.json SHA-256: ccd82052ec7c732bf8e945929029829edefbb7c904a7faedd92a4445422f0247.
All 22 manifest payloads, 19 original-source pins and 12 prior-review pins were independently rechecked from these bytes.

## Family and field premises

Let K be an exact field containing a supplied primitive 2N-th root psi, let w=psi^2, and use the negative-sign unnormalized transform X[k]=sum_n x[n]w^(-kn). The family is the union, for 0<=b<N, of sequences

    x[n] = psi^[b n(n-N)] sum_(a in S) c_a w^(an),  |S|<=r.

The root premise itself forces characteristic coprime to 2N: in positive characteristic p, an element of multiplicative order divisible by p cannot exist, since z^p-1=(z-1)^p. Thus 2 and N are invertible, w has exact order N, its N powers are distinct, and the Fourier matrix is invertible. No characteristic-zero or p>r assumption is needed for the mathematical proof. Factorial integers are never divided by. The executable is more restrictive: odd prime p<=2^31-1, 1<=N<=4096, 0<=r<=8, a canonical supplied psi, and a 50,000,000-unit maximum cap. It validates primality and exact root order on every call. It does not discover roots or build an extension field.

The exponent n(n-N) gives a genuinely periodic chirp: replacing n by n+N changes it by 2Nn. Consequently modular index wrap in every Hankel matrix is legitimate. This is the Phase44 order-2N-root convention, not the older w^(b n^2) convention; sign and family distinctions must be retained.

## Repair of the small branch

For N=2,r=1,F5,psi=2,x=(1,0), every nonzero one-mode chirp has two nonzero coordinates, so the input is outside the family. Its DFT nevertheless equals (1,1). This is the minimal positive-rank length counterexample: N=1,r>=1 contains every input; F5 is the smallest prime field with an order-four root.

The sealed code returns NONMEMBER, the ALL_PHASES gate, and one nonzero 2-by-2 cyclic-Hankel determinant for each of phases 0 and 1. Both determinants are 1. Optional direct fallback returns (1,1) while preserving NONMEMBER. The source's transform-only small return is not misrepresented as a historical classification theorem or rerun. The new API independently supplies the missing decision semantics.

For every 0<r<N with N<=2r, all N phases are explicitly enumerated. No phase is eliminated by a failed computation, a direct transform, or a budget failure. This is a complete finite search with rank witnesses, not an inference from the result of the original small branch.

## Why the eliminant gate is sound and exhaustive

For N>2r and nonzero x, choose its first nonzero coordinate c and s=c-r modulo N. Let e0=r(r+1)(r-1)/6 and D=r(r+1)(r+2)/6. Define

    P_t(u)=u^(-e0) det[x[(t+i+j) mod N] u^(ij)]_(0<=i,j<=r).

In the determinant expansion, the least possible exponent sum_i i*pi(i) is e0, attained uniquely by the reversal permutation; the largest exponent minus e0 is D. Therefore P_t is an ordinary polynomial of degree at most D. For t=s its constant is the reversal sign times x[c]^(r+1), which is nonzero in every admitted field. This argument survives small positive characteristic and singular other minors.

For a true phase b, dechirping the Hankel entries contributes nonzero row and column factors and the mixed term w^(-bij). Thus the dechirped consecutive (r+1)-minor is a nonzero scalar multiple of the raw determinant evaluated at u=w^(-b). Rank at most r forces both P_s and P_(s+1) to vanish there. Every true phase therefore belongs to the producer's candidate list.

The verifier independently recomputes the two coefficient arrays from raw x, checks equality with the supplied gate, evaluates both at every one of the N distinct grid points, and computes the candidate list itself. The ordered exclusions must match that entire list exactly. Missing, duplicated, reordered or substituted phases fail verification. A zero adjacent polynomial is allowed; a nonzero P_s always remains. An empty common-grid-root set is a valid complete negative certificate with no minor records.

The direct common-grid-root scan has exactly the same surviving phases as a correctly computed GCD would have. It is not a GCD speedup claim, and the sealed implementation retains the explicitly charged permutation coefficient kernel. Since P_s is nonzero, there are at most min(D,N) surviving phases.

## Why a cyclic-Hankel minor decides every surviving phase

For a fixed phase, write y[n]=sum_(a in T)c_a w^(an) with every c_a nonzero. The (r+1)-by-N cyclic-Hankel block factors as V diag(c) E. Its consecutive-row Vandermonde factor V has rank min(r+1,|T|); E has independent rows and hence a right inverse. Therefore the block rank equals min(r+1,|T|).

If |T|>r, some r+1 columns form a nonsingular square minor. The producer returns their original column indices and its exact nonzero determinant. The verifier rebuilds the indicated matrix from the raw input and phase, recomputes the determinant, and checks the claimed value is nonzero and equal. The first r+1 rows suffice; arbitrary row subsets are unnecessary.

If |T|<=r, the selected original columns span a |T|-dimensional space. Restricting that column space to the first |T| rows is injective because the corresponding square Vandermonde factor is invertible. Consequently those selected columns also give an invertible |T|-by-|T| recurrence solve. Its relation holds at every cyclic index, and its polynomial is exactly product_(a in T)(z-w^a). The full root-grid scan recovers T, normalized Fourier sums recover all amplitudes, and a final reconstruction checks every raw coordinate.

This handles cancellations, singular leading minors, leading zeros, nonzero data whose first samples vanish, and multiple valid phases. No prefix-BM failure or generic-position assumption enters. The zero input uses the empty support. Nonzero rank-zero rejection uses a witnessed nonzero raw coordinate. When r>=N every input is a member at phase zero with its full normalized ordinary spectrum. N=1 is included.

## Positive soundness and all output values

The verifier checks canonical distinct sorted support indices, nonzero amplitudes, cardinality at most r, and every raw coordinate. When a recurrence is present it recomputes its product from the frequencies. Omitted recurrence is expressly allowed; omitted support or amplitude information is not. Raw reconstruction alone establishes positive membership independently of the discovery procedure.

For a recovered phase b, put g=gcd(b,N), L=N/g and b'=b/g, including b=0 as g=N,L=1. Translation by L multiplies the chirp by epsilon=(-1)^[b'L(1-g)]. Fourier support is therefore the affine coset kappa+g Z_N, with kappa=0 if epsilon=1 and kappa=g/2 otherwise. In the latter case g must be even. This need not be the subgroup through zero.

The exact identity chi_b(n)w^(-bn)=psi^[-b(N+1)]chi_b(n-1) gives

    G_b(k+b)=psi^[-b(N+1)] w^(-k) G_b(k).

Since gcd(b',L)=1, stepping by b covers the entire permitted coset. One directly evaluated N-term seed and the recurrence determine it. If that seed were zero, the whole transform of the nonzero chirp would vanish, contradicting Fourier invertibility. Finally X[k]=sum_a c_a G_b(k-a). The implementation checks nonzero seed and orbit closure and writes all N entries, including zeros.

Independent full-output comparisons verify the sign and shift. In particular N=14,b=2,F29,psi=2 has support exactly the odd indices. An N=8,F17 order-16 chirp also supplies a strict rank-one extension beyond the older w^(b n^2) family: all older dechirps have eight nonzero Fourier coefficients. None of this changes the separate Q13 result.

## Paid work and operational limitations

For the large branch, with C=min(D,N), the stated field-operation bound covers the two factorial coefficient polynomials, the complete ND grid scan, all C attempted cyclic-rank tests and minor constructions, positive extraction and reconstruction, the Gauss seed/orbit, all N outputs, and certificate materialization. The explicit factorial term is O((r+1)!(r+1)) field work; permutation-sign/index control adds O((r+1)!r^2). Candidate rank work is O(C[N(r+1)^2+(r+1)^3]); inversions are separately bounded and implemented by metered binary exponentiation in the prime field.

For the small branch the N-phase rank tests cost O(N^2(r+1)^2+N(r+1)^3), which is O(N(r+1)^3) under N<=2r. For r>=N the dense spectrum costs O(N^2)<=O(rN). Thus fixed-r exact-field arithmetic remains O_r(N); this is not a uniform efficient-in-r FFT theorem. The workspace/certificate bound O(N+D+C(r+1)+(r+1)^2) includes failed-phase records and materialized full output.

Primality trial remainders, exact-order root preparation, checked inversions, selected reads/writes and final certificate/output materialization are charged. At p=998244353 the independent control observes 15,797 trial remainders; inverse exponent-bit counts equal the number of inversions times 30. The root-order sequence has 2N checks and is not cached across calls.

Rejected direct fallback adds N^2 field multiplies, N^2 field additions, N field writes and N final return writes. For the N=2 counterexample the independently verified ledger increment is exactly (4,4,2,2) in those categories. It uses only the already validated N-root; it is a quadratic direct fallback with no Bluestein/NTT claim.

The budget is a selected exact-field/data-event model, not a bound on all Python instructions, parsing, arbitrary-size integer bit operations, container comparisons, allocation, elapsed time, or operating-system memory. The contract expressly disclaims those stronger readings. General exact-field preparation/discovery must be added as P_K and R_K if needed; the supplied-root implementation does neither for free.

MEMBER/NONMEMBER are definitive only with their complete returned certificates. INVALID, UNSUPPORTED and LIMIT withhold both certificate and output. A finite budget never implies negative membership or validates a partial certificate. The admitted dimension/rank rectangle is not a promise that every valid input finishes within the 50,000,000-unit maximum. The essential distinction is: the mathematical certificate construction is complete; the bounded executable is resource-limited. A fresh default-cap endpoint confirms that N=4096,r=8,F65537,psi=6561,x=all ones returns LIMIT at exactly 50,000,000 units, with both certificate and values null. The input is plainly a member at phase zero; LIMIT is indeterminate, not an erroneous rejection.

## Independent evidence and stopping condition

Fresh reviewer code imports only the sealed new public classify/verify API. Its arithmetic oracles use exact Fourier sums and a division-free subset-DP determinant, not the producer's Gaussian elimination. An independently assembled subset-DP polynomial checks rank-one through rank-eight determinant identities. Neither uploaded original implementation nor prior reviewer implementation was imported or executed.

INDEPENDENT_RESULTS.json records 10,775 complete decisions: 3,635 MEMBER and 7,140 NONMEMBER. These include 10,169 exhaustive small-field/alphabet decisions, 465 all-phase structured cases and 135 additional deterministic-random cases. It separately checks 69,537 full-output coordinates, 26,461 reconstructed raw coordinates, 47,882 eliminant-grid determinants, 17,338 explicit nonzero minors, 656 independent polynomial identity points and both genuine large-regime rank-seven and rank-eight decisions. Their measured work is 4,441,210 and 47,909,610, respectively; high-rank evidence is not restricted to N<=2r.

ADVERSARIAL_RESULTS.json records 4,269 classifier and 2,498 verifier every-unit cutoffs across 11 representative paths, 22 exact cap-boundary replays, 368 malformed-certificate/output rejections, 14 invalid-domain controls, three unsupported-domain controls, four invalid-budget controls and three invalid-fallback-type controls. It checks zero, nonmember and rank-one inputs at N=4096, including all output entries and the 8,192 root-order checks. Certificates with cyclic metadata, oversized metadata trees, Boolean/integer aliases, missing phase records, altered gate coefficients, invalid columns, false minors, malformed support and wrong transform values fail closed.

The separate author-script replay is identified as replay, not counted as new independent cases. Its recorded 7,031 decisions and associated cutoff/content controls are additional corroboration only. Review acceptance rests on the proof and fresh independent controls above. The final source binding is rechecked after execution; the verdict applies only to the exact candidate hashes listed here.

The default-cap endpoint and exact four-file author replay pass. The release replay and final-byte readback receipt bind this completed review to the supplied bytes. Further generic FFT, efficient growing-r, extension-field implementation or priority claims require new evidence and are not follow-on consequences of this verdict.
