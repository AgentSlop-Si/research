# Independent N7 certificate controls

These freshly authored independent controls reproduce the accepted mirrored-pattern certificate. They use Python 3 and SymPy for exact arithmetic and polynomial algebra; they neither import nor execute supplied research programs. The three files in sources/ are inert JSON coefficient data. No source-author program is included.

Run in a disposable writable copy of this directory, with Python 3 and SymPy already available:

    python verify_reduction.py
    python verify_axis_norm.py

The scripts write their exact result JSONs beside themselves. Do not run them in the frozen publication copy. Dependencies: Python standard library and SymPy. The result files included here were produced by the independent acceptance pass.

The first control derives the degree-nine moments, checks all guard Bezout identities and all signed resolvent polynomial identities. The second independently derives the actual axis determinant by complementary minors, checks all 6,561 multiplication-matrix entries against the literal certificate, and produces determinant 14 modulo 29 with an explicit inverse. The characteristic-zero implication requires the good-reduction argument in the public proof; an isolated finite-field failure would not suffice.

Scope: (2,1,1,2) in (++,-+,+-,--) order is excluded, as is its verified transpose partner (1,2,2,1). The patterns (2,1,2,1) and (1,2,1,2), general six-bank attainment, and the exact N7 minimum remain open. The inherited bound is at least six.
