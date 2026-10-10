# Independent audit: source-constrained exposed packet obstruction

## Verdict

**Accepted within its stated N-input, unnormalized exact-output, bounded-coefficient complex linear model.** The actual-source fusion identity, complete-q-bank Fourier-diagonal Gram, constant-density high-weight construction, Cauchy–Binet count, determinant potential, asymptotic constant, and paid matching-order construction are valid. No substantive correction to the displayed identities or lower bound is required.

The dependence on one original vector is handled correctly: the ambient dimension remains **N**, rather than the dimension of independently supplied retained jets. The conclusion applies to circuits that expose the specified actual young-feedback values as ordinary, unnormalized field values. It does not cover a normalized-only output interface, an implementation that avoids those values, nonlinear or unrestricted arithmetic, or finite-field arithmetic. It is not a universal Fourier lower bound and supplies no faster complete transform. This audit assesses correctness and scope; it makes **no novelty claim**.

The normalization qualification deserves particular emphasis. Normalize each selected time-h row by 2^(-h/2). The Gram eigenvalues then become event counts rather than exponentially weighted event counts. Moreover, every N-row minor of the identity-augmented normalized matrix has modulus at most one. The specific determinant-growth witness used here therefore disappears. This does not demonstrate a fast normalized algorithm.

Audited target: `constrained_jet_fusion_0331/CONSTRAINED_JET_FUSION.md`

Target SHA-256: `f11dd814af83d7f8e3a40240cbd0ad0fc247ffb19776972f12666f8864d52112`.

All target and predecessor programs were treated as inert files. None was executed or imported. The executable in this audit directory was authored independently and uses only the Python standard library. It does not read any target or predecessor file. Mathematical proofs below establish the all-size claims; finite controls are corroboration, not an asymptotic extrapolation.

## 1. Actual N-input paths, phases, routes, and horizon

Write N=2^n, d=n-b, r=2^d, eta=omega^(2^b), and R={2^b a}. The young no-wrap regime is t<=L=2^(b-1) and L+2b<=n. Thus n-(b+t)>=b, the condition used below. The jet formulas are invoked only at h<=n.

For h<=n, an h-step path from source s to target z exists precisely when z=2^h s+w modulo N for an appended word w of length h. The word is uniquely determined by z modulo 2^h. Multiplying actual edge phases gives

    weight = omega^(s rev_h(w)+gamma(w)),
    gamma(2a)=gamma(a), gamma(2a+1)=gamma(a)+a.

For z=2^b a, h>=b, and a=2^(h-b)q+c, the word is w=2^b c. Its reversal is rev_(h-b)(c), and appending b zero bits leaves gamma unchanged. The predecessor class is s=q modulo 2^(n-h), with exactly 2^h terms. This establishes the target's packet formula including its phase, its index quotient, and all source merges.

For the alias, take a=2^(b+t)q+k in S_t and put ell=b+t. Then

    2^b a = 2^(2b+t)q + 2^b k.

Every full-Q predecessor at distance ell equals 2^b q modulo 2^(n-ell). Since n-ell>=b, every such predecessor belongs to R. The appended ell-bit word is exactly k followed by b zeros.

Because k begins with 1, the path initially leaves R. Because k avoids 0^b and ends with 1, no new suffix marker occurs before the final b appended zeros are complete. The original marker remains present throughout all intermediate states within ell<=n-b, so none of those states enters the marker-free retained set A. These are exactly first-return paths through eliminated states.

In the smaller-Q implementation, a t-step path from retained source index s has phase eta^(s rev_t(k)+gamma(k)). C_t multiplies by (omega/eta)^gamma(k), yielding eta^(s rev_t(k)) omega^gamma(k), and routes the intermediate coordinate z to 2^b(z-k)+k modulo r. That route merges precisely the sources s=q modulo 2^(n-2b-t). Thus both paths and phases agree with the full-N first return.

Consequently, within the target's horizon,

    C_t Q_r^t u_j = 1_(S_t) u_(j+b+t).

The sets S_t are disjoint because t is the age of the rightmost completed b-zero marker in the fixed-width d-bit coordinate. Leading zeros are included. The batch is therefore the asserted time-dependent mask of u_h, with no residual cancellation between different ages.

At a selected coordinate with h>=b+t, every h-step backward path encounters an earlier retained visit. A fresh eliminated-only path cannot contribute. The immediate predecessors are eliminated, so neither direct retained term contributes. Substitution into the retained recurrence gives u_h(a)=u_h(a). The alias identifies the needed value but does not compute that value causally from the source.

Independent controls compare three implementations: direct global Q propagation; smaller Q_r propagation with explicit C_t phases and routes; and full-N propagation with every intermediate R or A state killed. Complete source bases are included through N=64. Omitting the C_t phase fails at n=6,b=2,t=2,j=0 in GF(65537), so the phase check is nonvacuous.

## 2. Complete q banks, spectral diagonalization, and exact rank

At h>=2b+t, membership in S_t depends entirely on the c portion of a=2^(h-b)q+c. Hence all M=2^(n-h) quotients q occur independently for each allowed f. Reversal gives

    f = rev_t(k) 2^(h-b-t) + v,
    0<=v<2^(h-2b-t), k in K_t.

In an h-bit word, this is 0^b rev_t(k) 0^b followed by arbitrary lower bits. The h>=2b+t restriction is essential to the complete-q argument; this audit does not silently add the earlier, incomplete banks to H.

For fixed h and f, its M packet rows have disjoint residue-class supports. Each row contains 2^h unit-modulus coefficients, and hence has squared norm 2^h. Their span is precisely the Fourier subspace of frequencies ell=f modulo 2^h. One can verify that span directly from

    P_(h,q,f) = (1/M) sum_v omega^(-q v 2^h) y_(f+v 2^h).

The phase gamma changes each row by a unit scalar and has no effect on its Gram contribution. The complete bank therefore contributes 2^h times the orthogonal projection onto that Fourier subspace. Summing actual selected rows gives exactly

    H*H = F_unitary* diag(lambda_ell) F_unitary,
    lambda_ell = sum_(t=1)^L sum_(h=2b+t)^n 2^h 1_(E_(h,t)(ell)).

No arbitrary independent jet is introduced. Multiple occurrences across h are retained in the sum, so cross-time dependence and overlapping frequency supports are not discarded. At a fixed h, at most one t is possible: a longer admissible separating word cannot contain the earlier completed marker.

The rank is exactly the number of positive lambda_ell over C. Separately, stacking every full retained jet u_b through u_n includes a Fourier direction exactly when an n-bit frequency has an occurrence of 0^b. Its rank is N-a_b(n), as stated; that formula does not automatically extend to another time selection.

Fresh exact controls build H from literal global edge paths, rather than from the packet formula. They verify all q values and all permitted f labels, then compare every entry of N H*H with the claimed diagonal spectral expansion in Z[z]/(z^(N/2)+1). This is exact arithmetic in the power-of-two cyclotomic representation of a complex primitive root, with no floating-point tolerance. Modular rank checks independently verify both H and the complete retained stack in the tested cases.

## 3. Isolated-marker density and correct top-window placement

Let m=L/2=2^(b-2), let P=1 0^b 1, and count its occurrences in one m-bit half. There are a=m-b-1 starting positions, with p=2^(-b-2), so the mean is alpha=ap. For b>=7,

    1/32 <= alpha <= 1/16.

Two copies at positive shift delta are incompatible for 1<=delta<=b. At delta=b+1, their bounding 1s coincide, and their joint probability is 2p^2. At delta>=b+2, the bit sets are disjoint and the joint probability is p^2. In particular, it would be incorrect to treat all overlapping positions as independent; the target does not do that.

An exact second-moment formula is

    E[X^2] = alpha + 4 max(a-b-1,0) p^2
                   + q(q+1) p^2,
    q=max(a-b-2,0).

It is bounded by alpha+alpha^2+4alpha p<2alpha, as used in the target. Thus Pr(X>0)>=alpha^2/E[X^2]>=1/64. The two halves involve independent bits, so the probability of a marker occurrence in each half is at least 1/4096. At the boundary b=7, the exact mean is 3/64, the exact second moment is 787/16384, and the one-half lower bound is 36/787, comfortably exceeding 1/64.

The implication to a selected packet requires adjacent long zero runs, not just an arbitrary pair of pattern occurrences. Each isolated marker occurrence supplies a distinct maximal zero run. Between two witnessed runs, choose consecutive runs of length at least b. The intervening word k is nonempty, begins and ends in 1, and avoids 0^b. Taking the last b zeros of the upper run and the first b zeros of the lower run produces 0^b k 0^b entirely inside the highest L-bit block.

For an explicit coordinate check, number that top block's positions left-to-right starting at zero. If the chosen upper b-zero suffix begins at position a, set h=n-a. The low h-bit word starts at exactly that zero block. Since 0<=a<L, h>=n-L; since the whole selected pattern fits in those h bits, h>=2b+t. Also 1<=t<=L. Reversal of k preserves its endpoint and avoidance properties, so it is one of the permitted labels. Therefore E_(h,t)(ell) holds and lambda_ell>=2^h>=2^(n-L).

This proves at least N/4096 high-weight Fourier directions. The extra unused leading/trailing bits of the full n-bit word do not affect the count. No Poisson heuristic or independence assumption about overlaps is needed.

Fresh controls independently compare bit assignments for every overlapping shift for b=1 through 64, check the exact rational moment inequalities for b=7 through 512, and exhaust short top windows. The exhaustive controls also append arbitrary lower bits and verify the h=n-a placement, guarding against confusing a top-window occurrence with a low-frequency prefix condition.

## 4. Augmented minor count and bounded-coefficient cost

Let D be the actual number of selected rows. Since those rows are selected output-time/retained-coordinate pairs,

    D <= r(n+1).

Appending the original N coordinate rows gives M=[I;H]. These are already input forms, so no new information or independent jet variables are supplied. The spectral identity gives

    det(M*M) = product_ell (1+lambda_ell)
             >= 2^((N/4096)(n-L)).

Cauchy–Binet has exactly binom(N+D,N) candidate N-row subsets, including subsets containing identity rows and zero-valued minors. Bounding the maximum summand by the average is valid even if some minors vanish. Thus some N-row minor has

    log2 |det M_I|
      >= (1/2)[(N/4096)(n-L)-log2 binom(N+D,N)].

The determinant potential is the largest absolute determinant of N coefficient rows ever available. It starts at one. A scalar multiplication of modulus at most one cannot increase it. A binary addition/subtraction creates a row whose determinant with any N-1 old rows is the sum/difference of two old determinants, so one paid addition increases the potential by at most two. Copies, fixed permutations, overwrites, and arbitrary fanout do not circumvent this argument; allowing every historical row only strengthens the circuit model.

Using binom(N+D,N)<=[e(N+D)/N]^N and D/N<=(n+1)/2^b gives exactly the target's bound

    A >= (N/2)[(n-L)/4096 - log2(e(1+(n+1)/2^b))].

A negative finite-size right side carries no information; it is not a positive bound for every small test case. At b=floor(log2(n/(4 ln n))),

    n/(8 ln n) < 2^b <= n/(4 ln n),
    L<=n/(8 ln n),
    (n+1)/2^b=O(ln n).

The young no-wrap conditions hold eventually, L=o(n), and the logarithmic subtraction is O(log log n). Therefore

    A >= (1/8192-o(1)) Nn.

For a larger fixed scalar bound K, a total-gate version uses the fixed per-gate factor max(2,K), rather than retaining an addition-only claim. Constants growing with N require a separate growth budget. Finite fields have no positive absolute-volume analogue of this argument.

Independent Cauchy–Binet controls enumerate every augmented minor through its identity-row expansion, computing the remaining H minor exactly in the cyclotomic ring. The three cases contain 9, 4,845, and 33 minors respectively, exactly matching the binomial counts. Their squared-modulus sums are 9, 23,409, and 33, exactly the spectral determinants. Identity augmentation is therefore checked with the correct full N dimension rather than with a rectangular proxy of the wrong size.

## 5. Normalization sensitivity and the boundary of the conclusion

Define the different interface Hbar by multiplying every selected time-h row by 2^(-h/2). Every Hbar row has norm one. Its exact Gram is

    Hbar*Hbar = F_unitary* diag(mu_ell) F_unitary,
    mu_ell = sum_(h,t) 1_(E_(h,t)(ell)).

There is at most one admissible t at each h, so mu_ell<=n. More precisely, sum_ell mu_ell=D. Concavity gives

    log2 det(I+Hbar*Hbar) <= N log2(1+D/N)
                         = O(N log log n)

at the marker choice, already far below the unnormalized volume scale Nn. An even stronger observation applies to the exact minor argument: each row of [I;Hbar] has norm one, so Hadamard's inequality bounds every N-row minor by one. Thus no positive determinant-growth lower bound follows from these normalized output rows alone.

The controls verify the normalized Gram in exact cyclotomic arithmetic by clearing the powers-of-two denominators. They also evaluate every normalized augmented minor in the three small banks. The corresponding squared-modulus sums are 2, 16, and 2 instead of 9, 23,409, and 33.

This is a scope distinction, not a counterexample to the target. A circuit required to output the original unnormalized values must still pay for any restoration of their scale. Multiplication by 2^(h/2) is not a free unit-bounded scalar operation. Conversely, a task that requests only normalized values, or an algorithm that never exposes H, does not satisfy the interface premise used to infer the stated lower bound. The audit establishes neither a faster normalized solver nor a universal lower bound for normalized Fourier computation.

## 6. Explicit charged construction and remaining work

A direct orbit implementation supplies a matching O(Nn) bound with ordinary bounded coefficients. For each layer and s=0,...,N/2-1, use

    w_(2s)   = v_s + v_(s+N/2),
    w_(2s+1) = omega^s (v_s - v_(s+N/2)).

This is N additions/subtractions and N/2 unit-modulus multiplications per layer, plus linear reads, routes, and writes. Across n layers it is Nn additions and Nn/2 such multiplications. A literal two-edge executor gives the same order if it does not use this pairing.

Additional charges are explicit:

- Consecutive root powers, phase recurrences, and fixed-width marker/membership tables: O(N+n) field/address work. Binary-parent recurrences or a binary trie avoid per-index scanning through n bits.
- Read N input values and extract retained coordinates while the layers are live.
- Write all dense g values using the mask and copies: O(r(n+1)); sparse output may be smaller.
- Final Q^n phase/reversal correction and all N final writes: O(N).
- Live orbit storage: O(N); saving the entire requested g array adds O(r(n+1)) words.

The packet spectral identity is not an algorithm with free Fourier inputs. Computing all Fourier values first costs O(Nn) by the ordinary FFT; independent inverse q-bank transforms add sum_h O(D_h(n-h)), as well as routes and writes. The target correctly charges those terms and makes no faster claim from the factorization.

The contextual marker-cut fresh-source preparation is a separate operation with its accepted cost. It does not supply these future orbit values. The inverse correction remains uncomputed by the alias, and no correction or recovery bill is hidden inside a claimed sub-Nn algorithm because no such complete algorithm is asserted.

## 7. Fresh evidence, reproducibility, and preservation

Run `python independent_exact_controls.py` in this audit directory. The program reads no target files and imports no non-standard modules. It writes `INDEPENDENT_CONTROLS.json` deterministically. `EXACT_RUN.log`, `EXACT_REPLAY.log`, and `REPLAY_CHECK.log` record a byte-for-byte replay. The JSON snapshot is retained as an additional replay witness.

Coverage:

- 31 field/parameter/root-embedding cases in GF(65537) and GF(257), with exact root-order checks, through N=1024.
- 575 source inputs, including complete bases through N=64.
- 66,376 actual retained-source packet values.
- 70,384 fusion coordinates, each also compared to direct full-N first-return propagation.
- 83,064 full temporal batch coordinates.
- 9 all-entry complex-root Gram cases, through N=128, totaling 59,712 exact cyclotomic entries; another 59,712 entries for the normalized interface.
- Exact complete-q occupancy checks, selected ranks, and full retained-stack ranks in all nine cases.
- 4,887 exact augmented minors across three banks, with both unnormalized and normalized Cauchy–Binet sums.
- All overlap shifts for b=1,...,64; 506 exact first/second-moment checks for b=7,...,512; exhaustive top-window positioning checks on widths 8,10,12,14,16.
- A phase-omission negative control that fails as expected.

The input-preservation manifests cover every regular file in the target directory and the four contextual predecessor directories. `INPUT_FILES_BEFORE.sha256` and `INPUT_FILES_AFTER.sha256` are identical. The target seal passes before and after; all four contextual manifests pass independently. This audit's own manifest seals the report, independently authored verifier, evidence, replay records, and preservation records. The seal cannot include its own hash and is checked separately.

The finite controls deliberately include smaller b values outside the asymptotic b>=7 theorem. They test exact identities at their defined horizons, while the all-size proofs above establish the eventual lower bound. Modular controls do not establish complex positivity or a finite-field lower bound; the exact cyclotomic controls establish finite complex-root identities, not asymptotic complexity by experiment.
