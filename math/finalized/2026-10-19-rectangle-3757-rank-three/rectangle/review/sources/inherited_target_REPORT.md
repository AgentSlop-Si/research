# Two-prime rank-three separation and the N = 2873 closure

Date: 19 October 2026 UTC. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side proof; independent acceptance pending. No external writes.

## Result

Let p and q be distinct primes, both at least five. Every rectangle of the
complex cyclic Fourier matrix F_(p²q) having rank at most three satisfies

    min(|R|,|C|) ≤ max(6p,3q).

The repeated prime p need not be the larger prime. The bound is not claimed
sharp. Its decisive new step uses three rows in one residue class modulo p²,
a fourth row in a different class modulo p, and a repeated column residue
modulo q to produce a universally nonzero four-by-four minor.

At **N=2873=13²·17**, this gives min(a,b)≤78 and therefore the uniform
actual-rank-three density bound

    3(a+b)/(ab) ≥ 29/442 = 186/2873 + 5/5746.

Consequently the exact disjoint-rectangle endpoint-incidence optimum is
**534378 = 2873·186**. Every optimizer has exactly 2873 rank-one full
subgroup-coset × annihilator-coset tiles with unordered side sizes {17,169}.
A valid, not-claimed-sharp quantitative bound is

    total cost ≥ 534378 + (5/5746) A_(rank≥2).

An additional audit finding simplifies the target-only closure: integer
side lengths and stable rank alone already give the strict rank-three
floor 62/957>186/2873. Section 5.1 proves this exactly. Thus the new
structural theorem is not necessary just to settle N=2873; it provides a
uniform p²q result and the larger displayed quantitative penalty.

Adding just this target to the precisely retained accepted-domain union
settles every length through 3756. Its next residual is **3757=13·17²**,
with D_N=238 and rank three again the remaining gate. The general all-length
problem remains open. No owner status or priority change is asserted.

## 1. Exact model and dependencies

Write F_N[r,c]=ζ_N^(rc), where ζ_N is primitive of order N. A tiling
partitions all N² entries into disjoint nonempty Cartesian products R_t×C_t.
A tile of sizes a,b and actual complex rank r costs exactly r(a+b).
A_(rank≥2) is the total entry area of all tiles having actual rank at least
two. Every row and column subset may be arbitrary.

The accepted rank-two packet supplies the rank-one full-coset equality
classification, the sharp rank-two density

    E₂(N)/N,   E₂(N)=min_(d|N,d<N)(2d+N/d),

and the complex stable-rank inequality ab≤Nr. The mixed-prime packet and
its acceptance supply the prime-power universal-minor lemma and the
short-support zero bound at semiprime order. We restate and prove the precise
facts needed below to make the new argument self-contained relative to the
prime Fourier-minor fact. The accepted p<q theorem for N=pq² is not applied
with its primes reversed. No prime-cube occupancy assertion is extended to
a mixed-prime modulus.

Pinned source files and their SHA-256 hashes are recorded in SOURCES.json.
The prime-cube sharp packet and review provide the retained coverage through
2872. The dominant-prime packet is consulted only to reconstruct the precise
accepted-domain census. No historical checker is imported or executed.

All ranks, spans, and norm arguments are over C. The disjoint/no-sharing
model is unchanged. Root supply and coefficient preparation, storage, and
I/O remain separate; the inherited possible N extra additions for literal
zero-initialized accumulation are unchanged. No conclusion is made about
unrestricted Fourier circuits, arbitrary basis changes, overlapping or
cancelling summands, finite-field rigidity, production performance, or
worldwide novelty.

## 2. Fourier facts used in the proof

### 2.1 Universal prime-power minors

If ℓ is prime, k≤ℓ, and k distinct row indices are pairwise distinct modulo
ℓ, then every restriction to k distinct columns of F_(ℓ^m) is nonsingular.
The transpose statement also holds.

Indeed, the alternant det[x_j^(e_i)] is the ordinary Vandermonde times an
integer polynomial S. Its all-ones value is, up to sign,

    S(1,…,1) = ∏_(i<j)(e_j−e_i) / ∏_(i<j)(j−i).

Every numerator and denominator factor is an ℓ-adic unit, so this integer
is not divisible by ℓ. Reduction in Z[ζ_(ℓ^m)] modulo 1−ζ_(ℓ^m) sends
the roots to one and has residue field F_ℓ. Therefore S evaluated at the
selected roots is nonzero; the Vandermonde is nonzero because the columns
are distinct. At m=1 this gives the prime Fourier nonvanishing-minor fact.

### 2.2 Short-support zeros at order pq

For distinct primes p,q, put u=min(p,q) and v=max(p,q). A nonzero linear
combination of at most k≤u distinct characters of Z_(pq) has at most
(k−1)v zeros. Consequently, if |A|>(k−1)v and T contains k distinct
residues modulo pq, then F_(pq)[A,T] has column rank k.

To verify this, use CRT coordinates (x,z)∈Z_u×Z_v and group a combination
having exactly k′≤k nonzero terms by its v-frequency:

    f(x,z)=Σ_(j∈J) β^(jz) g_j(x),
    g_j(x)=Σ_(i∈I_j) c_(i,j) α^(ix).

Write t=|J| and k_j=|I_j|, so Σ k_j=k′. Prime nonvanishing minors imply
that every nonzero g_j has at most k_j−1 zeros. If z₀ values of x make all
g_j zero, then z₀≤min_j(k_j−1)≤k′−t. Every other x leaves a nonzero sum
of at most t prime-v characters, hence at most t−1 zeros in z. Thus

    Z ≤ vz₀+(u−z₀)(t−1)
      = u(t−1)+(v−t+1)z₀
      ≤ u(t−1)+v(k′−t)
      ≤ v(k′−1) ≤ v(k−1).

The inequalities use t≤k′≤u≤v. A dependence among the k selected columns
on A would violate this zero bound, proving the rank assertion.

## 3. A two-prime four-minor certificate

**Lemma.** Let N=p²q for distinct primes p,q, with q≥3. Suppose four
selected rows have the form

    r_i=r₀+p²w_i,  i=1,2,3,

with distinct w_i modulo q, while a fourth row r_* satisfies
r_*≢r₀ modulo p. Suppose selected columns c₁,c₂,c₃ are distinct modulo
q and c₄ is a distinct index with c₄≡c₁ modulo q. Then the four-by-four
Fourier minor on these rows and columns is nonzero.

**Proof.** Put Δ=c₄−c₁=qk, with k nonzero modulo p², and
λ=ζ_N^(r₀Δ). Replace column four by column four minus λ times column
one. For the first three rows, the resulting entries vanish, since

    ζ_N^((r_i−r₀)Δ)=ζ_N^(p²w_i qk)=1.

The entry at row r_* is

    ζ_N^(r_*c₁) λ [ζ_N^((r_*−r₀)Δ)−1].

It is nonzero: the bracket could vanish only if p² divides
(r_*−r₀)k; but r_*−r₀ is a unit modulo p², and k is nonzero modulo p².

The upper-left three-by-three block has entries

    ζ_N^(r₀c_j) (ζ_N^(p²))^(w_i c_j).

After nonzero column scaling this is a prime-q Fourier minor on three
distinct rows and columns. It is nonsingular. Expansion along the modified
fourth column now gives a product of two nonzero factors. QED.

The lemma is universal in all the displayed indices. It is not a claim
that arbitrary four-by-four Fourier minors are nonsingular, and it is not
inferred from the finite controls.

## 4. Uniform side bound at p²q

**Theorem.** For distinct primes p,q≥5, put B=max(6p,3q). If
rank F_(p²q)[R,C]≤3, then min(a,b)≤B.

**Proof.** Suppose a>B and b>B. We first show that both R and C occupy
at most three residues modulo p.

If C occupied four different residues modulo p, then a>3q puts at least
four rows in one residue class modulo q. Write those rows as y+q u_i,
with u_i distinct modulo p². On four columns distinct modulo p, removing
the nonzero column phases leaves the order-p² Fourier minor with these
row indices u_i and those column indices modulo p². By the transposed
universal prime-power-minor fact, this minor is nonsingular. This
contradicts rank≤3. Transposition, using b>3q, gives the same bound for R.
Let s=|R modulo p| and t=|C modulo p|; then 1≤s,t≤3.

### Case s=1

Write every row as y+p k. Removing column phases reduces the rectangle
to F_(pq) on a distinct row set A, with columns repeated according to their
residue modulo pq. A column fiber modulo pq has at most p members.
Because b>B≥6p>3p, at least four distinct column fibers occur. Also
a>B≥3max(p,q). Section 2.2, with k=4≤min(p,q), makes these four
columns independent, contradicting rank≤3.

### Case s≥2

The s≤3 occurring row residues modulo p have at most sp≤3p refinements
modulo p². Because a>B≥6p, one refinement contains at least three rows.
These are r_i=r₀+p²w_i with distinct lifts w_i modulo q. Since s≥2,
there is another selected row r_* in a different residue class modulo p.

The columns occupy at least three residues modulo q. Otherwise, since
t≤3 modulo p, they occupy at most 3·2 residue pairs modulo p and q.
Each pair specifies one residue modulo pq, with exactly p possible lifts
modulo p²q, giving b≤6p, a contradiction.

Also b>B≥3q>q, so some residue class modulo q contains two distinct
columns c₁,c₄. Choose c₂,c₃ from two other occurring q-residue classes.
These four rows and four columns satisfy Section 3, producing a nonzero
four-by-four minor. This again contradicts rank≤3.

The two cases exhaust all s. Therefore min(a,b)≤B. QED.

The proof in the s≥2 case handles both two and three row residues at once.
It requires no rich-fiber direct-sum subcase or assumption on which of p,q
is larger. All pigeonhole inequalities are strict exactly where needed.

## 5. Density at N=2873

Take p=13, q=17. The theorem gives B=max(78,51)=78. For an actual
rank-three rectangle, transpose so a≤b. Stable rank gives ab≤3N, hence

    3/a+3/b ≥ 3/a+a/N.

For 0<a≤78, this is at least its value at 78. An exact factorization is

    [3/a+a/N]−[3/78+78/N]
      = (78−a)[3/(78a)−1/N] ≥ 0,

since 78a≤78²=6084<3N=8619. The resulting bound is

    3/78+78/2873 = 29/442 = 377/5746.

The rank-one optimum density is D_N/N=186/2873=372/5746, so every
actual rank-three tile has strict density excess at least 5/5746.
Neither this rank-three density floor nor its side cutoff is claimed sharp.

### 5.1 A simpler target-only closure from integer side lengths

The accepted-domain threshold D_N²<12N is sufficient rather than
necessary. At 2873 it misses a strict improvement available from the
integrality of a and b. In fact the exact scalar relaxation

    a,b positive integers, 3≤a≤b≤N, ab≤3N

has minimum density 62/957, attained only at (a,b)=(87,99). This is a
statement about scalar shapes; no Fourier rectangle attaining that shape
or rank is asserted.

Here is a short sum-and-parity proof, independently confirmed during
review. Put s=a+b. If s≤185, AM–GM gives

    density = 3s/(ab) ≥ 12/s ≥ 12/185 > 62/957.

If s≥187, stable rank gives

    density ≥ s/N ≥ 187/2873 > 62/957.

The remaining possibility is s=186. Now d=b−a is even, and

    ab=(186²−d²)/4 ≤ 3N=8619

forces d²≥120. Since d is even, d≥12, so ab≤8613. Thus the density
is at least 558/8613=62/957, with equality exactly when d=12, namely
(a,b)=(87,99). This exhausts all integer side lengths. The difference
from the rank-one baseline is

    62/957 − 186/2873 = 124/2749461 > 0.

Therefore the target optimum and rank-one-only equality can also be
proved without Section 4, albeit with this much smaller common
higher-rank-area penalty. This audit avoids presenting the structural
theorem as indispensable to a target that integrality already closes.
The earlier packets' description of 2873 as the next retained-domain
residual was accurate for their stated sufficient domains; treating it
as a case that necessarily requires new rank-three structure was too
strong. No historical source is changed by this clarification.

## 6. Exact target optimum, equality, and quantitative slack

The divisors of N are 1,13,17,169,221,2873. Their unique unordered
minimizing pair is {17,169}, so D_N=186. The proper-divisor rank-two
values have minimum E₂(N)=203, attained at d=17. Thus rank-two density
is at least 203/N>377/(2N)=29/442.

For actual rank r≥4, stable rank and AM–GM give density at least

    2√(r/N) ≥ 4/√N > 377/(2N)=29/442.

The last comparison follows, after squaring positive quantities, from
64N=183872>377²=142129.

Therefore every tile of rank at least two has density at least
D_N/N+5/5746. Rank-one tiles have density at least D_N/N. Summing
these tilewise bounds over disjoint coverage, whose total area is N²,
gives

    cost ≥ N D_N+(5/5746) A_(rank≥2)
         = 534378+(5/5746) A_(rank≥2).

For attainment, take the subgroup K={169i:0≤i<17}, whose annihilator
is H={17j:0≤j<169}. Partition the rows into all 169 K-cosets and the
columns into all 17 H-cosets. The 2873 Cartesian products are rank one,
each of area N and cost 17+169=186, attaining 534378.

Any higher-rank tile would contribute positive excess, so every optimizer
has only rank-one tiles. Equality in the retained rank-one theorem forces
each tile to be a full mutually annihilating coset product with unordered
side sizes {17,169}. Each tile has area N, so exactly N=2873 tiles occur.
This is a tilewise equality statement; it does not require every tile to
have one common orientation.

## 7. Fresh controls and retained boundary

The new check_repeated_small.py neither imports nor executes any historical
author or review checker. It uses exact characteristic-zero determinant
reductions, rational inequalities, and explicit partition controls. Finite
checks supplement Sections 2–6; they do not prove the universal theorem by
sampling. RESULTS.json and controls.stdout.txt record counts and results.

All controls passed. The checker represents each determinant as a signed
integer sum of root monomials. CRT expresses the cyclic root as a product
of prime-power roots; each factor is reduced in its ordinary cyclotomic
basis. Because these prime-power conductors are pairwise coprime, their
product basis has dimension φ(N) and is a characteristic-zero basis.
Independent ordinary SymPy polynomial division by Φ_N cross-checks
108 determinants, including genuine zeros.

The completed controls include:

- 960 prime-square universal minors with arbitrary higher digits.
- 2400 new-pattern four-minors across ten ordered prime pairs, including
  both orderings of the two primes.
- All 26208 combinations of a nonzero target column separation k modulo
  169 and a unit row displacement modulo 169 in a fixed valid pattern.
- An exact zero counterexample after removing the row-unit hypothesis:
  rows {0,169,338,13}, columns {0,1,2,221}.
- 1200 semiprime short-support threshold examples over five prime pairs.
- 720 full 79-by-79 target rectangles, spanning every pair of row and
  column mod-13 occupancies in {1,2,3,4,5,13}; the proof selects a
  nonzero four-minor in each, and all certificates are retained. These
  are samples, not exhaustive rectangles of those shapes.
- Four independently structural rank-three coset examples, each with a
  nonzero three-minor and 150 separately evaluated zero four-minors.
- All 26612 scalar shapes under the new side cutoff. Their relaxed
  integer minimum is 47/715 at (78,110); no Fourier attainability follows.
  The unrestricted scalar relaxation independently yields Section 5.1.
- Every one of the 8254129 entries in the full 2873-tile target partition,
  with exact rank-one difference identities, once-only coverage, and
  total cost 534378.
- A fresh divisor/prime census through 10000, and unchanged source hashes.

There are 32281 exact determinant evaluations in total, plus the 108
independent polynomial-division cross-checks. The first completed run
took 7.752 seconds; RESULTS.json records the final run time.

The precise retained domain is D_N²<12N, lengths with a prime factor
larger than its cofactor, the isolated accepted length 1331, the accepted
family N=11q² for primes q>11, and the accepted length 2197. Adding just
2873 removes the first residual and leaves 3757 next. At that length,

    3757=13·17²,   D_N=238,
    12N=45084 < D_N²=56644 < 16N=60112.

Rank two is excluded by the retained theorem, and ranks at least four have
strict stable-rank density slack. The rank-three problem at 3757 is not
settled by this report. The new side bound there is max(6·17,3·13)=102,
which is not enough to force the required density; no Fourier counterexample
is inferred from that insufficiency.

## Proposed next-gate wording

Accept after independent review the uniform two-prime side theorem:
for distinct primes p,q≥5, rank-at-most-three rectangles in F_(p²q)
have min(a,b)≤max(6p,3q). Its key explicit four-minor lemma combines a
three-row mod-p² fiber, a row outside its mod-p class, three column
mod-q classes, and one repeated mod-q class. At N=2873=13²·17 this
gives min(a,b)≤78 and rank-three density at least 29/442, closing the
gap with exact optimum 534378, rank-one-only full-coset equality with
2873 tiles of unordered side sizes {17,169}, and valid higher-rank-area
penalty 5/5746. Extending only by this target covers all N≤3756 and
leaves 3757=13·17² as the next rank-three residual. Preserve actual
complex rank, the disjoint/no-sharing model, preparation/storage/I/O
qualifications, the inherited accumulation qualification, priority 42,
and the parent TO RESEARCH status. The all-length problem remains open.
