# Precision-adaptive Newton channels: finite producer and paid limits

15 October 2026. Construction 3, original arithmetic-progression Newton route.

## Result

A concrete finite LOW/full-product producer now avoids a single uniform factorial-coordinate CRT modulus. Each output coordinate stops at its own certified modulus; later primes evaluate and interpolate only the Newton sample prefix needed by the remaining coordinates. All data products are modular products at the actual prime width. No exact-integer sample-product wrapper is used. This is a different invoice from the obstruction in `newton_low_high_producer/REPORT.md`, Section 6.

The improvement is real but insufficient. On the tested r=8, p=7, g=4 maximal-digit example, the sum of retained coordinate-CRT capacity bounds falls from 1,155 to 713 bits, and online NTT butterflies fall from 4,320 to 3,840. The central coordinate remains active until the final prime, retaining at least r samples and conventional transform work per prime. The literal compiler still fails the pinned native-potential gate. Prime/root search, binary conversion, CRT, modular scalar reconstruction, and all constants are paid; the complete elementary implementation is not a fast-multiplication theorem.

A complementary even-g scalar functional bypasses exact Newton-coordinate reconstruction altogether, using different binary precision for each sample. Its necessary guard is nearly matched by a reachable product alias: for bit zero the sufficient common guard exceeds the alias threshold by only the population count of r−1. This is a samples-only statement, not a lower bound on raw-input multiplication. The sibling odd-g/integral-functional lane has a different valuation behavior and is not conflated with this result.

## 1. Typed one-block contract

Let p>=2, g>0, r>=2, and

    e_j(x)=product_(u<j)(x+gu), E_j=e_j(p), Q=E_r.

The binary inputs satisfy 0<=X,Y<Q. Paid successive divmod by p,p+g,...,p+g(r−1) obtains digits a_j,b_j, giving

    A(x)=sum_(j<r) a_j e_j(x), B(x)=sum_(j<r) b_j e_j(x).

Write the unrestricted product

    A(x)B(x)=sum_(j<d) D_j e_j(x), d=2r−1.

The output contract is R=XY modulo 2^k in [0,2^k). Setting k>=bit_length(X)+bit_length(Y) gives the full ordinary product. This is an all-size one-block family: increasing r makes Q arbitrarily large for fixed p,g. It does not claim that the implemented prefix pruning commutes with arbitrary outer-frequency quotient/carry operations in the many-block source.

After reconstructing D, scalar Newton-Horner evaluates it at p modulo 2^k. No periodic boundary fold is needed because A(p)B(p) is already the desired integer. Omitting that fold at this scalar interface does not make final arithmetic free; every Horner product, addition, signed binary reduction, and carry propagation within those operations is paid. There is no external multiplication/convolution engine and no hidden full-input X*Y in the producer.

## 2. Cheap coordinate-specific height bounds

Let B>=1 bound the magnitude of every input digit, b=bit_length(B), and

    H_j=min(j,2r−2−j),
    c=ceil(log2(1+g(r−1)^2)),
    h_j=2b+ceil(log2 r)+H_j c.

Then |D_j|<2^h_j. The elementary proof uses the exact basis product

    e_i e_l = sum_h (-g)^h h! binom(i,h)binom(l,h)e_(i+l−h).

A contribution to D_j has h=i+l−j, so 0<=h<=H_j. For fixed h there are at most r pairs (i,l). Also

    h! binom(i,h)binom(l,h) <= (r−1)^(2h)/h! <= (r−1)^(2h).

Therefore

    |D_j| <= r B^2 sum_(h=0)^H_j [g(r−1)^2]^h
           <= r B^2 [1+g(r−1)^2]^H_j < 2^h_j.

Only bit lengths and parameter-size integer arithmetic are needed to construct h_j. No factorial-height integer or dense basis-product table is formed. The bounds are conservative, not claimed minimal or attained simultaneously. Actual operand heights are used only to choose B, not assumed for free.

The tent has

    sum_(j<d) H_j=(r−1)^2,

versus d(r−1) for a uniform maximum bound. Thus coordinate dynamic-range storage can improve by a factor approaching two when this height term dominates. Prime overshoot and base digit height can reduce that saving, as the finite rows demonstrate.

## 3. Actual adaptive per-prime circuit

Use a prefix of distinct certified primes q_i. Let P_i=product_(u<=i)q_u, P_0=1, and declare coordinate j active before prime i precisely when it has not yet reached

    P_i > 2^(h_j+1).

Once the inequality holds, its signed CRT representative is uniquely D_j and is never updated again. Different coordinates therefore retain different prime sets and different-width CRT accumulators.

Before a prime, let ell=1+max(active j). For j<ell the Newton coefficient depends only on samples at 0,...,j. Thus only

    f(t)=A(−gt)B(−gt), 0<=t<ell,

are needed. Input Newton terms of index greater than t vanish at node −gt, so each input bank uses only its first min(r,ell) coefficients. This is an exact prefix property, not an assumption that the polynomial has lower degree.

Over F_q, use the recovered factorial convolution, with q>ell−1 and q not dividing g:

    U_A[t]=sum_(j<=t) a_j(-g)^j/(t−j)!,
    U_B[t]=sum_(j<=t) b_j(-g)^j/(t−j)!,
    W[t]=U_A[t] U_B[t] t!.

Convolve W with (-1)^u/u! and unscale by (-g)^(-j). The result is D_j modulo q for each active j. These are exactly the source Newton evaluation/interpolation maps, with a shorter prefix where justified. The two input convolutions share one prepared kernel. The output convolution has its own prepared kernel. No monomial-basis conversion is materialized.

Minimal power-of-two padding is

    n_E=pow2ceil(min(r,ell)+ell−1),
    n_I=pow2ceil(2ell−1).

A single certified order-L root suffices, where L=pow2ceil(2d−1), since every executed n_E,n_I divides L. Unlike output CRT storage, a field cell always has the actual w_i=bit_length(q_i) width at that prime. Coordinates are not assigned fictional fractional field widths.

Incremental CRT is also explicit. For each active j,

    z_j=(D_j mod q − R_j)(P_(i−1)^−1) mod q,
    R_j <- R_j+P_(i−1)z_j.

The inverse of the common P_(i−1) modulo q is shared for that prime. The growing-width P*z_j product, its addition, and reduction of R_j modulo q are all paid. A completed coordinate is centered in (−P_i/2,P_i/2). Odd P_i makes centering unambiguous.

Finally the code performs modular scalar Newton-Horner from high index to low. Since e_(j+1)(p)=(p+gj)e_j(p), this returns exactly XY modulo 2^k. Signed reduction modulo 2^k is bit truncation with the correct Euclidean representative, including negative D_j; truncation toward zero is not used.

## 4. Root conditions, cold setup, and uniform termination

The implementation searches q=cL+1 in increasing c, certifies primality by trial division, rejects q dividing g, and searches a with

    omega=a^((q−1)/L) modulo q,
    omega^(L/2)=−1, omega^L=1.

Because L is a power of two, these tests certify exact order L. Every factorial up to ell−1 and g is invertible. Smaller transform roots are powers of omega. Forward/inverse twiddle tables, inverse transform lengths, factorials, inverse factorials, signed g powers, and kernel spectra are constructed and charged per prime, then shared only within that prime's call. There is no free fixed-word list or unbounded root table.

The exhaustive prime search terminates mathematically without assuming a favorable prime-distribution bound. If only finitely many eligible primes had appeared, set X=2g times their product. Any prime divisor q of X^(L/2)+1 is odd, divides neither X nor g, and the order of X modulo q is exactly L. Hence q=1 mod L and is a new eligible prime, a contradiction. This proves existence, not fast setup.

The literal trial-division and root search are intentionally elementary. If C_i is the actual candidate set searched before q_i, a coarse setup bound is

    O(sum_(u in C_i) sqrt(u) bit_length(u)^2 + q_i w_i^3),

plus parameter construction, tables and kernels. The q_i term safely bounds an exhaustive root search with repeated-squaring modular exponentiation. This can be vastly larger than the online producer. No near-linear all-size setup bound is asserted. The finite implementation closes these calls with binary arithmetic rather than leaving an oracle.

## 5. Complete bit and native-child invoice

`producer.py` uses explicit shift/add for every data-dependent product, explicit binary long division for ordinary modular reductions and input divmod, and bit truncation for final binary reductions. The test file alone uses Python multiplication as its independent oracle. Ordinary language-level storage/iteration is not claimed to be a measured bit machine.

For prime i let a_i be the number of active coordinates and ell_i,n_Ei,n_Ii as above. The exact online butterfly count is

    T_i=2 n_Ei log2 n_Ei+n_Ii log2 n_Ii.

Prepared-kernel butterflies add

    K_i=(n_Ei log2 n_Ei+n_Ii log2 n_Ii)/2.

Beyond these twiddle products, the online field multiplication slots are

    4n_Ei+2n_Ii+2ell_i+2min(r,ell_i)+a_i.

These are respectively fixed-kernel products plus inverse normalization, one factorial bank plus sample products, two input scaling banks, and active output unscaling. Factorials/powers/twiddles/root exponents add their actual setup slots. Every butterfly also pays two field additions and data movement.

With elementary arithmetic each w-bit modular multiplication/reduction is O(w^2); it is not one bit operation. Thus a complete parameterized bound is

    C_input + C_bound + C_prime/root
    + sum_i (T_i+K_i+O(n_Ei+n_Ii+ell_i+w_i)) O(w_i^2)
    + C_CRT + C_output + C_movement.

Here the O(w_i) setup exponentiation count is per fixed number of inverse/root exponentiations after a root is chosen; exhaustive root search is already included in C_prime/root. Definitions of the remaining costs are explicit:

- Input conversion: sum of actual successive dividend/radix long-division costs, plus radix construction. With dividend length N_j and radix width v_j this is O(sum (N_j+1)(v_j+1)). Trailing zero digits and parameter storage are included.
- Bound construction: O(r) operations on the actual parameter/height widths, including the products that form g(r−1)^2 and H_j c.
- CRT: if ellP_i=bit_length(P_(i−1)), reductions and lifts cost O(sum_i (a_i+1)(ellP_i+w_i)w_i), plus the paid modular inverses. Completed coordinates are absent from later rounds. Overshoot is measured at actual P_i, not h_j alone.
- Output: with v_j=bit_length(p+gj), scalar products use at most k and v_j magnitude bits. Additions, signed reduction and coefficient reads give O(sum_j (k v_j+k+v_j+h_j)) bit work with the elementary scalar multiplication used here. This includes the binary carry work. A near-linear conversion/output procedure is not silently substituted.
- Storage: completed/active CRT accumulators at their actual stopping widths, current prime's O(n_Ei+n_Ii) field cells of w_i bits, the original input/output bits, and constants/indices. The reported 713 versus 1,155 capacity-bit comparison is only the coordinate CRT component, not total storage.

For an explicit native-wrapper ledger, every nonzero a-bit by b-bit integer product recorded by the implementation can be realized as F(a+b), multiplication modulo 2^(a+b)+1, with signs and copies paid. It is not F(max(a,b)). `native_wrapper_capacities` records the actual capacity histogram across online arithmetic, setup, CRT and output. A formal substitution has

    Cost <= C_nonproduct + sum_s histogram[s] F(s).

The concrete implementation instead closes all these products by shift/add. The histogram is a fully specified finite invoice, not a claim of a favorable same-native recurrence. In particular, large setup primes, growing CRT products, and final scalar products can fail strict child contraction; elementary base cases remain available. Even the online field subinvoice fails the desired potential screen below.

## 6. Why the adaptive NTT schedule still misses the native gate

This is a scoped statement about this literal conventional-transform compiler, not every prime-adaptive Newton circuit.

The tent-bound maximum is attained at j=r−1. That coordinate remains active until the last prime; consequently ell_i>=r at every prime, and T_i=Omega(r log r). This remains true even though high-index coordinates stop early. Power-of-two padding means many reductions in ell_i do not change n_Ei or n_Ii at all.

For a clean growing dense family take r powers of two, g=4,

    m=r(log2 r)^2, p=2^m−1, a_j=b_j=p−2.

These are legal inputs, and N=ceil(log2 Q)=(1+o(1))rm. The center bound is 2m+O(r log r), so the prime product must have Omega(m) bits, meaning sum_i w_i=Omega(m). Each prime supports order L=Theta(r), giving w_i=Omega(log r).

Charge each literal generic field twiddle/data slot its full product wrapper F(2w_i), and consider an ordinary-parent wrapper capacity n=2N. If some child has 2w_i>=n, the strict contraction requirement already fails. Otherwise, for any fixed beta in (0,1], the online field subinvoice has normalized potential at least a constant times

    [r log r * m * (log log r)^beta] / [N (log N)^beta]
      = Omega((log r)^(1−beta)(log log r)^beta),

which diverges. In particular it cannot admit the pinned beta=0.998327339802923082. CRT, root setup, input/output conversion and all extra work only add costs.

This is a declared full-width generic-slot invoice. It is not a bit lower bound for special constant multipliers, zero-skipping, a different convolution backend, whole-DAG sharing, or a direct scalar algorithm. The old exact-integer-sample width argument is not reused here. This different modular circuit has been specified and charged on its own terms.

## 7. Even-g sample precision: a near-matched reachable guard

For p odd and g even, set s=2r−2, a=v2(g), and

    lambda_t=s a+v2(t!)+v2((s−t)!),
    Lambda=s a+v2(s!).

Lagrange evaluation at p has weights

    L_t=(-1)^t product_(u!=t,0<=u<=s)(p+gu) / [g^s t!(s−t)!].

Every numerator is odd, so the denominator's exact binary valuation is lambda_t. An exact finite scalar LOW circuit uses sample t modulo

    2^K_t, K_t=k+lambda_t
             =k+Lambda−v2 binom(s,t).

For each term, invert only the denominator's odd part modulo 2^K_t; multiply its sample and odd numerator there; shift by Lambda−lambda_t; accumulate modulo 2^(k+Lambda); and divide the accumulated representative by 2^Lambda. The division is exact because the Lagrange identity equals the integer C(p). This is not division of each individual rational term. The result is C(p) modulo 2^k.

`even_guarded_low` executes this circuit using modular Newton-Horner sampling, paid modular numerator/odd-factorial products, a doubling-precision odd inverse, and the final exact shift. Its direct constant/sample schedule has O(r^2) arithmetic cells; schoolbook bit work is bounded by O(r^2 W^2), where W includes k+Lambda and the actual p,g,index parameter widths. It is exact, but not claimed fast. No q-adic or field factorial inverse is mistakenly used over an even ring.

The spread between maximum and minimum K_t is at most O(log r), since v2 binom(s,t)=O(log r). Thus even-g transposition removes materialized factorial-sized coefficients but does not yield a large per-sample precision taper.

There is also a genuine product-transcript alias close to this guard. Let h=r−1 and compare A=B=e_h against A=0,B=e_h. All samples of the first product are

    g^(2h)(h!)^2 binom(t,h)^2,

so they vanish modulo 2^G with G=2h v2(g)+2v2(h!). At t=h this valuation is exact. Yet the represented integer E_h^2 is odd. A samples-only algorithm at common precision <=G cannot recover bit zero.

The sufficient maximum bit-zero precision is Lambda+1, and

    Lambda−G=v2 binom(2h,h)=popcount(h)<=O(log r).

For r powers of two this gap is log2 r. This nearly matches the necessary common guard additively. It does not prove each K_t individually optimal on reachable products, nor constrain algorithms still allowed to inspect original input bits.

## 8. Why an odd-CRT low-bit shortcut needs more information

An odd modulus exceeding 2^k does not by itself identify an integer's residue modulo 2^k. A reachable source transcript makes the issue concrete.

Take r=2, p=2047, g=4, and the valid constant-digit input X=1649=17*97, versus X=0, with Y=1. Both primes support every required length (L=8), are distinct, and do not divide g. Every recovered sample/product transcript modulo either prime is identical for the two pairs. The actual products have different low bits, although the combined odd modulus greatly exceeds 2.

Thus replacing the coordinate reconstruction thresholds by “enough CRT bits for the requested LOW width” is not valid for a decoder that only sees those residues. Original-input access distinguishes the cases, and a separately derived carry/error relation could also change the interface. Neither is silently granted to this shortcut.

## 9. Fresh executed evidence

Run:

    python precision_adaptive_channels/test_precision.py

The newly written tests import no supplied implementation. They use a direct integer overlap-identity reference independent of the NTT/factorial interpolation path, and execute:

- 1,000 elementary signed multiplication/Euclidean-division comparisons;
- 77 adaptive LOW products, including zeros, maximal digits, unit-basis squares, signed Newton outputs, p=2, prime candidates dividing g, odd/even g, and r in {2,3,4,5,8};
- 511 exact Newton-coordinate comparisons and height-bound checks;
- 15 additional complete ordinary products;
- primality, exact root order and all transform support conditions on every executed prime;
- exact measured online/kernel butterfly counts against the formulas for every round;
- 84 even-g guarded scalar LOW products;
- 21 reachable binary sample-precision aliases, plus the odd-CRT low-bit alias;
- tent sums and central-binomial guard gaps through r=128.

All pass. The r=8, p=7, g=4 maximal-digit CRT example executes 9 primes. Sample prefixes are 15,15,15,14,13,12,10,9,8; interpolation padding stays 32 until the last round, then falls to 16. It executes 111 data products, 3,840 online butterflies, 1,296 kernel-preparation butterflies and 87 coordinate CRT lifts. Its coordinate capacity bounds total 713 bits versus 1,155 for retaining every coordinate through the last common modulus. The full recorded native-wrapper histogram for this row has maximum child capacity 78 bits against parent capacity 68 bits; its pinned-beta potential ratio is about 1,013.98, including setup, CRT and output. Thus even this finite complete invoice visibly fails contraction and the potential test. These are exact finite ledger counts and a floating evaluation of their potential, not runtime or whole-memory measurements.

`RESULTS.json` preserves seeds, rounds, prime widths, roots, coordinate bounds, arithmetic counters and native-wrapper capacity histograms. `test_output.txt` is the direct test result. Independent review/test findings are separate and are not preemptively claimed here.

## 10. Status and attribution

Retain both circuits and their scope: a per-prime/per-coordinate exact LOW/full producer with finite savings, and an even-g scalar precision certificate with a near-matched reachable alias. Neither establishes the missing-log fast multiplier or passes the strict native recurrence gate.

Arithmetic-progression factorial convolution, Lagrange interpolation, radix-two NTTs, CRT and odd Newton inversion are classical. The recovered source and normalized compiler are documented in `latest_multibase_material_audit/REPORT.md` and `fused_newton_channels/REPORT.md`. The contribution here is the explicit adaptive schedule, its finite bit implementation, and the scoped precision/native-invoice audit; no worldwide novelty claim is made.
