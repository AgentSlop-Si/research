# Necklace–Green Fourier transport
## Explicit short-orbit Hessians, a locality obstruction, and an unproved exact FFT factorization

**Date:** October 10, 2026.  
**Status:** Exact auxiliary algorithms, proved algebraic and cost statements, nine executed verification groups, and a specific unconstructed Fourier factorization. **No new exact sub-N-log-N Fourier algorithm has been obtained. External publication novelty is unconfirmed.**

## 0. What this attempt adds, and what it does not

The preceding marked-cycle proposal has an exact Fourier identity but leaves a fast input-dependent marked evaluator missing. The sparse-jet proposal has a valid Hessian compiler but no fast Fourier-compatible scalar source. The shared-scan proposal has an explicit evaluator but unconstructed sparse endpoint maps. This note combines the first two with a different, explicitly executable family of scalar sources: polynomial sums over rotational classes of short binary closed walks, with arbitrary edge weights.

Two unconditional deductions are supplied:

1. All traces of a weighted binary de Bruijn matrix through length log2(N)+c can be evaluated in O(N*2^c) exact scalar/word work, including the circuit/address construction. This remains true when every edge weight is an independent variable. Fixed c gives O(N), not merely an input-independent scalar precomputation.
2. The Hessian of one length-k orbit potential is local in edge coordinates. Each row has at most k*2^max(0,k-log2(N)-1) potentially nonzero entries. A sparse marking with at most s entries per column and d per row therefore cannot produce Fourier unless s*d*k*2^max(0,k-log2(N)-1) >= N.

For nonzero baseline weights, the Hessian also has an explicit diagonal-plus-sparse-Gram evaluator. The conjectural synthesis target places a dense but linearly applicable Green transport around that carrier. The resulting Hessian-vector algorithm is complete and tested as an operator evaluator; the growing parameter family making its operator equal Fourier is not supplied.

The classical ingredients include FKM necklaces, periodic-orbit trace identities, scalar automatic differentiation, and cyclic Green recurrences. The algorithmic combination and the particular locality statement are project deductions, not claims of historical priority.

## 1. Arithmetic contract

N=2^n, n>=1. Work over C with a supplied primitive N-th root omega, or over a field with such a supplied root. Fourier means the unnormalized symmetric matrix

    F_N[i,j] = omega^(i*j).

There is no conjugation in a Hessian or congruence P^T H P. The target is every N-vector and all N explicit scalar outputs, not amplitudes of a quantum state, sparse input, a cached spectrum, or an approximation.

Field addition, subtraction, multiplication, and inversion of a verified nonzero input-independent scalar are charged. Indices have O(log N) bits. Reads, writes, enumeration, parameter generation and root tables are charged. No arithmetic instruction operates on an unpriced matrix or polynomial register. The finite-field Python integers are verification devices; this is not a fixed-modulus asymptotic statement, bit-complexity result, or floating-point stability theorem.

Circuit construction in this note is uniform once the parameters are supplied. A Fourier claim additionally requires a uniform parameter generator within the advertised cost; an expensive separate solution of polynomial equations at each N does not qualify.

## 2. A weighted binary graph

There are N vertices, indexed by n-bit words, and 2N directed edges. Edge (s,b), b in {0,1}, maps

    s -> (2s+b) mod N.

Let its weight be w_(s,b), and let B(w) be the adjacency matrix under the column-source convention:

    B(w)e_s = w_(s,0)e_(2s mod N) + w_(s,1)e_((2s+1) mod N).

The weights are arbitrary field values, including zero. At

    gamma_(s,0)=1, gamma_(s,1)=omega^s,

this is exactly the preceding fixed-graph Fourier operator Q_N. That earlier Fourier relation motivates the choice; no fast Q_N^n application is assumed here.

### Closed-word identity

Fix a length k>=1. A binary word b_0,...,b_(k-1) determines a unique closed walk: before appending b_0, its state is the n symbols immediately preceding b_0 in the infinite periodic extension of the word. Explicitly, build that state from b_(-n),...,b_(-1), taking indices modulo k. Appending the k bits returns to the same state.

Conversely, any closed length-k graph walk supplies that periodic word. Thus the 2^k binary words index the terms in tr(B(w)^k).

A binary necklace is a word modulo cyclic rotation. If C has least period r_C dividing k, there are r_C distinct rotations, not necessarily k. Their edge products agree because field multiplication commutes. Therefore

    tr(B(w)^k) = sum_(C in necklaces(k)) r_C * product_(e along C, with multiplicity) w_e.       (2.1)

This is a polynomial identity over the integers, hence remains valid after field reduction. Periodic-word multiplicities are essential: the constant word contributes one w_loop^k term, not k such terms.

## 3. Fully charged short-orbit evaluator

Let L(k) be the number of binary necklaces of length k. Primitive words contribute at most 2^k/k necklaces. Nonprimitive periods are at most k/2, so

    L(k) <= 2^k/k + sum_(d<=k/2) 2^d <= 2^k/k + 2^(floor(k/2)+1).      (3.1)

FKM generates necklaces in constant amortized time; our implementation copies each output word explicitly, charging O(k). Building the initial n-bit state costs O(n) integer operations. Following the k edges, multiplying their weights and adding the contribution costs O(k). Thus one trace has cost

    O((n+k) L(k)).                                                    (3.2)

No canonical-rotation test is run on all 2^k words in the actual evaluator. Such a brute-force generator with an O(k) rotation test per word would lose the desired saving; it appears only as a small independent test.

### Theorem 1 — all short traces

For K=n+c with integer c>=0, all

    tr(B(w)),...,tr(B(w)^K)

can be evaluated and their scalar circuits constructed in

    O(2^K) = O(N*2^c)                                                  (3.3)

field/word operations, with O(N*2^c) stored circuit nodes, or O(N+K) streaming workspace for scalar values alone.

**Proof.** Sum (3.2) and apply (3.1). The elementary geometric-tail estimate

    sum_(k=1)^K 2^k/k = O(2^K/K)

gives O(n*2^K/K+2^K) from the primitive terms. Nonprimitive terms cost at most O((n+K)*2^(K/2)). Because K>=n and K=O(2^(K/2)), this is O(2^K). The N input weights and outputs/preparation scans fit the same bound. FKM generation and word copying have already been included. QED.

The proof also covers a single length K, or arbitrary input-independent coefficients alpha_C in place of r_C, provided generating all coefficients is charged within O(2^K).

### Determinant prefix consequence

When characteristic is zero or exceeds K, Newton identities compute det(I-tB(w)) modulo t^(K+1) from those traces in O(K^2) further scalar operations. Since K^2=O(2^K), the same cost bound holds. This is an auxiliary determinant-prefix result; it is not a fast determinant for an arbitrary matrix or a full Fourier output algorithm. The new code directly checks trace values, not an additional full determinant-prefix implementation.

## 4. A concrete scalar source and its Fourier conversion

For a fixed horizon k=n+c, fix the input-independent necklace coefficients alpha_C and define

    Psi(w) = sum_C alpha_C product_(e along C) w_e.                     (4.1)

Let gamma be a prepared baseline, and let P:K^N -> K^(2N) be a prepared linear map with application and transpose costs W(P). Define

    Phi(z) = Psi(gamma+Pz),
    H = Hessian_w Psi(gamma),
    T = Hessian_z Phi(0) = P^T H P.                                    (4.2)

All scalar source operations are polynomial in z; there are no divisions by z-dependent expressions. Zero gamma entries cause no singularity in this circuit.

### Theorem 2 — exact compiled transport

The operator Tx is computable for every fresh x in

    O(N*2^c + W(P) + parameter preparation)                            (4.3)

field/word work. An append-only compiled implementation uses storage of the same order.

**Proof.** Emit P as a scalar circuit, add gamma, and emit the orbit products. Apply forward directional propagation and reverse directional-adjoint propagation to compute Hessian(Phi)(0)x without forming that Hessian. Every scalar gate induces a bounded number of gates; all base derivatives are constants prepared at zero. This is classical Hessian-vector arithmetic differentiation. The inherited compiler is included byte-for-byte, with provenance. The resulting data program is linear, with no input-dependent inversion. QED.

A Fourier instance requires T=F_N. This is NOT automatic because T has high rank, is dense, shares Q_N's graph, or has enough adjustable parameters. The exact certificate

    T e_0 = ones,      T S = D T                                      (4.4)

with S e_j=e_(j+1 mod N), D=diag(1,omega,...,omega^(N-1)), is sufficient: T e_j=D^j ones. It is also necessary. Matrix-free random probes may reject candidates but do not prove a uniform family.

This construction supplies an actual bounded-cost scalar-source FAMILY. It does not supply the parameters that make a member Fourier. It is a more specific search than asking for an arbitrary fast scalar source, not an unconditional reduction of Fourier complexity.

## 5. An explicit sparse-Gram carrier

When every gamma_e != 0, automatic differentiation is not even necessary for application. For each necklace C let m_(C,e) be the number of times it uses edge e and put

    lambda_C = alpha_C product_e gamma_e^(m_(C,e)),
    u_(C,e) = m_(C,e)/gamma_e.

Twice differentiating one monomial gives

    H = sum_C lambda_C u_C u_C^T + Delta,                              (5.1)
    Delta[e,e] = -sum_C lambda_C m_(C,e)/gamma_e^2.

Keep each edge occurrence instead of expanding m_(C,e) into a dense vector or sorting repeated indices. There are k*L(k)=O(N*2^c) occurrences. Evaluate each dot product and scatter using those occurrences, so (5.1) applies in O(N*2^c) work with sparse incidence storage. All inverses 1/gamma_e can be prepared by batch inversion using O(N) multiplications and one field inversion.

In particular,

    rank(H-Delta) <= L(k),                                            (5.2)

but storing a dense rank factor is neither needed nor cheap. Formula (5.1) is an explicit shared evaluator for the growing collection of rank-one terms. It is not a claim that rank alone determines cost.

For zero baseline entries, use the polynomial circuit evaluator of Theorem 2. Formula (5.1) must not be used by dividing through zeros. The verifier tests both branches separately.

## 6. A new-to-this-synthesis locality obstruction

### Theorem 3 — short-orbit Hessian degree

In edge coordinates, each row of H in (4.2) has at most

    Delta_k = k * 2^max(0,k-n-1)                                      (6.1)

potentially nonzero entries. This holds for every choice of alpha_C and every baseline, including zero weights.

**Proof.** A mixed derivative involving edges e and f can be nonzero only if some length-k closed walk includes both occurrences. Anchor the first edge e=(s,b). When k>=n+1, its source state fixes n bits and its first appended bit fixes one more; closure fixes the last n appended bits. There are exactly 2^(k-n-1) possible remaining bit strings. Each such walk visits at most k edge labels. When k<=n, the n-bit state plus periodicity determines at most one possible continuation (and may be inconsistent). The union contains at most the quantity in (6.1). A repeated edge can contribute to a diagonal second derivative but fits the same bound. A monomial containing no such pair has zero mixed derivative formally, independently of numerical values. QED.

### Corollary — sparse marking cannot create dense Fourier phases

Suppose P has at most s nonzeros in each column and at most d in each row. Each output row of P^T H P then has support size at most

    s*d*Delta_k.

Because every Fourier entry is nonzero, necessarily

    N <= s*d*k*2^max(0,k-n-1).                                       (6.2)

For k=n+2 and s=d=1 this becomes N<=2(n+2), already false at N=16. For the target 2^c=O(log n), every fixed or polylog(n)-degree marking eventually fails. Thus a small number of local perturbations per raw input cannot yield the desired Fourier Hessian.

This is NOT a total-nnz lower bound for completely unbalanced sparse markings, and NOT a general circuit lower bound. A dense P with a separate cheap evaluator is not constrained by small s,d. Nor does failure of this gate prove that such a dense P exists with correct phases.

## 7. Concrete dense transport grammar and conjecture

The implemented test grammar uses four weighted cyclic Green maps. For an N-cycle pi and edge gains a_j, let G solve

    y_j = x_j + a_j y_predecessor(j),
    product_j a_j != 1.

Each G and its transpose have O(N) scalar circuits. Distinct maps may use completely different non-affine cycles and nonconstant gains. Define an interleaved rectangular transport

    (Px)_(s,0) = (G_1x+G_2x)_s,
    (Px)_(s,1) = (G_3x+G_4x)_s.                                      (7.1)

The tests use exactly this grammar, without hidden endpoint transforms. A broader search may insert a bounded number of diagonal masks, permutations and sums, but every such addition must be specified and charged. Positive controls in the broader affine-marking grammar do not certify the four-Green subfamily.

A particularly explicit carrier is obtained by fixing gamma_(s,0)=1, gamma_(s,1)=omega^s and alpha_C=r_C, so Psi=tr(B(w)^k). This fixes the whole middle carrier independently of the input. At the tested N=4,8,16,32, it has full edge-space rank 2N in both fields; at N=2 its tested k=3 carrier has rank N. These are finite certificates, not an all-size rank theorem.

### Necklace–Green Fourier-transport conjecture

There is a uniform family of bounded-size Green/sum/diagonal/permutation transports P_N, generated with O(N*2^c) work, such that

    P_N^T Hessian Psi_N(gamma_N) P_N = F_N,                            (7.2)

where Psi_N has the length n+c necklace form and its coefficients and gamma_N are generated within that budget. The fixed canonical carrier is a concrete narrower target, not an assumption of the conjecture's proof.

If (7.2) holds with c bounded, the compiled exact Fourier cost is O(N). If

    c = ceil(log2(log2(n+2))),

then 2^c=Theta(log(n+2)) and the cost is O(N log log N). Any schedule 2^c=o(n) gives o(N log N).

**No such growing Fourier-compatible transport has been constructed in this work.** The conjecture may be false for the four-Green subfamily or require a different bounded-cost grammar. The code contains no function advertised as that unknown FFT.

The existence of an arbitrary dense congruence P for a suitable symmetric carrier would not suffice: constructing/storing/applying a generic 2N-by-N P costs quadratic work. Synthesis must produce the priced low-work transport itself.

## 8. Exact Fourier positive control and honest negative controls

For N=4, omega a primitive fourth root, let

    a=z0+z2, b=z0-z2, c=z1+z3, d=z1-z3.

Assign those four affine markings to edges 0->0, 1->2, 2->1, 3->3 of the four-state binary graph. The three length-two necklace monomials, with coefficients 1/2, 1, omega/2, give

    Phi(z)=a^2/2 + b*c + omega*d^2/2 = z^T F_4 z/2.

The compiled Hessian is exactly F_4. The generic source emitter uses 16 arithmetic gates and its compiler emits 18 linear arithmetic gates in both fields. This is a classical four-point identity; it is neither an optimality claim nor an asymptotic saving. It lies in the broader sparse affine-marking grammar, NOT a proved four-Green factorization.

For random four-Green transports at N=2,4,8,16, the computed Hessians were dense and full rank in both fields, but every one differed from Fourier. Their exact mixed directional derivatives were independently verified. Thus this family supplies cheap dense operators but no empirical evidence of a Fourier factorization in the sampled parameters.

## 9. Reproducibility

Run `python verify.py` in this directory. Only the standard library is required.

Nine groups passed, then passed a second time with a byte-identical RESULTS.json:

- FKM enumeration versus exhaustive rotation grouping for lengths 1 through 10.
- 132 arbitrary-weight trace comparisons against independent dense matrix powers, including zero weights.
- 72 mixed edge-Hessian directions against independent bivariate dense matrix-power jets.
- 24 locality-support plans and 5,440 actual Hessian entries checked against the structural support bound.
- 24 transported mixed directions plus 680 basis-derived matrix entries across eight four-Green instances; all were dense/full rank and all were NOT Fourier.
- 40 actual F4 vectors, including every basis vector in two fields; 160 outputs checked against independent DFT sums.
- Six charged trace profiles through N=32,768; these compute graph polynomials, NOT Fourier spectra.
- Six input/denominator rejection controls.
- 40 sparse-Gram versus compiled-Hessian matvec checks, ten finite canonical-carrier rank checks, and a zero-baseline rejection for the Gram formula.

The dense matrix operations, full Hessian assembly and ranks are verification oracles. Their costs are not hidden inside the proposed online evaluator. Stored results from prior packages were not relabeled as fresh tests.

## 10. Prior art, research priority and scope

Binary necklaces and FKM generation are classical [1]. Periodic-orbit expansions for quantum graphs, including related binary graphs, are classical [2]. Fast exact Hessian-vector arithmetic is classical [3]; the circuit compiler is reused from the project's sparse-jet package. Green recurrences and quasiseparable representations are established [4].

This pass contributes a proof/evaluator for arbitrary weighted short binary-orbit polynomials, the explicit sparse-Gram form in this circuit setting, the edge-locality/marking obstruction, and their concrete Fourier-transport synthesis target. The inspection does NOT establish that these results are absent from earlier combinatorics, graph-trace, automatic-differentiation or circuit literature.

The official OpenAI #130 documentation [5] separately reports uniform exact complex DFT work O(N(log N)^(1-10^-13)), with supplied selected roots and unrestricted coefficients. That construction is not used here, and the present work does not improve its exact upper bound. No claim that all sub-N-log-N Fourier results are unknown is made.

The target here is first every dyadic N. A general-length extension would require a separately charged reduction and legitimate root supply. No numerical stability, finite-precision, bit complexity, practical crossover, external novelty or peer-review claim is supplied.

### Primary references consulted

[1] F. Ruskey, C. Savage, T. M. Y. Wang, *Generating necklaces*, Journal of Algorithms 13(3), 414–430 (1992), DOI 10.1016/0196-6774(92)90047-G. Author page: https://webhome.cs.uvic.ca/~ruskey/Publications/GenNecklaces/GenNecklaces.html

[2] J. Harrison and T. Hudgins, *Periodic orbit evaluation of a spectral statistic of quantum graphs without the semiclassical limit*, EPL 138 (2022) 30002, arXiv:2101.00006v3. Abstract inspected; no claim of independently auditing its full spectral-statistic proof.

[3] B. A. Pearlmutter, *Fast Exact Multiplication by the Hessian*, Neural Computation 6(1), 147–160 (1994), DOI 10.1162/neco.1994.6.1.147. W. Baur and V. Strassen, *The Complexity of Partial Derivatives*, Theoretical Computer Science 22, 317–330 (1983), is the general derivative-circuit antecedent preserved in the project's previous source ledger.

[4] P. Boito and Y. Eidelman, *Computation of quasiseparable representations of Green matrices*, Linear Algebra and its Applications 721 (2025), 47–80, DOI 10.1016/j.laa.2024.04.034.

[5] OpenAI Math, `lean/docs/130.md`, *Exact Fourier transforms below n log n*, public documentation checked October 10, 2026: https://github.com/openai/math/blob/main/lean/docs/130.md . The selected web search retrieved the scope statement; a subsequent direct page open failed. No Lean rebuild or independent full-proof audit was performed.
