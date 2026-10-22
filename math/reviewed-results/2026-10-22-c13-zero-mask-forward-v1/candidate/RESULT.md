# C13 prescribed-zero-mask forward constructor

22 October 2026 UTC. Owner: **C13-FIXED-DIRECTIONS**. This packet completes one
specified child gate, not the owner: an exact all-size constructor for supplied
legal invertible direction skeletons and prescribed zero/nonzero masks in the
one-sided endpoint grammar below. It is a standard useful construction; no new
algorithmic novelty, priority, or attribution claim is made.

## 1. Result, source boundary, and exact scope

For every admitted size and skeleton, a target has a completion in the stated
grammar if and only if its complete sandwich satisfies the sparse affine scale
equations together with the prescribed zero pins and nonzero exclusions. The
algorithm returns either actual-field scale values and valid forward Green
plans, or an exact off-support, affine-inconsistency, forced-nonzero-violation,
or finite-field-exhaustion certificate. No singular endpoint mask is inverted.
The packet also supplies an O(N) field-operation and index-operation executor
per vector, including zero edge weights, and charges dense reconstruction
separately.

This was not already asserted by the two immutable supplied sources:

- The accepted 10 October review assumes all x_i,y_j nonzero, explicitly says
  it does not establish a singular-endpoint converse, and requires a singular
  positive construction to supply a forward identity separately.
- The 19 October result explicitly leaves singular-mask work open and says
  singular endpoint masks require their own forward construction.

The displayed canonical plan formulas in those sources suggest this extension,
so the extension is not presented as a newly discovered identity. What is
completed here is the exact fixed-skeleton one-sided singular grammar,
construction/decision algorithm, verifiable negative outcomes, executable
forward plan, and accounting, with arbitrary prescribed mask patterns and all
admitted sizes. The inherited invertible-branch iff, entry-oracle adapter, and
prescribed-original-permutation recovery are dependencies, not new results.

Source commit: a8f8bc0cf82204267004df9f23d1ef02eda540b3, directory
math/finalized/2026-10-19-centered-support-entry-oracle-boundaries/c13/candidate.
Exact copies, Git blob IDs, SHA256 hashes, and source URLs are in sources/ and
SOURCE_BINDINGS.json. The worksheet owner remains TO RESEARCH, priority 34,
with supplied references Overview 218, Catalogue 101, novelty 149. This packet
does not modify that worksheet or any external resource.

Still open: general direction discovery, a theorem for arbitrary two-sided
singular endpoints, original endpoint values or restrictions outside the exact
grammar below, application-specific Fourier integration, any requirement that
the sum target be invertible, and historical attribution/primary comparison.

## 2. Exact input contract and one-sided grammar

Let F be the actual field. Use row-action permutation matrices
P_r[i,r(i)]=1. Input contains N>=2 and four **fixed structural permutations**
r0,r1,s0,s1. The prescribed source convention has distinct base/edge slots:
r0(i)!=r1(i) and s0^(-1)(j)!=s1^(-1)(j). Thus actual base/edge coordinates are
unambiguous. A Hamiltonian route is permitted at every N>=2; the theorem also
applies to any supplied permitted cycle partition with no singleton cycles.
One must check the requested cycle grammar, not silently substitute another
route or claim that every cycle partition is admitted by the original project.

This distinct-slot restriction matters: if r0(i)=r1(i), reading both a_i and
b_i as that same matrix entry does not yield the asserted two-term
factorization. We do not introduce a new labelled-coefficient convention for
singleton cycles and do not claim an N=1 extension of the inherited input
format. "All-size" here means every size in this exact source-compatible
contract, not a bounded-size experiment.

Input directions have no other nonzero entries and are specified by

    U[i,r0(i)] = a_i,       U[i,r1(i)] = b_i,
    V[s0^(-1)(j),j] = d_j, V[s1^(-1)(j),j] = e_j.

Require a_i!=0 and d_j!=0, separately from invertibility. Define

    rho   = r0^(-1) composed with r1,
    sigma = s1 composed with s0^(-1),
    W0 = -D_(b/a) P_r1 P_r0^(-1),
    W1 = -P_s0^(-1) P_s1 D_(e/d).

Then

    U = D_a (I-W0) P_r0,
    V = P_s0 (I-W1) D_d.

W0 has row-route rho and row weight w0_i=-b_i/a_i. W1 has row-route sigma and
row weight w1_i=-e_sigma(i)/d_sigma(i). In particular, the two relative orders
are different. Every prescribed cycle C must pass

    delta_l,C = 1 - product_(i in C) w_l,i != 0,  l=0,1.

The tests certify U,V invertible. They remain mandatory even when an entire
endpoint mask is zero. Edge weights b_i,e_j themselves may vanish. The supplied
routes remain fixed at those entries; zero edges never authorize a route
replacement. If full matrices are supplied instead of the sparse coefficient
representation, reading them and verifying that they have no other support is
an additional O(N^2) input validation cost.

Two prescribed subsets Zx,Zy encode the **exact** mask:

    x_i=0 for i in Zx; x_i!=0 otherwise,
    y_j=0 for j in Zy; y_j!=0 otherwise.

Nonzero magnitudes are free variables. The admitted branch family is exactly

    T0(x) = P_r0^(-1) (I-W0)^(-1) D_(x/a) = U^(-1) D_x,
    T1(y) = D_(y/d) (I-W1)^(-1) P_s0^(-1) = D_y V^(-1).

The first branch permits a singular **right** endpoint only; the second permits
a singular **left** endpoint only. Other factors are fixed and invertible.
This is a definition of the fixed-skeleton grammar, not a claim that arbitrary
singular Green branches can be normalized into it. In particular, no inverse
direction is recovered from a singular T0 or T1. The skeletons U,V are input.

The rank identities make the masks concrete:

    rank T0 = N-|Zx|,   rank T1 = N-|Zy|.

T0 has exactly the zero columns prescribed by Zx, and T1 exactly the zero rows
prescribed by Zy. Their sum can be singular or invertible; its rank is not
certified by branch rank counts. This task does not impose target invertibility.

## 3. All-size forward criterion and proof

**Theorem.** Under the exact guards in Section 2, B is a sum T0(x)+T1(y) with
the prescribed masks if and only if there exist x,y with those masks satisfying

    U B V = U D_y + D_x V.                         (1)

**Necessity.** For an admitted forward sum,

    U (U^(-1)D_x + D_y V^(-1)) V
      = D_x V + U D_y.

This multiplication is valid when D_x,D_y are singular, including zero.

**Sufficiency.** Multiply (1) on the left by U^(-1) and on the right by V^(-1):

    B = U^(-1)D_x + D_y V^(-1).

The two displayed factorizations in Section 2 give exactly the admitted forward
Green plans. Only U,V and their guarded denominator factors are inverted.
D_x,D_y are not inverted, and expressions D_(1/x), D_(1/y) are not formed.
This proves the converse directly; it is not an invocation of the inherited
invertible-endpoint theorem on singular data. QED.

No finite-size verification is used in this proof. The theorem permits every
mask pair, including both empty, both full, an identically zero branch, and
mixed patterns, at every admitted N and over every field satisfying the input
guards. If a particular field has no skeleton satisfying prescribed nonzero
edge restrictions and denominator guards, this is an input failure, not an
extension-field repair.

## 4. Full sandwich validation and sparse affine system

For every i,j, compute K_ij=(UBV)_ij. Each row of U and column of V has two
structural slots, so this uses at most four target entries. Let
S=supp(U) union supp(V), using the actual nonzero support after zero edge
weights are accounted for. Since |S|<=4N, equation (1) is precisely:

- For every (i,j) outside S, require K_ij=0.
- For every (i,j) in S, impose

      V_ij x_i + U_ij y_j = K_ij.                 (2)

- Add each prescribed zero pin x_i=0 or y_j=0, and require every remaining
  variable to be nonzero.

Every off-support position must be checked, including positions on a structural
edge whose actual coefficient is zero in both U and V. Row-pair gates,
pairwise nullspaces, and consistency of just a sampled support system are not
substitutes. An off-support failure has a short exact certificate: position
(i,j), its four input target entries, and the nonzero evaluated K_ij. The
reference output records position and residual; the verifier reacquires the
four entries from the same coherent exact target oracle.

## 5. Exact affine-mask solver and negative certificates

Write all variables as z_0,...,z_(2N-1). For a supported equation A z_u+B z_v=k:

1. If both coefficients are nonzero, use the invertible affine transition
   z_v=-(A/B)z_u+k/B and its reverse to build a graph edge.
2. If just one coefficient is nonzero, it pins that variable.
3. If both are zero, require k=0. This third case is included in the standalone
   solver even though actual supported matrix positions have a nonzero
   coefficient.

Build a spanning forest of the two-nonzero-coefficient graph. In each component
choose a root parameter t, and propagate

    z_v = alpha_v t + beta_v,  alpha_v != 0.

This uses only divisions by the nonzero coefficients already tested. Every
non-tree equation, one-variable equation, and prescribed zero mask becomes
C t=R. In particular a zero pin at v yields

    alpha_v t = -beta_v.                          (3)

Check all these constraints. A residual 0=R!=0 is a contradiction; incompatible
nonzero-coefficient constraints force two distinct values of t and are also a
contradiction. Otherwise the parameter is either uniquely forced or free.

Each required-nonzero variable excludes exactly

    t != -beta_v/alpha_v.                         (4)

Variables required to be zero are pins, not forbidden roots. Consequently an
isolated zero variable is correctly fixed to zero; it is not erroneously
rejected by the inherited all-nonzero test. A component containing a zero pin
has a forced parameter, because alpha_v is nonzero.

For a forced t, check every required-nonzero variable. For a free t, choose an
element of the **actual field** outside the union of excluded roots. If there
are r required-nonzero variables, at most r field elements are forbidden.

- Over an infinite field, such an element exists. An effective constructor
  needs a representation, equality test, and generation of r+1 distinct field
  elements; charge those operations explicitly. The integer list 0,...,r is
  valid over Q or characteristic-zero subfields, not arbitrary infinite fields
  of positive characteristic.
- Over a finite represented field F_q, generate min(q,r+1) distinct elements of
  F_q. If none is permitted, q<=r and the tested list is the complete field:
  exhaustion is exact. Finite extensions require their own field-element
  representation and enumerator. They are not replaced by integer residues
  modulo q, and an extension of the original field is never substituted.

The resulting choices independently solve all components, hence (2) and the
exact masks. Equation (1) then produces the valid forward plans by Section 3.

**Certificate format.** The sparse input equations, forest edge indices, affine
forms alpha,beta, and substituted root constraints allow a verifier to check
each derivation locally. The returned outcome is one of:

- Positive: x,y, the exact mask, and both guarded forward Green plans.
- Off-support failure: the location and exact nonzero sandwich residual.
- Affine contradiction: an original zero-coefficient contradiction or a
  substituted constraint 0=R!=0.
- Conflicting pins: two verified constraints C t=R and D t=S with C,D nonzero
  and R/C!=S/D. Pins may arise from the mask itself.
- Forced nonzero violation: a root-forcing constraint and a required-nonzero
  variable that evaluates to zero at that root.
- Field exhaustion: an unforced component and, for every element of the actual
  finite field, a required-nonzero variable that vanishes at that element.

These are distinct causes. "No solution" does not mean the whole target has no
Green representation; it excludes only this skeleton and prescribed masks.
Malformed routes, zero base coordinates, singular denominators, unsupported
field encodings, or unavailable element generation are input/representation
failures, not completion-infeasibility certificates.

## 6. Forward Green application with zero edges

A plan is executable without forming a dense inverse. On a cycle
q_0,...,q_(m-1), where rho(q_k)=q_(k+1 mod m), solving (I-W)h=c means

    h_qk = c_qk + w_qk h_q(k+1).

Set p_0=1 and p_(k+1)=p_k w_qk. Expanding once around the cycle gives

    h_q0 = (sum_(k=0 to m-1) p_k c_qk)/(1-p_m).

Then compute h_q(m-1),h_q(m-2),...,h_q1 by the original recurrence, using the
already known successor value. There are O(m) field operations. The only
division is by the guarded nonzero cycle denominator; individual weights may
be zero. A forward recurrence that divides by w_qk would be invalid here.

To apply T0, multiply the input by D_(x/a), solve the W0 cycles, then apply
P_r0^(-1). To apply T1, first apply P_s0^(-1), solve the W1 cycles, and multiply
by D_(y/d). Sum the outputs. Thus one full plan application uses O(N) field and
index operations and O(N) working storage. Applying to N basis vectors forms
the dense sum in O(N^2) field operations; the dense output has N^2 entries.
The sparse plan itself occupies only O(N) field elements and route indices.

The preceding formulas also prove all denominator checks are sufficient even
with zero edge weights. There is no hidden inversion of a mask or an edge.

## 7. Projective gauge compatibility, not an endpoint-recovery theorem

For nonzero lambda_i,mu_j, replace U by D_lambda U and V by V D_mu. Then choose
x'=lambda*x and y'=mu*y coordinatewise. Zeros and nonzeros are unchanged, W0,W1
and their routes remain unchanged, and

    (D_lambda U)^(-1) D_(lambda*x) = U^(-1)D_x,
    D_(mu*y) (V D_mu)^(-1) = D_y V^(-1).

Thus this extension respects the inherited projective directions, including
the exact zero mask. A solver need not choose the same representative among
multiple feasible scales after a gauge change; the solution sets and realized
branches correspond by the displayed map.

This is not a new theorem about separately prescribed original endpoint
permutations or values. If a caller has that stronger contract, an appropriate
forward adapter must verify it; the old inverse-based endpoint recovery cannot
be blindly applied to a singular branch. We leave values/restrictions outside
the displayed one-sided grammar open rather than silently freeing them.

The scope distinction is strict, not merely cautious wording. Over Q, let N=3,
P be the successor cycle, U=I-2P and V=I with its prescribed zero-weight cycle.
Then U^(-1)=-(I+2P+4P^2)/7. The two-sided singular branch

    E_00 U^(-1) E_11 = -(2/7) E_01

is not U^(-1)D_x+D_y for any x,y, with any masks. Entry (0,1) forces x_1=1,
while entry (2,1) forces x_1=0. Thus the new grammar must not be advertised as
exhausting arbitrary two-sided singular-endpoint branches, even on the same
invertible skeleton. A fresh exact control also verifies its rejection.

## 8. Costs, effective fields, and reference implementation

Let T_F be field setup/validation cost; T_B target setup cost; T_entry the cost
of one coherent exact target entry; and T_gen the cost of generating the needed
actual-field candidates. Charge target-entry normalization separately if the
callback does not already return canonical represented field elements.

- Validate supplied sparse routes, base coordinates, and denominators: O(N)
  field operations and O(N) storage. Permutations use linear seen-array/index
  validation. The reference implementation sorts supplied cycle-length lists
  to compare cycle types, charging O(N log N) integer comparisons in general;
  the default Hamiltonian check has a single cycle-length comparison.
- Complete target sandwich scan: at most 4N^2 target callbacks and 12N^2 field
  operations, plus O(N^2) equality/index checks. Repeated callbacks count again;
  no memoization or free target setup is assumed. Early rejection can cost less.
- Sparse supported solve including zero pins: O(N) field operations and O(N)
  storage for at most 4N supported equations and 2N mask decisions. Explicit
  candidate membership and exhaustion witnesses cost O(N^2) field-element
  comparisons conservatively, plus T_gen. No constant-time field-enumeration
  assumption is hidden.
- Emit scale values and sparse plans: O(N) field operations and O(N) storage.
- Apply the prepared plans to one vector: O(N) field/index operations and O(N)
  working storage, plus representation costs. Form a dense output matrix only
  when requested: O(N^2) field operations and O(N^2) output storage (or O(N)
  working storage with columns streamed).

The reference constructor therefore has a field-operation/comparison bound

    T_F + T_B + 4N^2 T_entry + T_normalization + T_gen + O(N^2),

with the preceding O(N log N) integer cycle-type comparison cost stated
separately. Auxiliary storage is O(N), excluding the target's own
representation, full-matrix input validation, dense output, and optional logs.

**Bit accounting is not suppressed.** Every field operation, division,
comparison, exact entry, normalization, and generated element must be charged
in its supplied representation. More explicitly, if L_* bounds the bit lengths
of all represented intermediate field elements in this execution, A_F(L_*)
bounds one exact field arithmetic/division operation, and E_F(L_*) bounds one
equality comparison, the non-oracle construction cost is bounded by
T_F+T_normalization+T_gen+O(N^2 A_F(L_*)+N^2 E_F(L_*)+N^2 log N) bit
operations, using O(log N)-bit indices. The last term conservatively charges
the full index scan and cycle-type comparisons; input/output encoding is
additional. Per-vector
application similarly costs O(N A_F(L_*)+N log N) with that application's own
intermediate bound. This is explicit representation-sensitive accounting, not
a polynomial bound on L_* in arbitrary black-box field input size.

Over Q, rational numerators/denominators are exact and may grow; L_* is not the
initial bit length and the Python Fraction operations include reduction/gcd
costs. Over F_p, canonical field elements have O(log p) bits, but modular
inversion/multiplication and prime validation are not unit-cost bit operations.
The reference uses trial division for primality, charged in T_F; no efficient
primality claim is made. Other finite fields require a separately validated
field representation, not an integer-composite modulus.

`constructor.py` implements Q and prime F_p only. It accepts exact integers or
Fraction objects and rejects floats rather than truncating them. Fraction
normalization modulo p requires a nonzero denominator and is explicitly counted
in target_normalization_field_ops separately from sandwich_field_ops. The
plan executor also validates vector length and normalizes exact scalar inputs
before application, with that O(N) normalization cost charged to application.
The
prepared skeleton must come from prepare_skeleton and must not be modified;
construct does not re-audit a caller-tampered preparation object. A target oracle
must be coherent and exact. Other effective fields are covered by the proof
with their stated field-generation interface, not by this reference program.

No target inverse or determinant is computed by this constructor. If a
forced-feedback application additionally requires B invertible, its certificate
or computation and costs remain separate. No fast Fourier implementation or
structured-target lower bound follows from the supported O(N) graph solve.

## 9. Fresh controls and reproducibility

Run `python3 -B check.py` in this candidate directory. This uses only the fresh
constructor and the Python standard library. It does not import or execute any
supplied/historical program. CHECK_RESULTS.json records the deterministic seed
and outcomes. Fresh exact controls currently pass:

- 1,152 affine-mask systems over F2,F3,F5 compared with exhaustive assignments,
  including every mask pattern for each sampled four-variable system; emitted
  positive and all four sparse-negative certificate types are independently
  checked from their defining equations.
- 225 exact dense target constructions over Q,F2,F3,F5,F7 at N=2,...,10, with
  nontrivial endpoint permutations, Hamiltonian and admitted multiple-cycle
  routes, zero edges, all-zero and mixed masks, and branch-rank checks.
- 225 projective-gauge controls, including mapped original witnesses, plus full
  basis reconstruction from the newly selected plans.
- 1,350 original-plan basis output vectors, covering 9,600 original target
  entries; all gauge variants also undergo full basis reconstruction.
- 201 exact off-support perturbation rejections; explicit zero-base,
  singular-denominator, illegal fixed cycle type, support-collision, composite
  modulus, exact-scalar typing, separately counted normalization, mask-pin
  contradiction, finite-field exhaustion, singular-sum, and excluded two-sided
  endpoint controls.

A diagnostic over F2 makes the extension nonvacuous: with U=V=I, fixed legal
zero-edge structural cycles, and B=I, the all-nonzero scale requirement is
impossible because x_i+y_i=1 has no pair of nonzero F2 values. Prescribing every
x_i=0 and every y_i nonzero instead yields x=0,y=1 and the valid singular-first-
branch sum 0+I. Prescribing both x_0=y_0=0 contradicts the same target. This
distinguishes zero-mask construction, forced mask failure, and actual-field
exhaustion; no extension field is used.

These bounded controls test formulas, certificates, route order, masks, and
operation accounting. The all-size theorem and solver correctness are proved
in Sections 2-6, not inferred from these examples. Independent acceptance is a
separate review step; this candidate file does not self-award that status.
