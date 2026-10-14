# PR622 owner-map and admission review

Date: 14 October 2026. Stable ID: `PR622-REPACKING-CANDIDATE-20261013`.

## Verdict

**The literal owner map passes the supplied-window placement problem. The full unchanged-provider admission gate remains OPEN.** No mathematical counterexample to the candidate has been established. Missing evidence and stale frozen bindings are not a rejection of the construction.

The existing independently accepted profile ordering, PR623 > candidate > PR624, is retained. It was not rerun or reopened. Nothing here establishes an all-size FFT, a bit-cost bound, practical speedup, or novelty.

The current question is the conjunction “legal owner map and full admission contract, or a precise failure.” Its full scope cannot be closed from this packet. The supplied-window subcomponent is now independently checked; the physical schedule/routing and full-admission components remain open.

## Exact source and identity

The candidate archive is retained byte-for-byte as `evidence/source.zip`, SHA-256:

`afb3280fda31e1a26e72d4dabf7870b9433ceef366114e66151be5e85ef4a05a`.

All 22 members were read as inert bytes; the internal manifest covers the other 21 members and every digest matches. No source script was executed, imported, or loaded dynamically. The retained pickle was not deserialized.

The primary upstream package is `research/complex-571-cold14-k492` at commit `f69477f4f6d3c7eb1f740b166881bffed4ffa9f6` of `jeremykothe2/integer-mult-bounds`. Five relevant upstream files were fetched as inert text. Their Git blob IDs were independently recomputed from the fetched bytes; exact URLs, SHA-256 and Git blob identities are in `output/UPSTREAM_SOURCE_PINS.json`.

The verified table snapshot binds this work to Research overview row 305, stable ID in B305, status E305 = TO RESEARCH; its source view is Incoming queue row 44, stable ID in A44. No table, repository, or other external state was changed.

## What was independently established

`check_literal_map.py` is a new, standard-library-only checker. It does not use the archive verifier or optimizer. It reads JSON and gzip data and exhausts all roles and all capacity cells. Normal and Python `-O` runs have byte-identical outputs. Fourteen deliberately invalid inputs are rejected in both modes.

- The 72 calls cover all 9 stages and 8 replicas exactly once. Each replica's stages retain their chronological order.
- The dispatch is ck × 7 and jp8 × 65. Each call has all 492 expected helper identities and widths, giving 35,424 roles.
- All role fields have integer types and valid ranges. Every role belongs to its supplied idle-time window.
- Each family equals `896*r + 112*(2*pairs[c] + sides[c]) + port`, with copy `112*r + port`, and lies in the 7,168-family live stock.
- Every complete call uses 492 distinct helper families. This does **not** establish distinctness from the additional 224 active data owners, whose actual list is absent.
- Each owner group's literal cells are disjoint, within capacity, and exactly a packed prefix. Every unused suffix is charged once. No capacity or packed-cell assertion is based on floating-point arithmetic.
- The provider registry, all widths, program hashes, supplied windows, family geometry, and call order are unchanged from the pinned baseline data. The registry's local profile and program hashes are still premises; their underlying programs are not present in this archive.

Candidate recomputed values:

- 1,377 changed serialized records, including 752 relocated roles
- 16,356 entering-helper roles and 26,483 cross-replica helper roles
- 2,359 idle remainder children, with profile `{1:128, 3:15, 7:1, 16:2, 48:2213}`
- Full paid profile `{1:181580, 2:29864, 3:31263, 4:11520, 5:5040, 6:576, 7:1, 8:576, 16:2, 48:2213}`
- Rank mass 520,704 and deficit `73*7168 - 520704 = 2560`

The profile difference from the baseline is exactly `e1 - 4e3 + 2e16 - e21`. These arithmetic checks certify the literal accounting conditional on the supplied provider profiles. They do not substitute for a fresh complete coefficient/phase invoice.

### Finite proof structure

The checker constructs the complete finite expected domain `(time, helper)`, then demands an injective record map of the same cardinality. This proves role coverage. For every `(owner replica, child, port)`, it explicitly assigns every integer cell in every role's half-open width interval and rejects repeated occupancy. Equality of the resulting occupied set with `{0,...,used-1}` proves disjoint packed-prefix coverage. Capacity bounds and the explicitly charged remaining suffix establish the advertised abstract packing. Per-call family sets prove helper-to-helper non-aliasing. The result uses the supplied windows, not windows independently derived from the true event schedule.

## The actual legal owner/routing model

The upstream controller requires more than the abstract packing. Its exact checker is the pinned [`code/audit_allcold.py`](https://github.com/jeremykothe2/integer-mult-bounds/blob/f69477f4f6d3c7eb1f740b166881bffed4ffa9f6/research/complex-571-cold14-k492/code/audit_allcold.py).

1. A complete invocation is indivisible. Its helper family must be idle between its actual previous physical touch and its upcoming idle sweep. Every bridge counts as a physical touch. Windows are rederived from the complete serialized schedule; an input window table alone is insufficient.
2. Every invocation has 716 mutually distinct live owners: 224 active data owners plus 492 helpers. Helpers cannot alias active data or enter the private namespace.
3. The actual residual axes come from the relevant port/child entry of `DATA-PHASES.json`. For width w, a helper consumes the exact pending slice at the declared offset, borrows 9-w complementary spectator axes, and extends these to a 73-column orthogonal chart.
4. For width 9 the route is `[3, child, offset]`. For smaller width it is `[4, child, offset, width, spectators]`. The chart must agree with those actual axes, not just with a dimension count.
5. The serialized local providers, wrappers and phase recipes must bind to the recomputed canonical programs and complete arbitrary-dirt replay receipts. Owner changes must preserve each complete call's wrapper boundaries.
6. Idle remainders act on the actual leftover inherited axes before the owning replica next touches that family. Source-event projection, dispatcher identity and the complete paid profile are independently audited.

The elementary routing extension is conditional: distinct pending axes from a 73-axis orthogonal basis can always be extended by 9-w unused spectator axes and then the remaining basis axes. The resulting chart is a basis permutation. This does not identify the candidate's actual pending axes or certify its schedule. The archive's generic orthobasis check cannot bridge that missing input.

## Precise blockers

The candidate archive lacks the actual parent `split-centres/GLOBAL-TEMPLATE.json.gz`, `work/complex-nine-native/DATA-PHASES.json`, and both providers' complete seven-artifact bundles. The required provider filenames and their already-declared hashes are enumerated in `output/MISSING_PROVIDER_ARTIFACTS.json`.

It also lacks a source-bound regenerated candidate witness/SPEC/EXPECTED set, the candidate serialized hosted controller and actual sigma map, independent controller controls, a fresh finite invoice, the conservative/native exact outer assembly, and the required assembly/recompression/phase-portability controls. Pinned upstream `verify.py`, lines 321–377, identifies these stages and receipt requirements. The five inert upstream source reads clarify the contract but do not supply those generated inputs or receipts.

A separate local archive search scanned 1,253 recovered ZIPs without errors and found no parent template, data phases, sigma map, or provider ck/jp8 artifacts under their required names. Its receipt is retained. This is a bounded local evidence search, not a claim that the sources cannot be recovered from upstream or reconstructed later.

There is also a demonstrable frozen-input mismatch:

- Upstream SPEC expects owner SHA-256 `2453696ff8c79da009bfdf148747562eafc21f1e164fbee2920cf1b347805bc8`; the candidate is `b52e0975d5605c58f8d3d4a32814d2f8a7324f1d331adebad57bf78405d2ee42`.
- Upstream SPEC expects plan SHA-256 `442d71a0a41e42503c645892f9fddd5b4d8fa722659974cedc27ae41b60319ac`; the candidate is `57fae3e2124b805c6f24e3c1b2dae2eb5189e98663552f85d6dbdc87c2a8a221`.
- The frozen SPEC also describes 26,466 cross-replica roles and 2,361 idle remainders, versus the candidate's recomputed 26,483 and 2,359.

`bind_providers_portable.py` line 21 pins the plan; `emit_allcold.py` lines 26–27 pin owners and runtime source plan. Direct substitution into the unchanged frozen admission inputs therefore fails before it can establish the new candidate. Regenerating the source-bound witness and expectations is the declared route forward. Simply weakening or deleting these guards would not finish the gate. This mismatch is not a semantic counterexample to the owner assignment.

## Next decisive work and stopping condition

Recover the exact pinned dependency packages and generated baseline data, then regenerate a candidate-bound witness while retaining the original checks. Independently rederive touch windows, check all 716 owners per call, serialize and check every actual residual/spectator route, and obtain fresh complete invoice and assembly receipts. Full admission can close only when these pass for the candidate, or a concrete semantic counterexample is exhibited. All-size compilation and analytic transfer remain separate even after such finite admission.

## Reproduction

From this directory, run only the newly written checker:

`python check_literal_map.py`

`python -O check_literal_map.py`

The source programs under `evidence/` are deliberately inert. This review ran neither the upstream construction/controller pipeline nor the archive's verifier/search scripts. All research inputs and previously accepted results are preserved.
