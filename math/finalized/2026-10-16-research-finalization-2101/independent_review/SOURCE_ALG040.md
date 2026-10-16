# Independent audit: exact weighted marker cut

## Verdict

**Accepted in its stated algebraic and paid-schedule scope.** No correction to equations (1)–(21), the source bound, the exact changed-cut feedback, or the source-rank argument was found. The proposed method improves fresh-source preparation to O(Nn/ln n) field/address work and O(N ln n) words at its stated marker choice. Its displayed complete inverse/recovery schedule still makes Theta(Nn) structural coordinate visits. It is not a faster complete arbitrary-input Fourier transform.

There is an additional important model boundary: over the complex numbers, the displayed executor uses only unit-modulus scalar multiplications and binary additions on input-dependent data. A complete redesign retaining that bounded-coefficient linear gate model is subject to the classical determinant lower bound, independently of this particular schedule. That observation is an application of existing theory, not a universal arithmetic lower bound, and does not transfer to the finite-field model by itself.

Audited target:

- `marker_cut_compression_0229/EXACT_MARKER_CUT_COMPRESSION.md`
- SHA-256: `8bc97582cb933e29bc16d4efb8c581a612af12813f630b6233256fd27c418628`

The target report and its existing seal were verified. Neither target nor predecessor programs were executed or imported. The independent verifier in this directory was written from the definitions and uses only the Python standard library. Predecessor prose was consulted for its elementary avoiding-word bound and cut comparison; no predecessor executable was used.

## 1. Exact states and nilpotence

Let N=2^n, 1<=b<n, d=n-b, r=2^d. The field contains a primitive Nth root omega. Put R={2^b j:0<=j<r}, let A consist of the fixed-length n-bit words avoiding 0^b, and put T=R union A. These two retained parts are disjoint.

For an eliminated word s, its rightmost marker ends h positions before the right edge. Because s does not end in a marker and contains one, 1<=h<=d. The suffix after that marker starts with 1; otherwise the marker would extend one position farther. It avoids another marker. Conversely any prefix j, followed by 0^b and such a suffix w, has rightmost-marker age h. Thus

    E_h = {2^(b+h)j+w : 0<=j<2^(d-h), w starts with 1 and avoids 0^b},
    e_h = 2^(d-h) a_b(h-1).

An edge either creates a new suffix marker and enters R, advances an existing rightmost marker from age h to h+1, or loses that marker at age d and enters A. An A word can only remain in A or enter R. In particular, A never enters E.

Every E-to-E path has fewer than d edges, so Q_EE^d=0. For sharpness, start at state 1 and append d-1 ones. This gives a nonzero path through every age. At any length at most n, a specified source and destination determine the appended bits uniquely. Therefore its nonzero weight cannot cancel with a second such path. The exact nilpotence index is d. When d=1 this means Q_EE=0 on a nonempty eliminated set. When b=n, E is empty and no compression is obtained; that endpoint is correctly excluded from the substantive formulas.

## 2. Schur algebra and free/forced accounting

Using the target's actual weighted restrictions U,L_h,V_h,W,D,J,H, successive substitution gives

    X_1=x_E1,
    X_h=x_Eh+z L_(h-1) X_(h-1),
    y_Eh=X_h+z^h F_h v_R,
    F_h=L_(h-1)...L_1 U.

Each X_h has degree at most h-1. Substituting the layer exits gives exactly the target source f_R,f_A and both retained equations. This is ordinary block elimination with constant Schur term I; it is valid as a formal-series identity over every field in the stated scope. It does not presume a new Fourier quotient of T.

At degree n, X_h contributes zero. The eliminated top output is exactly F_h(v_R)_(n-h), and the retained top output is v_n. There is no omitted free top term. This is structural disappearance, since the free E propagator is nilpotent, rather than a numerical cancellation assumption.

The suffix-only cut and this cut must not be mixed. Adding A changes both first returns and which output rows are retained. The old free/forced decomposition is not an extra correction to add to this new Schur solve. The new equations account for every path once. In particular, the old kernel at lengths greater than d+1 is invalid for the new retained set.

The target's explicit N=16,b=2,omega=64 example is correct: 0000→0001→0011→0110→1100 has weight 64. It first returns to the suffix-only R at length 4, but encounters the new retained set at 0110 at length 3. Direct killed propagation independently confirms old degree-4 coefficient 64 and new coefficient 0.

## 3. All-size weighted routes

For a length-t appended word k, direct multiplication of edge weights yields

    weight(s,k,t)=omega^(s rev_t(k)+gamma(k)),
    gamma(2a)=gamma(a),  gamma(2a+1)=gamma(a)+a.

Indeed, appending a final 1 contributes the preceding state to the exponent, while a final 0 contributes nothing; reduction of states modulo N does not change powers of omega. For s=2^b j the source-dependent factor is eta^(j rev_t(k)), eta=omega^(2^b).

For t<=d, an output index a of Q_r^t has appended word k=a mod 2^t. Its coefficient has the same source-dependent phase and scalar eta^gamma(k), so multiplication by (omega/eta)^gamma(k) gives the required full-N phase.

For a non-direct return to R, the appended word is k followed by b zeros, where k begins and ends with 1 and avoids 0^b. The zero suffix introduces no additional edge phase. The resulting retained index is

    2^b(a-k)+k mod r.

For lengths at most d+1 the original marker has not vanished at an earlier step, so there has been no prior A visit. At the next step beyond age d, an excursion either returns to R or enters A. Consequently the return coefficient is C_t Q_r^t at length b+t for 1<=t<=max(0,d+1-b), and all other non-direct R-to-R first returns vanish. The routing may merge coordinates; each merge is a paid addition.

For an R-to-A first return, length d+1 is necessary. Its appended word w begins with 1 and avoids 0^b; the resulting n-bit state has b-1 leading zeros and lies in A. If a=floor(w/2), then

    rev_(d+1)(w) = rev_d(a) + (w mod 2) 2^d.

The last summand vanishes in the eta exponent. Thus the endpoint coefficient is exactly omega^gamma(w) eta^(-gamma(a)) (Q_r^d u)_a. No missing summation or phase correction is needed.

Finally, the top E_h route is

    a ↦ 2^b(a-k)+k mod N,  k=a mod 2^h,

with the same phase correction. This route is injective: the low h bits recover k, and the higher bits recover a-k. Its image is precisely E_h.

## 4. Safe pruning and paid setup

For t<=d the low t output bits determine the appended word. A selected word has a selected prefix. Therefore mask-after-step propagation from the previous selected coordinates gives exactly Q_r^t u on the selected coordinates. Different source contributions may merge, but the same mask applies to all contributions at a coordinate; those merges do not invalidate pruning. The active structural width is e_t, not the number of language-automaton states. The argument is not licensed beyond t=d.

Generation-stamped scratch arrays and touched-coordinate lists suffice. The two outgoing edges from each active coordinate, membership tests, list writes, initialization, and merge additions are all chargeable to O(r+sum e_t) per trajectory. Since r=2e_1 and e_(t-1)<=2e_t, the initial full r-vector and predecessor lists are absorbed. Structurally present zero values remain present in the schedule count.

The asserted O(N+n) setup is attainable:

1. Enumerate the binary trie through depth n, maintaining the trailing zero run and the position of the latest completed marker. It has 2N-1 nodes, handles leading zeros directly, and generates exact membership, age, and coordinate lists without n work per leaf.
2. Build consecutive omega powers and the needed eta/ratio power and phase tables. Binary-parent gamma recurrence requires constant work per index. In fact gamma(k)<k for k>0, so indices and exponents fit O(log N) bits.
3. eta is obtained by b squarings. The report explicitly charges one scalar inversion. It is also possible to avoid that inversion: eta^(-1)=omega^(N-2^b) is already in the omega power table. All required scalar phases can therefore be prepared with O(N+n) additions/multiplications and address work.

Nothing here is a bit-complexity claim. Root provision, exact field arithmetic, and word-size address operations are the stated model. The audit verifier's dense arrays and modular exponentiation are finite oracles, not production-cost evidence.

## 5. Fresh source: moment bound and space

Each E_h coordinate carries exactly h polynomial slots in the layer schedule. Transferring its polynomial along at most two edges costs O(h), so the source work is

    O(N + m(n+1) + M_b(n)),
    M_b(n)=sum_(h=1)^d h e_h,  m=|T|.

This includes reading x, dense retained-jet initialization, polynomial-slot initialization, shifts by address offset, edge multiplications, and additions.

The avoiding-word generating function is

    A_b(z)=(1+z+...+z^(b-1))/(1-z-z^2-...-z^b).

Its nonnegative series converges at 1/2: the elementary recurrence majorant a_b(k)<=2(2-2^(-b))^k suffices. Extending the finite moment sum and differentiating gives

    M_b(n)/N <= 2^(-b-1)[A_b(1/2)+(1/2)A_b'(1/2)]
              = 2^(b+1)-b-2.

This identity is exact, including b=1. It is not justified only by fitting finite data.

Writing q=1-2^(-b-1), the same majorant gives e_h<=r q^(h-1). Because h q^(h-1)<=sum_(i=0)^(h-1)q^i<=1/(1-q), each live layer has at most h e_h<=2N scalar slots. Two adjacent layers suffice. Total source storage is therefore O(N+m(n+1)), not O(M_b(n)) simultaneous storage.

For b=floor(log2(n/(4 ln n))) and sufficiently large n,

    r<8N ln n/n,  |A|<=2N/n^2,
    m(n+1)=O(N ln n),  M_b(n)=O(Nn/ln n).

Thus the claimed O(Nn/ln n) source work and O(N ln n) words are accepted, with all-N algebra and an asymptotic marker choice. This improves the changed-cut source only.

## 6. Inverse and recovery counts

The online residual algorithm is a valid causal inverse because all updates from coefficient j land strictly later. Direct retained edges are paid, and the two non-direct blocks have exactly the routes proved above. Induction on j verifies the solution for arbitrary supplied retained jets, not merely jets produced by the source map.

At an age t<=kappa, R feedback requires starts j=0,...,d-t. R-to-A feedback requires j=0,...,b-1 at every age t<=d. For t>kappa only the latter starts remain, but then d-t+1<b. This proves the stated count without an implicit exception:

    V_inv=sum_(t=1)^d e_t max(b,d-t+1).

Recovery additionally requires the start j=n-h to reach age h. Combining those starts with the inverse trajectories gives exactly n-t+1 starts at age t, hence

    V_joint=sum_(t=1)^d e_t(n-t+1)
           =(n+1)|E|-M_b(n).

The initial r-vector work for every nonempty trajectory is covered by e_1=r/2. Sparse direct retained work and all residual storage are O(m(n+1)); final output, phase, and permutation work is O(N). Therefore there is no hidden unpaid recovery call.

At the marker choice, m=o(N), M_b(n)=o(Nn), and d/n→1. The displayed joint schedule has V_joint=(1-o(1))Nn. Its inverse alone is also Theta(Nn), by (d+1)|E|-M_b(n)<=V_inv<=n|E|. These are structural visits of the specified executor; they are not lower bounds for unrestricted circuits computing the same maps.

## 7. Fresh-source rank

The full source is already supported in degrees 0,...,d. If that source is zero, formal Schur invertibility forces v=0. The whole resolvent output then equals the eliminated polynomial (I-zQ_EE)^(-1)x_E, of degree at most d-1. Its degree-d coefficient is Q^d x, so Q^d x=0.

Q is invertible. Pair columns s and s+N/2; their common destination pair has matrix

    [1          1         ]
    [omega^s   -omega^s   ],

whose determinant is -2 omega^s, nonzero because a field with a primitive 2^n-th root has characteristic different from two. Therefore x=0, and x↦f has rank N.

A fixed linear summary through which the entire source factors must have dimension at least N. This does not prohibit a fast high-rank circuit, nonlinear encodings in a different model, or joint source/solve cancellations; it supplies no arithmetic lower bound on its own.

## 8. Existing bounded-coefficient boundary, carefully scoped

For the complex specialization, every omega, eta, omega/eta, inverse-phase factor, and their powers has modulus one. The source, pruned trajectories, routing, direct updates, and residual solve use binary additions and multiplication by these constants. Copies, permutations, signs, and initialization add no unbounded scalar gate. Constant-only setup can be performed before the input arrives; even granting that setup for free does not change the input-dependent model. The displayed control depends on indices and masks, not input values.

The restriction is on scalar gate multipliers, not on intermediate data magnitudes or the effective coefficients of accumulated linear forms. Those may grow through paid additions. An unbounded multiplier manufactured during a different setup would leave the stated gate model even if its manufacture were charged.

The relevant existing result is Morgenstern's bounded-coefficient lower bound for the **unnormalized** complex Fourier transform ([Journal of the ACM, 1973](https://doi.org/10.1145/321752.321761)). Applied here, its determinant argument is short. Track the largest absolute determinant of N coefficient rows among all linear forms computed so far. It starts at 1. A unit-modulus scalar gate cannot increase it. A new sum of two previous rows increases it by at most a factor 2, by determinant linearity. The final map obeys

    (Q^n)_(w,s)=omega^gamma(w) omega^(s rev_n(w)),

so it is a unit-modulus diagonal times a row-permuted unnormalized Fourier matrix. Its determinant modulus is N^(N/2). Thus at least (N/2)log2 N binary additions are necessary in this model.

This is stronger than a visit count, but narrower than a general arithmetic impossibility statement. In particular:

- It concerns complete exact output for arbitrary complex inputs, with ordinary scalar linear gates and bounded multipliers.
- It does not by itself bound source preparation or any isolated Schur block at Nn.
- It does not apply via an absolute-value determinant to the finite-field checks.
- Unbounded scalar constants, input-dependent nonlinear arithmetic/division, encoding or word operations on field data, and alternative normalization require separate model analysis.
- Producing normalized Fourier output is not interchangeable with the specified unnormalized map in this determinant proof; the final scale must be accounted for.

Therefore a faster complete complex redesign cannot arise solely by rearranging these unit-phase/addition primitives. This is an explanatory application of established theory, not a new theorem or a universal FFT lower bound.

## 9. A concrete next constructive bottleneck

The repeated work is already substantial at **young marker ages**, before any long tail or A endpoint. Let L=floor(2^(b-1)), and take n sufficiently large in the marker regime so L<=d and L<=kappa. A union bound on marker occurrences in an (h-1)-bit word gives a_b(h-1)>=2^(h-2) for h<=L. Hence e_h>=r/4 and

    sum_(h=1)^L e_h >= N/8,
    sum_(h=1)^L e_h(d-h+1) >= (N/8)(d-L+1)=Omega(Nn).

This lower estimate is only for the displayed independent-trajectory schedule. It locates the bottleneck: deleting late excursions or optimizing B alone cannot remove that schedule's leading order.

A focused next construction should explicitly batch the young-age R-feedback map on arbitrary coefficient vectors u_j:

    g_k = sum_(1<=t<=min(L,kappa)) C_t Q_r^t u_(k-b-t),

with out-of-range u treated as zero, all phases and merges paid, and a specified way to use the batch in the causal Schur solve. The acceptance test is an exact all-input implementation, its coefficient-magnitude/gate model, setup, storage, and arithmetic bill; scalar zero-run summaries do not meet it. An improvement to this batch is only a component, and must still be composed with inverse causality and complete recovery.

For a finite-field-only construction this is an open constructive target within this audit. For a claimed sub-Nn complete complex construction, an explicit, paid departure from the bounded-coefficient linear model is additionally necessary. Merely promising cross-coefficient sharing under unchanged primitives is insufficient.

## 10. Independent controls and sealing

The fresh verifier uses direct global weighted propagation with retained coordinates killed after every step, and independently compares it with the layer source and compressed routes. For arbitrary retained polynomial right sides, its inverse oracle is a full-N driven recurrence with fresh T-supported forcing at each degree. This avoids relying on the same reduced kernel as both implementation and oracle.

All checks passed:

- 88 parameter/field cases, through N=1024, in GF(257), GF(65537), and GF(998244353), with exact-order checks for every root.
- 1,284 global basis inputs for the source map.
- 646 R-basis route cases, including all R bases for every cut through N=256 in GF(257); each checks feedback beyond the new cutoff, pruning, and every recovery age.
- 88 arbitrary retained jets for the complete causal inverse and top recovery.
- 88 fresh arbitrary global inputs for the entire Q^n output.
- 10 full source-rank checks through N=32.
- 14,100 direct path-phase checks.
- 128 exact rational moment identities and 8,128 exact finite cardinality/moment cases.
- The old-kernel/new-cut counterexample.

These finite checks corroborate the proofs; they are not substitutes for all-size reasoning or implementations of the claimed production costs. The independent run was repeated and its log matched byte for byte. `AUDIT_SHA256SUMS.txt` seals this report, the independent verifier, its result data/logs, and read-only target seal/hash records. No target or predecessor file was modified.
