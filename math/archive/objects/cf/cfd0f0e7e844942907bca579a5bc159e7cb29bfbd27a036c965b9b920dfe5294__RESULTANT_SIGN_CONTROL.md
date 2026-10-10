# Known resultant convention hazard

The reduced-obstruction check initially failed at `d=21`, where the first resultant argument had degree 5 and the second degree 13. An explicit minimal control in installed SymPy 1.14.0 gave:

    Res(x+1,x^3+2) = -1
    Res(x^3+2,x+1) = -1

Both the `sympy.resultant` expression interface and the polynomial-ring method returned those values. Under the standard root-product definition the first value is `g(-1)=1`, and the second is `-1`. Thus this installed implementation's swapped-degree behavior must not be trusted for that sign.

The final reduced-obstruction program constructs the multiplication matrix directly and computes its determinant by ordinary elimination over the exact cyclotomic field. It separately cross-checks the resultant after reducing the second argument modulo the monic first argument, so the second degree is smaller. It checks the full predicted sign.

The original content computation and its direct alternate route use even-degree `H`, or a degree-`d` polynomial followed by the smaller even-degree `H`; their resultants do not encounter this odd-times-odd degree-swap sign. Every saved discriminant, cluster resultant, and product coefficient already agreed between those routes. Integer contents would in any case be insensitive to a global sign.

The first, failed reduced-obstruction script is retained as `reduced_obstruction_controls.failed.py` for transparency; it is not part of the reproduction sequence. The corrected script is `reduced_obstruction_controls.py`.

The parent independently reproduced the minimal control and located the pre-existing primary issue: https://github.com/sympy/sympy/issues/25406 . This is a known software hazard, not a new mathematical or software-discovery claim.
The issue links the corrective pull request https://github.com/sympy/sympy/pull/30329 , titled “fix(polys): correct the sign of resultant when deg(f) < deg(g)”. No claim is made about whether any newer released version includes that change, and no software was installed or updated.
