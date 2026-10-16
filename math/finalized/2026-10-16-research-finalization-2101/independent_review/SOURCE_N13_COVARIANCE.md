# Independent review: N13 free-cross rescaling covariance

14 October 2026 UTC. Verdict: **ACCEPT within the exact transport class stated below.**

The report's rescaling covariance, cyclic guard, product invariant, target-preservation obstruction, and specified arbitrary-c wrap correction are correct. No mathematical repair is needed. This is not a freely varying cross-node nonexistence theorem.

## 1. Source-pinned scope

The reviewed report is `n13_free_cross_covariance_2349/REPORT.md`, SHA-256 `04257ce0fdd9b1573ec6e73e56fdda53fe329ff5c3b30007ae374df418611a37`. Its checker and all four source bindings were inspected as text/data. The fresh independent checker verified every candidate manifest entry and every supplied source binding before testing. No candidate or historical scientific program was executed or imported.

The accepted sixteen-bank allocation supplies nonzero alpha values and at least one bank in each of the four orientations. The classification concerns labeled column scaling with a single common diagonal row multiplier, independently of the amplitude values. It allows initially independent node scales and independent bank/sector amplitude factors. It does not classify arbitrary changes of basis among columns, relabelings combined with support changes, or weight solutions tailored to one particular certificate.

## 2. Field-uniform mathematical audit

At b=0 all G coefficients equal one. At a=0, nonzero diagonal amplitude factors must coincide across every bank. With this common factor removed, rows a=1,2 force every positive-epsilon node scale to p, and every negative-epsilon scale m to satisfy m^12=p and m^11=p^2. Dividing gives m=p^(-1), and substitution gives p^13=1. Thus c=p has exactly the required cyclic guard. At a=0 in every other sector the amplitude factors again coincide.

Conversely, c^13=1 implies c^(epsilon [epsilon a]_13)=c^a for both signs, so the claimed common-row covariance holds, including a=0. Every row is covered by a nonzero G column: choose both signed residues at most six. The corresponding Gaussian binomial is nonzero because all numerator and denominator exponents lie between one and twelve. Hence the row multiplier is determined everywhere.

The coherent cross-node transport is (y,z) -> (c^(-1)y,cz), so yz is invariant. Both new nodes can equal one only if yz=1 and c=y=z^(-1); cyclic transport further requires y^13=1. Because the normalized Fourier coefficient f(a,b) never vanishes, target preservation forces every sector scalar kappa_b=1 at a=0 and c=1 at a=1. Therefore this transport normalizes only nodes that were already one.

The general independent-sign formula in section 4 has the correct residue convention. For the specific noncyclic correction p=c, m=c^(-1), u_b=kappa_b and v_b=kappa_b c^13, the negative contribution acquires c^a on a=1,...,12 but c^13 on a=0. Consequently the stated extra term kappa_b(c^13-1)N_b(0) is exact. The nonzero target rows a=1,2 force kappa_b c=kappa_b c^2=1 and hence c=1, regardless of the wrap term.

This last conclusion applies to that specified sign-adjusted transport. The preceding general equations for arbitrary independent u_b,v_b are necessary equations, not a proof that no specially chosen amplitudes or supports could solve them. The report maintains this distinction.

The forced-window comparison is also exact. At b=1,a=11, independently reconstructed constants are G_++=43, f=46 and f/G_++=6. The rescaled moment minus the pinned moment is 6(y^(-1)-1), which vanishes only at y=1 in every characteristic-53 field. This obstructs insertion of a rescaled certificate into the pinned equations; it does not obstruct freshly solved unpinned equations.

The matrix interpretation agrees: conjugation by T gives alpha -> q^epsilon alpha, preserves original-bank legality, and changes F to TFT^(-1). The cross nodes (10,16) have product one, but the entry (1,0) changes from 1 to 16. Reflection exchanges y and z and does not normalize their values.

## 3. Independent fresh checks

Only the newly authored `check_independent.py` in this review directory was run. It uses the standard library. In particular, its G coefficients are reconstructed from the closed Gaussian-binomial product rather than the candidate's recurrence.

The receipt `CHECK_RESULT.json` records:

- Every candidate manifest hash and all four source hashes verified.
- Complete thirteen-row compatibility tested for all 52^2 prime-field scale pairs, yielding precisely thirteen reciprocal thirteenth-root pairs.
- All 2,808 nonzero elements of F_53[u]/(u^2-2) tested; Euler's criterion independently verifies this is a field. Exactly thirteen coherent cyclic scalings occur, all in the prime field; only one fixes the target.
- 36,504 arbitrary-c wrap identities checked with genuinely extension-valued synthetic positive and negative contributions.
- The forced-window residual tested at all 2,808 nonzero quadratic-extension nodes; its only zero is y=1.
- 456,976 full G-column covariance identities checked over all four orientations, all 52 nonzero prime-field alpha values, all thirteen cyclic scales and all 169 rows.
- All 169 raw Fourier Weyl coefficients independently extracted, giving gamma=7 and the stated normalized target.
- Exactly 156 matrix entries change under the explicit q-scaling conjugation.

The extension-field test is a finite sanity check, not the basis of the field-uniform theorem. The algebra in section 2 is what proves the conclusion over every characteristic-53 extension.

## 4. Accepted conclusion and stopping boundary

The proposed lossless normalization by diagonal alpha-rescaling covariance is closed: it cannot reduce arbitrary y,z to one while retaining the specified Fourier target. The canonical arbitrary-c wrap correction does not rescue it.

No independent re-solving of full-sector amplitudes or replacement of supports was performed. The existence or exclusion of freely varying-cross sixteen-bank certificates over degrees 2, 3 and 4 remains unresolved by this artifact. No new minimum-extension-degree, attainment, novelty, or arithmetic-speed result follows from this review.
