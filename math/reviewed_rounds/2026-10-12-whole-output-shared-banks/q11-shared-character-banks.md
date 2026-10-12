# Q11 shared character-bank evaluator: independent bounded ACCEPT

12 October 2026 UTC. Verdict: **ACCEPT within the exact model below.**

## Finding

For q=483^m, m>=1, s=5q and N=5q², the frozen positive target has a two-bank shared evaluator with exactly 10N−75 nonzero middle coefficients. It computes the sum of the accepted source-legal matching Green representation in O(N log q) field operations and integer-word work, with O(N) preparation and storage. A literal, fully charged implementation uses

- (66m+11)N−75 field multiplications per application;
- (60m+10)N−75 field additions per application;
- 4N−1 setup multiplications and 75 setup additions, besides O(log N) scalar synthesis and optional supplied-root certification.

At m=1 this is 89,816,190 multiplications and 81,651,075 additions, verified by a newly written independent implementation on all 1,166,445 output coordinates.

**This is a fused arithmetic compilation of the legal sum, not literal separate execution of each Green branch.** The older restricted row-incidence lower does not apply to shared/fused circuits. The evaluator’s sparse factors are not asserted to be additive Green summands. The accepted closed-form representation still has 20q+1 branches; the better colored representation still has 20q−7. The fully paid Model R interval [20q−12,20q−7] is unchanged.

Cold O(N log q) applies using the closed-form 20q+1 witness. For the 20q−7 witness, checking a supplied O(s²) certificate takes O(N) word work, but constructing it cold by the accepted coloring algorithm still costs O(s³). Producing every expanded branch endpoint/route occurrence still costs Θ(Nq) writes/storage. The already known original two-DFT evaluator has the same asymptotic rate. No faster-FFT, novelty, bit-speed, numerical-stability, optimal-constant, all-N or negative-family result follows. Broader Q11 remains OPEN.

## Provenance and independent process

The immutable candidate is Q11_Shared_Character_Banks_CANDIDATE_2026-10-12.zip, 35,558 bytes, SHA-256 e7f40c59d8c07236d461db84cb906527560d590a25c5d5c1fc83bd4be2ec431b. Its REPORT.md hash is 1494953adc9a014a4144fe5778445781762b805ea5323d7872fba230910f3bf1. All 18 members and 17 manifest records pass. All three accepted source archives were independently rehashed; their copied reviews exactly match archive members. The author cold receipt is bound and records an unchanged-candidate replay; this reviewer did not execute its program.

The reviewer read the accepted target/upper, lower and coloring sources, independently derived the index identities and collision count, and recorded INDEPENDENT_DERIVATION.md before receipt of the sealed candidate (SHA-256 760d22f5ea62f5738266b38a63dfd3123f65c403dac738d41f647379d6b22bcc). The initial candidate formula was supplied by the author. The newly authored candidate code was inspected as text; it was never imported, compiled or run by this reviewer. The reviewer independently wrote all three checkers in this packet. In particular, its Fourier implementation uses decimation in frequency, whereas the candidate uses decimation in time. All author and historical programs in nested archives remain inert bytes.

## Exact target and source-legal equality

Let omega be the supplied primitive complex Nth root, h=(N+1)/2, eta=omega^(q⁴), G=q(1+2eta²+2eta³), c=NG and rho=(1+c)^(-1). The accepted identity is

B_ij = rho omega^(ij) − rho G omega^(−h(i+j)²) + rho c omega^(−hi²) delta_ij.

The inherited guards G²=N and rho=(1−c)/(1−125q⁶) hold uniformly. They ensure rho and G are nonzero, with no root extraction, eigenvalue calculation, interpolation or inverse oracle. All operations are in L=Q(omega).

Write i=a+su, j=b+sv, with a,b in [0,s), u,v in [0,q), and zeta=omega^s. The identity s²=5N gives

omega^(ij)=omega^(ab) zeta^(bu+av),
omega^(−h(i+j)²)=omega^(−h(a+b)²) zeta^(−(a+b)(u+v)).

Hence compute X[b,k]=sum_v zeta^(kv)x[b+sv], then

C[a,k]=rho sum_{b≡k mod q} omega^(ab) X[b,a mod q]
       −rho G sum_{b≡−a−k mod q} omega^(−h(a+b)²) X[b,k].

Both sums have five terms. A second positive q-DFT gives

y[a+su]=sum_k zeta^(ku)C[a,k]+rho c omega^(−h(a+su)²)x[a+su].

Substitution reproduces the target coefficient at every original i,j and therefore for every x, not merely tested inputs. The address map (a,u)↦a+su is bijective and all gathering/scattering is charged.

The accepted matching witness uses diagonal endpoints on zero-cut Hamiltonian structural cycles. Each paired component supplies one directed rank-one block. Opposite singleton triangles supply a complete same-class block and one duplicate diagonal. Its counted calibration is rho c omega^(−hi²)−rho omega^(i²)+rho G omega^(−4hi²). Combining these triangles and calibration leaves precisely the paid target diagonal above. Thus the evaluator changes how the sum is calculated; it neither introduces a free diagonal into the grammar nor claims a new branch factorization. The full source-legal representation remains the accepted one.

## Exact collision and nonzero counts

The first middle support is {(b,a mod q):b≡k mod q}; the second is {(b,k):b≡−a−k mod q}. An intersection requires k=a mod q and 3a=0 mod q. Conversely these conditions make the two five-element supports equal. Since q is divisible by 3, there are three residues and five lifts each: fifteen overlapping rows, with five merged coefficients per row. The other N−15 rows have ten coefficients. Thus nnz=10N−75.

Cancellation in a merged coefficient would imply G is a root of unity; G²=N>1 excludes this in characteristic zero. The exact count is therefore stronger than a structural pattern count. Finite-field images have their guards and nonvanishing checked separately. For the small controls outside the family the corresponding formula is 10N−25 gcd(3,q), with 5 gcd(3,q) merged rows.

## Cold setup, composite transforms, routing and output

P[e]=omega^e costs N−1 multiplications. U[e]=rho P[e], V[e]=−rho G P[e] and D[i]=rho c P[−hi²] each cost N further multiplications. The 75 merged coefficients are prepared with 75 additions. Scalar synthesis and the optional checks omega^N=1, omega^(N/r)≠1 for r in {3,5,7,23} cost O(log N) field operations. The supplied root is used directly; finite test-prime/root searches are test-harness work, not an algorithmic oracle.

Because q=3^m7^m23^m, the transform plan is known. A literal radix-r level costs nr multiplications and n(r−1) additions, with combined twiddle coefficients drawn from P. Recursion gives 33mq multiplications and 30mq additions per q-transform. Two s-transform banks cost 66mN and 60mN. The middle’s nnz products and (nnz−N) additions, followed by N diagonal products and N additions, give the displayed totals. Products by one and zero inputs are still counted.

Index synthesis, gathers, scatters, sparse accesses, loop work, recursion allocations and scratch initialization are all O(N log q) word work. The fixed radix list avoids generic factorization. Modular products use a fixed number of O(log N)-bit words; the field slots are not assumed to have fixed bit width. The candidate’s eight length-N arrays plus less than 3q scratch field slots and 75 merged coefficients give its stated 8N+3q+75 field-slot bound. Integer storage is O(N). No expanded branch descriptor array is produced. Final output writes are O(N) and included.

The ambient field degree grows linearly with N. These field and word counts do not establish bit complexity or real-machine speed. The no-sharing scalar-cache-and-scatter observation in the candidate is only about that stipulated executor; it is not an arithmetic-circuit lower bound.

## Independent executable controls

check_independent.cpp was compiled afresh using the standard C++ library only. It does not load any other checker. It performs eight exact finite-field controls: q=1,3,7,21,69,483, plus second primitive-root embeddings at q=1 and q=3. All pass:

- Complete original-coordinate Green finite-walk matrix sums at q=1,3,7 and the second embeddings: 64,125 matrix entries, with Hamiltonian route coverage and paid calibration checked.
- Every basis vector at both embeddings of N=5 and N=45; deterministic dense vectors, and zero vectors at every size.
- Two-bank positive and negative q-DFTs independently compared with literal quadratic DFTs at every tested q, including all q=483 frequencies.
- Full shared outputs against the original two-DFT formula and original defining inverse at every size: 1,192,800 coordinates for each comparison across the controls.
- A complete directly evaluated basis column at q=21,69,483.
- Exact setup and online operation counts and every middle row’s support collision/nonzero count.
- Negative controls for wrong output-bank sign, wrong middle routing, omitted paid diagonal, imprimitive root and invalid finite-codec q.

At m=1 the reviewer independently selected p=39,659,131 and omega=7,465,461, distinct from the author’s p=18,663,121 image. A dense full shared output and the original defining inverse both pass all 1,166,445 coordinates. The basis-column and zero-vector shared applications also run at this size. All 11,664,375 coalesced middle coefficients are nonzero in this chosen field. No million-by-million matrix is built.

check_cyclotomic.py independently constructs Phi_N by exact integer polynomial division and works in Z[X]/Phi_N. At q=1,3,7 it verifies G²=N, the full Gauss sum, all 62,075 shared/target coefficient identities, and all 125 coalesced coefficient nonvanishing checks. At q=1,3 it checks 2,050 entries of the original inverse identity after clearing N and 1+c; symmetry also gives the opposite product. An exact wrong-sign control is nonzero. These small q values are controls, not members of the frozen m>=1 family. The all-m result is the proof above, not finite extrapolation.

check_bindings.py verifies candidate/source hashes, all copied reviews, author result ledgers, and the bound author cold receipt. The review’s own cold replay extracts the sealed review into a new directory, verifies its complete manifest, recompiles only the reviewer’s source, reruns all three checkers and compares parsed results. The sibling seal binds that receipt and the final archive.

## Attribution and disposition

The bounded-radix transform is classical; the candidate attributes Cooley and Tukey (1965), DOI https://doi.org/10.1090/S0025-5718-1965-0178586-1. The primary AMS endpoint returned 403 during this review; a university-hosted copy of the primary paper was reachable at https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Cooley65.pdf. No historical novelty conclusion is drawn from this limited check. The algorithmic recurrence itself is derived above rather than delegated to a citation.

The bounded shared-evaluator improvement preserves the branch-count interval, cold coloring cost, expanded-output cost, original two-DFT baseline, Model M/R restrictions, ordinary-order obstruction, all-Q(eta) impossibility, completed five-coordinate minimum-three result, and the open negative-family/all-N/stability/priority questions.

Derivative note: private tracking/integration instructions are omitted or restated as mathematical scope. Complete proof, model, evidence, costs, source limitations and open obligations are preserved. Original report SHA-256: `09dd60729e61ef9ae3e121d207e76adddbf114eff8fc26993c807911f9482494`.
