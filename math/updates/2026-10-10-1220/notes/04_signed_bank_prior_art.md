# Four signed magnetic resolvent banks: bounded prior-art comparison

Checked 10 October 2026. This is a comparison of primary-source passages, not a worldwide priority certification.

## Conclusion

The algebra underlying a magnetic bank is classical: root-of-unity noncommutative binomial expansion, a finite geometric inverse, character projection, and exponential-sum recurrence/Hankel rank. A particularly close magnetic precedent also contains the same cyclic inverse matrix and scalar denominator as a specialization. The potentially distinctive result is the **exact Fourier synthesis classification in the specified four-bank architecture**, including its small-length exclusions. No equivalent classification was identified in the sources and passages inspected. Historical priority remains unresolved.

The accepted project result is: over every characteristic-zero field containing a primitive odd Nth root, the negative Fourier matrix is a sum of four legal signed magnetic banks if and only if N=3, for odd N≥3. A bank is

R_(ε,δ) = (1/N) Σ_(j=0)^(N−1) w_j (I−αS^ε−βζ^jT^δ)^−1,
ζ=q^(εδ),  1−α^N−β^N≠0.

There is one parameter pair per orientation (ε,δ)∈{±1}² and arbitrary phase weights. The support gate forces all four orientations whenever only four banks are available. This is not a classification of arbitrary resolvent sums, arbitrary generating pairs, products of factors, or all bank counts. The four-bank exclusion gives a lower bound of five at N=5. The separately accepted [construction in this update](05_n5_five_bank_construction.md) attains it, so the minimum is exactly five in characteristic zero. This literature comparison concerns the four-bank classification; it does not establish priority of the new five-bank realization.

## Closest primary sources and exact overlap

### 1. Potter–Schützenberger expansion and the entire triangular inverse numerator

Holtz, Mehrmann and Schneider, *Potter, Wielandt, and Drazin on the matrix equation AB=ωBA, with some new answers to old questions* (published 2004), Theorems 1–2, reproduce and develop the root-of-unity identity and noncommutative binomial expansion. Schlosser, *A noncommutative weight-dependent generalization of the binomial theorem*, Proposition 1, gives the same Gaussian-coefficient convention for yx=qxy. [Author manuscript](https://people.math.wisc.edu/hans/hms_sub.pdf), [Schlosser, Proposition 1](https://arxiv.org/pdf/1106.2112).

The following is a direct specialization, not a separately claimed theorem of those papers. Put A=αS^ε and B=βζ^jT^δ. Then BA=ζAB and (A+B)^N=(α^N+β^N)I, so

(I−A−B)^−1 = (1−α^N−β^N)^−1 Σ_(n=0)^(N−1)(A+B)^n.

Expanding gives exactly the Gaussian coefficients with r+ℓ≤N−1. Thus the single-bank triangular support is already an immediate consequence of classical algebra. The four-orientation coverage/exclusive-point argument is a further model-specific deduction, not a new binomial or inverse identity.

### 2. A magnetic cyclic system with the same denominator

Ouvry, Wagner and Wu, *On the algebraic area of lattice walks and the Hofstadter model* (2016), §2 and §2.2, equations (7)–(8), study a finite cyclic system with diagonal 1−ζ^k y₁−ζ^(−k)y₂ and two directed shift coefficients x₁,x₂. Its determinant is 1−x₁^N−x₂^N−y₁^N−y₂^N+V(x₁x₂,y₁y₂), where V(0,0)=0. [Primary preprint](https://arxiv.org/pdf/1606.03273).

Setting x₂=y₂=0, x₁=α and y₁=βζ^j gives the same ordinary-orientation branch matrix and denominator 1−α^N−β^N; this identification is our explicit specialization. Their object is a lattice-walk generating function/magnetic spectral problem, rather than additive synthesis of the full Fourier matrix by four independently weighted banks. These passages strongly precede the branch algebra but do not provide the classification at issue.

### 3. Finite Weyl expansion and root-of-unity projection

Gross, *Hudson's theorem for finite-dimensional quantum systems* (2006), §II A–D, defines shift/boost Weyl operators for arbitrary odd dimension, their trace orthogonality, and finite character Fourier transforms. Phase conventions differ from the unphased W_(a,b)=S^aT^b used here. [Primary paper, equations (2)–(4), (9), (11)–(14)](https://arxiv.org/pdf/quant-ph/0602001).

For the bank, γ_ℓ=(1/N)Σ_j w_jζ^(jℓ) is simply a finite Fourier coefficient. The elementary character identity (1/N)Σ_jζ^(j(ℓ−m))=1 when ℓ=m modulo N and 0 otherwise supplies the projection. Neither this filtering nor extraction of Weyl coefficients should be presented as new. The particular Fourier chirp coefficient Cq^((a+b)²/4) follows by the project's direct trace/Gauss-sum calculation; this comparison does not attribute that exact phase convention to Gross or treat his Wigner-positivity theorem as a bank-count theorem.

### 4. Exponential sums, recurrences, and Hankel restrictions

Potts and Tasche, *Parameter estimation for exponential sums by approximate Prony method* (2010), §2, relate exponential samples to a homogeneous recurrence and Hankel nullspace. Peter and Plonka, *A generalized Prony method for reconstruction of sparse sums of eigenfunctions of linear operators* (2013), Theorem 2.1, explicitly use an annihilating polynomial and the Hankel factorization V diag(c) diag(Fv) Vᵀ. [Potts–Tasche author text](https://www-user.tu-chemnitz.de/~potts/paper/prony.pdf), [Peter–Plonka, Theorem 2.1](https://num.math.uni-goettingen.de/plonka/pdfs/Operator_Prony_revised2.pdf).

Accordingly, “r exponentials imply Hankel rank at most r” and the associated recurrence are classical. The project-specific bridge is that a whole bank contributes at most two exponentials on b=±1, with constrained root ratio q or q^−1. Combined with the Fourier chirp's full-rank Vandermonde minor, this yields the bank lower bound. The N=9 argument additionally uses the special pairing of recurrence roots; generic Prony rank alone does not exclude that boundary.

## What remains distinctive in the accepted statement

- N=3: a legal full-matrix construction using four orientations, with the support argument proving four minimal.
- Odd N≥11: the signed-bank row isolation plus the classical Hankel/Vandermonde mechanism.
- N=9: exact incompatibility of the forced Fourier recurrence with paired roots x,qx,z,qz.
- N=7: an exact characteristic-zero unit ideal for necessary row equations.
- N=5: coupling the two row-compatible parameter pairs through the actual coefficients at (0,2) and (0,3), followed by exhaustive diagonal/nondiagonal elimination. A row-only non-unit ideal did not settle this case.

These identify the project's mathematical increment relative to the inspected ingredients. They do not establish first publication. The N=5 proof was independently accepted; this literature check did not rerun its certificates. No finite-field failure was used to infer characteristic-zero impossibility.

## Priority and scope still unresolved

1. “Bank” is local terminology. An equivalent theorem could be formulated using quantum-torus rational functions, cyclic inverse families, finite Weyl synthesis, or restricted additive decompositions. Exact-phrase searches are especially weak evidence here.
2. This pass inspected the indicated primary passages, not every cited work, all later citations, theses, or unpublished results. Potter's original 1950 note was bibliographically identified but not obtained in full; its result and proof were checked through the primary Holtz–Mehrmann–Schneider and Schlosser texts. No first-in-history claim about the ingredients is made.
3. A publication-level priority review should match the full permitted parameter/weight class, the one-pair-per-orientation restriction, singularity guards, all odd sizes, and the full Fourier target against any candidate precedent. General Weyl/Clifford constructions or multiplicative factorizations are not automatically equivalent.
4. The classification does not prove an FFT improvement, an evaluation-time lower bound, a minimal count above four for every size, or an all-positive-characteristic N=5/N=7 theorem.

Suggested public wording: “We establish the exact odd-size, characteristic-zero four-bank classification for this signed phase-weighted magnetic-resolvent model. The proof combines classical q-binomial, finite-character and Prony/Hankel ingredients with model-specific support and coefficient obstructions. The N=5 boundary is closed by additional axis constraints. Historical priority for the exact classification remains under review.”
