# Prime-power equality-mask proof candidate

Read REPORT.md first, especially Sections 3–6. This is a new uniform theorem candidate, not a finite census and not yet independently accepted.

Reproduce the new exact checks:

    python verify_primepower.py

The checker uses only the Python standard library and reads no historical program. It overwrites only RESULTS.json, DESCENT_CERTIFICATES.json, and CONNECTED_INVERSE_WITNESS.json in this packet. Expected status: PASS.

The proof explicitly permits repeated character labels and unequal row weights in the induced blocks. The connected (8,4) source counterexample is a positive control; a separate direct-sum control tests repeated labels in both coordinate sets. Both Grams are verified at every descent node. The actual original inverse-row minimizer is independently recomputed in Q[z]/(z^4+1).

Source reports are copied solely as text/data. SOURCE_BINDINGS.json records both original and copied bytes. MANIFEST.json covers the frozen files; SEAL.sha256 covers the manifest. No external write, owner change, or acceptance claim is made.
