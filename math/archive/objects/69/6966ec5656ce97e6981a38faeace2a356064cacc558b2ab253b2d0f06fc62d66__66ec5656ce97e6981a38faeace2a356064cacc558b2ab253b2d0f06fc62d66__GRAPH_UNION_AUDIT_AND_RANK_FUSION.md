# HERO17 graph-union convolution: independent audit and bounded rank fusion

Audit date: 9 October 2026 (UTC). The uploaded directory is dated 10 October 2026; that filename is preserved, not treated as an independently verified publication date.

## Verdict

The graph-union formula, post-cancellation support guard, and claimed fixed-parameter exact linear-time convolution route are correct on the stated validated sparse-fiber inputs. The implementation does not establish a universal exact linear-time FFT, unrestricted convolution, or integer multiplication. Its public certificate executor trusts certificates; the raw-input wrapper supplies the validation boundary.

Two independently justified extensions are supplied here:

1. A sharp state-count bound, S <= min(N, E, sqrt(Q Kx Ky)), where Kx and Ky are the total detected input modes. The source's one-mode-per-row construction attains the Q^(3/2) term exactly.
2. A fixed-rank fallback for the merged coefficient matrix. It accepts some graphs rejected by every fixed S/Q budget and still costs O(N) for fixed input-mode bounds and fixed output rank. Active-column sparsity removes an initially plausible extra balance requirement: no M^2 = O(N) hypothesis is needed.

These are project-level extensions, not publication-priority claims. The extension is separate independently authored work, not functionality attributed to the uploaded program.

## Scope and provenance

Source reviewed as text/data only:

- RESEARCH.md, especially section 4 and the accounting contract
- fiber_convolution.py
- fiber_union.py and fused_fft.py at the graph interface
- test_hero17.py, independent_audit.py, and saved AUDIT_RESULTS.json as historical evidence

No uploaded module, test, helper, or binary was imported, executed, or compiled. Source hashes and byte counts are in source_provenance.json. The earlier research master was read only. No master, Library, or source archive was modified.

The sibling tensor/fiber audit owns full proof and testing of the raw-input recognizer. This report independently checks graph algebra from raw arrays via direct short transforms, but those direct transforms are correctness oracles, not replacements for its linear-work recognizer. The sibling independently cross-checked the rank-fusion theorem and strict-escape construction below.

## 1. Exact model and notation

Let N=QM. Work in a supplied prime field F_p, with p>N and a supplied certified primitive Nth root omega; put eta=omega^Q. For each row t, input modes are distinct canonical labels 0 <= h < M with nonzero coefficients:

x[t+Qu] = sum_h A[t,h] eta^(hu),
y[t+Qu] = sum_h B[t,h] eta^(hu).

There are at most rx modes per x row and ry per y row. Put Kx=nnz(A), Ky=nnz(B), so Kx<=rx Q and Ky<=ry Q. The raw recognizer validates this representation and every input coordinate. Its field/root assumptions, including the requirement that p actually be prime, remain premises. Root order is validated; primality/root generation is not provided for free by the graph theorem.

The online factor choice satisfies Q^2 <= cN for a fixed constant c. Input-mode bounds rx,ry and the output-state budget C are fixed constants in the linear-time result. Output means every one of the N time-domain convolution coefficients, not a compact certificate.

Arithmetic counts below include field operations, comparisons, table preparation, input scans, explicit output writes, and bounded-size index operations. For a word-RAM interpretation, p=N^O(1), canonical field elements, O(log N)-bit words, and unit-cost word modular arithmetic/addressing are additional assumptions. The recognizer's O(Q(rx+ry)) scalar inversions require a separate word/bit charge; for fixed bounds and Q=O(sqrt N), standard polylogarithmic inversion work is absorbed by O(N) word work. This is not O(N) bit complexity: merely writing N field words generally costs Theta(N log p) bits. Exact complex identities do not establish finite-precision recognition or stability.

## 2. Independent derivation of the carry sign

Define circular convolution z[j]=sum_a x[a] y[j-a], indices taken modulo N. Fix an output j=t+Qu and an input-row pair t1,t2. Their row sum obeys

t1+t2 = t + Q e, with e=floor((t1+t2)/Q) in {0,1}.

The corresponding internal coordinates satisfy u2=u-u1-e modulo M. A character pair h1,h2 contributes

A[t1,h1] B[t2,h2] eta^(h2(u-e)) sum_(u1=0)^(M-1) eta^((h1-h2)u1).

Character orthogonality makes this zero unless h1=h2=h, in which case the sum is M. Therefore

C[t,h] = M sum_(t1+t2=t+Qe) A[t1,h] B[t2,h] eta^(-he),
z[t+Qu] = sum_h C[t,h] eta^(hu).

Both the negative carry sign and the factor M in fiber_convolution.py are correct. No extra 1/M belongs in the reconstruction because A,B are character amplitudes, namely normalized partial Fourier coefficients.

### Sparse quotient convolution identity

For a fixed label h, set

alpha_h[t]=omega^(-ht) A[t,h],
beta_h[t]=omega^(-ht) B[t,h].

Then, with ordinary length-Q cyclic convolution,

C[t,h] = M omega^(ht) (alpha_h circledast_Q beta_h)[t].

Indeed, omega^(ht)omega^(-h(t1+t2))=eta^(-he). Equivalently the ungauged coefficient product takes place in F_p[T]/(T^Q-eta^(-h)). This identifies exactly which quotient operation is being reused. Frequency bucketing reuses routing and root tables; it does not make the distinct labelwise cyclic products free. At full fiber density the method is a standard polyphase/Cooley–Tukey decomposition with arbitrary channels. There is no proved universal joint evaluator here, and this observation is not an unrestricted lower bound either.

## 3. Charged implementation audit

Let a_h and b_h count nonzero input modes with label h. The exact matching-edge count is

E = sum_h a_h b_h <= Kx Ky <= rx ry Q^2.

The source allocates M frequency buckets, an N-cell accumulator, an active-event list, and an N-cell seen marker. Each matched pair creates one field contribution and one bounded-size index operation sequence. The active list can be longer than the final support because a slot can cancel to zero and later revive. Its length is at most E, not necessarily S. The separate seen marker deduplicates these events correctly using final accumulator values.

Consequently the literal storage bound is O(N+Kx+Ky+E), and the pre-reconstruction work is O(N+Kx+Ky+E) after recognition. Both are O(N) only under the fixed-mode/Q^2 assumptions. Calling a trusted-certificate routine with arbitrary growing-size certificates does not inherit that theorem automatically.

Let S=nnz(C) after all edge summation and cancellation. The complete source route has cost

O((rx+ry)N + (rx^2+ry^2)Q + E + N + M S),

plus the scalar-inversion/root validation qualifications already stated. Thus S<=C Q makes M S<=C N. The source tests this after aggregation and before the length-M expansion of each surviving state; this is the right place for the guard. Early rejection based on the number of touched or temporarily nonzero states could be wrong because later edges may cancel.

Important boundaries:

- A guard rejection is a refusal of this fast reconstruction route, not a statement that convolution is undefined or impossible in linear time.
- Raising C with N removes the fixed-constant O(N) guarantee. A large finite test accepted by a larger C does not prove a uniform linear-time algorithm.
- union_and_convolve checks common metadata and the local root table, but does not independently certify every caller-created FiberCertificate, its mode uniqueness, lengths, field primality, or the Q/r budgets. convolve_if_supported is the validated raw-input entry point.
- The uploaded fused_fft.py fuses transform branches. It does not implement the rank-fusion convolution extension in this report or a universal fallback convolution.
- The source's supplied tests and saved test totals are historical claims. The fresh evidence below is separate.

### Cancellation/revival control

At Q=M=3 over F_19, take every x row to have h=0 coefficient 1 and y-row h=0 coefficients (1,-1,2). In the uploaded loop order the accumulator is populated, canceled, and revived. There are 9 edges, 6 active-list entries, and only 3 surviving states. All 9 raw outputs equal 6. Independent bookkeeping and raw convolution agree. Final cancellation to zero and disjoint-label zero products are also covered.

## 4. Positive and negative coverage controls

### Maximal input matrix rank can be real

For Q=M, give each input exactly one mode per row, using every label exactly once in independently permuted order and nonzero amplitudes. Each Q-by-Q raw fiber matrix is an invertible diagonal/permutation modification of the Fourier matrix and hence has rank Q. Every label has exactly one matched edge, so E=S=Q and complete output materialization costs O(N).

This corrects an overly narrow heuristic that constant ordinary input matrix rank is necessary for a linear-time structured route. It does not remove the sparse-fiber hypothesis.

At the opposite extreme, if all rows use the same label, E=Q^2 but S<=Q. Counting edges alone misses the benefit of aggregation.

### Exact family-count limitation

For fixed field, the length-M Fourier transform is a bijection. The number of admissible rows with at most r active characters is

L_r = sum_(j=0)^min(r,M) binom(M,j)(p-1)^j.

There are L_r^Q admissible inputs among p^N possible raw vectors. For a pair, the eligible fraction is (L_rx L_ry)^Q / p^(2N), even before the output-state guard. For balanced large Q,M and fixed r this is p^(-2N+O((rx+ry)sqrt N)) for pairs, with the standard polynomially bounded field assumption. Dense time-domain support and full row rank do not imply arbitrary-input coverage. The rank fallback below leaves this input-coverage limitation intact.

## 5. Sharp state-growth theorem

For any validated inputs, the output states carrying label h occupy no more than Q rows and no more than the a_h b_h matching pairs. Cancellations can only decrease support. Therefore

S <= sum_h min(Q,a_h b_h).

For every nonnegative v, min(Q,v)<=sqrt(Qv). Cauchy–Schwarz then gives

S <= sqrt(Q) sum_h sqrt(a_h b_h)
  <= sqrt(Q Kx Ky).

Together with the immediate bounds,

S <= min(N, E, sqrt(Q Kx Ky)).

No algorithm needs to compute square roots for this proof. For fixed rx,ry it implies S<=sqrt(rx ry) Q^(3/2).

The bound is attained by the source's one-mode construction. Let Q=M=s^2, x row t have label t mod s, and y row t have label floor(t/s), all coefficients nonzero. At fixed h, x rows are h+s a and y rows are hs+b, for 0<=a,b<s. Their sums are h(s+1)+sa+b modulo Q; (a,b) runs bijectively through all Q residues. There is exactly one edge per output (t,h), no cancellation, and

Kx=Ky=Q, E=S=sQ=Q^(3/2).

The literal reconstruction executes M S=N^(5/4) contributions. This proves the sharp worst-state behavior of this particular expansion mechanism, not a time lower bound for every algorithm on that input family. Independent examples at s=2,3,4,5 match the exact counts. At s>2 they reject the uploaded default ratio C=2.

## 6. Bounded extension: rank fusion after graph union

### Theorem

Retain validated input fiber bounds rx,ry and Q^2=O(N). Let H be the number of nonzero frequency columns of C after graph union. Suppose rank(C)<=d, for a fixed d. Then the two raw inputs can be completely convolved in O_(rx,ry,d)(N) exact work and O_(rx,ry,d)(N) words, even if S/Q is unbounded.

Proof:

1. Form C by the audited graph stage, costing O(N+E) after recognition.
2. Scan the already charged N-cell array to identify active columns. A surviving label must occur in both input certificates. Consequently H<=min(Kx,Ky,M)<=min(rx,ry)Q.
3. Restrict C to its H active columns and run bounded row elimination. Reject immediately on rank d+1. Successful elimination constructs C[t,h]=sum_(ell=1)^d f_ell[t]g_ell[h] in O(dQH+N)<=O(dN+N), with at most d scalar field inversions. Since the basis rows are linear combinations of C rows, they have zero entries outside these same H columns. No support growth is hidden in the factorization.
4. For each basis row evaluate all M character sums

G_ell[u]=sum_(h active) g_ell[h] eta^(hu).

A charged M-entry root table gives O(d M H) direct multiply/add terms. Since M H<=min(rx,ry)MQ=min(rx,ry)N, this is linear for fixed bounds. Computing a dense M-by-M transform is unnecessary.
5. Write every raw output using z[t+Qu]=sum_ell f_ell[t]G_ell[u], at O(dN+N) work. Zero rank produces the explicit zero vector.

The full ledger is

O((rx+ry)N+(rx^2+ry^2)Q+E+N+dQH+dMH+dN),

with the recognizer's inversion charge and at most d additional inversions. Memory includes N accumulator/output cells, O(E) events if the source storage schedule is retained, O(d(Q+H+M)) factor/evaluation words and charged root tables. Fixed bounds make this O(N).

Only Q^2=O(N) is needed for the existing edge stage. In particular, unbalanced M>>Q does not invalidate this extension because active-column sparsity pays for the short transforms. Treating those transforms as dense quadratic work would impose an unnecessary M^2=O(N) restriction.

A deterministic fused policy is: first try the source S<=C Q route; if that fails, test the fixed rank bound d on C and use this reconstruction. If both fail, refuse the structured fast route. The second rank test itself is linear and does not compromise charged rejection. This is a legitimate union of two structural acceptance conditions, not a generic FFT.

### Explicit strict escape from every fixed state budget

Choose an integer s>=2, Q=s^2, and any M>=s with Q^2=O(QM); take a valid field/root and eta=omega^Q. Square choice M=Q suffices. For h=0,...,s-1:

- At x row a=h+s v, 0<=v<s, place the single mode h with coefficient eta^(h floor((h+v)/s)). Thus every x row has one mode.
- At y rows b=(s-1)h+w, 0<=w<s, place mode h with coefficient 1. These length-s intervals have spacing s-1, so each y row has at most two modes. Some trailing rows are zero, which is allowed.

For fixed h,

a+b=s(h+v)+w,
e=floor((h+v)/s).

The carry does not depend on w, and the x coefficient cancels eta^(-he) exactly. As v,w vary, target rows cover every t exactly once. Hence

C[t,h]=M for every t and 0<=h<s; C[t,h]=0 otherwise.

Therefore E=S=sQ, H=s, and rank(C)=1. For any fixed C, choose s>C: the original state budget rejects, while the rank-d=1 fallback accepts with rx=1 and ry=2. Arbitrary nonzero label-dependent weights can also be inserted, giving an arbitrary nonzero rank-one basis on those H columns; a geometric-series special case is not essential.

This example has one mode on x and at most two on y. It is not asserted to have one mode on both inputs, nor to have maximal input row rank. The maximal-rank example in section 4 is a separate source family. The distinction prevents overstating the extension.

## 7. Independent checks and reproducibility

independent_graph_checks.py is newly authored and uses only Python's standard library. It never loads an uploaded Python module. It supplies separate direct cyclic convolution, raw fiber coefficient recovery, graph summation, quotient-gauge checks, rank factorization, and sparse-column rank reconstruction. Source bytes are optionally rehashed if present; source_provenance.json makes the mathematical checks portable without an archive dependency.

The saved successful run covers:

- 7,062 full-output convolution pairs, totaling 38,171 independently calculated output bins
- 6,561 exhaustive one-mode-or-zero pair cases at N=4 over F_5
- 1,002 raw mode recoveries from independently materialized inputs
- 38,171 statewise quotient-identity comparisons
- 7,062 support-bound checks, including cancellation and dense small controls
- 18 full-row-rank input pairs
- Four tight one-mode state-growth constructions
- Seven rank-one escape families, including unbalanced Q=4,M=64; Q=9,M=81; and Q=16,M=64
- 104 extra rank-factor/reconstruction cases, including rank zero and explicit d+1 rejection

The seven escape tests include two s=2 boundary controls where C=2 does not reject; five have s>2 and do reject it. The all-size proofs, rather than finite tests, establish the asymptotic extensions. Tests do not measure a practical speedup over optimized FFT libraries.

Portable commands, from this directory:

    python independent_graph_checks.py
    python independent_graph_checks.py --output independent_graph_results.json

The first command performs no output-file writes. The second writes only the requested result file. No external Python packages, network, original source executable, or prior master is required. The saved result JSON and provenance file are part of the sealed audit. SHA256SUMS and MANIFEST.json identify its exact contents.

## 8. Integration guidance and stopping point

Accept the uploaded sparse graph theorem within the exact finite-field/fixed-parameter contract. Retain the support guard, raw-certificate boundary, cancellation event charge, and all-output materialization cost. Add the sharp state bound and output-rank fallback as separately authored scoped improvements.

Do not promote any of them to arbitrary-input FFT coverage, an unrestricted arithmetic lower bound, O(N) bit complexity, generic integer multiplication, robust floating-point recognition, or a priority claim. A universal joint evaluator for arbitrary dense polyphase channels remains unestablished. This bounded audit and the verified rank extension complete the assigned work; no broader search or modification of the master is included.
