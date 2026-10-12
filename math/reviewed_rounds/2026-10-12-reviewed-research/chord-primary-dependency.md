Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 1c33edd3fa02554fa1019e68ba73ff54e24e60a85e6eb570c514e8dc3f0c19d3

---

# M-CHORD primary-incidence dependency: independent acceptance

Date: 2026-10-11 UTC. Gate: M-CHORD::primary-incidence-dependency.

## Verdict

**ACCEPT, bounded citation/dependency closure only.** The Heineken primary source and the explicit premise mapping discharge the previously unpinned geometric dependency. Applying the citation addendum to the manuscript remains an editorial step. Neither the manuscript nor any external research table was edited in this review. No bound, novelty classification, worldwide-priority claim, or discovery count is promoted.

Reviewed candidate: `M_CHORD_Primary_Incidence_Dependency_CANDIDATE_2026-10-11.zip`, SHA256 `f04baa73485dbb951666e46507d656dd93bed2b8b23a4fbb6a0d6b0f403dd6f9`. Its CRC, manifest hash, all 17 manifest members, and all eight declared original-upload member hashes pass. The original upload, including its embedded program, and the candidate program remained inert. Only the newly written `independent_checks.py` was executed.

## Primary source and access qualification

Hermann Heineken, “Regelmässige Vielecke und ihre Diagonalen,” L'Enseignement Mathématique (2) 8 (1962), 275–278, [DOI 10.5169/seals-37967](https://doi.org/10.5169/seals-37967). Exact locator: unnumbered concluding theorem, p. 278; proof Eqs. (1)–(9), pp. 276–278; exclusions, p. 275. [ETH primary body](https://www.e-periodica.ch/cntmng?bot=1&pid=ens-001%3A1962%3A8%3A%3A93).

The reviewer independently retrieved the complete primary PDF text extraction. Its 161 body lines match the author's observation exactly. This is **text-extraction access**, not possession of PDF bytes or visual facsimile inspection. No PDF-byte digest is asserted. The full extracted text is excluded from this package.

The source permits unrestricted real line parameters (p. 276), excludes original vertices and intersections at infinity (p. 275), and uses six distinct endpoints (p. 277). The theorem is phrased with diagonals; applicability to side-lines is a proof-level extension, because nonadjacency is never used. Exterior intersections are directly included by the unrestricted parameters. The proof begins with odd n>6; n=5 follows separately because three distinct lines at a nonvertex point require six endpoints. Rigby's unread body is no longer indispensable. Keep Rigby and Sidorenko only as supplementary historical references.

## Independent algebraic closure of the line premise

Here is an independent reconstruction of the needed implication and its division guards. It resolves equation-extraction ambiguity without claiming a visual reading of the source.

Let the three endpoint pairs, after rotation, be (1,R), (S,T), (U,V), where all six entries are distinct nth roots and n is odd. A line through two unit-circle points x,y has equation

    w + conjugate(w) x y = x+y.

Indeed for w=x+lambda(y-x), the difference between its two sides is (y-x)(lambda-conjugate(lambda)). Thus this describes the complete real line, with no restriction to the segment.

Three concurrent lines make the determinant of rows (1,R,1+R), (1,ST,S+T), (1,UV,U+V) vanish. Direct expansion equals -RF, where

    F=(1-S)(1-T)(1-UV/R) - (1-U)(1-V)(1-ST/R).

All variables lie in Q(zeta_n). Since n is odd, zeta_n -> zeta_n^2 is an automorphism. It sends F=0 to its simultaneous square substitution F[2]=0. Define

    G=(1+S)(1+T)(1+UV/R) - (1+U)(1+V)(1+ST/R),
    H=S+T+UV/R-U-V-ST/R,
    K=(R-U)(R-V)-(R-S)(R-T),
    J=(R+U)(R+V)-(R+S)(R+T).

The exact identities checked independently are

    F[2]-(1+S)(1+T)(1+UV/R)F = (1-U)(1-V)(1-ST/R)G,
    G-F=2H,  RH=K,
    K[2]-(R+U)(R+V)K = (R-S)(R-T)J,
    K+J=2(UV-ST).

The first coefficient is nonzero: U,V differ from 1, and ST=R would make the first two distinct lines parallel, impossible for finite concurrence. Therefore G=H=K=0. The automorphism gives K[2]=0, and R differs from S,T, so J=0. Characteristic zero permits division by 2, giving UV=ST. The last two lines are then parallel. They cannot coincide because a real line meets the circle in at most two distinct points, contradicting six distinct endpoints. Finite nonvertex three-line concurrence is impossible. Nothing in this derivation distinguishes adjacent from nonadjacent endpoints.

For n=5, a putative three-line nonvertex concurrence would likewise require pairwise disjoint endpoint pairs: two distinct lines sharing a polygon vertex can intersect only at that vertex. Six distinct endpoints do not exist. This supplies exactly the small case the matrix application needs.

## Matrix premise mapping and exceptional branches

The accepted source uses complex unnormalized Fourier matrices, odd n>=5, nonsingular monomial endpoints, Hamiltonian routing and the ordered frequency triple r,r+d,r+2d with gcd(d,n)=1. Its permissible row/column gauges give

    h(t)=(1-at, t(1-bt))^T,  t in mu_n.

The unit step makes every parameter distinct. Column relabeling conjugates the right cycle; nonzero column scales change effective edge weights without changing zero supports or Hamiltonicity.

The checked determinant is

    det(h(t),h(u))=(u-t)[1-b(t+u)+abtu].

If b=0, every distinct pair is independent. Otherwise a dependent pair satisfies t+u=z+a tu with finite z=1/b. Two distinct unordered pairs cannot have equal products: their sums would then also agree, yielding the same quadratic and hence the same pair. Conjugation gives t+u=conjugate(a)+conjugate(z)tu. Subtracting equations at two different products forces a=conjugate(z). Consequently all dependent pairs are complete circle-secants through z.

The coefficient matrix [[1,-a,0],[0,1,-b]] has a 2x2 minor equal to one. Every three-column parameter Vandermonde is invertible. Thus three selected nonzero columns cannot be proportional, so dependent nonzero pairs are disjoint. Their lines are distinct. Their common z cannot be an original vertex: a line through a pair not containing z would contain three circle points. The primary premise therefore permits at most two such pairs.

Under P_beta[k,beta(k)]=1, right multiplication yields output column beta(k) equal to H[:,beta(k)]-weight[k] H[:,k]. With both columns nonzero, cancellation requires one of the dependent pairs. A Hamiltonian cycle of length >=3 cannot use both orientations of a pair, because doing so would create a two-cycle. At most two output columns can therefore vanish jointly.

If h(t0)=0, then a=b=1/t0, and h(t)=(1-t/t0)(1,t)^T. There is exactly one zero selected column; every other pair is independent. A zero output can occur only at the zero target, and then requires its incoming effective weight to be zero. This gives at most one cancellation. No zero-entry division has been used.

The resulting adjacent-row support bound remains n-2. The existing local sharpness construction uses the disjoint pairs (1,omega^2), (omega,omega^3). Their distinct products make the lines nonparallel; an odd polygon has no antipodal pair, so their intersection is nonzero. Two dependent pairs exclude a zero h-column. Both directed cancellations fit into one Hamiltonian cycle, with all other edge weights zero and inverse guards one. This is local sharpness only.

## Other source dependency and unchanged deductions

Independently inspected [Tao, arXiv:math/0308286v6](https://arxiv.org/pdf/math/0308286), Lemma 1.3, p. 3, proof pp. 3–4. Its complex prime-Fourier minor statement applies at minor size three with distinct frequency and column labels. Fourier sign or nonzero normalization does not affect determinant nonvanishing. The rank-two coefficient map then forbids three proportional nonzero columns; if a zero column occurs, all remaining columns are pairwise independent. This gives the weak local support bound ceil(p/2), as previously accepted.

No derived constant changes:

- All strong profiles: nnz(T)>=ceil(n(n-2)/2).
- Prime p>=5 with g strong profiles: nnz(T)>=ceil([g(p-2)+(p-g)ceil(p/2)]/2).
- Exact scalar-polynomial bridge X P_L(K)Y, with X=A+B, K=CB, Y=C+D and row degrees <=3,4,3: nnz<=9n sum_(r=0)^L 4^r. Combined with the strong density bound, 4^(L+1)>=1+(n-2)/6.

These follow respectively from summing adjacent support inequalities, the same sum with strong and weak terms, and elementary support reachability. Green-factor inverses require their separate nonzero denominator guards; the local support argument does not. The degree obstruction is restricted to the stated exact scalar-polynomial grammar. There is no arbitrary arithmetic-work lower bound, unrestricted fast-solve obstruction, or full two-layer impossibility result.

## Independent exact countercontrol

The fresh checker reconstructs the complete 9x9 product A F_9 B over F19, with root 4, natural left cycle, left weights [1,12,0,0,0,0,0,0,0], right cycle [3,8,5,4,1,6,7,0,2] and weights [0,14,15,0,0,0,10,0,0]. Root order is nine and both cycles are Hamiltonian. The dependent nonzero pairs are (1,8), (2,5), (6,7). Selected output rows are

    [0,16,4,13,11,0,9,0,0]
    [8, 2,3, 8, 6,0,3,0,0].

Joint zeros are exactly [5,7,8], and the support union is 6<7. Full modular elimination gives det(A)=det(B)=1, agreeing with both cycle inverse guards. The finite-field exclusion remains essential. The fresh symbolic checks and 24 five-vertex Hamiltonian controls are consistency evidence, not finite sampling substituted for the all-odd proof.

## Writer instructions and stopping scope

Use `ACCEPTED_ROW_PROPOSALS.json` only as a bounded append overlay to existing M-CHORD rows. Its row positions come from a historical baseline. Freshly read each stable ID and old cell value before writing; relocate by stable ID if needed, preserve historical text, and perform verified readback afterward. A citation/dependency gate can be marked independently accepted; novelty, discovery count and numerical bounds must remain unchanged. Never describe Rigby's unread body, an unavailable PDF, or a visual facsimile as inspected.

Publication still needs the addendum applied to manuscript Section 0, Theorem A Step 5, and the references. The complete-line scope should retain the proof-level side-line extension and the n=5 endpoint argument. The underlying manuscript has not been rewritten by this review. Broader priority, finite-field, nonaffine-composite and circuit questions remain outside the closed gate.
