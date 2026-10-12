# Independent Q11 two-call Fourier recovery review

Date: 12 October 2026 UTC. Verdict: **ACCEPT, bounded exact-arithmetic two-call sharpening of an already available reverse reduction**. This is neither a new FFT exponent nor a historical novelty claim. The broader Q11 representation/efficiency gate remains open.

## 1. Accepted statement and prior-result check

For q=483^m, m>=1, N=5q², a supplied primitive Nth root omega, L=Q(omega), F_ij=omega^(ij), h=(N+1)/2, A_ii=omega^(hi²), G=sum_i A_ii, c=NG, and B=(F^(-1)+A)^(-1),

    F=(1+c) B A B+(1-2c) B+c A^(-1).

This holds as a full N-by-N operator identity, hence on every x in L^N. The algorithm uses two sequential arbitrary-input calls to one prepared exact B evaluator, plus exactly 4N scalar multiplications and 2N additions under the stated literal schedule. Setup, copies, routing and output are additional paid work below. The reverse comparison already accepted in the research is the two-DFT formula for B. Together these give constant-factor mutual simulation in the exact ambient-field arithmetic model, with linear extra work and storage.

**This equivalence was already available with three B calls.** The pinned accepted odd-chirp review (SHA-256 c6c30444abc7563e8b02ee613abdd61103c1ce18ded3d39cff6fdb38452dad76), section 3, gives K=BA, the cubic annihilator, (I-K)^(-1)=(1+c)I+(1-2c)K+(1+c)K², and a three-B/two-A Horner evaluator. The pinned prior-feedback audit (SHA-256 dfea8a0a54f747e9af09acceb7d92b0345233731da03fe9ed0e86f4d26524c6a), section 2, explicitly writes

    F=(1+c)B+(1-2c)BAB+(1+c)BABAB.

A bounded local text search found those exact antecedents. It is not an exhaustive search of the repository, archived binary contents, all research versions, or external literature. The accepted difference here is reducing that three-call expression to two B calls and exposing its complete same-family cost. The result should not be advertised as discovering DFT/B complexity equivalence for the first time.

## 2. Independent derivation from the original definitions

The source files were copied and hashed as inert documentary inputs; no historical program was imported, executed, compiled or modified. The original Fourier sign, normalization, full dimension and chirp are retained.

Because 2h=1 modulo N, completion of the square gives, for T=AF,

    (T²)_ij=omega^(hi²) sum_k omega^(hk²+(i+j)k)
           =G omega^(-ij-hj²).

Thus T²=G Fbar A^(-1)=NG T^(-1), since F^(-1)=Fbar/N. Hence T³=cI. This uses the primitive-root geometric-sum identity at the original dimension; it does not assume a Fourier oracle is free.

For q odd and coprime to 5, residues x=q²u+5v are unique with u modulo 5 and v modulo q². The cross term of hx² is divisible by N. Let eta=omega^(q⁴), a primitive fifth root. The u-sum is g=1+2eta²+2eta³ because h=3 modulo 5. In the v-sum, write v=s+qt; only s=0 survives because 2,5,h are units modulo q. Therefore G=qg and g²=5, so

    G²=N, c²=N³=125q^6,
    (1+c)^(-1)=(1-c)/(1-125q^6).

The denominator is nonzero in characteristic zero for every positive q. This fixes the Gauss sign by the supplied root, rather than choosing a square root. The frozen q=483^m family satisfies oddness, coprimality with 5, and q=1 modulo 241. No root extraction or field extension beyond L is introduced.

From F^(-1)+A=(I+AF)F^(-1),

    B=F(I+T)^(-1), U=AB=T(I+T)^(-1).

I+T is invertible because (I+T)(I-T+T²)=(1+c)I. The matrices U,T commute as rational functions of T. Multiply

    (1+c)U²+(1-2c)U+cI

by (I+T)². Its numerator is

    (1+c)T²+(1-2c)T(I+T)+c(I+T)²
    =cI+T+2T²=T(I+T)²,

where the last equality uses T³=cI. Thus T=(1+c)U²+(1-2c)U+cI. Left multiplication by A^(-1) yields the displayed formula for F, with factor order B A B exactly as written.

The prior result contracts directly too. Let K=BA; its relation is

    (1+c)K³-3cK²+3cK-cI=0.

Multiplying the prior three-B formula by A on the right gives (1+c)K+(1-2c)K²+(1+c)K³. Substitution of the cubic leaves cI+(1-2c)K+(1+c)K². Multiplication by A^(-1) gives the same two-call identity. This makes its relationship to the existing result explicit.

## 3. Exact oracle contract and paid cost

The comparator is an evaluator for the full B_N at the same q,N, root, field, ordering and normalization. It must accept every exact input in L^N and return all N exact outputs. A basis-column oracle, restricted structured-input algorithm, approximate oracle, advice for one fixed x, or a five-coordinate principal-block method does not meet this contract.

Prepare the scalar a=1+c, b=1-2c and the diagonal d_i=c omega^(-hi²). For input x execute:

1. v=B x.
2. w=A v: N multiplications.
3. z=B w, using the same prepared oracle on its actual arbitrary input.
4. y_i=a z_i+b v_i+d_i x_i: 3N multiplications and 2N additions.

The overhead counts products by 0 or 1, with no data-dependent savings. Retaining v and x across calls is necessary. Copies, allocation/initialization, every address access, and all N output writes cost O(N) word/data movements. A destructive oracle needs the corresponding preserved copies. Oracle scratch can be reused sequentially; extra storage is O(N) field elements and O(N) index words. No second independent B preprocessing is required if the prepared oracle is reusable; if the actual interface requires rebuilding, that cost must be charged.

Let M_B,A_B be one prepared-call arithmetic costs. The constructed forward evaluator costs

    M_F <= 2M_B+4N, A_F <= 2A_B+2N.

With no previously shared tables, construct P[e]=omega^e in N-1 multiplications and d_i=cP[-hi²] in N multiplications. A entries use P[hi²]. Thus extra table work is 2N-1 multiplications, O(N) reads/writes and storage, plus explicitly paid scalar synthesis, supplied-root checks and integer indexing. q,N,h and scalar constants can be synthesized in O(log N) field/word arithmetic as appropriate. Powers and indices use a fixed number of O(log N)-bit words; unit-cost unbounded integers are not assumed. Certified root input may skip its checks; otherwise omega^N=1 and omega^(N/p)!=1 for p=3,5,7,23 are checked in O(log N) field operations. Constructing or selecting an exact root is not hidden in either oracle's cost.

For r inputs with reusable B preparation P_B and standalone extra table setup E, charge P_B+E+r(2C_B+linear overhead). If supplied B advice is not uniformly generated, the consequence is an equally advised/nonuniform F circuit, not a uniform fast Fourier algorithm. A cold speed claim must include actual B preparation. Expanded Green endpoint artifacts retain their own output-size cost; this reduction does not construct them.

## 4. Same-family comparator; no new FFT proof

The pinned existing full-target formula is

    B=rho F-rho G D Fbar D+rho c D,
    rho=(1+c)^(-1), D=A^(-1).

Fbar is the reversed-exponent transform, not conjugation of arbitrary input data. It is F followed by the paid output reversal i -> -i. With prepared coefficients rho, e_i=-rho G D_ii, f_i=rho c D_ii, one B application takes two forward-F calls, N multiplications for D x, 3N scalar multiplications and 2N additions for the three-term combination, and O(N) paid routing:

    M_B <= 2M_F+4N, A_B <= 2A_F+2N.

Its standalone extra power/coefficient table setup costs 3N-1 multiplications plus scalar/root setup and O(N) word work. This 4N overhead describes that explicit F/Fbar schedule, not an optimal constant. The equivalent existing formula B=rho[F-F A F+cA^(-1)] admits a tighter schedule: r=Fx, s=F(Ar), y=rho(r-s+D_c x). With D_c=cA^(-1) prepared, its overhead is exactly 3N multiplications and 2N additions, and it shares the reverse reduction's 2N-1 table setup. Thus M_B<=2M_F+3N is available as well. This is the already present two-DFT evaluator. The two inequalities mean constant-factor cost equivalence up to linear work in this model, not equality of best constants, equal wall time, or an FFT lower bound.

For transparent numerical comparison only, use the same literal bounded-radix direct-small-transform schedule as the accepted shared-bank packet. A length N=5*3^(2m)*7^(2m)*23^(2m) Fourier transform has (66m+5)N multiplications and (60m+4)N additions. The literal F/Fbar B comparator therefore has (132m+14)N multiplications and (120m+10)N additions. The tighter F-F A F schedule has (132m+13)N multiplications and the same addition count. No optimality claim attaches to these deliberately literal counts.

The accepted shared-bank B evaluator has (66m+11)N-75 multiplications and (60m+10)N-75 additions. Substitution into two-call recovery gives (132m+26)N-150 and (120m+22)N-150 respectively. This is still O(N log N), as expected; it is not a new exponent improvement, and these counts exceed the literal direct-DFT schedule above. At m=1, shared-B recovery takes 184,298,160 multiplications and 165,635,040 additions; direct DFT takes 82,817,595 and 74,652,480. These are algebraic operation counts, not timings.

## 5. Preserved limitations

- Field growth: [L:Q]=phi(N)=1056*483^(2m-1), proportional to N. A unit L-operation is not one fixed-cost machine operation. Input, output and intermediate canonical coordinate sizes, coefficient heights, modulus arithmetic and conversions must be paid. In a bit model the second B call may receive larger-height data; replacing it by another cost at the original height is unjustified.
- Approximation: there is no stability equivalence. With exact surrounding arithmetic and a uniform operator approximation B+E, ||E||_2<=epsilon, the recovered error is bounded by |1+c|(2||B|| epsilon+epsilon²)+|1-2c|epsilon. Here ||B||<=sqrt(N)/(sqrt(N)-1), |c|=N^(3/2), and ||F||=sqrt(N), so this elementary relative bound can grow on the order of N epsilon. Separate approximate calls with uniform input-relative error satisfy the same bound. Rounded roots, coefficients and arithmetic require further analysis. Good conditioning of B alone does not prove stable recovery through a cancellation-prone formula.
- Grammar: the operation B A B composes two B evaluations. If B is a sum of legal diagonal-ended Hamiltonian-cycle Green branches, expansion produces products of Green maps with a middle diagonal. Such products are not generally individual permitted branches or a sum with the same branch count. The extra diagonal is legal only when represented/charged under the chosen grammar. The algorithmic reduction does not preserve additive Green branch counts, matching/coloring constraints, or their restricted lower bounds.
- No unrestricted circuit lower bound, new O(N) B construction, all-length FFT theorem, negative-chirp theorem, finite-network exponent comparison, numerical-speed result, or historical novelty conclusion follows. The two-call count is not proved minimal among every computational architecture.

## 6. Fresh independent evidence

check_symbolic.py is newly authored standard-library code. It checks the exact integer-polynomial residual after T³=cI, the independently cleared rational substitution, the direct contraction of the prior three-call expression, g²=5 in the fifth cyclotomic ring, all six documentary source hashes, and exact integer family/cost controls for m=1 through 8. It rejects a perturbed polynomial residual. The all-m conclusion is the proof above, not extrapolation from the parameter controls.

check_reduction.cpp is newly authored and separately implements the defining Fourier convention, exact finite-field B via the known two-transform formula, direct Gaussian inversion for small defining matrices, and the proposed two-call schedule. No candidate or historical program is imported or run.

Fresh exact controls at q=1,3,7,11,483 check all outputs, direct dense Fourier values through N=605, every basis input at N=5 and 45, and (F^(-1)+A)B x=x on both actual oracle inputs. The small q controls are outside m>=1 and are explicitly algebra/model tests. The true smallest-family test has N=1,166,445, p=18,663,121, omega=65,536; all 1,166,445 recovered outputs pass. It performs complete transform evaluations but never constructs an N² matrix. Instrumentation confirms 4N multiplications and 2N additions above two B-call costs. A wrong coefficient sign and one-coordinate corruption are rejected. A separate N=5,F_31,omega=4 case has c=-1 and confirms that the defining matrix is singular; it is rejected rather than inverted. A nonprimitive root is rejected.

These are exact finite-field implementation controls. They do not replace the characteristic-zero proof or establish a finite-bit implementation at unbounded m. The bounded C++ harness supports only the tested sizes and 64-bit-safe products. The test oracle is itself built with Fourier transforms and is never presented as a novel cheap B implementation.

The exact author candidate archive audited is Q11_Two_Call_Fourier_Recovery_CANDIDATE_2026-10-12.zip, SHA-256 0ec068ae864f44c2db226ecb82e0b3e1228e4924b1c24e6e6c7f674b85c20f9d. All 14 candidate manifest payloads were byte-verified. Its final report and both fresh checker sources were read; the reviewer ran only its own newly authored checkers. The candidate report agrees with the accepted bounded scope above.

## 7. Scope and remaining work

The two-call recovery and complete exact-field overhead are a bounded refinement of the already accepted three-call feedback reduction. Prior-result attribution and all source-model restrictions remain essential. No new historical claim or broader Q11 closure follows. The useful conclusion is diagnostic: a genuinely faster full arbitrary-input exact B evaluator with cheap uniform preparation would transfer to F on this same family, while the current shared evaluator remains classical O(N log N).

Derivative note: integration instructions are restated as mathematical scope. All proof, prior three-call attribution, exact schedules, costs, source limits and independent evidence are preserved. Original report SHA-256: `ac4a8e47a6041dee4b06ee0b4b16c7fd7a6eaef96e0b1d7a39094c5609fbb86c`.
