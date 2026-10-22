# C10 prime field decision and common quadratic witness contract

21 October 2026 UTC. Version 3 candidate bounded theorem and cost contract, awaiting final independent acceptance. This version makes the shared-field conclusion explicitly existential and the binary-case cost notation explicit. Versions 1 and 2 remain preserved unchanged; the fixed empty-input overhead correction from version 2 is retained. No native table, repository, or external state was changed. The existing C10 owner remains open.

## Result and exact boundary

Specialize the accepted C10 forest, component-domain, canonical-label, and sequential-2SAT solver to matrices over a supplied prime field F_p. This removes the abstract-field ambiguity for inversion, sortable keys, degree-two root tests, and witness representation. It does not replace the solver by a different algorithm.

There are two conclusions.

1. Both F_p decision and algebraic-closure decision have the deterministic bit-cost bound D below. Neither needs a supplied quadratic nonresidue or a root-finding oracle.
2. Every selected system that is feasible over the algebraic closure has at least one solution with all row directions in one common F_(p^2). This does not assert that every pre-existing closure solution belongs to that field. Thus no growing compositum is needed for this prime-field specialization. With a certified supplied nonsquare for odd p, construction has the deterministic bound W below. Without one, the stated witness bound is expected Las Vegas time, or has an explicit deterministic nonsquare-search surcharge. It is not an unconditional deterministic polylogarithmic witness bound.

The output is a selected-subsystem decision and, when requested, nonzero coordinate pairs for its row directions. Column compatibility, supported-entry scales, legal Green denominators/weights, fixed endpoint choices, full two-Green factorization, and Fourier application remain outside this contract. No parent closure, historical novelty, lower bound, or arbitrary-field bit theorem follows.

## Authoritative scope and source pins

The retained open-record index identifies C10 as “Projective row-constraint graph solver”, priority 34, TO RESEARCH. Its current gate explicitly permits a separately named root/representation/bit-cost obligation and preserves the broader owner.

The accepted original reduction is the 8,526-byte review at commit 0339a31eb6109f0b96074ab8321f8653641e7530, Git blob 7bd7146ab8d8257f0b973bf9ccb7a3b1408e7fb8, actual SHA256 93b237e0e3d425cc126df06c60d686ec644159fa31e035df38dc7bfa849f4835:
https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/93/93b237e0e3d425cc126df06c60d686ec644159fa31e035df38dc7bfa849f4835__REVIEW.md

The sorting/sequential-2SAT report and its independent acceptance are pinned to commit 228288f489fef7bd534275a54d4c4c2c842cff38:
https://github.com/AgentSlop-Si/research/blob/228288f489fef7bd534275a54d4c4c2c842cff38/math/finalized/2026-10-16-research-finalization-1749/c10/REPORT.md
https://github.com/AgentSlop-Si/research/blob/228288f489fef7bd534275a54d4c4c2c842cff38/math/finalized/2026-10-16-research-finalization-1749/independent_review/INDEPENDENT_REVIEW.md

Their actual SHA256 values are 72a2777bd409eea831567306c9c920332f99febb73d5c767bfbbab7606539a76 and f8536528b7637caa0eac54e069e5f70a06559f349aa99a77508ab7d9fbfa7230 respectively. SOURCE_PINS.json records full byte counts and recomputed Git blob hashes. All four source texts were fetched read-only and their returned blob identities independently recomputed. No supplied research program was run or imported.

The accepted algorithm retains N vertices, M selected equations u_j^T L_e u_i=0, rank-two transports over the base field, degree-at-most-two component gcds, an explicit infinity bit, at most 2M named base-field points, at most 4M Boolean variables, and at most 9M clauses. Its existing correctness proof, including all-false repair, is the dependency here, not a newly claimed theorem.

## Input and machine contract

The input includes a prime p, endpoint indices, and all selected 2-by-2 matrices with entries already represented by canonical residues 0,...,p-1. Let b=ceil(log2(p+1)), n=N+M+2, and ell=ceil(log2 n). These definitions handle p=2 and N=M=0.

Primality is a promise of the field input. If p is untrusted, add the actual cost P_prime of establishing primality or verifying its supplied certificate before using the field theorem. Checking a nonsquare certificate is not a primality test. If input integers are unreduced or longer than b bits, add their actual input-reading and reduction costs; they are not silently b-bit inputs.

The model is a bit-cost random-access machine. Arithmetic is charged for the stated elementary bit algorithms, and accessing/copying a stored record charges its index and payload lengths. Local arithmetic can use scratch registers; graph/index operations on ell-bit words cost O(ell). This is not a unit-cost field RAM and is not an asserted bound for every Turing-machine memory model.

Use schoolbook integer multiplication and long-division remainder: modular multiplication/reduction costs O(b^2), addition/subtraction/zero testing costs O(b), and copying a residue costs O(b). Binary powering by an exponent below p uses at most 2b modular products. For nonzero a, use a^(p-2) for inversion, costing O(b^3), including its final residue representation. For p=2 the only nonzero inverse is 1. No fast-integer-multiplication or arbitrary-DFT assumption appears.

## Exact quadratic decision

The accepted forest/domain phase supplies either an unrestricted domain, or a chart gcd g(t) of degree at most two and a Boolean h allowing infinity. If h is true, the component is already nonempty. A zero polynomial permits every finite t; a nonzero constant permits none. For degree one, solve using one charged nonzero inversion.

For odd p and g(t)=A t^2+B t+C with A nonzero, put Delta=B^2-4AC. The finite domain is nonempty over F_p exactly when Delta=0 or Delta^((p-1)/2)=1. This uses a bounded number of field operations and one exponentiation, O(b^3) bit work. Over the algebraic closure every such quadratic has a root, so no exponentiation is needed for this test.

To justify the residue test without a root oracle: the nonzero squares form a set of (p-1)/2 elements, all satisfying X^((p-1)/2)=1 by Fermat. A polynomial of that degree has at most that many roots. Every remaining nonzero element has half-power -1, since its squared half-power is 1 and the characteristic is odd. This proves the test and distinguishes repeated roots from nonsquares.

For p=2, evaluate g at t=0 and t=1. Never divide by 2. The infinity bit remains separate. At most C<=min(N,M) components are restricted: each such component contains at least one distinct internal equation whose substituted quadratic is nonzero. Thus all needed root-existence tests fit O(M b^3).

## Canonical labels and full decision ledger

Every cross-component named point is over F_p, because its defining forms and transports are over F_p. Normalize a nonzero [x:y] to the distinguished infinity key when x=0, otherwise to the finite key y*x^(p-2) mod p. Exactly equal projective points get equal keys: for nonzero first coordinates this is equivalent to xy'-yx'=0; the zero-first-coordinate case is separate. The key is unique, uses O(b) bits, and takes one charged inversion and one multiplication when finite.

Sort at most 2M occurrence records by component, chart tag, and residue. Use deterministic comparison sorting and retain occurrence-to-flag references, as in the accepted solver. Each comparison/copy costs O(b+ell). No equality-oracle order or constant-size arbitrary algebraic key is assumed.

Define

D = O((N+M+1)(b^2+ell) + M b^3 + M log2(M+1)(b+ell)).

This charges the entire selected-matrix decision algorithm:

- Read all matrix entries and endpoint indices; build graph/forest lists and test ranks.
- Propagate all 2-by-2 transports; reverse edges use adjugates rather than inversions.
- Form every internal quadratic, update constant-degree gcds, and retain infinity flags. There are O(M) divisions, each implemented at O(b^3).
- Factor cross rank-one edges without division, normalize all at-most-2M point occurrences, sort and deduplicate them, and record all occurrence references.
- Test all named-point memberships against their summaries, emit all positive/forbidden/sequential clauses, build the implication graph, and run linear graph SCC processing with charged indices.
- Perform all required base-field quadratic-existence tests. Closure decision uses a subset of this bound.

Initialization, copying, graph bookkeeping, and output of the decision bit are included. The added 1 in the leading term explicitly charges reading/storing the prime-field descriptor, fixed initialization and the decision bit even when N=M=0. Storage is O((N+M+1)(b+ell)) bits beyond any retained target oracle, including the fixed field descriptor and working registers. The b^2 term is intentionally retained even though many arithmetic operations are cheaper. This is a conservative implementation upper bound, not an optimality claim.

Target extraction is not free. If target setup and entry access have SAME-MODEL costs S_B^bit and E_B^bit and return canonical F_p residues, the accepted constant-degree extraction adds

S_B^bit + O((N+1) ell + b + M E_B^bit + M b^2).

The fixed extraction interface and field descriptor are explicitly charged by the +ell+b terms, even if no selected matrix is emitted. Consequently the extraction-plus-decision bound is S_B^bit+O(M E_B^bit)+D. Scalar-operation S_B or E_B values cannot be substituted for these bit costs. All-triples extraction can still have M=Theta(N^3). Root-of-unity construction, target power-table preparation, input precision conversion, and target field construction must remain in S_B^bit where applicable; none is newly bounded here.

## One common quadratic field suffices

For odd p, choose eta in F_p with eta^((p-1)/2)=-1 and set E=F_p[alpha]/(alpha^2-eta). The defining polynomial has no F_p root, hence is irreducible; E is a field with p^2 elements. Store a+b alpha as the unique pair (a,b) of canonical residues. Addition, multiplication, equality and copying use a bounded number of base-field operations and O(b) storage per element. In particular, multiplication is

(a+b alpha)(c+d alpha)=(ac+eta bd)+(ad+bc)alpha.

Every quadratic over F_p splits in E. In the odd characteristic quadratic formula, Delta=0 is immediate. If Delta is a nonzero square, its square root lies in F_p. If Delta is a nonsquare, Delta/eta is a square by the multiplicative residue test; writing r^2=Delta/eta gives sqrt(Delta)=r alpha. Thus (-B+r alpha)/(2A) is a root, using only a base-field inverse. These constructions also cover an arbitrary nonmonic chart gcd after its nonzero leading coefficient has been recognized.

For p=2 use E=F_2[alpha]/(alpha^2+alpha+1). The polynomial has neither binary root and is irreducible. The only irreducible monic quadratic over F_2 is this polynomial; all remaining degree-at-most-two polynomials have linear factors or repeated roots. Equivalently, direct evaluation of at most four E elements finds every required finite quadratic root. All operations here have constant cost; there is no generalized characteristic-two quadratic-formula assumption.

Run the existing 2SAT reconstruction with these component points. A true flag selects its named F_p point. For an all-false component, choose infinity if allowed, otherwise a finite allowed point in E, using a linear solution or the quadratic construction; an unrestricted component can choose [1:0]. If the chosen point is a named base-field point, turn that one flag on and recompute prefix auxiliaries. If its alpha coefficient is nonzero, it cannot equal ANY named base-field point, so all its flags stay false. This is precisely the accepted repair argument.

Each T_i is over F_p and invertible, so u_i=T_i z_C is nonzero and belongs to E^2. All internal equations vanish by domain membership; all cross rank-one clauses remain satisfied. Hence existence over the algebraic closure is equivalent to existence over this single E for the whole selected subsystem, not merely for each component separately. Returning all coordinates in one field now permits direct evaluation of every original equation. This finite-field result does not remove the accepted general-field compositum warning.

## Constructive root routine and witness costs

Use the standard Tonelli-Shanks root subroutine, not an unpriced root oracle. Its classical quadratic dependence on v2(p-1) is documented by Algorithm 1 in J.-C. Schlage-Puchta, “On Shanks' Algorithm for Modular Square Roots”, Applied Mathematics E-Notes 5 (2005), 84-88, https://arxiv.org/pdf/1105.1456. The faster variants in that paper are NOT substituted here. The following explicit accounting and its integration into C10 are the present candidate contract.

Write p-1=2^s q with q odd by trailing-zero inspection. For a nonzero square d and certified eta initialize c=eta^q, t=d^q, r=d^((q+1)/2), m=s. While t!=1 find the least i with t^(2^i)=1, set h=c^(2^(m-i-1)), then c=h^2, r=r*h, t=t*c, m=i. Return r.

Initially c has order 2^m, t has order at most 2^(m-1), and r^2=d*t. When t!=1, 1<=i<m. The correction makes c have order 2^i, cancels the order-2 part of t, and preserves r^2=d*t, so the new t has order at most 2^(i-1). Strict decrease of m proves termination with r^2=d. This uses only the fact that -1 is the unique element of order two in an odd field.

The three initial exponentiations use at most 6b modular products. In one loop, testing i uses i squarings, constructing h uses m-i-1, squaring h uses one, and updating r,t uses two products: exactly m+2 products. Distinct successive m values lie in s,s-1,...,2. Therefore the root subroutine uses at most

6b + s(s+5)/2

modular products, a slightly loose integer upper bound valid also when s=1. Input residue tests and eta certification are separately charged; zero roots require no loop. A final square check costs one additional product if performed. All loop/exponent/control costs are covered by O(b^3+s^2 b^2), hence by O(b^4); this is not a unit-cost scalar count relabeled as bit time.

Let W be the number of quadratic roots actually needed for all-false restricted components after 2SAT, so W<=min(N,M). In the displayed uniform upper-bound notation, take s=0 when p=2: the binary root work is O(1+W), and no nonsquare eta is required or tested. For odd p with supplied eta, verify its certificate by one exponentiation costing O(b^3). Cache eta inverse if needed. Required square roots, discriminant divisions, linear component solutions, and nonzero leading-coefficient inverses then add O(b^3+W(b^3+s^2 b^2)) beyond D; linear-root costs O(M b^3) are already absorbed in D. Reconstructing all u_i and directly verifying all M input equations in the common E costs O((N+M)(b^2+ell)), already covered by D. Thus

T_witness = S_B^bit + O(M E_B^bit) + D + O(b^3 + W(b^3+s^2 b^2)).

For F_p witnesses this applies after base-field acceptance and returns coordinates with zero alpha coefficient; no extension is necessary. For closure witnesses it returns all coordinates in the same explicit E. The output consists of nonzero coordinate pairs, not additionally projectively normalized pairs. The row-coordinate payload has size O(Nb), using at most four b-bit residues per vertex. Including the prime/common-field descriptor and decision bit, total output size is O((N+1)b), which remains nonzero as a bound when N=0. If canonical normalized vertex outputs are required, add O(N b^3) for their inversions. In odd-characteristic E an inverse can be computed via (a-b alpha)/(a^2-eta b^2), whose denominator is nonzero for a nonzero element; p=2 is constant-size. Auxiliary storage, beyond the already stored solver, is O(b) with scratch and roots processed sequentially.

For odd p, if eta is not supplied, uniformly sample independent elements of F_p^* and verify each Euler certificate. Exactly half qualify, so the expected number of candidate tests is two. Uniform sampling by b-bit rejection has expected constant retries. This gives a Las Vegas version with expected O(b^3) setup and always-verified answers. A deterministic scan is allowed, but its conservative O(p b^3) search surcharge must be shown. No unproved unconditional deterministic polylogarithmic nonresidue discovery is claimed. Invalid eta is an auxiliary-input error or a reason to search again, not a certificate that the subsystem is unsatisfiable.

## Original F241 control instantiated

The original accepted source separates closure and base-field roots using t^2-7 over F241. Here 7^120 mod 241=240, so 7 itself is a certified nonsquare and E=F241[alpha]/(alpha^2-7) supplies the exact closure witness alpha. Base-field decision still rejects that finite chart when infinity is excluded. For p=241, b=8 and s=4, so the above supplied-nonsquare square-root routine uses at most 66 modular products, excluding the explicitly separate input tests, denominator inversion, and optional final verification. This finite instantiation does not assert a bound for target extraction or Fourier execution.

## Narrow controls and next independent verification

Fresh standard-library controls in work/narrow_controls.py execute only independently authored arithmetic/interface code. They do not execute, import, compile, or parse a supplied research program. Inherited, unchanged normal-mode results are in NARROW_CONTROL_RESULTS.json. Versions 2 and 3 change only proof/cost text and candidate metadata, not the arithmetic control program or its recorded executions. The enumeration used to obtain expected small-field answers is a test oracle, never the claimed runtime algorithm.

The controls pass 38,146 square roots and 75,958 inversions over odd primes through 997; 8,062 base-field and 8,062 closure domain summaries over primes through 13, including both infinity settings; 258,121 canonical projective-pair equivalence checks through F19; and 365 simultaneous components sharing one extension across six fields including F241. There are 1,659 checked domain polynomials empty over the base field but nonempty in the quadratic extension. Tonelli loop product counts and the explicit root budget are checked at each iteration. These counts are narrow interface controls, not newly replayed whole-C10 instances.

Next independent verification target: derive the single-E reconstruction and full cost formula from the pinned accepted solver, then independently implement small complete selected systems over F2/F4 and F3/F9 and compare closure decisions and returned witnesses against exhaustive original-bilinear-equation assignments. Explicitly include a nonbase all-false component adjacent to a forced named base point, infinity-only domains, repeated roots, all named finite-field points, rank-one loops, multiple irreducible quadratic components, invalid eta, and normalization-output surcharges. Independently audit address/copy charging, prime-input promises, and extraction costs. Do not relabel the present narrow tests as that whole-solver independent replay.

After independent acceptance, only the named prime-field root/representation/bit-cost obligation can be marked completed. Remaining independent obligations include original target-extraction bit costs for a concrete target representation and columns/scales/legal-Green integration. A full C10 owner closure is not authorized by this result.
