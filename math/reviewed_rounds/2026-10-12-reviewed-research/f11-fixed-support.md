Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 7449a592a69b16b9dde95d623040f4a9a7bfe33cbdda6a5140d282b8b0845170

---

# Independent review: exact Fourier exclusion for the pinned F11 support

Review date: 2026-10-11 UTC.

## Verdict

ACCEPT_SCOPED. The recovered uploaded v40 theorem is correct: the exact pinned
99-edge, three-layer support cannot realize the 11-point Fourier matrix over
the complex numbers, even with arbitrary edge weights, including zero. The
same obstruction excludes every independently row/column-permuted and nonzero
row/column-scaled Fourier matrix, including normalized and inverse-sign forms.
This is a verification of the later uploaded result, not a new discovery or
literature-priority determination.

The full 121-entry Fourier target ideal is the unit ideal. No localization,
nonzero-edge assumption, or chart guard is needed. This closes Fourier
synthesis on this particular support, including every proposed E25/E41
chart continuation as a route to full Fourier factors.

Important limitation: the accepted 50-residual/19-guard chart system was only
certified as necessary for full Fourier synthesis. This review does not prove
that its abstract relaxed chart domains, or their E25/E41 necessary-condition
loci, are empty. It proves that no point in them can extend to a full Fourier
factorization on this support. No equivalence with the full target ideal is
assumed. Retiring that queue as a Fourier-synthesis route is justified;
labeling each relaxed chart infeasible is not.

## Exact source and architecture binding

The uploaded archive is fft_quintic_transfer_gate_v40.zip, Library identity
[private reference omitted], 11,515,862 bytes, SHA-256
4d2056c04d2e7ab2c3969721c62ea1dcff5047cf51ac66ac089d92d0ffb50680.
Its full CRC check and all 27 manifest entries pass. The preserved nested
v39 archive also passes CRC. Its SHA-256 is
1425fc7321cda9bd47ce17384e2c5e3c4c762b5077bc2014dabd708133b2f5b5,
matching the accepted v39 receipt.

The independently retained original-v39 topology and the v40 topology are
byte-identical, SHA-256
4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b.
The accepted v39 review binds these exact ordered bytes to the original
research_cycle_1734 topology. Independently, the accepted six-chart atlas
pins the same hash. The historical binding is inherited from these pinned
accepted artifacts; the underlying original 1734 archive is not newly
retrieved or re-reviewed here. No graph isomorphism or relabeling substitutes
for byte identity.

There are three lists of 33 distinct (destination, source) edges. Every
vertex has indegree/outdegree three in each consecutive-layer relation.
The convention is H=CBA, with first-layer weights w0 through w32, middle
weights w33 through w65, and last weights w66 through w98. Indices in the
polynomial below are zero-based. No different topology, Q27 unit-gain model,
or Phase56 model is used.

The source report has SHA-256
71362f708829be944df83ac38905a0e1f6f53994d747c7e6dde0c99b9a4b0506;
the source quintic certificate has SHA-256
476ffeeb840875aa9f4bae9d93cf4a38956c25203d6372c0333a5d7a7ab3946f.
The source archive and source programs are inert. No uploaded, author, or
historical research program was imported or executed.

## Independent integer identity reconstruction

Set

    a = h[1,1]h[2,4] - h[1,4]h[2,1]
    b = h[4,1]h[8,7] - h[4,7]h[8,1]
    c = h[4,1]h[8,4] - h[4,4]h[8,1]
    P = h[4,1]h[8,9](h[1,1]h[0,4]h[2,7] - h[0,7]a)
        + h[0,9](ab - h[1,1]h[2,7]c).

The fresh reviewer checker directly joins the original edge lists to
reconstruct all 297 paths. Across the 121 transfer entries their count
histogram is 22 entries with one path, 42 with two, 39 with three, 16 with
four, and two with five.

The nine distinct signed transfer monomials in P contribute respectively
8, 24, 12, 32, 16, 12, 8, 16, and 8 path families: 136 in all. Sorting the
15 edge IDs in each contribution yields exactly 52 edge monomials. Every
integer coefficient is zero. The complete occurrence-level cancellation
ledger and all 297 paths are retained, so this is an identity in
Z[w0,...,w98], valid after specialization to every commutative ring.

A separate direct symbolic matrix multiplication with 99 distinct SymPy
symbols checks all 121 entries against the reconstructed paths, and both
the factored and expanded P(CBA) expressions simplify to zero. The proof is
not numerical evaluation, sampled rank, or an assumption that a supplied
numeric transfer matrix has the correct architecture.

Semantic controls bypass the topology hash gate: all nine single-term sign
flips break the identity; transposing the original all-one transfer gives
P=66; and adding the otherwise absent edge A[0,4]=1 to all-one weights gives
P=4. The one-edge control neither realizes Fourier nor settles any enlarged
support.

## Independent Fourier arithmetic

For F[i,j]=zeta^(ij), direct integer phase accumulation gives

    P(F(z)) = z^91-z^85+z^82+z^69-z^66-z^51-z^45+z^42+z^39.

Modulo Phi11(z)=1+z+...+z^10 the remainder is

    f(z) = z^9-z^8-z^7+z^6+z^5+2z^3-z-1.

The canonical coefficient vector is
[-1,-1,0,2,0,1,1,-1,-1,1]. Its value at z=1 is 1. Thus reduction
Z[zeta] -> F_11 sending zeta to 1 takes P(F) to 1, which already proves
nonvanishing. This reduction is applied to the target after the integer
identity is established; no integrality of hypothetical edge weights is
assumed.

The algebraic norm is independently checked two ways: an integer Bareiss
determinant of the 10-by-10 multiplication-by-f matrix in the basis
1,zeta,...,zeta^9, and a SymPy resultant with Phi11. Both give 101729.
The complete integer multiplication matrix is preserved. An exact integer
Bezout check also verifies f*u_num+Phi11*v_num=101729, with

    u_num = -5919-2094z+10593z^2-8124z^3-1030z^4+1037z^5
            +16510z^6-5812z^7+25628z^8-8920z^9.

Consequently P(CBA)=0 and P(F)!=0 contradict CBA=F over C, or any
characteristic-zero field containing a primitive 11th root.

## Endpoint permutations, gauges, and full-target ideal

Every term of P has row multiset [0,1,2,4,8] and column multiset
[1,1,4,7,9]. The checker verifies these margins term by term. Nonzero endpoint
gauges therefore multiply P by the common nonzero factor

    d0*d1*d2*d4*d8 * e1^2*e4*e7*e9.

Every independent permutation of the Fourier rows and columns still has
all entries equal to 1 under the cyclotomic reduction, and P(J)=1.
Thus every such permuted Fourier matrix has nonzero P before any gauge;
nonzero complex gauges cannot change this. No permutation enumeration or
assumption on the gauges' coefficient field is needed.

The reviewer also independently constructs a full-target unit certificate.
For each signed product of five entries, telescope its difference from the
Fourier product using an H prefix and Fourier suffix. Group the resulting
45 summands by their 15 distinct residual coordinates R_ij=H_ij-F_ij.
After path substitution these grouped multipliers contain 72 terms. Fresh
integer cyclic polynomial arithmetic, separate from SymPy, verifies

    sum_ij Q_ij(w,zeta) R_ij(w,zeta) = -f(zeta),
    (-u_num(zeta)/101729) * sum_ij Q_ij R_ij = 1.

The full multiplier data and the exact inversion certificate are included.
Only the nonzero rational scalar 101729 is divided by. There is no weight,
pivot, or guard division. Hence the full target ideal in Q(zeta)[w] is (1),
and equivalently the ideal of Phi11 and all full target residuals in
Q[z,w] is (1). Saturating or localizing this already-unit ideal by any
original guard keeps it unit. This does not assert an ideal membership
certificate for the separate reduced 50-equation system.

## Earlier chart accounting and scope

The accepted six-chart atlas certificate has SHA-256
3fd7382a6207024853f7cf466b05a1f7aba9d9ef7e1b737353711a0394d49024.
Its accepted review and receipt match their pinned report hash. Fresh
structural checks confirm that all six branches retain exactly the same
50 original residual references and 19 original guard references, with
three inputs per branch. Their complete reference mappings are retained
in ATLAS_BINDING.json. H=0/H!=0 is crossed with d=0 (including M=0),
d!=0 and M=0, or d!=0 and M!=0.

This review does not rerun the historical chart algebra or fetch the
original 81-polynomial source pool. Those accepted historical reductions
are a provenance boundary, not an unreported new computation. Neither
their correctness nor their sufficiency is required for the new full-target
obstruction. Every full Fourier realization would violate P, regardless
of its chart label, its guards, or whether a chart omitted some solution.
The later E25/E41, decic, and exceptional residual calculations remain
historical auxiliary results; their relaxed-domain feasibility is not
newly classified here.

Do not generalize the conclusion to other supports, all graphs with 99
edges, arbitrary depth-three networks, all Fourier lengths, or an
asymptotic FFT lower bound or speedup. There is no exact Fourier executor
on this support. Its hypothetical 99 multiplications and 66 additions are
only the cost of evaluating a supplied generic supported map.

The source's rank-59 assertion in one 60-monomial quintic bidegree is not
needed and is not independently replayed or accepted by this review.
Historical v39 degree-at-most-four injectivity is not newly re-proved.
No literature search or novelty certification is performed.

## Reproduction

Run only the fresh reviewer file:

    python review_fresh.py

Python 3.12 and SymPy are used. The packet includes the source archive as
inert bytes and the exact topology, source statement, source certificate,
atlas, and accepted historical binding reports needed for this replay.
No external writes are performed. The final receipt pins the fresh checker,
report, source inputs, and all deterministic generated evidence.

## Frozen candidate audit and cold replay

The author's final candidate ZIP is SHA-256
99e06db43478b67d06d7a565b98926f44466ebc509779f8dd8b96c17dde03961,
3,064,652 bytes. Its CRC and all 184 manifest entries pass independently.
The frozen proof hash is
5838a8953e828a83d1c66ba177db7e6ed4033d0b369fad7e55c86b9f7a078216;
the scope hash is
81e70e4de7fe3ce8f023351866655509175153b28ffd519bca9ff58a89546514.
The review reconstructs all 45 stored ideal summands, verifies the supplied
raw-target Bezout coefficients against the raw Fourier polynomial, and
checks their inverse against the independently obtained inverse. The frozen
scope explicitly excludes both relaxed-chart emptiness and a reduced-ideal
unit certificate. No correction to the frozen core theorem is required.

A separate cold directory, containing only these packaged inputs and the
fresh reviewer checker, regenerates every evidence JSON byte-identically.
This cold replay executes only the fresh reviewer program.
