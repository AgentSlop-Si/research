# Independent audit: first-Schur displacement and cost boundary

## Verdict

Accept the exact marked Schur identities, generic leading-minor rank bounds for the supplied charts, singular-tree kernel observation, and the O(N log N) formal coefficient schedule. This is a bounded obstruction to particular displacement representations and a paid baseline evaluator. It establishes neither a Fourier circuit lower bound nor a faster retained inverse.

The inspected constructor seal is `cfcc867e7071e0d4be8eb814f8ba961c1daa1ad9365299351e4ac3d211819055`; its report hash is `6d47c681f8eb246fbc92c9344b4287b6c4c5f05b7a51cce769ba2f5df291558e`. All four entries in its checksum manifest match. Complete report and checker source were read statically; supporting JSON was parsed and preserved. No constructor checker or uploaded program was executed. `constructor_snapshot/` preserves all five files. This review is an additive post-checkpoint20 seal.

Dependencies are the independently accepted pole-free/first-Schur review (manifest `0b6aaaf41f51c6eabcc863bc7d706211ca680449aaf41005e3432d95ec89ec3c`) and next-pivot/variable-block review (manifest `f31d650b774d0c87d7d7000d5a4a1857ece43d0527af0fc812fd91f21619d567`). Their seals are unchanged.

## 1. Exact setup and source/marker preservation

Let N=2^n≥8, m=N/2, ℓ=N/4 over a field with a supplied primitive Nth root ω; characteristic is not two. Set `A0 e_j=e_(2j)`, `A1 e_j=ω^j e_(2j+1)`, `Q=A0+A1`, and

`K0(z)=Σ_(a<n) z^a(A0^a−e0 1_N^T)`.

With `J e_j=e_(2j+1)` and `(Cx)_r=ω^r(x_r−x_(r+m))`, split `H=CK0J` into even/odd interface blocks F,G,R,T. Directly from A0's support, R and T have no positive powers of z, and

`R e_j=ω^(4j+1)e_(2j mod ℓ)`, `T e_j=ω^(4j+3)e_(2j+1 mod ℓ)`.

The latter functional graph has one fixed root, at ℓ−1, of weight ω^−1; other paths feed it. Therefore `det(I−zT)=q=1−zω^−1`. Write W=(I−zT)^−1 and

`S=I−zF−z²GWR`, `β^T=−z1^T−z²1^TWR`,
`M=[[S,−e0],[β^T,1−z]]`.

For a constant input x, put f=CK0x and σ=Σx. Eliminating the odd coordinate yields source `g=f_E+zGWf_O`, `s=σ+z1^TWf_O`. Solve `M[e;t]=[g;s]`, then `o=W(f_O+zRe)` and `y=K0x+zK0J(Ee+Oo)+t e0`. Substitution gives `(I−zQ)y=x` whenever these scalar inverses exist; as formal series their constant terms are invertible.

For arbitrary h, define `a_E=z h^TK0JE`, `a_O=z h^TK0JO`. The correct marker is `p^T=a_E+z a_OWR` and the independent scalar contribution is `c=h^TK0x+a_OWf_O`. Consequently

`h^T(I−zQ)^−1x=c+[p^T,h0]M^−1[g;s]`.

All source, border, eliminated-marker and root-marker terms are required. The present review checks the full input recovery, not only determinant equality or one special marker.

## 2. Displacement algebra and exactly what is paid

For supplied retained operators X_L,X_R and an eliminated-coordinate operator Y, write `Δ_F=X_LF−FX_R`, `Δ_G=X_LG−GY`, `Δ_R=YR−RX_R`, `Δ_T=YT−TY`. The resolvent identity is

`YW−WY=zWΔ_TW`.

Expanding the product without commuting any factors proves

`X_LS−SX_R=X_L−X_R−zΔ_F−z²(Δ_GWR+GWΔ_R+zGWΔ_TWR)`.

For `Xbar_L=diag(X_L,χ)`, `Xbar_R=diag(X_R,χ)`, the full displacement has upper-left block above, last column `−X_Le0+χe0`, last row `χβ^T−β^TX_R`, and zero bottom-right entry. These two border terms each have rank at most one; they do not erase the upper-block residual.

If all five residuals are supplied as explicit outer-product generators, pushing them through W,G,R gives exactly the constructor's concatenated factors. Its O(Nr+N) arithmetic bound is valid for these generator transformations, using the guarded O(N) tree maps and their transposes. Generation or discovery of the input residual factors must be charged separately. The bound does not automatically include applying arbitrary dense X_L,X_R,Y, or forming the full border row `β^TX_R`: those actions require their own supplied efficient representations or paid access. For the specified shift/tree charts, these actions are sparse and O(N). Root tables and scratch require O(N); total working storage may be stated safely as O(N(r+1)), while the r-column generator entries themselves are O(Nr).

For invertible S,

`X_RS^−1−S^−1X_L=−S^−1(X_LS−SX_R)S^−1`.

Thus inverse displacement has equal rank with the operators swapped. Computing these inverse generators still requires solves with S. The identity does not supply those solves for free. The same qualifications hold for M.

## 3. All-size rank certificates

Let E0=e0 1_ℓ^T and `V e_j=ω^(8j+2)e_(4j+1 mod ℓ)`. From actual A0 powers and the C half-difference,

`F(0)=G(0)=−E0`, `[z]F=V−E0`,
`S=I+zE0+z²(−V+E0+E0R)+O(z³)`.

The half-wrap sign is already incorporated by `ω^(N/2)=−1`. Every extra term in the first two nonconstant coefficients is supported on row zero.

### Forward shifts with distinct wrap values

Take `Z_φ e_j=c_j e_(j+1)` for j<ℓ−1 and `Z_φ e_(ℓ−1)=φe0`, with common nonzero internal weights c_j for the left and right shifts. Their wrap values φ,ψ may be arbitrary, including zero. Select rows `4i+2` and columns j for 0≤i,j<ℓ/4. On this minor, degrees zero and one of `Z_φS−SZ_ψ` vanish. At degree two, the only contribution is −Z_φV, with diagonal

`−ω^(8j+2)c_(4j+1)`.

Its factors are nonzero and none uses a wrap edge. Therefore the minor has a nonzero leading determinant coefficient at degree 2(ℓ/4), proving generic/rational-function rank at least `ℓ/4=N/16` for N≥16. This proof also covers the usual distinct-wrap Sylvester displacement; it is not restricted to a same-operator commutator.

### Weighted doubling maps

For `X_b e_j=c_j e_(2j+b)` with all weights nonzero and b∈{0,1}, the supports of X_bV and VX_b occupy different row classes, `2+b` and `4b+1` modulo eight. Root terms occupy rows zero and b. Rows `8i+2+b`, columns j, 0≤i,j<ℓ/8 again isolate the same nonzero diagonal at degree two. Thus generic rank is at least `ℓ/8=N/32` for N≥32.

These lower bounds transfer to guarded inverses and full bordered systems by invertible multiplication and the upper-left submatrix inclusion. They are statements over K(z), or generic scalar parameters. At z=0 the same-tree commutator is zero; a pointwise all-z bound would be false. They exclude only these exact supplied charts in the stated coordinates. Neither long-word trees, arbitrary changed bases, every distinct left/right pair nor arbitrary structured-generator formats are classified.

### Stein and homogeneous information

For invertible A, `rank(A−XAY)≥dim(A)−min(rank X,rank Y)`. A nonzero weighted doubling map has rank ℓ/2, so it forces Stein rank at least ℓ/2. Adding a scalar border raises the tree rank by at most one and the ambient dimension by one, preserving the ℓ/2 bound.

If X,Y are rank-ℓ/2 trees, choose independent columns U spanning ker X and V spanning ker Y^T. The injective family `U Z V^T`, with arbitrary (ℓ/2)×(ℓ/2) Z, lies in the kernel of `A→XA−AY`. Thus at least ℓ²/4 matrix directions are invisible to this displacement. In the same-tree example, `u=e0/c0−e_(ℓ/2)/c_(ℓ/2)`, `v=e_(1−b)` gives a nonzero `uv^T` with zero residual, detectable by a suitable source and marker. A low-rank residual alone is not a uniquely specified matrix.

## 4. Formal recurrence and finite-horizon cost

`M0=[[I,−e0],[0,1]]` has an explicit O(N) inverse. For arbitrary coefficient source b(z), solve through degree n using

`v_j=M0^−1(b_j−Σ_(d=1)^j M_d v_(j−d))`.

To realize the asserted upper bound, process each newly known constant vector v_j with the previously audited constant-input first-Schur jet program, keeping only degrees ≤n−j. That program uses O(N) arithmetic and coefficient routing through this finite horizon. Accumulate its shifted positive-degree output into future residuals, then proceed. There are n+1 vectors, so work is O(N(n+1)); explicitly stored residuals/unknowns may occupy O(N(n+1)) slots. The scalar lower-border tree series has shrinking image support and at most O(ℓ+n) visited states. Shared powers of ω are prepared once in O(N), not independently per edge.

An arbitrary polynomial input cannot be passed once to a constant-input bound. The coefficient schedule correctly pays for its n+1 constant pieces. Likewise arbitrary marker contractions can be performed on each shifted constant-vector jet and added within the same bound, without forming a free dense left polynomial row. Full recovery and extraction of the degree-n vector cost no more than this paid O(N log N) schedule. This reaches the scale of direct n sparse Q applications; a faster coupled inverse/top-coefficient contraction remains open.

The constructor checker and our checker use dense bounded matrix oracles and direct powers. Their runtime is not evidence that they implement this asymptotic schedule. The operation proof depends on the already audited shrinking-state primitives, not on timing either checker. No numerical stability, coefficient-height or bit-complexity guarantee follows from exact field-operation counts.

## 5. Separate guards and retained counterexamples

The q guard concerns only the eliminated tree. In F65537, at z=ω, it vanishes while the full determinant is nonzero: N=8 gives 23312, N=16 gives 47406, N=32 gives 34804. Our second field F257 independently gives 243, 26 and 117. Conversely N=8 over F257 at z=2 has q≠0 and invertible S, while M and the full system are singular. An eliminated-pivot guard cannot replace a retained/full determinant guard.

The earlier variable-block coupled-guard counterexample remains intact: N=4 over F17, ω=13, b=2, z=8 has separately nonsingular branch determinants 3 and 14, but a singular coupled packet determinant, while `det(I−zQ)=7`. This is an inherited accepted control from the prior independent seal, not a new test run in this package. Separate resolvent existence does not imply invertibility of a coupled sum/packet. Formal expansions at z=0 avoid those scalar poles because the relevant constant terms are invertible.

## 6. Fresh controls, provenance and portable replay

The only executed program is auditor-authored `independent_displacement_checks.py`, which has no constructor or uploaded imports. It constructs the global A0,A1,C,J matrices and their actual powers before extracting blocks. Across F65537 and F257, N=8,16,32,64,128, it passes:

- 60 formal leading-minor certificates, with fresh nonzero weights, nilpotent/same/distinct wraps and both doubling maps;
- 320 scalar product/resolvent, full-border and inverse displacement checks, including an arbitrary dense noncommuting intermediary Y and the Stein inequality;
- 31 full input recoveries and arbitrary marker contractions through N=64;
- 20 explicit invisible rank-one perturbations;
- six arbitrary-polynomial-source coefficient recurrences, plus complete constant-input recovery through degree n, checking every coefficient against successive Q applications;
- six q=0/full-invertible controls, and the independently detected q≠0/full-singular case.

All pass. The all-size rank claims rely on the leading-minor proof, not extrapolation from these samples. `INDEPENDENT_RESULTS.json` preserves all bounded cases. `PORTABILITY_CHECK.json` records an actual relocated run with byte-identical output. The manifest hashes the report, checker, results and unmodified constructor snapshot.

## 7. Primary literature scope

[Bostan, Jeannerod, Mouilleron and Schost, Sections 1–2](https://arxiv.org/pdf/1703.03734) explicitly condition a generator's role as a succinct representation on invertibility of the displacement operator, state inverse-rank preservation with swapped operators, and provide algorithms for specified companion-block classes with polynomial-arithmetic costs. [Nevanlinna's author abstract](https://arxiv.org/abs/1904.07549) discusses Sylvester uniqueness under disjoint spectra. These statements were independently checked. Neither paper licenses a fast solve solely from low residual rank for the present singular-tree charts. No historical novelty or published solver improvement is claimed here.
