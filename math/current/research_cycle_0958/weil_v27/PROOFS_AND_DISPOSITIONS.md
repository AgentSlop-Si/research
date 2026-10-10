# v27 primitive Weyl embedding audit and cyclic-resolvent fusion

Date: 2026-10-10. Complete mathematical reconstruction; independent review is recorded separately. Supplied programs and bytecode were not executed, imported, or AST-parsed. The only research program executed for this audit is the freshly authored `fresh_controls.py`.

## 0. Disposition

1. The primitive Weyl normal form, full matrix algebra, common invariant-subspace classification, swap-intertwiner classification, and covariant extraction identity are correct under the exact hypotheses below. They are classical finite Stone–von Neumann/matrix-algebra consequences, not a new representation-theoretic discovery.
2. Three qualifications matter: the extracted scalar can vanish; an individual Schrödinger copy need not be invariant under the swap; and the normalizing similarity need not be unitary or cheap to apply.
3. The coordinate spectator theorem is correct for the stated ambient `(Z/NZ)^n`. Its blanket extension to every larger character table is false: `F_N` occurs in `F_(N²)` at rows `Ni` and columns `j`, while `Z/N²` has no direct `Z/N` summand.
4. The operation ledger needs correction. Generic multiplicity-space injection/extraction can cost `Theta(Nm)` in canonical coordinates, and arbitrary physical similarities can be much more expensive. A unitary normalized ambient coordinate extraction also has a nontrivial normalization loss.
5. These facts do not prove that a faster FFT must abandon Weyl covariance. They exclude smaller common invariant state spaces and classify operators; they provide no unrestricted arithmetic runtime lower bound.
6. A separate useful new-to-project fusion is proved in §7: an exact ambient swap on `Nm` dimensions has minimal-polynomial degree at most `4m`, whereas a nonzero weighted Hamiltonian-cycle resolvent has degree `Nm`. Thus the latter cannot be the ambient swap for `N>4`, even after arbitrary similarity. This is a representation exclusion, not an FFT runtime result.

## 1. Exact contract and primitive block normal form

Let `N>=2`, let `K` be a field with a specified primitive `N`th root `zeta`, and let `W` be a finite-dimensional, nonzero K-vector space. Assume

`X^N=Z^N=I`, and `ZX=zeta XZ`.

The power identities already make X and Z invertible. Existence of a root of exact order N implies that char(K) does not divide N; stating that condition separately is harmless. No algebraic closure, positivity, square root of N, oddness, or complex absolute value is needed. The N=1 case is trivial; W=0 is accommodated by m=0 rather than the source's m>=1.

Define `S e_j=e_(j+1 mod N)` and `D e_j=zeta^j e_j`. Put `M=ker(Z-I)`. Since `t^N-1` splits into distinct factors over K,

`W=direct_sum_(j=0)^(N-1) W_j`, where `W_j=ker(Z-zeta^j I)`.

The relation ZX=zeta XZ gives `X W_j=W_(j+1)`. Nonzero W therefore has all N eigenspaces present with the same positive dimension m. The explicit map

`B: K^N tensor M -> W`, `B(e_j tensor a)=X^j a`

is an isomorphism and satisfies

`B^-1 X B=S tensor I_m`, `B^-1 Z B=D tensor I_m`.

The last-to-first shift uses X^N=I. Starting from an arbitrary Z-eigenvalue lambda without relabeling gives lambda D, not literally D; choosing W_0 fixes this minor omission in the source proof. In particular `dim W=Nm`.

### 1.1 Explicit matrix units and the whole module category

Set `Q_j=N^-1 sum_(b=0)^(N-1) zeta^(-jb) D^b`. Character orthogonality gives `Q_j=e_j e_j^T`. Thus `S^(i-j)Q_j=E_ij`; the generated algebra is M_N(K). The N² words S^a D^b span and therefore form a basis. On W, the algebra is `B(M_N(K) tensor I_m)B^-1`.

An operator commuting with the diagonal matrix units is diagonal in the first coordinate, and commuting with all E_ij forces those diagonal multiplicity blocks equal. Therefore the commutant is `B(I_N tensor End(M))B^-1`.

If L is a common X,Z-invariant subspace, it is invariant under every matrix unit. Define `M_L={a : e_0 tensor a lies in B^-1 L}`. Applying E_0j to each coordinate component and E_j0 in reverse proves

`L=B(K^N tensor M_L)`.

This establishes the complete common invariant-subspace classification, not merely a lower dimension bound. There is only one irreducible isomorphism type: W is isotypic, consisting of m equivalent N-dimensional Schrödinger modules. More generally, all intertwiners between multiplicities m and r are `I_N tensor A`, for arbitrary `A:K^m -> K^r` in the chosen normal forms.

The word “invariant” must mean invariant under both X and Z. It cannot mean invariant merely under J or under the Weil group: Fourier itself has proper eigen-subspaces, and Weil representations can be reducible even though the underlying Heisenberg representation is irreducible.

### 1.2 Essential hypotheses

If zeta has order d<N with d dividing N, the d-dimensional standard pair satisfies X^N=Z^N=I and the same nonprimitive commutation relation. The N-dimensional minimum then fails. For example N=6, zeta=-1, and S_2,D_2 give dimension two.

If the power identities are dropped, taking X=tS with t^N!=1 retains the primitive commutation relation but cannot be similar to S. In the unrestricted quantum-torus algebra, X^N and Z^N are additional central operators; they cannot silently be normalized away. If a central character varies between summands, one must first separate its isotypic components. The theorem here fixes the primitive scalar zeta on all of W.

## 2. Swap classification and exact extraction, including zero coupling

Use the unnormalized matrix `F[i,j]=zeta^(ij)`. Direct entries give

`FS=DF`, `FD=S^-1 F`, `F²=N R`, `F^4=N² I`,

where `R e_j=e_(-j)`. Also `F^-1[i,j]=N^-1 zeta^(-ij)`.

For an invertible J satisfying `JXJ^-1=Z`, `JZJ^-1=X^-1`, put `J0=B^-1 J B`. Then `(F^-1 tensor I)J0` commutes with S tensor I and D tensor I. By §1.1,

`J=B(F tensor U)B^-1`, with `U in GL_m(K)`.

Conversely every such U gives a swap. Without invertibility, the linear solution space of `JX=ZJ`, `JZ=X^-1J` is still exactly `B(F tensor U)B^-1` for arbitrary U in M_m(K), and its dimension is m².

Let E and P satisfy all four exact intertwining equations

`XE=ES`, `ZE=ED`, `PX=SP`, `PZ=DP`.

The full Hom classification gives

`E=B(I_N tensor a)`, `P=(I_N tensor ell)B^-1`,

for a in M and ell in M*. Hence

`PE=ell(a)I`, and `PJE=alpha F`, where `alpha=ell(Ua)`.

E is injective iff a!=0; P is surjective iff ell!=0. Neither implies alpha!=0. Even PE=I does not imply nonzero coupling: take m=2, a=e_1, ell=e_1*, and `U=[[0,1],[1,0]]`. Then PE=I but PJE=0. The identity remains true, but recovery of F requires the separate condition alpha!=0 and the charged multiplication by alpha^-1.

An image copy `B(K^N tensor Ka)` is J-invariant iff Ua is a scalar multiple of a. A general U mixes those copies. Over a field where U has no eigenvector, there need not be a J-invariant N-dimensional common X,Z-submodule at all. Even over C, a nondiagonalizable U need not admit a decomposition into J-invariant N-dimensional copies. The precise statement is “Fourier on the representation factor, with arbitrary multiplicity action,” not “the same Fourier operator on each separately preserved block.”

## 3. Similarity, unitarity, conditioning, and preparation

### 3.1 Algebraic similarity is not a unitary coordinate change

Over C, if X and Z are unitary in the physical inner product, their Z-eigenspaces are orthogonal. Choose an orthonormal basis of W_0; powers of unitary X transport it to orthonormal bases in all W_j. The B constructed in §1 is then unitary.

For the normalized Fourier `Fhat=N^-1/2 F`, write J in that basis as `Fhat tensor V`. If J is unitary, V is unitary. With the source's unnormalized F, unitary J instead requires `U*U=I_m/N`.

Without unitary X,Z, the claimed unitary normal form is false. Take any N>=2 and `B=diag(t,1,...,1)` with real t>1, let X=BSB^-1 and Z=D. The Weyl identities hold, but X is not unitary, whereas a unitary conjugate of S would be unitary. Thus only arbitrary similarity is guaranteed. The construction also shows that its condition number can be arbitrarily large.

### 3.2 Extraction norm cost

For the unitary normal form and normalized J=Fhat tensor V,

`||E||=||a||`, `||P||=||ell||`, `alpha=ell(Va)`.

With E,P exact and an ambient application error `||Delta J||<=delta`, the normalized recovered map has error at most

`delta ||P|| ||E|| / |alpha|`.

There is no uniform bound without a quantitative nonzero-coupling certificate. For instance a=e_1 and ell=e_1* have norm one while a unitary rotation V can have V_11=epsilon arbitrarily small. PE=I still holds. For a nonunitary B the same bound holds with the actual physical norms, and `||P||||E||<=kappa(B)||ell||||a||`; no small kappa(B) follows from covariance.

For coordinate extraction from a normalized ambient character table on M points whose unnormalized selected submatrix is F_N, the selected normalized matrix is

`sqrt(N/M) Fhat_N`.

Coordinate injection and extraction have norm one, so normalization requires sqrt(M/N). In particular an N²-point ambient table incurs sqrt(N), not unit normalization. This matters for any approximate evaluator or precision ledger. Finite-field tests do not establish complex norm or stability claims.

### 3.3 Fully charged work

For dense a and ell in canonical multiplicity coordinates, explicitly materializing E(v) writes Nm entries, and applying P performs N length-m dot products. Those straightforward operations cost Theta(Nm), not automatically O(N) when m grows. Sparse fixed a,ell or implicit layouts may give O(N), but that is an extra implementation contract. In physical coordinates, E and P include B and B^-1; a generic B can make them dense even when m=1. Finding B from a given matrix description also requires charged eigenspace/linear-algebra work.

The exact guaranteed reduction is

`T(F_N) <= T(E) + T(J on E-inputs) + T(P) + O(N)`

when alpha!=0 and scalar arithmetic/scaling is charged. The source's Omega(N) statement about reading/writing N coordinates belongs to a model that charges data movement. Identity views may perform no scalar arithmetic. Neither this I/O bound nor the representation classification implies Omega(N log N) arithmetic.

Roots and coefficient-field construction, orders/primitive-root certificates, stored constants, normalizing scalars, descriptions of E,P,J, and preparation are separate charges. Existence of a primitive root in K is an algebraic hypothesis; it is not an efficient root-discovery theorem. Complex sqrt(N) is used only for the metric normalization above. Exact finite-field controls use no analytic square root.

### 3.4 What the theorem leaves open

The source's conclusion that a faster route “must abandon” the covariance contract does not follow. Taking W=K^N, E=P=I and J=F already satisfies it. A hypothetical faster exact algorithm for J would preserve all those identities. Larger-space structured evaluation can likewise only be judged by its actual charged algorithm. The established obstruction is to shrinking the common primitive Weyl state factor below N, not to every possible faster way of evaluating it.

## 4. Coordinate embeddings: complete proof and precise domain

Let `R=Z/NZ`, `V=R^n`, with the perfect bilinear pairing x^T y. Suppose, after selecting and ordering N rows and columns, there are nonzero row/column scalars r_i,c_j such that

`zeta^<x_i,y_j> = r_i c_j zeta^(ij)` for 0<=i,j<N.

Dividing the (i,j),(0,0) entries by (i,0),(0,j) removes all gauges. Because zeta has exact order N,

`<x_i-x_0,y_j-y_0>=ij mod N`.

Put u=x_1-x_0 and v=y_1-y_0. Then <u,v>=1. The maps `R -> V`, t↦tu, and `V -> R`, x↦<x,v>, compose to the identity. Thus

`V=Ru direct_sum ker<-,v>`.

Dually `V=Rv direct_sum ker<u,->`. Define

`w_i=x_i-x_0-iu`, `w'_j=y_j-y_0-jv`.

The j=1 and i=1 equations give <w_i,v>=<u,w'_j>=0. Expansion of the general equation leaves <w_i,w'_j>=0. This proves necessity for all N, including even and composite N. Conversely these identities imply the anchored grid ij, and translations x_0,y_0 contribute only separable row/column gauges. They therefore completely characterize the stated ordered embeddings.

The residual coordinates need not be affine-linear in i,j. For N=p², take `x_i=(i,p i²)` and `y_j=(j,p j²)` modulo p². Both sides can have nonzero spectators, yet their products vanish modulo p². The selected matrix remains exactly F_N.

The conclusion concerns a split cyclic factor of the paired module, not a claim that the selected N-row and N-column sets are themselves Cartesian product subsets. Their mutually orthogonal residuals do not affect this selected phase grid. It does not follow that they cannot affect the cost or conditioning of an ambient implementation.

### 4.1 Valid broader setting, and an exact counterexample to an overbroad setting

The same splitting proof works for a finite abelian group G of exponent dividing N paired perfectly with its character group, with values in the Nth roots. A primitive pairing forces an element u of order N and a character v evaluating zeta at u, giving `G=<u> direct_sum ker v` after identifying v's values with Z/NZ. The exponent bound is substantive.

For any N>=2, instead take G=Z/N²Z with a primitive N²th root eta and set zeta=eta^N. The unnormalized character table has entries eta^(xy). Choosing row labels x_i=Ni and column labels y_j=j gives

`eta^(Ni j)=zeta^(ij)`.

So it contains F_N exactly, but its unique subgroup of order N is not a direct summand: a decomposition Z/N² ≅ Z/N × H with |H|=N would have exponent at most N, contradicting exponent N². This is a counterexample to a blanket “every larger additive character table” claim, not to the source's explicitly stated V=(Z/NZ)^n theorem and not to the Weyl-covariant theorem.

For normalized transforms the selected submatrix is N^-1/2 Fhat_N, requiring a sqrt(N) rescaling. Running a complete N²-point transform is not a speedup over a conventional N-point FFT; no fast restricted evaluator has been supplied here. Primitive roots of order N² would also be part of the preparation contract.

## 5. Primary-source comparison and novelty limits

The following are primary texts actually inspected on 2026-10-10, including their stated theorems and the nearby proofs. They give a substantially closer comparison than the source's general background citation.

- **Amritanshu Prasad, On character values and decomposition of the Weil representation associated to a finite abelian group**, [arXiv:0903.1486](https://arxiv.org/pdf/0903.1486), §§2–5. Theorem 3.1 treats every finite abelian group over C, including even orders; Lemma 3.2 explicitly states that Weyl operators form a full endomorphism-algebra basis; Example 3.4 identifies Fourier as the translation/modulation intertwiner; §5 gives uniqueness up to scalar for center-preserving automorphism intertwiners. These are direct antecedents of v27 §§2–3. The arbitrary-multiplicity tensor/Hom formulas are the standard matrix-module consequences proved in this audit. The paper also distinguishes Heisenberg irreducibility from reducibility of the Weil representation.
- **Prasad, An Easy Proof of the Stone–von Neumann–Mackey Theorem**, [arXiv:0912.0574](https://arxiv.org/pdf/0912.0574), §4 theorem and §4.2 proof. Its second assertion decomposes any unitary representation with the prescribed central character into orthogonal copies of the canonical model; the proof transports an orthonormal basis of a distinguished eigenspace. This is an explicit multiplicity-level predecessor of the unitary normal form, not merely irreducible uniqueness.
- **Gurevich–Hadani, Quantization of symplectic vector spaces over finite fields**, [arXiv:0705.4556](https://arxiv.org/pdf/0705.4556), Theorem 1.2.1, §1.3, Theorem 0.3.1 and §2.2. The ordinary uniqueness theorem and one-dimensional intertwiner spaces produce the projective Weil action; the stronger theorem canonically normalizes a compatible system of intertwiners between oriented-Lagrangian models. That extra canonical construction is not required for v27's elementary swap calculation. Its ambient finite-field, odd-characteristic setup is not itself an all-composite-N cyclic theorem, so it should not be cited as though it alone proves that extension.
- **Prasad–Vemuri, Inductive Algebras for Finite Heisenberg Groups**, [arXiv:0803.2921](https://arxiv.org/pdf/0803.2921), §2 Theorem 2.3. It treats the general finite symplectic abelian quotient, with a U(1) central extension, and states the prescribed-central-character uniqueness. This confirms that the finite-abelian formulation is classical beyond prime-field examples.
- **Ladisch, The character of the Weil representation of a finite abelian group of odd order**, [arXiv:2303.09676](https://arxiv.org/pdf/2303.09676), §3 Proposition 3.3 and §4. The symplectic twisted group algebra is a full matrix algebra over a field of character values, and covariance implementers are constructed through it. This is a direct algebraic comparator in the odd-order setting. The inspected setup uses a subfield of C; it must not be misrepresented as that paper's positive-characteristic theorem.

Conclusion: the block uniqueness, full algebra, Fourier intertwiner, and multiplicity extraction mechanism are classical ingredients and immediate standard consequences. Extending the elementary proof to any root-rich coefficient field is legitimate, but not evidence of a new conceptual theorem. The exact coordinate-spectator packaging and §7 fusion may be useful project-specific statements; this bounded review does not establish literature-wide priority for either. The prior v26 whole-table monomial-equivalence comparison does not, by itself, classify all submatrices of higher-exponent tables. No negative search result is used as a novelty certificate.

## 6. Fresh controls and source evidence

The fresh exact program independently constructs F,S,D and modular constraint matrices. It checks (N,m,p)=(2,2,5),(3,2,7),(4,2,5),(5,2,11),(6,1,13),(9,1,19), using first primitive roots 4,2,2,3,4,4 respectively. Each Weyl span has rank N²; each commutant and swap-solution space has dimension m²; swap identities and the fourth-power formula hold. A nontrivial simultaneous similarity preserves the zero-extraction counterexample despite PE=I.

An independent exhaustive loop over all 254,016 ordered row/column triples in F_3² recovers exactly 9,720 valid embeddings, all 9,720 classified, with 7,776 having nontrivial spectators. Independently generated N=9,25 nilpotent-spectator examples pass all pairings. Higher-exponent counterexamples are checked at N=2,3,4,5,9. The single-cycle resolvent minimal-polynomial degree is independently recovered in dimensions 6,10,12 over F_7,F_11,F_13, including a dimension divisible by the representation root order but without assuming eigenvalue formulas.

The source's “9/9 automated test groups” and its own cold run remain source-reported; no supplied test suite was rerun. Reconstructing the exhaustive count is fresh independent evidence, not a claim that the supplied implementation has been execution-audited. The all-size arguments above establish the mathematical claims; finite tests are controls only.

Integrity: the standalone RESEARCH is byte-identical to the archive's RESEARCH.md; all 15 entries of the supplied internal hash manifest match; archive CRC and embedded v26 CRC checks pass. The v26 sign repair remains the prior audit's correction; embedding its archive does not erase that correction.

## 7. New fusion: cyclic inverse versus multiplicity-bounded minimal polynomial

### 7.1 Theorem: no single-cycle ambient swap for N>4

Under §§1–2, let dim W=Nm. Then

`deg minpoly(J) <= 4m`.

Indeed J is similar to F tensor U, and `J^4` is similar to `N² I_N tensor U^4`. Let p(t) be the degree-m characteristic polynomial of U^4. Cayley–Hamilton gives `p(J^4/N²)=0`; after clearing the nonzero leading scalar this is an annihilating polynomial of degree 4m. This proof is valid in every allowed coefficient field, including characteristic two when N is odd; it does not rely on four distinct Fourier eigenvalues or diagonalizability of U.

Now let C be a weighted Hamiltonian cycle on M=Nm coordinates, with every edge weight nonzero, holonomy h, and h!=1. Then C^M=hI, and for any coordinate vector e, the list e,Ce,...,C^(M-1)e is a basis: these vectors occupy distinct coordinates with nonzero weights. Consequently C is cyclic and its minimal polynomial has degree M.

The inverse G=(I-C)^-1 exists because h!=1. Moreover K[C]=K[G]. One inclusion follows because inverses of an invertible matrix are polynomials in that matrix; the other follows from C=I-G^-1. Since the dimension of the polynomial algebra K[A] is deg minpoly(A),

`deg minpoly(G)=M`.

If G, or any matrix similar to G, were an exact primitive Weyl swap, it would have both degree M=Nm and degree at most4m. Thus N<=4. For N>4 no such ambient swap exists, regardless of the normalizing similarity, its cost, or conditioning.

The same statement holds for any nonzero scalar multiple of G and, more generally, `aI+bG` with b!=0, provided the candidate is invertible so it can be a swap. Indeed its generated polynomial algebra still equals K[G]. When b=0 it is scalar; for N>1 a scalar cannot satisfy the swap relations of the standard noncommuting Weyl pair. Zero edge weights or a singular resolvent are outside this stated cyclic proof. No claim is made that N<=4 is sufficient.

### 7.2 Several cycles, still without arbitrary endpoint maps

If C is a weighted permutation with c disjoint cycles of lengths L_1,...,L_c, all edge weights nonzero and every cycle holonomy different from1, each resolvent block has minimal-polynomial degree L_i. For G=(I-C)^-1, its global minimal polynomial is the least common multiple of those of the blocks, so each L_i is at most its degree. If G is an exact multiplicity-m Weyl swap, each L_i<=4m. Since sum L_i=Nm,

`c >= ceil(N/4)`.

This counts cycles in this literal ambient inverse architecture; it does not establish superlinear application cost. A sum or product of independently routed resolvents need not have the same minimal-polynomial constraint. Independent left/right endpoint maps, arbitrary extraction maps, or equality only of PGE with F are not covered by the cyclicity argument for G itself.

### 7.3 Coordinate-support companion and the exact open contract

In the actual canonical Weyl coordinates, J^-1=F^-1 tensor U^-1. Every row of U^-1 is nonzero and every entry of F^-1 is nonzero, so each row of J^-1 has at least N nonzero entries. A literal single weighted-permutation inverse has G^-1=I-C with at most two entries per row. This already excludes equality for N>=3 in those coordinates. Arbitrary similarity destroys this support comparison; §7.1 supplies a basis-independent alternative for N>4. Neither argument can be transferred through arbitrary independent endpoint maps.

For the inverse/cycle project, the useful next specification is therefore: is the proposed ambient inverse itself a global swap, or only a component of an extracted map? In the former case §§7.1–7.2 are certified rejections. In the latter, supply E,P,C and prove their actual identities and work bounds; do not infer a fast restricted evaluator from a representation-theoretic normal form. For fixed-pair sums of two Weyl resolvents, the separately proved branch bounds remain available in their own literal grammar; the new minimal-polynomial theorem does not silently broaden them.

## 8. Source identities and reproducibility

- Research Library identity: `[private-id]`, backing file `[private-id]`, version 0; 11,911 bytes; SHA-256 `3035a1cdb78d6e454de7d311651faa27d31d8a00b6a39741837237b85e1edf8c`.
- ZIP Library identity: `[private-id]`, backing file `[private-id]`, version 0; 366,130 bytes; SHA-256 `97ff89fdf78ea2f1a0d50c526c16d4e66f3123f4fa6cecff3cf2922f254ed550`.
- Embedded v26 ZIP SHA-256: `8fe968b5b02e58b336d53cdd105938b5f93551d2b19645603f0c7c472ba475d9`.
- Source conversation statement: [v27 message]([private source omitted]).
- Previous coherent convention/support audit: `../intake_audit/PROOFS_AND_DISPOSITIONS.md`, §1.
- Fresh exact evidence: `fresh_controls.py`, `fresh_control_results.json`; inert source/member hashes: `SOURCE_MANIFEST.json`.

No exact sub-N-log-N FFT, unrestricted FFT lower bound, automatically stable extraction, or literature-wide novelty claim is established by this audit.
