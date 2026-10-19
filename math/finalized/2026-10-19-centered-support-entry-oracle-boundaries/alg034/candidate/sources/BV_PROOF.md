# A bounded-variation centered-source family beyond constant originals

18 October 2026 UTC. New construction and finite execution, pending independent review.

## Main statement

Let m >= 11, M=2^m and N=M/4. Let the actual nonzero original be

    u0_j = c_j 2^(-F),  0 <= j < N,

where c_j are Gaussian integers on a canonical common dyadic grid. A supplied dense array is scanned in full. Alternatively, the original can be supplied as a canonical ordered partition into q nonempty constant blocks. The latter is a compressed original representation; it is not a claim to have read N unavailable entries.

Set c_(-1)=c_N=0, and define the exact integer quantities

    E = sum_(j=0)^(N-1) |c_j|^2,
    B = sum_(j=0)^N ( |Re(c_j-c_(j-1))| + |Im(c_j-c_(j-1))| ),
    C = ceil sqrt( N B^2 / (4 E) ).

The block representation computes B from its two boundary jumps and q-1 interior jumps, without expanding the blocks. C is computed using integer square root and exact squared comparison, never a floating estimate. Fix a variation budget A and admit only C <= A. This is a structured class selected by variation relative to energy. It is not an arbitrary-original or unknown-support recovery theorem.

Normalize using

    h = ceil log2 sqrt(E),  u_j = c_j 2^(-h),
    R = ||u||_2,  sigma = h-F.

Then 1/2 < R <= 1 and u0=2^sigma u exactly. Assume the accepted scale condition |sigma| <= 4m. Let J_N place coordinate j at residue j-a0 modulo M, where a0=floor((N-1)/2), and let U_L be the negative unitary DFT. Define z=U_M J_N u. Put

    T = 2^ceil(m/4),  K = C T,  P = 16m+16,  rho=2^(-P).

Assume K < M/2. There is a fully finite deterministic provider supported on the 2K+1 locations of circular distance at most K from zero, with P-grid coefficients, satisfying

    ||Z-z||_infinity <= R M^(-1/4).

The norm is the complex modulus infinity norm. This supplies the same accepted beta=1/4 outer premise as the constant-only provider. Source identity, normalization, center and eventual target U_N u0 remain unchanged throughout the composition.

For fixed A and fixed q, this gives O(M^(1/4)) supplied coordinates and the same conservative polylogarithmic-front-end form as the earlier constant family. When q grows, q is retained in every formula-evaluation, recognition, storage and replay cost below. The theorem does not treat a q-block descriptor as q exact Fourier coefficients.

## 1. Why the class is genuinely broader

The new actual original can have arbitrary block endpoints, unequal complex values, sign changes, and several jumps. No modulation, target renaming, or preexisting sparse Fourier object is used as a substitute for the original. The executed fixture has values 1, 2 and -1 on intervals of lengths 173, 211 and 128, respectively. Its full DFT has nonzero coordinates away from zero, so its target is not the constant-vector closed form.

A further mathematical subclass is nonnegative real monotone sequences satisfying

    max_j c_j * sqrt(N) / sqrt(E) <= A.

For these B=2 max_j c_j, hence C <= ceil(A). The number of distinct samples can be N. For example, c_j=N+j has C<=2 and q=N for N>=2, so the family includes strictly nonconstant affine sequences at arbitrarily large admissible lengths. The present block-sum evaluator pays for all q=N blocks in that example; no fast affine evaluator is claimed. The finite reference's q<=64 engineering cap does not execute that unbounded subclass.

The old exact-support obstruction is untouched. Every nonzero exactly centered source obeys |supp(U_M J_N u)| >= M-N+1. For the new family the exact support can be larger; no new exact-support size is asserted. Only the approximation Z is sparsely stored. The earlier impossible <=16 centered bridge is not used.

## 2. The variation tail bound

Write theta=2 pi k/M and S(theta)=sum_(j=0)^(N-1) u_j exp(-i j theta). Multiplying the finite sum by 1-exp(-i theta) telescopes:

    (1-exp(-i theta)) S(theta)
      = u_0 + sum_(j=1)^(N-1) (u_j-u_(j-1)) exp(-i j theta)
        - u_(N-1) exp(-i N theta).

The extra centering multiplier exp(2 pi i a0 k/M) has modulus one. For nonzero circular distance d=dist_M(k,0), concavity of sine gives sin(pi d/M)>=2d/M. Thus

    |z_k| <= 2^(-h) B / (2 sqrt(M) |sin(pi k/M)|)
            <= 2^(-h) B sqrt(M)/(4d)
            = [ B sqrt(N)/(2 sqrt(E)) ] R/d
            <= C R/d.

For omitted k, d>K=CT, hence |z_k|<R/T<=R M^(-1/4). At retained locations the finite evaluator certifies complex error <=rho. Since R>1/2 and P>1+m/4, rho<R M^(-1/4). Combining the disjoint cases proves the theorem. No probabilistic recovery, independence or amplification claim is needed.

The factor C is at least one: if Amax=max_j |c_j|, the zero-extended total complex variation is at least 2 Amax, B dominates that variation, and sqrt(E)<=sqrt(N) Amax. Its exact minimal integer value is checked by C^2(4E)>=NB^2 and, when C>0, (C-1)^2(4E)<NB^2.

## 3. Certified finite block formula and precision

For a block [s,e) with value a=c 2^(-h), let l=e-s. For k != 0 modulo M its contribution is exactly

    a/sqrt(M) * exp( pi i k(2a0-s-e+1)/M )
      * sin(pi l k/M) / sin(pi k/M).

At k=0 it is a l/sqrt(M). Summing these q contributions gives the exact z_k. The phase explicitly contains both the source block endpoints and the original centering offset. The old constant-block half-sample phase is the q=1 special case, not a rule incorrectly reused for each shifted block.

The new code uses byte-identical accepted interval arithmetic primitives from the previous provider, copied as runtime/interval_core.py. It calls only their ledger, exact rational interval arithmetic, Machin pi enclosure, finite Taylor trigonometric enclosure, inverse-root enclosure and rounding functions. It does not invoke that file's old source recognizer, old coefficient formula, old cutoff or old production/replay APIs. The four outer numerical sources are separately byte-identical accepted sources. This is reuse of explicit verified arithmetic, not an uncharged numerical oracle.

Choose

    Q = P + 2m + ceil(log2(q+1)) + 20.

The implementation uses q.bit_length(), exactly ceil(log2(q+1)) for positive q. One paid pi preparation is shared. The accepted rational Machin/Taylor construction at working precision Q encloses every sine/cosine endpoint within delta=4*2^(-Q) of the true value, after signed reduction modulo 2M. Its Taylor degree is Q+40 and its explicit factorial remainder and pi uncertainty remain included. The inverse-root interval has endpoint error at most 2^(-Q). All subsequent operations are exact rational interval operations; there is no hidden floating tolerance or adaptive-precision oracle.

A fixed precision proof is as follows. For k!=0, the true denominator has magnitude at least 2/M and delta<1/M, so its entire interval is separated from zero. If n',d' are numerator/denominator endpoints, then

    |n'/d' - n/d| <= M^2 delta,  |n'/d'| <= M.

Combining with the root enclosure gives gain error at most 3M^2 delta and gain magnitude at most 2M. Combining that gain with a phase endpoint gives coordinate error at most 4M^2 delta. Every block's normalized value satisfies |a|<=R<=1, so |Re a|+|Im a|<=2. Exact multiplication by a therefore gives at most 8M^2 delta endpoint error per Cartesian component. Summing q block intervals gives at most 8qM^2 delta per component, and its complex half-diagonal is at most 12qM^2 delta.

Nearest-even midpoint rounding on the P-grid consequently has maximum complex endpoint distance less than

    rho/sqrt(2) + 12qM^2 delta
      <= rho/sqrt(2) + (48/2^20) rho < rho.

At k=0 the exact integer block sum has normalized Cartesian magnitude at most sqrt(N), by Cauchy-Schwarz. The inverse-root uncertainty gives a smaller radius, at most rho/sqrt(2)+sqrt(2N)2^(-Q). Thus the same precision suffices. The code additionally performs the exact squared complex-radius check for every returned coefficient. Rejection preserves the paid prefix; no certificate failure is relabeled success.

Unitarity implies |z_k|<=R<=1, hence |Z_k|<=1+rho. Every returned Cartesian numerator is strictly below the accepted every-tape cap 3M^2 2^P. Signed locations are reduced modulo M, sorted, and remain distinct by K<M/2. Zero-valued records are permitted; the candidate-list upper bound is exactly S=2K+1 and the nonzero support is at most S.

## 4. Recognition, source identity and finite domain

The original grammar has exactly m, F, kind and data. In kind='blocks', data contains (exclusive_end, real, imag) records, starting implicitly at zero and ending exactly at N. Every block is nonempty, adjacent values differ, and zero-valued blocks are allowed. In kind='dense', data is the actual array of N integer pairs; every entry is type/width checked and read, and maximal constant runs are recognized. At least one Cartesian integer in the original must be odd, making the common grid canonical. The all-zero case is outside this nonzero family and needs its own zero branch in any general dispatcher.

Exact built-in types exclude booleans, coercions and overloaded equality. Widths are inspected before copying numerical magnitudes. The immutable Source retains m,N,F, all block records, E,B,C,h,sigma and the representation consumed. This exactly reconstructs the admitted original and never aliases the caller's mutable array. A compressed descriptor has no dense-scan receipt. The 512-entry executed fixture is genuinely supplied and scanned as dense data, twice when source replay is requested.

The finite reference enforces 11<=m<=28, raw Cartesian width<=1024 bits, F encoding width<=128 bits, q<=64, C<=8, and N<=4096 for supplied dense arrays. |sigma|<=4m and K<M/2 are checked before numerical preparation. The mathematical theorem is not limited by those engineering ceilings, but the executable is. Raising the private recognizer's ceilings is not an assertion of tested all-length production coverage.

All dense entries must be read to certify the original's exact run list and energy. Otherwise an unread entry can be changed while the same recognition output is returned. This lower bound concerns complete recognition/source binding, not every possible approximation task. A changed last value need not be rejected merely because it is different: nonconstant originals are now allowed. Rejection controls must instead violate an explicit new contract, or comparison must detect a changed source.

Source replay calls this new provider afresh on the actual original, paying the entire recognition, normalization, precision preparation and coefficient construction again. It then recursively checks exact built-in type, field, integer width and value equality. The report separates replay production and comparison receipts. Median-only replay does not certify this source association.

## 5. Composition with the unchanged outer theorem

For D=5, beta=1/4 and d=4, the accepted outer parameters are

    t=160m+4 < M, eta=2^(-8m), b=ceil(9m/4), P=16m+16.

The adapter accepts the actual original grammar, invokes the new provider, optionally performs full source replay, copies the actual sparse pairs into one immutable estimate row, and pays the accepted median production and its mandatory replay. One-row Cartesian medians reproduce every supplied pair exactly. It constructs the accepted Outer and FullTransfer with the actual scale sigma, then calls FullTransfer.run and writes every one of the N outputs. No externally supplied estimate list or callback can replace this source path.

The accepted theorem therefore yields, deterministically,

    ||Y-U_N u0||_infinity
      <= [3t E_M + t eta(1+E_M) + 12*4^(-5m) + 2^(1-b)] ||u0||_2,

where E_M=4M^(-1/4). The new provider is stronger than that premise by a factor of four; the outer theorem is used unchanged. It remains a loose theorem at the small executed sizes. A sharper finite output certificate in this packet is a fixture result only.

The adapter carries the same immutable source and estimate objects into its output and preserves the accepted median/outer/transfer association. Single-use and output-substitution controls are paid. These are trusted-program invariants, not hostile-Python security guarantees or remote historical attestation.

## 6. Full recognition, arithmetic, replay and outer costs

Let W be the maximum raw Cartesian width, f the encoding width of F, and

    L=2+m+W+f.

Here q<=N, so endpoint, q, cutoff and loop-address widths are O(L). Fixed A is assumed for the sparse-size asymptotics; for a varying budget retain C and S=2C*2^ceil(m/4)+1 explicitly, with K<M/2. Normalization uses O(L)-bit integers, including E,B,C,h and the symbolic scale; enormous input exponents are not materialized.

Exact recognition by itself has safe schoolbook cost O(N L^2+q L^3) on a dense original and O(q L^3) on a supplied block descriptor. It stores the actual q-block descriptor, O(q(W+m)+f) bits. Dense recognition on a failing q-limit input can temporarily retain O(N) runs before rejection; its failure receipt and storage are not claimed to fit the accepted q bound.

At working precision Q=O(m), each finite trigonometric evaluation uses O(L) rational operations on O(L^2)-bit intermediates. This follows from the fixed-grid angle denominator, its powers, factorial and pi-series denominators. Conservative cubic-width primitive envelopes give O(L^7) bit work per trig evaluation. There are 2q+1 trig evaluations per nonzero retained coefficient, with all interval operations, root preparation, certificates, locations and records charged. Summing q block intervals does not create q unrelated denominator factors: all trig endpoints are on the same Q-grid, the only non-dyadic division factors are the two endpoints of the common sine denominator for this k, and the source uses one common dyadic grid. A common denominator formed from those two factors and powers of two has O(L) bits; the q-term numerator adds only O(log q) bits. Thus the O(L^2) intermediate-width bound remains valid even when q grows. Thus a safe complete bound matching the deliberately conservative global ledger is

    T_front_dense = O(N L^6 + q S L^7),
    T_front_blocks = O(q L^6 + q S L^7).

The global control envelope uses the largest reached rational width even for simple input visits, explaining N L^6 rather than a claimed intrinsic recognition lower bound of that order. These front asymptotic bounds assume a freshly initialized ledger. If a caller supplies an already accumulated Ledger, its previous numerical/event history and cumulative receipt remain present, and the actual reached history widths must be retained in the control envelope; an arbitrary prior ledger is not bounded by the new input parameter L alone. Nothing hides the q multiplier. One full source replay adds another whole T_front and its separately charged O((q+S+1) H_front^3) conservative structural comparison, where H_front includes actual operand and comparison-counter widths. For bounded W,f=O(m), a coarser O((q+S+1)m^6) covers that comparison. Original allocation, testing oracles, repeated reports, export and packaging are separate harness work.

The adapter source copy/association, estimate copying, one-row median producer and mandatory median replay add O((q+S+1) H^2) work and O((q+S+1)H) produced/retained bits, separately from the front costs. H includes actual source/data/address widths, previous history counter widths, and the logarithm of cumulative events, exactly as required by sources/OUTER_COST_ERRATUM.md. Prior receipts are preserved rather than reset. For general history, H must not be replaced by m without justification.

With fixed D,beta,d and O(m)-bounded original/history widths, the unchanged outer stage adds

    O(Nm^2 + S m^6),

including every one of E_outer<=St coefficient calls, setup, scatter, validation, scale-back and N output writes. Therefore for fixed variation budget C<=A and W,f=O(m), the conservative whole dense-original path, including a bounded number of complete source replays, is

    O(Nm^6 + q M^(1/4) m^7).

For fixed q this specializes to O(Nm^6+M^(1/4)m^7). For q=N it is larger and no near-linear or practical speedup claim is made. A supplied compressed original replaces the dense-recognition term with its actual q-dependent term. No free dense recognition, free oracle access, or all-length executable theorem follows.

Under the same bounded metadata conventions, new production peak data are

    O(Nm + Sm + qL + L^2) bits,

including source blocks, all median origins/rows, endpoint tables, N accumulators, N output records, scalar temporaries and associations. An independently retained dense caller array adds its actual O(N(W+m)) bits. The algorithm stores no E_outer-sized coefficient table. Keeping the independent direct-sum oracle's root tables and all checked rows adds separate harness storage. Cumulative produced/control bits and serialized report size are not peak production storage.

## 7. What the executable establishes

run_example.py executes the entire nonconstant 512-original path, including complete source replay and the accepted outer stream. It separately computes the actual centered target and original DFT by direct summation of every supplied raw coordinate. Those oracles use the preserved independent reviewer sine enclosure, a different pi identity, fixed-grid forward interval recurrence and an independent bisection inverse square root. They do not use the production block formula, variation tail estimate, production trigonometric code or outer coefficient iterator as their target oracle.

The original-target checker visits all N^2 direct-sum terms and all N output rows; the centered-target checker visits all MN direct-sum terms, checks every retained complex radius against rho, and checks every coordinate, including all omitted coordinates, against the squared universal premise by exact rational comparison. The harness tables, integer work and exports are additional work outside production receipts.

Read RESULTS.json, PROVIDER_CHECKS.json and TARGET_CHECKS.json for the completed measured run and exact finite certificate. fresh_checks.py provides grammar/variation/rejection controls and complex nonconstant coefficient checks. check_plans.py adds 44 allocation-free guard/precision plans through m=1024 and 12 exact affine-family energy/variation checks; these are expressly not numerical executions at those sizes. Process seconds and resident-memory observations are not complexity bounds. All sources and results are pinned by MANIFEST.json and SEAL.json after completion.

The contribution is a broader structured source theorem, finite certified provider and nonconstant end-to-end witness. General source-dependent unknown-support recovery, arbitrary-original coverage, general randomized amplification, an all-length dispatcher and ALG-034 remain open. No external write is part of this packet.
