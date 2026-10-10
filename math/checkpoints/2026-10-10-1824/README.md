# Reviewed Fourier research preservation supplement

10 October 2026

Repository export of the frozen 18:24 reviewed supplement, including its separately dated 18:25 Sheet checkpoint. This export omits only private delivery/account identifiers and machine-local path prefixes. Two metadata-only source objects have new content hashes. The two JSON sources above the connector request limit reuse their existing byte-verified gzip counterparts; the preservation utility restores both JSON files exactly. All 81 logical source names remain, and all mathematical source files and research programs restore byte-identically. There are 75 stored content objects, compared with 77 in the original ZIP. [The export ledger](REPOSITORY_EXPORT.json) records storage encoding, original ZIP hash, raw provenance and exported-file hashes. Historical preservation/publication receipts describe their original snapshot, before this repository commit. The utility restores the sanitized repository-export versions of the two metadata files.

This is a new, additive preservation supplement for the corrected axis criterion, the guarded fixed-topology Fourier reduction, and the bounded prior-art audit. The two new mathematical review receipts accept the corrected statements within their stated scope. They establish no stronger uniform Fourier bank bound and no new FFT arithmetic-complexity breakthrough. Historical novelty remains unresolved.

The previously delivered 206-member checkpoint is unchanged. Its filename, size, and SHA-256 are recorded in [the prior checkpoint reference](PRIOR_CHECKPOINT_REFERENCE.json). This supplement is not a replacement for that archive.

Scope cutoff: the four author packets from research cycles 1805, 1807, 1810, and 1815; the two frozen independent reviews from cycle 1819; the recorded rejected axis shortcut; and, when verified, the five-cell Sheet checkpoint from 1825. Later circuit reductions, group-theoretic extensions, and candidate stronger bank theorems belong to a later checkpoint and are outside this supplement. Its 12-variable circuit count and unchanged accepted bank bound describe this frozen scope.

## Corrected axis criterion

Let g be monic of degree 1 ≤ m ≤ N−1 over a field, with c=g(0)≠0. Write d=N−m, H=t^m g(1/t), and S_N=1+t+⋯+t^(N−1). For the quotient-coordinate axis matrix X_N(g), assume gcd(g,H)=1 and 2m>N−1. Then the row corank is at most one. Define the unique remainder

    R = (c S_N H^(-1)) mod g,  deg R < m.

The exact failure criterion is

    rank X_N(g) = N−1  if and only if  R(0)=0 and deg R≤d−1.

Otherwise the row rank is N. This quotient-algebra statement does not require squarefreeness; the interpretation using distinct physical root nodes does. The dependence-space proof also works in characteristic two. The equivalent constrained reciprocal Bézout equation has the corrected sign C=−B.

Reciprocal coprimality alone does not imply full rank. At N=5, g=t³+t²+t+2 is squarefree and reciprocal-coprime, but A=(t−1)g=t⁴+t−2 gives an axis dependence, and the axis rank is 4. The documented automatic-full-rank shortcut and its dependent proposed 7N/4 bank bound are rejected. The accepted 9N/5+O(1) bank theorem remains unchanged.

A separate conditional theorem says that rank A_(N,m)=4d−11 in the specified Fourier recurrence system forces g(1)=0 for every kernel polynomial. Adding or removing a simple root 1 preserves the axis dependence space; it does not remove the remaining corank-one obstruction. Finite modular kernel gcd data alone do not determine the full characteristic-zero kernel gcd.

The author controls contain 112 deterministic trial records across 16 parameter pairs. They represent 82 distinct coefficient polynomials when counted separately within parameter pairs. All 112 records were independently checked; the criterion applies to 111 records and agrees with direct rank in all 111. One zero-constant sample lies outside its hypotheses. The 16 baseline lifting recipes and nine refined-rank-saturated pairs are finite results. The independent review additionally checks 694 applicable cases over characteristics 2, 3, and 5, including 46 nonsquarefree cases, and an additional nonsquarefree characteristic-three failure example. No asymptotic nonvanishing theorem is inferred from these controls.

Sources: [author proof](objects/sha256/da/daa14fcb57d3702661abde4d1d50f35342f3519d655794188c6724b59649b0d7.md), [independent review](objects/sha256/ab/abedfe3514a20cf76e3d74aa6e6866f620e718d382197301132ca9f7bee362e1.md), [frozen review receipt](objects/sha256/cd/cd3cdab3e680f3e8d30c77aff0c7755ca3235fd01f96a1697df1192753401852.json), and [documented rejected route](objects/sha256/2c/2cf57ca330e182d7941ea8f3fc7d7d035e12f51a4f63a0773d7f74455778e710.md).

## Guarded rational circuit reduction

The independent review accepts equivalence to the earlier guarded necessary system over Q(ζ₁₁). The strongest preserved form has 12 free variables and 55 stored residual rational circuits. These counts do not assert algebraic independence or a fully expanded 12-variable polynomial system.

The free coordinate indices are 0, 11, 22, 25, 34, 41, 49, 52, 65, 83, 88, and 92. The expanded step removes x91 by a field-unit pivot and leaves 15 variables, 58 equations, 124,465 terms, and at most 25,534 terms in one equation. It includes 34 exact mandatory-monomial cancellations and three guard normalizations. The compact triangular reconstruction then removes x39, x44, and x55, using denominator identities proved nonzero on the retained guarded domain.

All fourteen nonvanishing conditions remain mandatory:

- The eight inherited coordinate exclusions x39, x41, x44, x52, x83, x88, x91, and x92, evaluated through the recorded substitutions and normalizations
- The six retained edge guards g98, g96, g89, g95, g46, and g48, also evaluated through the recorded substitutions

These labels identify the original guarded obligations. An eliminated coordinate still has to satisfy its reconstructed exclusion. The exact retained polynomial hashes and circuit definitions are in [the compact branch](objects/sha256/a4/a4f266dde7c4e29151119f0280361b969d71625e19b6a7d35cae7ed5d2cbaa7b.json) and [the expanded guarded checkpoint](objects/sha256/a4/a4fcb7b9d5b73fc53916e01621500b563ee7a87f30b085ca62f59d4af5dde253.json).

The simplified formulas are T=ζ−ζ⁹x41+x11 x41(x34+x49), A=(ζ⁹−ζ⁴)/(ζ−1), U=AT−1, x39=U/T, and x91=−U/(ζ⁷−ζ⁶). The normalized x91 guard supplies T≠0; the retained x39 exclusion supplies U≠0. These simplifications do not replace the other guards or the residual equations.

The review independently verifies all four pivots, all 34 cancellations, all three normalizations, six guard-irreducibility arguments, 826 exact initial nondivisibility witnesses, and the simplified core. Operational timing and failed-expansion resource counts were not reproduced and are not accepted mathematical certificates. Exploratory checkpoints and failed-checker-development logs are retained with their original labels for provenance.

This remains a necessary-system reduction. A candidate requires every guard, the earlier reverse reconstruction, and all original 121 entry equations before it could establish a factorization. No original factorization, unrestricted complex impossibility theorem, exhaustive remaining-pivot search, or FFT speedup is certified.

Sources: [author report](objects/sha256/cb/cbbdabb42069d6fcc98540d106fba7932b1871a12a7cb7c624ad848adca9cdef.md), [independent review](objects/sha256/30/3023446853538aa3bfcbe3361cbc6791fe09bce6f388f3ae3730ed12643e28ee.md), and [frozen review receipt](objects/sha256/51/51f6adcf4c160cc5b83ae44d99f77544067f91ec915db1fcc234ae83d4f48c39.json). Historical author-pending labels are intentionally preserved byte for byte. The later review receipt gives the current status.

## Prior art correction and unresolved novelty

The bounded priority audit retains the correctness-versus-priority distinction for the prefix-stabilizer theorem and the 9N/5 bank theorem. Neither exact historical priority nor publication significance is certified. Standard interpolation, simultaneous Padé, Prony, scroll, and Bézoutian tools retain their established attribution.

The Erdős–Faigle–Kern 1992 comparison is corrected by a partial addendum. The singleton-regularity exclusion is conditional and cannot be extended to the paper's empty-minimum specialization. The empty-minimum antichain inequality uses the same orbit-stabilizer weights as the prefix objective, but the full prefix chain is not an antichain. Substituting every prefix into that inequality is invalid. For the C4 order 0,2,1,3, it would produce the false assertion 2≤1.

This corrects an overbroad exclusion; it does not establish an equivalent predecessor. Complete source access and statement-level comparison remain unfinished. Only excerpts from printed pages 323, 326, 327, 331, 332, and 333 were inspected; no page images were successfully inspected, and the entire twelve-page paper was not read. The accumulated-stabilizer lemma, global upper bound, equality classification, and exact optimizer count still require a complete comparison with all relevant source statements.

Sources: [bounded priority position](objects/sha256/8e/8ee3d869e00ec5583a49a065fbad620d4a04978fde2dfbd1da1528ffa25bff8e.md), [partial corrective addendum](objects/sha256/50/50f284385577e35b615e5c2267a047782be17fb4d285c1798f91aa7e0d26853e.md), and [source coverage receipt](objects/sha256/e4/e42bda4163f78fa0126a70430ca4a46e2a146c86d994bb257c9918ee36bd8715.json). The addendum qualifies the earlier report without changing its preserved bytes.

## Preservation and audit

The original archive stores one physical content object per distinct SHA-256; this repository export additionally reuses two existing gzip objects for their large logical JSON counterparts. [The source manifest](SOURCE_MANIFEST.json) preserves every original relative filename, byte count, hash, and object location; [the source index](SOURCE_INDEX.md) links each name directly to its bytes. Original gzip and JSON hashes remain distinct. The two large JSON files are reconstructed from their existing gzip counterparts; all other representations remain separately stored. [The compression audit](COMPRESSED_SOURCE_AUDIT.json) verifies the corresponding decompressed contents. Interpreter cache files are explicitly excluded; source programs, intermediate checkpoints, and review evidence are retained.

Run RESTORE_AND_VERIFY.py to verify this archive. To recover the original source tree, pass --restore-to followed by a new directory name. The utility only hashes, decompresses objects explicitly marked gzip, and copies bytes. It refuses an existing destination and does not execute, import, or compile any research program. Original relative links inside byte-identical source documents should be used after restoration. The source index links work directly in the extracted supplement.

[The binding audit](SOURCE_BINDING_AUDIT.json) checks declared source hashes against the local frozen bytes. [The link audit](SOURCE_LINK_AUDIT.json) distinguishes included sources, references to the 1804 checkpoint, and other predecessor dependencies. This is an additive supplement, not a self-contained rerun environment. External citation URLs are preserved; this packaging pass does not claim a new availability test or new full-text inspection.

The prior checkpoint was published at [GitHub commit c1c6d9e](https://github.com/AgentSlop-Si/research/commit/c1c6d9ed3d5801750f3fe68a7e3c1f055eddbdc5). Its publication receipt reports 206 added files and one README update, with 10,897 earlier non-README files preserved. It verifies 183 downloaded distinct blobs covering 206 changed paths. One 1,113,781-byte gzip is verified by the creation acknowledgment, remote Git hash, and size; independent downloaded-byte verification of that binary remained blocked. The historical preservation operation made no additional GitHub write; this separately prepared repository export publishes the frozen supplement. See [the precise publication status excerpt](PUBLICATION_STATUS.json).

[Sheet inclusion status](SHEET_INCLUSION_STATUS.json) records whether a separately verified final Sheet receipt was available for this snapshot. This preservation operation does not edit the Sheet. The archive and protected-checkpoint verification files document unchanged prior bytes.
