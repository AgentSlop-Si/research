# RS/Q08 reference-validator implementation review

Verdict: ACCEPT repaired version 1.1 at checker SHA-256 `7cf350bfa8037e2addb3f26454a0e047b4f8df501500158292f45b9020d8a60c`. The original candidate remains REPAIR for the two resolved contract/API findings.

Read `INDEPENDENT_IMPLEMENTATION_REVIEW.md` first. `VERDICT.json` is the machine-readable scope. `Q08_ROW_PROPOSAL.json` is a proposal only.

- `candidate/`: unmodified original archive extraction, with its original manifest.
- `repaired_candidate/`: runnable accepted checker, corrected documentation, same pinned sources, and regenerated examples.
- `repair/`: exact source and minimal patch received for re-review.
- `evidence/`: sealed original archive.
- `results/`: both rounds of independently produced logs and exact reproductions.
- `independent_review_controls.py`: fresh controls and original finding reproductions.
- `repaired_review_controls.py`: full re-review plus repaired API controls.

From the extracted review directory:

    python3 -B independent_review_controls.py
    python3 -B repaired_review_controls.py
    cd repaired_candidate
    python3 -B -m unittest -v test_rs_certificate.py
    python3 -B rs_certificate.py verify examples/separated.certificate.json

The review controls intentionally import only the fresh candidate implementations. Historical source programs remain inert. Rerunning the controls rewrites their local result logs; retain the sealed archive as the immutable record. The manifest binds all original packet members except the manifest itself. The external delivery receipt binds the whole archive and its Library identity.
