# Independent review of the Q16 exact centered source constructor

13 October 2026 UTC

## Verdict and scope

**REPAIR. The exact built-in input validator has two concrete type-identity defects.** Both can be corrected with a small local guard change and fresh adversarial tests. No numerical counterexample was found on the declared genuine built-in input domain. On that domain, the source-level normalization, zero handling, centered representation, precision bound and paid growing-word argument are accepted, subject to the existing fixed-d, trusted dependency, stable acquisition and finite-resource premises.

The reviewed candidate archive is Q16_Exact_Centered_Source_Constructor_Candidate_2026-10-13.zip, 81,643 bytes, SHA-256 a837bf0dfc376a6914e6fa3e75d10323766be41202a30e240eb85ccb2e446ae9. The constructor is src/exact_source.py, 8,862 bytes, SHA-256 d3dda699a77db8d80142bdd9d02f723707dc33d4bd318b93f08684077de38c82.

The required repair concerns the promised rejection boundary and exclusion of callbacks. It does not refute the previously accepted materialization lemma or sparse recovery theorem. The entire constructor should not be labeled independently accepted until a newly sealed revision closes this defect. This review neither modifies the candidate nor supplies an accepted replacement.

## Required repair at the two exact sites

At constructor line 102, the outer-container guard is:

    if type(values) not in (tuple, list):

At line 138, the cell-container guard is:

    if type(pair) not in (tuple, list):

Membership in a tuple uses equality, rather than exclusively identity. An object's class can have a metaclass implementing custom equality. That equality can claim the foreign class is equal to tuple and bypass either guard. Subsequent len and indexing operations then invoke the foreign object's protocols. A list subclass with such a metaclass is also admitted, contradicting the expressly promised subclass rejection.

A freshly authored standalone witness is:

    class CounterfeitMeta(type):
        def __eq__(cls, other):
            return other is tuple

    class ForeignVector(metaclass=CounterfeitMeta):
        def __len__(self):
            return 1
        def __getitem__(self, key):
            return (0, 0)

    value = ForeignVector()
    assert type(value) is not tuple and type(value) is not list
    assert type(value) in (tuple, list)

The independent checker executed this general Python-language witness, plus a foreign cell and a list-subclass witness. It did not import or execute the candidate. Its recorded calls show metaclass equality followed by foreign length and indexing. The candidate's source then supplies a complete static trace: for ForeignVector(), e=0 and d=1, the header obtains N=1, m=2, M=4; the scan receives the genuine pair (0,0), validates two zero integers, and reaches the successful zero result. No scientific dependency is needed on that trace. Likewise, a genuine outer list containing a foreign two-zero cell bypasses line 138. A foreign length method could instead raise or perform arbitrary work; the guard has already failed its promised isolation before that occurs.

This is not merely an absent rejection-time complexity guarantee. The contract explicitly restricts accepted containers to exact built-ins, rejects subclasses, and excludes user-defined sequence protocols. The malformed-field resource caveat cannot make equality-based acceptance satisfy those claims. The issue is not a change to the trusted import environment, monkey-patching or concurrent mutation; it is behavior of an ordinary supplied invalid object.

The minimal repair is identity-only rejection at both sites:

    if type(values) is not tuple and type(values) is not list:
        raise InputError('VECTOR_TYPE')

    if type(pair) is not tuple and type(pair) is not list:
        raise InputError('CELL_TYPE', validated, j)

The standalone controls confirm that these predicates reject the foreign witnesses without invoking their equality or sequence methods. The change adds only constant work. A proposed patch is provided as REPAIR.diff for review, not applied to the candidate.

Required regression coverage for v2: metaclass equality returning true, returning false, and raising; foreign outer containers; foreign cells after a genuine zero prefix; list and tuple subclasses with hostile metaclasses; ordinary exact tuple/list acceptance; and unchanged cell-prefix diagnostics. The adversarial equality and sequence hooks should raise if invoked, making their non-use an explicit assertion. Re-run the author's current complete fixture suite and reseal the source, tests and results. An independent delta review can then verify the guards and remaining claims.

## Genuine built-in validation and zero handling

Subject to replacing the two guards, or restricting this subsection to genuinely exact list/tuple inputs, the rest of the source validator is consistent with the stated domain. Scalar and metadata checks use identity, namely type(x) is int, so bool and integer subclasses cannot pass. Positive d and the exponent interval 0 <= e <= dm are enforced. N comes from the container rather than a separate header. The magnitude interval includes both endpoints, -2^(dm) and 2^(dm).

The complete scan is lines 135–172. Each real field is acquired, type checked and range checked before validated increments; then its absolute value updates maximum. The imaginary field receives the same sequence. Pair copies are made only after both scalar fields validate. A cell failure reports the count for preceding whole cells; an imaginary-field failure reports 2j+1. The scan has no successful early return or break. The only zero test lies after the entire loop, so a late invalid or late nonzero imaginary field cannot be hidden by a zero prefix.

The zero branch constructs N complex dyadic zeros with zero exponents and returns ZeroResult before the buckets import. It provides no k0, scale or nonzero promise. Exact Fourier zeros follow mathematically for the globally zero input. The retained pairs and output tuples isolate subsequent input mutations; concurrent mutation during acquisition remains excluded.

## Normalization, precision and centering on valid records

For A >= 1, k0=(A-1).bit_length() is the least nonnegative exponent with A <= 2^k0. At every exact power A=2^q it gives q, including A=1 and q=0. Consequently 1/2 < A/2^k0 <= 1 and 0 <= k0 <= dm. The erroneous A.bit_length() would lose strictness at exact powers; it is not used.

Writing S=sum_j(a_j^2+b_j^2), one attaining Cartesian field gives 4S > 2^(2k0), while all 2N bounded fields give S <= 2N*2^(2k0). Thus 1/2 < ||v||_2 <= sqrt(2N). The bound is Cartesian amplitude <= 1; complex amplitude may reach sqrt(2), which is consistent with the inherited source contract. No norm oracle, floating calculation or logarithmic approximation is executed by this normalization path.

The scale lambda is encoded by the signed exponent k0-e. Multiplication of the normalized exact dyadic by 2^(k0-e) restores the original x exactly. Negative scale exponents require no floating underflow or dense power representation. The source F is the numeric value k0, rather than a bit-count encoding of an arbitrarily huge exponent. Every cell exponent, including padding and zero components, is exactly F <= dm; all numerator magnitudes are <= 2^F. F=0 is valid.

For center=floor((N-1)/2), the occupied residue is (j-center) mod M. The implementation's inverse gather uses j=r+center and at most one subtraction of M, which is sufficient because 0 <= r+center < 2M. The test j<N selects exactly the N input images. Distinct input indices cannot collide, since N<M. The odd-N lifts are [-p,p] for N=2p+1; even-N lifts are [-p+1,p] for N=2p. Therefore |j-center| <= N/2 <= M/8, including the even right endpoint. The direction matches the accepted centered representation.

Fresh tuples hold all numerical container levels. The source output and intermediate retained pair copies hold only immutable exact integers; later list changes cannot change them. Frozen dataclass metadata is sufficient in the stated ordinary trusted model. Reflective mutation through object internals was explicitly excluded, and this review does not expand that protection.

## Pinned class identity and the execution boundary

The production constructor has no local DyadicSource class or user-supplied factory. Line 229 imports DyadicSource from buckets, and line 230 calls that imported object with (frozen, k0). The pinned historical buckets class is a frozen dataclass with exactly two ordered fields: values: tuple and fractional_bits_bound: int. Its hash is df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1. The pinned pipeline imports the same class and, like buckets, requires exact source type identity. Cell checks demand exact tuples, exact integers, exponents in [0,F] and amplitude bounds. The valid-domain constructor satisfies that schema.

This is a static same-class binding argument under the declared trusted import resolution. The runtime does not authenticate an arbitrary package by SHA-256. A fixture or same-named class cannot by itself pass the actual consumer. The candidate's tests explicitly put a newly authored class into sys.modules['buckets'] before loading the new constructor. Those tests can establish behavior with that fixture; they do not establish actual historical-class integrated execution. The candidate discloses this correctly.

Neither this review nor its fresh checker imports or executes the candidate, historical scientific modules, their tests, or previous review programs. No extracted function, AST interpreter or compiled candidate fragment is used. The production import and all consumer identity gates were inspected as text/AST. An actual pinned integrated conformance run remains unperformed and must not be represented as a completed execution result.

## Paid words, copies and bit cost

The event and allocation formulas agree with source inspection on successful genuine-built-in paths. Common work is 11N+4 events. The zero branch adds 3N+1, giving E=14N+5, A=256+11N slots and B=67+4N headers. The nonzero branch adds 7M+center+3, giving E=11N+7M+center+7, A=258+3N+8M and B=68+N+3M. The center subtractions occur for exactly center residues. Both temporary lists and final tuple reference copies are included. No zero interning or free outer freeze is assumed.

With H=(dm+m+16)^2 and the additional fixed margin, these formulas yield U_zero=29N+584+H and U_nonzero=15N+18M+center+589+H. The source meters macro events, not literal Python bytecode instructions. Its fixed factor 1024 and bookkeeping margins are interpreted as a conservative elementary source-model realization, not a measured interpreter bound or formally verified allocator count.

For m>=4, m^2<=2^m=M<8N; m=2,3 satisfy m^2<=8N directly. For m>=2, dm+m+16 <= (d+9)m. Thus H <= 8(d+9)^2 N. Along with M<8N and center<=N/2, both U formulas satisfy U <= [750+8(d+9)^2]N. Header preparation, bit scans, fixed-size event accounting and receipt arithmetic receive one-time metadata work. They are not uncharged per-coordinate polynomial work.

The word width W=64+(d+16)(m+1) accommodates a fixed d-dependent number of ordinary growing words per field and index. For fixed d, this proves O_d(N) growing-word work and cumulative storage. The conservative local random-access bit simulation costs O_d(Nm^2), and cumulative represented storage costs O_d(Nm) bits. This is not O(N) bit work or storage, not a one-tape memory-access bound, and not a CPython heap or speed certificate. Source construction remains additional to the sparse theorem's own auxiliary resource bound.

The identity-only repair preserves these asymptotics and has ample constant budget. Until repaired, the resource argument and no-callback claim must not be extended to counterfeit containers that the current guards erroneously admit.

## All sizes, practical caps and inherited prerequisites

The all-size statement is an abstract finite source-level construction for each fixed d and every finite valid N, with sufficiently large finite resources. It does not certify one Python host for arbitrary lengths. The separate practical wrapper freezes N<=65,536 and d<=8, so m<=18, M<=262,144 and dm<=144. These caps neither prove a practical speed promise nor limit the unrestricted mathematical theorem.

The candidate records 8,213 valid fixture cases, 62 rejection cases, 13 ordinary zero cases and a separate zero-import check; its reported maximum practical case is instantiated by the producer. This reviewer did not rerun that producer suite or independently execute the candidate at the cap. Those results are retained as candidate-authored evidence, not relabeled independent execution.

The accepted sparse bridge and materialization review were read and source-bound. The constructor supplies the source-side promises on its genuine valid domain: global validity, immutable centered representation, R>1/2, Cartesian magnitudes <=1 and numeric F=O_d(m). Applying sparse recovery additionally needs fixed rational beta in (0,1/2), the exact source guards B|M, B>=4, T>=4, B>=4096k and W<M, the pinned numerical contracts, and an independent uniform tape. It does not follow from source construction alone.

The outer theorem retains fixed 0<alpha<beta<1/2 and the additional outer transfer conditions such as beta*m>=2 and t<M. lambda is a normalization scale, not a revised alpha. No claim at alpha=1/2, exact DFT, relative-l2 recovery or new Fourier exponent is accepted here.

## Independent controls, evidence integrity and remaining gates

The new reviewer program reports 161,701 passed assertions, 1,876 fresh exact mathematical model cases and 1,548 metadata-only boundary cases through m=8192. These compare independent power-doubling/forward-scatter models with declarative inverse-residue formulas, verify strict squared-norm and exact scale identities, reconstruct pass inventories and check envelopes. No enormous corresponding vector is allocated in metadata controls. The three adversarial type witnesses are reproduced, and the proposed identity predicates reject them without invoking protocols. Finite models corroborate arithmetic; source inspection and the universal arguments establish the valid-domain result.

Integrity checks verify the candidate archive hash, CRC, 34 unique members, all 33 manifested payloads and seven provenance records. The accepted sparse review is byte-equal to the separate acceptance archive, SHA-256 4ebd428764c96ec2c233db76604fc47b3705fa3489850ab0b2a468c7a3f17333. The historical sources are checked against its nested frozen bridge archive, SHA-256 55c074877d47b7c0f8d0d6f5f1394005b650ff29a428b9180e6de34d488d5f6f. The materialization lemma matches the independent gap-ledger archive, SHA-256 1248773169d32ed606b2750843d6cf9992840dde2eb86ca974ed8637003d330e; the copied materialization review matches the supplied original, SHA-256 597542bc5a30d6fc2b023c40817e0433d758b7c1fd647ad74f98abeacfcb71da.

Immediate gate: repair both equality-based container guards, add adversarial regressions, reseal and obtain independent delta acceptance. After that, the declared source-level input constructor can be accepted without claiming an integrated replay was performed.

Remaining expanded executable gates are unchanged: actual source-pinned full-path conformance; exact all-length dispatch and a certified dense fallback; active interpolation coefficient generation and scatter; finite accumulation, final rounding and scale-back; fresh J-call outer amplification; and complete end-to-end input/output accounting. Physical entropy, host exhaustion, general text parsing and practical performance remain separate claims. No Sheet, repository, accepted scientific source, publication, sharing setting or external state was changed by this review.
