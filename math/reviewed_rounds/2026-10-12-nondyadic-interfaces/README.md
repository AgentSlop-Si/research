# Reviewed bounded non-dyadic interfaces

12 October 2026 UTC.

## Ternary raw q-Weyl interface

[Independent Q07 review](q07-ternary-raw-weyl.md).

The accepted exact reference interface adds N=3,9,27,81,243,729 over a supplied and verified prime field, with N<p<=65537, a verified primitive N-th root, 1<=t<=floor(N/2) and at most 16 fresh vectors. It checks all raw coordinates, returns the complete positive-sign unnormalized DFT, and applies the same-sign two-Fourier-factor operator. The previously accepted dyadic baseline remains valid.

The review independently checks 2,559 raw/cap cases, 53,673 DFT coordinates and 56,082 action coordinates. The author replay is separate and byte-identical. Recognition, root enumeration, scatter, cold preparation and failed-recognition fallback are charged. Each fresh action costs O(N(s+1)); the sparse ternary transform bound does not make that action O(N log s). These are semantic field/event counters, with physical runtime and arbitrary-bit costs outside the acceptance.

## N15 nondivisor direct-bin interface

[Independent Q14 review](q14-n15-nondivisor-interface.md).

The accepted N=15, Q=3, M=5 interface uses Q(zeta_15), represented by eight Fraction coefficients modulo Phi_15. This is distinct from Q07's prime field. It supports B=1..5, including nondivisors 2,3,4, full raw reads, exact support certification, guarded Green reduction and complete 15-coordinate output. A preliminary kernel-sign defect was corrected before sealing; the accepted source and its replays are unchanged.

Direct character-projector recovery is dense: O(BM²+M²) per attempted fiber. Fallback is the separately charged O(N²) direct DFT of the saved original input. Malformed candidates and internal/resource faults propagate. The independent review checks 207 API cases, 2,790 DFT coordinates, all 100 hash settings and 1,500 projector-character tests, with observed cost, Green, fallback and mutation controls. Exact zero leakage or random bits in this field model does not imply numerical stability or a fast HIKP constructor.

## Remaining scope

Both are bounded implementation increments. Unrestricted fields and lengths, extension fields or other representations, common-chirp/caller integration, fast arbitrary-length windowed binning, a sharper paid uniform RIP constructor, finite-word/bit/numerical production, stability and historical priority retain their separate open obligations. No generic FFT speedup, new theorem count or novelty clearance is asserted. Q09 work is outside this dated report collection.

Earlier: [b=19 overlap completion](../2026-10-12-b19-ramified-completion/README.md). Existing scientific reports, repository visibility and licensing remain unchanged.
