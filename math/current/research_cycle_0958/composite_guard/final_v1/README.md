# Composite half-order RS guard extension

Read COMPOSITE_GUARD_EXTENSION.md for the complete proof and exact limits. The all-composite question stays open. The new family theorem is for d=sp, s∈{3,7,11}, with p prime and p≡1 mod4. It does not improve the scalar-bank minimum at d≡3 mod4.

Fresh bounded controls (from the workspace root):

    python research_cycle_0958/composite_guard/fresh_augmented_content.py
    python research_cycle_0958/composite_guard/fresh_pairing_controls.py
    python research_cycle_0958/composite_guard/fresh_exception_control.py

The first computes fixed lower-base constants exactly. The second checks the parity-complete pairing through discriminant-polynomial gcds at p=3,5,7,11,13; it is corroboration, not the all-p proof. The third exhibits the real exceptional residue component at s=7,p=13 and the other two good components. These programs were newly authored and import only installed SymPy and Python standard library modules. No archived/source research program is imported or run.

SOURCE_PROVENANCE.json records the inert mathematical inputs. FINDINGS.json is the integration summary. Independent reviewer acceptance should be recorded separately and against the exact proof hash; it must not be inferred from this directory's own controls.
