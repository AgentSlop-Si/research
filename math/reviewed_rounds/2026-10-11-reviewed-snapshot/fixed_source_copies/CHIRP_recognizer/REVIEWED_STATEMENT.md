# Reviewed bounded CHIRP implementation contract

11 October 2026. Independent verdict: PASS FOR THE BOUNDED DENSE REFERENCE. No source repair required.

This statement applies to chirp_exact.py SHA256 7d263f616526bd1123658771afc73bb44fc15282ef8ee0131e48ade0b59d18b7 and check_certificate.py SHA256 556337c6bc1f4215d1782f82fb63bfd67771152a442af1688bf91080f763699f in Library libfile_bf879c07b8208191a33e55429d9675ca v1, archive SHA256 f0f6ab4c1601a2875d48aa61c48fd347154357b95f21cf41e0de351d0a61c9db. Candidate source bytes remain unchanged.

For an exact built-in record with exactly N,p,r,omega,x, require integer headers (not booleans), N>=2, 1<=r<N, supplied prime p, N|(p-1), canonical supplied omega of exact order N, and exactly N canonical raw residues in an exact built-in list or tuple. The implementation verifies primality and exact order; it does not discover the field/root. N=1, r>=N, and the order-2N-root curvature extension are outside this API.

The target family is x[j]=omega^(a*j*j) sum_b gamma[b] omega^(b*j), with at most r distinct frequencies and nonzero listed amplitudes. Zero is represented by the empty list. Returned phases lie in 0<=a<N/gcd(2,N), with no uniqueness claim.

When computation finishes with MEMBER, the implementation returns one representation verified against every original raw coordinate and all N positive-sign unnormalized DFT entries. When it finishes with NONMEMBER, every canonical phase has been rejected and no transform is supplied. The cyclic eliminant is only a filter; exact Hankel recovery, distinct supplied-grid roots, unwrapped recurrence checks, weight recovery, and full raw synthesis establish the decision. Wrapped 2r>N instances are included.

INVALID_INPUT and INVALID_PARAMETERS describe detected malformed/domain/configuration conditions, not signal nonmembership. LIMIT is indeterminate, including during prime/root validation and after a possible representation is found but before dense output finishes. It provides neither representation nor transform. First-detected status controls, so LIMIT does not assert input validity.

Default caps are N<=128, r<=64, bitlen(p)<=32, and 2,000,000 metered units. Configurable caps cannot exceed N=512, r=128, 64 bits, and 20,000,000 units. Being within those dimension/width caps does not guarantee enough permitted work to finish. The JSON CLI caps the entire finite record at 1 MiB. The Python API assumes the object is already resident. Ordinary runtime/operating-system failures are not promised to become status results.

All validation, root preparation, attempted/rejected phases, recovery arithmetic, inversions and their exponentiation work, full synthesis, and dense accepted output are included in the implementation ledger's stated instrumentation. The ledger does not claim complete bit-cost RAM accounting, processor time, or a process-memory limit. Dense recognition uses O(L*(r^3+N*r)+N^2+N) field additions/multiplications before inversion internals, O(L*r) scalar inversions, O(L*r*B) additional implemented inversion multiplications, and O(N+r^2) live field entries plus O(L) phase records; L=N/gcd(2,N), B=bitlen(p). Trial division and ordinary integer/control work are separate. The accepted-output N^2 term is absent on NONMEMBER.

The separate checker independently verifies parameters and every mathematical decision. MEMBER certificates are checked by complete raw synthesis and dense DFT. NONMEMBER is checked by Fourier support at every canonical phase. Its VERIFIED statuses do not authenticate execution telemetry, individual rejection reasons, or runtime claims. The checker can independently return CHECKER_LIMIT.

Independent testing passed 643,632 differential decisions, including 640,921 exhaustive vectors against explicit family generation, 1,366 recognizer cutoffs, 802 checker cutoffs, and 27 corrupt certificates. A separate full-rank N=512/r=128 test passed and withheld all outputs when its final DFT write was denied one remaining work unit. The pinned author suite also replayed without failure.

This accepts a bounded dense reference only. It does not implement or validate the fast Toeplitz/blocked/dyadic kernels, the optimized dispatcher or Gauss-output routines, and supplies no production-readiness, measured-speedup, new bit-cost theorem, numerical robustness, historical-priority, or unrestricted FFT claim. Q13's reference implementation milestone advances; STR-Q2 optimized production validation stays open. No Sheet or GitHub mutation was performed.
