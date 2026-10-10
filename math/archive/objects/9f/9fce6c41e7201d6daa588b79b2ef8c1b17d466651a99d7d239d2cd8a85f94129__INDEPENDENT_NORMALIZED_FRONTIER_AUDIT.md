# Independent audit: normalized packet frontier and selected convolution

## Verdict

**Accepted within the explicitly restricted models and interfaces stated in the target.** No substantive correction is required to the normalized recurrence, complete-bank ancestor lemma, orthonormal frontier, paid `O(NL)` interconversion, linear-time mask preparation, integer-triangular chirp reduction, constructive `O(L)` modulation cover, or simultaneous-unitary entropy bound.

The target does **not** supply a sub-`N log N` selected-convolution algorithm, a complete fast Fourier algorithm, a constant-size cover, or a universal normalized Fourier lower bound. Neither does this audit. Its graph obstruction remains graph-specific. Its entropy obstruction requires simultaneous unitary realization. The accepted predecessor's unnormalized determinant theorem cannot be reused for this normalized interface.

There is a useful **strengthening, not a correction**: a single selected interval at depth `n` forces all `N` graph nodes at each depth `1 <= j <= n-2b-1`. Thus the fixed-recurrence lower bound improves to

    number of required non-input nodes >= N(n-2b-1).

The extension worker identified this interval; the argument and finite controls below independently verify it. The sharpening changes neither the permitted algorithm model nor the unresolved constructive task.

### Inspected inputs and independence

- Target: `normalized_packet_escape_0358/NORMALIZED_PACKET_ESCAPE.md`
- Target SHA-256: `4cf8e9936c6ff131769b212536f28b022892416346065bc12f1831e8f3395c14`
- Accepted actual-source predecessor: `constrained_packet_independent_audit_0342/INDEPENDENT_CONSTRAINED_PACKET_AUDIT.md`
- Predecessor SHA-256: `bf520e2fe8c328bfc207b67b299074dc37cd1035172e6036d576f45a7f86124e`

Both reports were read in full. No supplied or predecessor program was executed, imported, or used as a code template. The fresh standard-library verifier in this directory reads no input files. Input-directory hashes are recorded before and after; the target's and predecessor's actual manifests are checked separately. Finite controls corroborate the all-size arguments, rather than substituting for them.

## 1. Exact recurrence and distinct graph nodes

Let `N=2^n`, `M=2^(n-h)`, `a=2^(h-1)`, and `f=f0+sigma a`. The packet is

    p[h,q,f] = 2^(-h/2) sum_(s=q mod M) omega^(sf) x_s.

Split its sources into `s=q mod 2M` and `s=q+M mod 2M`. Since `2Ma=N` and `Ma=N/2`, the extra factor `omega^(s sigma a)` is respectively `omega^(q sigma a)` and `(-1)^sigma omega^(q sigma a)`. The ratio of normalization factors is `1/sqrt(2)`. Consequently the target's exact recurrence is correct:

    p[h,q,f] = omega^(q sigma a)/sqrt(2)
                 * (p[h-1,q,f0] + (-1)^sigma p[h-1,q+M,f0]).

The phase cannot generally be dropped. For example, `N=4,h=1,q=1,f=1,x=e_1` requires `omega/sqrt(2)`, while omitting it gives `1/sqrt(2)`.

For fixed `q,f0`, the two rows of the butterfly matrix are `(1,1)/sqrt(2)` and `omega^(qa)(1,-1)/sqrt(2)`, hence are orthonormal. Different `q` values have different supports. At fixed `q`, two canonical frequencies differ on the support by a nonconstant character, unless they are equal modulo `2^h`, which canonicality excludes. Different depths have different support cardinalities. Scalar-phase copying therefore does not identify distinct packet nodes. This argument does not prohibit algebraic elimination or another factorization which declines to materialize those nodes.

## 2. Complete-q closure, density, and the stronger interval witness

For a collection `S` of complete banks with depths at least `H0`, write

    E = union_(h,f in S) {ell : ell=f mod 2^h}.

A bank's first reverse step reduces its frequency modulo `2^(h-1)` and splits every residue class into its two children. Starting with every `q` makes the resulting child bank complete. Iteration proves, exactly, that the depth-`j` ancestor set for `j<=H0` is

    {(j,q,a) : a in {ell mod 2^j : ell in E}, 0<=q<N/2^j}.

Each reduced label has at most `N/2^j` preimages in `E`. Thus each such layer contains at least `|E|` ancestors. The predecessor's adjacent-marker placement supplies `|E|>=N/4096` in the high-time window, with no extrapolation from finite experiments. Therefore the target's node bound `N(n-L)/4096` is valid. Counting two-output butterflies instead of single constructed scalar nodes changes the bound by at most a factor of two.

Complete-q inclusion is essential. At `N=4`, a lone requested node `(h,q,f)=(1,0,0)` has only the input ancestors `q=0,2`, not all four inputs. The verifier includes this failed incomplete-bank alternative as a negative control.

### Stronger graph-only bound

The allowed word `k=1` occurs at `t=1,h=n`. Its selected frequency labels form precisely the aligned interval

    I = [2^(n-b-1), 2^(n-b-1)+2^(n-2b-1))

coming from the `n`-bit pattern `0^b 1 0^b [arbitrary]`. This entire depth-`n` bank is included in the target's high-time bank. Its length is `2^d`, where `d=n-2b-1`, and its starting point is divisible by `2^d`. Hence for every `j<=d`, the projection of `I` modulo `2^j` contains all `2^j` labels. The ancestor lemma applied to this subset alone gives `N` ancestors at each such depth. Summing over non-input depths yields `Nd`.

At the accepted asymptotic choice, `b=O(log n)`, so this is `(1-o(1))Nn` required scalar nodes. It still does not lower-bound an unrestricted linear circuit, a fused multistage operation, a selected-convolution oracle, or a different butterfly factorization.

## 3. Orthonormal antichain and the exact Fourier formulas

Cylinders defined by congruence modulo powers of two are laminar: compatible residues yield containment; incompatible residues yield disjointness. Remove every selected cylinder strictly contained in another selected cylinder. The remaining cylinders are disjoint and have union `E`.

A bank at `(h,f)` has `M=N/2^h` disjoint-support, unit-norm rows. With the positive-sign unitary Fourier convention

    ybar_ell = N^(-1/2) sum_s omega^(s ell) x_s,

the target's two transforms are exactly

    p[h,q,f] = M^(-1/2) sum_v omega^(-qv2^h) ybar_(f+v2^h),
    ybar_(f+v2^h) = M^(-1/2) sum_q omega^(qv2^h) p[h,q,f].

Indeed the first sum's coefficient on `x_s` vanishes unless `s=q mod M`; in that residue class its factor is `M/sqrt(MN)=2^(-h/2)`. The inverse follows by character orthogonality. There is no missing factor `omega^(qf)` in these formulas.

It follows that each bank spans exactly its cylinder's Fourier subspace. Different antichain banks are orthogonal, even where their source-domain supports intersect, because their Fourier subspaces are disjoint. Consequently `WW*=I_m`, with

    m = sum_(h,f in A) N/2^h = |E|,     N/4096 <= m <= N.

The construction removes redundant representations of the same subspace, not independent source information. The ambient input dimension remains `N`.

## 4. Paid conversion and preprocessing

Every high-time bank has `n-h<=L`. Its q-transform requires `O(M(log M+1))` scalar work, including reads, phases, and writes. Summing over antichain banks costs `O(m(L+1))=O(NL)`.

At a fixed time at most `r=N/2^b` retained-coordinate rows are requested. There are `L+1` times in the high-time window. Thus

    D_hi <= r(L+1) = N(1/2+2^(-b)).

Applying the bank conversion to every selected bank costs `O(D_hi(L+1))=O(NL)`. Alternatively, refine antichain banks forward with the checked butterflies: the total live dimension stays at most `m` at each depth, and there are at most `L` refinements. Save requested rows as encountered. That costs `O(mL+D_hi)`. Extracting antichain rows from the original high-time bank costs `O(m)`.

All these estimates pay for existing inputs to the conversion. None computes Fourier coefficients for free. The equivalence is an additive-cost reduction between the high-time normalized bank and the explicit partial Fourier transform on `E`.

### Why the mask really can be prepared in O(N+n)

A direct `n`-bit scan for each frequency would be too expensive. The target's stated two-pass trie method avoids it:

1. Traverse the ordinary MSB-reading binary trie, containing fewer than `2N` nodes through depth `n`. Maintain the initial-zero count, whether the mandatory first `1` was seen, the current zero-run length, and the number of bits since the initial marker. The first following run of `b` zeros determines the unique candidate `k`. Check its length against `L`, then retain an accepted/dead flag for descendants. These counters fit one address word each and update in constant work per node. Apply the high-time depth condition separately.
2. Store selected flags indexed by `(h,f)`. Traverse the different low-bit trie whose parent is `(h-1, f mod 2^(h-1))`. A selected-ancestor flag identifies the antichain. The syntax trie's parent is instead `(h-1,floor(f/2))`. They must not be conflated.

The independently written automaton agrees with a literal pattern predicate for every enumerated node in its finite controls. The two passes use `O(N)` words and `O(N+n)` word-address work. Root/phase and normalization tables use scalar recurrences with the same or smaller preparation order. This is a scalar-arithmetic plus word-routing statement, not a bit-complexity statement.

For `b=floor(log2(n/(4 ln n)))`, eventually

    n/(16 ln n) < L <= n/(8 ln n).

Hence `L=Theta(n/ln n)=Theta(log N/log log N)`, and the paid conversion is `O(Nn/ln n)=o(Nn)`.

## 5. Integer-triangular chirp: exact indices and root requirements

For all integers `s,ell`, including negative `ell-s`, the identity

    s ell = s(s-1)/2 + ell(ell+1)/2 - (ell-s)(ell-s+1)/2

is an integer identity before reducing exponents modulo `N`. Define

    a_s = x_s omega^(s(s-1)/2),                         0<=s<N,
    b_(N-1+t) = N^(-1/2) omega^(-t(t+1)/2),  -(N-1)<=t<=N-1.

In the ordinary product of lengths `N` and `2N-1`, the coefficient at `N-1+ell` has kernel index `N-1+ell-s`. Thus multiplying it by `omega^(ell(ell+1)/2)` gives `ybar_ell` exactly. The product length is `3N-2`; all requested indices `N-1+E` are inside it.

The chirp diagonals require only powers of the supplied `omega` and normalization using the already permitted `1/sqrt(2)`. The exponent division by two occurs on even integers; it is not division in an exponent group, nor a hidden choice of a `2N`th root. Successive chirp ratios are successive powers of `omega`, so preparation takes `O(N)` field operations.

A whole-product FFT with length `4N` would need further roots. The target explicitly does not hide that implementation requirement. There is also a straightforward way to avoid it altogether without improving complexity: split `a` into two blocks of length `N/2`, and `b` into four such blocks, with the last block possibly shorter. Each of the eight block products has length at most `N-1`, so an `N`-point convolution using only `omega` suffices. Reassemble at offsets `(i+j)N/2`. This proves an `O(N log N)` scalar implementation with no larger-root extension. It is not a faster selected-coefficient algorithm; a bounded-coefficient realization must additionally account for the sizes of its fixed spectrum multipliers, just as the target requires.

The familiar FFT/convolution background is described in [AMD's primary Bluestein design documentation](https://rocm.docs.amd.com/projects/rocFFT/en/docs-6.3.0/design/bluestein.html). The triangular identity and block observation above are checked directly here.

Therefore the conditional bound

    cost(H_hi x) <= T_E(N) + O(NL+N)

is valid if `T_E` counts the exact fixed-kernel selected convolution in the same declared computational model, including constants and preparation. Defining such an oracle does not establish that it is sub-`Nn`.

## 6. Constructive modulation cover and its actual cost

Let `Q=2^L`, and let `T` consist of top-block words containing `1 0^b 1` in each half. The accepted predecessor proves `|T|/Q=alpha>=1/4096`; using consecutive long zero runs makes this a valid subset of the target mask. The two half-events are independent because they concern disjoint bits; overlapping occurrences within a half are treated by the predecessor's exact second moment, not assumed independent.

For any uncovered set `U` in the cyclic group, the average over translates `a+T` of `|U intersect (a+T)|` is exactly `alpha|U|`. Greedily select a translate with at least that average. After `k` steps the uncovered count is at most `Q(1-alpha)^k<=Q exp(-alpha k)`. Thus `ceil((ln Q+1)/alpha)=O(L)` steps suffice. Testing every translate by direct membership costs at most `O(kQ^2)=2^O(L)` word operations. At the marker choice this is `N^o(1)`, not an uncharged search.

Set `B=N/Q`. Each shift by `aB` modulo `N` changes only the top-block label and preserves the lower `B`-block coordinate. Modulating the input by `omega^(aBs)` shifts the output labels accordingly. The sign can be chosen to match either translation convention; both cost one diagonal modulation. Each call pays `O(N)` routing and modulation work.

Accordingly a partial Fourier oracle has total full-transform cost `O(kT(N)+kN+2^O(L))`; a high-time packet oracle has the additional `O(kNL)` conversion. These equations do not imply a sub-`Nn` full transform from an arbitrary sub-`Nn` partial oracle. No constant translation or affine cover is established. Density alone is insufficient for that inference, and arbitrary frequency-bit permutations are not justified source permutations.

## 7. Simultaneous unitary realization, with ancillas

The model restriction in [Ailon's 2013 primary paper](https://arxiv.org/pdf/1305.4745) was checked directly: its operations are two-register unitary gates, not arbitrary bounded-coefficient linear operations.

For a full unitary coefficient matrix, use the sum of row entropies of squared magnitudes. It starts at zero. In one gate, each column's mass in the affected two rows is preserved; splitting that mass between two entries changes entropy by at most the mass. Those column masses sum to two. Thus each gate raises potential by at most two bits.

Every final frontier row at depth `h` contributes `h>=n-L`. Other rows contribute nonnegative entropy. Hence simultaneous realization requires at least `m(n-L)/2` gates. Zero-initialized ancillas do not weaken this: a requested row already has original-input coefficient norm one, so unitarity forces all its ancillary formal-input coefficients to vanish.

The conclusion fails to cover a free historical output tape, unrestricted copies, or nonunitary intermediates. The target preserves those boundaries. No more general well-conditioned theorem is invoked in this audit.

## 8. Fresh exact controls and final scope

`independent_frontier_controls.py` uses only the Python standard library. It compares literal source sums against normalized recurrence evaluations over `GF(65537)` with an explicitly verified square root of two and primitive-root order; it separately checks root exponents symbolically for complex primitive roots. Exact power-of-two cyclotomic reductions establish the finite antichain Gram controls. Modular tests do not establish complex positivity or a finite-field lower bound.

Coverage and exact totals are recorded in `INDEPENDENT_CONTROLS.json`. They include complete input bases through `N=16`, two root embeddings, antichains with genuinely nested requested cylinders, literal-versus-automaton mask checks, independently enumerated dependency closure, triangular convolution and block-product reconstruction, top-block placement, exact rational second moments for `b=7,...,256`, greedy covers on separately stated small windows, and the stronger interval projections. Five negative controls catch a missing recurrence phase, missing butterfly sign, incomplete-q closure, the wrong trie parent, and a missing chirp output phase.

Small marker parameters are deliberately used for exhaustive identity tests; they do not satisfy all asymptotic density hypotheses and are not presented as instances of that theorem. The all-size proofs above and the accepted predecessor establish the asymptotic claims.

`CONTROL_SNAPSHOT.json`, `EXACT_RUN.log`, `EXACT_REPLAY.log`, and `REPLAY_CHECK.log` witness deterministic byte-for-byte replay. Input hashes and input-seal checks verify preservation. `AUDIT_SHA256SUMS.txt` seals the report, independent program, controls, and preservation records. The manifest cannot seal itself; its own digest and verification are recorded separately.

**Final scope:** the high-time normalized bank has a sound, well-conditioned, `O(NL)` transition to a concrete selected Fourier/chirp problem. Ordinary packet-graph pruning is asymptotically insufficient, with the sharpened bound above. Simultaneous unitary realization is also insufficient for sub-`Nn` work. A genuinely different selected-convolution or frontier algorithm remains unprovided, and early-time outputs, causal inverse construction, full recovery, and any finite-precision encoding costs remain separate obligations. No novelty conclusion is drawn.
