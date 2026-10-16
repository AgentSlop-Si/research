# Q29: source-bound correction of the uniform transfer gate

16 October 2026 UTC. Read-only mathematical/source audit; local deliverable only.

## Result and boundary

The all-layer shared endpoint is already settled by the independently accepted
F021 resonance theorem. For every e in the Q29 tower,

    U_e(-1) != 0.

This is an inherited theorem, not a new Q29 discovery or a newly completed
mathematical gate. The new contribution of this report is the exact cross-record
map and correction of the remaining obligation. The latest Q29 transfer audit
correctly displays the endpoint factor in its discriminant identity, but its
description of that endpoint as requiring a new uniform proof is redundant.

Together with the already accepted Q29 residual/Hensel facts, the unresolved
successive-layer question is precisely ordinary discriminant nonvanishing.
In particular, putting D_e = Disc(R_e),

    B_e != 0 iff D_e != 0,

so the proposed bridge is equivalent to

    D_e != 0 implies D_(e+1) != 0, for every e >= 3.

No proof or counterexample to this implication was obtained. No actual
higher-layer multiple root was found. The fixed e=3 theorem remains complete.
Q29 and its broader parents remain open, with no status/count/priority or
novelty promotion.

## 1. Sources and live target

Repository snapshot: AgentSlop-Si/research at commit
4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a.

The following source was fetched from that exact commit:

https://github.com/AgentSlop-Si/research/blob/4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a/math/finalized/2026-10-15-frontier-boundaries/README.md

Its manifest pins the two current Q29 transfer documents and the completed
fixed-instance aggregate/scope reviews. The corresponding local source bytes
match those manifest SHA-256 values; SOURCE_BINDINGS.json records the bindings.
The README and manifest connector payloads are saved in this directory.

The live workbook was read through native Sheets metadata and bounded values:

https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit

- Research overview, row 15, A:Q, tab ID 1731260011
- Research queue, row 32, A:Z, tab ID 1877766156

The complete read payloads are saved locally. They retain the complete fixed
e=3 acceptance, the open all-e bridge, priority 54, and the instruction not to
repeat fixed-instance censuses. Their older history already says the root -1
stays simple and resonant; that statement is reconciled here with its actual
accepted source rather than treated as a new claim.

The extra controlling sources are the F021 primary classification and its
independent audit, both fetched from the same exact repository commit:

https://github.com/AgentSlop-Si/research/blob/4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md

https://github.com/AgentSlop-Si/research/blob/4477338817cf2bd54a32f6bcc7c0d8ab0466ac4a/math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md

Their retrieved bodies are byte-identical to the previously recovered local
sources. These are primary mathematical text and its accepted review, not
unverified recollections or a table-level inference.

## 2. Exact F021-to-Q29 map

Use the unchanged Q29 definitions

    N_e = 27*5^e,
    n_e = (N_e-1)/2,
    m_e = (N_e-3)/4 = (n_e-1)/2,
    q_e = alpha*zeta_(5^e),
    U_e(z) = H_(n_e)(z;q_e)/(z+1),
    U_e(z) = z^m_e R_e(z+2+z^-1).

Here alpha has order 27 and the two factors defining q_e have coprime orders.
Thus q_e is a primitive N_e-th root. N_e is 3 modulo 4, so n_e is odd.

F021 uses its degree index m=(N-1)/2. Under the present substitution that
index is n_e, NOT Q29's reciprocal-quotient degree m_e. Its polynomial is

    T_(n_e)(x;q_e) = (-1)^n_e H_(n_e)(-x;q_e).

F021 primary §2, especially its odd-index kernel argument, proves x=1 is an
algebraically simple root of T_(n_e) for every odd N_e congruent to 3 modulo 4.
The independent audit's “Uniform resonance theorem” explicitly verifies
algebraic simplicity, rather than merely a one-dimensional eigenspace.

Since n_e is odd,

    T_(n_e)'(1;q_e) = H_(n_e)'(-1;q_e) = U_e(-1).

Consequently U_e(-1) is nonzero at every layer. The proof is not conditional
on a lower-layer discriminant, any finite local jet, or any conjectural
higher-layer squarefreeness.

The underlying accepted argument first works at the principal complex root.
It factors the relevant complex Jacobi matrix as J=D R D, with R real
symmetric and B=D^(-2) having positive real and imaginary diagonal parts.
At the zero eigenvalue the real kernel is one dimensional; its first
determinant coefficient is a nonzero real factor times v_0^T B v_0, which is
nonzero. A nonzero derivative is an algebraic statement in Q(q), so it passes
to every primitive root by cyclotomic field automorphisms.

Finally Q(q_e) embeds into the actual characteristic-zero local coefficient
field K_e. An injective field embedding preserves a nonzero algebraic element.
No assertion about preserving arbitrary complex absolute values or changing
the selected 5-adic component is used. No uniform 5-adic valuation is inferred.

## 3. What the complete uniform gate now is

The already accepted residual statement is

    U_e mod pi_e = (1+z^27)^a_e Ebar(z),
    a_e = (5^e-1)/2.

Here Ebar is the accepted degree-12 squarefree factor, nonzero at every primary
center and at 1. Thus the accepted Hensel decomposition is

    U_e = E_e * product_(j=0)^26 P_(e,j),

where E_e has degree 12 and each P_(e,j) has degree a_e. The discriminant of
E_e and all cross-factor resultants are units. Also

    U_e(1) is a unit.

These are inherited uniform facts. This report performs no new center census.

Together with §2, both reciprocal branch values are nonzero:

    R_e(0) = (-1)^m_e U_e(-1) != 0,
    R_e(4) = U_e(1) != 0.

The exact ordinary discriminant identities therefore give

    Disc(U_e) = Disc(R_e)^2 R_e(0) R_e(4),
    Disc(H_(n_e)) = Disc(U_e) U_e(-1)^2,
    B_e = (-1)^m_e [Disc(R_e) R_e(0) R_e(4)]^2.

Over the characteristic-zero field these yield the equivalent conditions

1. B_e is nonzero.
2. Disc(U_e) is nonzero.
3. Disc(R_e) is nonzero.
4. Disc(H_(n_e)) is nonzero.
5. Disc(P_(e,j)) is nonzero for every j=0,...,26.

Condition 5 uses the exact product-discriminant formula and the known unit
cross-resultants. This is an equivalence of nonvanishing, not equality of
valuations or an assertion that an endpoint is a unit.

The existing same-q reciprocity could pair the primary factors, but no new
reciprocity calculation is needed here and it gives no cross-layer transfer.
The genuine unresolved family consists of the within-primary ordinary
discriminants as the degree grows from a_e to 5a_e+2.

For additional geometric context, F021 already implies that in the principal
complex embedding U_e has no root on the unit circle: the only unit-circle
root of H_(n_e) is the removed simple root -1. Hence R_e has no root in [0,4]
in that embedding. This does not prevent multiple roots away from that set.
Arbitrary field automorphisms need not preserve absolute values.

## 4. The endpoint must remain in valuation formulas

The correction does NOT change the accepted exact factorization

    B_e = epsilon_e P_(e,0)(-1) * product_j Disc(P_(e,j)),

where epsilon_e is a local unit. The factor P_(e,0)(-1) is known nonzero by
§2 and the unit evaluations of the other factors, but it need not be a unit.

At the completed e=3 instance,

    v_pi U_3(-1) = 75,
    v_pi Disc(U_3) = 127737,
    v_pi Disc(R_3) = 63831,
    v_pi B_3 = 127812.

Thus absorbing the endpoint into epsilon_e would already be false at e=3.
The exact identity

    v_pi(B_e) = 2 v_pi(Disc(R_e)) + 2 v_pi(R_e(0))

holds whenever the discriminant is nonzero, since R_e(4) is a unit. No
uniform formula for either valuation on the right has been proved here.

In particular, the inherited endpoint does not repair the q-Lucas reference:
that reference still contains the repeated factor (1+z^N_e)^2. Its ordinary
discriminant vanishes, so it cannot be the nonsingular reference required by
the accepted valuation-stability transfer lemma.

## 5. Actual-family endpoint cross-check beyond the Q29 specialization

The following direct proof is valid for any odd degree n=2m+1 and primitive
root q of order N>n. It is included as an independently derived broader
endpoint identity, not as a new Q29 theorem, a literature-priority claim, or
a solution to the discriminant problem.

Let

    d_m(Q) = H_(2m+1)'(-1;Q).

The exact Rogers–Szegő recurrence yields

    H_(2m)(-1;Q) = product_(j=1)^m (1-Q^(2j-1)),
    d_0(Q) = 1,
    d_m(Q) = product_(j=1)^m (1-Q^(2j-1))
             + (1-Q^(2m)) d_(m-1)(Q).

Unwinding this polynomial recurrence proves in Z[Q]

    d_m(Q) =
      sum_(r=0)^m
        [product_(j=1)^r (1-Q^(2j-1))]
        [product_(j=r+1)^m (1-Q^(2j))].                 (5.1)

Take q=exp(2*pi*i/N). Every factor used has exponent between 1 and 2m<N,
and

    1-q^j = 2 sin(pi*j/N) exp(i[-pi/2+pi*j/N]).

Each summand in (5.1) has exactly m factors. Its exponent-label sum is

    (1+3+...+(2r-1)) + ((2r+2)+...+2m)
      = m(m+1)-r.

Therefore the summands have positive moduli A_r and arguments

    -m*pi/2 + pi*(m(m+1)-r)/N.

All those arguments lie in an arc of width pi*m/N<pi/2. If phi is the
midpoint of that arc, then

    Re(exp(-i*phi) d_m(q))
      >= cos(pi*m/(2N)) * sum_r A_r > 0.

Thus d_m(q) is nonzero. The polynomial identity and cyclotomic Galois action
transfer this to every primitive q of order N. Since H_n=(z+1)V_n,

    V_n(-1;q) = H_n'(-1;q) = d_m(q) != 0.

The proof also works at N=n, but no use of that extension is needed for Q29.
It provides no 5-adic unit claim or ordinary discriminant bound.

Fresh bounded controls independently build Gaussian coefficients by q-Pascal
in Z[Q] and compare their ordinary derivative at -1 to (5.1) for the eleven
odd degrees 1,3,...,21. Every polynomial coefficient agrees. The phase-label
formula is checked exactly. These small controls support transcription only;
the uniform proof is the recurrence and half-plane argument above.

## 6. Recommended research wording and stopping boundary

Suggested correction to current Q29 explanatory text:

“The shared endpoint U_e(-1) is already nonzero at every layer by the accepted
F021 uniform resonance/simplicity theorem, with its degree index identified as
n_e. U_e(1), the degree-12 residual discriminant, and all cross-primary
resultants are already units. The remaining all-layer bridge is ordinary
primary-discriminant nonvanishing, equivalently Disc(R_e)!=0 implies
Disc(R_(e+1))!=0. Keep the nonunit shared endpoint in exact valuation
accounting. No fixed-instance census or unchanged raw-jet normalization proves
this bridge.”

This is a proposed source-bound correction; no Sheet or repository was edited.

A meaningful next mathematical result must control the actual higher-layer
ordinary discriminants, either by a genuine Rogers–Szegő correction theorem
with enough precision, or an independent all-layer argument. The fact that
endpoints are nonzero does not provide the missing primary coefficients.
Generic positive-pencil or synthetic-lift examples cannot resolve the actual
family. No automatic next fixed layer has been selected.

## 7. Verification and scope receipt

- Exact repository README, manifest, F021 primary, and F021 review fetched.
- Native workbook metadata and the two requested current rows read.
- Four local frontier text hashes checked against the repository manifest.
- Two F021 fetched bodies checked byte-for-byte against recovered originals.
- Eleven small independently authored polynomial controls passed.
- Supplied scientific programs executed: 0.
- Large solver jobs, installations, and network bypasses: 0.
- External writes: 0.
- Fixed e=3 census repeated: 0.
- New proof of uniform discriminant transfer: none.
- Q29 status/count/priority/novelty delta: none.

