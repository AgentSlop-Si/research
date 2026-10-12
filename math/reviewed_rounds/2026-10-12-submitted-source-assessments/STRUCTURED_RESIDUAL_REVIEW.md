# Structured cyclic/Weyl residual executor: independent local review

Review date: 12 October 2026. Sources are identified by exact file and member hashes in [Source citations](SOURCE_CITATIONS.json).

## Verdict

The main exact identities, dyadic structured-input work bound, and static correspondence to the supplied implementation are supported. The accepted statement is conditional on a supplied exact field and primitive root, power-of-two length N, a supplied power-of-two divisor m, constant-cost exact scalar operations/equality, and O(log N)-bit index operations. Under that contract the hybrid has

    O(N[1 + log(s* + 1)] + m log m) work and O(N) field-word/index space,

where s* is the smaller of the two actually measured residual supports when the second candidate exists. The dense rational family has linear work for fixed m. The executor's generic/worst-case cost remains Theta(N log N). No unrestricted FFT improvement, historical novelty, all-integer-length implementation, finite-word accuracy, or production runtime result follows.

One statement needs correction: the implementation has two candidate-support censuses, not a literal two-pass input interface. Additional complete passes are paid and preserve the asymptotic bound.

This is a static mathematical/code-correspondence review with fresh finite identity controls. The supplied implementation and verification programs were never executed, imported, compiled, or AST-parsed. Their recorded test results remain author-reported. This review is not a cold replay or an acceptance of the supplied runtime/counters.

## 1. Source integrity and reviewed evidence

The materialized ZIP has SHA-256 `63ef69704ba2bcf3917346164d2123e81d949b516da8c3cd65a21c72b984f11f`. All nine member byte counts and SHA-256 values in its manifest match. In particular:

- `filtered_fft.py`: `ea5c8eb78e34e36791bf59d970be2baa7b77ecb811d41c3edf0b9c5c6077ed2d`
- `Filtered_Fourier_Fusion.tex`: `d95f19679386e18e2c25b1411bdf98fdd376c231ad91a3961749e7ec40428d41`
- `source_evidence.json`: `d9600c29716a7fea73f12fe820934cae1d73db5e0580e919e7b71b1b98ca5496`

The source citations retain the complete member-hash inventory. All supplied programs were inspected as inert text. The review reads the README, TeX proof, Python source, verification source, and selected ledger evidence. The PDF was checksum-verified; no claim of a separate visual PDF audit is made.

The supplied source ledger is a historical snapshot. It cannot establish the current state of another research record.

## 2. Exact reconstruction and boundary information

Use the positive, unnormalized transform Y_k = sum_j x_j omega^(jk), cyclic shift (Xx)_j = x_(j-1), and modulation (Zx)_j = omega^j x_j.

### Cyclic branch

For d = (I - X^m)x, R = F_N d satisfies R_k = (1 - omega^(mk))Y_k. Set L = N/m. The denominator vanishes exactly at k = Lh, 0 <= h < m. Define v_r = sum_t x_(r+mt). Then

    Y_(Lh) = F_m(v)_h, with short-transform root omega^L.

Every missing frequency is explicitly recovered from this short transform. Constants and m-periodic inputs are not accidentally sent to zero. For m=N, the residual is identically zero and the kernel transform is a full N-point FFT; no free full transform is hidden. N=1, x=0, and m=1 are included correctly. Source correspondence: `innovation_fft`, Python lines 333–377; proof TeX lines 60–104.

### Weyl branch

For d = (aI+bZ-cX)x,

    (F_N d)_k = b Y_(k+1 mod N) + (a-c omega^k)Y_k.

The exact seed Y_0=sum_j x_j and b!=0 yield all remaining outputs by forward recurrence. The source uses this sign convention consistently. It need not invert the full Weyl operator, and does not divide by cyclic holonomy or require its determinant to be nonzero. The last cyclic equation need not be solved: the supplied true seed plus induction already identifies every output. A singular diagonal or shift/modulation operator is consequently allowed. Source: Python lines 380–418; TeX lines 107–139.

### Automatic rational candidate

If N>1 and x_0!=x_1, the candidate u=(x_0-omega x_1)/(x_0-x_1) makes g_0=g_1. The algorithm measures all coordinates of (I-X^m)g, with g_j=(u-omega^j)x_j. It does not infer low support from two samples. The recurrence Y_(k+1)=uY_k-(F_N g)_k is correct for every candidate, even when u is an Nth root and the weighting operator is singular. No division by u-omega^j occurs in this executor. If the candidate is unavailable or loses, the ordinary branch remains correct.

For the promised family x_j=C/(u-omega^j), C!=0, u^N!=1, N>=2, x_0!=x_1 and the computed candidate is exactly u. Then g is the constant C, so its cyclic residual support is zero for every m. At fixed m all stages are O(N). With u!=0 both the input and full output can be dense; the improvement is not dependent on a sparse final spectrum. The closed form is Y_0=NCu^(N-1)/(u^N-1) and Y_k=NCu^(k-1)/(u^N-1) for 1<=k<N. The u=0 edge case is legal but need not have dense output. Source: Python lines 421–478; TeX lines 141–148 and 233–237.

## 3. Cold cost, recognition, space, and scan audit

### Recognition and pruning

The ordinary and weighted supports are determined by complete length-N loops. There is no support oracle. The support tree uses 2N entries and an amortized-linear incremental bit reversal, rather than N separate logarithmic reversals. At recursion depth d, an s-supported residual has at most min(2^d,s) active parity subproblems, each of length N/2^d. Thus the total merge/allocation traffic is bounded by

    sum_d (N/2^d) min(2^d,s) = O(N[1+log(s+1)]).

Absent subtrees return `None`, not a fresh dense zero array. Even the zero-support case pays N output entries. All root-bank, support-census, fold, denominator, and output stages are linear. The length-m kernel FFT contributes O(m log m). Depth-first recursion retains geometrically decreasing sibling/intermediate arrays; all root, residual, support, fold, denominator, and output banks total O(N) live field words/indices. This is not a byte-memory bound for arbitrary-size field elements.

The second root bank and recomputed chosen residual/support are constant-factor duplication. The weighted branch retains its already formed g but the child still differences g, builds a support tree, folds it, and constructs another bank. Both losing-candidate work and the chosen execution remain charged. There is one optional u candidate at one supplied m. The algorithm does not adaptively try all periods, filters, or Weyl parameters. A broader search must add the work of every attempted candidate and cannot inherit a free global-minimum guarantee.

### Correct the pass-count description

The hybrid has an ordinary-support loop over x, an optional loop forming g from x, and a loop measuring g's support. If the Weyl branch wins, there is another complete x loop for the seed. If the cyclic branch wins, `innovation_fft` rereads x to form the chosen residual and fold.

Ignoring O(1) candidate reads, the Weyl path makes 4N direct accesses to original x in those source loops: 2N ordinary-census accesses, N weighting accesses, and N seed accesses. The cyclic path makes 6N original-x accesses if a weighted candidate was attempted, or 5N without that candidate. Internal arrays are scanned additionally. These counts describe source accesses rather than a hardware memory-traffic experiment.

Replace “two input scans” with “two complete candidate-support censuses and a constant number of additional paid linear passes.” No two-pass streaming or external-memory guarantee is established. The README's less literal wording “both scans” can reasonably mean the two support censuses, but should be clarified before integration.

### Roots, inversions, and counters

No discrete logarithm is called or required. Powers of the supplied primitive root are generated successively in O(N), and dyadic exact order is validated with omega^N=1 and omega^(N/2)!=1 using O(log N) field operations. The initial field and primitive root are supplied, not discovered. “Cold” therefore includes fresh table construction and validation within this input contract; it does not include arbitrary field construction or root finding.

The N/m-1 distinct cyclic denominators are all nonzero and batch-inverted with one inverse and linear multiplications. Candidate inversion is guarded by x_0!=x_1. The supplied Weyl routine checks b!=0 before inversion. The general filter enumerates its zero mask and never sends those entries into batch inversion. These guards eliminate the apparent singularity concerns in the claimed domain.

`Fp` assumes a verified odd prime and canonical residues; it does not prove primality or validate every scalar's canonical representation. Those are contract requirements, not an accepted robust raw-input validator. Abstract field inversions cost one operation. Its Euclidean-step counters are separate from named field-operation totals. Source inspection and the proof support the asymptotic model, but the named events are not a complete count of every Python instruction, every memory access, wall time, or arbitrary-bit inversion cost. Exact equality and field elements are mathematical model primitives. The cyclotomic verifier's rational coefficients can grow, so unit field-word space and arithmetic must not be translated into O(N) machine bytes or runtime.

## 4. General filter extension and worst-case boundary

For a supplied nonempty t-tap cyclic polynomial P, forming P(X)x and the complete spectral mask P(omega^k) costs O(Nt). A sparse-input transform recovers its residual, while a separately specified pruned-output transform computes the q missing frequencies directly from x. The source uses start/stride input addressing and O(N)-size level plans, giving the stated O(N[t+log(s+2)+log(q+2)]) model cost and O(N) field-word space. This is not the hybrid's smaller two-candidate formula. Filter discovery is extra. For x_j=j^2 in characteristic zero, the cyclic third difference is supported on at most three wrap-boundary positions and the filter has one spectral zero, so the claimed linear example is consistent.

The Cauchy-minor obstruction is valid for the stated complex family with u=2. Any nonzero t-tap scalar cyclic filter has residual support at least N+1-t. Small t therefore leaves a dense pruned transform; large t makes this literal filter application quadratic. The Weyl branch changes operator families and can escape this example. Neither fact is a lower bound on all Fourier algorithms.

For the broader one-stage Weyl family, normalization b=1 leaves two parameters. The operator aI+Z-cX has nullity at most one, so composing with I-X^m gives nullity at most m+1. For a fixed support of at most s, the preimage dimension is at most s+m+1; adding two parameters gives at most s+m+3. Finitely many support/minor charts therefore lie in a proper algebraic subset when s+m+3<N. This justifies the manuscript's generic-complex limitation. Separately the ordinary cyclic branch has kernel dimension m, so generic residuals there are also large. For dyadic m<=N/2 the generic relevant support is Omega(N); for m=N the explicit kernel FFT already costs Theta(N log N). Combined with the algorithmic upper bound, this gives its generic/worst-case Theta(N log N) statement. It is not a probability claim over every finite field and not a universal FFT lower bound.

All-length scope remains restricted: the code rejects non-power-of-two lengths and uses radix two. The algebraic identities themselves hold more broadly with suitable roots, but neither the implemented fast executor nor its N log s pruning bound has thereby been established for every integer N. Padding changes the transform/root problem and is not a free extension.

## 5. Fresh independent checks

A reviewer-authored identity checker was written for the underlying review. It uses only literal quadratic modular DFT sums and fresh elementary formulas. It never reads or imports the supplied programs. [Verification scope](VERIFICATION_SCOPE.json) records the retained PASS result for:

- 2,160 cyclic reconstruction cases, 16,563 output coordinates
- 62,956 Weyl recurrence cases, 257,578 output coordinates, including 10,045 singular diagonal operators
- 554 hybrid candidate recoveries, including 418 root-valued/singular u cases; 131 skip cases
- 237 rational-family cases, 219 with dense input and output
- 65,814 exhaustive support masks through N=16 for the occupied-residue census bound
- 5 cyclic quadratic boundary cases

This includes all inputs over F_3 at N=1,2 and F_5 at N=4, all nonzero-b Weyl triples for those inputs, and additional direct controls through N=64. Finite checks support sign, boundary, kernel, recurrence, and singularity analysis; they are not proofs over all fields/lengths and do not certify the imported program, its output counts, or its reported performance.

## 6. Relationship to accepted Q07, FUS-05, and FUS-11 evidence

Q07's accepted raw-mode API recognizes c_j=sum gamma_l q^(u_l j), verifies every raw coordinate, returns explicit positive-sign DFT values by sparse scatter, and separately applies diag(a)Fdiag(c)Fdiag(b) to fresh vectors at O(N(s+1)) each. The new residual executor solves a different input representation problem. Its universal exact correctness within a dyadic field contract does not extend Q07's raw-mode recognition, mode extraction, refusal behavior, fresh-vector action, ternary interface, or actual-caller integration. Classical input pruning is shared; that is a supporting mechanism rather than a replacement theorem.

FUS-05's raw orbit-weight recognition and full-rank Weyl-correction action are not the same as this first-order output recurrence. The new package has no fresh-vector correction interface, general diagonal discovery, or Q07-mode certificate. Preserve its accepted theorem and every separately charged action bound.

FUS-11's supplied-field common-chirp/blocked-recognition integration is a different dispatcher. The new package does not implement phase acquisition, common-chirp min(B,H), optimized blocked/Toeplitz kernels, or the established INVALID/NONMEMBER/LIMIT interface. A losing u candidate is safely included in this package's linear recognition overhead, but that does not settle other dispatchers' rejected-search budgets. This source does not complete the broader Q07 or Q13/FUS-11 obligations.

## 7. Bounded conclusion and remaining work

The scoped mathematical statement and static implementation correspondence are supported. The source program has not been cold-replayed. State the complete dyadic field/root/divisor contract beside the bound, including exact scalar equality and division, explicit N-coordinate input/output, and the constant-size attempted-candidate family. Describe two candidate-support censuses and additional paid linear passes.

Q07, FUS-05 and FUS-11 retain their distinct interfaces and action bounds. Source-bound full-output and meter tests, invalid-domain and failed-candidate accounting, a named actual caller, non-dyadic execution, field/root discovery, general phase acquisition, finite-word stability, physical/bit costs and priority remain open. None can be inferred from the identities or the reported timing evidence in a different source package.
