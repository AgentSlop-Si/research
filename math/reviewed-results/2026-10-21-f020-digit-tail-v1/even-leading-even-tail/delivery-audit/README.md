# Detached independent delivery audit

Read REPORT.md for the exact scope, dependency qualifications and completed checks. VERDICT.json binds this acceptance to one exact main archive; it does not accept later changes.

Verify this audit with its separately supplied trusted manifest digest:

    python -I -B verify_binding.py --expect-manifest TRUSTED_AUDIT_MANIFEST_SHA256 MAIN_ARCHIVE.zip

The main archive must be f020-even-leading-even-tail-public-20261021_v1.zip with SHA-256 67436b165548df8b095e0b6e40c6de9921fd7168ab2601f474dd82873bccef19. Historical omissions are expressly qualified in the main package. No raw execution logs, private locators or external publication are included or authorized by this audit.
