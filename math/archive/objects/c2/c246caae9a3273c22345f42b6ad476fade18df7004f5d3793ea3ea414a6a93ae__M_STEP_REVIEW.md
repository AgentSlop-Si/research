# Independent review of the M-step application circuit

9 October 2026 UTC. This continuation is separate from the sealed first review. No uploaded source code was executed or imported.

## Verdict

The iterated identity, polynomial recurrence, explicit application schedules, exact Fourier-grid support count, and stated scope restrictions are correct. The literal product applies M full-array factors and costs Theta(MN). Its ordinary compiled two-dimensional convolution costs Theta(N log N) in the specified radix schedule. That count is an implementation ledger, not a lower bound for other circuits.

A useful improvement was found in review: all raw coefficients of both P_M and D_X can be prepared in O(N) using cyclic weighted-shift solves and one shared scalar inversion. RAW_KERNEL_PREPARATION.md supplies the proof and complete ledger. Kernel preparation therefore need not remain a Fourier-scale cost. Arbitrary-input application is still unresolved below the current Fourier-scale circuit.

## Identities and branches checked

The recurrence

    (1-X^s)p_s=(X^(s-1)-eta)p_(s-1)

and coefficient identity (1-eta^s)k_s=sum_(r=1)^s p_r eta^(s-r)k_(s-r) follow from the finite q-binomial product and M-step substitution. All denominators are nonzero at every q_h=omega eta^(-h). The full product includes its degree-M term. Compiled multiplication of two degree-r polynomials requires a lag convolution length at least 2r+1, rather than 2r; a power-of-two length 4r suffices. This changes no asymptotic count.

With T_r f(z)=f(X^r z), P_(2r)=P_r(X,z)P_r(X,X^r z) is exact. The conjugated second multiplication is T_r M_(P_r) T_r^(-1). It does not turn two applications into one. Similarly A=(I+Z)T gives A^M=M_(P_M)T_eta, so M_(P_M)=A^M T_eta^(-1) is M explicit sparse passes, not logarithmically many.

For arbitrary a(z), multiplying the kernel identity cannot replace D_X(eta z)a(z) with y(eta z). At M=4,p=17,eta=13 and a(z)=z, the proposed shortcut has z coefficients 1 and 13. Nonunit or zero input constant terms also prevent using an input-polynomial inverse as a uniform repair.

## Butterfly ledger

At dyadic M, embed an M-by-M raw input in an M-by-2M array. Zero padding means only M active length-M transforms are needed on the first coordinate. Then M length-2M lag transforms are required. One forward bank uses

    (N/2)log2 M + N log2(2M)

ordinary radix-two butterflies. Invert the lag dimension first and compute only the M requested first-coordinate transforms; the same count results. Total data-dependent butterflies are 3N log2 M+2N, before pointwise products, phases and charged kernel preparation. The balanced rectangle recurrence B(M)=4B(M/2)+Theta(M^2) is consistent. This count assumes those unpruned lag transforms; it is not a claimed minimum for every output-only or pruned transform.

## Exact zeros and invertibility distinction

At rho=omega^(M/2), the grid multiplier is

    product_(j=0)^(M-1)(1+q_h^j rho^ell).

A zero requires q_h^j in the subgroup of order 2M. Exactly j=0,M/2 qualify, since q_h has order M^2. The two zero lag indices are precisely

    ell=M,  and  ell=M-1+Mh mod 2M.

Thus each channel has exactly two zeros, and the complete grid has 2N-2M nonzero multipliers. Discarding the degree-M coefficient changes this polynomial and may destroy that exact count.

The full 2M-lag cyclic convolution has 2M zero eigenvalues. However, requested degree-<M truncated multiplication by P_M remains invertible, because its constant coefficient is 1 and its coefficient map is block lower triangular with identity diagonal. The grid zeros do not imply loss of information about the embedded input. They only allow O(M) pointwise products to be skipped in this particular transform schedule.

## Evidence

check_m_step_review.py independently uses direct raw twisted-ring products and direct two-dimensional transforms, rather than the constructor’s FFT code. It verifies:

- 1,426 exact coefficient identities and 258 doubling products
- 10 complete raw 2D convolution applications, with all 5,456 output coefficients checked
- Exact zero locations and counts for M=2,4,8,16,32
- Invertibility of the corresponding truncated products in all ten cases
- The displayed radix butterfly totals by an independent per-axis count

check_raw_preparation.py verifies the separate O(N) preparation improvement. Exact all-size proofs establish scope; finite controls, matrix support, and condition numbers are not promoted to unrestricted lower bounds or finite-precision algorithms.
