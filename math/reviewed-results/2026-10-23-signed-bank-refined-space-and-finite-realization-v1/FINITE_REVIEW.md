# Independent acceptance: complete finite original signed banks

23 October 2026 UTC.

## Verdict and precise scope

ACCEPT the executed finite fixture N=19, d=4, m=15 over F191, with supplied q=5, in the explicit minimal splitting field L=F191^22. There are 32 effective ORIGINAL signed weighted banks and 608 internal literal resolvents. Every complete inverse, both inverse products, the raw weights, prepared application data, and the full negative unnormalized Fourier matrix have been independently checked by fresh exact arithmetic.

This is a finite physical realization, not another coefficient-only or formal-root certificate. It is not a new uniform theorem, an FFT improvement, an optimal bank-count result, a characteristic-zero realization, or a generic degree-22 splitting claim. No external write was performed.

## Source and coefficient binding

FROZEN_INPUT.json identifies fixture 0 in the accepted structural-endpoint independent CONTROL.json by SHA-256. The reviewer checked that exact byte binding and exact equality of the fixture, rather than accepting a newly selected coefficient vector. The polynomial, in ascending order, is

    [84,93,116,164,163,51,158,162,28,105,119,186,101,82,106,1].

Fresh base-field code reconstructs the constrained structural-endpoint envelope directly from its monomials and formal-endpoint relation. It checks all six envelope equations against this g, independently obtains envelope rank 6, verifies every one of the three original whole-left recurrence rows, and reconstructs and rank-tests the original 19-by-31 axis matrix to rank 19. The monic and nonzero-constant guards, squarefreeness, and forced root 1 are checked. These are direct finite checks of this g's accepted origin and applicability, not an inference from author counts.

The original signed-magnetic and whole-left source text, the accepted structural-endpoint theorem and ledger, and its independent review were read as mathematics. The source bindings and all reviewed candidate bytes are separately frozen. No author or historical scientific program was executed or imported. The candidate C++ source was inspected only as inert text when reviewing its operation ledger; the arithmetic runs below use only reviewer-authored programs.

## Actual field and roots

The reviewer independently proves primality of 191 by trial division, checks that 5 has exact order 19, and multiplies the four factors to recover g. For the degree-2 and degree-11 factors it independently computes the Frobenius residues and proper-subfield gcds in Rabin's irreducibility criterion, using a fresh polynomial implementation without SymPy or candidate helpers. The factors have degrees 1,1,2,11.

Thus the two extensions of degrees 2 and 11 are fields whose intersection is F191. Coprimality of their degrees makes the represented tensor algebra

    F191[A,B]/(A^11+158A^10+43A^9+32A^8+42A^7+173A^6
                +183A^5+33A^4+17A^3+153A^2+48A+175,
               B^2+78B+121)

a genuine field of degree 22, rather than a product ring. Any splitting field must have degree divisible by both 2 and 11, and this field contains all roots, so 22 is the minimal splitting degree of this particular g. Its cardinality is exactly 152311985478009383067227682495511875196478871953281.

Every coordinate is represented in the explicit ordered basis [1,A,...,A^10,B,AB,...,A^10B]. Fresh tensor-polynomial arithmetic checks both generator equations and Frobenius closure. All 15 supplied roots are actually evaluated in this field, checked nonzero and pairwise distinct, and their 15 linear factors are multiplied to recover g coefficient by coefficient. The independently computed root-orbit counts are two roots of orbit length 1, two of length 2, and eleven of length 11. No symbolic-root placeholder, trace, or unexecuted root oracle replaces these calculations.

## Independent complete physical execution

The literal convention is

    S e_t=e_(t+1), T e_t=q^t e_t,
    Q_(k,j)=I-alpha_k S^epsilon_k-q^(epsilon_k delta_k j) T^delta_k,
    B_k=(1/19) sum_j w_(k,j) Q_(k,j)^(-1).

The reviewer checks all signs and indexing, exactly 15 ++ and 15 -- banks using every actual root once in each group, and one bank at node 1 for each cross orientation. All beta values are 1. Every alpha is nonzero, every supplied alpha inverse is checked, and every Delta is independently computed as -alpha^19 and checked nonzero. All supported Gaussian denominator factors, the bank average 1/19, and gamma=(1/19)sum_t q^(-t^2)=157 are checked in the stated field.

All 608 raw weights are recomputed from the supplied amplitudes, with the original negative character exponent. All 361 Fourier-Weyl coefficients are separately accumulated and verified. These coefficient checks are supplementary, not substitutes for the physical execution.

The author used sparse cyclic solves. The reviewer instead computes each inverse using the literal matrix series

    (I+X+...+X^18)/Delta, X=alpha S^epsilon+q^(epsilon delta j)T^delta.

For each of the 608 bank/phase pairs, every matrix power is actually evaluated. All 361 entries of X^19=(alpha^19+1)I are tested, totaling 219,488 entries. Both Q times the resulting inverse and the inverse times Q are then explicitly multiplied using Q's sparse entries. This tests 219,488 entries in each direction, 438,976 in total. It is not merely an invocation of the telescoping proof.

Every resulting inverse coordinate is also compared byte-for-byte with the candidate archive, including all zero extension coordinates: 4,828,736 independent coordinate comparisons. The weighted physical inverses are summed entry by entry. All 361 final L-valued entries equal q^(-at), including the vanishing nonconstant coordinates. All 32 banks are effective. Direct counting of the frozen arrays also gives 604 nonzero raw weights and 355 nonzero amplitudes, without changing the counted bank or resolvent totals.

All 608 prepared ratios and 608 normalized weights are recomputed. An independent implementation then actually executes the original warm sparse schedule for three complete inputs: the archived example, a dense 22-coordinate input, and a base-field input. All 57 L-valued outputs are checked against direct Fourier multiplication. The supplied example agrees with the archived output; for the base-field input all 399 nonconstant output coordinates are explicitly checked zero.

## Reproducibility and negative controls

The independently written C++ verifier is run once at -O2 and once at -O1 with undefined-behavior sanitizer and fail-fast diagnostics. Both runs have identical check counts, arithmetic API counts, warm results, and complete physical matrix output. All tests use explicit exceptions, not optimization-removable assertions. Python 3.12.14 and g++ 14.2.0 were available; no installation was used. The -O2 physical review took about five seconds and the sanitized review about twelve seconds on this environment, not a comparative benchmark.

Four independent input mutations are rejected: a zero node, a changed raw weight, a wrong orientation, and one changed archived inverse coordinate. Mutated files are temporary reviewer copies; no author file is modified. The initial expected diagnostic for the wrong-orientation mutation was adjusted to the earlier, correct cross-singleton guard that actually caught it. No mathematical check was removed.

## Paid costs and storage boundaries

The independently executed warm schedule costs exactly 23,104 L multiplications, 22,496 L additions and 608 L subtractions per input, with no inversion. It includes all bank/phase/output entries, including zero weights. Hence its total additions/subtractions are 23,104. This agrees with the executed author schedule, and is deliberately distinct from the theorem ledger's more optimized 22,477-addition schedule. That smaller schedule was not executed here.

A straightforward 22-coordinate tensor-polynomial multiplication requires at most 746 F191 multiplications and 746 F191 additions/subtractions: at most 484 convolution products, 42 quadratic-relation products, and 220 degree-11 reductions. One extension addition/subtraction costs 22 base operations. Therefore this literal warm schedule admits the conservative independent bounds 17,235,584 base multiplications and 17,743,872 base additions/subtractions, before modular-reduction, addressing and data-movement costs. The candidate kernel uses scalar shortcuts and instruments smaller particular-run counts; its complete-run instrumentation is reported separately and is not substituted for these independent bounds. Inversions and field preparation are not part of a unit-cost warm loop.

The candidate's factorization, field/root preparation, and setup are cold costs. The accepted g was reused; this does not make its prior discovery free. The final factorization records deterministic Berlekamp polynomial-level work; the earlier exploratory factorization has disclosed but uninstrumented internal trials. This review independently verifies the factors, not that exploratory runtime. Per-base-operation counts inside the factorization library are not available. No efficient generic factorization or root-finding claim is inferred.

The actual amplitude builder solves 19 separate original sector systems by dense elimination. Its conservative scaling is O(N^4) post-root field work, rather than an execution of the theorem's more structured O(N^3) interpolation construction. Complete dense inverse verification also has its separate cost. Our geometric-series verification has a still different, larger arithmetic count and is only a review method. Neither verification method is advertised as the warm application.

Every L element has 22 base coordinates. In the candidate C++ representation this is 88 bytes, not one arbitrary-size word. Raw weights alone require 608*22=13,376 coordinates. Prepared ratios plus normalized weights require 1,216*22=26,752 coordinates, plus 32 node inverses and working buffers. One complete 19-by-19 matrix requires 7,942 coordinates; all 608 archived inverse matrices require 4,828,736 coordinates, stored as 4,828,736 unsigned bytes. A complete input or output has 418 coordinates. Base-field output compression requires checking its nonconstant coordinates; the review explicitly does so for the base-input control.

The literal schedule is cubic when the bank count grows linearly and it uses a larger field. Dense Fourier multiplication for base-field input already requires only 361 F191 multiplications and 342 additions at N=19. This artifact therefore closes one concrete finite physical-instantiation gap, not an algorithmic speed gap. No FFT speedup, novelty, optimality, general small splitting field, or closure of a broader research owner is accepted.

## Reproduce the independent checks

Run verify_base.py and prepare_independent_input.py, then compile verify_literal.cpp with a C++17 compiler and run it on INDEPENDENT_INPUT.txt with this directory as output. The optional third argument selects a copy of the inverse archive for mutation testing. run_mutations.py reproduces the four negative controls. The default archive path is recorded in the source and binding receipt. These commands read frozen data only; they never run prepare_field.py or realize.cpp from the author artifact.

BASE_CONTROLS.json, LITERAL_CONTROLS.json, WARM_CONTROLS.json, MUTATION_CONTROLS.json, REPRODUCIBILITY.json, AUTHOR_BINDINGS.json, VERDICT.json and MANIFEST.json contain the machine-readable scope, exact checks and byte bindings.
