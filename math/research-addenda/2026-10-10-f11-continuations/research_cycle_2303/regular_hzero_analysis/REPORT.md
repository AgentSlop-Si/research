# Bounded H=0 continuation of the accepted fixed-F11 circuit

## Result and boundary

**Author-checked candidate; independent review pending.** On the surviving regular chart `H=0, d*M!=0`, the accepted rational reconstruction of `b=x11` can be replaced by a degree-two polynomial in `e=x83`, with unit denominator. The same exact calculation proves that three original guards, `x83`, `D25`, and `g98`, are automatically nonzero on this chart.

A bounded attempt with the next small original residual, E41, produces a 33-term exact necessary polynomial `P(e,c,q)` with degrees `(2,3,2)`. It does not produce a safe linear reconstruction of `c` or `q`, and no further input elimination is claimed. No feasibility obstruction or feasible point is established.

All 50 original residuals, all 19 original guards, the chart predicates, and accepted extra guards are retained. The input coordinates remain `(c,q,e)=(x34,x41,x83)`. Redundancy is proved without deleting guards. No optional-zero exclusion is added.

This is a continuation within the already accepted fixed-F11 theory, not a new fusion. It makes no unrestricted Fourier-factorization, output-only invariant, general FFT, novelty, dimension, or unrestricted-parameter claim.

## Accepted trust boundary and sources

The original atlas is `research_cycle_2014/fused_chart_atlas/CERTIFICATE.json`, SHA-256 `3fd7382a6207024853f7cf466b05a1f7aba9d9ef7e1b737353711a0394d49024`.

Its independent acceptance is `research_cycle_2016/three_input_atlas_review/RECEIPT.json`. The accepted later exceptional-chart exclusions are recorded in `research_review_dispatch_2056/ACCEPTED_F11_CONTINUATIONS.json`. This packet changes neither those conclusions nor the H!=0 chart. It uses the accepted identities and nonvanishing facts exactly within their recorded boundary.

`SOURCE_PINS.json` freezes 28 source-file hashes. The fresh build reads all referenced original polynomial data and validates the content-addressed hashes for 80 polynomials, including all residuals, guards, and inherited definitions needed by this chart. Historical author and review programs are not imported or executed. Their accepted theorems remain the trust boundary.

Work is over `K=Q[zeta]/Phi11(zeta)` and every field extension of K. No specialization of an algebraic root of H to K itself is assumed. No finite-field test, approximate root, numerical residual, or resultant is used as infeasibility evidence.

## 1. Unit-denominator reconstruction on H=0

The atlas uses

    b = -C0(e)/C1(e),
    H(e) = 0,

with `C1!=0` already certified. The new exact univariate Euclidean calculation supplies polynomials `I(e), J(e), B(e), T(e)` satisfying

    I*C1 + J*H = 1,
    C1*B + C0 = H*T,
    deg B = 2.

The coefficients are stored in `CERTIFICATE.json` under `C1_inverse`, `C1_inverse_H_multiplier`, `new_b_polynomial`, and `b_relation_quotient`.

Consequently, on every algebraic root of H, `B=-C0/C1`. Replacing the ordered b-definition by `b=B(e)/1` leaves its value unchanged. Every subsequent coordinate therefore reconstructs identically. Conversely, `H=0` and the polynomial b-definition imply the original b-definition. The projection/reconstruction maps, their domains, and all retained predicates are unchanged.

Only this definition is replaced in `preserved_chart`. It is not an unrestricted two-input parametrization: e remains an input subject to H=0 and the remaining residuals.

## 2. Three guards forced by H alone after reconstruction

After `x22=1` and `x49=zeta-c`, the original `g98` is a polynomial solely in b. Substitute `b=B(e)` to obtain `G98(e)`. The packet gives three exact identities

    S_e(e)*e + T_e(e)*H(e) = 1,
    S_D(e)*D25(e) + T_D(e)*H(e) = 1,
    S_G(e)*G98(e) + T_G(e)*H(e) = 1.

Their complete coefficient vectors appear in `guard_Bezout`. On H=0 the guard factors have polynomial inverses, so each is nonzero over every field extension. The original D25 and g98 references are checked against their exact source polynomials; no replacement of their meaning is made.

The original x83, D25, and g98 guards remain in the chart. These proofs justify future coefficient-ring simplification without assuming away guard-zero cases.

## 3. The bounded next-residual attempt

Use the accepted notation `A35=F_A`, `B35=F_B`, `a=Q_a`, `t=Q_t`, and `C=Q_C`. Define

    d = Nd/Dd,
    y = x92 + x0*d,
    Yn = -(q*b*t*Nd + C*Dd),
    Yd = q*a*Dd.

The accepted x92 formula gives `y=Yn/Yd`. The accepted regular x0 formula and E35 identities give

    r=x88 = -B35/A35.

For clarity, this does not introduce a new assumption. Since

    J35 = A35*N88 + B35*K0,
    x0 = -J35/(B35*q*M*d),
    D88 = q*M*x0*d + K0,

one has `B35*D88=-A35*N88`, hence `N88/D88=-B35/A35` on the retained guards.

The fresh build checks the exact original N25 polynomial identity

    N25 = alpha(e) + beta(e)*r*(1-y).

Thus the reconstructed x25 is

    x25 = N25n/N25d,
    N25n = alpha*A35*Yd - beta*B35*(Yd-Yn),
    N25d = A35*Yd*D25.

Let `N39,D39` be the unchanged inherited x39 definition. Substituting `x25=N25n/N25d`, `x39=N39/D39`, `x22=1`, and `x49=zeta-c` into the 22-term original E41 and clearing exactly the first powers of N25d and D39 gives the polynomial `E41_clear`. The build then verifies the exact factor identity

    E41_clear = (q^2*b*D25*a*D39)*E(b,c,q,e).

The cancelled factors are all nonzero on the original chart; the full ledger is below. The resulting E has 105 terms and degrees `(b,c,q,e)=(4,3,2,3)`.

Finally define the polynomial, without rational evaluation,

    S(c,q,e) = C1(e)^4 * E(-C0(e)/C1(e), c, q, e).

The displayed expression means termwise denominator clearing. Fresh exact division in e supplies an explicit polynomial Q and a remainder P such that

    S = H*Q + P,
    deg_e P = 2, deg_c P = 3, deg_q P = 2.

P has 33 terms. `E41_H_reduction` stores the complete Q and P vectors with variable order `(e,c,q)`. Every accepted point in this chart must satisfy P=0. In fact, on the original guarded H=0 chart, these identities also make P=0 equivalent to E41=0; the original E41 is retained regardless.

No coefficient of q or c is inverted. In particular, the leading q coefficient may vanish at some input values; that case is retained. A general multivariate factorization probe was stopped without a result and contributes no evidence. The completed, bounded result is this explicit residual polynomial and the guard/reconstruction certificate, not a claim to eliminate q or c.

## Division and saturation ledger

| Divisor or cancellation | Exact justification |
|---|---|
| C1 | Existing atlas Bezout certificate; freshly regenerated inverse identity |
| New b-definition denominator | Unit 1 |
| q | Original x41 guard |
| b | Accepted global b!=0, retained as an additional chart guard |
| e and D25 | Original guards; also proved automatic on H=0 here |
| Dd | Accepted identity `Dd=zeta^4*b*q*e*D25` |
| a | Accepted global a!=0, retained as an additional chart guard |
| A35 and B35 | Accepted global nonvanishing, both retained |
| D39 | Exact inherited x39 denominator after the unchanged initial bindings; the accepted circuit requires it nonzero before evaluation |
| M and d in regular x0 reconstruction | Explicit regular-chart predicates, unchanged |
| All other inherited denominators | Unchanged accepted circuit definitions and original guard logic |

The E41 numerator calculation is conducted in this already guarded localization. It neither discards a denominator-zero branch that belongs to the chart nor asserts a conclusion about the unsaturated affine numerator system. There is no division by c, x0, x49, a q-leading coefficient, or another optional-zero coordinate. All originally allowed optional-zero cases remain subject to the same original predicates.

## Reproduction and status

From the workspace root:

    python research_cycle_2303/regular_hzero_analysis/build_certificate.py

The fresh author code uses exact SymPy polynomial arithmetic over the rational cyclotomic field. Its computations are deterministic. The source pins, complete coefficient identities, guarded chart, and bounded negative controls are included. Source-content hashing, exact coefficient arithmetic, original N25 rebinding, original D25/N39/D39 rebinding, exact factor division, Euclidean identities, and retained predicate equality are checked by the build.

The certificate is an author-checked candidate until an independent checker validates it. No full feasibility conclusion follows. The H!=0 regular chart remains untouched, and the remaining H=0 residual system remains open.
