# Exact lazy residues and a concrete coefficient-lift batching target

Date: 2026-10-17.

## Result

The attached matrix/Fermat route can be extended with an exact signed, lazy-reduction kernel. The fresh implementation removes all canonical modular corrections inside transform stages. Five held-out input pairs, three repetitions each, give convolution-only improvements of 1.083–1.257 times against a fresh matched canonical kernel. Every forward and inverse boundary normalization and every pointwise product is timed.

This is a finite implementation improvement. It does **not** prove multiplication in little-o(N log N). The transform still has Theta(K r log K) bit work in the explicit representation. Native pointwise products remain fully disclosed.

A second construction below gives an exact, O(N)-volume polynomial-coefficient representation with O(log N)-bit coefficients throughout the transform, using a mildly skewed digit size m approximately sqrt(N log N). It is a concrete representation for a stage-fused algorithm, not a completed fast batch algorithm. Two precise missing lemmas remain: a collective layer/movement saving and control of total recursive child mass.

## 1. Sources and execution scope

The supplied zip's enhanced.py, COMPLEXITY_PROOF.txt, and ENHANCEMENT_REPORT.txt were read as data. No historical program was imported or executed. The fresh lazy_fermat.py was inspected before execution: standard-library imports only, no subprocesses, no networking, no external writes, bounded deterministic validation and benchmark loops, and stdout JSON. The shell redirected its output to results.json in this directory.

The comparison is between two modes of this fresh program. It is not a remeasurement of the historical program and not an end-to-end radix-conversion benchmark. The code also validates end-to-end products, but those correctness checks are separate from timing. There is no parameter tuning on the measured pairs.

The underlying power-of-two roots in Fermat rings are established, for example in the [GMP FFT multiplication documentation](https://gmplib.org/manual/FFT-Multiplication). No novelty claim is made for lazy modular reduction. The particular proof and experiment here are supplied to extend the user's prototype honestly.

## 2. Signed split-fold, including negative inputs

Let R = 2^r, Q = R+1, and K = 2^ell with K dividing 2r. For an arbitrary signed integer x and 0 < s < r, define

    F_s(x) = ((x << s) & (R-1)) - (x >> (r-s)).

The right shift of a signed integer means floor division. Write

    x = a * 2^(r-s) + b,    0 <= b < 2^(r-s).

Then F_s(x) = b*2^s - a, whereas x*2^s = aR + b*2^s. Their difference is aQ. Thus F_s(x) is exactly x*2^s modulo Q, including x < 0 and the exceptional canonical input x=R.

For a general root exponent e, reduce e modulo 2r. If e >= r, use a final sign change and replace e by e-r; if the resulting exponent is zero, return x or -x without a split-fold.

For every integer C >= 1, |x| <= C R implies |F_s(x)| <= C R. Indeed,

    -C*2^s <= a <= C*2^s,
    0 <= b*2^s <= R-2^s,

so F_s(x) lies between -C*2^s and R+(C-1)*2^s, both inside [-CR, CR]. Sign changes preserve the bound. No assumption of a nonnegative representative enters this argument.

## 3. The exact lazy transform

Use the same forward decimation-in-frequency and inverse decimation-in-time schedule as the canonical transform. At each butterfly:

1. Perform any required inverse twiddle with the signed split-fold.
2. Compute u+v and u-v as signed integers, with no canonical modular correction.
3. Perform any required forward twiddle with the signed split-fold.

Starting from canonical residues, |x| <= R. After t butterfly stages, the bound is

    |x| <= 2^t R.

The preceding signed-shift bound proves that twiddles do not increase this stage envelope. At the end, all values have magnitude at most K R. A signed implementation therefore needs at most r+ell+1 magnitude bits, plus its sign convention. It does not require a full extra r-bit limb or an unspecified precision budget.

For the inverse transform, apply the root action with exponent -ell to implement multiplication by K^(-1) modulo Q. This action also preserves the K R envelope.

Canonicalize once at each transform output:

    z = (x & (R-1)) - (x >> r).
    if z < 0: z += Q
    elif z >= Q: z -= Q

For |x| <= K R, the first line gives -K <= z <= R+K-1. The root constraint implies r >= K/2. For powers of two K >= 2, 2^(K/2) >= K, hence R >= K. Consequently -Q < z < 2Q; at most one correction suffices. This includes negative x and x at either endpoint of the envelope.

Both forward transforms return canonical residues before pointwise multiplication. Their products are at most R^2. One ordinary product fold, followed by one addition of Q if negative, produces the canonical product. The inverse returns the exact convolution coefficients under the original bound Q > min(Lx,Ly)*(base-1)^2 and the original zero-padding requirement.

This procedure applies unchanged to the original matrix factorization: each axis has the same stage envelope, cross phases are signed shifts that preserve it, and the two axis lengths multiply to K. The executable uses the vector factorization to isolate the reduction change.

## 4. Counts, charged complexity, and measurements

Let F(K) = K*ell/2-K+1. Across two forward and one inverse transforms:

- Both modes perform exactly 3*K*ell butterfly additions/subtractions.
- Both modes perform 3*F(K)+K nonidentity root actions, counting inverse scale.
- Both modes perform K native general integer products in the pointwise step.
- The matched canonical mode makes 3*K*ell+3*F(K)+K = (9/2)*K*ell-2K+3 canonicalization calls inside and after transforms.
- The lazy mode makes just 3K boundary canonicalizations. Pointwise folding is identical in both modes and is not counted under this name.

The matched canonical mode uses conditional correction after ordinary addition/subtraction. It does not pay an unnecessary split-fold after those additions. Modulus and mask are cached in both modes. During timing, counters and peak-width scans are disabled.

The extra guard width is explicit. Summing stage widths gives

    O(K * sum_(t=1)^ell (r+t))
      = O(K r ell + K ell^2).

Since r >= K/2, the extra term is dominated in this family. For m approximately sqrt(N), K and r are Theta(sqrt(N)), so the transform cost remains Theta(N log N) in the full-width evaluation model. The same remains true for the logarithmically skewed family in section 5. Conditional-correction elimination is not elimination of the charged full-width addition itself.

Validation completed:

- 6,831 signed-shift cases, including negative multiples, exceptional residue R, and negative exponents
- 420 defining-DFT and inverse cases, including composite Q and boundary vectors
- 576 exact integer-product cases in binary and Mersenne positional radices
- Every measured convolution compared with an independent direct coefficient convolution outside its timed interval

Fixed configurations and median convolution time:

| K | m | r | Canonical ms | Lazy ms | Ratio |
|---:|---:|---:|---:|---:|---:|
| 64 | 192 | 416 | 0.566416 | 0.494632 | 1.1451 |
| 128 | 384 | 832 | 2.086731 | 1.659764 | 1.2572 |
| 256 | 768 | 1664 | 6.314346 | 5.337873 | 1.1829 |
| 512 | 1536 | 3328 | 22.348526 | 20.633895 | 1.0831 |

These are 15 calls per mode per configuration: five deterministic held-out random digit pairs times three repetitions, with matched modes randomly interleaved. Digit radix is 2^m-1, and the transform length is exactly twice the input digit length. No historical timing or native-Python superiority claim is imported. Full conversion and final positional evaluation are excluded from these convolution timings. In particular, this does not prove the same percentage gain for a complete multiplication application.

At K=256, canonicalization calls drop from 8,707 to 768, while additions remain 6,144 and root actions remain 2,563. Measured peak absolute bit length rises from 1,664 to 1,672, within the proved bound.

## 5. A concrete representation for genuine stage batching

This is an additional constructive direction. The fresh coefficient_lift.py implements and validates this representation, but its ordinary layer loop is not a fast collective-layer algorithm. It was inspected before execution and imports only the fresh companion kernel and standard-library modules.

Because r is a multiple of K/2, set

    d = K/2,    w = r/d = 2r/K,    B = 2^w.

Lift each canonical residue below 2^r to its d radix-B digits, viewed as a polynomial A(Y) in

    P = Z[Y] / (Y^d+1).

The exceptional canonical residue 2^r=Q-1 must instead be represented by the constant polynomial -1. Treating it as d zero digits would be wrong. Every initial coefficient therefore has absolute value at most B-1, including this exception.

Evaluation Y=B defines a ring homomorphism from P to Z/(2^r+1). The root omega=2^(2r/K) is represented by Y. Thus every twiddle is a signed cyclic permutation of polynomial coefficients; no large coefficient multiplication is needed. The whole transform can be performed by coefficientwise additions/subtractions and these signed permutations. Evaluation at the end gives exactly the original Fermat-ring transform. An inverse normalization can be performed after evaluation, since K is invertible modulo Q.

At stage t, an unnormalized coefficient has magnitude at most 2^t*(B-1), so it needs O(w+t+1) bits. Equivalently, normalized butterflies H0(u,v)=((u+v)/2,(u-v)/2) keep coefficient magnitudes bounded, but exact dyadic denominators require the same t additional bits. Merely calling the butterflies contractive does not erase these precision bits.

The stored volume is

    V_t = O(K d (w+t+1))
        = O(Kr * (1 + (t+1)/w)).

For the prototype's balanced m=Theta(sqrt(N)) parameter family, w=Theta(1), so carrying the entire exact coefficient lift to t=Theta(log N) costs O(N log N) bits rather than O(N). That defeats a naive linear-volume claim.

There is, however, a useful exact fix within the same route: choose

    m = Theta(sqrt(N log N)),
    K = Theta(sqrt(N/log N)),
    r = 2m + O(K + log N), aligned to a multiple of K/2.

Then w=Theta(log N), Kr=Theta(N), and t <= log K=O(log N). Therefore the live-layer volume V_t=O(N) throughout the transform, with every polynomial coefficient having O(log N) bits. Stage buffers are overwritten or exchanged, so only a constant number of layers is retained. Storing every historical layer would instead require O(N log N) bits. This avoids any appeal to unit-cost unbounded integer operations. It is an exact, linear-live-volume, small-coefficient representation, suitable for investigating simultaneous layers.

Entry conversion is also charged: read each canonical residue once as bytes, then extract each w-bit chunk using a bounded byte slice with at most one extra overlapping byte. Advance the byte cursor and its three-bit offset by precomputed quotient/remainder increments for w/8; do not recompute w*j at every chunk. This costs O(r+d) data work per residue. Cursor/index additions cost O(log r) each, adding O(d log r), which remains O(r) when w=Theta(log N). The executable uses this bounded-slice and incremental-cursor method, not repeated shifts of an r-bit value or repeated index multiplication. The exceptional residue uses the constant representation just described. This statement concerns conversion from canonical ring residues into the coefficient lift; it does not make original binary-to-Mersenne positional conversion free.

Boundary evaluation can also be linear in this volume. For signed coefficients c_j, propagate a radix-B carry by

    t_j = c_j + carry;
    digit_j = t_j mod B;
    carry = floor(t_j/B).

Pack the bounded digits in one streaming pass. The final carry multiplies B^d, which equals -1 modulo Q, so subtract it and perform bounded final folding. Coefficients and carries are O(w+log K) bits. Charge O(d(w+log K)) per residue and O(N) overall under the skewed parameters. Growing Horner evaluation would not justify that bound and is not proposed.

What is still missing is a routine that applies s successive transform layers and their controlled signed permutations to this representation in

    O(V s^beta + V),    beta < 1,

uniformly for a growing s, with all rearrangements, carries, and boundary changes charged. The ordinary layer loop costs O(Vs). Direct expansion of a 2^s-point block costs O(V*2^s), which is worse. A lookup proposal must charge table construction, addressing, input transposition, and output volume; treating them as free would simply move the missing lemma elsewhere.

Thus this section supplies an exact data representation and a specific parameter choice. It does not supply the requisite sublinear-in-s batch algorithm. The fresh representation validation passed 768 lifted-transform comparisons against the direct residue kernel and 384 independent signed-carry evaluations, including non-byte-aligned w and exceptional canonical inputs. The inverse validation uses a charged native boundary scale only as a correctness oracle; an implementation can use the signed root action already proved above. The parameter table in lift_results.json uses a certified Mersenne digit bound L=ceil(N/(m-1)); it stores only integer parameters, not exponentially sized test inputs.

## 6. Why two tempting precision shortcuts fail in their naive forms

First, modular halving is not a contraction of canonical integer magnitude. In Z/(2^r+1), the residue 1 divided by 2 is 2^(r-1)+1. Small input magnitude can therefore become essentially full width after a normalized modular butterfly. A contractive real/dyadic analysis cannot be transferred to canonical residues without a representation proof.

Second, approximate coefficient lifts cannot simply use a short fixed precision and then evaluate at B. An error delta in the coefficient of Y^(d-1) contributes delta*B^(d-1) to ordinary evaluated value. A worst-case absolute-error argument ensuring less than 1/2 after this step needs |delta| < 2^(-(r-w+1)). Such a rule would require almost r precision bits per coefficient and destroy the linear-volume gain. This is an obstruction to this naive evaluation-and-rounding argument, not to all structured or correlated-error schemes. Exact coefficients with the preceding width bounds avoid it.

A variable-modulus ladder has an analogous issue: there is no unital ring homomorphism from a smaller modulus Z/qZ into Z/QZ with Q>q preserving integers, because q=0 would force q=0 modulo Q. Early reduction to a smaller modulus loses information unless a reconstruction side channel or a valid restricted-domain invariant is supplied. Initial digit vectors are structured, so this is not a universal lower bound on every compressed algorithm for those vectors.

## 7. The independent recursive-product condition

Even a proved layer batching bound would not by itself settle multiplication. In an idealized fixed-ratio recurrence

    T(N) = a(N) T(b(N)) + O(N*(log N)^beta),
    b(N) = approximately sqrt(N),
    a(N)*b(N)/N = rho,

normalizing by N and writing v=log N gives U(v)=rho*U(v/2)+O(v^beta). This implies the following upper bounds: O(v^beta) when rho<2^beta; O(v^beta*log v) when rho=2^beta; and O(v^(log_2(rho))) when rho>2^beta. With a matching positive Theta(v^beta) toll and the usual positive bounded-size base cost, these become matching Theta solutions. An O-toll alone does not establish those lower bounds. The independent leaf-mass argument below concerns the specified complete recursion and does not infer a lower bound from its O-toll.

For the zero-padded ordinary product, K approximately 2N/m and r approximately 2m, hence Kr approximately 4N before rounding: rho approximately 4. Even if the transform toll were reduced below N log N, independently expanding these pointwise products reproduces a log-squared-type obstruction in that idealized recursion.

The native negacyclic modular variant can reduce the child-volume ratio toward 2; that is a separate useful improvement. But with an exact constant rho=2 and square-root children, its leaf mass is already Theta(N log N), even if every internal transform were free. A literal sub-N-log-N result therefore needs a further saving in shared pointwise products, in the recursive expansion schedule, or in the cost of its leaves.

A convenient sufficient condition is a uniform rho <= 2-epsilon together with beta<1 and child size O(sqrt(N)*polylog(N)). Choose gamma with max(beta,log_2(rho)) < gamma < 1; induction on T(N) <= C*N*(log N)^gamma then closes for sufficiently large N. This is a sufficient condition, not a universal necessity: a scale-dependent rho approaching 2 from below can accumulate a smaller logarithmic saving. The general missing condition is that the fully charged total leaf mass and internal costs are o(N log N).

It would be invalid to assert an unconditional lower bound by declaring all transformed children independent. The transformed data come from a structured image with only the original input's information content. A genuine shared-product representation might exploit that structure. No such routine or bound has been supplied here.

Complex conjugacy does not automatically halve these Fermat-ring products. Every unital automorphism of Z/QZ fixes 2, and consequently fixes its powers; it cannot generally map omega to omega^(-1). A real-FFT symmetry must be proved for a different representation rather than assumed from complex FFTs.

## 8. Relation to the cited 2026 preprint and stopping point

The [cited introduction](https://github.com/openai/math/blob/main/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/00-introduction.tex) describes separate collective arithmetic and address-movement procedures. Its stated construction is substantially more than replacing a residue loop, and its ultimate ring products use an established multiplication subroutine. Its theorem is not adopted as a black box here; its full proof has not been independently audited in this task.

The honest deliverables are: an exact tested lazy kernel, a matched finite gain, a signed-negative-fold proof, a concrete O(N)-volume coefficient lift with a workable parameter skew, and explicit batch/recursive-mass lemmas that remain open for this proposed route. No claim of a new little-o(N log N) algorithm is made.

Reproduce the fresh experiment:

    python lazy_fermat.py > results.json
    python coefficient_lift.py > lift_results.json

All code, raw results, and this report are in this directory.

Review correction: the chunk reader now uses an incremental byte/bit cursor, and the recurrence paragraph separates upper bounds from matching-toll solutions. The affected lift validation was rerun successfully. SHA256SUMS_pre_review.txt preserves the preceding file bindings; SHA256SUMS.txt seals the corrected artifacts and that historical manifest. The convolution kernel and its recorded timings are unchanged.
