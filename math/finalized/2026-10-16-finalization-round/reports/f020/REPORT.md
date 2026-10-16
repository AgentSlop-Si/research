# F020 mathematical finalization: exact open proof boundary

16 October 2026. Read-only review and locally saved report. No supplied research program was run; no Sheet or repository record was changed.

## Disposition

**Retain F020 as OPEN / TO RESEARCH, priority 58, with a precise mathematical blocker.** Its separate general endpoint gate remains 53. The reviewed all-order local formulas, fixed-base results, reciprocal descent, complementary endpoint certificate and three off-line endpoint-order lines remain accepted at their existing scopes. This review proves neither the all-family unit ideal nor an actual-family counterexample.

There is a meaningful distinction between two possible archival decisions:

- Archive completed finite-base calculations and the specifically refuted shortcut routes from active work. Do not launch another growing fixed-b/m census automatically.
- Do **not** relabel the actual-family uniform support question as solved, refuted or merely classical. The sources establish neither a uniform certificate nor a disqualifying mathematical-value assessment of that question. A continued proof attempt must use a genuinely new property of the actual Rogers–Szegő coefficients.

This is a finalization of the current proof boundary, not a new theorem acceptance or a request to reopen completed stages. The exact remaining assertion is specified below; no missing historical source is used as evidence of closure.

## 1. Current owners, read live and checked by stable ID

Spreadsheet: [Research cycle](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit).

The following cells were read directly on 16 October 2026. Earlier text retained inside the same cells is historical, not a newly selected task.

| Owner | Stable-ID cell | Current status / score | Current gate | Pass / stop | Evidence |
|---|---|---|---|---|---|
| Research overview, gid 1731260011 | B9 = F020 | E9 = TO RESEARCH; L9 = 58 | C9, P9 | Q9 | J9 |
| Catalogue, gid 214001001 | A4 = F020 | AA4 = 58; AC4 current scoped proof | AE4 | AF4 | AC4 and N4 |
| novelity breakthough, gid 214001003 | C7 = F020; R7 = F020 | U7 = 58; W7 current scoped proof | O7, Y7 | N7, Z7 | Q7 |
| Theorem register, gid 404576783 | A22 = F020 | C22 = full gate OPEN58 / endpoint OPEN53 | G22 | G22 | J22 |

The relevant current Catalogue columns are AA:AF. Its older V4 text is not the current successor instruction. The current owners agree on the full four-channel obligation, the separate endpoint obligation and the completed endpoint lemma.

[Overview owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A9:Q9) · [Catalogue current owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001001&range=AA4:AF4) · [Novelty current owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001003&range=U7:Z7) · [Theorem owner](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=404576783&range=A22:J22).

Repository main was verified as `a74d66f28f70e721cd1adfad668146a0d53bb78c`. The [pinned open-record index](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json) contains the same F020 gate and 58 score. Its census remains 248 open, 79 closed, 327 overview records. This review changes none of those counts.

## 2. The exact actual-family question

Work in F2[q]. Set b=2m+1 for m>=1. Use the actual Gaussian family and ordinary derivatives:

H_b(z;q)=(z+1)U_m(z;q),
U_m(z;q)=z^m P_m(z+z^-1;q),
P_m(X;q)=A_old(X^2;q)+X B_old(X^2;q).

Define E_m=P_m(0;q), R_m=Res(A_old,B_old), Q_m=E_m R_m, N_m=deg Q_m=m(m+1)(2m+1)/3 and Q_m*=q^N_m Q_m(q^-1). Reversal is at the actual nonzero degree. Let L_b=product_{r=0}^m(1+q^(2r+1)).

The open assertion is, for every m>=1,

    (Q_m,Q_m*)=(1) in F2[q,1/L_b].

Equivalently, one must produce all-m polynomial coefficients a_m,c_m satisfying a_m Q_m+c_m Q_m*=L_b^N_m, or disprove the assertion by one actual-family common irreducible factor whose root has certified exact odd order greater than b. The coefficient-pair descent to T=q+q^-1 gives a smaller equivalent certificate, not its proof: with the accepted balanced pair A_m(T),B_m(T), the missing statement is support(gcd(A_m,B_m)) contained in support(D_m), where D_m=T product_{r=1}^m J_(2r+1)(T).

The obstruction has four channels: endpoint/endpoint, endpoint/collision, collision/endpoint and collision/collision at inverse parameters. A zero of E_m at one parameter, or a zero of R_m with a good inverse parameter, is insufficient. Distinct inverse Frobenius orbits cannot be silently identified. A self-reciprocal component must also be covered.

This interpretation follows the exact reciprocal descent in `sources/RECIPROCAL_DESCENT.md`, Sections 1, 4, 5 and 7, and the current live owner cells. The free quadratic algebra and coefficient syzygies are sound; they do not force the descended coefficient gcd to have low-order support.

## 3. Mathematical value and the theorem already obtained

The characteristic-zero all-A separated and one-simple-overlap formulas have an explicit accepted derivation from the finite q-binomial identity, the weighted block-divisibility lemma, the first derivative at the shared root, and root-product discriminant algebra. The complete local leading constants are more information than below-weight vanishing alone. The copied all-order proof is SHA-256 `8ca570c7e7c41c50827b1dea3feb931cbcfe0fdab3c3a2016c6e7d0989126abc`, exactly the proof identified by its independent review.

That is useful explicit algebraic work with a clear scope. It does not establish historical priority, a general new q-binomial mechanism, arbitrary residual guard removal, all-A overlap guard removal for every b, or an FFT improvement. The primary [Schultz–Walker Theorem 1.1](https://arxiv.org/pdf/1202.0199v1), printed page 3, was re-opened in this pass: it supplies a cyclotomic divisibility/vanishing result, not all of the surviving moving-root coefficients. The [DLMF confluent Christoffel–Darboux identity](https://dlmf.nist.gov/18.2.E13) identifies the classical kernel mechanism; its usual positive orthogonality interpretation cannot be transferred to characteristic-two noncancellation.

The remaining actual-family paired-support assertion has a concrete, potentially substantial consequence: it would supply a uniform sufficient modular guard for characteristic-zero ordinary residual squarefreeness. It is therefore not justified to discard that mathematical question solely because its reductions use classical tools. Its present tractability remains low: the known mechanisms have reached explicit nonimplication boundaries, and this review found no all-m certificate. No score increase or novelty claim is proposed.

## 4. What the accepted endpoint results do and do not cover

At an exact odd order d=2h+1, the accepted complementary identity relates indices m+n=h-1 through unit products C_j and D_j:

    C_h C_n E_m + D_h C_m E_n* = C_m C_n.

For n=m it proves paired endpoint exclusion on d=4m+3. The later eighth-root/affine transport, followed by three exact small symbolic certificates, proves endpoint-only exclusion on d=2m+3, 2m+5 and 2m+7 for all m>=1. The [pinned independent review](https://github.com/AgentSlop-Si/research/blob/a74d66f28f70e721cd1adfad668146a0d53bb78c/math/reviewed_rounds/2026-10-13-reviewed-2222/f020/REVIEW.md) explicitly preserves the general endpoint and full gates as open.

The repository review was fetched and compared byte-for-byte with the accepted local review. Both have SHA-256 `8588aaf1e538a85b6d63c43412aa53d2368e50900f022409172ba6ecb1a3a180`.

A complementary index smaller than m gives a prescribed nonzero affine endpoint value, not another smaller paired-zero problem. Thus this is not a descent induction. The all-n affine-polynomial support formulation is equivalent to the unproved general endpoint assertion; it is not a completed proof. Even a future full endpoint proof would leave the three channels involving collisions open.

## 5. Directly checked reason full-spectrum reflection does not finish the proof

The source-bound complementary-chain construction gives the exact squarefree full trace polynomial CYC_d and forces common spectral roots of complementary blocks to be simple in their gcd. It does not exclude distinct repeated-root coordinates. The following source countermodel was independently re-expanded algebraically in this pass, without executing a supplied program.

Let w^2+w+1=0 in F4. Consider the five-vertex tridiagonal chain with diagonal (0,0,1,0,0), upper diagonal entries all 1, and lower diagonal (w^2,w^2,w,w). All edge products are units and Frobenius conjugation w -> w^2 reverses the diagonal/edge data. Its complementary degree-two polynomials are

    L=X^2+w^2=(X+w)^2,
    R=X^2+w=(X+w^2)^2.

Both have double roots, at different coordinates. Their product is X^4+X^2+1. The full central-cut expansion is

    (X+1)LR+w^2 X R+w X L
      =X^5+X^4+X^2+X+1=CYC_11(X).

The last two summands combine to X^3, canceling the X^3 term in (X+1)LR. The derivative of the resulting polynomial is X^4+1=(X+1)^4 and its value at X=1 is 1, so it is squarefree. Hence exact simple full spectrum, reflected unit edges and complementary common-root restrictions do not imply that one of the two blocks is squarefree.

This is not the actual RS chain: its first diagonal is zero, whereas the actual a_1=alpha(1+alpha) is nonzero at order 11. It therefore blocks only that structural inference. A valid actual-family continuation must exploit further features of a_j=q^(2j-1)(1+q) and c_j=(1+q^(2j-1))(1+q^(2j-2)), or another genuinely stronger actual-family property.

The separate accepted actual m=12/order-31775 witness blocks one-sided collision-kernel noncancellation: every edge and kernel summand is nonzero but the sum vanishes, while the inverse parameter is good. That numerical certificate was read as accepted source evidence here, not recomputed. It is not an actual paired-support counterexample.

## 6. Clarified discriminant implication and its strict scope

The following elementary derivation clarifies why the full modular question is sufficient but stronger than necessary for the characteristic-zero residual goal. It is not claimed historically new or accepted as a replacement task.

For a monic integral trace polynomial P_m with U_m(z)=z^m P_m(z+z^-1), root products give

    Disc_z(U_m)=P_m(2) P_m(-2) Disc_X(P_m)^2.

Indeed write U_m as the product of quadratics z^2-x_i z+1. Each quadratic contributes x_i^2-4; the resultant of the quadratics for x_i and x_j is (x_i-x_j)^2. Multiplying the within- and cross-factor discriminants proves the formula as a universal polynomial identity, including specializations with repeated roots.

Modulo 2, P_m=A_old(X^2)+X B_old(X^2), so the ordinary derivative is B_old(X^2) and the monic resultant identity gives Disc(P_m)=R_m^2. Consequently

    reduction_mod_2(Disc_z U_m)=E_m^2 R_m^4.

Suppose the characteristic-zero residual has zero discriminant at a primitive odd d-th root, d>b. The monic cyclotomic polynomial Phi_d then divides its integer discriminant polynomial. After reduction, every irreducible factor of the squarefree reduced Phi_d divides Q_m. Since reduced Phi_d is reciprocal and its roots retain exact order d, both each factor and its reciprocal divide Q_m. Thus there is a common factor of Q_m,Q_m* outside L_b. The proposed full unit ideal excludes this situation.

The converse does not follow. One high-order common inverse pair can be only a proper subset of the primitive cyclotomic components, and modular vanishing need not lift to characteristic zero. For a concrete logical illustration unrelated to the RS family, over F2 take f=q^5+q^2+1 and f*=q^5+q^3+1. The first has no linear factor and reduces to 1 modulo q^2+q+1, so is irreducible of degree five; its nontrivial root has order 31 because 31 is prime and divides 2^5-1. Its reciprocal is distinct with the same order. The reciprocal polynomial f f* has a paired order-31 obstruction but degree 10, whereas Phi_31 has degree 30; it does not contain all primitive components. This illustrates only a strict logical gap and is not an actual-family counterexample.

Therefore a direct all-m/all-d proof that some primitive mod-2 component is good would also suffice for characteristic-zero residual squarefreeness. It would not prove the owner's full paired-support assertion. No such uniform component-selection proof is supplied here, and no alternative task is automatically selected. General overlap simplicity remains another guard even after ordinary residual squarefreeness.

## 7. Exact stopping and reopening conditions

Current justified stop: the known reductions and source-bound accepted results do not provide the missing actual-family uniform nondegeneracy. The blocker is mathematical, not lack of a file, computer or execution permission.

The current full gate can close only with one of:

1. An all-m actual-family localized certificate, with m=1 and zero-coefficient boundaries, actual-degree reversal, low-order localization and all four channels retained; or
2. One actual-family common factor, with m, both exact divisibilities, irreducibility, exact root order greater than 2m+1 and its inverse-orbit behavior certified.

A source-bound new lemma may be a bounded research advance, but must state what remains. Do not promote another finite-b certificate, a norm zero, common-coordinate exclusion, a synthetic spectral model or a one-sided actual collision to closure. Preserve completed finite stages and their original claims. This report recommends no external status, score or count change.

## Evidence inventory and review limits

Native owner snapshots and connector responses are excluded from this publication. The eight inert proof/review bodies cited here are retained under sources/, with their identities in SOURCE_BINDINGS.json.

This pass reread the actual formulas and mathematical arguments, checked owner consistency, re-expanded the exact F4 model, and derived the discriminant implication above. It did not rerun historical certificates, conduct a new fixed-m search, verify every archived control, retrieve every historical source body, or establish publication priority. The route counterexample is inherited and independently re-expanded, not a new family discovery. The author of this report does not supply a separate independent acceptance of any new proof claim.
