# A complete finite original signed-bank realization

23 October 2026. Exact finite execution, not a new uniform theorem or a speed claim.

## Outcome

The already accepted N=19, d=4, m=15 fixture has now been realized end to end in an explicitly represented field of degree 22 over F191. Its 15 distinct nonzero roots were recovered. Every one of the 32 original signed banks has a nonzero raw-weight vector (604 of the 608 individual raw weights are nonzero). The 608 internal resolvents, not 608 banks, were explicitly constructed and archived. All 438,976 entries of their two inverse identities and all 361 entries of their complete weighted sum were checked exactly. The weighted sum equals the negative unnormalized Fourier matrix q^(-at), q=5.

The independent reviewer is separately recomputing the archived inverse matrices by a different method; this author report does not itself grant independent acceptance.

## Frozen origin and exact grammar

FROZEN_INPUT.json freezes fixture 0 of the accepted endpoint independent CONTROL.json. The coefficient data were read as data. No prior author or historical mathematical script was executed. The original contract is the endpoint THEOREM.md, sections 1 and 8, and its bound source WHOLE_LEFT_RANK_ENVELOPE.md. Source hashes are in SOURCE_BINDINGS.json.

The physical object used, with S e_t=e_(t+1), T e_t=q^t e_t, is precisely

    B_(eps,delta)(alpha,1;w)
      = (1/19) sum_(j=0)^18 w_j
          [I-alpha S^eps-q^(eps delta j) T^delta]^(-1).

There are 15 (++ ) banks at the roots of g, 15 (-- ) banks at the same roots, and the two singleton (-+) and (+-) banks at alpha=1. All beta values are 1. All alpha values and Delta=1-alpha^19-1=-alpha^19 are nonzero. No physical zero node, derivative atom, trace, mask, product bank, new generator, or direct-Fourier replacement is used. Solving coefficient equations during setup does not replace the application operator.

The ascending coefficient vector is

    [84,93,116,164,163,51,158,162,28,105,119,186,101,82,106,1].

## The actual splitting field, not a root oracle

Exact factorization over F191 gives

    g=(t+62)(t-1)(t^2+78t+121) f11(t),
    f11=t^11+158t^10+43t^9+32t^8+42t^7+173t^6
        +183t^5+33t^4+17t^3+153t^2+48t+175.

The final reproducible factorization uses installed SymPy 1.14.0 with the deterministic Berlekamp method explicitly selected. It took about 0.009 seconds in the recorded run. Its polynomial-level instrumentation records 123 gcd calls, of which 120 returned a constant or the complete input polynomial, and 680 division/remainder calls. Every gcd input/output degree triple is retained. Per-base-operation counts inside SymPy are not measured and are not declared free. An earlier exploratory run used the installed Cantor-Zassenhaus default; its internal random retries were not instrumented, its approximately 0.004-second wall time is disclosed, and no deterministic bound on that exploratory work is claimed.

Fresh modular polynomial code separately verifies the factor product and Rabin irreducibility criterion for the degree-2 and degree-11 factors. It checks t^(191^r)=t modulo each degree-r factor and the required proper-degree gcd conditions. The full residues are in FIELD_CERTIFICATE.json.

Set

    L = F191[A,B]/(f11(A), B^2+78B+121).

The finite-field extensions of degrees 11 and 2 intersect only in F191, since gcd(11,2)=1. Thus this 22-dimensional tensor algebra is a field, not a product ring. The irreducible degree-11 factor remains irreducible over F191^2. The field size is 191^22, namely

    152311985478009383067227682495511875196478871953281.

Every element is represented by 22 actual base-field coordinates in the ordered basis

    [1,A,...,A^10,B,AB,...,A^10 B].

The complete ordered root list is 129, 1, B, B^191, A, A^191, ..., A^(191^10). These powers were actually computed in this field. Both Frobenius orbits close at their stated lengths, every root is nonzero and distinct, every g(root) is zero, and the product of all 15 linear factors reconstructs g coefficient by coefficient. This proves that 22 is the minimal splitting degree for this particular base-field polynomial: both irreducible degrees must divide a splitting degree, and their least common multiple is 22. It is not a generic bound for this family.

BANK_DATA.json contains all 15 root coordinate vectors, all 32 alpha inverses, all Delta values, all amplitudes, gamma=157, and all raw weights. No new coefficient or modulus search was needed. Existing accepted coefficient data were used once; new coefficient candidates and rejected new coefficient candidates are both zero. Development and exploratory costs are separately disclosed in DEVELOPMENT_LOG.json.

## Amplitudes, weights, and exact physical construction

For each Fourier sector b=0,...,18, the code builds the original 19-by-32 Weyl coefficient equations

    sum_k G_(eps_k,delta_k)(a,b) alpha_k^[eps_k a]_19
          h_(k,[delta_k b]_19) = q^(5(a+b)^2),

where G is the supported Gaussian coefficient of the original grammar. Ordinary exact elimination solves these equations, with free variables set to zero. All 19 equations in each sector are then explicitly re-evaluated. Sector ranks are

    [19,17,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,17].

Only the axis sector is required to have full row rank. The two rank-17 sectors are consistent because of the original recurrence restrictions; falsely requiring their full row rank would be stronger than the theorem. There are 355 nonzero sector amplitudes among the 608 slots.

The raw weights are computed, without FFT, by the complete sums

    w_(k,j) = gamma Delta_k sum_(ell=0)^18
                h_(k,ell) q^(-eps_k delta_k j ell),
    gamma=(1/19) sum_(t=0)^18 q^(-t^2)=157.

All 608 character-inversion identities are separately checked.

For each actual bank and actual phase j, define the literal sparse matrix Q_j. Its row equation is

    (1-q^(eps delta j+delta i)) v_i-alpha v_(i-eps)=x_i.

There is exactly one zero diagonal, at i0=-eps j modulo 19. The code starts with v_(i0-eps)=-x_i0/alpha and traverses the remaining rows backwards using this exact equation. It does this for every one of the 19 standard basis right-hand sides, obtaining the entire 19-by-19 inverse, not only a coefficient proxy. It then multiplies by Q_j on both sides and checks every entry against the identity matrix.

Every completed inverse is stored before moving to the next phase. The complete original physical sum (1/19) sum_(k,j) w_(k,j) Q_(k,j)^(-1) is accumulated entry by entry and compared to q^(-at). The target Fourier matrix is used only as the equality target, not as the constructed operator.

RESOLVENT_INVERSES.u8 is a complete uncompressed coordinate archive. Its axes, from slowest to fastest, are bank index 0..31, phase 0..18, row 0..18, column 0..18, and field coordinate 0..21. Each coordinate is an unsigned byte from 0 through 190. The file has exactly 4,828,736 bytes. BANK_DATA.json uses the same bank and coordinate ordering.

## Full application and mutation controls

PREPARED_DATA.json stores the actual ratio table (1-q^s)/alpha and normalized raw weights w_j/19. A separate complete warm application runs the original sparse solves on a vector with genuinely mixed extension coordinates and checks all 19 outputs against the independently formed Fourier target. APPLICATION.json archives the entire input, actual output, and expected output. The matrix identity already covers every possible input, and this application additionally checks the runtime schedule.

Executed mutations:

- Add 1 to the first raw weight: 190 entries of the physical matrix identity change and the mutation is rejected.
- Add 1 to entry (0,0) of the first stored inverse: one entry of its left inverse product fails.
- Shift the physical phase of the first bank by one while retaining its weights: all 19 outputs of the mixed-field input test change.
- Substitute a zero node: inversion is explicitly rejected.

The normal optimized build and a separate -O0 build with standard-library bounds checks and undefined-behavior sanitizer produce identical bank data, prepared data, inverse archive, applications, sector ranks, and operation/check counts. Runtime values alone differ. Explicit require checks are not compiled away under optimization. REPLAY.json records this comparison.

## Costs actually paid, and what was not claimed

The final exact C++ execution took approximately 0.43 seconds on the available cloud environment, excluding compilation and the separately measured factorization/preparation process. Its measured maximum resident set was 9,344 KiB. These are observations for one tiny fixture, not a benchmark or a complexity improvement. Successful runs, exploratory attempts, and development failures are distinguished in the logs.

Field API counts in the frozen optimized execution:

- Field/root preparation and arithmetic controls: 15,634 multiplications, 662 additions/subtractions, 44 inversions.
- All amplitudes, raw weights, checks, and warm preparation: 291,252 multiplications, 126,195 additions/subtractions, 357 inversions.
- All literal inverses, both inverse products, and the complete weighted matrix sum: 1,755,904 multiplications and 877,952 additions/subtractions, with no additional inversions.
- One actual prepared warm application, all outputs included: 23,104 multiplications and 23,104 additions/subtractions, no inversions.

The warm addition count includes 608 explicit input negations and additions into initially zero output accumulators. It is intentionally not identified with the more optimized 22,477-addition schedule in the theorem ledger, which was not executed here. The multiplication count matches 2BN^2=23,104.

The direct per-sector elimination used here is a simple auditable finite implementation and can cost O(N^4) post-root field arithmetic as N grows. It does not implement or improve the theorem's more structured O(N^3) amplitude construction. Dense archived inverse verification also costs O(BN^3). Only the warm original-bank schedule has the familiar O(BN^2) arithmetic count, cubic when B is proportional to N.

Each generic L multiplication is explicitly expanded into at most 746 F191 multiplications, 746 F191 additions/subtractions, and 42 modular reductions in the written schoolbook tower kernel. A base-scalar multiplication uses 22 base multiplications. An L addition/subtraction uses 22 base operations. Inversion is exponentiation by 191^22-2: 167 exponent bits, 166 squarings and 90 multiply steps, followed by a product check. It is not a unit-cost black box. All 401 successful L inversions are verified; the 402nd counted inverse call is the deliberately rejected zero-node mutation.

The complete run, including arithmetic controls and mutations, instruments 476,523,043 base multiplications, 465,791,071 base additions/subtractions, and 82,113,214 modular reductions. These are counts of the explicit arithmetic kernels and instrumented scalar helpers, not claims about CPU instructions. Coordinate comparison-read upper bounds, indexing, array initialization, file encoding, allocation, and I/O are additional work. The full run has 488,654 explicit require checks. The separate SymPy preparation is not included in these kernel totals and is charged above.

Storage is also expanded. One field element is 22 base coordinates, not one arbitrary-size machine word. The C++ representation uses 22 ordinary 32-bit ints (88 bytes); the archive uses 22 bytes per element. Raw weights alone use 608*22=13,376 base coordinates. Prepared ratios plus normalized weights use 1,216*22=26,752 coordinates, in addition to node inverses and buffers. A streamed inverse or a complete 19-by-19 matrix uses 7,942 coordinates; all stored inverses use 4,828,736 coordinates. A full input or output vector uses 418 coordinates. Every archived coordinate was written, and every final matrix coordinate compared, including the extension coordinates that must vanish. Coordinate addressing/copying is O(22^2) per generic multiply and O(22) per add, rather than being encoded into a free large integer.

No FFT speedup, numerical claim, asymptotic arithmetic improvement, generic small splitting degree, minimum bank count, or novelty claim follows from this fixture. Dense Fourier multiplication over F191 already takes only 361 base multiplications for base-field input. The result closes the specific implementation gap between accepted coefficient-only tests and one complete finite instance of the original physical grammar.

## Reproduction

Run only the new source files supplied in this artifact:

    python prepare_field.py
    g++ -O2 -std=c++17 -Wall -Wextra -pedantic realize.cpp -o realize
    ./realize .

No network, account access, installation, historical script, or external write is required. All input is local frozen data. The complete artifact hashes are recorded in MANIFEST.json.
