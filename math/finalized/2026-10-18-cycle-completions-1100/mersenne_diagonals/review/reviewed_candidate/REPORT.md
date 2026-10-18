# Width-adaptive streamed diagonal maps for the Mersenne converter

18 October 2026 UTC. Fresh local continuation of the pinned, independently accepted short-factor setup. No external write was performed.

## Result and limits

The two full-width diagonal maps in the accepted factorial-Toeplitz Taylor shift can be evaluated without multiplying two W-bit values at every coordinate when the coefficient width is sufficiently large relative to the shift length.

Put

\[
\alpha=\log_2 3,\qquad a=\alpha-1,
\quad B_n=\max(1,(n-1)\lceil\log_2 n\rceil),
\quad B=\min(W,B_n).
\]

There is a complete, exact batch construction for both diagonal maps, the full inverse-factorial kernel, and their preparation with cost

\[
O\bigl(nW B^a+nW(\log(n+1))^a\bigr).
\tag{1}
\]

It uses the accepted, independently terminating difference-form Karatsuba routine only on O(B)-bit local operands and O(log n)-bit short factors. It also replaces the separately charged W-bit Newton inverse by a streamed modular division using one O(B)-bit Newton inverse. All carry digits, inverses, coefficient scans, output bits, and tables are charged. This is an explicit evaluation of the maps, not an unevaluated rescaling or a transfer of their costs to the matrix stage.

For the accepted wide-digit Mersenne interface, N=Lm and m>=cL for fixed c>0, define

\[
B_* = \max\{1,\min(m,L\lceil\log_2(L+1)\rceil)\}.
\]

The resulting complete conversion bound is

\[
O\bigl(M(CN)+N B_*^a+N(\log(L+1))^a\bigr).
\tag{2}
\]

M is still the **paid backend of the same-scale convolution**. No property of M beyond the previously accepted convention is needed for the new local construction. If the accepted full-width M backend is preferable, one can keep that alternative: the local diagonal/inversion contribution is bounded by the minimum of the old L M(Cm) bound and the new N B_*^a bound, up to fixed constants. Formula (2) does not claim the new explicit Karatsuba local routine beats every independently supplied backend for every parameter regime.

With the same explicit Karatsuba arithmetic core on both sides, the old diagonal bound is O(n W^alpha); the new one is O(nW B^a). Their displayed upper-bound ratio is (B/W)^a. It tends to zero when W/(n log(n+1)) tends to infinity. This is a genuine improvement of this operation's construction bound, not a measured runtime comparison or a lower bound for the old algorithm.

For example, whenever L=O(log N), the entire new diagonal, inversion, setup and reconstruction contribution is

\[
O\bigl(N(\log N\log\log N)^a\bigr)=o(N\log N).
\tag{3}
\]

The same-scale packed convolution remains M(CN). The matrix-transform and correlated point-product gates remain separate. At the balanced scale m=Theta(L), B_*=Theta(m) and this construction does not improve the old Karatsuba diagonal order. Supplied-prime conditions remain necessary: (3) is an implication for admissible supplied parameter families, not a proof that unbounded Mersenne-prime families of these sizes exist or can be selected cheaply. No complete sub-N-log-N integer multiplier is claimed.

## 1. The exact operation being replaced

For a length-n signed coefficient list |a_i|<2^h, the accepted shift by sigma in {+1,-1} uses

\[
H=h+n+1,\quad g=\lceil\log_2 n\rceil,\quad W=H+g,
\quad s(i)=\operatorname{popcount}(i),
\quad u_i=i!/2^{i-s(i)}.
\]

Every u_i is odd. The two paid diagonal maps are

\[
A_i=2^{g-s(i)}u_i a_i\pmod {2^W},
\qquad R_j=2^{s(j)}u_j^{-1}D_{n-1-j}\pmod {2^W}.
\tag{4}
\]

The kernel is J_i=sigma^i 2^{s(i)}u_i^{-1} mod 2^W. D is the ordinary convolution of reversed A and J. The accepted identity remains

\[
2^{s(j)}u_j^{-1} A_i J_{i-j}
=2^g\binom{i}{j}\sigma^{i-j}a_i\pmod {2^W}.
\]

The present change affects only how the products and inverse action in (4), and the kernel inverses, are computed. The convolution, g guards, centered signed reconstruction and output remain exactly the accepted operations.

## 2. A bounded-carry modular-division primitive

Let R=2^t, 0<u<R with u odd, and let v=u^{-1} mod R. For 0<=x<2^W write x as q=ceil(W/t) zero-padded radix-R limbs a_j. Starting c_0=0, compute from low limbs to high limbs

\[
b_j=((a_j-c_j)\bmod R)v\bmod R,
\qquad c_{j+1}=(u b_j+c_j-a_j)/R.
\tag{5}
\]

The division by R is a bit shift and is exact: the choice of b_j gives u b_j+c_j-a_j=0 mod R.

### Carry bound and correctness

Assume 0<=c_j<u. The numerator in (5) is strictly greater than -R and strictly less than uR:

\[
-(R-1)\le u b_j+c_j-a_j\le u(R-1)+(u-1)=uR-1.
\]

Since it is an integer multiple of R, it is nonnegative, and 0<=c_{j+1}<u. This proves the invariant from c_0=0. The carry never exceeds t bits. The product and pre-split numerator have at most 2t bits, including the subtraction bookkeeping.

For prefixes X_r=sum_(j<r) a_j R^j and Y_r=sum_(j<r) b_j R^j, induction gives

\[
uY_r=X_r+c_r R^r.
\tag{6}
\]

At r=q, reduction modulo 2^W discards the final carry because R^q is divisible by 2^W. Thus the low W output bits equal x u^{-1} mod 2^W. No promise that u divides the ordinary integer x is needed. This is modular division; the final carry need not vanish. The partial last limb is handled by masking the final W bits.

### Paid operation count

Once v is available, there are exactly 2q local t-bit multiplications, q bounded additions/subtractions and q limb writes. All input and output are processed through fixed windows. With K(t)=O(t^alpha), the cost is

\[
O\bigl(q(K(t)+t)+W+t\bigr).
\tag{7}
\]

Computing v by precision-doubling Newton iteration costs O(K(t)); every operand is reduced to the current precision before multiplication. The full cost including v is O(W t^a+t^alpha). The corresponding accepted streamed product x u mod 2^W uses q local t-bit products and has the same asymptotic bound.

The supplied code converts the input to a byte buffer once, reads bounded slices once, writes output slices once, and assembles the output once. It never repeatedly right-shifts an entire W-bit input or updates a growing whole output. The proof is in the same sequential-bit/array arithmetic-core model as the accepted setup. It is not a Python interpreter or allocation timing claim.

Low-to-high quotient-digit recovery using a modular inverse is an established technique. The [GNU MP exact-division documentation](https://gmplib.org/manual/Exact-Division) describes that principle. The present recurrence is proved separately for the modular, not necessarily ordinary-exact, division needed here. No priority for modular division, Karatsuba, or factorial diagonalization is claimed.

## 3. Why the factorial multiplier can be shorter than W

For 0<=i<n and n>=2,

\[
1\le u_i\le i!\le(n-1)!<n^{n-1}\le 2^{B_n}.
\tag{8}
\]

For n=1, u_0=1 and B_n=1. Choose B=min(W,B_n) and byte-rounded t=8 ceil(B/8). Therefore B<=W and t=O(B). Work with

\[
U_i=u_i\pmod {2^t},\qquad v_i=U_i^{-1}\pmod {2^t}.
\]

These small representatives always define the correct action modulo 2^W:

- If W<=t, congruence modulo 2^t implies congruence modulo 2^W.
- If W>t, B cannot equal W. Hence B=B_n, (8) gives u_i<2^B<=2^t, and U_i=u_i as ordinary integers. There is no truncation error.

Thus U_i=u_i mod 2^W in both cases, and U_i is odd. Applying streamed multiplication or (5) with U_i gives exactly the two maps in (4), followed by their bounded shifts. A full-width inverse residue can be replaced by modular division by its short denominator; its displayed W-bit residue is not evidence that a W-by-W product is necessary.

When W=Theta(n), B=Theta(W), so this argument deliberately makes no asymptotic saving. It is the W>>n log n regime that supplies narrower local products.

## 4. Shared preparation and full kernel output

Set o_i to the odd part of i. Prepare the small tables by

\[
U_0=1,\quad U_i=U_{i-1}o_i\pmod {2^t};
\quad v_{n-1}=U_{n-1}^{-1}\pmod {2^t};
\quad v_{i-1}=v_i o_i\pmod {2^t}.
\tag{9}
\]

There is only one O(t)-bit Newton inversion for the entire batch. The 2(n-1) table products have O(log n)-bit factors and use the accepted short-factor streaming method. The U table contains ordinary odd factorial integers when they fit; when they do not fit, it contains residues. Constructing those values is paid explicitly. The older implementation's prohibition on silently building full factorials is not being used to treat this new work as free.

To prepare V_i=u_i^{-1} mod 2^W for the convolution kernel:

- If W<=t, take the low W bits of v_i.
- If W>t, compute V_(n-1)=stream_div_odd(1,U_(n-1),W,t,v_(n-1)), then recover V_(i-1)=V_i o_i mod 2^W by the accepted short-factor recurrence.

This supplies every W-bit kernel entry. The single long modular division costs O(W B^a), not M(W). Its carry is bounded by U_(n-1), although its output has W bits. The reverse recurrence costs O(nW(log(n+1))^a). Reusing the small v_i table for all final diagonal divisions needs no further inversion.

The full preparation charge is

\[
O\bigl(K(t)+WB^a+nW(\log(n+1))^a\bigr).
\]

Because B<=W and t=O(B), K(t)=O(WB^a). Both full diagonal batches together cost O(nW B^a). Tables, scans, signs, bounded shifts, guards, and all output bits fit in O(nW), giving (1). Factor construction and small-index arithmetic are covered by the inherited O(n log^2(n+1)) allowance; W>=n absorbs it. The n=1 shift is returned directly in O(W), with no convolution or table construction.

Storage is O(nW), plus the convolution backend's workspace. Microtables use O(nt)=O(nW) bits; full kernel and diagonals use O(nW); each streaming carry/transient uses O(t). This construction neither combines unrelated coordinates in a single packed product nor claims cross-coordinate independence as a lower bound. Its batch saving is the narrower denominator width and the shared microinverse table.

## 5. Unchanged convolution, conversion, grouping and output ledger

The convolution remains the accepted base-2^b packing,

\[
b=8\left\lceil\frac{2W+\lceil\log_2 n\rceil}{8}\right\rceil,
\quad S=nb.
\]

Every unreduced coefficient is less than n 2^(2W)<=2^b. One product of two S-bit-capacity integers and O(nW) bounded-window extraction gives the exact modular convolution. This operation costs M(S), and it is not performed using the short-divisor trick. The new complete shift bound is

\[
C_{new}(n,h)=O\bigl(M(S)+nWB^a+nW(\log(n+1))^a\bigr).
\tag{10}
\]

The accepted valuation identity proves the low g bits of R_j vanish. Dividing by 2^g keeps exactly H bits. The strict coefficient bound |(T_sigma a)_j|<2^(H-1) gives unique centered reconstruction, as before. All n outputs are returned. The masks and shifts in the implementation do not change the guard precision.

For binary, redundant p, canonical p, lazy raw-product and inverse interfaces, n=O(L), W=O(m) and S=O(N) under m>=cL. Consequently B=O(B_*), nW=O(N), and (10) yields (2). The existing local exact Mersenne quotient/carry and binary carry streams cost O(N), including final carry drainage and possible extra p digits. They are retained, not replaced by an uncharged long division or repeated whole-integer construction.

For 1<=d<=L, grouping/ungrouping adds O(L/d) length-at-most-d shifts. Their convolution cost is still (L/d) M(Cdm); the new local contribution is at most

\[
O\left(N\min(m,d\log(d+1))^a+N(\log(d+1))^a\right).
\]

Using monotonicity of M(t)/t, the first contribution aggregates into O(M(CN)); the local terms are no larger than their global L counterparts. Partial groups, a possible additional p digit and the accepted bounded-overlap raw grouped expansion preserve the bound. The accepted actual-width handling of a lone digit with d greater than its length is retained; no fictitious d-entry table is allocated.

The finite grouping controls test positional identities. They are not a new implementation of the full grouped matrix product. The original matrix coefficient bounds must still account for enlarged redundant input heights.

## 6. The precise residual obstruction and open gates

For the nontrivial binary input shift, n=L>=2 and h=m, so W=m+L+1+ceil(log_2 L)>m. The prescribed convolution capacity satisfies

\[
S=nb\ge 2LW>2Lm=2N.
\tag{11}
\]

Therefore the literal recipe that replaces this backend call with the entire same binary-to-Mersenne multiplier on its prescribed capacity has a larger recursive child. If that recipe is applied at every nonleaf and terminates only below a fixed size cutoff, repeatedly following this child never reaches the cutoff. It is not an independently terminating recursion. A different contraction, fusion, special-kernel evaluator or independent backend is required.

This is an obstruction to **that specific capacity-parametrized recursive substitution**, not a multiplication lower bound, not an assertion that every actual operand has S nonzero significant bits, and not a lower bound against specialized convolution algorithms. Actual-value pruning or joint circuit simplification would be additional constructions needing proof and their own charges.

Packing the coordinate lists densely and extracting even coefficients does not evaluate a diagonal map: coefficient 2i also contains all a_j U_k with j+k=2i. A negative control records this failure. It is not used to rule out more sophisticated packing or shared arithmetic.

The following remain open for the user's full target:

1. The same-scale factorial-Toeplitz convolution, even in the logarithmic-L regime where the new local terms are little-o.
2. Full diagonal improvement at the balanced width W=Theta(n), or another construction avoiding it.
3. The Mersenne/matrix transform schedule and correlated point-product work. This result changes neither their transform-layer bill nor their aggregate recursive coefficient width.
4. Availability, validation and selection cost of growing primes p=2^m-1 when strict primality and adaptive sizes are required. Arithmetic in this report needs no primality; composite controls do not establish prime availability. Fixing p=3 does not permit unbounded L under m>=cL.
5. A complete composition ledger proving all recursive leaves, conversions and explicit output are o(N log N). The present result establishes only the stated local-conversion advance.

No known full multiplication algorithm was swapped in and credited to this route. M(S) remains visible; the new code uses only explicit short Karatsuba, streamed carries and modular inverse digits for the changed operations. Fully instantiating the separate convolution with Karatsuba still gives O(N^alpha) total conversion, dominated by that convolution.

## 7. Fresh bounded evidence and provenance

The new files diagonal_core.py and fresh_controls.py were written for this continuation. No historical program was imported or executed. After one harness-only decimal-string serialization failure on a 16,385-bit test value, the digest representation was changed to hexadecimal; the failed log is retained. No arithmetic assertion had failed. The complete fresh run then passed:

- 4,192 independent Karatsuba products.
- 65,280 exhaustive modular divisions, including W<t.
- 360 larger product/division cases, with every modular-division prefix identity and carry bound checked independently, up to 16,385 input bits.
- 48 odd-factorial/microinverse/full-kernel tables checked against exact factorial and independent modular-inverse oracles.
- One empty shift and 400 signed Taylor-shift/inverse controls against direct binomial sums.
- 45 binary/p conversion round trips, including supplied small Mersenne primes and composite controls.
- 135 grouped-digit positional identities.
- Six instrumented controls proving exactly 2 ceil(W/t) local products per modular division, all with argument widths at most t.
- Two negative controls: omitted carry and naive dense diagonal packing.

The microinverse is supplied to the instrumented division so its exact 2q count excludes preparation; the separately proved and paid Newton routine is tested through tables and other controls. Native Python multiplication, factorials, modular inverses and binomial coefficients in the test driver are independent correctness oracles only. The production convolution uses the explicit Karatsuba routine unless a separately paid backend is passed. No timing or asymptotic conclusion is inferred from samples.

The accepted source package is pinned to repository AgentSlop-Si/research, commit d1c6910aa9fc4ef861981358e8bf3e0c71585689, under math/finalized/2026-10-18-cycle-completions. Exact restored source bytes and their checksums are recorded in SOURCE_PINS.json. The accepted setup and inherited conversion/matrix scopes remain distinct from this new candidate result. Independent review of this continuation is still required.
