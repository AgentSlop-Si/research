# Portable validation and replay

Requirements: Python 3 standard library, a C++17 compiler such as g++, and ordinary POSIX shell utilities. No network access, third-party Python package, secret, native document session, or local absolute path is required. Work in a disposable copy if preserving a pristine release object matters, because scientific replay writes deterministic output files and a compiled local binary.

## Validate the frozen object

From this directory:

    python -I -S verify_packet.py

This checks the publication seal, every publication member, both exact scientific manifests, the final narrow mathematical verdict, and the unchanged owner status/priority.

## Independent scientific replay

From review/:

    python -I -S independent_structure.py
    g++ -O3 -std=c++17 independent_minors.cpp -o independent_minors
    ./independent_minors AUTHOR_FIXED_MINORS.txt > replay.txt 2> replay.log
    cmp replay.txt FIXED_REPLAY.txt
    cmp replay.log FIXED_REPLAY.log

This reconstructs all original six Green matrices at the sixteen Boolean interpolation points, checks every inverse in both directions, and verifies the 560 specified 126-by-126 minors without replacement. It checks 70,560 full original-polynomial quotient identities, 53,760 Green inversions, and 6,881,280 inverse-entry comparisons per complete fixed replay, plus two duplicate-row determinant zero controls. The support and ring-homomorphism proofs are in the scientific reports.

Optional independent source-to-input binding, from review/:

    python -I -S bind_frozen_candidate.py

Its sibling candidate/ dependency and all inputs are present in this object.

## Fresh author replay

From candidate/:

    python -I -S make_chart_header.py
    g++ -O3 -std=c++17 certify_four.cpp -o certify_four
    ./certify_four > COVERAGE_PRIMARY.jsonl 2> COVERAGE_PRIMARY.log
    ./certify_four 430477711 > COVERAGE_CONJUGATE.jsonl 2> COVERAGE_CONJUGATE.log
    python -I -S verify_structure.py > STRUCTURE_CHECKS.log

This reconstructs every original window for all 280 labels in both embeddings: 439,040 full quotient/multiply-back checks. The author and independent reconstructions are distinct.

Do not use review/seal_review.py as a replay entry point. It is an exact archival administrative script whose convenience-run directories were intentionally not published. Do not run the historical programs named in the copied source prose; they are not dependencies of this new result.
