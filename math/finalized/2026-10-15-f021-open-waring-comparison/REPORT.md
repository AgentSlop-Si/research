# F021: Exact legal scalar chirp-resolvent minima and open Waring rank

Date: 2026-10-15 UTC  
Repository baseline: AgentSlop-Si/research, commit 21aac668f52b5680b8b22eb99d53a850ae0cd394  
Intended path: math/finalized/2026-10-15-f021-open-waring-comparison/REPORT.md

## Verdict

Independent mathematical review ACCEPTED, with no correction. The generic legal-node minimum mechanism is already implied by classical binary-form theory. The chirp-specific classification and implementation retain their separate obligations.

This is an analytical mathematical and source-attribution comparison. No Lean proof, kernel check, or other formal verification occurred. Keep F021 OPEN and parent priority 53 unchanged. This is an attribution refinement within the existing claim, not a new canonical theorem.

## 1. Primary source and precise result

Edoardo Ballico and Alessandro De Paris, “Generic Power Sum Decompositions and Bounds for the Waring Rank,” Discrete & Computational Geometry 57(4), 896–914 (2017), DOI 10.1007/s00454-017-9886-7.

The accepted manuscript was read at Definition 2.1 and Proposition 3.1, including the complete proof and characteristic-zero, algebraically closed field convention:

- HTML: https://arxiv.org/html/1312.3494v2
- PDF: https://arxiv.org/pdf/1312.3494v2
- Journal DOI: https://doi.org/10.1007/s00454-017-9886-7

In the PDF, Definition 2.1 and Proposition 3.1 are on printed pages 4–5. Version 2 was posted in 2018; the journal publication is 2017.

For a nonzero degree-d binary form F, Proposition 3.1 gives Ork(F)=d+2−ℓ(F), where ℓ is its least nonzero apolar degree. Definition 2.1 quantifies over every prescribed proper closed subset of the projective node line. Such subsets are finite. This provides exact decompositions outside the forbidden set, rather than only limiting or confluent representations.

The following moment/resolvent translations and consequences are derived here.

## 2. Exact common-cycle bank translation

Work over the algebraic closure of K=Q(q), where q is primitive of odd order N=2m+1≥3. Set h=(N+1)/2 and f_k=q^(h k²). Fix the same natural N-cycle P throughout.

The legal resolvent identity is

    (I−λP)⁻¹ = Σ_(k=0)^(N−1) λ^k P^k /(1−λ^N).

Because I,P,…,P^(N−1) are linearly independent, a no-diagonal bank is equivalent to

    f_k=Σ_i b_i λ_i^k, 0≤k≤2m,
    b_i=a_i/(1−λ_i^N).

Define the binary moment form

    B_d(u)=Σ_(k=0)^d binom(d,k) u_k X^(d−k)Y^k.

Then

    B_d(u)=Σ_i b_i(X+λ_iY)^d

is exactly the same finite moment identity. Nonzero coefficients can be absorbed into dth powers over the algebraic closure, so weighted and ordinary Waring formulations have the same minimum.

The forbidden projective set is precisely

    E_N={[1:0],[0:1]} ∪ {[1:ξ]: ξ^N=1}.

These exclude λ=0, λ=∞, and every resonant pole. Every remaining node gives an actual legal resolvent, with a_i=(1−λ_i^N)b_i.

Repeated projective nodes can be combined and zero coefficients deleted. Neither operation creates an illegal node. Thus a minimum decomposition can be taken with distinct nodes and nonzero coefficients. The count is scalar resolvent occurrences; it is not the count of distinct closing weights λ_i^N.

## 3. Apolarity normalization

For a homogeneous degree-r differential polynomial

    A(U,V)=Σ_(j=0)^r t_j U^(r−j)V^j,

direct differentiation gives

    A(∂X,∂Y)B_d(u)
      = [d!/(d−r)!] Σ_(k=0)^(d−r) binom(d−r,k)
        (Σ_(j=0)^r t_j u_(k+j)) X^(d−r−k)Y^k.

Therefore the apolar equations are exactly the Hankel recurrence equations. In particular, A(1,λ)=Σ_j t_j λ^j, so there is no reciprocal-node or sign reversal hidden in the map.

## 4. No free diagonal: the legal minimum follows

Take F=B_(2m)(f_0,…,f_(2m)). Its degree-m contraction matrix is

    H=[f_(i+j)]_(0≤i,j≤m).

The chirp identity

    f_(i+j)=f_i f_j q^(ij)

factors H into invertible chirp diagonals and a Vandermonde matrix on 1,q,…,q^m. Hence H is nonsingular.

There is no nonzero degree-m apolar polynomial. A lower-degree one would yield a degree-m one by multiplication, so none exists below m either. At degree m+1, the contraction map has domain dimension m+2 and target dimension m; its kernel is nonzero. Thus ℓ(F)=m+1.

Proposition 3.1 now provides an exact decomposition with at most m+1 nodes outside E_N. Meanwhile any Q-node moment representation expresses H as a sum of Q rank-one matrices, forcing Q≥m+1.

Consequently Q_min=m+1 in the exact legal scalar common-P model.

The upper and lower bounds also force every term of a minimum representation to survive merging/deletion. Its nodes are distinct and its amplitudes nonzero.

## 5. Free diagonal: the complete generic root-guard criterion follows

Allow

    C=δI+Σ_i a_i(I−λ_iP)⁻¹.

Only f_0 changes. Set g_k=f_(k+1), 0≤k≤2m−1, and G=B_(2m−1)(g).

A bank gives shifted weights

    c_i=b_iλ_i,
    g_k=Σ_i c_i λ_i^k.

Conversely, any shifted decomposition outside E_N gives

    a_i=c_i(1−λ_i^N)/λ_i,
    δ=f_0−Σ_i c_i/λ_i.

Thus the minimum number of nontrivial branches with a free diagonal equals the fixed-forbidden-set rank of G.

The shifted Hankel matrix

    H₁=[f_(i+j+1)]_(0≤i,j<m)

is nonsingular because

    f_(i+j+1)=f_1(f_iq^i)(f_jq^j)q^(ij).

The degree-(m−1) contraction matrix contains H₁ as an invertible submatrix. The degree-m contraction has m rows and m+1 columns, with its first m columns equal to H₁. Therefore ℓ(G)=m and its degree-m apolar kernel is one-dimensional.

Its uniquely normalized monic polynomial is exactly the existing shifted annihilator T_m:

    Σ_(j=0)^m t_j f_(k+j+1)=0, 0≤k<m,
    t_m=1.

Proposition 3.1 gives the legal upper bound m+1. The shifted Hankel rank gives the lower bound m.

An m-node legal decomposition necessarily has annihilator ∏_i(z−λ_i)=T_m(z). Therefore T_m must be squarefree and its roots must avoid 0 and μ_N. Its monicity already excludes a projective root at infinity.

Conversely, suppose these guards hold. Solve the first m shifted moments using the invertible Vandermonde matrix at T_m’s roots. The annihilator recurrence then supplies the remaining m shifted moments. Every shifted coefficient c_i is nonzero, since otherwise H₁ would have rank below m. The displayed coefficient conversion gives nonzero legal a_i and restores f_0 with δ.

Hence

    Q_min=m     if T_m has simple, nonzero, nonresonant roots;
    Q_min=m+1   otherwise.

This is the full generic criterion in F021’s grammar. It uses no different cycles, repeated-pole derivatives, projective closure, approximate fitting, or branch-dependent endpoints.

An arbitrary added diagonal still collapses to δI: both the target and bank are circulants, and a diagonal circulant is scalar.

## 6. Concrete distinction from ordinary Waring rank

At N=3, h=2 and g_0=g_1=q². Thus G=q²(X+Y) has ordinary Waring rank one, but its unique one-node representation uses λ=1, which is resonant. Its legal rank is two.

An explicit legal choice is λ₁=2, λ₂=3 with shifted weights c₁=2q², c₂=−q². Conversion gives

    a₁=−7q²,
    a₂=26q²/3,
    δ=1−2q²/3.

Indeed c₁+c₂=q² and 2c₁+3c₂=q². Both nodes are nonzero and neither is a cube root of unity. The corresponding bank is

    C=(1−2q²/3)I
      −7q²(I−2P)⁻¹
      +(26q²/3)(I−3P)⁻¹.

This is an exact hand-checked symbolic example, not an executable experiment. It shows why the forbidden-set formulation is essential.

## 7. What this comparison does not establish

Ballico–De Paris does not itself compute or establish:

- T_m(z)=(-1)^m H_m(−z;q);
- the chirp-specific gcd with z^N−1;
- prime-order, family-specific, or all-composite squarefreeness;
- the evaluated forced-diagonal product;
- individual nodes lying in Q(q);
- the finite 2N+1-parameter search or its precise operation count;
- the root-free quotient-algebra implementation or its charged costs.

These must keep their existing sources and qualifications. “Not supplied by this theorem” does not imply novelty.

In particular, the existing LS87 attribution of moment, annihilator, and product identities remains intact. The accepted O(N³) general setup/O(N²) application, and O(N²) successful lower-bank setup, remain exact base-field-operation statements with supplied q. No bit-complexity, stability, root-extraction, unrestricted inverse minimum, or FFT speedup follows here.

The source’s Ork is a worst-over-forbidden-sets quantity. It must not be identified automatically with the rank for E_N. The full-moment equality above uses its Hankel lower bound; the shifted case uses the unique-annihilator test.

Historical priority of the exact chirp specialization remains unresolved. The present implication narrows the attribution boundary; it does not certify worldwide priority for any remaining part.

## 8. Exact proposed attribution text

“Ballico–De Paris (2017), Definition 2.1 and Proposition 3.1, via exact full/shifted moment-to-binary-form maps, already imply the finite-forbidden-node legal m+1 existence and generic free-diagonal m-versus-m+1 root-guard criterion over an algebraic closure. Zero, infinity and all cycle-resonant nodes are excluded explicitly; simple distinct nodes and nonzero weights are retained. The chirp-specific resonance classification, scoped squarefreeness, previously attributed moment/product identities, and charged construction remain separately sourced. Correctness unchanged; exact specialization priority and all-composite squarefreeness remain unresolved.”

Suggested next-action text:

“The generic legal-node existence/minimum mechanism now has an exact primary-source implication. Further attribution work should target a concrete primary theorem for the chirp-specific root-of-unity resonance/simplicity classification or the explicit charged construction. Preserve all current field, model and complexity guards.”

Keep F021 OPEN and parent priority 53 unchanged. This is an attribution refinement within the existing claim, not a new canonical theorem.

## 9. Exact minimal cell proposal

This is a proposal only; no spreadsheet mutation was made by the author of this report.

Make four additive cell edits, preserving each cell’s existing text verbatim. Append two newline characters followed by the exact supplement specified below.

Append to Catalogue!AD14 and 'Research overview'!O19:

[2026-10-15; independent mathematical review ACCEPTED]
Ballico–De Paris (2017), Definition 2.1 and Proposition 3.1, via exact full/shifted binary-moment maps, imply the legal m+1 existence and generic free-diagonal m-versus-m+1 root-guard criterion over an algebraic closure. The forbidden set explicitly includes zero, infinity and every Nth root of unity; nodes remain simple and weights nonzero. Chirp-specific resonance, scoped squarefreeness, previously attributed moment/product identities and charged construction remain separately sourced. Correctness unchanged. Exact chirp-specialization priority and all-composite squarefreeness remain unresolved. Analytical review only; no Lean or kernel verification. Parent priority 53 and OPEN research status are unchanged.

Append to Catalogue!AE14 and 'Research overview'!P19:

[2026-10-15; narrowed attribution next step]
The generic finite-forbidden-node minimum mechanism now has an exact primary-source implication from Ballico–De Paris (2017), Definition 2.1 and Proposition 3.1. Resume attribution only for a concrete primary theorem matching the chirp-specific root-of-unity resonance/simplicity classification or the explicit charged construction. Retain the same natural cycle, scalar first-order nonconfluent branches, simple nonzero nonresonant nodes, algebraic-closure field scope, optional single scalar diagonal, and existing cost qualifications. No new correctness re-audit, all-composite squarefreeness, unrestricted inverse minimum, numerical stability or worldwide-priority clearance.

Do not change Catalogue!AA14, 'Research overview'!L19, the existing status cell 'Research overview'!E19, either accepted theorem statement, or either current stopping-boundary cell. In particular, the source comparison does not close the remaining chirp-specific priority gate.

## 10. Evidence and limits of this pass

Read against commit 21aac668f52b5680b8b22eb99d53a850ae0cd394:

1. Original global-bank theorem:
https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/a1/a1a1343cfb791786360752cd1e32f4767a469657223c98aa8fd418fb7b811c3e__GLOBAL_MOMENT_CHIRP_BANK.md

2. Global-bank independent audit:
https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/df/dfea8a0a54f747e9af09acceb7d92b0345233731da03fe9ed0e86f4d26524c6a__INDEPENDENT_AUDIT.md

3. Free-diagonal classification:
https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/c6/c64b813620686131f520339c14a0e5efc1c859999c228c823faf68e943d5a0b1__CLASSIFICATION.md

4. Classification independent audit:
https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/af/af52543f5eddb8bbcdc1c96bc3fde65db64b58090eb0ed36d93eb0cc1d141333__INDEPENDENT_AUDIT.md

The live owner rows supplied the current accepted scope and stopping gate:

- Catalogue row 14:
https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001001&range=A14:AF14

- Research overview row 19:
https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A19:Q19

The separate October 13 source-closure archive was not re-extracted. Its absence from this pass is not a claimed proof gap. No executable checks, formal verification, fresh archive-hash verification, or spreadsheet changes were performed in this analytical comparison.

The independent reviewer checked the derivative normalization, both kernel-dimension arguments, coefficient bijections, forbidden set, distinctness/nonzero amplitudes, optional-diagonal recovery, and proposed attribution text, and accepted this bounded comparison. Its verdict is independent mathematical review ACCEPTED, not formal verification.

This report contains original mathematical explanation and bounded source attribution, not a reproduced third-party paper. Persistence as a Git blob alone does not commit a path or update a branch; publication requires a separately verified commit/ref update.
