# Sparse prefix Fourier endpoint bound and tour correction

Version 2026-10-10, source shared-scan package version 0. Mathematical status: independent scoped pass, with a necessary open/reset versus closed-cyclic correction.

For F_N=R G C, where G is one nonsingular scalar first-order weighted cyclic Green inverse, nnz(C)+nnz(R)=Omega(N log N/log log N). The result permits uneven endpoint degrees, zero recurrence weights and arbitrary latent length M. It bounds representation size and an executor that processes every scalar endpoint entry. An O(N log N/log log N) uniform construction is still conjectural; the supplied growing construction costs Theta(N^(3/2)).

For dyadic B, an open/reset Fourier-row tour needs (2B^2+1)/3 injections. A nonsingular closed cyclic tour instead needs (2B^2-2)/3 for B>=2. Both are quadratic.

## Proof of the uneven-degree bound

Let A=nnz(C), B=nnz(R), a=A/N and b=B/N. All endpoint matrices are fixed independently of the fresh input. Let K contain an element ω of exact order N.

Fourier is invertible over K: its rows are evaluations at the N distinct values 1,ω,…,ω^(N−1), giving a nonzero Vandermonde determinant. Therefore A≥N, B≥N and M≥N. In particular a,b≥1.

Set r=floor(2b). An output of degree greater than r has degree at least r+1>2b. Thus fewer than N/2 outputs have degree greater than r, and more than N/2 have degree at most r. This proves the source's Markov step even when the degrees are very unequal. For even N the stronger integer count is N/2+1; ceil(N/2) is a valid weaker count.

If r≥N, then B≥N²/2, which already gives the asserted asymptotic lower bound. Otherwise k=r+1≤N.

Consider the N cyclic windows of k consecutive input columns. Each input degree appears in exactly k windows. The average window degree sum is ka, so some window J has integer degree sum at most floor(ka). If f(J) counts nonzero forcing rows of C[:,J], then

    f(J) ≤ sum of the input degrees in J ≤ floor((r+1)a).

Write V=G C[:,J]. Between forced positions, the scalar recurrence is homogeneous. Each nonzero latent row is a scalar multiple of a row at a preceding forced position. Zero weights can erase a direction but cannot introduce another. There are therefore D≤f(J) projective directions.

The restricted Fourier matrix F_N[:,J] has rank k. Hence V must have rank at least k, and D≥k. It is useful to state this explicitly before padding supports to size r: it ensures D≥r+1 and makes the binomial count unambiguous.

Each low-degree output combines at most r latent directions and lies in the span of one r-element subset of the D directions. There are at most binom(D,r) such subspaces.

For the cyclic consecutive column window J, any k distinct Fourier rows are independent. Wrapping the column indices modulo N does not change powers of ω. Factoring out the initial column power leaves a Vandermonde matrix on k distinct values ω^i. Consequently a subspace of dimension at most r contains at most r restricted Fourier rows. The low-degree output positions need not be consecutive.

Combining these facts gives

    ceil(N/2) ≤ r binom(floor((r+1)a), r).

The transpose gives the companion inequality with a and b exchanged. Reversing the latent coordinate order converts G^T to another weighted cyclic recurrence, so the model is preserved.

Put q=a+b. Since r≥2, (r+1)/r≤3/2, and r≤2q. The elementary binomial bound gives

    log(N/2) ≤ log(2q) + 2q log((3e/2)q).

If q<log N, the right-hand side is O(q log log N); otherwise the desired lower bound is immediate. It follows that q=Ω(log N/log log N), and hence A+B=Ω(N log N/log log N).

No bounded-coefficient, positivity, prime-length or stability assumption is used. In particular, the argument does not assert the false statement that every minor of a composite-length Fourier matrix is nonzero.

## Exactly what is excluded

The theorem excludes a uniform O(N) explicit endpoint family and an O(N log log N) explicit endpoint family in this one-scan model. For the latter, the ratio of the claimed forbidden cost to the necessary scale is

    (log log N)² / log N → 0.

It excludes the corresponding running times when every stored scalar endpoint term is individually processed, as in the supplied executor. Increasing M cannot improve the endpoint inequality and only adds work to that executor.

It does not exclude:
- implicit endpoint algorithms with independently proved cheaper evaluation;
- multiple interacting scans or a general arithmetic DAG;
- approximation, finite-precision promises or sparse-input promises outside the contract;
- word operations that pack many scalar values or process vectors at unit cost;
- unrestricted exact FFT algorithms.

A fast method from one of these classes cannot be rejected merely by applying this endpoint-size theorem to an expanded representation.

## Precision and accounting

The algebra is over an exact field. Unit-cost field arithmetic is not a statement that arbitrary complex numbers occupy one finite machine word. An implementation claim should specify a field-element representation, coefficient and root generation, bit lengths, and precision/stability requirements separately.

Sparse indices require enough bits to address N and M, normally Θ(log(N+M)) bits per index. The stated word-work interpretation uses individually accessed scalar records and no uncharged packing. For a family meeting the conjectured size, M is itself near-linear, so ordinary O(log N)-bit indices suffice.

The instrumented apply count

    4M + 2(nnz(C)+nnz(R)) + 1

agrees with a static reading of the generic implementation. It counts multiply-by-zero/one and additions into zero too; it is a count of that evaluator, not an optimal arithmetic count. Cycle setup separately has M products, one subtraction and one inversion. Root preparation, endpoint generation, canonicalization, indexing and data movement must remain separate charges.

The cycle-to-prefix formulas are correct. With nonzero weights they add at most one read per output; broken cycles use segment-prefix differences and at most double output reads. The linear algebraic transformation is linear in the number of records. The generic Python constructor also calls sorted on sparse rows; for arbitrary unsorted records, a literal linear word-work claim needs a specified linear-time canonicalization strategy or an additional sorting charge. This is an implementation-accounting caveat, not a flaw in the normalization theorem. The supplied block constructor emits monotone endpoint indices, and its balanced construction bound is not invalidated by this caveat.

The source's 109 operations at N=8 are consistent with M=8, A=22, B=16. They do not establish a speed advantage over an optimized eight-point FFT.

## Correction to the exact tour statement

The corrected open-tour hypothesis is:

“Consider an open/reset scalar scan, starting from zero, whose B marked states visit the B Fourier rows once, allowing nonzero row rescaling.”

Under this restriction, the first row needs B injections and the source's exact minimum (2B²+1)/3 is correct for dyadic B. This is exactly the reset grammar used by block_tour_plan.

Without the open/reset restriction, the broad wording admits the nonsingular closed cyclic model introduced earlier. The package's own B=2 positive control already gives a counterexample: C=I has two injections, while the displayed open-tour expression equals three.

For a closed Hamiltonian Fourier-row tour on dyadic B=2^b, the exact minimum is instead

    (2B²−2)/3,   B≥2.

Here is a self-contained proof. A transition between different frequencies k and l can preserve at most gcd(k−l,B) coefficients, allowing arbitrary row scalings and recurrence multipliers. For each 1≤ell<b, the edges staying in one residue class modulo 2^ell form a forest: a proper subset of a Hamiltonian cycle cannot contain the whole cycle. Summing over the classes gives at most B−2^ell such edges. The cycle has B edges, so the total number of preserved coefficients is at most

    B + sum_(ell=1)^(b−1) 2^(ell−1)(B−2^ell)
      = (B²+2)/3.

This lower-bounds injections by B²−(B²+2)/3=(2B²−2)/3.

Bit-reversal order attains the residue-class bounds. Let ζ have exact order B. Use multiplier 1 on every nonwrap transition and multiplier ζ on the wrap transition from frequency B−1 to frequency 0. The latter frequency difference is 1 modulo B and preserves exactly one coefficient. The product of weights is ζ≠1, so the cycle is nonsingular. Defining injection rows as the differences between successive desired Fourier rows gives the stated exact count.

This corrected cyclic optimum remains Θ(B²). It does not modify the source's explicit reset-constructor count Q(2B²+1)/3 and does not supply a uniform near-linear Fourier plan. A collection of disjoint cyclic block scans is also not automatically one scalar cyclic scan.


## Evidence and prior work

Fresh exact controls checked 5,456 degree vectors, 30,944 window averages, 237 cyclic systems, 3,792 projective restrictions, 134 cycle normal forms and 51,404 Fourier minors; B=2,4,8 open/closed tour optima were checked exhaustively. The programs and mathematical result data are included. Original supplied programs remain source evidence, not newly executed performance measurements.

The Vandermonde ingredient is classical; see [Alexeev, Cahill and Mixon, Full Spark Frames](https://borisalexeev.com/pdf/spark.pdf). Green/quasiseparable structure is classical; see [Boito and Eidelman](https://arxiv.org/abs/2308.02701). Neither citation certifies priority of the endpoint synthesis or proves the conjectured upper bound.
