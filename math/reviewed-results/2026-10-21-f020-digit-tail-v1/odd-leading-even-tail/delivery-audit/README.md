# Independent audit: odd-leading even-tail public package

This clean detached audit accepts only the exact public ZIP and bounded scope pinned in VERDICT.json. Read REPORT.md for the proof/scope review, conservation, provenance, execution and adversarial checks. AUDIT_RESULTS.json records portable conclusions only; no raw runtime diagnostics are included.

Verify this detached directory with the Python standard library:

    python -I -B verify_binding.py
    python -I -B -O verify_binding.py

Also bind the exact public ZIP:

    python -I -B verify_binding.py --package-zip PATH_TO_PUBLIC_ZIP

The public ZIP SHA-256 is 6d38e41244af02d4d45b64396b134ac24910bd3287ba0a2ca620b1290269ed31. Its own replay instructions remain in that package. SHA-256 is a byte binding, not an author signature or a proof of mathematical truth. New credit is only odd 3<=c<p, even 4<=d<p, r>=2, s>r and all characteristic-zero primitive p^s-th phases; d=0/d=2 and other accepted sectors are inherited. No global closure, novelty or FFT/cost claim is made.
