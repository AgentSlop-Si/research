Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 5e157faa626093f4af5a9e3c1c377a7fee87ea74a2aa8b9b644a6188463984e1

---

# Independent review: exact C8 phase-defect optimum

Review date: 12 October 2026 UTC.

## Verdict

**ACCEPT, in the frozen exact rank-only model.** For the normalized negative-sign Fourier matrix F8 of the cyclic group C8,

    min_{P,Q diagonal unitary} rank_R Im(P F8 Q) = 3,
    rho(F8) = 2.

Here rho minimizes the complex rank of E in F8 = L(B+E)R; B is unrestricted real, and L and R are arbitrary invertible complex monomial matrices, with unrestricted nonzero magnitudes. External operator error is exactly zero.

The candidate's proof is valid without amendment. The reviewer additionally verified equality rigidity by a separate sum-of-squares identity and audited both opposite-real cases without discarding any real-sign choices. Neither a finite phase search nor numerical ranks enter this verdict.

This closes the named C8 exact rank-only case of `PHASE-DEFECT::finite-rank-optimum`. It does not close all finite-group rank minima, any nonzero-error minimax problem, or an unspecified Green/FFT architecture problem. The accepted general rank/gauge theorem and its arbitrary-magnitude stability correction remain unchanged.

## Frozen candidate and provenance

- Archive: `PHASE_DEFECT_C8_Exact_Optimum_CANDIDATE_2026-10-12.zip`
- Bytes: 103,335
- SHA-256: `da65362dbac1c4ba507d743982446f29b0b80a70530ed75f635193c7ece2dc82`
- Candidate manifest SHA-256: `19ae250d16dce80aa4b44a56acce14008f43e0fa0f1d024ec0606009e2e20cab`
- Candidate theorem SHA-256: `daca55e396aa6c913f3d29aa6403e1c574a7677631c471791584ee2acd599357`

The ZIP CRC, all 21 manifest-listed members, the five pinned originals and their snapshots, and all five listed inert members of the predecessor ZIP were independently checked. Original hashes were checked before and after the review. The frozen candidate is included under `frozen/`.

The predecessor source and accepted review were read directly. They leave C8 at 1 <= rho <= 2 and give an imaginary-rank-3, correction-rank-2 upper construction. Their accepted rank/gauge identity includes arbitrary complex monomial magnitudes. The candidate therefore strengthens the lower bound in this exact case rather than merely recomputing a coincident-bound case.

Source priority is bounded to the supplied pins and reconciliation record. This review did not perform a new historical-priority search or independently repeat the author's live Library search. Those limits do not affect the self-contained mathematical result.

## 1. Model and imaginary-rank equivalence

Each complex monomial L admits L = D_L S_L, where D_L is diagonal unitary and S_L is invertible real monomial. Choose the analogous right factorization R = S_R D_R, using column rather than row phases. Then

    L(B+E)R = D_L(S_L B S_R + S_L E S_R)D_R.

The first inner term stays real and the second retains its complex rank. This is equality of the approximating matrices, not an argument that applies inverse ill-conditioned gauges to the target or to an external residual. The reverse inclusion is immediate. Thus positive magnitudes and permutations do not enlarge this unrestricted-real-core feasible class.

For a complex matrix E of rank r, its real imaginary part has rank at most 2r: rank_R Im E = rank_C Im E <= rank_C E + rank_C conjugate(E). Conversely, each pair of real rank-one terms a1 b1^T + a2 b2^T is the imaginary part of (a1+i a2)(b2+i b1)^T; an unpaired term uses i a b^T. This yields exactly ceil(m/2) as the minimum correction rank for a prescribed real imaginary matrix of rank m. Realness of the residual supplies the unrestricted B.

Consequently the candidate's variational identity is exact in both directions. A realized least integer rank exists, so no assumption about continuity of rank or attainment of an infimum is needed.

Fresh controls cover all m=0,...,8, including every odd case. A separate exact reconstruction uses nontrivial row/column permutations and positive magnitudes from 10^-60 through 10^60. These are controls of the algebraic absorption, not the basis of its general proof. No constrained real-core model is implicitly substituted.

## 2. Energy bound and its equality case

Let V=P F8 Q, Y=Im V, a_j=p_j^2 and b_k=q_k^2. Both V and its entrywise conjugate are unitary, hence ||Y||_2 <= 1. If rank Y <= 2, then ||Y||_F^2 <= 2.

For H[j,k]=(-i)^(jk), expansion of each squared imaginary part gives

    ||Y||_F^2 = 4 - Re(a^T H b)/16.

Let J exchange each index k with k+4 and Pi=(I+J)/2. Direct root-of-unity algebra gives H*H=HH*=16 Pi and Pi H=H. With ||a||=||b||=sqrt(8), this bounds Re(a^T H b) by 32 and therefore gives ||Y||_F^2 >= 2.

There is no ambiguity from the bilinear transpose: a^T H b is the Hermitian inner product of conjugate(a) with H b. Equality forces H b=4 conjugate(a) and Pi b=b, exactly as the candidate states.

An independently derived identity makes the equality implications explicit:

    32 - Re(a^T H b)
      = 2 ||conjugate(a)-H b/4||^2 + 2 ||(I-Pi)b||^2.

This holds when both squared norms are eight. More generally, replace 32 by 2(||a||^2+||b||^2), an identity checked as a polynomial in 32 independent real coordinates. Equivalently, under the phase assumptions,

    ||Y||_F^2 = 2 + [||conjugate(a)-H b/4||^2
                         + ||(I-Pi)b||^2]/8.

Thus low rank forces both squared-norm terms to vanish. Since H has identical rows j and j+4, both a and b are four-periodic. Nonzero phases with equal squares differ only by real signs. Independent real row/column signs make p and q themselves four-periodic without changing imaginary rank.

This does not assert that equality in energy is sufficient for rank two. A fresh exact control uses p=(1,e^(i pi/4),1,e^(-i pi/4)) repeated twice and q=(1,1,1,i) repeated twice; it has squared imaginary Frobenius norm 2 and imaginary rank 3. This separation was checked exactly.

## 3. Four-block reduction and exhaustive branch coverage

After the periodicity reduction, real Hadamard transforms of paired indices (r,r+4), followed by real permutations, give four diagonal 2 by 2 blocks:

    C_cd[u,v] = p_(c+2u) q_(d+2v)
               exp(-pi i (c+2u)(d+2v)/4) / sqrt(2).

The reviewer independently constructed the complete left and right real orthogonal transforms directly in block order and verified every entry of the 8 by 8 identity with symbolic p0,...,p3 and q0,...,q3. Therefore imaginary ranks add exactly across these four blocks.

All block entries are nonzero. If C_cd is real, its first-column row ratio (-i)^d p_(c+2)/p_c and first-row column ratio (-i)^c q_(d+2)/q_d are real. For fixed c, changing d multiplies the first ratio by -i, so both cannot be real; the analogous statement holds for fixed d. No two real blocks can be adjacent in the 2 by 2 block array.

Rank sum at most two leaves at least two real blocks. Once adjacency is excluded, there are exactly two possible rank patterns, in the order (C00,C01,C10,C11):

    (0,1,1,0) and (1,0,0,1).

This covers rank zero, rank one, putative rank two in a single block, and three- or four-real-block possibilities. As a bookkeeping check, all 15 rank allocations with entries in {0,1,2} and sum at most two reduce to the same two patterns. This finite rank bookkeeping is not phase enumeration.

## 4. All signs in the two surviving cases

The candidate's simultaneous real-sign normalizations are valid: the two opposite real blocks use disjoint base row and column parities. To avoid relying on that convenience, this review retained six independent signs r0,r1,c0,c1,h0,h1 in each case. Let zeta=exp(-pi i/4), with A,G arbitrary unit complex phases.

Case A, real C00 and C11, is parameterized without loss by

    p=(A,G,r0 A,i r1 G),
    q=(h0/A,h1/(zeta G),c0 h0/A,i c1 h1/(zeta G)).

The nonreal blocks have scalar prefactors t=A h1/(zeta G), u=G h0/A. Their imaginary determinants are respectively r0 c1 Re(t^2)/2 and r1 c0 Re(u^2)/2. In every sign case,

    (tu)^2 = i.

Case B, real C01 and C10, is parameterized without loss by

    p=(A,G,i r0 A,r1 G),
    q=(h1/G,h0/A,i c0 h1/G,c1 h0/A).

The other block prefactors are t=A h1/G, u=zeta G h0/A. Their imaginary determinants are -r0 c0 Re(t^2)/2 and -r1 c1 Re(u^2)/2; in every case,

    (tu)^2 = -i.

The real-block equations, all four general block formulas, determinant factors, and scalar product identities were checked symbolically. All 64 sign assignments in each case also pass, for 128 sign cases total. A and G remain symbolic; there is no discretization of their continuous phases.

Since the two nonreal blocks must each have imaginary rank one, both determinants vanish. Unit modulus then forces t^4=u^4=-1. Thus the product t^4 u^4 is 1, while squaring either displayed product constraint gives -1. This is impossible in characteristic zero.

For the supplied polynomial certificate, setting z=t^2 and w=u^2 gives z^2+1=w^2+1=0 and zw=sigma i, sigma=+1 or -1. The exact identity

    2=(zw-sigma i)(zw+sigma i)-w^2(z^2+1)+(w^2+1)

is correct for both signs. The candidate's polynomial passage from |t|=1 and Re(t^2)=0 to t^4+1=0 is also correct. These algebraic identities apply to all complex phases, including transcendental ones; the upper witness's coefficient field is not imposed on the lower proof.

It follows that every rephasing has imaginary rank at least three.

## 5. Matching upper construction

At identity gauges, columns 0 and 4 of Y=Im F8 vanish and opposite columns negate. Columns 1,2,3 therefore give a real rank decomposition with three terms. The corresponding (1,2,3)-row and column minor is exactly 1/8, so rank Y=3. Pairing the first two terms and leaving the third as i a3 b3^T gives precisely the candidate's complex E, with Im E=Y and rank E<=2. The imaginary-rank inequality forces rank E>=2, so rank E=2. F8-E is real.

The reviewer reconstructed F8 from an explicit exact eighth-root table, without exponential or floating-point evaluation, and checked unitarity, the minor, both ranks, realness, and reconstruction. Every serialized F, B, and E entry matches the candidate's inert WITNESS.json. The construction is exactly in the allowed model and uses identity gauges.

The lower and upper bounds match. This proves both stated optima.

## 6. Evidence and limitations

`independent_checker.py` was freshly written for this review. It imports only standard-library modules and installed SymPy. Neither the candidate checker nor any uploaded/predecessor program was imported or executed. All matrix and polynomial calculations use characteristic-zero exact arithmetic. The script supports, but does not replace, the analytic proof.

Four deliberate errors are rejected: replacing the doubled Fourier energy table by the undoubled one, dropping the C11 phase factor, reversing the last sign of the inconsistency certificate, and omitting the last term of the rank-two witness. Results are recorded in INDEPENDENT_RESULTS.json.

No external files, table cells, repository entries, or Library items were written. Original source files remain unchanged. No historical-novelty, uniform construction-cost, arithmetic-lower-bound, nonzero-error optimum, or Green-realification claim is accepted here.

## Scope and remaining work

Accepted delta: "Exact C8 rank-only optimum independently accepted: minimum phase-rephased imaginary rank 3 and minimum complex correction rank 2, for unrestricted real B and arbitrary invertible complex monomial outer gauges. Universal continuous-phase lower proof and exact rank-two witness match."

The named finite-case completion test is satisfied. Preserve general finite-group optima, positive-error optimization, and any specific Green application as separate open work. Do not mark the broad FFT or Green construction research stream solved, and do not restore the predecessor's incorrect arbitrary-magnitude conditioning caveat.
