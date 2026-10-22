# ALG031 public package audit

Verdict: ACCEPTED PUBLIC PACKAGE ONLY. The audited public archive is the exact frozen 45,806-byte package identified in VERDICT.json. Its 16 members are ordinary non-executable UTF-8 text or JSON files, with no duplicate, symlink, absolute-path, parent-path, encrypted, or executable entry. The 14 payload members match the public manifest; the two manifest files are the explicitly excluded self-reference pair. The archive can be reconstructed byte-for-byte from its frozen directory using its fixed metadata and DEFLATE level 6.

## Accepted preservation

The current proof, three complete mathematical source bodies, historical v1 report, and historical wording-only HOLD are byte-identical to their frozen origins. All author and reviewer origin-manifest member hashes were independently checked as opaque bytes; no supplied program was executed. The only author v1-to-v2 changes are the exact documented attribution sentence and the two manifest files. The proof's frozen candidate and pending-review wording is explicitly explained as chronology in the public README. Historical HOLD and v1 text are not presented as current status.

The independent derivation reconstructs exactly after two documented administrative substitutions at original byte offsets 427 and 841. The acceptance record reconstructs exactly after its sole candidate-root substitution at offset 130. The original lengths, fragment SHA256 values, output hashes, and every byte outside those substitutions pass. No mathematical or acceptance prose changed. The public source-binding rows equal the exact six-field public projection of the originals. No omitted private locator is reproduced in this detached audit.

## Scope and cost

The public summary, scope record, proof, and accepted review consistently restrict the result to odd-prime M, 1 <= K <= M, N=KM, a fixed input independent of the seeds, one shared nonzero a, fresh independent uniform pairs (b,d) over every residue including d=0, independent pairs across repeats, and positive odd R. For nonzero input the diffuseness hypothesis is p_star=2 M Lambda_star^2 rho/epsilon^2 < 1/4. The all-bin probability bound remains N(4p_star)^(R/2); Lambda=1 and the M-bin union apply only to aliases. Zero input is handled separately and exactly.

The retained model is exact complex-root arithmetic with ordered-real median comparisons charged separately. All R sketches, decoders, repeat-dependent convolutions, table preparation, and outputs remain charged at O(RN log(2K)) exact scalar work, plus O(RN) median-selection comparisons. Sorting's O(NR log R) alternative, 2R independent residue draws, and both stated storage alternatives are retained. Sharing a is table reuse, not an unproved reduction in R-fold convolution work.

No sub-FFT claim is introduced. Stability, finite-bit complexity, exact comparison representation, stronger general or all-bin concentration, arbitrary-input guarantees, dyadic/composite extensions, other shared-seed schemes, genuinely faster joint decoding, production performance, novelty, and whole-ALG-031 closure remain outside acceptance.

## Sanitization and controls

Exact allowlisting excludes scripts, private provenance records, scope captures, diagnostic results, and runtime logs. The included historical proof and source references to omitted controls are retained provenance prose, not bundled executable artifacts. A scan of all members found none of the omitted original private locator fragments or standard local absolute-path markers. This is a bounded, source-aware sanitization check, not a universal proof that arbitrary prose cannot contain private information.

Twenty-one negative controls all failed the expected independent gate. They cover extra and missing members, duplicate and unsafe paths, symlink and executable metadata, manifest-sidecar corruption, changed proof/source/history/review bytes, projection-offset and acceptance-root tampering, a private locator marker, removed seed or diffuseness guards, dropped R costs or comparisons, false owner closure, and an alias bound promoted to all bins. Mutations were in memory only. Where indicated, hashes were refrozen in memory so rejection came from the anchored invariant rather than a trivial stale-manifest mismatch. These are package-gate tests, not new mathematical finite controls.

The original archive and all 16 directory members were rechecked unchanged after the controls. This detached audit contains only inert evidence and does not modify the audited package. No external writes or uploads occurred. It preserves the earlier bounded mathematical acceptance but does not issue a new broad theorem acceptance or rerun historical controls.
