# Independent acceptance: fourteen signed banks at order eleven

Review date: 10 October 2026. Verdict: **accepted, as an upper bound only**.

For every primitive eleventh root q, the frozen construction proves

M_C(11;q) <= 14

in the exact permitted grammar of the accepted small-order manuscript. The construction is defined over the splitting field L of an explicit monic sextic over K=Q(q), with [L:K] <= 720. Its orientation multiplicities, in the order (++,-+,+-,--), are (6,1,1,6). The twelve root-bank occurrences use the same six distinct nonzero roots, while the two singleton nodes are one. Each bank has beta=1.

**Count and cost boundary.** Fourteen means fourteen whole phase-weighted banks. There are 154 original resolvent branches, eleven per bank. It is not a count of fourteen individual Green-function applications, scans, arithmetic operations, or Fourier stages. No O(14N) execution bound, variable-order algorithm, FFT speedup, conditioning bound, or bit-complexity claim is accepted. The stated algebraic preparation and splitting-field cost remain part of the construction.

## 1. Frozen material and independence

The mathematical note reviewed is `sources/N11_FOURTEEN_BANK_CONSTRUCTION.md`, SHA-256:

`4e34c980cecd18b62b0c9b7840620860d63e0fe4b402612bdb37463ac4312154`.

The exact witness reviewed is `sources/N11_EXACT_WITNESS.json`, SHA-256:

`9d7a37435454b1b70bc4dde4ff9d3fb2a7d8bc98c112a9946eede2f17e3be8a7`.

`REVIEWED_SOURCE_HASHES.json` pins these, the modular certificate, the accepted manuscript grammar, and the accepted order-seven witness and receipt. The copies in `sources/` are inert mathematical inputs, not programs. The original accepted files were not modified.

Both controls in this review were written afresh. Neither author nor predecessor research programs were read, imported, executed, compiled, or parsed. SymPy is used solely as an exact arithmetic library. The first control rebuilds the construction from the bank coefficient formulas and verifies the literal data. The second imports only the reviewer's own first control and calculates original matrices by sparse polynomial-matrix multiplication. No numerical roots or finite-field roots are selected.

## 2. The grammar and guards match the accepted problem

The permitted bank is

B_(epsilon,delta)(alpha,1;w)
 = (1/11) sum_j w_j (I-alpha S^epsilon-q^(epsilon delta j)T^delta)^(-1),

with S e_i=e_(i+1), T e_i=q^i e_i. Its guard is Delta=1-alpha^11-beta^11=-alpha^11. Thus alpha=0 is the only forbidden alpha at beta=1. In particular alpha^11=1 and alpha^11=-1 are both legal. No extraneous restriction from another resolvent grammar has been imposed.

The construction adds whole banks in the original four signed orientations. It introduces no free gauges, alternative Weyl generators, matrix pre/post factors, products of banks, or coordinate changes of the synthesis target. Replacing a six-bank amplitude vector by its first six power moments is a method of specifying those same banks, not an additional permitted operation.

The target normalization is also unchanged: F[k,t]=q^(-kt), C=(1/11) sum_t q^(-t^2), and its Weyl coefficient at (a,b) is C q^(3(a+b)^2). Here 3 is 4^(-1) modulo eleven. The reviewer separately computed all 121 original trace-extraction sums and verified this convention exactly.

## 3. Characteristic-zero definition precedes good reduction

The reviewer independently built Gaussian coefficients by their Pascal recurrence, reconstructed the two edge moment sequences, solved the defining 4-by-4 system over the exact degree-ten field Q(q), and obtained exactly the source sextic

g(t)=t^6+c_3 t^3+c_2 t^2+c_1 t+c_0.

The source's explicit cyclotomic-basis coefficients agree with that exact solve. The good-reduction argument is valid in R=Z[q] localized at (23,q-2):

- 2 has order eleven in F_23.
- All factors 1-q^j for 1<=j<=10, 11, and 1+q have nonzero residues.
- Every nonzero Gaussian factor used in the construction therefore is a unit of R.
- The defining matrix has determinant residue 1, so its inverse and the sextic coefficients lie in R.
- The reduced sextic has ascending coefficients (12,21,2,4,0,0,1).
- Its constant term has residue 12, and its Sylvester resultant with its derivative has residue 6.

The last two assertions prove that the characteristic-zero sextic has six distinct nonzero roots. They justify every node inverse and derivative denominator. The reviewer rebuilt the full Sylvester matrix and its determinant rather than trusting the supplied resultant flag.

This is a nonvanishing certificate for objects already defined over K. It is not a lift of a random modular solution, and it does not argue from an absence of finite-field points. Every embedding of K carrying q to another primitive eleventh root preserves the resulting characteristic-zero identities and nonzero elements.

### Important localization warning

Some canonical rational-basis coefficients of the exact row vectors have denominators divisible by 23. Such expanded coordinates must not be reduced termwise. Membership in R is established by the original formulas and square systems with unit determinants. Those formulas are the objects reduced in the proof. The sextic coefficients themselves have common denominator 469219301, which is 4 modulo 23, and can be reduced directly. The review never termwise reduces the problematic row-vector coordinates.

## 4. All eleven rows, including the deficient edges

The reviewer reconstructed all eleven 11-by-14 matrices from the actual accepted support rule, using r=[epsilon a]_11 and ell=[delta b]_11. Power reduction modulo the sextic was independently implemented. The exact source row vectors satisfy every one of the 121 equations M_b z_b=f_b.

More strongly, the reviewer separately rebuilt the displayed recipes for b=1 and b=2, performed the four selected exact square solves for b=0,3,4,5, and applied the specified simultaneous reflection to obtain b=6,...,10. All eleven rebuilt vectors equal the literal witness.

The independently reproduced reduced row ranks are

(11,8,10,11,11,11,11,11,11,10,8).

The proof does not infer solvability of the deficient rows from these ranks. It supplies exact compatible solutions to b=1,2 and then to b=10,9 by reflection. The shared sextic's three first-edge recurrence constraints and one second-edge constraint are precisely the compatibility conditions used in those explicit solutions.

For the four primary nonsingular rows b=0,3,4,5, the chosen determinant residues are respectively 5,3,18,8. The review checks those exact column selections as well as the additional reflected-row minors supplied in the modular certificate. All eleven modular matrices agree entry by entry with fresh reductions. No unsupported claim about the exact characteristic-zero ranks of the deficient rows is required.

## 5. Shared nodes and independent sector amplitudes

All sectors of a given root bank use the same alpha, and the ++ and -- groups use the same six roots. The construction does not silently choose a new root set for each row. What varies independently by sector is the amplitude, which the permitted arbitrary phase weights allow.

For moment vector k=(k_0,...,k_5), put

N_k(t)=sum_(d=0)^5 k_d sum_(m=d+1)^6 c_m t^(m-1-d).

At each root x_i the amplitude is N_k(x_i)/g'(x_i). Lagrange interpolation gives

sum_i N_k(x_i) x_i^r/g'(x_i)=k_r, 0<=r<=5.

The review verifies all 36 basis pairings of this dual interpolation map exactly. It then checks the corresponding identities for every root-group sector, including all higher moments through power ten. The relation t^6=-sum_(m=0)^5 c_m t^m supplies those higher moments.

For each orientation, b maps bijectively to ell=[delta b]_11. Hence the row recipes assign all eleven sectors of each of fourteen banks exactly once. There is no consistency condition identifying amplitudes from different sectors beyond use of the same bank node; that node sharing is respected.

The raw weights are exactly

w_j=C Delta sum_(ell=0)^10 h_ell q^(-epsilon delta j ell).

Finite-character orthogonality yields (1/11) sum_j w_j q^(epsilon delta j ell)=C Delta h_ell. Thus the 1/11 in the bank definition is accounted for once, with no missing or duplicated normalization factor. All 154 raw weights are specified algebraically over L.

## 6. Separate control in the original matrix basis

The second reviewer control is stronger than a reread of the Weyl-coefficient residuals. For each of four orientations and eleven phases it constructs the literal matrix

X_j=t S^epsilon+q^(epsilon delta j)T^delta

over K[t], and builds its powers by sparse matrix multiplication. For every one of these 44 symbolic group/phase cases it verifies

X_j^11=(t^11+1)I,
(I-X_j)(I+X_j+...+X_j^10)=-t^11 I,
(I+X_j+...+X_j^10)(I-X_j)=-t^11 I.

For root groups, evaluating at each of the six distinct nonzero roots yields six valid two-sided inverses. For a singleton, evaluate at t=1. These exact symbolic checks therefore cover all 154 original resolvents, not merely 44 physical branches. The reviewer also constructs and verifies an exact inverse of t and of the guard -t^11 modulo g.

In the separable algebra E=K[t]/(g), the trace identity

Tr_(E/K)(N(t)/g'(t)) = coefficient of t^5 in N(t) mod g

is the Lagrange duality already proved and checked above. After cancellation of the legal guard in each raw weight against the geometric inverse, the control uses this coefficient functional for root groups and evaluation at t=1 for singletons. It directly accumulates the eleven weighted matrix phases for each group. No Gaussian row-expansion formula is used in that matrix accumulation.

All 121 entries of the final matrix agree exactly with q^(-kt) in K. `LITERAL_ORIGINAL_MATRIX_RESULTS.json` records all branch checks and all final entry checks; `LITERAL_AMPLITUDE_CERTIFICATE.json` records the sector numerators and exact node/guard inverses used by this control. Thus the passage from the shared-node moment construction to actual permitted raw resolvent banks is independently verified in characteristic zero.

## 7. The twelve-bank diagnostic remains restricted

The separately stated depressed-quintic calculation also checks out. For the symmetric (5,1,1,5) ansatz with both singleton nodes equal to one, the same five distinct nonzero roots on both sides, and zero t^4 coefficient, the first-edge equations determine the candidate quintic. Its defining determinant has residue 20, its ascending reduced coefficients are (10,1,4,8,0,1), and its two second-edge recurrence residuals are 21 and 17 modulo 23. The reviewer reproduces both residuals exactly over K and matches the new literal fields in the frozen witness.

This excludes that ansatz only. It does not exclude a nondepressed quintic, changed singleton nodes, different root sets, repeated-node strata, other multiplicity distributions, twelve banks in general, or thirteen banks. No minimum at eleven follows. Combined with the already accepted general lower bound, one can report only 6 <= M_C(11;q) <= 14 from these results.

## 8. Accepted and excluded scope

Accepted:

1. The exact constructive upper bound of fourteen whole permitted banks at order eleven, for every primitive q.
2. Attainment in the specified sextic splitting field, hence over C; [L:K]<=720 is a degree bound, not an asserted exact degree.
3. All eleven shared-node row recipes, every guard, all sector and raw-weight formulas, all 154 two-sided resolvents, and all 121 original Fourier entries.
4. The precisely bounded depressed-quintic incompatibility.

Not established:

- Minimality or classification of all fourteen-, thirteen-, or twelve-bank representations.
- Sufficiency over K=Q(q) itself.
- A general-size upper-bound formula derived from this fixed-order example.
- A fast implementation, operation count, stability result, or asymptotic FFT claim.
- Historical novelty or priority; this review did not conduct a literature search.

There are no remaining mathematical corrections or blockers within the accepted scope.

## 9. Reproduction

From this directory, run:

1. `python review_n11.py`
2. `python review_literal_n11.py`

The only nonstandard dependency is SymPy. The second script imports only the first reviewer script, so its log intentionally includes the first exact reconstruction as well. Both scripts read the frozen local `sources/` copies and write only reviewer results next to themselves. Run them in a writable copy if preservation of the hash-pinned packet is required. The logs from the reviewed run are `exact_review.log` and `literal_review.log`.

`ACCEPTANCE_RECEIPT.json` records the accepted theorem and source hashes. `MANIFEST.json` pins the final review packet. No external, repository, or publication writes were performed.
