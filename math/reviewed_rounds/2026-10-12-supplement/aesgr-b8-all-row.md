Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: ddb817372c777e813265bb853f76b2a868164ce6a26ea61e37ebb4cda433708e.

# Independent bounded acceptance: AESGR B=8, q=2

Date: 2026-10-12 UTC. Family: AESGR.

## Decision

ACCEPT the exact B=8, q=2, depth-10 full-row Fourier construction in the previously accepted core Hamiltonian-Green/nonzero-diagonal grammar. ACCEPT its strict canonical immutable prepared API and its stated field-arithmetic ledgers under the precise supported input and cost model below. There is no requested repair and no identified mathematical or boundary defect within that model.

This closes only the finite q=2, B=8 all-row experiment. The accepted B4 result and its original, narrower API contract remain unchanged. This is a finite classical radix-2 FFT translation into the Green grammar. It proves no uniform fixed-depth family, arc-capacity saturation, special arc-code or global-rewiring architecture, varying-q coefficient-generation theorem, asymptotic improvement, optimal depth, or novelty. The broad AESGR record remains OPEN.

The exact candidate is AESGR_B8_Q2_Full_Row_CANDIDATE_2026-10-12.zip, 635,676 bytes, SHA256 77616a5f31ab85031657be3e2897adc628592d150c233238b520f131fa6877df. Its 21 members and complete 20-entry payload manifest were verified. The fresh source and certificates tested by this review are byte-identical to that archive.

## Algebra and conventions independently checked

Vectors are columns; indices are 0 through 7; F[i,j]=zeta^(ij). The supplied root belongs to K=Q[t]/(t^4+1), and satisfies zeta^4=-1. In characteristic zero it therefore has exact order eight. The four roots t, t^3, t^5, t^7 are all supported; none is silently substituted for another. No root extraction or field extension is generated. Field degree over Q is four; generated extension degree relative to the supplied field is one.

For a matching ((a0,b0),...,(a3,b3)), the cycle order is (a0,a1,a2,a3,b0,b1,b2,b3). Its outgoing gains are (1,1,1,1,1,1,1,-1), meaning W e_v[k] = g[k] e_v[k+1]. This explicitly resolves the original source's shifted edge subscripts. Hence W^8=-I. On each ordered pair (a,b), W^4 is [[0,-1],[1,0]].

Write iota=zeta^2. W, -W, iota W, and -iota W are legal weighted Hamiltonian cycles. Each has nonzero edges and holonomy -1, so I minus that cycle is invertible and the Green denominator is 2. The two branches of each layer share an order but are distinct weighted operators. This is the same core-grammar interpretation accepted in B4. It does not establish the additional independent arc-code separation or global rewiring requirements elsewhere in the source.

For A=(G_W+G_-W)/2 and B=(G_iotaW+G_-iotaW)/2, direct multiplication establishes A=(I-W^2)^-1 and B=(I+W^2)^-1. Both factors are invertible: each comes from products of already invertible I minus/plus a legal cycle. They commute as rational functions of W, and BA=(I-W^4)^-1. On each pair this is (1/2)[[1,-1],[1,1]]. With E=diag(1,-1) on each pair, H=2BAE is the usual simultaneous pairwise Hadamard butterfly.

The three DIF matchings M0=((0,4),(1,5),(2,6),(3,7)), M1=((0,2),(1,3),(4,6),(5,7)), and M2=((0,1),(2,3),(4,5),(6,7)) give the full eight-point cyclic transform in bit-reversed output order after the stated twiddles T0 and T1. Primitive eighth-root phases enter T0 explicitly, so this is not a tensor-product character table with missing cyclic phases.

The output permutation exchanges (1,4) and (3,6). Let R=((1,4),(3,6),(0,2),(5,7)), and J=diag(1,1,1,1,-1,1,-1,1). Then (1/2) H_R J H_R is exactly that permutation, since H^2=2I on the fixed pairs and H diag(1,-1) H=2 swap on the exchanged pairs. Those two additional butterflies consume four Green layers; output routing is not free.

Thus the five butterfly stages M0, M1, M2, R, R expand to ten two-branch Green layers with all eleven diagonals exactly as serialized in the candidate. The final diagonal 16I accounts for 2^5/2. All 88 diagonal entries are nonzero. The proof establishes arbitrary-input correctness by linear identities, beyond the finite test set. The review also independently assembled every Green inverse by exact Gauss-Jordan elimination, verified both left and right inverses, multiplied the full dense operator, and checked every matrix entry for each permitted root. These dense operations are verification only.

For Weyl covariance this review uses S e_j=e_(j+1 mod 8) and D=diag(zeta^i). The certificate satisfies M e_0=1 and MS=DM. A reversed shift or a negative-exponent Fourier convention must not be silently substituted.

## API boundary

The exposed compiler has fixed B=8, q=2, depth=10. It accepts a built-in int, an exact Fraction, or a built-in four-entry list/tuple with int/Fraction coefficients. Bools, float/complex approximations, subclasses and malformed scalar shapes are rejected. Nonprimitive roots are rejected.

prepare_certificate admits only canonical built-in JSON containers, exact fields and sizes, canonical four-rational-string scalars, genuine integer dimensions and indices, valid orders and inverse orders, and the checked nonzero edges, alphas, diagonals, holonomies, denominators and reciprocals. It then regenerates the known formula from the supplied root and compares every scalar and order. Structural legality alone is not Fourier certification. This narrow public admission theorem covers the canonical family only; a different correct certificate requires a separate admission theorem.

The returned Prepared object and its nested dataclasses are frozen and slotted, with recursively immutable tuples. The source certificate can be destroyed or changed after preparation without affecting execution. execute accepts only this module's exact Prepared type with its seal, admits exactly eight inputs into a value snapshot, and returns eight explicit exact outputs. It rejects raw JSON, structure-only objects, empty or improperly constructed Prepared objects, generators, extra/missing inputs, booleans, approximate numbers and numeric/container subclasses.

This is an accidental-mutation interface, not a hostile Python object sandbox. Reflective object.__setattr__, alteration of private Fraction/module internals, untrusted executable code, and concurrent mutation during admission are outside the supported model. These exclusions are explicit in the candidate; this review does not claim stronger security or concurrency guarantees.

Independent boundary evidence includes 420 original structural/canonical rejections, 34 additional interface rejections, and 217 further controls. Of the latter, 148 are structurally legal noncanonical changes, including every diagonal slot, every branch alpha, two-edge sign changes preserving holonomy, and reordered cycles with correctly recomputed inverses. All were rejected by canonical preparation. Consistently singular cycles, container subclasses and noncanonical strings were rejected. Eight separate snapshot/frozen/shape controls passed.

## Arithmetic ledger independently reconstructed and instrumented

Counts are operations over K, including operations on zero, one, and signs. They are not machine instruction counts or rational bit complexity. The reviewer replaced the candidate's entire Ops implementation with separately authored arithmetic and a global audit counter; both the independent counts and returned counts agreed.

Compiler only:
- Multiplications: 3 supplied-root powers/order checks + 24 merged diagonal entries + 80 phase/gain products + 160 holonomy products = 267.
- Additions: construct 2,4,8,16 = 4.
- Subtractions: construct -1 + 80 negative branch gains + 20 denominators = 101.
- Divisions: one common half + twenty explicitly computed reciprocals = 21.
- Scalar equalities: one root-order predicate + twenty nonzero-denominator predicates = 21.

One structural pass:
- 2 root-check + 160 holonomy + 20 reciprocal-verification multiplications = 182.
- 20 denominator subtractions; no additions or divisions.
- 329 scalar comparisons: root 1, edge nonzero 160, alpha nonzero 20, holonomy 20, denominator nonzero 20, reciprocal 20, diagonal nonzero 88.

Canonical comparison adds 309 scalar comparisons, plus 320 stored order/inverse-index comparisons charged as nonfield work. Regenerating its canonical template adds the entire compiler ledger. Consequently prepare_certificate is 449 multiplications, 4 additions, 121 subtractions, 21 divisions and 659 scalar comparisons. compile_prepared additionally charges the original compiler, for 716 multiplications, 8 additions, 222 subtractions, 42 divisions and 680 scalar comparisons. Calling either helper again incurs its cost again; there is no implicit cache exemption.

For one Green branch, the seven-step forward pass costs 7 multiplications/7 additions. Closure costs 2 multiplications/1 addition using the prepared reciprocal. Reconstruction costs 7 multiplications/7 additions. Thus each branch costs 16 multiplications and 15 additions, with no online division. Each of 20 branches was also checked on fresh exact vectors against its independently computed inverse and the residual equation (I-W)y=x.

Per fresh full vector:
- 20 Green actions: 320 multiplications and 300 additions.
- Branch weighting: 160 multiplications.
- Ten two-branch sums: 80 additions.
- Eleven eight-entry diagonal actions: 88 multiplications.
- Total: 568 multiplications, 380 additions, no subtractions or divisions. No roots are extracted or generated online.

Independent structural counting confirms 629 model scalar/index slots: 160 orders, 160 inverse orders, 160 weights, 20 alphas, 20 holonomies, 20 reciprocals, 88 diagonals, one root. There are 309 field scalars; the implementation encodes each by four rational components. The 629 number is not bytes or the total number of rational components.

The omitted nonfield costs are disclosed rather than assigned zero: schema and type tests, dimensions, indices, canonical string parsing, Fraction normalization and arithmetic, coefficient/input copying, creation of the immutable snapshot and the regenerated template, allocations, loops, routing, temporary branch vectors, metadata, JSON and object overhead, and eight explicit input/output slots. These have bounded fixed-size word/data traffic, but rational numerator/denominator bit lengths can grow with input size. There is no bit-complexity, numerical-stability, varying-B, wall-clock, or practical speed guarantee. Fixed-loop O(depth*q*B) descriptions refer only to this bounded instance and do not provide the uniform family required by AESGR.

## Fresh evidence and regression controls

Independent main checker, not the author's oracle:
- Four primitive-root conventions, all 256 matrix entries across them.
- 80 full Green inverses, each checked on both sides.
- 20 two-layer quadratic-filter matrix identities.
- 32 seed and 256 Weyl equations.
- 32 production basis vectors, 128 production fresh vectors, 512 fresh vectors using independently replaced scalar arithmetic.
- 160 fresh branch residuals, with exact per-branch arithmetic ledgers.
- Boundary, immutable snapshot, and storage counts stated above.

Known-wrong but structurally legal controls fail the full matrix and are rejected by preparation: half output scale changes 64/64 entries; missing output bit reversal changes 28/64; replacing iotaW filtering with W filtering changes 44/64; changing only the supplied-root label to its conjugate changes 32/64. No successful first-row or seed-only test was accepted as a full-row certificate.

The author's fresh checker was separately replayed in an extraction of the sealed candidate. Its 1,024 fresh vectors and own checks passed. All 20 manifested payloads, including the four certificate files and result JSON, remained byte-identical. Author controls supplement but do not substitute for the independent checker or algebraic proof.

Original uploaded programs, the accepted B4 archive and repair source remain inert evidence. Neither author nor review executables import or execute those originals. All six source-file pins were verified, and the accepted B4 archive/repair bytes were compared with the already accepted local artifacts. The source text SHA256 remains 9a723a072a427aa6c1633981ba0efaf711fd5cc0e5bda8c69da188fab2490daf. B4 review archive SHA256 remains 914a84d3bc40cc0c22781fa215ebed95f377861b06ce7784dd28fb6e1b19275d; its repaired API remains e34654cc71afa5b7b4a8de3850cde1cce682598bcb218105d829c8baf049e782.

## Scope and remaining work

The finite q2/B8 all-row experiment is accepted alongside B4. The broad AESGR program remains open, with historical corrections and external-theorem qualifications preserved.

A source-bound classical construction in the narrow grammar is neither a proof nor a disproof of the full AESGR conjecture. In particular, B4 depth 4 and B8 depth 10 are two finite instances, not a demonstrated uniform constant-depth family. No novelty search or priority adjudication was performed by this review.
