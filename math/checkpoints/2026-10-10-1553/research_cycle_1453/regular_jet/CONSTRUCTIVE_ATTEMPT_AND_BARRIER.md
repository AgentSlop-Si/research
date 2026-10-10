# Regular sparse-jet source: a fully specified four-Green attempt and its obstruction

Date: 10 October 2026. Task: canonical Research queue Q31, row 34.

## Outcome

The explicit origin-regular source below has uniformly charged O(N) work at every dyadic length and uses the current Necklace carrier. It is a genuine inexpensive scalar family, but **no choice of its four natural-cycle constant gains or scalar branch coefficients gives the Fourier quadratic jet once N >= 1024**. A two-sided denominator-clearing proof establishes this for all admissible fields and all such parameter choices, rather than just sampled ones.

This closes a specific constructive specialization of the current strongest candidate. It does not close Q31, exclude four independently ordered/variably weighted Green maps, or give an unrestricted FFT lower bound. The accepted sparse-jet/Hessian compiler is unchanged and is not presented as a new result.

## 1. Exact current contract and source lineage

The current Sheet is `Research cycle — accepted proofs and live fusion queue — 10 October 2026`, Research queue row 34, Q31. Its recorded state remains “Construction blocked”; its conditional proof is closed. The latest bound snapshot inspected is `research_sheet_1435/ALL_BOUNDED_FINAL.json`, SHA-256 `86808838396f8873e308b21c653e9b84dfad1a8334879d5a2966466fe8b94c7f`.

The original required object is one uniformly generated scalar straight-line program Phi_N, regular at the input origin, whose formal degree-two restriction to every one/two-coordinate plane is that of

    Q_N(x) = (1/2) x^T F_N x,    F_N[i,j] = omega^(ij).

All scalar preparation, code generation, indexing, fresh-input work, and all N output writes are charged. The intended new source must have total work o(N log N), ideally O(N log log N), independent of an imported exact Fourier algorithm. Formal identities, rather than finite-field pointwise equality, are required. Storage from the accepted compiler is O(s+N), not automatically O(N).

The 13:00 and 14:03 Sheet continuations specifically add the Necklace transport obligation:

    H_N = Hessian_w Psi_N(gamma_N),    P_N^T H_N P_N = F_N.

Equivalently the transported matrix T must satisfy both T e_0 = ones and T S = D_omega T. The source carrier is cheaply evaluable; the missing object is the generated transport with its exact identity and paid application/transpose, not another proof of differentiation.

Bindings:

- Original sparse-jet THEORY.md: SHA-256 `94da2df24bd6f6bc073b35ab3c8cc0c0d57d94e1b1ee0d4a860a1fc4458f5af1`.
- Necklace archive: SHA-256 `afd7a3dc1ed24109cb57f90f714ae0242224b8d029030b5e3b450a6ed85ac183`.
- Necklace THEORY.md: SHA-256 `8f9e1d4a0de9826fba802e885f7cff244119dffcb543153d6a25173c804eaaea`.
- Paths and other read-only source hashes are in SOURCE_BINDINGS.json. No supplied research program was executed or imported.

## 2. Construct the candidate before testing its Fourier identity

Let N=2^n, n>=1, over a field K of characteristic other than 2 containing the supplied primitive N-th root omega. Define S e_j=e_(j+1 mod N). Use the binary graph edges (s,b): s -> 2s+b mod N, with 2N edge coordinates. Let k=n+2 and

    gamma_(s,0)=1,    gamma_(s,1)=omega^s,
    Psi(w)=tr(B(w)^k).

The accepted necklace identity represents Psi as a sum over length-k binary necklaces C with coefficient equal to the least period of C. Each monomial has its repeated edge occurrences retained. Uniform enumeration plus edge/constant generation and scalar circuit emission costs O(2^k)=O(N). This accepted cost is not reproved here.

Choose four scalar gains a_1,...,a_4 with a_l^N != 1 and four scalar coefficients lambda_1,...,lambda_4. All may depend on N if their generation is paid. Define

    G_a=(I-aS)^(-1),
    P_0=lambda_1 G_(a_1)+lambda_2 G_(a_2),
    P_1=lambda_3 G_(a_3)+lambda_4 G_(a_4),
    (Px)_(s,0)=(P_0 x)_s,    (Px)_(s,1)=(P_1 x)_s.

This is the source four-Green grammar restricted to the common natural cycle and constant edge gains, with optional scalar branch coefficients. The source's equal coefficients are the lambda_l=1 case. There is no Fourier matrix inside its implementation: each Green map is a two-pass cyclic recurrence y_j=x_j+a y_(j-1), closed with the nonzero denominator 1-a^N.

For a literal uniform characteristic-zero instance at every dyadic N choose gains (2,3,5,7) and all lambda_l=1. Computing gains, their powers/denominators, the N root powers, all edge addresses, and all code has O(N) work. The modular controls use another explicitly listed safe four-gain tuple; no finite-field root selection is smuggled into the theorem's supplied-root model.

Center the scalar source:

    Phi(x)=Psi(gamma+Px)-Psi(gamma)-g^T Px,
    g=gradient Psi(gamma).

Thus Phi(0)=0 and gradient Phi(0)=0. This centering matters: the uncentered source alone need not meet the original constant/linear jet contract. Its gradient can be prepared in O(N) by accumulating the first derivative of each orbit monomial, using prefix/suffix products or the nonzero canonical baseline. The Hessian is unchanged:

    Hessian Phi(0)=P^T H P,    H=Hessian Psi(gamma).

All source inversions are input-independent and guarded; Phi is a polynomial in x with prepared field constants, hence origin-regular. It is a legitimate short source family. The next section decides whether it supplies the Fourier jet.

## 3. General two-sided denominator-clearing theorem

**Theorem.** Let H be any symmetric M-by-M matrix with at most Delta nonzeros per row. Let R be an M-by-N matrix with at most s nonzeros per column and d per row. Let

    q(t)=sum_(a=0)^r q_a t^a,    0<=r<N,    q_0 != 0,
    Q=q(S) invertible,    P=R Q^(-1).

If P^T H P=F_N, then

    N-r <= s d Delta.                                      (1)

The field need only contain the primitive root, and all operations are algebraic. There is no conjugation, absolute-value hypothesis, positivity condition, or generic-coefficient assumption. Zero entries/cancellations in H or R only improve the support upper bound.

**Proof.** Fourier equality implies

    Q^T F_N Q=R^T H R.                                    (2)

Since Q is diagonalizable on the N Fourier characters, invertibility is equivalent to q(omega^j) != 0 for every j. For fixed j and the convention S e_j=e_(j+1), the left side has exact entries

    (Q^T F_N Q)_(i,j)
      = sum_(a,b) q_a q_b omega^((i+a)(j+b))
      = omega^(ij) L_j(omega^i),
    L_j(z)=sum_(b=0)^r q_b q(omega^(j+b)) z^b.             (3)

Here L_j is a polynomial of degree at most r and has nonzero constant term q_0 q(omega^j). It therefore vanishes at at most r of the N distinct values omega^i. Every column of Q^T F_N Q has at least N-r nonzeros, giving total support at least N(N-r).

A row of R^T starts on at most s carrier coordinates. Applying H reaches at most s Delta carrier coordinates. Each of those rows of R reaches at most d output coordinates. Consequently every row of R^T H R has support at most s Delta d, and its total support is at most N s Delta d. Comparing total supports in (2) proves (1). This total-support comparison avoids any row-versus-column ambiguity. QED.

The q_0 hypothesis is a convenient sufficient guard for the displayed constant-term proof. We retain it rather than silently broadening the certificate. It always holds for the candidate denominator below.

This theorem is not the previous sparse-P marking bound: P is dense here. Sparsity appears only after the explicit common denominator Q has been paid and cleared. Nor is it the previous one-sided Cayley feedback proof: the arbitrary symmetric H remains between two transports, and T need not be a rational function of S.

## 4. Apply the theorem to all four-gain choices

Put

    q(t)=product_(l=1)^4 (1-a_l t),
    r_0(t)=lambda_1 product_(l !=1)(1-a_l t)
           +lambda_2 product_(l !=2)(1-a_l t),
    r_1(t)=lambda_3 product_(l !=3)(1-a_l t)
           +lambda_4 product_(l !=4)(1-a_l t).

The Green guards make Q=q(S) invertible; q(0)=1. Commutativity of scalar polynomials in S gives

    P Q=R,    R x=(r_0(S)x,r_1(S)x)

in the two edge blocks. The edge reordering from blocked to interleaved source notation is a fixed permutation and changes no support count. Every r_b has degree at most 3, including repeated or zero gains and vanishing lambda coefficients. Thus d<=4 and s<=8, while r=deg q<=4.

The already accepted short-orbit locality bound is

    Delta <= k 2^max(0,k-n-1)=2(n+2).

It holds for every choice of orbit coefficients and baseline, not just the canonical ones. Therefore a necessary condition for this four-Green specialization is

    N-4 <= 64(n+2).                                    (4)

At n=10 this reads 1020<=768, which is false. Moreover 2^n-4-64(n+2) strictly increases for n>=10. Hence every dyadic N>=1024 is excluded, for every legal four-gain/scalar-coefficient choice.

The conclusion remains true if one retunes the necklace coefficients or changes any baseline: the same carrier support bound survives, provided the horizon remains n+2. In particular, merely fitting different natural-cycle gains, changing the primitive-root embedding, or using a different constant-gain tuple cannot repair this attempted construction.

For a general accepted horizon k=n+c, exactly the same proof gives

    N-4 <= 32 (n+c) 2^max(0,c-1).                     (5)

For any fixed c, or 2^c=O(log n), the bounded four-Green attempt eventually fails. This is a necessary representation condition, not a runtime lower bound for a growing number of rational terms or general shared circuits.

## 5. Complete cold cost ledger

For fixed c=2, the candidate is inexpensive even though it is wrong as Fourier:

- Read N, the supplied root, fixed/scalarly supplied gains and branch coefficients; generate the N root powers: O(N) operations/storage. Root discovery and field construction are not silently claimed.
- Generate the two natural-cycle edge maps and all index/code addresses: O(N) word operations, with O(log N)-bit addresses.
- Check each 1-a_l^N !=0, compute its inverse, and generate each Green recurrence circuit: O(N) total; four scalar inversions, plus linear arithmetic. Scalar parameters themselves have no unpriced fitting step.
- Enumerate necklace representatives through k=n+2 and retain edge occurrences, orbit coefficients, and scalar circuit: O(2^k)=O(N) work and O(N) stored nodes, using the accepted FKM-based proof. No N-by-N Hessian is formed by the candidate.
- Prepare Psi(gamma), g and any derivative constants; add the centering subtraction: O(N) work/storage. Prefix/suffix products make the centering valid even at zero baselines in the broader family.
- Apply P, the scalar source circuit, and the accepted Hessian-vector compiler to a fresh vector: O(N) field/index work. Transpose application of each Green is also a pair of reverse scans with its own paid circuit.
- Emit all N values of P^T H P x: O(N) writes. These are not labeled Fourier outputs because (4) proves they cannot be so at growing sizes.

For k=n+c and K=O(log N), replace the source portion by O(N 2^c) work/storage; the four-Green portion remains O(N). The accepted sparse-Gram formula assumes nonzero baseline weights; the polynomial source/centering does not. If characteristic divides canonical k, its trace Hessian is zero, an existing stronger failure in that special case. The new obstruction needs no division by k and includes that case.

The independent controls deliberately build slow exact verification oracles. Their enumeration, dense small transforms, and support inspection are not claimed as the candidate's production executor, optimal arithmetic constants, or hardware benchmarks.

## 6. Hermite/Jordan continuation: exact compatibility and the remaining construction

The Phase 22 accepted family is x_t=h_t sum_i P_i(t) u_i^t with bounded total Jordan order R. Its O(N R^2+R^3) accepted-input algorithm, grid-root recognition, and interval recurrences do not give the Q31 origin-regular scalar source. The following pinpoints the interface rather than rejecting that structured algorithm.

1. **The blind mode selector itself has no regular origin extension.** Already for one mode, an origin-regular rational function U(b_0,b_1) agreeing formally with u on (b_0,b_1)=(a,au) for two different allowed roots u would give U(0,0)=u for both by setting formal a=0. This is impossible. A determinant/rational Prony chart also has vanishing denominators at zero. This excludes differentiating that selector. It does not exclude an invariant formula that eliminates the selector before evaluation.
2. **Fixed low-order linear encodings cannot repair the missing full jet.** If Phi=f(Ax) with A having R rows and f regular, its Hessian rank is at most R. Fourier rank is N. This is an inherited gate from the original sparse-jet theorem, recorded here solely to prevent a false new construction through a bounded Hermite/moment basis. Nonlinear encodings with their own curvature are outside this rank statement and need their entire scalar circuit charged.
3. **The full-order polynomial lift is an explicit circular factorization.** Assume characteristic zero or >N, distinct time nodes 0,...,N-1, and h_t!=0. Set V_(t,j)=t^j, D_h=diag(h_t), and Y=F_N D_h V. Every x has the full polynomial representation c=V^(-1)D_h^(-1)x, giving

       Y c=F_N x,    Phi(x)=(1/2) x^T Y V^(-1)D_h^(-1)x.

   This source is formally correct and regular, but Y has N^2 entries when all N jets are explicitly prepared, already requiring Omega(N^2) writes/storage. The supplied O(N R^2) recurrence, extended through degree N-1 where legal, gives no sub-N-log-N bound. Avoiding the table is the genuine next problem: one must implement the composite contraction Y V^(-1) D_h^(-1) without invoking Fourier or an unpriced generic transform. The identity alone does not implement it. Nor may the blind-recognition guarantee 2R<=N be applied at R=N.

The quasi-Hermite discriminant source was inspected as text. Its squarefreeness/exclusion-disk theorem removes a local algebraic guard in a different problem. It supplies neither a shared N-variable Fourier quadratic jet nor an inexpensive Fourier-compatible change of basis. No new FFT consequence is attributed to that accepted result.

## 7. Exact controls and their limits

`fresh_regular_jet_controls.py` is newly authored here and uses only Python's standard library. No source research module is imported. It sums closed binary words as a deliberately slow independent oracle, differentiates products by ordered factor positions, and separately propagates bivariate truncated jets.

The run in F_65537 passes:

- Six sizes N=2,4,8,16,32,64: 18 formal mixed-direction comparisons; 18 identities P Q x=R x; 18 direct-versus-root-polynomial checks of Q^T F Q; all 126 columns across those sizes checked for the support lower bound. For r>=N at the smallest sizes the numeric inequality is vacuous, not a claimed new theorem case.
- Four larger sizes N=256,512,1024,2048: sparse carrier construction and 16 selected cleared-column comparisons. The all-parameter threshold applies at 1024 and 2048; the smaller failures are only explicit fixed-gain negative controls.
- At N=1024, the universal lower/upper bounds are 1020 versus 768. In the four sampled columns, the actual cleared-carrier supports were 193, 228, 312, 199 while the cleared Fourier columns each had all 1024 entries nonzero.
- A bounded-two-moment control at N=8 explicitly annihilates v=(1,-2,1,0,...,0), whereas Fourier does not.

All checks are exact modular arithmetic. They corroborate orientation, centering-invariant Hessians, support counts, and the constructive equations. The all-N theorem comes from Sections 3–4. The checks do not establish global novelty, real/complex numerical conditioning, or the source's claimed production operation constants.

## 8. What remains worth constructing

The original broad candidate permits four distinct non-affine cycles, variable edge gains, diagonal masks, and other independently charged linear maps. This theorem deliberately does not exclude them. To escape this particular certificate, a proposed low-work transport must avoid a factorization P=R q(S)^(-1) with small-degree natural-cycle q and bounded row/column supports of R relative to the short-orbit Delta.

A meaningful next positive deliverable would therefore be explicit noncommuting transport formulas with no such cheap common denominator, plus an all-N proof of both the Fourier seed and covariance and a complete generator/application/transpose ledger. Merely choosing unrelated cycles removes this proof's premise; it does not establish the Fourier identity. Higher horizon or many rational terms must be charged and satisfy (5), not waved away as constants.

Q31 remains construction-blocked. No new discovery count or universal algorithm claim is warranted. This packet is a scoped constructive attempt resolved negatively, with a precise escape condition.
