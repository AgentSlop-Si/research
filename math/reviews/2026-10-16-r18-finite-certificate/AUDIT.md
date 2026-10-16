# R18 finite Fourier certificate audit

Date: 16 October 2026. Scope: the supplied R18 report, complete proof,
certificate implementation, root data, preconditioner, and package integrity.
No source executable was run or imported. No external file or catalogue was
changed, and no claim was closed. This is not a novelty or priority assessment.

## Finding and evidence level

The stated finite existence certificate survives static mathematical review
and a separately authored exact-arithmetic computational cross-check. No
mathematical defect affecting this witness was found. This is stronger than
reading author-produced success logs, but is not a formal proof-assistant
verification or independent human review. The supplied validation suite and
searches were not rerun; their counts and outcomes remain author-reported.

All 44 files listed in the package manifest match their recorded SHA-256
hashes. The separately delivered report and proof are byte-identical to the
copies in the package. A matching manifest establishes internal consistency,
not mathematical validity or trusted authorship.

## Exact theorem and hypotheses

The model is four stages S_k = D_d + D_a H_pi D_b + D_c H_rho D_e, with eight
specified permutation orders. H_pi[i,j] is the sign of the difference of
the positions of i and j in the order. It equals 2G-I for the stated
antiperiodic first-order cyclic inverse; this identity and its linear-work
scan are valid. This is a sum of two diagonally ended Green branches and a
diagonal per stage, followed by a product of four stages.

Of 320 complex coefficient coordinates, 64 are fixed exactly at dyadic
values and 256 are active. The 256 complex equations assert the full matrix
identity S_3 S_2 S_1 S_0 = F16, where F16[i,j] = exp(-2*pi*sqrt(-1)*i*j/16)/4.
The active-coordinate ball is centered at the recorded 320-bit dyadic
numbers, with radius 2^-100 in max_j(|Re z_j|+|Im z_j|). The exact circuit
uses the unique zero in this affine ball, not the saved center.

For the map T(z)=z-B f(z), the proof's bounds on the coefficient neighborhood,
stage derivatives, and product Hessian are valid in the stated norm:
L=6, B0=L+2NL^2, B1=1+4NL, B2=4N, and
H=t B0^(t-1) B2+t(t-1) B0^(t-2) B1^2 = 2782698762672.
The row-sum complex-l1 matrix norm is a valid operator-norm upper bound.
The bounds q=beta+||B|| H r<1 and
alpha+beta*r+||B|| H r^2/2<r prove contraction and self-mapping.
Since beta=||I-B J0||<1, square B is invertible, so the fixed point is a
zero of f. Local uniqueness is restricted to this ball and fixed chart.
The isolated nonsingular zero of this polynomial system has coordinates
algebraic over Q(zeta16). No exact algebraic-field runtime is supplied.

## Separate finite check

The audit program consumes only root_candidate.json and inverse_witness.npy
as data. NumPy loads the latter with allow_pickle=False and verifies a
256-by-256 complex128 array. No code from the packet is imported.

The program builds all stage matrices and their product as exact integer
numerators with denominators powers of 2^320. It independently constructs
the whole selected Jacobian by inserting each sparse stage derivative into
the full product. All 256 columns were also checked against exact one-unit
coefficient perturbations; each individual parameter enters the product
affinely, so these are exact derivative checks rather than approximations.

The Fourier enclosure is constructed directly from sqrt(2),
sqrt(2+sqrt(2))/2, sqrt(2-sqrt(2))/2 and quadrant symmetries, using integer
square-root endpoint bounds at 512 bits. This differs from the supplied
verifier's repeated half-angle/power interval construction. For the beta
test, the exact Jacobian is rounded downward coordinatewise to 256 bits,
and the full induced error bound 2*256*2^-256 is explicitly charged through
||B||. All acceptance comparisons use exact rational numbers.

The fresh check proves the following convenient rational bounds:

- ||f(z0)|| < 4*10^-95
- alpha <= ||B||*||f(z0)|| < 10^-91
- beta < 4*10^-9
- ||B|| < 616
- q < 4*10^-9
- self-map bound < 4*10^-39 < 2^-100

Illustrative values are beta approximately 3.951889320523132e-9,
q approximately 3.951890672149537e-9, and self-map bound approximately
3.117491519843742e-39. The fresh alpha upper bound is approximately
2.292565932007741e-92. It is smaller than the source's interval alpha
because the new computation keeps the center product exact instead of
rounding its intermediate products at 320 bits. The two bounds need not
be numerically equal. The full exact rational outputs are retained in
independent_result.json. Including all derivative perturbation checks,
this run took approximately 17 seconds; the finite check is tractable.

## Scope relative to prior work

According to the supplied source ledger and the audit's prior context,
C09 already records a different exact F16 Green construction with three
layers and eight branches per layer. That old certificate was not rerun
here. R18 is a different chart/model, not the first exact F16 project seed.
Raw branch counts do not establish a fair model or cost improvement.

R17's one-additional-block exclusion concerns a frozen prefix. R18 refits
all stages and changes the correction class, so its finite identity does
not contradict that exclusion. The complete historical R17 proof was not
freshly reviewed in this audit.

The literal R18 executor count is correctly 320 complex multiplications
and 496 additions/subtractions at N=16, compared with the stated normalized
radix-two upper count 48 and 64. Exact online evaluation assumes access to
the isolated algebraic coefficients; the dyadic-center executor is not an
exact F16 implementation. No FFT speedup, growing-size construction,
uniform coefficient generator, stability theorem, or asymptotic exponent
improvement follows. Failed N32 searches are not nonexistence results.

## SHA-256 provenance

- Report: ab2738a6162485c8a9db06a960891c998442dc0bdc30fea0fde6c808eeae8926
- Proof: ca1b14c018d1a96587c2cec5fd9df4184869c6492d29ea96b8a75c60e21ddfaa
- ZIP: 2972a8dab65fe0851fb222da4bc2fb859c553fc1177231721587c8b8d949808e
- root_candidate.json: 8457f187c24ce1d0eb5ec55c5628c4d66e7e443d344848deec6a3ec4dfd30e88
- inverse_witness.npy: 8ba041f5c08f96b7b4604ece84142c54382dd0ab2094e9558d19ad6a55d24ada
- Supplied ball_certificate.py, inspected only: e1e90309dc7bf2d18fea0083dea442a32efc751702af408bbf94819a103f4d3b
- Supplied exact_certificate.json: 3adf0cd1ee7d47989b844cddbdf8369b6bc17d46ba6bf709853a814312255a66
- Original review copy of independent_check.py: 5d8bf1d21e4b4200a282f2d3eb49b69e7dd0dd8198b012c9fbc01f8ea16a2995
- Original review copy of independent_result.json: 241e2975d6abdf601ee353b8019b5e5d9179499644754894b0806021931a0e43

## Portable export note

The private conversation locator was removed from this export. Original
source identities remain bound by SHA-256 hashes. The exported checker
uses data/ relative to its own file, verifies both input hashes before
loading either witness, and compares every exact result field with the
preserved reference result. Only elapsed seconds are excluded from that
comparison. PROVENANCE.json distinguishes original and exported hashes.
The clean proof/report text is retained unchanged under source_text/;
references within it to other package files do not imply their inclusion.
No supplied executable or full supplied archive is included.
