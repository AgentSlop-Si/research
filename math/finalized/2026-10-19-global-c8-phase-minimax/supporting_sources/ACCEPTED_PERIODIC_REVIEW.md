# Independent review: C8 rank-one positive-error partial result

Review date: 18 October 2026 UTC.

## Verdict

**ACCEPT, at the stated partial scope.** The frozen candidate proves:

1. A global upper bound delta_1 <= sin(pi/16), with explicit legal outer phases, real B, and complex rank-one E attaining that error.
2. Equality with sin(pi/16) for the entire continuous sector p[j+4]^2=p[j]^2 and q[k+4]^2=q[k]^2, including every independent real row/column sign choice.
3. An exact 78-real-variable semialgebraic feasibility problem equivalent to a counterexample to the proposed unrestricted lower bound.

**The original unrestricted global continuous-phase minimax remains OPEN.** No global lower certificate, elimination result, or reduction to the periodic sector is accepted. This is a partial mathematical advance and a precise stopping lemma, not closure of the original gate or its broader research owner.

No correction to the frozen mathematical text is required.

## Frozen bytes and execution discipline

The author froze the candidate before this review's replay and independent acceptance. Its authoritative MANIFEST.json has SHA-256:

8076458ad511a6aae8b09586f138ce5e02c004f69dfa61017bae0791a93722e3

All 19 listed files and their byte lengths were verified. The complete candidate, including its manifest, is preserved under frozen/. In particular:

- PROOF.md: e521ac28ce632203d3f86a998964efb2180b42a95cbac1533149f8ebb7d9bd3e
- GLOBAL_PHASE_GAP.md: d4d039e1ac998927f0d66ce9bae4248a0d02f0955fc4e2fb1cbb4013c289beb3
- WITNESS.json: 0167099b5208da554ec3e685e9dfcba5c23c40064f22a266dadcc61685789465

Both fresh candidate checkers were read before execution. Only these two short sibling checkers were replayed, in the separate replay/ copy. Their regenerated WITNESS.json, EXACT_CHECKS.json, and GENERAL_BLOCK_CHECKS.json are byte-identical to the frozen versions. Neither numerical search script was executed. No historical research package was imported or executed; the accepted predecessor was read only as text.

The review's independent_checker.py uses SymPy's algebraic-number implementation, rather than importing or adapting the candidate's arithmetic class. Its exact reconstruction, algebraic controls, and input-integrity checks pass. The original candidate's hashes were checked again after review. All work was local; no external writes, publication, owner changes, or census changes occurred.

## 1. Model and exact upper witness

The fixed-phase identity is valid in the stated operator-norm model. Entrywise imaginary part is a contraction because Im(A)=(A-conjugate(A))/(2i) and conjugation preserves the operator norm. For complex rank-one E, Im(E) has real rank at most two. Conversely every real rank-at-most-two approximation can be realized as the imaginary part of a complex rank-at-most-one matrix using the displayed two-term factorization. Choosing B as the real part of PFQ-E leaves precisely the real rank-two approximation residual multiplied by i. Thus the optimum is min sigma_3(Im(PFQ)). The accepted real-monomial absorption preserves the approximating matrix itself, so arbitrary nonzero monomial magnitudes do not create a conditioning restriction.

The explicit phases, vectors a and b, and formulas

E=c(a+i b)(a+i b)^T,
B=Re(PFQ)-c(aa^T-bb^T)

are correct. The transpose is essential here. The independently reconstructed F, V, B, E, and inner residual agree entry-for-entry with the frozen serialized witness. Exact checks confirm F is normalized negative-sign unitary, B is real, E is nonzero with all 784 two-by-two minors zero, and every entry of the original external residual identity holds.

The spectral identities are also independently verified:

Y^2=s^2 I+(c^2-s^2)R,
Y_0^2=s^2(I-R),
R=aa^T+bb^T.

R is a rank-two orthogonal projector and Y_0 is real symmetric. Therefore the external error is exactly s=sin(pi/16), and Y has singular values c,c,s,s,s,s,s,s. The asserted s and t=s^2 polynomials and rational isolating intervals are correct. These characterize the attained upper value, not an established global optimum.

## 2. Continuous periodic-sector lower theorem

### Complete block and sign coverage

If paired squared phases agree, each pair differs by a real sign. Independent diagonal real sign matrices turn both arrays into literally four-periodic arrays and preserve the singular values of their imaginary parts. This covers all real-sign variants without a branch exclusion. The candidate's paired-index real orthogonal transforms give exactly its four unitary two-by-two blocks; the arbitrary-phase 64-entry identity passes the inspected symbolic checker.

The centered block representation is correct. With the candidate's theta and phi definitions, the two imaginary singular values are |sin(theta+phi)| and |sin(theta-phi)|. One can derive this from

Y_block^T Y_block = (I-Re(C^T C))/2.

The symmetric unitary C^T C has commuting real and imaginary parts, hence a simultaneous real orthogonal diagonalization, with eigenvalues exp(2i(theta+phi)) and exp(2i(theta-phi)). Its trace and determinant are as stated. The exact phase discrepancy theta00+theta11-theta01-theta10=-pi/4 is indispensable and independently checked.

### Good-block counting and both cases

Assume sigma_3<sin(pi/16), and put epsilon=arcsin(sigma_3). At most two of eight singular values exceed sin(epsilon); at least two blocks are therefore good in both directions. Each good block implies |h|>=cos(2epsilon). Adjacent good blocks would force both the sine and cosine of the same row or column difference to have magnitude at least cos(2epsilon), contradicting 2 cos^2(2epsilon)>1. Hence exactly two opposite blocks are good, and each remaining block has at least one small singular value.

The normalization in each opposite case is legitimate: the signs of p2,p3,q2,q3 independently shift R0,R1,S0,S1 by pi. Each chosen cosine or sine can therefore be made positive simultaneously. Arbitrary representatives are then reduced by full periods; no continuous phase restriction is added. The centered-angle discrepancy continues to hold exactly from its definitions.

For Case A, good blocks 00 and 11, write Phi=phi00+phi11. The good conditions imply distance(theta00+theta11, pi Z)<=2epsilon-Phi. The other angles' total deviation from pi/4 is at most Phi, by |arcsin(sin x sin y)|<=min(|x|,|y|) on the stated intervals. Their small singular directions imply

distance(theta01+theta10, (pi/2)Z)<=2epsilon+Phi.

The phase discrepancy simultaneously gives the lower bound pi/4-2epsilon+Phi for the same distance. Thus pi/4<=4epsilon, contradiction.

For Case B, good blocks 01 and 10, the independently checked normalized formulas give the same deviation estimate, with Phi=phi01+phi10. The good and remaining sums exchange roles and the discrepancy changes orientation only; its distance to (pi/2)Z remains pi/4. The identical contradiction follows. This verifies both branches rather than relying on an unstated symmetry.

The proof is a continuous angular inequality, not finite phase enumeration or numerical optimization. Together with the explicit witness it establishes the full stated sector optimum.

## 3. Complete residual semialgebraic formulation

The coefficient field is correctly specified by the isolated smallest positive root t=sin^2(pi/16). The identity sqrt(2)=16t^2-16t+2 holds exactly, and the specified embedding makes this expression positive. The Fourier cosine/sine table and the negative-sign formula for Y are correct, including the normalization r/4=1/sqrt(8).

Fixing q0=1 loses no matrices: multiplying P by the original q0 and Q by its conjugate preserves PFQ. The count is exactly 16 row-phase coordinates, 14 remaining column-phase coordinates, and 48 frame coordinates, for 78 real variables. There are 15 circle equations and 21 independent symmetric frame equations, giving 36 equations.

With H=Y^T Y and eigenvalues lambda1>=...>=lambda8, the six-dimensional min-max identity is

lambda3 = min_{T^T T=I6} lambda_max(T^T H T).

Consequently there is an orthonormal 8-by-6 frame with t I6-T^T H T positive definite exactly when sigma_3(Y)<sqrt(t). The six leading principal minors express positive definiteness by Sylvester's criterion. Strict positivity is essential; exact synthetic below/at/above-threshold controls confirm this distinction. No auxiliary variables are needed for the determinant expressions. Y has variable degree at most two, the compressed Gram matrix at most six, and its leading l-by-l determinant at most 6l, hence at most 36.

The nonnegative Np+Nq is precisely the sum of squared real and imaginary differences of paired squared phases. Its zero set is exactly the sector already proved. The strict guard removes only points that the sector theorem already excludes from any counterexample. Therefore the guarded system remains equivalent to a global counterexample. This formulation does not assert that the system is empty.

## 4. Independent controls and limitations

The independent exact checks additionally reject four separate mistakes: replacing the rank-one transpose by an adjoint, omitting the global z phase, dropping the pi/4 phase discrepancy, and altering the sqrt(2) polynomial. They also check symbolic real-sign covariance, both branch h formulas, root isolation, constraint counts, and all eight semialgebraic Fourier-entry formulas. These checks support the analytic review; they are not substitutes for the continuous sector proof or an infeasibility certificate for the global set.

The prior exact-rank equality argument does not force periodicity at positive error. The new witness has ||Y||_F^2=2+4 sin^2(pi/16)>2, as stated. No numerical run, positive-rank theorem, or finite control closes that missing step. A global lower certificate or a proven minimizer-reduction theorem is still required.

Accepted status: exact global upper witness and continuous squared-four-periodic sector theorem independently accepted; complete residual formulation accepted; original global gate remains open.
