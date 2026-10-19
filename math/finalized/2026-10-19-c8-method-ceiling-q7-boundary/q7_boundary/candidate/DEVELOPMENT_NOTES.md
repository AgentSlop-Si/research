# Development provenance

The two scripts retained under `development/` were exploratory incidence calculations using installed SciPy linear programming. Their numerical outputs are not certificates, not evidence of square-mask nonexistence, and not required by the proof or final checker. The final proof replaces all such exploration with explicit integer inequalities and symbolic arguments. The final verifier uses the Python standard library only and no floating arithmetic.

The key repair is square column regularity: a line-free, fiber-free row has too few possible primitive partners. At degree eleven this eliminates every 3+4 split, including all possible arrangements rather than only the previous rectangular control. Saturated stars then force full lines before the final primitive-overlap contradiction.

No optimizer infeasibility result, failed construction search, general square-block assumption, or re-execution of the accepted q>=11 theorem is counted as a result.
