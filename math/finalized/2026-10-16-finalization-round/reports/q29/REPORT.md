# Q29 finalization: exact ordinary-discriminant gate and research value

16 October 2026 UTC. Read-only research pass; no external changes.

## Verdict

The uniform implication `Disc(R_e) != 0 => Disc(R_(e+1)) != 0` for
`N_e=27*5^e`, `e>=3`, remains unresolved. No actual-family counterexample was
found. The complete fixed `e=3` theorem remains complete and is not rerun.

This report gives an explicit denominator-free ordinary-derivative kernel
for the actual reciprocal family, an exact resultant identity, and its
uniform known ramification charge. These are classical recurrence and
Christoffel–Darboux reductions, with proofs below. They are not a new
noncancellation theorem or an inter-layer transfer. Their purpose is to pin
the precise missing lemma, rather than manufacture another solved subtask.

**Recommendation:** park automatic continuation of this selected tower unless
a proposed method can control the actual variable-layer kernel/correction.
Another fixed layer, endpoint census, or re-normalization of unchanged old jets
has low identified mathematical value. Preserve the broader owners as open.
Even a proof for this tower would not improve its motivating scalar-bank
minimum: every `27*5^e` is `3 mod 4`, and accepted F021 already establishes
the exact minimum `(N_e+1)/2` in its scalar common-cycle model, regardless of
squarefreeness. An all-layer arithmetic squarefreeness theorem would still be
a genuine result; its value would chiefly be a reusable method or an explicitly
independent arithmetic objective. It would not settle the canonical
`N=1 mod 4` composite classification.

No status, priority, canonical-claim count, novelty, or performance change is
proposed as a mathematical consequence of this report.

## 1. Current owners and accepted boundary

Fresh native reads of the workbook's `Research overview!A14:Q16` confirm:

- `ALG-OPEN-UNIFORM-SQUAREFREE`, row 14: TO RESEARCH, priority 54.
- `Q29`, row 15: TO RESEARCH, priority 54.
- `NEXT-RS-AUGMENTED`, row 16: TO RESEARCH, priority 54.

These are related work views, not three equivalent theorems or three new
results. Native owner snapshots are retained privately and excluded from this publication.
The controlling queue source is `Research queue`, row 32, stable ID Q29.

The live Q29 text already incorporates the accepted endpoint reconciliation:
`U_e(-1)!=0` at every layer by F021. Also `U_e(1)`, the degree-12 residual
discriminant, and all cross-primary resultants are units. The only unresolved
nonvanishing is within the actual higher-layer primary factors, equivalently
the ordinary discriminant of `R_e`. The nonzero shared endpoint must still be
retained in valuation accounting; at `e=3` its valuation is 75.

The inherited fixed theorem has `v_pi Disc(R_3)=63831`, and the corresponding
U and H squarefreeness statements. No numerical reconstruction is repeated.
The old transfer audit proves that the adjacent-layer q-Lucas reference has
a repeated factor and that replacing the lower polynomial's argument by the
actual lower root fails already at valuation 1. The unchanged e=3 raw
rectangles and content-60 normalized residues vanish at higher layers.
These are obstructions to those specific proof routes, not counterexamples
to actual higher-layer squarefreeness.

## 2. Actual-family contraction and a denominator-free kernel

Work first over `Z[q,w]`. Write `a_j=1-q^j` and define

    S_0(x)=1, S_1(x)=x,
    S_(r+1)(x)=x S_r(x)-a_r S_(r-1)(x).

The Rogers–Szegő recurrence gives the Laurent-polynomial identity

    H_n(z;q)=z^(n/2) S_n(z^(1/2)+z^(-1/2)).

For `n=2m+1`, parity gives `S_(2m+1)(x)=x C_m(x^2;q)`. Consequently

    H_(2m+1)(z;q)=(z+1) z^m C_m(z+2+z^-1;q).

This has no branch ambiguity: both sides are ordinary polynomials after the
displayed cancellation, and the identity follows from the recurrence.
Thus the actual Q29 reciprocal polynomial is exactly

    R_e(w)=C_(m_e)(w;q_e),  m_e=(27*5^e-3)/4.

Eliminating the even S terms gives

    C_0=1,
    C_1=w-2+q+q^2,
    C_(k+1)=(w-2+q^(2k+1)+q^(2k+2)) C_k-beta_k C_(k-1),
    beta_k=(1-q^(2k))(1-q^(2k+1)),  k>=1.

This recurrence is already present in the accepted Q29 reciprocal
implementation sources. It is not claimed as a new identity here.

Define the integral polynomial

    K_m(w;q)=sum_(k=0)^(m-1) C_k(w;q)^2
                         product_(j=k+1)^(m-1) beta_j(q).

Empty products are 1. In particular `K_1=1`. All derivatives below are
ordinary derivatives with respect to w, not Jackson or q-derivatives.

**Kernel identity, for every m>=1:**

    K_m=C'_m C_(m-1)-C_m C'_(m-1).                 (2.1)

Proof. Let the right side be W_m. Differentiating the three-term recurrence
and subtracting yields exactly

    W_m=C_(m-1)^2+beta_(m-1) W_(m-1),  W_1=1.

Iteration gives the stated finite sum. This proof is uniform in m and q.

**Resultant identity, in Z[q]:**

    Res_w(C_m,K_m)=Disc_w(C_m) product_(j=1)^(m-1) beta_j^j.   (2.2)

Proof. Equation (2.1), evaluated at the roots of the monic C_m and interpreted
as a resultant identity including multiplicities, gives

    Res(C_m,K_m)=Res(C_m,C'_m) Res(C_m,C_(m-1)).

The recurrence and monicity give, by induction,

    Res(C_m,C_(m-1))=(-1)^(m(m-1)/2) product_(j=1)^(m-1) beta_j^j.

The ordinary discriminant formula supplies the identical sign in
`Res(C_m,C'_m)`, so the signs cancel. No simple-root assumption was used.

When q has exact order N=4m+3, every exponent in these beta factors is
between 2 and `2m-1<N`. Thus no beta factor vanishes. The recurrence also
shows that C_m and C_(m-1) are coprime: a common zero propagates backwards
to C_0=1. We therefore have the exact equivalences

    Disc(C_m)!=0
      iff Res(C_m,K_m)!=0
      iff K_m(lambda;q)!=0 for every root lambda of C_m.

There are no divided differences or denominator guards hidden in K_m.
However, it is a bilinear sum of complex squares, not a positive sum of
absolute squares. The nonzero beta factors do not prevent cancellation.

## 3. Exact known ramification charge

Use the accepted Q29 component

    q_e=alpha*zeta_(5^e),  ord(alpha)=27,
    pi_e=zeta_(5^e)-1,  v_pi(pi_e)=1.

Put `P_e=product_(j=1)^(m_e-1) beta_j(q_e)^j`. This is nonzero.
For `1<=k<N_e`,

    v_pi(1-q_e^k)=0                         if 27 does not divide k,
    v_pi(1-q_e^k)=5^v_5(k)                  if 27 divides k.

Indeed the first case has nonzero tame residue. In the second case the tame
factor is 1 and the ordinary cyclotomic valuation of the remaining 5-power
root gives the result; its order is still greater than 1 in the stated range.

Since beta_j uses the two exponents `2j,2j+1`, this yields

    s_e := v_pi(P_e)
         =sum_(r=1)^((5^e-1)/2) floor(27r/2) 5^v_5(r)
         =[(216e+45)25^e-16e*5^e-45]/160.          (3.1)

Here the upper limit follows from
`floor((2m_e-1)/27)=(5^e-1)/2`.

For completeness, let `a_t=(5^t-1)/2`, which is even. Use

    5^v_5(r)=1+sum_(s=1)^v_5(r) 4*5^(s-1),
    sum_(u=1)^A floor(Bu/2)=A[B(A+1)-1]/4

when B is odd and A is even. Then the first sum in (3.1) is

    a_e[27(a_e+1)-1]/4
      +sum_(s=1)^(e-1) 5^(s-1) a_(e-s)[27*5^s(a_(e-s)+1)-1].

Summing the geometric series simplifies to the displayed closed expression.
This is a uniform arithmetic identity, not an observed valuation fit.

Equation (2.2) now gives the exact integral relation

    Res(C_(m_e),K_(m_e))=Disc(R_e) P_e.             (3.2)

If either side is nonzero, its valuation is therefore

    v_pi Res(C_(m_e),K_(m_e)) = v_pi Disc(R_e)+s_e.

If the discriminant is zero, the resultant is zero as well. A finite valuation
must not be assigned in that case. The prefactor's known positive valuation
does not make the remaining discriminant a unit or prove it nonzero.
This identity is an exact ordinary-discriminant normalization, but it does
not create a new independent invariant: dividing by P_e simply recovers D_e.

## 4. Exact unresolved lemma and a meaningful restart condition

The actual-family missing lemma can be stated without endpoints or local
center enumeration:

> For every integer e>=3, assume `Disc(C_(m_e)(.;q_e)) != 0`.
> Then for every lambda with `C_(m_(e+1))(lambda;q_(e+1))=0`,
> the explicit polynomial `K_(m_(e+1))(lambda;q_(e+1))` defined above is nonzero.

The compatible component is mandatory:

    q_e=alpha*(1+pi_(e+1))^5=alpha^-4 q_(e+1)^5.

By (2.2) this lemma is exactly the requested inter-layer ordinary-discriminant
implication. Proving unconditional upper-layer noncancellation would be a
stronger sufficient result. This report has proved neither version.

The principal-embedding exclusion of roots of R_e from [0,4], inherited from
F021, does not prove the kernel nonzero at nonreal roots. Likewise the
already-reviewed positive-complex-pencil shortcut fails for general pencils.
A q-discriminant calculation cannot be substituted for (2.2): Ismail–Witte's
explicit Rogers–Szegő formula is for the q-discriminant, as its equations
(5.16)–(5.17) explicitly state. Their introduction also distinguishes it from
the ordinary discriminant. [Primary paper](https://arxiv.org/html/math/0012259v2)

Restart the selected tower only for an actual, quantified mechanism such as:

1. a no-self-orthogonality/noncancellation theorem for this particular
   q-dependent kernel, with root and component guards proved; or
2. a nonsingular reference and a proved correction bound that is strictly
   strong enough to preserve its ordinary discriminant, uniformly in e.

A source-bound actual multiple root is also decisive. A new synthetic lift,
finite-m test, nonvanishing q-discriminant, or new fixed-layer coefficient
census does not meet this condition. The lower-layer nonvanishing assumption
alone supplies none of the upper-layer kernel values.

## 5. Mathematical-value recommendation

The problem is genuine, but the current selected route has weak direct payoff
for the original bank objective. F021's accepted primary theorem and review
prove for every odd `N=3 mod 4` that the resonant node persists and forces
the exact legal scalar-bank minimum `(N+1)/2` in the stated common-P scalar
model. Our tower stays in this class at every layer. Proving its squarefreeness
does not remove that node or reduce the minimum. This is a deduction from
the accepted theorem, not a new lower-bound discovery.

The broader canonical owner includes all composite `N=1 mod 4`, general
content support, and repeated-prime extensions. None is discharged by the
current tower reduction or by a hypothetical proof limited to this tower.
It would also be wrong to mark all three related owners solved merely
because this pass has a complete report.

Recommended disposition:

- Preserve all accepted fixed-case mathematics and the exact unresolved
  statement.
- Stop automatic finite-instance or endpoint redispatch in this selected
  tower; require a genuinely reusable mechanism before another active pass.
- Leave mathematical status OPEN for Q29 and the related broader owners.
  An administrative parking decision is separate from theorem completion.
- Do not count this classical kernel/valuation reduction as a novel theorem,
  canonical discovery, FFT improvement, or newly completed uniform stage.

An arithmetic-squarefreeness theorem could justify renewed attention if it
has an independently important application or a method that reaches beyond
this already-classified bank-parity class. No such downstream result is
established by the present sources or this pass.

## 6. Sources, verification, and limits

Repository reads were pinned to
`a74d66f28f70e721cd1adfad668146a0d53bb78c` in AgentSlop-Si/research.
The fetched frontier manifest matches six locally retained Q29 source files
byte-for-byte. The fetched F021 primary and audit match their archived SHA256
digests after preserving the exact final newline. `SOURCE_BINDINGS.json`
records all checks.

Controlling source links:

- [Current frontier packet](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/finalized/2026-10-15-frontier-boundaries/README.md)
- [Pinned frontier manifest](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/finalized/2026-10-15-frontier-boundaries/MANIFEST.json)
- [F021 primary classification, especially sections 1–2](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md)
- [F021 independent audit](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md)
- [Live workbook](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit)

Local original sources inspected include the transfer author/review,
aggregate accounting, scope audit, latest accepted endpoint reconciliation,
its independent review, and the reciprocal recurrence in
the previously reviewed sparse execution contract.

Five fresh symbolic transcription controls check the polynomial contraction
and kernel identity for m=1,...,5; three also check the resultant identity.
The valuation formula is checked against its elementary integer sum at six
small e values. These are transcription controls, not a root/layer census
and not evidence of uniform noncancellation. The proofs in sections 2–3,
not those checks, establish the displayed universal identities.

Supplied programs executed: zero. Historical large computations rerun: zero.
External writes: zero. Actual-family transfer proof: none. Actual-family
multiple-root counterexample: none. Worldwide-priority assessment: none.
