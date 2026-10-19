# C13 fixed-direction entry-oracle integration packet

Read RESULT.md for the elementary query lower bound, matching adapter contract,
owner mapping, exact model limits, and retained gates. Start with DISPOSITION.json
for the administrative disposition. This packet makes no whole-owner closure,
Fourier lower-bound, publication-priority, or independent-review claim.

Reproduce with Python 3.10 or later and its standard library:

    python3 -I check.py

For a minimal exact callback example, run `python3 -I example.py`. Its known
formula is only a demonstration of the API; the unstructured-input lower bound
does not apply to a promise that the target is exactly that formula.

This executes only the freshly authored adapter/checker in this directory.
RESULTS.json and REPLAY.log record the finite exact controls. The source-bound
accepted theorem and owner snapshots are copied unchanged under sources/.
SOURCE_BINDINGS.json records their origins and hashes. MANIFEST.json hashes all
packet files except itself and SEAL.sha256; SEAL.sha256 binds that manifest.
