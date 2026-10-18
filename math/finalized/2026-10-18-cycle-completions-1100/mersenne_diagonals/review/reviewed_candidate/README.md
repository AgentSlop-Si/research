# Width-adaptive Mersenne diagonals

Read REPORT.md for the complete theorem, operation ledger and limitations.

New result: both full-width factorial diagonal maps, the kernel and inversion can be evaluated in O(nW B^(log2(3)-1)+nW(log(n+1))^(log2(3)-1)), where B=min(W,max(1,(n-1)ceil(log2 n))). This strictly improves the explicit Karatsuba diagonal construction in the very-wide-digit regime. The same-scale convolution and matrix/prime-selection gates remain open.

Run the fresh standard-library controls with:

    python fresh_controls.py

They write RESULTS.json, so use a disposable copy if preserving the manifest. Source code from prior work was restored and read only; it was not executed. This package is a candidate awaiting independent review and authorizes no external write.
