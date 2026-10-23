# Paid cold and warm costs for the first-order support construction

23 October 2026. Companion to THEOREM.md. The changed theorem reduces the NUMBER OF ORIGINAL BANKS, not the arithmetic order of the literal evaluator. This ledger reproduces and rechecks the accepted conservative cost model with d=floor((N+2)/6) (or arbitrary d>=4,N>=6d-2).

## 1. Input and units

Input: odd N>=23, a certified representation of F_Q, and supplied q of exact order N. Let m=N-d, B=2m+2, E=F_(Q^2), R=Q^2, s=dim U-1<=m, H=d(d+1)+2m-1, and t=m!. Verify q's exact order by successive powers up to N in O(N) base arithmetic, without an integer-factorization oracle. Provisioning q or an uncertified starting field is an additional task, not hidden in the bound.

Count field additions, multiplications and inversions separately; coefficient reads/writes, address updates, storage and all outputs are charged. No machine word is assumed to hold Q, R, m!, or a complete extension-field element. For infinite input fields the theorem is an algebraic existence/construction statement, not an unqualified finite bit-complexity guarantee.

## 2. Coefficient-field preparation

Find an irreducible monic quadratic over F_Q by enumerating at most Q^2 candidates and testing all Q possible roots for each: O(Q^3) base operations/comparisons. A quadratic with no root is irreducible; finite-field existence guarantees termination. Store its two coefficients, and use the resulting polynomial-basis E/F_Q representation. Multiplication/reduction and addition have O(1) base-operation cost at this degree. Inversion can use extended Euclid with paid base inversions or O(log Q) E multiplications by exponentiation; do not silently change conventions.

If F_Q=F_p[z]/P has degree e, supplied certified P is part of the input interface. Schoolbook multiplication/reduction costs O(e^2) F_p operations, addition O(e), and inversion by exponentiation is bounded by O(e^3 log p) F_p operations. Initial representation/certification is not declared free if it is not supplied.

## 3. Envelope, affine slice and all failed candidates

Prepare q powers, Gaussian factors, D values, and E using O(N^2) entries. The unchanged envelope/nullspace and monic affine parametrization cost O(N^3) field arithmetic, O(N^2) storage, and O(N) pivot inversions. The first-order support proof is an existence certificate; no additional runtime black box is required.

For each affine point, construct g, check c_0!=0, compute gcd(g,g') by Euclidean division, form p_j=t^j mod g for 0<=j<N, and rank-test the N by (2m+1) axis matrix. Building all remainders costs O(Nm). A conservative whole candidate test costs O(N^3) E operations, O(N) inversions and O(N^2) storage, including failed tests.

- Deterministic: enumerate R^s affine points, giving O(R^s N^3) E arithmetic, or enumerate an explicit (H+1)-element scalar grid in each coordinate, giving O((H+1)^s N^3). H<R ensures that grid exists; preparing it costs its actual element writes.
- Las Vegas: sample s independent uniform E elements each trial. The proved rejection bound H/R<1/2 gives expected fewer than two candidate tests after field and affine preparation, hence expected O(N^3) E arithmetic. Each trial also costs s element writes and expected O(s log R) unbiased random bits via rejection sampling. Every candidate is verified exactly. This is not a deterministic two-trial cap, nor a statement about nonuniform heuristic sampling.

At this stage only g's coefficients are available. No physical root or bank has yet been produced.

## 4. Genuine splitting field and roots, without an oracle

Every irreducible factor degree r of squarefree degree-m g has 1<=r<=m and divides t=m!, so all roots lie in L=F_(R^t). The actual minimal finite-field splitting degree is their lcm, not automatically t. No polynomial bound in N is asserted.

An explicit, deliberately astronomical construction is:

1. Enumerate at most R^t monic degree-t polynomials over E.
2. For each, divide by every monic polynomial of degrees 1 through floor(t/2). There are fewer than 2R^floor(t/2) such divisors; a reducible polynomial has an irreducible factor in this range.
3. Each division costs O(t^2) E arithmetic. Thus O(t^2 R^(t+floor(t/2))) E operations guarantee a degree-t irreducible modulus. Store its t coefficients and use the polynomial-basis field L/E.
4. Enumerate all R^t elements of L and evaluate g by Horner. This costs O(m R^t) L multiplications/additions and finds all m roots. Verify their count, distinctness, nonzeroness, and product polynomial. No formal roots, derivative nodes or factorization oracle replace this stage.

With schoolbook polynomial arithmetic, an L multiplication/reduction costs O(t^2) E operations, an addition O(t), and inversion by exponent R^t-2 costs O(t^3 log R) E operations. Root enumeration alone costs O(m t^2 R^t) E arithmetic. Every L element has 2t base F_Q coordinates. Better proven factoring/extension algorithms may replace this ledger only with their own explicitly charged contracts; none is assumed here.

## 5. Amplitudes, raw weights and operator preparation

All arithmetic in this section is in the ACTUAL root field L.

- Build the two Vandermonde matrices for exponents 0,...,m-1 and 1,...,m; the latter differs by nonzero column scales. Invert one in O(m^3) arithmetic and O(m) inversions, then pay for scaling.
- For each positive row, pad and recover left/right moments with this inverse, using O(Nm^2) total arithmetic across sectors. Reflect with paid assignments. Prepare Fourier/Gaussian arrays in O(N^2) arithmetic/divisions. Optional direct checks of all recurrences cost O(N^3).
- Solve the axis by ordinary elimination in O(N^3) arithmetic, O(N) inversions; convert moments to root amplitudes by the same Vandermonde inverse.
- Recover all BN raw weights by direct length-N sums: at most BN^2 multiplications and BN(N-1) additions, plus O(BN) scaling. Prepare gamma, Delta, 1/N, alpha inverses and powers, paying every inversion and write. Normalize weights by 1/N with BN multiplications after one inversion.
- For each bank precompute the N values (1-q^k)/alpha and alpha^-1, shared between its branches by phase-index permutation, in O(BN) arithmetic and B inversions.

Thus post-root construction costs O(N^3) L arithmetic, O(N^2) L storage, and the stated paid inversions. None of these cold costs is included in the warm application count.

Optional literal dense inverse verification can stream BN branch matrices and solve N right-hand sides each by the sparse recurrence below in O(BN^3)=O(N^4) L operations, check both inverse products and the final aggregate. Storing all inverses unnecessarily would take O(BN^3) field elements. The fresh finite controls do NOT claim to have run the huge root-field construction or this full literal verification.

## 6. One warm literal application, all N outputs

For beta=1, v=Q_j^(-1)x satisfies

    (1-q^(epsilon delta j+delta i))v_i-alpha v_(i-epsilon)=x_i.

There is one zero diagonal at i_0=-epsilon j mod N. With prepared a_(j,i)=(1-q^(epsilon delta j+delta i))/alpha, compute b_i=-x_i/alpha once per bank in N multiplications. The zero-diagonal equation gives v_(i_0-epsilon)=b_(i_0); traverse the other N-1 indices backwards in epsilon via

    v_(i-epsilon)=a_(j,i)v_i+b_i.

Each branch takes N-1 multiplications and N-1 additions. Weight all N outputs by stored w_j/N, then sum N branches. Per bank this totals

    2N^2 multiplications,
    2N^2-2N additions.

For all B banks, including final bank accumulation, the complete conservative budget is

    2BN^2 multiplications,
    2BN^2-BN-N additions.

It includes every output coordinate and does not exploit zero/unit weights. Branch output buffers can be reused. Index updates, input/weight reads and accumulation writes cost O(BN^2); the input and output each require N field-element reads/writes. Working buffers cost O(N) field elements on top of O(BN) prepared operator data.

With B~5N/3 this warm schedule is still O(N^3) in the possibly huge field L. Its leading multiplication bound changes from approximately (7/2)N^3 to (10/3)N^3 under this particular literal implementation, but neither is an FFT improvement: ordinary dense Fourier multiplication over the original base field already takes N^2 multiplications and N(N-1) additions after coefficient preparation.

Base expansion costs O(BN^2 t^2) E arithmetic for L multiplications and O(BN^2 t) for additions, then the E/F_Q and possible F_Q/F_p costs apply. Raw weights require BN*2t base coordinates, or Theta(BNt log Q) bits. All outputs require N*2t base coordinates unless a separately paid descent compression is used. For base-field input the proven Fourier identity implies base-field output; verifying and removing its zero extension coordinates costs O(Nt) base-coordinate checks, not a free identification.

## 7. Boundary

Included: field representations, all failed coefficient candidates, actual splitting-field preparation, all roots, all amplitudes and raw weights, literal admissibility, full-output application, inversions, storage, indexing, and base-field expansion. Not claimed: efficient root finding, polynomial extension degree, practical FFT benefit, numerical stability, optimal bank count, or historical priority. The only improved asymptotic object is the proved count of original signed banks.
