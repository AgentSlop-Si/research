# Sources, inherited work, and coverage

**Date:** October 10, 2026.

## Coverage and limitations

The current conversation contains the mass-contraction, annihilator-feedback, marked-cycle, growing-fiber, norm-tabulation, sparse-jet, shared-scan and necklace-transport proposals. Their stated distinctions between exact identities, missing fast factorizations, structured input promises and finite-word approximation were preserved.

The checkpoint-26 archive was present. Its findings ZIP's `INTEGRATED_RESULTS.md` and `CHECKPOINT25_MATHEMATICAL_RESULTS.md` were consulted as the broad project synthesis. Those documents describe an earlier static review and explicitly distinguish static coverage from execution or proof correctness. I do not credit those historical inspections or historical test counts as work repeated in this pass.

Two attempted broad tar.xz text reindexing runs did not finish within the tool execution limits. No new comprehensive archive index or all-files re-verification is claimed. The source hashes of the specific consulted local materials are in SOURCE_HASHES.json. This is a targeted synthesis using the available checkpoint and relevant controlling notes, not an independent audit of every historical research file.

## Directly used inherited source

`[local source reference]` was read, including its model, error, preparation, and reference-implementation boundaries. It is preserved as `INHERITED_DYADIC_THEORY.md`.

`norm_tabulation.py` was copied without changes as `inherited_norm_tabulation.py`:

    SHA256 726c8e709e9ddbc9c6d0f6d8760fb707fe8c9ee35790446c7af350c638458a41

Its dyadic mathematical primitive has the normwise tolerance contract. Its ReferenceFFT class computes high-accuracy blocks on demand, so it is NOT the theoretical eager-table runtime implementation. The new wrapper overrides `_block` to remove persistent input-specific block caches. This inheritance is explicit rather than presented as newly written or independent code.

## Relevant retrieved project checkpoints

- `RESEARCH(20261009-171053).md`: earlier randomized all-length lift; acknowledges Anderson–Dahleh and Ruiz-Antolin–Townsend antecedents and leaves a complete finite-precision composition open. The new work replaces its random row mechanism with the deterministic norm-certified dyadic backend and uses an operator-norm proof.
- `CHAIN_CHECKPOINT_2026-10-10_v30.md` and `RESEARCH(20261010-121950).md`: exact independent-order/Schur-interface restrictions. The new approximation theorem does not contradict or solve those exact factorization constraints.
- The current necklace-transport and shared-scan manuscripts: fast auxiliary exact operators or representation constraints do not supply missing Fourier phases. Their candidate factorizations are not assumed.

## Mathematical contribution actually made here

The contribution is the centered oversampled all-length identity, dimension-free factorial operator tail, a concrete fixed-point wrapper and end-to-end rounding bound, the resulting arbitrary-length finite-word complexity theorem (including an inverse-polylogarithmic tolerance corollary), and the exact Vandermonde rank of the same phase-correction matrix.

The general Taylor/near-grid idea, table method, normalized Fourier factorization, Vandermonde rank, and elementary rounding techniques are not new. The work is an incremental extension of the project's constructive approximation branch. No publication-level historical novelty is established, and no new exact arbitrary-complex FFT is obtained.

## Primary public sources inspected

1. Anderson and Dahleh, *Rapid Computation of the Discrete Fourier Transform*, SIAM J. Sci. Comput. 17(4), 913–919 (1996), DOI 10.1137/0917059. Publisher abstract: unrestricted lengths/nonuniform points through local Taylor expansions and FFTs. Only the retrieved material was used; no complete article audit is claimed.
2. Ruiz-Antolin and Townsend, *A Nonuniform Fast Fourier Transform Based on Low Rank Approximation*, SIAM J. Sci. Comput. 40(1), A529–A547 (2018), DOI 10.1137/17M1134822; arXiv:1701.04492. Publisher/preprint abstracts support the known diagonally scaled FFT-sum method and rank/accuracy dependence.
3. Alman, *Faster Walsh-Hadamard Transform and Matrix Multiplication over Finite Fields using Lookup Tables*, SOSA 2023, 137–144, DOI 10.1137/1.9781611977585.ch13; arXiv:2211.04643. Established adjacent lookup-transform acceleration, with a different field/model contract.
4. Liu, Li, Chan and Lam, *A Novel Approach to Fast Discrete Fourier Transform*, J. Parallel Distrib. Comput. 54(1), 48–58 (1998), DOI 10.1006/jpdc.1998.1472. The inspected abstract describes a Taylor/moment approach and sub-N-log-N multiplication/systolic measure. The full paper's model and error bounds were not independently audited.
5. Official OpenAI Math repository, `lean/docs/130.md`, inspected October 10, 2026. Reports separate subsequential and uniform exact-complex results and their supplied-root/unrestricted-coefficient scopes. No such construction is imported or independently certified here.

No PDFs were needed to support the facts stated from these publisher/abstract pages. A limited literature search is insufficient to establish originality.

## Executed evidence

Only the new wrapper/test suite was fully rerun twice. Source/results hashes and run logs identify the actual tested versions. NumPy full-matrix norm computations and 70-digit mpmath comparisons are numerical corroboration; rational schedules and finite-field rank tests are separately identified. Historical eager-table test totals are not reused as current run totals. The reference wrapper itself is not a practical speed demo.
