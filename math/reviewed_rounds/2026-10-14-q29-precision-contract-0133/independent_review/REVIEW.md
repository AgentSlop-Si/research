# Independent bounded review of the Q29 precision contract

2026-10-14 UTC.

## Verdict

**ACCEPT for the exact finite-ring and precision contract, with the execution conditions below.** No mathematical repair is needed for the claimed ring, carry boundaries, staggered quotients, guarded division, or uniform precision-140 design bound. This accepts a bounded design and its small controls. It does not accept an executed mixed-characteristic H1687/R843 lift, a terminal repeated-branch computation, or any value/nonvanishing claim for the full ordinary discriminant. Those remain open.

Targets reviewed:

- `q29_precision_contract/PRECISION_CONTRACT.md`, SHA-256 `e1d40ce00296465e93d8607d45e645fb040c403945bd6e2f1961373c13ee5149`
- `q29_precision_contract/fresh_exact_controls.py`, SHA-256 `3c2017ee711aa858cb3baffe909982bd021bd8d3e92ff7f921b3fa6a7eb0059c`

The original files were not edited. The submitted fresh controls were copied into this review directory and executed there; all non-timing output values agree with the submitted result. Every one of the six target manifest entries matches its length and hash. Predecessor documents and archive contents were treated as inert inputs. No historical scientific program was executed.

## Mathematical audit

1. **Exact ring.** The order of 5 modulo 27 is 18, so Phi27 is irreducible over F5. Its monic lift gives the unramified degree-18 integer ring O. The polynomial f(T)=Phi125(1+T) is monic Eisenstein of degree 100 with constant term 5. Consequently A=O[T]/f(T) is the required complete DVR, with pi=T and v_pi(5)=100. Thus B_M=A/(5^M)=A/(pi^(100M)). The specified alpha/xi root decomposition is consistent: the CRT exponents 1000 and 2376 recover the order-27 and order-125 factors from q. The standard unramified and Eisenstein assertions used here match [MIT Lecture 10, Theorem 10.13 and Corollary 10.15](https://math.mit.edu/classes/18.785/2021fa/LectureNotes10.pdf) and [MIT Lecture 11, Lemma 11.4 and Theorem 11.5](https://math.mit.edu/classes/18.785/2021fa/LectureNotes11.pdf), which were checked in this review.

2. **Valuations and staggered moduli.** In the power basis sum_j b_j pi^j, the terms have valuations 100 v_5(b_j)+j, pairwise distinct modulo 100 when j differs. Therefore a minimal valuation cannot cancel. Reduction of the alpha basis modulo 5 likewise gives v_5(b_j) as the minimum coordinate valuation. The ideal pi^N consequently means exactly that the j-th O-coordinate is divisible by 5^max(0,ceil((N-j)/100)). This proves the stated unique quotient representative and the count 5^(18N). It also proves that monic reduction must precede staggered coefficient reduction.

3. **Guarded division.** The constant coordinate condition c_0 in 5O is exactly the condition of divisibility by pi. Substituting d_99=-c_0/5 into pi sum_j d_j pi^j and applying f(pi)=0 gives the displayed d_(j-1)=c_j+f_j d_99 formula, with the correct sign. It provides a representative quotient, not an inverse of pi. Its ambiguity is the kernel of multiplication by pi, namely pi^(100M-1)B_M. For an input known only modulo pi^P, h guarded divisions lose exactly h from the certified precision. The code respects h<P, but callers must continue to carry this precision separately: the arrays themselves do not enforce it.

4. **Carries.** The complete mod-25 relation has the eight displayed lower terms, including coefficients at pi^25, pi^50, pi^75, pi^80, pi^85, pi^90 and pi^95. The defects have valuations 100 for 5, 125 for 5+pi^100, and 101 for (1+pi)^5-1-pi^5. They first become observable at precisions 101, 126 and 102 respectively. Dividing the Frobenius defect by pi^101 has residue 4. Ordinary alpha-coordinate digits and integer centers must not be silently treated as Teichmuller digits.

5. **Jet and tail precision.** If G-J belongs to (pi^N,v^K), substitution v=pi^s Y and division by pi^h leave error at least min(N,sK)-h. Translation by an integral center at nonnegative scale preserves the lower bound; further normalization subtracts its exponent. Formal differentiation in the current variable cannot decrease coefficient valuations, but conversion to an earlier variable requires the inverse scale. No hidden hypothesis of squarefree reduction is needed for this error lemma.

6. **The proposed shared-center gate.** For R843 truncated at w<100, every discarded summand in the exact reciprocal transformation starts at v^200 or higher. The recurrence uses polynomial additions/multiplications and never moves discarded w powers down. With B2 coefficient precision 200, the raw U jet is therefore valid modulo (pi^200,v^200). Once the pi^60 content is certified and guarded division passes, F is valid modulo pi^140. Keeping w<50 while merely increasing M would retain the old uniform ceiling 40. A direct H implementation needs v<201 before exact extraction of -H/v to obtain U at v<200.

The claimed precision 140 is a genuine worst-case ceiling for this information: 1 and 1+pi^140 give exactly the same numerator after multiplication by pi^60 in B2, while their difference is visible modulo pi^141. Independently, an omitted raw term v^200 can become pi^140 Y^200 after substitution and normalization. Special additional information can improve a particular coefficient or branch, but it cannot be assumed.

The optional extension f(rho^d) remains Eisenstein of degree 100d. It is a correct model for adjoining rho with rho^d=pi, provided the embedding and valuation conversion are explicitly fixed. It was not implemented or computationally validated here.

## New bounded controls

`independent_small_audit.py` supplies an independently written dense schoolbook reduction that reduces pi before alpha, opposite to the submitted sparse code. It agrees on 20 fixed-seed sparse products in B2. It also checks:

- every staggered precision N=1,...,200;
- guarded division for exponents 1, 2, 25, 60, 99, 100, 101, 125 and 199 with nontrivial unramified coordinates;
- the precision-140 ambiguity witness described above;
- all three carry valuations and visibility boundaries;
- the full displayed mod-25 relation;
- submitted manifest integrity and equality of all non-timing replay outputs.

Both the author-code replay and the independent bounded controls completed successfully, with empty stderr. These tests corroborate the algebraic proof; they do not replace it and do not test the large proposed recurrence. Results are in `INDEPENDENT_CONTROLS.json`, `CONTROL_RESULT.json`, and the corresponding stdout/stderr files.

## Transparent operation and storage budget for the proposed run

The following is a baseline estimate for one shared-center R843 computation over B2 with w<100. It is not an observed run time or a claim that the supplied Python dictionary code is practical at this size.

Each B2 coefficient has 18*100=1,800 coordinates modulo 25. Let A_m=-2+q^(2m)+q^(2m-1) and B_m=(1-q^(2m-1))(1-q^(2m-2)). A straightforward recurrence computes A_m times every retained coefficient of R_(m-1) and B_m times every retained coefficient of R_(m-2), with zero absent coefficients omitted:

- A-products: sum_(m=1)^843 min(m,100) = 79,350.
- B-products: sum_(m=1)^843 min(max(m-1,0),100) = 79,250.
- Total: at most 158,600 coefficient-ring products, plus recurrence additions. Algebraic zero/one and multiplier structure can reduce the actual count.

A completely dense schoolbook B2 product performs 1,800^2=3,240,000 scalar product-accumulations before reduction. The resulting declared baseline is at most **513,864,000,000 scalar product-accumulations**, excluding monic reduction, coefficient setup, checks and output. This is an algorithm-specific upper budget, not a lower bound on the best algorithm. Generic dense multiplication is avoidable: the q powers and recurrence multipliers have substantial structure, and a production implementation should exploit it while independently checking the kernel.

Monic reduction and modular reduction also cost work. A dense raw product uses a 35 by 199 coefficient workspace. For M=2, only eight lower f_j are nonzero modulo 25. A descending reduction can process at most 17*199 alpha-high cells with two updates each, then at most 18*99 pi-high cells with eight updates each. These bounds describe a dense implementation; the submitted dictionary implementation has additional allocation, hashing and scanning costs.

The v<200 reciprocal transformation has sum_(k=0)^99 (200-2k)=10,100 scaled coefficient additions, since the k-th summand begins at v^(2k). Integer binomial coefficients can be reduced modulo 25 before acting on B2. This is at most 18,180,000 coordinate multiplications and a comparable number of additions in a dense representation. Normalization, comparison with old coordinates, and output serialization are additional bounded work.

For storage, assuming explicit uint8 coordinates in 0,...,24:

- One retained R slice: 100*1,800 = 180,000 payload bytes.
- Three rolling R slices: 540,000 payload bytes, approximately 0.515 MiB.
- One raw v<200 U jet: 200*1,800 = 360,000 payload bytes, approximately 0.343 MiB.
- A dense raw-product scratch array has 6,965 cells; accumulator width depends on the reduction schedule. Use a proved-safe wider type and modular reduction schedule, never overflowing uint8 arithmetic.

The transform can reuse the recurrence buffers. These numbers exclude q-power caches, language/container overhead, proof metadata, source arrays and serialized output. Caching all 3,375 q powers densely would add 6,075,000 payload bytes; it is optional because powers can be streamed or stored in structured form. Python dictionaries require much more memory than these packed-array figures. No justified seconds estimate follows from the tiny controls. Any claimed practical runtime must come from a separately authorized, instrumented implementation and its actual completed receipt.

## Conditions still required before a larger result can be accepted

- Recompute the integral recurrence in the full mod-25 ring. Merely assigning zero high digits to the characteristic-5 array does not reconstruct its lift.
- Bind the selected primitive q, alpha residue identification, basis order, sign -H/v, and branch-center lifts to the imported reference data.
- Supply and test a production ring/recurrence implementation. The current file is a small control program, not an H1687 runner. Independently compare all available old raw coordinates modulo 5.
- Certify the pi^60 normalization using the source-bound integral-content argument and verify the guard on each required divided coefficient. This review accepts the precision implication; it did not reconstruct the old degree-1687 data.
- Keep the actual certified precision attached after every division. Any valuation reported from a representative above that precision is unproved, despite the array's capacity of 200.
- Keep the raw v-tail, coefficient error and subsequent branch scales together. Resolve or stop every repeated branch at its certified ceiling. The next run is only a shared-center jet, not all-center coverage or a full-degree discriminant computation.
- Do not infer nonvanishing, a derivative unit, squarefree residual factors, center symmetry, or the required eventual precision from the present contract.

Minor terminology only: the arrays use the power basis 1,alpha,...,alpha^17 and 1,pi,...,pi^99; calling this “normal-basis arithmetic” in the Teichmuller paragraph could be changed to “power-basis arithmetic.” This does not affect the proof or controls.

No external writes, uploads, commits, table updates, ranking changes, or full-Q29 closure were performed by this review.
