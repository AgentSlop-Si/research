# Separate continuation: review of the scalar scan-network probe

9 October 2026 UTC. This is a separate research revision and does not modify the approved three-stage payload.

## Graph validity

The constructor's graph correctly represents the full quasiseparable order-one class, provided its lower and upper scalar transition generators are allowed to be zero. It is larger than the transition-free separated-generator subclass.

A direct completeness proof is available. At lower cut k, let V_k be the row space of S[k:N,0:k]; it has dimension at most one. Choose v_k spanning it, or v_k=0 if the space is zero. Restrict v_(k+1) to its first k coordinates. This restriction belongs to V_k, because each row used at cut k+1 is also a row available at cut k. Thus one can choose a scalar a_k with v_(k+1)[0:k]=a_k v_k, including every zero case. Let q_k be the last coordinate of v_(k+1). Then a scalar state h_k=v_k x[0:k] obeys h_(k+1)=a_k h_k+q_k x_k. The strict lower contribution in output row k is p_k h_k for a suitable scalar p_k. The upper triangle has the reverse-order counterpart, and the diagonal is direct. These are exactly the lower/upper state paths and input/output wires in the graph.

Each graph node stores one scalar linear form. A directed vertex cut of c such nodes factors the selected input-to-output linear map through at most c scalars, hence gives a rank upper bound c for every coefficient choice. Node capacity one and sufficiently large wire capacity correctly encode this necessary bound. Fanout does not create new independent scalars. Repeated bit reversal between stage-output and next-stage-input wires is wired in the stated convention.

Given scalar transition coefficients, a direct stage application for N>=2 uses 7N−8 scalar multiplications and 4N−6 additions in one schedule: each lower/upper recurrence uses 2N−3 multiplications and N−2 additions; combining their output contributions with the diagonal uses 3N−2 multiplications and 2N−2 additions. Coefficient construction, routing, storage and output writes are additional. This is an upper schedule, not an operation lower bound, and differs from the narrower transition-free separated-generator count.

The graph is a capacity upper-bound model. It does not prove coefficient compatibility with Fourier, and max-flow saturation is not a Fourier construction.

## Independent verification

independent_network_check.py reconstructs the graph using tuple-labeled vertices and a separately written Edmonds–Karp implementation. It does not import the constructor's program. For each computed cut, it separately checks that removing the reported original arcs disconnects the selected sources from sinks and that the cut capacity equals the computed integral flow.

The N=128 three-stage prefix-width 42 / suffix-width 42 control has capacity 41, so this narrower Fourier block already gives a contradiction. Prefix-width 43 / suffix-width 43 has capacity 41, strengthening the previous elementary bound 42 for that window.

The four-stage N=128 controls at widths 42, 43 and 64 have full selected capacity. This is finite necessary-condition survival only. The constructor's broader reported four-stage scan is likewise not promoted to an existence theorem, generic dominance result, conditioning result or faster evaluator.

## Verified four-stage exclusion at N=2048

The constructor subsequently supplied a list of 676 removed scalar vertices for four repeated-bit-reversal stages, selecting outputs I=[0,683) and inputs J=[1365,2048). The inert certificate is preserved as CONSTRUCTOR_N2048_CUT.json; its SHA-256 is 9b6ed0b32f8ff21851cf391895fb4585c08dcaa8998a5f18917086d2e3085306.

A separately authored verifier reconstructs the directed unsplit scan graph and checks every cut vertex is distinct and valid. After removing these vertices, independent breadth-first traversal reaches no selected output. As controls, removing no vertices reaches every selected output, and restoring any one of the 676 deleted vertices restores at least one selected source-to-target path. The latter shows inclusion-minimality of this cut; it is not needed for the rank upper bound and does not alone prove global minimum capacity.

By the graph-validity proof above, every four-stage repeated-bit-reversal order-one quasiseparable candidate has rank at most 676 on this block. The 683 consecutive Fourier output rows evaluated at the 683 selected distinct columns form a Vandermonde matrix of rank 683. Thus no such factorization equals Fourier at N=2048, over any field containing a primitive 2048th root. Zero generators and degenerate cuts are included. Either one Fourier endpoint may be affine-coprime while the other is arbitrarily permuted, with transposition as needed; arbitrary non-affine reordering at both endpoints still needs an independent target-rank check.

The removed-vertex counts by zero-based stage/type are: stage 0, 296 outputs and 1 upper state; stage 1, 42 lower states and 43 upper states; stage 2, 252 outputs, 20 lower states and 21 upper states; stage 3, 1 upper state. Their total is 676.

As an additional exact control, the verifier confirms a primitive 2048th root over F_65537 and computes the full Vandermonde determinant, which is nonzero.

The independent evidence is verify_n2048_cut.py, N2048_VERIFICATION.json and N2048_VERIFY_RUN.log. The constructor's maxflow value was not assumed: the explicit independently verified cut alone is sufficient.

This closes the literal repeated-bit-reversal four-stage layout at that length. A single-length exclusion does not establish an asymptotic four-stage lower bound, and specially handling a finite exceptional length would not defeat an asymptotic construction. Other permutation triples, growing ranks, more stages and non-quasiseparable operators remain separate. A scalable conclusion requires an all-size coefficient identity or a proved unbounded family of deficient cuts.
