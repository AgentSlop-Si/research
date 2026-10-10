# HERO17 tensor/fiber sealed audit

Read AUDIT_REPORT.md first. EXTENSION_AND_FUSION.md gives the separately budgeted uniform-rank union and a bounded degree-independent polynomial-phase corollary. PRIOR_ART.md supplies limited primary-source context.

Portable independent checker (Python standard library only):

    python independent_checks.py

Run inside this folder, or pass its absolute path. It imports no supplied archive or master code and needs no input files or network. It rewrites only independent_results.json and prints the report. The checked-in independent_run.log preserves the original run. Runtime is diagnostic; counts and exact identities are the test evidence.

provenance.json records source/reference file hashes. SHA256SUMS seals all deliverable files other than itself. Rerunning changes the timing field, so preserve the sealed original before regenerating results. The source archive and prior master were not modified. This audit does not claim the archive’s programs were executed.
