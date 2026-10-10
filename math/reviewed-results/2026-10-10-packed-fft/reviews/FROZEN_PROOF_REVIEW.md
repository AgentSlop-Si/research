# Hash-pinned review of the completed packed dyadic theorem

Date: 10 October 2026.

## Reviewed artifact and disposition

Reviewed final file: `packed_fft_candidate_1355/executor_derivation/DYADIC_PACKED_THEOREM.md`

SHA-256: `bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`

Disposition: no unresolved mathematical objection remains to this exact artifact's main dyadic theorem. For N=2^v, v>=1, and supplied 2<=t<=v+1, the stated deterministic finite-dyadic word-RAM algorithm has cold work O_c(N(t+log2(v+1))), O_c(N) words, explicit dyadic output, and all-input relative-l2 error at most 2^-t. The RAM has sufficiently wide Theta_c(v+1)-bit words and integer multiplication/division. This is a paper-level acceptance, not validation of a production executor, a practical crossover, an exact-complex FFT result, or historical priority.

## Independence and review process

The independent derivation and controls were completed before reading the construction worker's full proof. They are recorded in `INDEPENDENT_AUDIT.md`, SHA-256 `56b73f7fc5379ace895532a8259279d5062e6537b6df9d9adeb325ea756a2e06`.

The full initial construction SHA-256 `88ab5998a68143f1b6d79e991bd6c923bab19279428413aaa41f711edb4ab91f` was then read and audited. Every changed line from that complete version to the intermediate reviewed version `de77b9721637b1367d5086fce98af3648665640b0ed01ee2ab632b3da5388d5c` was read. The subsequent single-sentence pre-abort offset clarification was then diff-checked, its bound verified, and the new final hash above was re-read. The initial version is preserved by the constructor as `DYADIC_PACKED_THEOREM_v1_REVIEWED.md`. This review applies to the final hash above, not to unseen subsequent revisions.

The initial proof had two scope/wording issues: exact transcendental truncation conflicted with its polynomial interval-selection argument; and its separate arbitrary-t cost did not charge the larger number of leading-bit chunks. The final artifact repairs the former with midpoint-to-grid approximation and removes the latter proposition. Neither affected the fixed-word main theorem.

## Specific final checks

1. The constructor's p=t+10+ceil(log2(v+1)) suffices: its final 14u(v+1) bound is at most 14 epsilon/1024. The complex grid error constant (2pi+sqrt(2))/1024 is less than 1/128, and the butterfly spectral error allowance u/32 is conservative.
2. The sharper complete Q-1 catalogue and its O(1) ID formula are exact. For r>g, the remainder (Pc+l)/(P 2^(r-g)) belongs to [0,1), so all lanes equal h; row (g,h) is the same constant vector.
3. The normalized DIT layout, small/large-span boundary, word pairing, total key decoder, clipping response definition, payload ordering, natural output order and explicit input/output costs are all accounted for.
4. The first-overflow argument is noncircular: only preceding nonclipping stages are used to bound the next prequantized norm; this norm is strictly below the threshold 32N.
5. The literal preparation budget counts actual RAM operations within multiword exact-rational routines, and all preparation scratch allocations are checked before use. No high-level arbitrary-precision operation counts as one instruction. Abort does not expose partial tables, and storage reclamation costs at most O(N). Candidate offsets already have O(v) bits; live memory addresses are budgeted.
6. Throughout b<=v/64, p<=v/128 and unbudgeted preparation is bounded uniformly by C 2^(17v/128) poly(v)=o(N). Hence failed low-b builds occur only below one absolute finite v threshold. High-b scalar fallback work O(Nv) is O(Nb). This proves uniformity without an unspecified run-time polynomial cap or a computable crossover threshold.
7. The scalar fallback's K=p+v+20-bit full-circle recurrence costs O(N), gives coefficient error below u/131072, and uses O(v+p)=O(v) bits per exact product. Certified seed/root work and scratch are polynomial(v), hence O(N) with a fixed uniform constant in the stated finite-precision domain. Scalar quantization uses only O_c(1) v/8-bit helper chunks in that domain.
8. Appendix A's explicit coefficient routine is sufficient. L-term Machin series give the claimed exponentially narrow pi enclosure. For m=64L, the bound 7^m/m! <= (98/m)^(m/2) makes the Taylor remainder far smaller than required. Exact term representations have O(L^3) bits and unreduced summation O(L^4) bits, so elementary integer algorithms are polynomially charged. Interval midpoint rounding avoids transcendental tie decisions. The square-root enclosure uses the stated integer-square-root formula correctly.
9. Outputs retain the common lattice 2^(-v-2p) Z[i] before exact input-scale restoration, with O_c(v+p) numerator bits. This supplies an arithmetic interface beyond normwise correctness, but this review does not itself prove an all-length interpolation compiler.

## Fresh control evidence and limits

The independently authored controls passed 130,216 exact phase-vector checks, 524,288 complete eager P=2 response checks, 210 packed/scalar stagewise executions, and all 65,536 keys of a separate invalid/overflow alphabet including 768 clipping responses. Additional bit-reversal and numerical stress controls passed. Details and exact counts are in `control_results.json`.

The constructor's reported symbolic and toy controls are clearly separated from its theorem and are not presented as a production transcendental executor. This reviewer did not rerun the constructor's script; the numerical evidence here is the independent script, not an inherited execution claim. No predecessor/uploaded research code was executed or imported.

The new Appendix B explicitly disclaims novelty of packed FFT arrays. The external primary-source/model comparison is another worker's task and is not independently re-certified by this mathematical review. No historical novelty conclusion is needed for the accepted bound.
