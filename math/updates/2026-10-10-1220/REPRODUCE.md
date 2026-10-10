# Reproduce the exact algebra controls

This packet contains mathematical proofs, exact certificate data and source programs. Independent acceptance concerns the proofs and scoped checks summarized in PROOF_STATUS.json. It does not establish novelty or a running-time improvement.

Use Python 3 with NumPy for the selected-pair modular verifiers, SymPy for its direct characteristic-zero N=4 check, and the standard library for the even-chart controls. These are dependency descriptions, not automatic installation instructions.

Run from this packet's root in a disposable working copy. To keep the distributed checksums unchanged, use a temporary directory:

```sh
work=$(mktemp -d)
mkdir -p "$work/finite_edit/independent_review" "$work/even_chart"
cp programs/finite_edit/*.py "$work/finite_edit/"
cp programs/finite_edit/independent_review/*.py "$work/finite_edit/independent_review/"
cp certificates/finite_edit/FRESH_PAIR_OBSTRUCTION_RESULTS.json "$work/finite_edit/"
cp programs/even_chart/*.py "$work/even_chart/"
python "$work/finite_edit/independent_review/verify_pair_obstruction.py"
python "$work/finite_edit/fresh_characteristic_zero_n4.py"
python "$work/finite_edit/fresh_pair_obstruction.py"
python "$work/even_chart/fresh_even_chart_rank.py"
```

The first verifier consumes the distributed explicit weights and reconstructs Green matrices by cycle-orbit geometric sums. The direct N=4 check consumes the same recorded weights. The author-side modular program regenerates seed-19 weights; compare them against the distributed JSON rather than silently substituting a different random-generator output. The recorded arrays, not a generator version, define the frozen characteristic-zero instances.

Expected selected-pair determinants modulo 65537 are 27524, 30664, 29989 and 24911 at N=4,16,64,256. The independent verifier uses the negative of the author's resultant-row convention; a 4 by 4 determinant is unchanged. Its 15 reachable controls cover 10,710 row pairs and include zero horizontal, zero vertical, both-zero and sparse replacements.

The even-chart program checks 378 prime-field cases through N=64, 549,096 matrix entries, an exact F9 case at N=4, and an altered-truncation negative control. Finite controls support the all-field proof, which requires an exact-order root and the strict cutoff a+b<N.

Compare regenerated JSON values with certificates/finite_edit and certificates/even_chart. No files outside the temporary working directory need to change.

## Five bank witness and four bank exclusion at N equals 5

Both included author-side N5 checkers use Python's standard library. The literal witness is encoded as four rational coefficients in the basis 1,q,q²,q³, modulo Φ5. Raw phase weights already include C; normalized sector amplitudes do not.

```sh
mkdir -p "$work/n5"
cp programs/n5/verify_five_bank.py programs/n5/verify_n5_four_bank.py "$work/n5/"
cp certificates/n5/WITNESS.json "$work/n5/"
python "$work/n5/verify_five_bank.py"
mv "$work/n5/certificate_results.json" "$work/n5/five_bank_author_results.json"
python "$work/n5/verify_n5_four_bank.py" > "$work/n5/four_bank_exclusion_results.json"
```

The first checker verifies the literal five-bank witness, all 25 original branch inverses on both sides, all Fourier entries, guard values, phase weights, and the stated determinant residues. The second checks 95 exact identities in the four-bank exclusion and prints JSON, redirected above to its own result file. These prove different halves of the exact-minimum conclusion.

The portable independent witness control keeps all 742 mathematical checks. The original full acceptance run had 756 checks, including 14 checks of private-source provenance hashes that are not needed for public mathematical reproduction. It verifies 100 signed branch instances over four conjugates, 100 reindexed branch instances, 100 Fourier entries, all normalizations and the support gate.

```sh
cp programs/n5/verify_witness.py programs/n5/verify_lemma.py "$work/n5/"
cp notes/05_n5_five_bank_construction.md "$work/n5/N5_FIVE_BANK_CONSTRUCTION.md"
python "$work/n5/verify_witness.py"
python "$work/n5/verify_lemma.py"
```

The lemma control additionally uses SymPy. It checks 186 symbolic identities, coefficient matrices, determinant/rank statements and the entire amplitude table against the witness. The independent reviewer supplied and reran both portable controls; their program bytes are included unchanged. Because the exported proof has editorial/path changes, a regenerated proof hash differs from the accepted source proof hash in the original saved result; the mathematical checks and table are unchanged.
