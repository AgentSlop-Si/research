# Chain checkpoint — exact 99-edge Fourier-compatible superconcentrator gate v33

**Inherited:** v31 finds sparse depth-three superconcentrators could have `Theta(N log log N)` edges; v32 proves a phase-count/phase-alphabet gap only for positive root-weight circuits. Exact fresh-input `O(N)` or `O(N log log N)` Fourier is **not** achieved in this project. Official OpenAI Math result #130 reports a much smaller all-length exact-register power saving, in a different model/approach.

## New exact positive topology

- 11 inputs, 22 hidden nodes, 11 outputs, exactly three 3-regular bipartite layers of 33 edges each, `E=99<121` direct-dense edges.
- `topology_11.json` fixes all 99 edges and its search provenance.
- Every equal-cardinality nonempty terminal-subset pair has vertex-disjoint paths, all `C(22,11)-1=705431` pairs proved by exact subset-DP Boolean relational composition.
- Fixed integer weights `weights_11.json` modulo prime `q=1000000123` give a full-spark 11×11 transfer `transfer_11.txt`. C++ exhaustively verified **all 705431 square minors nonzero**, not just samples.
- Generic independent complex weights on this graph are full spark by LGV; full spark ≠ Fourier.

## Exact Fourier phase and dimension gate

- For dense `H=CBA`, diagonal-equivalence to `F_11` iff each of the 100 anchor crossratios `H_ij H_00/(H_i0 H_0j)` equals `zeta_11^(ij)`.
- These are degree-6 equations in 99 edge variables.
- 44 graph vertices yield a connected 43-dimensional effective vertex-gauge torus leaving every crossratio invariant. Therefore projective image dimension ≤56.
- The exact 100×99 Jacobian over GF(1000000123) has rank **56**, with an explicit 56×56 minor determinant residue **915710031** and all 44 infinitesimal gauge directions checked. Modular nonvanishing of integer numerator lifts to characteristic zero. Generic complex dimension is **exactly 56**, codimension **44** in 100 crossratios.
- The saved full-spark weight assignment violates all 100 Fourier crossratio equations (first witness `379306912` at (1,1)). **Does NOT prove no other weights exist.**
- 16-start complex numerical optimization reached squared error per entry ~0.176876844; heuristic only.

- **No affine linear relations** among the 100 Fourier crossratios: 101 independent evaluations have nonzero determinant **763214669** modulo 1000000123. The 44 relations are necessarily degree >=2; quadratic existence unproved.

## New model audit (classical basis)

- Morgenstern's bounded-coefficient determinant method dominates v32 for unnormalized Fourier even with signed cancellations.
- For any linear DAG, `sum_v ln(max(1,sum_in |w_e|)) >= (N/2)ln N`.
- If all `|w_e|≤1`, counting all incoming edges gives `E >= (3/(2 ln3)) N ln N`.
- For max amplitude B≥1, `ln B >= (N ln N)/(2 E) - ln3/3` (when positive).
- These do **not** imply an unrestricted or normalized Fourier bound. Every circuit can be reweighted to incoming l1 mass exactly 1 internally by path-mass gauges, pushing requisite Fourier gain `P_out≥N` to final output multipliers. All endpoint scalar multiplications must still be charged.
- Exact ordinary radix Fourier and Gram controls pass at N=4,8,16,32 using integer cyclotomic quotients.

## Verification

- **17/17 tests**, 705431 exact graph path-pair checks, 705431 exact finite-field nonzero-minor checks, exact 56×56 Jacobian minor, 44 vertex gauge derivatives, 220 independent maxflows, 330 independent random minor checks.
- Full v32 archive embedded unchanged, SHA/CRC checked. Cold-run and archive SHA manifest reproducible.

## Next v34 exact gate

Compute a **nonlinear (degree >=2) elimination identity** for this fixed support in the projective Fourier crossratios and evaluate on `zeta_11^(ij)`. A true negative requires a characteristic-zero polynomial certificate covering all exceptional charts. A positive requires all edge weights plus exact matrix equality, all operations/constant preparation charged, and an all-length generalization. Random optimizer failure and generic dimension deficiency do not decide a single special Fourier point.
