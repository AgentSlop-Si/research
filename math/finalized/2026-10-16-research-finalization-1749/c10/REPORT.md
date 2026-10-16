# C10: sorting and linear 2-CNF for the selected projective row subsystem

16 October 2026 UTC. Proposed bounded theorem increment; independent review pending. No external state was changed in preparing this report.

## Outcome and boundary

The accepted C10 gate's quadratic point-deduplication and pairwise-exclusion overhead can be replaced by sorting canonical projective labels and a linear-size sequential at-most-one encoding. For N vertices and M selected bilinear equations, the new solver uses O(N+M) field operations and graph work, O(M log(M+1)) canonical-key comparisons, and O(N+M) stored field elements/words, with normalization, exact representation, and root costs charged as specified below. With unit-cost field operations/inversion and constant-cost canonical-key creation/comparison, this is O(N+M log(M+1)); including target extraction gives S_B+O(N+M E_B+M log(M+1)).

This is an exact decision/reconstruction result for the selected projective subsystem only. It does not solve column compatibility, supported-entry scales, legal Green parameters, complete two-Green factorization, or a Fourier construction. It is not a bit-complexity bound. All-target extraction can still have M=O(N^3). No historical or worldwide novelty claim is made; sorting, sequential at-most-one encoding, and 2-SAT are standard algorithmic ingredients.

## Source and input model

The accepted source is REVIEW.md at repository commit 0339a31eb6109f0b96074ab8321f8653641e7530, Git blob 7bd7146ab8d8257f0b973bf9ccb7a3b1408e7fb8, archive SHA-256 93b237e0e3d425cc126df06c60d686ec644159fa31e035df38dc7bfa849f4835. Its exact pinned URL and inspection record are in SOURCE_REGISTER.json. The full review was read as inert text, including component domains, finite-field exhaustion repair, root/field distinctions, costs, and singular endpoint scope.

The input is a list of M directed equations u_j^T L_e u_i=0, with L_e in Mat_2(K), over an exact field K, on N projective unknowns u_i in P^1(F). Here F is either K or a specified algebraic closure of K. Loops, parallel edges, rank-one and zero matrices are allowed. The graph may be disconnected and N or M may be zero. The accepted source supplies the selected-system extraction and its necessity; the present increment starts from those matrices and does not rederive target-entry extraction.

Required field operations are exact addition, subtraction, multiplication, division by a certified nonzero element, and equality/zero tests. For the improved deterministic deduplication bound, the base field additionally has an exact canonical representation with a computable total order on its representations. Equal field elements must have identical keys; distinct field elements must have distinct keys. The order need not be a field order. For F_p, canonical residues 0,...,p-1 suffice; for other exact fields, representation creation, comparison and length must be charged. An equality-only abstract field oracle does not imply this sorting model.

## Algorithm

### 1. Rank-two forest and component transports

Let J=[[0,1],[-1,0]]. For rank-two L, the equation forces u_j proportional to A u_i, where A=J L is invertible. Reverse traversal can use adj(A), which is projectively A inverse and requires no division. Construct adjacency lists of all rank-two edges and a spanning forest. Set one root transport to I in each component, then propagate nonsingular 2-by-2 transports T_i along forest edges. Thus u_i=T_i z_C projectively, with one z_C per component C. This uses O(N+M) field/graph work, including all rank tests. A rank-two edge cannot join different final forest components.

### 2. Summarize every internal equation once

For every edge whose endpoints lie in C, form q_e(x,y)=(T_j(x,y))^T L_e T_i(x,y). This is a homogeneous binary quadratic, possibly zero, regardless of the original edge rank. Compute the gcd g_C(t) of all nonzero chart polynomials q_e(1,t). Also retain h_C, the Boolean statement that every q_e has zero y^2 coefficient. If all q_e vanish identically, mark the domain unrestricted.

For a restricted component, the permitted points are exactly [1:t] with g_C(t)=0, together with infinity [0:1] when h_C is true. Every gcd has degree at most two; each gcd update takes a bounded number of field operations, including any nonzero divisions. The summary therefore costs O(M) field operations. Membership of any named point subsequently takes O(1) operations, rather than checking it against every equation.

Reject any component with an empty domain. Over the algebraic closure, a restricted domain is nonempty exactly when h_C is true or deg(g_C)>=1, so no root extraction or quadratic-root test is required for this decision. Over K, use a certified base-field root-existence test when neither an allowed infinity nor an immediate linear root resolves nonemptiness. This is a separately charged operation; no quadratic formula or division by two is presumed.

### 3. Rank-one cross edges and canonical names

Ignore rank-zero cross edges. For a rank-one matrix L, choose a nonzero pivot L[r,c]=lambda. Let v be column c and w^T be row r. Since L=v w^T/lambda, and lambda is nonzero, the equation is equivalent to (u_j^T v)(w^T u_i)=0. After transports, it becomes (z_C=alpha) OR (z_D=beta), where alpha is the kernel line of w^T T_i and beta is the kernel line of v^T T_j. Both forms are nonzero, because T_i,T_j are invertible. Computing their kernel points requires no division.

There are at most 2M named point occurrences. Normalize every nonzero [x:y] to the key infinity if x=0, or finite(y/x) otherwise. Sort the occurrence records by (component identifier, infinity/finite tag, exact canonical scalar key). A linear scan assigns one flag X_C,a to each distinct named point in its component and records occurrence-to-flag references. The original edge clause is then emitted using those references in O(1), without a pairwise search or a later repeated dictionary search. Let K_names be the number of distinct flags; K_names<=2M.

This step uses at most 2M point-normalization inversions, O(M) remaining field/index work, and O(M log(M+1)) key comparisons. Key creation and comparison costs are not silently treated as unit cost outside the declared representation model.

### 4. Linear-size 2-CNF

Emit each positive cross-edge clause X_C,alpha OR X_D,beta. For every named point outside its component domain, emit the unit clause NOT X_C,a. Unit membership uses only the precomputed component summary.

For a component with k distinct flags x_1,...,x_k, emit no exclusion clauses if k<=1. If k>=2, introduce s_1,...,s_(k-1), and emit:

* (NOT x_i OR s_i), for 1<=i<k;
* (NOT s_(i-1) OR s_i), for 2<=i<k;
* (NOT x_i OR NOT s_(i-1)), for 2<=i<=k.

This has k-1 auxiliaries and 3k-4 clauses. If two flags x_a,x_b with a<b were true, the first two clause families propagate s_(b-1)=true, contradicting the third. Conversely, any assignment with at most one true flag extends by s_i=OR_(j<=i) x_j. Thus the encoding is exactly an existential at-most-one condition, without enumerating pairs.

Across all components, the number of variables is at most 2K_names<=4M; the number of clauses is at most M+4K_names<=9M. Build the implication graph and solve 2-SAT with a linear-time strongly connected component algorithm. No component-sized quadratic loop is used. Isolated components with no named flags need no Boolean variable.

### 5. Reconstruction, including all-false components

Domain nonemptiness was already checked. If a component has a true flag, choose its named allowed point. If all its flags are false, choose any point in its allowed domain. An unrestricted component may simply choose [1:0]; it need not search for an unnamed point. If the chosen point is named, set its single matching flag to true. This repair changes at most one false flag to true in that component; all other flags remain false.

The repair preserves positive cross-edge clauses, preserves at-most-one, and never turns on a forbidden flag. Recompute each auxiliary prefix s_i from the repaired flags; the original auxiliary assignment need not remain valid. Thus the repaired flags are exactly their equality meanings. This handles a finite unrestricted component even when every projective point is named, and a restricted component whether or not its permitted roots are named. No large at-least-one clause, root-list comparison, pair enumeration, or search for an unnamed point is needed.

Finally return u_i=T_i z_C. Every internal equation holds because z_C lies in its common-root domain; every cross edge holds because its positive equality clause is realized. If a compatible common output field representation is already available, direct evaluation of all M original equations costs O(N+M) operations in that representation. With only separate component root representations, one can instead verify internal equations within their component representations and each cross edge through the certified zero of one of its rank-one factors, without constructing a common compositum. Direct base-field evaluation certifies every returned finite-field test witness.

## Correctness proof

Completeness: a solution of the selected system induces forest component points z_C, all in their internal domains. Its named equality flags satisfy the positive cross-edge clauses, forbidden units, and at-most-one conditions. Set the auxiliary prefixes to the corresponding prefix disjunctions. The 2-CNF is satisfiable, and no true solution is rejected by the component-domain tests.

Soundness: if every component domain is nonempty and the 2-CNF is satisfiable, reconstruct points by the repair step above. The repaired assignment has exact equality meanings and still satisfies all cross-edge clauses and component domains. Transporting gives a nonzero projective direction at each vertex because each T_i is invertible. It satisfies every selected equation. If 2-SAT rejects, completeness shows that no selected-system solution exists. Thus decision and reconstruction are exact for F=K or the specified algebraic closure, subject to the field-specific domain test and witness operations.

The proof does not require characteristic different from two, squarefree quadratics, a finite base field, distinct roots, invertible original rank-one transitions, or an affine-only chart. Repeated roots only affect multiplicity, not point existence. Infinity is explicitly handled. The historical example xy, x(x-y), y(x-y) remains a valid tight three-equation obstruction and is not replaced by pairwise quadratic tests.

## Cost ledger and representation cautions

1. Input/extraction: if the accepted extraction uses setup S_B and per-target-entry cost E_B, its cost is S_B+O(N+M E_B). This is retained, not newly proved. An all-triples selection can have M=O(N^3).
2. Field arithmetic: O(N+M) operations, including O(M) divisions/inversions for constant-degree gcds and point normalization. Tree reverse transports and rank-one factorization can be division-free as described. If inversion is not a unit primitive, add its actual cost for every call.
3. Representation: create at most 2M exact canonical scalar keys; perform O(M log(M+1)) key comparisons, and store O(N+M) field elements/keys/indices. Add actual key lengths, copying/canonicalization and comparison costs. Algebraic and rational coefficient growth is not bounded here. This prevents an unsupported bit-complexity conclusion.
4. Graph/Boolean work: O(N+M), with at most 4M variables and 9M clauses. Sorting is the only superlinear combinatorial step in this implementation.
5. Base-field decision: add certified degree-two root-existence costs for restricted components unresolved by infinity/linear cases, at most O(M) nontrivial components. For an arbitrary field these tests are an explicit assumed capability, not an automatic polynomial-time algorithm.
6. Witness: add the costs of finding/representing any required allowed roots and doing output arithmetic. Over a closure, each component root can be individually represented in a degree-at-most-two extension, since its polynomial has degree at most two. A request for all coordinates in one common explicit extension may require a nontrivial compositum and is charged separately; the theorem does not assert that this representation has linear bit size. Closure decision alone uses no root extraction.

Under the declared unit-cost field/inversion and sortable-canonical-word model, the extraction-plus-decision bound is S_B+O(N+M E_B+M log(M+1)), plus base-field root tests when relevant. Witness/root-representation costs are additional. In an equality-only field model, deterministic sorting cannot be inferred; the accepted conservative quadratic bound remains an available fallback.

## Validation and limits

Fresh standard-library code and exact results accompany this report. The checker is newly authored for this increment. It does not execute, import, compile, or parse supplied research programs. Direct exhaustive P^1 assignment checks evaluate the original bilinear matrices independently of forest/domain/2-SAT reduction. The prime-field root routine in the test implementation enumerates field elements and is explicitly charged as an oracle cost; it is not presented as a fast large-field root algorithm. Large unrestricted stress cases make no such enumeration.

CHECK_RESULTS.json records 16,469 exact differential cases: 9,521 satisfiable and 6,948 unsatisfiable. These include every ordered pair of 2-by-2 matrices on parallel two-vertex edges and on a one-vertex loop system over F2 and F3; 2,800 seeded mixed graphs over F2, F3, F5 and F7; infinity, repeated-root, characteristic-two, three-quadratic obstruction, empty-graph, finite-field exhaustion and F241 base-field nonroot controls. All 2,047 Boolean flag patterns of sizes zero through ten match the sequential encoding's existential at-most-one semantics. Explicit forced-all-false tests cover unrestricted finite fields with every point named and restricted one/two-point named domains; repairs turn on exactly one permitted name and recompute auxiliaries. Stress systems with 1,000, 10,000 and 30,000 edges verify exact linear formula counts; the largest has 60,000 named flags, 29,999 auxiliaries and 119,996 clauses, without calling the enumerative root oracle.

These are exact finite controls, not a substitute for the general proof. General target-entry extraction and the historical N3/N5/Fourier construction controls are not replayed in this increment. The result is a bounded solver/encoding improvement, not evidence of a full target construction or historical novelty.
