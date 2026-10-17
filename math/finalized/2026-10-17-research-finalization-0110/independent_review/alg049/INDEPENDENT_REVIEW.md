# Independent acceptance: ALG-049 nonuniform Möbius cut-rank gate

17 October 2026. **ACCEPT at the stated fixed-prefix scope.** ALG-049 remains TO RESEARCH at priority 42. No novelty, speed, whole-parent closure or unrestricted Fourier lower bound is established.

## Mathematical review

The prefix is exactly the previously accepted N=8 pair, with no first-boundary separator. I independently reconstructed its integer Laurent matrices from the two cycle edge lists. The identities K(M)=(3I+M+...+M^7)/2 and K(M)^-1=(129I-64M-...-M^7)/257 follow from M^8=-I and were checked in both inverse orders. Thus the Gram matrices are bound to the actual prefix, rather than abstract certificate polynomials.

For every sign pair and each of the twenty balanced cuts containing coordinate 0 and excluding coordinate 1, all stored minors were reconstructed independently. The final certificate contains 160 monic minor identities and 80 exact two-term rational-polynomial Bézout identities. All pass. Its SHA-256 is fc0c7c1236f239d9e1271f68b00b5a372ae73e40f57b03b34fa33f2322114009. The formal Laurent conclusion holds for every nonzero z; identification with the Hermitian physical Gram requires |z|=1, as the report correctly states. Eighty deliberately corrupted witness identities were rejected. Independent reverse-triangle checks additionally certify 71 of the 80 cuts directly; the Bézout argument covers all 80 without numerical phase sampling.

The Möbius cross-rank lemma is valid. For nonzero a and b, principal restrictions of the weighted cycle to proper contiguous intervals are nilpotent paths, so the needed diagonal blocks of aI+bQ are invertible. Block inversion and the affine resolvent decomposition bound each cross block of C^-1 by rank one. The separately stated b=0 and a=0 cases are correct; the latter legitimately forces Q invertible before Q^-1 is used. Zero edge weights and proportional coefficient pairs are covered. Singular numerators already fail the nonzero scalar-unitary target by rank.

The cross block of (C^-1)*C^-1 is a sum of two rank-one terms, hence has rank at most two on a contiguous cycle cut. Any two marked coordinates admit a length-four cyclic interval containing one and excluding the other. Invertible monomial congruence transports that interval and preserves its block rank. The exact orientation L=t S^-* (C^-1)*C^-1 S^-1 is correct even for nonunitary diagonal amplitudes. It contradicts the rank-at-least-three certificate on the transported separating cut.

Independent rational controls passed 912 legal Möbius instances and 5,472 contiguous cuts, including a=0, b=0, proportional coefficients and zero cycle weights. A higher-degree invertible polynomial control has Gram cross rank four, confirming the degree boundary. These controls support transcription; the proof above supplies the universal claim.

## Scope and disposition

Accept the new exclusion for arbitrary complex nonuniform weighted eight-cycles, legal Möbius numerator/denominator factors, and arbitrary invertible monomial last separators, at the unchanged prefix. This genuinely extends the old deficient-difference-support and constant-diagonal mechanisms. Preserve the earlier results at their own scopes.

Reject any extension to all higher-degree rational factors, every balanced cut, a changed prefix/first boundary, nonmonomial separators, other dimensions, longer words, arbitrary Fourier algorithms, numerical conditioning, implementation speed or historical priority. The report explicitly avoids these extensions. The exact unseparated rank-two countercontrol is important.

The initial construction file retained sixteen zero-weight witness terms; these were removed without changing the mathematics. I rechecked the final 160-minor file. No author program or historical program was executed or imported. Only freshly written reviewer programs ran. No external state was changed. Acceptance of the mathematics does not certify publication or native-table application; those require their own fresh preimage and postimage guards.
