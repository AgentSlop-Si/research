# N=3757: strict rank-three rectangle density

Date: 19 October 2026 UTC. Owner M-RECTANGLE-TILING; priority 42 unchanged.
Status: author-side theorem and exact controls; independent review required.

## Result and precise scope

For arbitrary nonempty subsets R,C of Z/3757Z, with the original complex
Fourier matrix F[r,c]=zeta^(rc), rank(F[R,C])<=3 implies

    min(|R|,|C|)<=51 OR max(|R|,|C|)<=78.                 (1)

Consequently every actual rank-three rectangle has

    3(a+b)/(ab) >= 16/221 = 272/3757 > 238/3757.

This closes the specified N=3757 rank-three lemma, subject to independent
acceptance. The exact original disjoint-rectangle cost optimum at this
length is 894166=3757*238. Every optimizer consists of exactly 3757 full
rank-one subgroup-coset times annihilator-coset tiles with unordered side
sizes {17,221}. Tile orientations need not agree. One valid nonsharp bound is

    total cost >= 894166 + (7/3757) A_(rank>=2).

There is no rank-three equality at the target density. This report neither
changes the owner status or priority nor claims a general all-length result,
a new owner, or worldwide novelty. No next target is selected or counted.
The accepted N=2873 computation and tiling are not rerun.

All ranks and subspaces are over C. Tiles are disjoint nonempty Cartesian
products and cost exactly r(a+b), without inter-tile sharing. Paid root
supply and coefficient preparation, storage, and I/O remain separate. The
inherited possible N additional operations for literal zero-initialized
accumulation remain unchanged. Nothing is asserted for unrestricted Fourier
circuits, overlaps with cancellation, arbitrary basis changes, numerical
rank, finite-field rank, or production performance.

## 1. Source pin and the actual strengthening

SOURCE_PINS.json records bytes, SHA256 and Git-blob hashes of the supplied
source report at commit 32d3ca18b8327d69a9b9c9e9e37e22620d22c94b and its
published supporting mixed-prime and rank-two reports. Byte-bound local
copies are under sources/. Their hashes match the inherited source pins.

The mixed-prime report supplies a direct-sum separation argument and the
cutoff min(a,b)<=4q OR max(a,b)<=max(6p,3p+2q-2,3q), for N=pq^2, p<q.
At p=13,q=17 that alone leaves a few dangerous shapes. The strengthening
here is the rank-one bottleneck in its two-row-residue case: a rank budget
of three across two nonzero supported blocks forces one block to have
rank one. On Z/221Z, a rank-one block having two distinct columns has at
most 17 rows. This replaces the previous largest-row-class pigeonhole
cutoff 4q=68 by 3q=51. The one- and three-residue cases also hold at 51.

The proof below establishes the target completely. No sampled rectangle,
finite-field rank, or scalar shape count is used as a complex-rank proof.

## 2. Characteristic-zero facts

### 2.1 Prime-power universal minors

Let ell be prime and k<=ell. In F_(ell^m), k rows that are pairwise
distinct modulo ell, together with any k distinct columns, give a
nonzero determinant. The transposed statement holds.

To prove this, write the alternant det[x_j^(e_i)] as the ordinary
Vandermonde times an integer polynomial S. At all x_j=1,

    S(1,...,1) = product_(i<j)(e_j-e_i) / product_(i<j)(j-i),

up to a harmless ordering sign. Every factor is an ell-adic unit, so this
integer is nonzero modulo ell. Reduction of Z[zeta_(ell^m)] modulo
1-zeta_(ell^m) sends every selected x_j to 1 and has residue field F_ell.
Thus S at these roots is nonzero in characteristic zero. Distinct columns
make the Vandermonde nonzero. This proves the fact for arbitrary higher
digits, not just for residue representatives. At m=1 it proves that all
prime Fourier minors are nonzero.

### 2.2 Short-support zeros on Z/221Z

A nonzero combination of at most k<=13 distinct characters of Z/221Z has
at most 17(k-1) zeros. In particular, any three distinct columns on more
than 34 rows have rank three; any four distinct columns on more than 51
rows have rank four.

Here is a proof of the only bound used. CRT expresses the characters as
alpha^(ix) beta^(jz), with alpha of order 13 and beta of order 17.
For k'<=k nonzero terms group by the beta-frequency:

    f(x,z)=sum_(j in J) beta^(jz) g_j(x),  t=|J|,
    g_j(x)=sum_(i in I_j) c_(i,j) alpha^(ix), sum |I_j|=k'.

Each nonzero g_j has at most |I_j|-1 zeros by prime Fourier minors.
If z0 values of x make all g_j zero, then z0<=k'-t. For each other x,
a nonzero sum of at most t beta-characters has at most t-1 zeros. Hence

    #zeros <=17z0+(13-z0)(t-1)
            <=13(t-1)+17(k'-t)<=17(k'-1)<=17(k-1).

The first inequality remains valid if some of the g_j(x) are zero.
All coefficient choices and all CRT supports are covered. A dependence
among the selected columns on more rows than this bound is impossible.

### 2.3 Rank-one bottleneck on Z/221Z

If F_221[A,T] has rank one and T contains at least two distinct indices,
then |A|<=17. Fix t0!=t1 in T and a0 in A. Vanishing 2-by-2 minors gives

    221 divides (a-a0)(t1-t0) for every a in A.

Put g=gcd(t1-t0,221). Since the difference is nonzero modulo 221,
g is one of 1,13,17. All a lie in one residue class modulo 221/g,
which has exactly g elements in Z/221Z. Thus |A|<=g<=17. No assumption
on positions, interval structure, or coefficients is involved.

## 3. Supported-column separation, including all parameters

Write R as its s nonempty residue classes R_y modulo 17, and set

    A_y={(r-y)/17 mod221:r in R_y}.

For a column residue v modulo 221, its fiber comprises the selected
columns c=v+221w, w modulo 17. If the fiber has at least s members,
select any s distinct w values. For r in R_y,

    zeta^(r(v+221w)) = zeta^(rv) zeta17^(yw).

The s-by-s scalar matrix (zeta17^(yw)) on the s occurring y values
and these w values is invertible by Section 2.1. Linear combinations
of the selected columns therefore yield, separately for each y, the
vector that equals column v on R_y and is zero on every other class.

If T is any collection of distinct column fibers each containing at
least s columns, it follows that

    rank F_3757[R,C] >= sum_y rank F_221[A_y,T].            (2)

On R_y the representative column v equals
zeta^(yv) zeta221^(kv), k=(r-y)/17; removing its nonzero column phase
gives exactly F_221[A_y,T]. The spaces for distinct y have disjoint
coordinate supports, so the sum is direct. The formula holds for every
fiber representative, every selected higher digit, and every nonempty
row class. It is an internal rank argument and introduces no sharing
between tiles.

## 4. Exhaustive proof of the target dichotomy

We prove that a>51 and b>78 are impossible when the rectangle has
rank at most three. No ordering of a and b is assumed. Write
s=|R mod17| and t=|C mod17|.

First s,t<=3. If C occupied four residues modulo 17, then a>51>3*13
would put four rows in one residue class modulo 13. Write them as
r0+13u_i, with distinct u_i modulo 289. Removing column phases leaves
an F_289 minor with four distinct row indices and columns distinct
modulo 17. Section 2.1 (transposed) makes it nonzero, contradicting
rank<=3. Interchanging rows and columns gives s<=3 because b>78>39.
This eliminates every residue occupancy outside {1,2,3}.

There are now exactly three cases for s; t<=3 throughout.

### Case s=1

Removing column phases reduces to F_221[A_y,T], with columns repeated
only according to their residue modulo 221. A fiber has at most 17
columns. Since b>78>3*17, at least four distinct fibers occur.
Since a>51, Section 2.2 makes four such columns independent. Contradiction.

### Case s=2

A fiber modulo 221 is rich if it has at least two columns. Since t<=3,
there are at most 3*13=39 occurring fibers modulo 221: each mod17
class has 13 refinements modulo 221. If at most two were rich, then

    b<=2*17+(39-2)=71,

contradicting b>78. Choose any three distinct rich fibers as T.
Equation (2) gives rank at least rho1+rho2, where
rho_i=rank F_221[A_i,T]. Both blocks are nonzero, so rho_i>=1.
Rank<=3 forces one block to have rank one. Section 2.3 gives at most
17 rows in that class. The other class then has a-17>34 rows, so
Section 2.2 makes its three columns independent: its rank is three.
The rank sum is at least 1+3=4, contradiction. This covers all row
class size splits, all three-fiber choices, and all coefficients.

### Case s=3

If every column fiber had at most two members, b<=2*39=78.
Thus one fiber has at least three columns. Those three columns give
three independent supported vectors by Section 3; they span the entire
column space of the assumed rank-at-most-three rectangle.
Within each R_y the restrictions of all three basis columns are scalar
multiples of the same nowhere-zero vector (zeta^(rv))_(r in R_y).
Consequently every selected column restricts to a multiple of that
vector. All selected rows in a fixed R_y are therefore projectively
equivalent on all of C. There are at most three projective row classes.

Fix c0 in C. Let H be the subgroup generated by c-c0 for c in C,
and let K=H-perp have size d, with d dividing 3757. Two Fourier rows
are projectively equivalent on C exactly when their difference lies
in K. It follows that

    a<=3d, b<=3757/d, d in {1,13,17,221,289,3757}.

Since a>51, d>17. For every remaining divisor d>=221, b<=17,
contradicting b>78. This includes the case in which fewer than three
projective classes occur. The exhaustive cases prove the contradiction.

The statement just proved holds in either orientation. If both side
sizes exceed 51, each is at most 78. This is exactly (1).

## 5. Strict density, equality audit, and original cost

For actual rank three, transpose so 3<=a<=b. Stable rank gives
ab<=3*3757. If a<=51, then

    3/a+3/b >= 3/a+a/3757 >= 3/51+51/3757=16/221.

The second inequality follows from the exact factorization

    (3/a+a/3757)-(3/51+51/3757)
      =(51-a)(3/(51a)-1/3757)>=0,

since 51a<=51^2=2601<11271. In the other branch both a,b<=78,
so the density is at least 6/78=1/13>16/221. Thus rank-three density
has strict target slack34/3757. The floor16/221 is attainable as a
local rank-three rectangle: take R to be three distinct cosets of the
order17 subgroup and C its full order221 annihilator. The resulting
three different order221 character rows are independent, e.g. for
coset representatives 0,1,2 on columns 0,17,34 by the ordinary
Vandermonde. Its sides are51,221, area3N, and density 272/N.
This local example is not a claimed all-rank optimum tiling.

The six divisors of 3757 give D=min(d+3757/d)=238, with unique unordered
minimizing pair {17,221}. The retained rank-two density theorem gives
E2=min_(d proper)(2d+3757/d)=255. For actual rank r>=4,

    r(a+b)/(ab)>=2*sqrt(r/3757)>=4/sqrt3757>245/3757,

because 16*3757=60112>245^2=60025. Therefore all ranks>=2 have
at least the nonsharp common density excess7/3757 over238/3757.
Rank one has density at least238/3757 by the retained annihilator
containment proof, with equality only at full coset pairs{17,221}.

Summing over a disjoint partition of area3757^2 gives the displayed
cost and area-penalty bound. For attainment, partition rows into the
221 cosets of K={221i:0<=i<17}, and columns into the 17 cosets of
H={17j:0<=j<221}. These 3757 tiles have rank one, area3757, and
cost 238 each. All entries occur exactly once, so cost is894166.

All higher ranks have strict excess, so every optimizer is rank-one-only.
Its tiles must achieve the rank-one equality conditions. Each has
area3757, hence exactly3757 tiles occur. The isolated dangerous scalar
equality shape(68,156) is excluded by (1), not treated as a Fourier
rectangle. Strict and nonstrict conclusions have thus been separated.

## 6. Exact finite verification and coverage contract

check_target.py is fresh and imports no historical checker. It uses
ordinary exact integers and rational arithmetic only. RESULTS.json and
COVERAGE_CERTIFICATE.json retain its exhaustive finite parameter checks;
DANGEROUS_SHAPES.json lists the750 inherited scalar shapes and their
structural exclusion. Source copies, source pins, and a manifest make
the candidate reproducible. Every executed check and its count is
reported by RESULTS.json rather than inferred from a sample.

The mathematical proof is parameter-complete in arbitrary row/column
sets. The finite checker supplements it by verifying the complete
residue/value parameter reductions: all Schur quotient residues for
ell=13,17 and k<=4; every prime17 inversion minor for s<=3; every
nonzero difference modulo 221 in the rank-one bottleneck; all allowed
residue occupancies, all low-rank block budgets and row-size splits;
all possible annihilator divisors; all 750 dangerous shapes including
the sole equality shape; and every stable-rank scalar shape allowed
by (1), together with exact cost/density arithmetic. It additionally
checks a legal local rank-three extremizer and compact, complete
coset-partition certificates. It does not exhaust arbitrary subsets of
Z3757 or assert that it does: arbitrary lifts, coefficients and subsets
are covered by Sections 2--4.

The counter-controls demonstrate exactly why the strengthening needs
two distinct semiprime columns and why the strict side cutoff matters.
A one-column F_221 block can have221 rows and rank one. The legal
51-by-221 rank-three rectangle shows that a>=51,b>78 cannot be
excluded. Neither invalid weakened premise is silently used.

Independent review must separately check the theorem, finite reductions,
original complex model, strict equality classification and source pins.
No owner/index/publication action is performed by this candidate.

### Completed author-control receipt

The fresh checker passed in 1.909040 seconds on the recorded run. It checked
481185 characteristic-zero prime-17 determinants (all scalar separation
matrices for s=1,2,3), 4305 Schur quotient row-residue sets, all 220 nonzero
semiprime differences, 22 short-support integer parameter cases, all nine
remaining occupancy pairs, 1445 compatible two-block row-size cases, all
750 dangerous shapes, and all 33110 stable-rank scalar shapes admitted by
the new dichotomy. It checked all 11271 local-extremizer entry identities,
7514 partition-coordinate identities, all 3757 subgroup difference products,
four source snapshots, and both stated negative controls. These counts
supplement the complete theorem; they are not counts of all arbitrary
Fourier rectangles.
