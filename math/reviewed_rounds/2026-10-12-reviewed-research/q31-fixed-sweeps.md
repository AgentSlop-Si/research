Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 1e11e4b1ff34314e6742abcc85322e158d0d76b8157822dc8114e01fedab8ed4

---

# Independent review of the Q31 regular sweep obstruction

Date: 12 October 2026 UTC.

## Verdict

ACCEPT_SCOPE_LIMITED, subject to the exact final author-byte binding in INPUT_BINDINGS.json. The formal transcript argument, Fourier rectangle argument, and fixed-sweep reduction are valid. No positive Fourier source is supplied. Q31::regular-shared-jet remains open. This is an additional scoped obstruction, not a solution of the constructive gate or a general Fourier arithmetic lower bound.

The author made the requested interface clarifications before sealing: the source reads original Fourier coordinates, final readout cannot access Alice's raw inputs without additional counted crossings, and multivariate jets or derivative/coefficient oracles cannot be treated as one primitive field register. The core rank lemma is explicitly attributed to classical work. No mathematical correction to the final factorization was required.

## Exact accepted model

Let K be a field of characteristic other than two, with a supplied element omega of exact order N >= 2, and set F_N[i,j] = omega^(ij). The source is an actual scalar rational arithmetic program using input-independent constants, additions, subtractions, multiplications, and inversions. Every inverse is defined at the actual zero-input execution. The required identity is a formal Hessian identity Hessian(Phi)(0)=F_N, not equality of function values on finite-field points.

For the sweep conclusion, p >= 1 full scans read the original coordinates x_0,...,x_(N-1) in that fixed left-to-right order. Initial state is input-independent. At most w scalar field registers carry computed input-dependent information between positions and scans. Any separate accumulated output, derivative coefficients, caches, or stored intermediate values crossing the cut belong in the interface. The final readout is origin-regular and uses the final state, with at most direct access to Bob's local raw suffix. Any other input reads or input-dependent communication must be counted separately.

Then (2p-1)w >= floor(N/2). More generally, the sum of the scalar interface widths over all crossings of the balanced cut is at least floor(N/2). A true alternating-direction p-scan schedule has p such crossings and therefore pw >= floor(N/2), provided output remains local at its final endpoint.

The theorem permits nonlinear state transitions, repeated input reads within their paid schedule, zero gains, noninvertible updates, and input-dependent regular coefficients computed from available values. Its proof does not assume a fixed linear transcript, generic Jacobian rank, nonzero transition determinants, or constant-rank neighborhoods.

## Independent proof audit

For a two-party protocol, put all c scalar messages in a triangular transcript t. Each message is a regular rational function of the sending party's own raw inputs and earlier messages. Retaining the entire old transcript for the proof is a relaxation of the actual memory model and is therefore legitimate. Vector state messages can be scalarized without changing c; simultaneously computed coordinates do not need to depend on earlier coordinates in their own message.

Choose constant reverse multipliers at the actual transcript basepoint so that the constraint Lagrangian L equals the output on the transcript and L_t=0 at that point. Every local constraint and the output depends directly on at most one party's raw input, so L_ab=0 with independent transcript coordinates. The mixed chain rule is therefore exactly

    Phi_ab = L_at T_b + T_a^T L_tb + T_a^T L_tt T_b
           = L_at T_b + T_a^T (L_tb + L_tt T_b).

There is no missing transcript mixed-derivative term: its coefficient L_t vanishes. There are no derivatives of the multipliers: these are constants chosen at the basepoint, and the equality along the transcript holds for every fixed choice of their values.

Let J be the strictly lower triangular matrix of message derivatives with respect to earlier transcript coordinates. Implicit differentiation gives (I-J)T_a=D_a and (I-J)T_b=D_b. The matrix I-J is invertible over every field because it is unit lower triangular. D_a has nonzero rows only for Alice messages, and D_b only for Bob messages. Thus rank(T_a)<=c_A and rank(T_b)<=c_B. The displayed factorization proves rank(Phi_ab)<=c_A+c_B=c, not merely 2c. No inverse of a state transition or direct-input derivative is taken.

Rational local computations can be inlined into these functions while preserving regularity at the enlarged basepoint: each original inverse denominator remains nonzero when earlier transcript coordinates are set to their actual values. This is why actual-program regularity is sufficient and a symbolic removable singularity in an unregularized program is not.

For m=floor(N/2), rows 0,...,m-1 and columns m,...,2m-1 of F_N give the Vandermonde matrix with nodes omega^m,...,omega^(2m-1). Their distinctness follows from exact root order. Its nonzero determinant proves rank m. For odd N, assign the remaining final coordinate to Bob; the same square minor remains valid. No assumption about all Fourier minors, prime N, numerical conditioning, or an uncertainty principle is used.

The scan simulation makes p Alice-to-Bob transfers and p-1 Bob-to-Alice transfers of at most w scalars. The output is already at Bob, so no final return transfer is required. This establishes the exact coefficient 2p-1. If the output is instead required at Alice, or a postprocessing step reads Alice coordinates, the extra communication must be counted rather than silently applying the same coefficient.

## Exact sharpness and controls

The displayed polynomial

    Phi=(1+b3)((1+a2)(a1*b1+b2)+a3)

has mixed Hessian I_3 at zero. The reviewer separately replayed its literal one-register update expressions in two natural-order scans and symbolically expanded their output. This attains rank 3 with three scalar boundary messages. It refutes both rank<=w and rank<=pw for repeated same-direction scans. The multiplication by b1 has zero base gain, so the control also checks that zero transition gains do not invalidate the proof.

An independently found second polynomial,

    Psi=(1+b3)(1+a3)(a2+(1+b2)(a1+b1)),

has mixed Hessian [[0,1,1],[0,0,1],[1,0,0]], determinant one. Both controls are exact sharpness examples for the separator coefficient. Neither is asserted to be a Fourier source, to have zero linear jet, or to prove an optimal Fourier implementation for all p,w,N.

Fresh reviewer code, written from the displayed mathematics, passed 401 exact assertions. It uses SymPy 1.14.0 independently of the author's derivative-jet implementation and imports no author or recovered research program. There are 24 symbolic rational protocols with zero through seven messages, inverses, nonzero transcript basepoints, mixed message owners, and both output-party choices. Direct quadratic Taylor composition is checked against the frozen Lagrangian factorization, triangular implicit derivatives, ownership ranks, and final mixed rank. There are also 31 exact finite-field Fourier rectangle checks for N=2,...,32, literal sharpness controls, and countercontrols for uncharged global preprocessing and unrestricted final readout. The universal result rests on the proof, not extrapolation from these cases.

The author's own reported 9,681 assertions are provenance, not reviewer replay credit. The author code remains inert. Source bindings and author manifest are separately checked byte-for-byte when sealed.

## Boundary and accounting findings

- Unrestricted final access to both raw input blocks would invalidate the claimed scan count: a free final readout could directly compute any cross bilinear form with no prior state. The final report explicitly forbids this shortcut.
- Dense preprocessed forms z=Px can mix both parties' original inputs. A short source scanning z is not automatically a short source scanning x. Its preprocessing and access interfaces must be included. The report explicitly uses original x order.
- The protocol theorem grants private local preprocessing and private memory. That strengthens the lower bound's applicability; it does not authorize uncounted cross-party precomputed data.
- An output accumulator that crosses the cut is a state register. Write-only output fragments aggregated later require their own information interface unless that aggregation is genuinely local and already represented in the protocol.
- Input-independent constants and their preparation can be granted free for this negative result. This does not excuse their omission from a future positive Q31 construction's bill.
- Formal multivariate jet coefficients cannot be packed into one scalar and manipulated by arbitrary free coefficient extraction. A jet algorithm must lift to the stated scalar arithmetic program, or every stored scalar coefficient must be counted in its different model.
- The bound is a field-scalar space/pass restriction. It implies no bit-space, stability, finite-word, arbitrary DAG, or universal FFT operation lower bound.
- The optional pN update-count consequence applies only to an implementation actually performing N updates per scan, with w>0. No-op input visits cannot be silently counted as nontrivial field operations.

## Scope and remaining work

The mixed-Hessian communication bound is classical Abelson. A verified primary account is Luo and Tsitsiklis, On the Communication Complexity of Distributed Algebraic Computation, JACM 40(5), 1993, section 1.1 (protocol model), section 5.1 Theorem 5.1, printed page 1035 (bound and attribution): https://www.mit.edu/~jnt/Papers/J047-93-luo-algebr.pdf . The paper also treats real and complex protocols; the packet supplies a self-contained formal-field proof. No broad novelty audit or priority claim for the Fourier/sweep application has been established.

Q31’s positive constructor remains open. No generic Green-family cutoff, exceptional Green locus closure, or impossibility for arbitrary O(N)-workspace/O(N)-work scalar DAGs follows. The accepted sweep model and counted-register interface are required.
