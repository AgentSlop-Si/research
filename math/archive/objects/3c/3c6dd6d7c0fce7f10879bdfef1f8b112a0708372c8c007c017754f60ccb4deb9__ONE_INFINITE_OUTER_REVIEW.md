# Both one-infinite-outer N4 charts are excluded

Independent replacement-reviewer result, 9 October 2026 UTC.

## Statement

Write Z e_j=e_(j+1 mod 4), let V have cycle order (0,2,1,3), and set

G0=(I-Z/4)^(-1), G1=(I-V/5)^(-1), H(x)=G0+x G1,
F[j,k]=i^(jk).

Neither F=H(x) L H_[r:s] M G1 nor
F=G1 L H_[r:s] M H(x) is possible for finite complex x,
nonzero [r:s], and invertible diagonal L,M. Here
H_[r:s]=r G0+s G1; internal permutations are identity.
Nonzero scalar multiples of the outer stages are absorbed in the masks.

Together with the existing common-outer-infinity witness, this excludes
every projective chart with at least one pure-G1 outer factor. It does
not exclude independently variable finite outer couplings on their
regular chart. The existing equal-outer result and finite-outer
zero-middle exclusions retain their stated scopes.

## Independent construction

The accompanying script constructs G0,G1 using their exact four-term
geometric sums. It builds adj(H(x)) directly from symbolic 3-by-3
cofactors and checks H(x) adj(H(x))=det(H(x)) I. No project program or
uploaded code is imported or executed.

The exact determinant is

det H(x)=(15x+16)(10625x^3+30500x^2+29920x+9984)/159120.

A singular outer stage cannot produce invertible F and is excluded for
this elementary reason. For each chart form K=adj(H(x)) F adj(G1) or
K=adj(G1) F adj(H(x)), respectively. Outside determinants contribute
only nonzero scalar factors for a putative solution.

## Regular middle chart, including middle infinity

For i,j=1,2,3, diagonal equivalence requires

K_ij K_00 B_i0 B_0j - K_i0 K_0j B_ij B_00 = 0,

where B=r G0+s G1. Collecting coefficients of r^2,rs,s^2 gives a
9-by-3 polynomial coefficient matrix. The vector (r^2,rs,s^2) is
nonzero for every projective [r:s], including [0:1]. Therefore all
3-by-3 coefficient minors must vanish.

The script uses equation order (1,1),(1,2),(1,3),(2,1),...,(3,3).
In each outer chart, the minors with row indices (0,1,2) and (0,1,3)
both have degree 18 and their exact monic gcd has degree 5 over Q(i).
Every root of this gcd is a root of the explicitly forbidden guard
det(H(x)) K_00(x): repeated exact gcd and division by that guard
leaves the constant 1. All coefficients and removed factors are in
ONE_INFINITE_OUTER_RESULTS.json.

The guard is justified only on this regular chart: if B is entrywise
nonzero and the masks are invertible, K is entrywise nonzero, so
K_00 is nonzero. Thus these two minors alone exclude this chart.
Pure G1 is entrywise nonzero, so middle infinity is included.

## All zero-middle branches

The finite zero-entry middle parameters are exactly the nine values
obtained as -G0_ij/G1_ij. For each value the script imposes K_ij=0 at
every zero position of B and the cross-product equations on every
fully supported 2-by-2 rectangle. These are necessary even when the
anchor vanishes. In each of the 18 cases (nine values in each of two
outer charts), the exact univariate gcd of those necessary equations
is 1. No determinant or support guard is removed in those branches.

This completes both charts, without using a modular diagnostic or
numerical root test. Changing Fourier phase conjugates the equations
and gives the same conclusion.

## Reproduction

Run check_one_infinite_outer.py with Python and SymPy. It has no data
file dependency. ONE_INFINITE_OUTER_RESULTS.json is its complete
exact output. A separate portable replay and checksums accompany the
frozen checkpoint.
