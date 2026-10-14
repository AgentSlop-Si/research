# Q29 exact mixed-characteristic precision contract

14 October 2026. Independent review **accepts the exact finite-ring and bounded precision contract, with the stated execution conditions**. The H1687/R843 higher-precision lift is **UNPERFORMED**. No new full ordinary-discriminant value, nonvanishing, all-center closure or terminal repeated-branch computation is accepted.

## Accepted design and controls

The exact ring is B_M=(Z/5^M Z)[a,T]/(a^18+a^9+1, Phi125(1+T)), representing local cyclotomic integers modulo pi^(100M). Integer carries and the complete ramified relation are essential. The independent review accepts the valuation formula, staggered precision quotients, guarded pi-division and the jet-tail transfer lemma.

A proposed M=2, reciprocal w<100 computation gives coefficient precision200 and raw U tail v<200. After separately certifying pi^60 content, guarded normalization would yield uniform F precision140. This bound describes information available from that design; it does not claim that any repeated branch resolves at140. Merely increasing coefficient precision with the old tail cutoff retains the old uniform ceiling40.

Small controls include author-code replay and an independent opposite-order dense reduction, 20 fixed-seed product comparisons, staggered precisions1 through200, selected guarded divisions, all three carry visibility boundaries, the full mod25 relation and a precision140 ambiguity witness. They support the bounded algebraic contract and do not test a large recurrence. The original source calls one power-basis paragraph “normal-basis arithmetic”; the independent review records that terminology correction without identifying a mathematical defect. The historical source wording is preserved.

## Budget and implementation gap

For one proposed shared-center R843 computation with w<100, the review bounds the straightforward recurrence by at most158,600 coefficient-ring products. A fully dense 1,800-coordinate schoolbook product gives a baseline of at most513,864,000,000 scalar product-accumulations, before reduction, setup, checking and output. This is an algorithm-specific upper budget, not a lower bound on efficient implementations and not observed runtime.

Packed uint8 coefficient payloads require180,000 bytes per retained R slice,540,000 bytes for three rolling slices and360,000 bytes for the raw U jet; actual accumulators, metadata, containers and optional caches add storage. Packed size does not establish Python-dictionary practicality. No seconds estimate is justified by the small controls.

A sparse structured production alternative is under development and is not included or independently accepted here. Before a larger result can be claimed, the integral mod25 recurrence must be recomputed with source-bound root/basis/sign/center conventions, production kernels tested, old available mod5 coordinates compared, pi^60 content certified and precision carried through every division and branch. The next shared-center jet itself would still not cover all centers or establish the full discriminant.

## Preservation

The combined ZIP preserves the contract and independent review in distinct directories, retaining every original file and all unique scientific sources. It is explicitly a publication-safe projection. The mathematical calculations, assertions and numerical control values are unchanged; three code files change only source-directory strings. Original and publication hashes disclose all eight changed files; nine files remain byte-exact. An exact original local snapshot is also sealed and remains private.

The full provenance replay needs original predecessor input bytes that are not bundled here, so this is not a self-contained historical replay archive. The [earlier bounded Q29 publication](../2026-10-14-q29-bounded-normalization-0119/README.md) separately preserves that evidence with its own documented projection. The independent small audit uses the bundled Ring source. No scientific code or projected checker was run during packaging.
