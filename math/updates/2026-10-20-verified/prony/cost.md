# Cost and scope ledger

This ledger accompanies the NEW candidate PROOF.md. It separates three mathematical objects; none is a free-input root oracle.

## Original P_h, canonical q, accepted 16-not-dividing-N squarefree range

- Algebraic representation: h=N/2 distinct nonzero legal nodes, all h weights nonzero, all N moments, original T^N=-I generator and original normalized Fourier target.
- Raw conditioning: new lower bound > (4/pi)^((h-1)/2)/sqrt(h). Applies to all h>=2 with infinity if the root multiset repeats. This is a coordinate statement, not a bit/algorithmic lower bound.
- Uniform upper envelopes: R=2^(N+1); separation and forbidden-node logarithmic margins O(N^4); inverse-Vandermonde, weight and residue logarithmic upper bounds O(N^5). Proof uses actual all-embedding coefficient bounds and nonzero algebraic-integer norms, not a floating-point experiment.
- Root acquisition: explicit exhaustive rational Rouché-disk algorithm; coefficients and q acquired at paid precision. No root engine is assumed implemented. Cold preparation 2^[O(p+N^5)] bit operations, including failed grid tests; deliberately weak, not optimal.
- Weights: actual pivoted rational system, O(N^3) rational operations; moment coordinates explicitly rounded first. Conservative bit solve O(N^7(p+N^5)^2), included within cold preparation. No unproved floating-point solve.
- Precision: sufficient p+O(N^5) prepared-coordinate bits from explicit UPPER perturbation envelopes. The exponential LOWER condition bound is not used to assert a necessary precision or runtime.
- Storage: O(N(p+N^5)) bits for rounded root/weight/residue/endpoint constants; polynomial streamed root-certificate and setup workspace. Online O(N+m) scalar registers have growing rational operand sizes, with safe O(N^3(p+b+N^5)) bits, not O(N) fixed-word memory.
- Complete online transform: h independent length-N signed recurrences, weighting and accumulation, both endpoint diagonals, normalization, input reading and full output writing. O(N^2) rational operations; conservative O(N^6(p+b+N^5)^2) bit operations for relative error <2^-p on nonzero b-bit dyadic input. Setup is additional.
- Implementation state: mathematical contract plus finite exact interface controls; no executed full grid, production program, speed benchmark, or polynomial-time original-P_h root preparer.

## Older explicit all-even large-t pencil, NOT the same node family

B_N(z)=zP_h(z)+2^(10N^3+2)P_(h-1)(z), m=h+1.

- All even N>=4: inherited legal distinct nonzero h+1 nodes and at most h+1 nonzero resolvents; Hankel rank ensures at least h nonzero residues. Zero residues need not be decided.
- Unscaled condition lower bound exp(Omega(N^4)); accepted review gives the stronger explicit >=2^(2N^4). This differs from the new original-family exponential-in-N lower bound.
- Oct11's exhaustive root route had 2^[O(p+N^7)] bit preparation. It is historical, not the latest known preparation result.
- The retained Oct19 independent preparation review accepts a deterministic mathematical polynomial-bit preparer for this EXACT large-t family, using an MSW/Pan root engine with paid coefficient acquisition: fully charged Õ((N^8+Np)^3). The smaller Õ(N^9+Np) is root-engine cost only, not total preparation.
- Accepted scalar precision p+O(N^7), polynomial storage, all weights/residues/endpoints charged, O(N^2) full-bank rational application and conservative O(N^6(p+b+N^7)^2) bit application. This mathematical algorithm was accepted, but a complete implemented MSW/Pan preparer and practical performance were not.
- The recovered historical review is evidence for that existing scope. This new packet does not rerun its whole proof, claim its engine is implemented, or transfer its polynomial preparation theorem to P_h without a separate source-bound derivation.

## General finite-choice pencil B_t and broader owner scope

The accepted t in {1,...,2N} existence argument proves h<=Q_min<=h+1 for every even N; the cardinality argument itself is not a favorable root-preparation or condition bound. Universal t=1 remains open. Original Q_min=h is accepted for 16 not dividing N, with the unrepaired all-even squarefreeness step still open.

ALG-EVEN-PRONY-EXTRA-POLE is the owner; NF-03/Q20/Q08 are linked workflow views, not extra discoveries or automatic closures. The historical NF-03 demand includes an actual legal family, separation, conditioning, and charged preparation. This packet completes only a bounded original-coordinate result and an explicit expensive contract on the previously accepted squarefree range. It does not close useful stability under scaling/preconditioning, practical execution, all-even optimality, general growing-degree stability, or any faster-FFT parent. No live table status or counts changed.

Comparison guard: a lower bound exp(Omega(N)) for P_h versus a lower bound exp(Omega(N^4)) for the large-t family does not by itself prove the former is better conditioned. The new original-family upper envelope is only exp(O(N^5)), so no improvement comparison is inferred from these two lower bounds.
