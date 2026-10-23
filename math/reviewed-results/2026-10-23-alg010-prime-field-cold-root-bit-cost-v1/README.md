# ALG010 prime field cold root and bit cost child

23 October 2026. Accepted only for the represented-prime-field cold-root and bit-cost child, under the mandatory qualifications below. ALG-010 remains TO RESEARCH at priority 42. This is not an arbitrary-input FFT acceleration, practical-speed result, new Fourier mechanism, historical-novelty claim, or whole-owner closure.

## Accepted result and root contract

For a supplied prime p, b=bit_length(p), dyadic N>=4 dividing p-1, all N canonical input residues, and the exact supplied primitive Nth root q, recognize exactly the original degree-one finite-boundary family and, on acceptance, return all N positive-sign q-Fourier values. The supplied-root bit-charged random-access bound is T_prime(p)+O(N b^2+b^3), with at most six Fermat inversions and O(Nb) represented evaluator storage. All input validation, root validation, failed family recognition, endpoint forcing, singular recovery, and complete output encoding are charged.

The actual reference validates primality by deterministic trial division. Its T_prime(p)=O((1+sqrt(p))b^2) charge may dominate exponentially in b. A faster primality certificate or free prime context is not supplied.

A separate caller-authorized any-root interface returns the exact acquired q, which defines both the tested family and output ordering. DECLINE is relative to that q only, not a denial of membership in the union over all primitive roots. At p=17, N=8, x=(1,14,12,1,3,0,0,0) is accepted at q=2 but declined at q=8. An acquired root cannot replace a prescribed unavailable root, and no free discrete logarithm or permutation oracle is assumed.

## Mandatory diagnostic and cap qualifications

The frozen API always increments diagnostic counters. There is no implemented disable switch. The historical candidate report's contrary wording describes a possible implementation modification, not a feature of this source. Read the independent review as the controlling qualification; do not treat the unchanged candidate wording as a current implementation claim.

For t nonzero candidates and d raw draws, acquisition has counter-free tariff O(t b^3+d b), plus the actual random-bit provider's setup/work cost. Add O((t b+d)log(t b+d+2)) conservative diagnostic work and O(log(t b+d+2)) extra counter bits. The normal evaluator cost covers ordinary post-root counters; very large acquisition counters require the stated extra tariff. Requested serialization is paid separately.

Independent unbiased supplied bits give zero-error almost-sure root acquisition with expected O(b^3) arithmetic work and at most 4b expected bits, plus the provider tariff. These are expectations, not deterministic caps. Uncapped acquisition has no finite deterministic worst-case bound.

A T-candidate cap alone has failure 2^(-T) but leaves raw rejection draws unbounded. A D-raw-draw cap has failure (1-r)^D<=(3/4)^D, where r=(p-1)/2^(b+1), and at most Db supplied bits. Its O(Db^3) arithmetic tariff is not a complete diagnostic arbitrary-cap bound: add O((Db+D)log(Db+D+2)) counter work, provider costs and cap/input encoding. With both caps the valid upper bound is 2^(-T)+(3/4)^D, not either separate exact equality. Zero caps are allowed. ROOT_LIMIT means only the allowed search budget was exhausted, never root infeasibility or family rejection.

## Complete output and scientific boundary

The caller-known-p,N wire format has a one-byte status and residues of ceil(b/8) bytes. ACCEPT includes q and every output: 1+(N+1)ceil(b/8) bytes. DECLINE includes q: 1+ceil(b/8) bytes. ROOT_LIMIT is one byte. The explicit encode_result callable must be invoked; evaluate does not itself return the serialized result. Malformed inputs raise exceptions rather than mathematical DECLINE. Foreign or unbounded encodings require their own paid conversion and are not silently covered.

No generic-input fallback is implemented or certified. The selected cyclic-hypergeometric comparison is preserved, not reopened. Other represented fields, unavailable prescribed-root acquisition, numerical recognition/stability, complete-interface historical priority and caller/fallback integration remain open.

## Files and evidence

- PROOF.md is the byte-exact candidate REPORT.md. It must be read with the mandatory qualifications above and the independent review.
- INDEPENDENT_REVIEW.md preserves the full scientific review, with only one explicitly recorded private worksheet URL replacement.
- evidence.zip contains the 23 retained scientific/provenance originals or documented projections, historical manifests and SHA256SUMS, all three unchanged scientific programs, stored controls, exact original-source README copies, and selected inherited comparison bodies.
- PUBLIC_MANIFEST.json binds the public archive, each member, source correspondences, historical inventory entries, exclusions and direct files. Original manifests are historical original-byte inventories, not current public-file manifests.
- SOURCE_CLOSURE.md states provenance, exclusions and reading limits. REPRODUCE.md states integrity verification and the non-turnkey scientific replay boundary.

The local packaging pass executed no scientific program, altered no frozen source, and made no Git, native-table, publication or other external write. Stored control results are historical evidence, not a new run. Run python -B verify_package.py for data-only integrity checks; it does not execute archived programs or prove the mathematics anew.
