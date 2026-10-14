# Exact-width H16 finite-win admission and all-length DFT lift

Date: 14 October 2026. Status: conditional interface audit; no 31-call word has been supplied or established.

## Decision

The proposed finite target is appropriate: an exact word for H2 tensor-powered four times on exactly 16 arbitrary registers, using at most 31 forward H2 calls and invertible monomial factors, is a strict finite win. The second required word, an exact unit shear on two registers, is already explicit and independently checked below.

The source appendix's bounded-printer theorem alone concludes only uniform all-length o(n log n). It does not furnish a rate that can be compared to exponent 0.9991237522. However, for an admitted fixed word with usable exact coefficients, the appendix's tensor recurrence can be combined with the same paper's explicit local compiler, linear sector traversal and all-length reduction. That stronger, fully charged conditional route gives

    O(n (log n)^(199/200) (log log n)^(601/200)),

and hence eventual O(n (log n)^(997/1000)). The exponent 0.997 is below the specified matched baseline 0.9991237522. This is a conditional consequence of a future word, not a new unconditional Fourier bound or a claim that the word exists. The general mechanism and the same rational exponent choice were already recorded in the prior exact-width research notes.

## 1. Exact admission interface

Let H = [[1,1],[1,-1]], with no normalization. Number the 16 input coordinates by four-bit strings. The target matrix is T[a,b] = (-1)^(a dot b), where the dot product is modulo two. A candidate must provide:

1. A chronological list with exactly the same 16 logical registers throughout. Each counted call applies H to an explicitly ordered pair of distinct registers and leaves the other 14 unchanged. The budget is g <= 31, not 31 scalar arithmetic operations.
2. Every intervening and endpoint monomial: an explicit bijection of the 16 coordinates and one proved-nonzero scaling per coordinate. Identity entries may be compressed by a specified finite convention. No projection, addition, singular diagonal, overwrite, unrecorded fan-out or nonmonomial map can be hidden in a monomial slot.
3. A finite exact description of every coefficient, with every inverse/division justified. Rational or Q(i) coefficients are the simplest admission path. Floating-point residuals, fitted decimal constants or heuristic equality tests are not an exact certificate.
4. The full 16-by-16 identity, replayed on the 16 independent basis inputs. The test must account for chronological multiplication order, pair orientation, normalization and endpoint routing. Equality on selected vectors or a restricted input distribution does not suffice.
5. Independent replay plus negative controls for a changed coefficient, pair, normalization and omitted call. A search program's success flag alone is not acceptance.
6. No additional register, whether clean or dirty, is part of this 16-register word. A word using and restoring an extra arbitrary register is a different interface. A construction working on repeated/equal input values is not this interface either.

All placements can alternatively be absorbed into adjacent monomials, giving T = M0 Y M1 ... Y Mg, Y = H direct-sum I14. The matrices Mj must remain invertible. Since H^(-1) = H/2, an inverse-H notation can be converted to one forward call plus explicit scalings; it cannot conceal an uncharged operation.

A useful necessary diagnostic is det(T) = 2^32. With exactly 31 H calls, product_j det(Mj) = -2. This diagnostic does not prove the identity. In particular, invertible monomials are not restricted to phases or bounded magnitudes.

The exact word has width 16 even if its implementation uses address metadata or a paid movement buffer. Such implementation storage must not become extra mathematical inputs or uncharged auxiliary values in the finite identity.

## 2. The second certificate is explicit

The general synthesis interface also requires a positive-call word for U = I2 + E12 using the same kernel. For any nonzero t,

    U_t = diag(-t/10,-1/6) H diag(2,1) H diag(-3,1) H diag(5/(4t),1)
        = [[1,t],[0,1]].

This follows by multiplying H diag(2,1) H diag(-3,1) H = [[-8,-10],[0,-6]]. It uses three forward H calls, exactly two arbitrary registers and invertible rational diagonals when t is nonzero rational. The t=1 word supplies the required finite certificate without further search.

The same formula works for any nonzero complex t. For a local Fourier shear coefficient mu that might vanish, prepare t1 = 1 + mu*conjugate(mu), t2 = mu-t1. Both are nonzero and U_t1 U_t2 = U_mu. The conjugate coefficient is prepared by evaluating the coefficient's shared arithmetic DAG at inverse roots; no conjugation of variable input data or complex-zero oracle is used. Thus all local shear layers have one fixed six-H slot pattern, including zero coefficients. This is the source's local compiler with its H kernel used directly.

## 3. Fully charged fixed-word tensor amplification

This is the quantitative bridge needed in addition to the generic slow-printer theorem. Suppose the fixed candidate passes Section 1. Put Q=16 and j=floor(k/4). Tensor each finite-word slot across j groups and handle the remaining at most three binary axes by the usual H calls. A call slot is

    (H direct-sum I14) tensor-powered j
      = direct sum over r=0..j of H tensor-powered r,
        with multiplicity binomial(j,r)*14^(j-r).

There is no sector padding. A sector with r active factors has exactly 2^r coordinates, and the sector widths sum to 16^j. After including the leftover axes, the total logical width is exactly 2^k.

The permutation and diagonal factor in each tensor monomial can be applied using a mixed-radix depth-first traversal. Maintain the original address, image address and running scaling while extending one digit. A constant number of operations per prefix suffices. Because the radices are at least two, the total number of prefixes is less than twice the number of leaves. All scalar products of local diagonal entries are charged; they are not separately recomputed by scanning every axis at every leaf.

Similarly, pack each call slot's sectors, enumerate their contiguous starts and widths, recursively process them, then unpack. The source's sector-start rule uses local block widths q_i in {1,2}, preceding block-coordinate counts p_i and suffix radix products tau_i:

    S = sum_i (product_{h<i} q_h) p_i tau_i.

The traversal updates this state in constant work per prefix. Identity-only axes and width-one sectors remain charged. The number of call and monomial slots is fixed. Consequently all nonrecursive work for the invocation is O(2^k), including routing, coefficient products, copying and invocation descriptions. Metadata depending polynomially on k can also be absorbed in O(2^k) for sufficiently large k; bounded k is a finite base case. The algorithm generates the recurrence directly rather than invoking an unbounded printer for each growing radix.

If f(k) is the full running time divided by 2^k, this gives

    f(k) <= C0 + g E[f(K)],   K ~ Binomial(floor(k/4), 1/8).

The binomial distribution is exact dimension-weighted accounting of all sectors, not randomized execution. Its mean is floor(k/4)/8 <= k/32. Concavity gives E[(K+1)^alpha] <= (1+k/32)^alpha. If g*32^(-alpha)<1, a standard induction absorbs C0, after enlarging the leading constant for the finite base range. Hence f(k)=O((k+1)^alpha).

For g<=31, the critical threshold is log(31)/log(32)=0.990839262077375... . Strict inequality above this threshold is needed for this induction; this audit does not claim the endpoint exponent. Take alpha=199/200. The exact integer certificate is

    31^200 < 32^199.

No numerical logarithm is used in this acceptance decision. It yields a uniform, fully charged H tensor-power routine of cost O(2^k (k+1)^(199/200)). A fixed 31-versus-32 saving in an ordinary blocked FFT would only change a leading constant; it is the recursive active-sector construction above that produces a logarithmic power saving.

## 4. From H tensors to the exact DFT at every length

Use the source's Fourier-layer compiler, which acts on exactly r coordinates. It uses O(1+log^4 r) monomial/shear layers and r^O(1) scalar and integer preparation. Its borrowed coordinates start arbitrary and are restored. In particular, the measured-fit condition counts every gate coordinate inside the existing r coordinates. Padding each local axis to a larger width is not permitted, because a factor of padding on each of many axes would multiply the total volume.

Replace shear layers by the fixed H word of Section 2, and synchronize all axes by identity slots. A simultaneous H slot is a direct sum of H tensor-powered k, k at most the axis count ell. Its sector widths sum to the original product width R. The tensor routine plus linear-time sector packing therefore costs O(R(ell+1)^alpha) per slot. Tensor monomials cost O(R). This gives

    O(R(ell+1)^alpha (1+log r_max)^4)
      + polynomial(ell,r_max,log(R+2))

including local preparation. A tensor identity permits one axis to move values temporarily used as borrowed data by another axis: each local word is correct on arbitrary inputs and each slot is synchronized algebraically. It is not necessary to freeze the other axes throughout a local word.

For requested length n, choose the maximal product R_ell of initial odd primes not exceeding 2n. Multiply it by the least power 2^e making L=R_ell*2^e >= 2n. The source proves

    2n <= L < 4n,
    ell = Theta(log n / log log n),
    r_max = polynomial(ell), and e=O(log(ell+2)).

Find these primes and local schedules using polynomial(log n) work. CRT permutations are performed by the same linear-prefix traversal, not by scanning ell factors per entry. Use the synchronized routine on odd-prime axes and the ordinary small power-of-two FFT on the remaining axis.

Bluestein's identity then reduces F_n to one length-L chirp convolution. Charge all three transforms: variable vector, fixed chirp-kernel preparation and inverse. Padding, chirp tables, pointwise prepared-scalar multiplications and output scaling cost O(n). Inverses use reversal and scaling, so no new inverse primitive is assumed.

Substituting the estimates above gives

    T(n)=O(n (log n)^alpha (log log n)^(4-alpha))
           + polynomial(log n) + fixed setup.

For alpha=199/200, 4-alpha=601/200. The positive gap 997/1000-199/200=1/500 absorbs the fixed log-log power eventually. Thus O(n(log n)^0.997) follows, after a finite initial range handled directly. This proves an all-length exact-complex consequence conditional on the finite word and the stated source compiler interfaces; it is not merely a Walsh transform statement.

## 5. Coefficients, roots, workspace and the matched model

The comparison is in the paper's exact-complex-register model: complex field operations are unit cost; variable-data computation is linear; coefficients and intermediate magnitudes are unrestricted; scalar preparation and schedule construction are charged; integer arithmetic and random access use a fixed number of O(log(n+2))-bit words. It is not a finite-precision, bounded-coefficient, bit-complexity, fixed-tape or practical runtime statement.

For a rational or Q(i) finite word, its finitely many constants are prepared once, with a fixed cost independent of n. The remaining local Fourier coefficient DAGs have polynomial(log n) total preparation because their widths are polynomial(log n). All full-array scalar products and the chirp-kernel transform are charged separately in the main running time. There is no growing lookup table or n-dependent advice.

The explicit master-root order can be the source's

    D_* = (2n) L 2^ceil(log2(16L)) < 1024 n^3.

One supplied canonical root zeta_D* produces all working, chirp and local convolution roots by integer powers. Root extraction work is charged. The root resource must match the comparator: restricting the implementation to arithmetic starting from zeta_n alone is a different model, since required odd-prime roots need not lie in Q(zeta_n).

An exact but non-rational complex certificate needs a separate finite representation argument. The source's extraction lemma can encode the fixed word equations, nonzero witnesses and the fixed rational H target over a nonzero finite-dimensional rational algebra E. Once E and the word are explicitly obtained, use its fixed rational multiplication table and faithful scalar simulation. The dimension of E is fixed before n is known; multiplying by a fixed element costs a constant number of scalar operations. The H kernel and the local Fourier coefficients act centrally. Local coefficient conjugates are prepared before extension to E. This offers a route without supplying an arbitrary algebraic-number oracle, but the actual E table, unit witnesses and word identities must be provided or derived and checked. The safe default admission is an explicit rational/Q(i) word; unknown complex constants are not silently free.

The finite-word hypothesis is exactly 16 arbitrary logical registers. The all-length algorithm is allowed its explicitly charged linear arrays and movement buffers under the matched model. These are separate claims: accepting paid implementation storage does not license clean scratch inside the finite identity. Nor may unused sectors, spectators, register roles, coefficient construction or packing be discarded from the runtime accounting.

## 6. What blocks an unconditional result

- No exact word with g<=31 has been found or delivered to this audit. This is the decisive missing witness.
- The bounded-printer theorem by itself gives o(n log n), which can be slower than every n(log n)^beta for fixed beta<1. It cannot by itself establish the exponent comparison.
- A merely nonuniform H tensor circuit, an uncharged coefficient oracle, axis-by-axis O(R ell) packing or separately padded local axes does not satisfy the quantitative bridge.
- A finite-field identity does not establish the characteristic-zero word. A numerical near-word, low-rank surrogate, limited input family or low scalar-addition count is not the required exact-width certificate.
- A negative result in one topology neighborhood is not a general 31-call lower bound. No such lower bound is asserted here.
- Even after a word is found, the proof should be independently reviewed, and any implementation claim requires the full exact compiler and scheduler to be implemented and tested. The finite controls below do not constitute that implementation or a Lean proof.

## 7. Fresh checks and source binding

Only newly authored control code was executed. No historical downloaded program, build, dependency or external write was used. fresh_contract_checks.py reports PASS for:

- 162 exact rational instances of the three-forward-H shear identity;
- 25 exact binomial sector-mass/mean cases;
- the strict integer exponent inequality and exact comparison of 0.997 with 0.9991237522;
- 1,554 sector-packing configurations covering 111,150 coordinates, including nonconsecutive/reversed pairs and singleton axes;
- 2,509 working-length and polynomial-master-root checks.

The all-size claims are carried by the algebraic arguments and cited source interfaces, not by these finite checks. The historical THEORY.md and README.md in the prior exact-width research were read as context only and were not executed. They already record the same conditional exponent route and a separate bounded topology obstruction.

Primary source snapshot: OpenAI math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a, An explicit power saving for the exact discrete Fourier transform, September 25, 2026:

- [Finite certificate, extraction and amplification](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/synthesis.tex): certificate lines 18–29; amplification subsection; bounded-printer theorem.
- [Exact-width local compiler and three-kernel shear](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/local.tex): uniform compiler, measured fit, Fourier layers and fixed kernel-word subsections.
- [Linear sector traversal and synchronized Fourier tensor](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/synchronization.tex).
- [All-length reduction, charged preparation and master root](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex).
- [Exact arithmetic/address/root model](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/introduction.tex).

## 8. Sussman comparator: primary source checked

The comparison is with jacobalansussman/wht-power-saving-lean at commit 9c94857bbaee886f8649edee0bc2d3c738f9555e, not with a Walsh-only corollary. This audit fetched and inspected these pinned files:

- [UniformFourierChallenge.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/UniformFourierChallenge.lean) defines the exact scalar/index RAM and DFTProgram: one fixed program for every n>0 and every complex input vector, valid preparation divisions, charged order/preparation/execution work, polynomial integer/address bounds, and one supplied canonical root of order below 1024*n^3. It defines decimalExponentE8 = 1 - 8762478/10^10 = 0.9991237522. Its two sorry statements are comparator targets, not the solution proof.
- [Goal.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Goal.lean) imports the original OpenAI DFTProgram and defines the modified exponent and time/DFT goals.
- [Main.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Main.lean) contains the proof body of transform_mainE8 via transform_main_orderE8. The order variant supplies the same all-length DFTProgram and a stronger actual root bound below 8*n^3. The comments explicitly say general rational-algebra extraction, symbolic search and bounded-printer synthesis are outside this formalization.
- [Seam.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Seam.lean) defines alphaE8 = 1 - 8762479/10^10 = 0.9991237521 and gives hillsE8_program for all batches and input modes.
- [Asymptotics.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Asymptotics.lean) defines flightE8 as n*(log n)^alphaE8*(log log n)^2 and bounds the full cost envelope by it. Main then absorbs that log-log factor into the slightly larger final exponent.

These source definitions support the matched model and the distinction between underlying exponent 0.9991237521 and final pure-log exponent 0.9991237522. The conditional 0.997 consequence above is asymptotically smaller than either displayed comparator envelope. This audit did not build Lean, run its comparator, inspect every imported proof dependency, or certify that this pin is the latest world record. It is a direct primary-source theorem/model check.

## 9. Completion state

The parallel fresh construction pass reports that every one of its 1,845,120 labeled delete-two/insert-one modifications of the fixed 32-call schedule fails full reachability, with a second complete independent enumeration agreeing. No candidate word reached exact scalar verification. This reported finite-family exclusion does not change the admission contract and does not imply a general impossibility of a 31-call word. The construction artifact should be reviewed on its own evidence.

Outstanding obligations before any claimed new Fourier exponent are therefore explicit: obtain a different admitted exact word; verify all of its coefficients, inverses and full target identity; bind its actual program to the linear-overhead recurrence and the exact-width Fourier compiler; and independently review the resulting end-to-end argument. Any claimed running implementation or formal theorem additionally needs the corresponding complete implementation/tests or formal build. The present report closes the contract and comparator audit, while keeping the missing-word gate open.
