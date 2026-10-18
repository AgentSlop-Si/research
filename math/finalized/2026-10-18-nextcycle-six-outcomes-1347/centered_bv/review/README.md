# Independent bounded-variation review

Read REVIEW.md for the final verdict, scope and exact evidence. This directory is separate from the unchanged author packet.

The reviewer independently checks all 512 original-target outputs, every one of the 2,048 centered coefficients, all 21,609 retained-operator incidences, eleven recognition rejection prefixes, and seven auxiliary complex-source estimates. The complete copied frontend and semantic source replay are actually rerun; the complete outer production stream is not rerun by this review.

Key evidence:

- REPRODUCTION_COMPARISON.json and FRESH_SOURCE_REPRODUCTION.json: exact fresh source and receipt reproduction.
- INDEPENDENT_OUTPUT_CHECKS.json: actual original norm, exact scale-back, all original rows and all centered coefficient contracts.
- INDEPENDENT_RETAINED_CHECKS.json: complete independently assembled retained operator and row inequalities.
- INDEPENDENT_CONTROLS.json: reexecuted rejection receipts and separately checked complex estimates.
- ALGEBRAIC_TARGETS.json: outward 512-bit nested-radical direct-sum targets, with no shared production trigonometric construction.
- MANIFEST.json and SEAL.json: frozen review bytes and candidate association.

Verify retained bytes with python verify_review.py. No external services or third-party packages are needed.

For numerical reproduction, work in a copy to preserve the original measured fields and seal. SOURCE in independent_review.py and write_review.py must identify the retained author packet. Then run:

    python independent_review.py math
    python independent_review.py front
    python independent_review.py saved
    python independent_retained.py
    python independent_controls.py
    python write_review.py
    python verify_review.py

The frontend reproduction runs a full provider and a full semantic source replay. Its measured duration is not a complexity theorem. Independent oracle, control, export and packaging work is separate from production receipts. General ALG-034 remains open.
