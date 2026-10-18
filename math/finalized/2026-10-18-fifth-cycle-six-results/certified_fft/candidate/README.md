# Certified all-length fallback packet

Start with REPORT.md. The proof is complete at its declared absolute-error contract; independent review is requested before acceptance.

Fresh source:
- certified_fft.py: exact-grid Bluestein/radix-2 backend and paid root constructor
- independent_oracle.py: independent direct-transform enclosure algorithm with a different pi identity
- checks.py: regression, negative controls, invoice audit and saved exact outputs

Reproduce with `python checks.py` (Python standard library only). Historical source is read-only text in sources/. No historical executable package is imported.

`certified_dft(x, epsilon, failed_work=(), cap=None)` takes component pairs of integers or fractions.Fraction values. Denominators must be powers of two. It returns `(all_outputs, receipt)`. Output components are exact dyadic Fractions. Optional failed_work contains immutable FailureCharge records from work already performed; all records are preserved. Optional cap only validates the original cap's domain and does not initiate discovery.

The JSON format represents every exact rational as {"n":"numerator","d":"positive denominator"}. OUTPUT_VECTORS.json includes all inputs, outputs, independent enclosure rectangles and complete receipts. CHECK_RESULTS.json records finite coverage and hashes. MANIFEST.json binds the frozen deliverables; it excludes itself and any Python cache.
