# F020: exact obstructions to a positive-metric solution of the complex kernel

19 October 2026 UTC. Canonical owner F020; F023 remains its alias. Fresh, source-bound mechanism probe. No external write, prior-program execution, new root-order census, or closure claim.

## Result and precise terminal boundary

The requested nonisotropy lemma remains open. No characteristic-zero counterexample was found or is claimed. This packet instead gives an exact, unlimited-range failure of the proposed **hidden Hermitian/positive-metric mechanism for the actual family**, rather than another generic warning about complex coefficients:

1. For every odd order d and every 3 <= b < d, the actual b-by-b Jacobi matrix cannot be made normal by any diagonal similarity. Allowing arbitrary diagonal amplitude changes as well as phases does not help.
2. At b=4 and every primitive odd order d>=5, no nonconstant affine transformation of the actual Jacobi matrix is similar to a Hermitian matrix, even by an arbitrary, nondiagonal similarity. Equivalently, no positive-definite Hermitian metric can make any rotated/rescaled J_4 self-adjoint. This obstruction holds at every primitive embedding, including every admissible odd prime power.
3. The full d-by-d matrix does have simple real Chebyshev spectrum and positive-definite self-adjointness metrics. But **none** of these metrics can be block diagonal across a residual cut 2 <= b < d. The exact compression formula retains a nonzero boundary coupling; simply restricting a full-order positive metric is invalid.

These are structural no-go results for a particular approach, not counterexamples to ordinary squarefreeness. Indeed, the b=4 calculation also makes its already-established simplicity transparent. The terminal failed premise is now explicit: the full-order real spectrum or a diagonal phase/amplitude normalization cannot supply a positive Hermitian norm for the residual bilinear Christoffel-Darboux kernel in the proposed way. A proof of that kernel's nonisotropy must use something beyond these premises.

## 1. Source-defined matrix and the actual missing assertion

The controlling report, Section 6, and its accepted independent review define

    P_0(X)=1, P_1(X)=X,
    P_(k+1)(X)=X P_k(X)-(1-q^k)P_(k-1)(X),
    w_k=product_(j=1)^k(1-q^j), w_0=1.

Here q is a primitive dth root of unity, d odd, and b<d. For 1<=k<d set

    u_k=1-q^k,  a_k=sqrt(u_k),

using the principal complex square root. Since Re(u_k)>0, no branch ambiguity or zero occurs. Let J_b be the symmetric tridiagonal matrix with zero diagonal and off-diagonal entries a_1,...,a_(b-1). Its characteristic polynomial is P_b.

At a root xi of P_b, use the eigenvector

    v_k=P_k(xi)/(a_1 ... a_k), 0<=k<b.

The empty product is 1. The three-term recurrence proves J_b v=xi v. Every eigenspace has dimension one: the first coordinate determines the rest, and a zero first coordinate forces the entire vector to vanish. Furthermore

    v^T v = sum_(k=0)^(b-1) P_k(xi)^2/w_k.

Thus the target is a bilinear, not Hermitian, nonisotropy assertion. The accepted diagonal CD identity shows that it is equivalent to P_b'(xi)!=0. In this irreducible tridiagonal setting, assuming an arbitrary similarity to a normal matrix would already assume diagonalizability and therefore simple spectrum; it would be circular unless independently constructed. Our first obstruction concerns only the much more explicit diagonal-similarity construction.

The accepted node theorem, exclusions of X=+/-2, monicity statements, failure t_3(4)=8>=phi(9), and the exact relation to ordinary H_b squarefreeness are not reproved or enlarged here.

## 2. Diagonal amplitude-and-phase normalization cannot make J_b normal

### General path lemma

Let T be an irreducible complex tridiagonal matrix with zero diagonal, superdiagonal s_k, and subdiagonal t_k. If T is normal, then all edge products s_k t_k lie on one common complex ray with strictly positive real multipliers.

Proof. The first diagonal entry of TT* = T*T gives |s_1|=|t_1|. Successive diagonal entries then give |s_k|=|t_k| for every k. The entries two places above the diagonal give

    s_k conjugate(t_(k+1)) = conjugate(t_k) s_(k+1).

Because the entries are nonzero,

    s_k/conjugate(t_k)=c

is independent of k, and |c|=1. Consequently s_k t_k=c |t_k|^2, proving the claim. Conversely, if all edge products have that form, a diagonal similarity makes the matrix a scalar multiple of a real symmetric path matrix. So this criterion is also sufficient.

Diagonal similarity preserves each edge product. In the actual J_b these products are u_k. Already the first two violate the criterion:

    u_2/u_1 = 1+q.

For any primitive odd order d>=3, q is nonreal, so 1+q is nonreal. Therefore for every 3<=b<d, **no diagonal similarity makes J_b normal**. This includes arbitrary nonzero complex diagonal entries, not merely unitary phase changes, and holds at every primitive embedding.

At the principal embedding one can also see the obstruction from

    u_k=2 sin(k pi/d) exp(i(k pi/d-pi/2)).

The sine amplitudes are positive, but successive edge products rotate by pi/d. Amplitude changes cannot change that invariant. This is an actual-family algebraic obstruction, not an inference from positivity or from a different recurrence.

## 3. A stronger obstruction: J_4 cannot be made Hermitian by any affine similarity

For b=4, direct use of the actual recurrence gives

    P_4(X)=X^4-A X^2+B,
    A=u_1+u_2+u_3=(1-q)(q^2+2q+3),
    B=u_1 u_3=(1-q)^2(q^2+q+1).

For |q|=1 with order d>=5, A and B are nonzero. The ratio invariant under rescaling X is

    R=B/A^2=(q^2+q+1)/(q^2+2q+3)^2.                 (1)

Write q=c+i s, c and s real, c^2+s^2=1, and a=1+2c. Since

    q^2+q+1=q a,
    q^2+2q+3=2q(a-i s),

we obtain

    R = a/[4q(a-i s)^2],
    Im R = -a s c(c+2)/[4(a^2+s^2)^2].              (2)

For a primitive root of odd order d>=5, none of a, s, or c vanishes: their vanishing would respectively force order 3, order 1 or 2, or order 4. Also c+2>0 and the denominator is positive. Hence Im R != 0 at every primitive embedding. At the principal embedding, c>0 and s>0, so Im R<0.

Now suppose tau J_4+sigma I, tau!=0, were similar to a Hermitian matrix. Its trace is 4 sigma, so sigma is real. It follows that tau J_4 has real spectrum. Because the original spectrum is invariant under lambda -> -lambda and B!=0, it would consist of two real nonzero opposite pairs after scaling. In particular the coefficient ratio

    (tau^4 B)/(tau^2 A)^2 = R

would be real, contradicting (2). Thus no such affine similarity exists.

Equivalently, there is no positive-definite Hermitian M for which a nonzero scalar multiple of J_4 is M-self-adjoint: M^(1/2) would turn such an operator into a Hermitian matrix. This refutes a hidden-Hermitian mechanism even when its positive metric is allowed to be completely nondiagonal.

This is not a squarefreeness counterexample. In fact B!=0 and R nonreal imply A^2-4B!=0. The two roots in Y=X^2 are distinct and nonzero, so P_4 has four distinct roots. That subfamily was already covered by prior accepted results; it is used here to separate failure of the proposed proof mechanism from failure of the target theorem.

## 4. Why the full Chebyshev spectrum does not descend to residual positive metrics

### Exact full-order symmetry and spectrum

At every primitive q of order d,

    u_(d-k)=conjugate(u_k),
    a_(d-k)=conjugate(a_k).

Therefore reversal R_d gives R_d J_d R_d=conjugate(J_d). Also all intermediate Gaussian coefficients at degree d vanish, so H_d(z;q)=1+z^d. The recurrence transformation then gives

    P_d(X)=2 T_d(X/2).

Its eigenvalues 2 cos((2r-1)pi/(2d)), 1<=r<=d, are real and distinct. Thus J_d has positive-definite Hermitian self-adjointness metrics. For example, if J_d=V Lambda V^(-1) with Lambda real diagonal, then

    W=(V^(-1))* V^(-1)>0,   W J_d=J_d* W.

Existence at the full order is therefore true, not the failed premise.

### Residual reflection has a nonzero defect

For a cut b<d the analogous edge formula is instead

    u_(b-k)=1-q^b+q^b conjugate(u_k).               (3)

The additive term 1-q^b is nonzero. It is an exact obstruction to simply reusing the full reversal-conjugation identity on J_b.

### No full positive metric decouples an admissible residual cut

At the principal embedding theta=2pi/d, for every 2<=b<d,

    Im tr(J_b^2)
      =-2 sum_(k=1)^(b-1) sin(k theta)
      =-2 sin((b-1)pi/d) sin(b pi/d)/sin(pi/d)
      <0.                                           (4)

The finite sine sum follows by summing a geometric series. In particular J_b cannot have wholly real spectrum and cannot be self-adjoint for any positive-definite Hermitian metric. The same nonvanishing holds at every primitive embedding theta=2pi a/d: neither numerator sine vanishes because a is coprime to d and 1<=b-1<b<d. The sign need not be preserved at another embedding, and is not needed.

If a positive metric W for J_d were block diagonal across the split b | d-b, its upper-left block M>0 would satisfy M J_b=J_b* M. That would make J_b similar to a Hermitian matrix and contradict (4). Hence **every** full-order positive metric has nonzero cross-block coupling at every residual cut 2<=b<d.

More precisely, write

    J_d = [ J_b  C ; C^T  D ],
    W   = [ M    N ; N*   L ],

where C=a_b e_b e_1^T. The upper-left block of WJ_d=J_d*W is

    M J_b-J_b* M = conjugate(C) N* - N C^T.         (5)

The principal block M remains positive, but the right-hand side cannot simply be discarded. At a residual eigenvector v with eigenvalue xi, (5) gives

    (xi-conjugate(xi)) v* M v
       =v* [conjugate(C)N* - N C^T] v.

This is a boundary-coupling identity, not a representation of v^T v as a positive norm. Restricting the full-order metric therefore does not establish the required bilinear nonisotropy. The stronger Section 3 result also excludes repairing this approach at b=4 by an arbitrary affine rotation and a different positive metric.

## 5. Certified scope, controls, and remaining work

The new lemmas are proved algebraically for unlimited ranges. The fresh checker has 19 exact symbolic transcription assertions: the actual P_4 recurrence and matrix characteristic polynomial, the invariant and imaginary-part computation, generic normality equations, the reversal defect, and compression bookkeeping. They are not finite-order evidence for an unlimited squarefreeness claim. The initial check had a SymPy symbol-identity mismatch between the characteristic-polynomial generator and an assumption-bearing X; explicitly substituting the returned generator fixed it without changing any mathematics. The failed and passing run logs are retained.

Two exploratory inline probes preceded the final mechanism: numerical spectra at four previously covered pairs, and characteristic-two discriminant factorization in small degrees. Neither is used as a proof or a new certification; their purposes and limits are recorded in RUN_LOG.md. No prior research script was imported or executed.

The exact report and accepted-review copies read for this task are retained and SHA-256-bound in SOURCE_BINDINGS.json. The controlling report's previously pinned source metadata is preserved as provenance, not represented as a new remote fetch. A brief web search of primary-literature leads did not supply a missing lower-degree simplicity theorem; no result in this packet relies on that search or asserts historical originality.

The proper terminal status is **mechanism ruled out, ordinary guard still open**. This does not settle lemma (L), supply a characteristic-zero collision, extend the all-A theorem, alter F020/F023 status or priority, close another gate, change historical attribution, or update an external record. The remaining useful direction must independently control complex bilinear eigenvector norms or provide another actual-family nonvanishing mechanism; it cannot assume the residual matrices inherit a positive real spectral problem from J_d.
