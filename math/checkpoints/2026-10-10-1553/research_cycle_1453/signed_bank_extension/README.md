# Order-eleven signed-bank extension

Independently accepted main result: M_C(11;q)≤14 for every primitive eleventh root q, in the exact accepted signed magnetic resolvent-bank grammar.

Read N11_FOURTEEN_BANK_CONSTRUCTION.md for the complete characteristic-zero construction, every amplitude and branch weight, field and denominator conditions, good-reduction certificate, restricted quintic-ansatz obstruction, and cost boundaries.

Core exact data:
- N11_EXACT_WITNESS.json: exact cyclotomic coordinates for the sextic, edge moments, all eleven transformed row vectors, and the restricted quintic residuals.
- N11_MODULAR_CERTIFICATE.json: all reduced row matrices, selected nonzero minors, determinant1 of the defining system, and resultant6 of g,g′ at (23,q−2).
- N11_LITERAL_MOD23_RESULTS.json: both literal inverse products on44 generic branch matrices representing154 branches, and all 121 original Fourier entries, passed at the good reduction.

Fresh author controls, authored from the displayed mathematics and run only in this new directory:
- fresh_exact_n11_control.py: exact arithmetic over Q(q), all 121 Weyl equations and direct trace coefficients; also exact restricted-quintic failure.
- fresh_n11_construction.py: good-reduction certificate with no numerical roots.
- fresh_literal_mod23_control.py: literal original-resolvent control in F23[t]/g.
- fresh_modular_probe.py: exploratory depressed-quintic control; its failure is confined to that stated ansatz.

All source research programs remain unexecuted and unimported. None of the accepted N=7 files was modified. Ordinary installed SymPy is used by the exact fresh control; the modular controls use the Python standard library only. Corresponding run logs are retained.

Independent acceptance is recorded in ../signed_bank_review/ACCEPTANCE_RECEIPT.json and, separately for the two-parameter family, ../signed_bank_review/parametric_family/FAMILY_ACCEPTANCE_RECEIPT.json. The reviewer independently proved both original inverse products for all 154 branches and directly verified all 121 Fourier entries in characteristic zero. The pending-review wording inside the frozen author mathematics records its historical author status; the later receipts establish acceptance. Do not rerun frozen reviewer scripts in place, because they refresh outputs. No bank minimum at11, all-size family, runtime speedup, or historical novelty claim is made.

PARAMETRIC_FAMILY_ADDENDUM.md gives a nonempty Zariski-open two-parameter family at fixed order eleven. It is separately accepted and does not claim a family of transform orders.
