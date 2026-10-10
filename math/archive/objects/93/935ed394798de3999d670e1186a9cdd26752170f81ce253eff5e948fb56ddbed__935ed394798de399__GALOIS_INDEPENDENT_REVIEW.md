# Independent review of the Galois-defect evaluator and hybrid

Reviewed `galois_defect.py`, `run_audit.py`, the recorded `results.json`, and
the root `README.md`. The reviewer separately implemented the tensor branch;
this review concerns the independently authored Galois branch.

**Verdict: the exact identities, output indexing, arithmetic counts, hybrid
comparison, and restricted-class claims are correct.** No arbitrary-input
sub-N-log-N theorem follows. The existing focused audit was inspected, not
rerun: its recorded source hash matches the reviewed implementation.

## Algebra and full output coverage

At conductor q, pair sums give its even-frequency subproblem and pair
differences r give all odd outputs as evaluation modulo z^(q/2)+1. Replacing
z by z^5 explicitly permutes those retained coefficients with the correct
sign, so evaluating d=(P_5-I)r at an odd root gives Y_(5k)-Y_k. This proof
works for arbitrary complex coefficients; it does not apply an implicit
Galois automorphism to a scalar register.

For q>=4, 5 has order q/4 modulo q and the odd residues split into the two
cycles represented by 1 and 3. The implementation emits one dense anchor
per cycle and then q/4-1 exact recurrence edges. The q=4 singleton and q=2
one-coefficient cases are handled correctly. Scattering odd index k to
k*N/q gives each original nonzero frequency its unique conductor. Together
with DC, the number of output writes is N/2+N/4+...+1+1=N.

In the hybrid, modulation of r_j by zeta_q^j reduces these same odd outputs
to a length-q/2 DFT with root zeta_q^2. The local `Field.root_stride=2*N/q`
uses exactly that root from the shared original table. The local FFT indexing
and subsequent scatter to (2k+1)*N/q are correct; no additional root table
is assumed free.

## Independently derived operation ledger

For N>=2 and d=log2(N), root validation and power preparation cost N+2d
field multiplications. Discovery costs 3N-4+nu field operations, where nu
counts executed coefficient negations. Across q>=4, the total reduced
length is N-2, dense anchor terms total 2N-4, and recurrence edges total
N-2d. Writing T=sum_(q>=4)(q/2)s_q, all-orbit emission costs
5N-8-2d+2T, giving the reported total

    9N-12+2T+nu.

At an individual conductor, orbit emission costs 5m+2ms-2; modulation and
the local radix-two FFT cost m+(3/2)m log2(m). Both match the actual loops.
Summing the latter option at every conductor and adding discovery gives
at most the fully prepared full radix-two comparator plus N-3+nu field
operations. Therefore taking their minimum per conductor preserves generic
O(N log N) work plus O(N) overhead and retains O(N(S+1)) work on the
uniformly bounded-defect class.

Copies, scans, exact zero tests, support storage and output materialization
are linear in the charged conductor lengths. Sparse evaluation entails
O(N(S+1)) word operations. In a bit model, its `j*k` index products are
O(log N)-bit integer multiplications and must also be paid. Under the
standard monotone multiplication model they are absorbed by M_mod(b)
because supporting prime fields have b>=log2(N+1); a conservative alternative
is to add N(S+1)M_int(log N) explicitly. Schoolbook O(N(S+1)b^2) already
absorbs these terms. The final README explicitly includes this index-product
term and states the absorption conditions. A supplied prime and primitive root are explicit
hypotheses. The implementation's order test must not be generalized to an
arbitrary composite residue ring without a principal-root condition.

## Structured family, stability and limits

For q>=8, 5^(q/8)=1+q/2 modulo q, so P_5^(q/8)e_1=-e_1. The stated half-orbit
sum telescopes to the single-coordinate defect -2a e_1. Inverting all
sum/difference steps reconstructs valid original inputs. Over C a generic
DC choice avoids the finite set of coordinate-zero hyperplanes, so dense
examples exist; density does not imply arbitrary-input coverage.

At fixed conductor the odd-root evaluation map is invertible and conjugates
P_5 to the two-cycle output permutation. Thus dim ker(P_5-I)=2. Restricting
the defect to a fixed support of size at most S leaves dimension at most
S+2. The invertible dyadic decomposition gives O((S+2)log N) parameters for
each fixed full support pattern. This is a restricted union of subspaces,
not the full-dimensional domain required by the new global rank theorem.

An anchor error alpha, defect-evaluation error eta and local addition error
gamma accumulate along at most q/4-1 edges, giving the stated
alpha+(q/4-1)(eta+gamma) bound. It is polynomial but is not a complete
floating-point certificate: discovery and root errors must be included in
those terms. Similarly, omitting a defect tail of l1 norm tau_q changes
each defect evaluation by at most tau_q and each emitted odd output by at
most (q/4-1)tau_q when anchors are exact. Conductors have disjoint output
sets, so the full-output bound takes the maximum, not a sum. The executable
modular path does not implement truncation or floating-point zero tests.

## Recorded verification

The audit records 30 structured full-output checks, all with nonzero input
entries; 21 independent direct DFT comparisons; 62 exact orbit identities;
four generic fallbacks; 12 zero-cap controls; six invalid-input checks; and
34 full-output hybrid comparisons. Assertions also verify the operation
formula and hybrid bound on the structured runs.

Reviewed implementation SHA-256:

    9940bcb774b94f8f9250c8760868cfd5f709d926290bfabef7931287ae6218ef

Reviewed audit SHA-256:

    9af4e863f97d6b3fecfc02efbf8e4b7a7d042e0741b1ad8738c549e6293e7b74
