# ALG-034: independent review of the dyadic zero and one-shot precision policy

16 October 2026. FINAL VERDICT: ACCEPT the scoped conditional mathematical policy below. One precision-dependent cap wording repair was required and verified before acceptance. No outstanding required repair.

## 1. Scope and current task

The new result is an exact projected-zero decision and a finite sufficient precision plan for dyadic N and exact complex common-grid dyadic input. It is conditional on the accepted specified serial fixed-point producer actually executing with its complete premises. It is not a source-authenticated implementation of that producer, a stable fast backend, a replacement of the original arbitrary-length problem, or an execution of the accepted bounded wrapper.

I contacted the author before testing and read the exact retained v14 definition, accepted serial producer theorem and independent acceptance, accepted mathematical bridge, accepted bounded-wrapper review, and public input contract. SOURCE_INTEGRITY.json records their byte identities. I independently fetched the complete v14 body at repository baseline 4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a. Its SHA-256 a0a5d23b1ca51bfe2b2734d64ee4cf0cce61e7735eac04a060a99430749113ef matches the separate local antecedent exactly.

I also independently reread the current workbook ranges Catalogue!AC19:AF19, 'novelity breakthough'!W20:Z20, and 'Research overview'!N30:Q30. They retain the genuine-producer, all-size-adapter, justified-policy, and valid-downstream-integration stopping condition. This subcase does not satisfy that full condition. Broader ALG-034 status remains OPEN, with the inherited priority 48 unchanged. No workbook or repository write was made.

## 2. Exact zero decision

Let N=2^m, m>=2, D=N/2, and zeta=exp(2 pi i/N). Then i=zeta^(N/4). For the actual even-length phase convention, h=N mod 2=0 and

S_(b,t)=zeta^[a t(t-1)/2+(a s_b+beta)t].

If x_j=(u_j+i v_j)2^-F with exact signed integers u_j,v_j, then 2^F d_b is an integer polynomial in zeta. Add u_j at the phase exponent and v_j at the exponent plus N/4, reduce exponents modulo N, and replace zeta^(j+D) by -zeta^j. The resulting h_b has degree less than D.

The polynomial X^D+1 is irreducible over Q: after substituting X+1, all intermediate binomial coefficients are even, the constant term is 2 and is not divisible by 4, and the leading coefficient is 1. Eisenstein at 2 applies. Therefore h_b(zeta)=0 exactly if every reduced coefficient is zero. A numeric tolerance or small computed summary is not used.

The source map has (P x)_(s_b+t)=conjugate(S_(b,t)) d_b with no 1/ell_b factor. Its exact norm satisfies ||P x||_2^2=sum_b ell_b |d_b|^2. Because every block has positive length and the Fourier transform is unitary, Y=U_N P x vanishes exactly when every h_b is zero. This can hold with x nonzero.

An EXACT_PROJECTED_ZERO policy result therefore establishes Y=0 for the supplied exact x and state, but does not establish x=0. It cannot be serialized as the old wrapper's EXACT_ZERO_INPUT contract. ZERO_APPROXIMATION continues to mean only that the stored approximation is zero, with no exact-target conclusion from a positive radius. The three facts must remain separate.

## 3. Nonzero signal floor

For any nonzero h_b, put A_b=sum_j |h_(b,j)|>=1. Every Galois embedding zeta -> zeta^r, r odd, maps the polynomial value to one of magnitude at most A_b by the triangle inequality. The field norm is a nonzero integer. Equivalently, multiplication by h_b in the basis 1,zeta,...,zeta^(D-1) is a nonsingular integer matrix, so its determinant is a nonzero integer. Thus

1 <= product_(r odd) |h_b(zeta^r)| <= |h_b(zeta)| A_b^(D-1),

and |h_b(zeta)|>=A_b^(-(D-1)). The selected minimum nonzero A_b is legitimate and maximizes this particular bound. Cancellation during exact coefficient reduction may materially improve it; no field norm or determinant has to be computed by the policy.

Writing A for that selected value, K=ceil(log2 A), W for the actual maximum Cartesian input-numerator width, e=W-F, and G=W+(D-1)K, the candidate floor

mu=2^(-F-(D-1)K)=2^e 2^-G

satisfies ||Y||_2>=mu. The degree and coefficient mass cannot be discarded from the bound. This is a data-dependent finite lower bound on the exact-input domain, not a positive uniform floor for every nonzero complex input.

These norm facts are classical. Milne's Algebraic Number Theory, Corollaries 2.20 and 2.21, gives respectively the embedding product and integrality statements; both were independently opened at https://www.jmilne.org/math/CourseNotes/ANT.pdf, printed page 32 (PDF page 33). No novelty or priority conclusion follows.

## 4. Precision plan and scale audit

Retain the exact accepted C=64 H B_A 2^B_A N^2, H=min(binomial(N+B_A-1,B_A),2^(N-B_A)). The genuine specified producer returns Delta=2^e C 2^-p and ||Yhat-Y||_infinity<=Delta. Let c=ceil(log2 C), Pq=16m+16, rho=2^-Pq. The candidate plan is

p*=max(W,c+t+1,c+Pq+G+2), for integer t>=0.

The first two terms supply exact input loading and 2C2^-p<=2^-t. The last gives Delta<=rho mu/4. Since sqrt(N)rho<1, the reverse triangle inequality yields

||Yhat||_2 >= mu-sqrt(N)Delta > mu/2 >0.

The accepted normalization has lambda>=||Yhat||_2 and alpha=lambda/d with d in {1,2}; hence alpha>=||Yhat||_2/2>mu/4. Therefore Delta/alpha<rho. The strict margin is valid even though the wrapper's exact check also accepts equality.

This is a sufficient one-shot theorem for the already specified producer. It does not assert that the historical blocked FFT, a different rounding schedule, an unverified phase table, or a forged declaration satisfies the upstream bound. A failed plan or failed actual sufficient guard is not an observed error lower bound.

Scaling is consistent: Delta/mu=C 2^(G-p), so F cancels exactly. Absolute exponents remain encoded integers. For the accepted N=64, B_A=3 kernel x=e_0-e_1, all summaries are zero. For x_K=e_0-(1-2^-K)e_1, the common-grid numerator summary is 1, so A=1, K_coefficient=0, and G=W=K+1. The plan still grows with the paid input width; exact cancellation does not erase near-kernel precision dependence.

The second ideal unitary negative-sign transform still gives U_N(Y/alpha)=R P x/alpha. I independently checked the corresponding exact unnormalized identity F_N^2=N R in the quotient ring. No extra sqrt(N) factor is introduced, and the target does not become U_N x.

## 5. Resource and implementation boundary

The policy must read the original exact input and state, calculate W, build and zero-test all reduced block polynomials, and accumulate their coefficient masses. Dense degree-D arrays cost O(B_A D) initialized/scanned coefficient slots in addition to the N inputs. With h=O(W+log N) coefficient width, a straightforward streaming design pays O((N+B_A D)h) bit additions/reads/writes plus exact phase-index arithmetic and encoded-exponent costs, retaining O(Dh) scratch beyond input and output. The factor D is real. A sparse variant would require its own data-structure ledger.

Constructing C, K, G and p* uses exact integer arithmetic at their actual widths. A symbolic mu does not require expanding 2^|F| or materializing A^(D-1). The full accepted serial-producer ledger remains due at this selected p*, including root construction, B_A^2 coefficients and seeds, NB_A recurrence work, normalization, scan, input/output storage, and exact-width arithmetic. Subsequent normalization, copied immutable source construction, all Q16 window preparation and calls, reconstruction, and final outputs are additional work. There is no fast or sub-FFT conclusion.

The old deployment wrapper requires 4<=N<=4096, output numerator magnitude widths <=65536, metadata fields <=256 bits except C<=16384 bits, and its exact grammar. For the policy's choice p=p*, its sufficient stored-width bound is p*+I, with I=B_A+2m+10. If a larger actual p is used, the check must use p+I and kappa=W-F-p. Failure of that sufficient upper certificate is only SUFFICIENT_CAP_NOT_ESTABLISHED; it does not prove the actual produced numerators exceed the cap, nor authorize silently increasing the accepted cap.

A concrete independent example is N=4096, B_A=3, one real numerator 2^53-1, all other coordinates zero. It gives p*=108823 and I=37, so the upper certificate exceeds 65536. This harmless exact-input example demonstrates the conservatism and deployment limitation; it is not a numerical failure. No theorem-scale sparse Q16 instance is covered by the old N<=4096 wrapper, and no new all-size adapter is delivered here.

Source identity is separate from numerical validity. The exact original x, grid, state, p*, intended embedding, arithmetic/range contract and returned Yhat must be bound together. Digest equality and attestation strings cannot establish that a genuine producer ran. This report and the author's exact algebra/planning controls do not implement or authenticate one.

## 6. Independent controls

The independently authored independent_controls.py imports only Python standard-library modules. It imports or executes no author, historical, wrapper, or Q16 program. It passed 32,342 assertions, detailed in INDEPENDENT_RESULTS.json:

- 19,863 comparisons of separately constructed phase/reduction routes, including exhaustive {-1,0,1}^8 complex numerator data at N=4 and larger selected states through N=32.
- 1,538 exact Galois-product integer norms, nonzero equivalences and embedding coefficient-mass checks in each category.
- 16 exact projected-energy, Fourier-reflection and projected-zero identities in each category, through N=16.
- Exact original-zero distinction, complex-phase kernel, N=64 nonzero kernel, and eight near-kernel inputs with widths through 65,537 bits.
- 153 precision plans in each relevant category through N=4096, 765 symbolic scale-cancellation checks including F=+/-10^30, and explicit sufficient-cap failures.
- A negative control showing that removing the degree-dependent floor term invalidates the stated sufficient planning inequality. It is not a lower bound on every algorithm's required precision.

Finite controls corroborate the independent algebra and arithmetic implementation. Universal correctness is supplied by Sections 2-4 and the accepted producer/bridge premises, not extrapolated from the test census. The candidate's fresh control source was read as text only.

## 7. Final disposition

ACCEPT the frozen report REPORT.md, SHA-256 b2578bccccdd4dfc95038c07cb625ee014ffda86cef35d73d764e356f78f9f9c, only for the dyadic exact-input mathematical policy subcase. Authentic execution, producer binding, certified fast backend, actual compatible integration, all-size source adapter, original-input Fourier recovery, practical performance and global novelty remain open. The accepted bounded wrapper is neither reopened nor enlarged.


## 8. Frozen-object and change audit

CANDIDATE_FREEZE.json binds the report, source bindings, proposal, author control source, and its result receipt. The final report was reread after the author explicitly chose actual p=p* and required a fresh p+I/kappa check for any higher actual p. I requested and verified that repair; using the smaller planned precision to certify a larger actual run would be unsound. The exact canonical state guards were also made explicit.

The author's accepted archive provenance was independently checked, rather than merely accepted from metadata: I fetched both baseline repository manifests, computed the local archive SHA-256 and Git blob SHA-1, and matched all five source bodies three ways against local originals, candidate snapshots, and exact ZIP members. ARCHIVE_INTEGRITY.json records the matches. No remote archive binary download is claimed. Conrad's cited Theorem 5.3, printed page 10, was also opened and supports the stated prime-power Eisenstein argument.

The two-cell proposal is scientifically consistent with this acceptance. Its P30/Q30 preimages exactly match my independent live read, and prior cell text is preserved verbatim. Application remains a separate parent action requiring a fresh conflict check and any appropriate authorization. No source link may be invented. The overview, Catalogue and novelty statuses, parent priority, historical accepted wrapper, and full stopping condition must remain unchanged except for an accurately scoped description of this new subcase.
