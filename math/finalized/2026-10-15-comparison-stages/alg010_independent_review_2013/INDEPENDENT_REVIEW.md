# ALG-010 cyclic-hypergeometric comparison: independent scoped acceptance

Date: 2026-10-14 UTC.

## Verdict and exact source binding

ACCEPT the selected primary-source comparison in
`alg010_cyclic_comparison_2010/COMPARISON.md`, SHA-256
c3d56d36ea643d193f5c533ca52e371056ee86e61a8feeb3355fc06c6b39a231.
No mathematical repair is required. It establishes an exact classical match
on the declared regular periodic subfamily and a qualified nonmatch between
the compared formulas and the complete raw-input/finite-boundary interface.
It does not prove worldwide novelty of that interface or change ALG-010's
accepted correctness, broad open status, or priority42.

REJECT any inference that the periodic first-order Fourier product, its
generic one-dimensional singular scale recovery, or O(N) full-output field
evaluation on that matched family is a new asymptotic advantage over this
antecedent. Conversely, this comparison does not invalidate the broader
accepted finite-boundary algorithm or replace it by a homogeneous periodic
formula outside the latter's hypotheses.

## Primary-source access

I independently opened the primary PDFs through public-web text extraction:

- Au-Yang and Perk, [The Many Faces of the Chiral Potts Model](https://arxiv.org/pdf/q-alg/9609003v1),
  Section9.1, page11, equations26-29: the periodic product, positive-sign
  Fourier transform, source recurrence, and transformed normalized product.
- Perk and Au-Yang, [Recent Developments on Ising and Chiral Potts Model](https://arxiv.org/pdf/math-ph/0606027v1),
  Section2.2, page4, equations12-14: the same family and explicit dual
  parameters. The finite cyclic-sum convention is on page3.

These passages support the exact antecedent, and themselves refer to earlier
work. I make no earliest-priority claim. No local primary PDF bytes or PDF
SHA-256 are available; neither this review nor the candidate claims a
downloaded-facsimile audit. A screenshot request did not supply an inspectable
image payload, so the primary inspection is explicitly text-based. The
optional 2002 and2016 sources are unnecessary to this acceptance.

## 1. Independent parameter and domain check

Let q have exact order N in a field and use y_k=sum_n q^(kn)x_n. The direct
literature comparison is over C. The field-general version below is an
algebraic deduction, not an attributed software theorem of the papers.
Exact order ensures q is nonzero and N is invertible in the field.

For the declared safe chart, x_0,alpha,beta,gamma are nonzero,
alpha^N and beta^N differ from1 and from each other, and
gamma^N(1-alpha^N)=1-beta^N. Define

  x_n=x_0 gamma^n product_(i=0..n-1)(1-alpha q^i)/(1-beta q^i).

All ratios are defined. The source relation is exactly

  (-gamma+gamma alpha q^i)x_i+(1-beta q^i)x_(i+1)=0.

Thus the parameter map (-gamma,gamma alpha,1,-beta) is correct. Its inverse
on p_0 r_0!=0 is gamma=-p_0/r_0, alpha=-p_1/p_0, beta=-r_1/r_0.
The candidate does not silently apply this chart at zero chart coordinates.
The identity product_i(1-aq^i)=1-a^N and the stated parameter constraint
give x_N=x_0. No endpoint term remains in this periodic case.

For the Fourier identity, let D=diag(q^i) and Sx have coordinate x_(i+1)
cyclically. Direct finite summation gives F D=E F and
F S=diag(q^(-k))F, where E shifts Fourier coordinates forward.
Hence F D S has coefficient q^(-k-1) on that forward shift. Substituting
the source parameters and multiplying row k by q^(k+1) yields

  (beta-alpha gamma q^(k+1))y_(k+1)=q(1-gamma q^k)y_k.

This independently checks the sign and extra factor q. Dividing by beta
gives the stated dual parameters gamma, q alpha gamma/beta, q/beta.
The comparison with the cited product formula is exact.

## 2. Dual regularity and the singular scalar

Periodicity gives gamma^N=(1-beta^N)/(1-alpha^N). Therefore gamma^N=1
exactly when alpha^N=beta^N. Likewise

  (q alpha gamma/beta)^N
    =alpha^N(1-beta^N)/(beta^N(1-alpha^N))

equals1 exactly on that same locus, using beta!=0 and alpha^N!=1.
The candidate's extra inequality removes all zero dual numerator/denominator
factors. Since F is invertible and x is nonzero, at least one Fourier
coordinate is nonzero; propagation through the nonzero cyclic ratio makes
all of them nonzero. Thus y_0 normalization is valid on the chosen chart.
Input regularity alone would not suffice.

The homogeneous target operator is singular even on this regular chart:
the actual nonzero Fourier vector lies in its kernel. Forward propagation
through nonzero edges leaves precisely one scalar, and the paid sum
y_0=sum_n x_n fixes it. The candidate correctly credits this regular
singular-scale recovery to the classical formula instead of labeling all
singular handling an unmatched contribution.

The accepted ALG-010 alternate anchor uses source and target kernel vectors
and the inverse-Fourier functional sum_k q^(-kj)y_k=N x_j. Its nonzero
denominator follows from similarity and a source kernel coordinate v_j!=0.
This is beyond direct use of a normalized formula at y_0=0, but the comparison
does not prove that no earlier limiting identity or alternate anchor exists.

## 3. Endpoint and degenerate boundaries

For a source relation imposed only at indices0 through N-2, extend its regular
ratio once and set delta=x_N-x_0. Replacing x_N by x_0 in the final cyclic
row gives residual u_(N-1)=-(1-beta/q)delta. Its Fourier transform has
coordinate u_(N-1)q^(-k). The same finite calculation therefore gives

  (beta-alpha gamma q^(k+1))y_(k+1)
    =q(1-gamma q^k)y_k+delta(q-beta).

The forcing sign and multiplier are correct. In Q(i), q=i, the vector
(1,2,4,8) has delta15 and cyclic residual-15. Direct four-term summation
gives (15,-3-6i,-5,-3+6i), also15/(2q^k-1). Setting the forcing to zero
would instead force the zero solution of its nonsingular diagonal target
system. This distinguishes the finite-boundary problem; it is not a
counterexample to the classical periodic theorem.

For the periodic mode (1,i,-1,-i), the transform is (0,0,0,4). The choice
alpha=beta=2,gamma=i gives regular nonzero source ratios but y_0=0. This
validates the explicit dual-regularity warning and shows why the displayed
normalization alone is insufficient. It does not exclude a meromorphic
limiting formula or another normalization. Zero input and zero coefficient
bands similarly require explicit interface cases, not silent division.

## 4. Discovery and paid full-output scope

An unknown projective quadruple is selected from an (N-1) by4 homogeneous
system. Streaming fixed-width elimination is O(N) field work, and a complete
residual recheck verifies the accepted recurrence and its endpoint. The
compared displayed formulas receive their parameters; they are not themselves
a raw-array recognition/rejection contract. This is a specific interface
nonmatch, not novelty evidence for elementary linear algebra.

On the matched regular periodic family, supplied parameters, paid root powers
and validation, a complete input/recurrence check, the single sum for y_0,
and N-1 ratio steps genuinely yield all N outputs in O(N) field operations
and O(N) field-element storage. There is no hidden full transform or repeated
N-term sum per frequency. This is a transparent algorithmic consequence of
the identity, not a runtime statement quoted from a physics paper. It leaves
root acquisition, bit sizes, conditioning and finite precision unproved.

The candidate retains the inherited ALG-010 loop counts as prior accepted
claims rather than reporting new machine measurements. The new finite-field
and Gaussian-rational control source was read as source only; its saved
120-case/2,976-coordinate result was not replayed by this reviewer. Universal
acceptance rests on the finite-sum algebra and domain arguments above.

## Final scope

The selected comparison's exact-match/qualified-nonmatch stopping condition
is satisfied. The complete-interface priority question, numerical stability,
bit complexity, and arbitrary-input FFT acceleration remain unresolved.
No supplied historical code ran and no external state changed during this
review. Table mutation, publication execution, and final readback are not
covered by this scientific acceptance.
