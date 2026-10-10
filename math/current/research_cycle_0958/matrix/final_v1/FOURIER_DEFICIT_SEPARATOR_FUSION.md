# Autocorrelation-deficit Fourier bounds and routed separators

10 October 2026. A supported extension of FUS-03. The Fourier moment, contraction, separator and low-rank approximation tools are classical. This is a new-to-project quantitative synthesis and parameter generalization, with worldwide priority unresolved.

## 1. General finite-abelian-group theorem

Let G be a finite abelian group of order N≥2 and U its complex unitary-normalized character table. Choose r rows R and h columns H, with 1≤r,h≤N. For a nonidentity translation s define

c_H(s)=|H∩(H−s)|,
d_H=h−max_(s≠0)c_H(s).

Thus d_H≥0; it is positive exactly when H has no nontrivial translation stabilizer. Let V=U[R,H], and put

B_H= h(N−r)/N − d_H r(N−r)/N².

Then

rank V ≥ ceil(rh/N + d_H r(N−r)/N²).                         (1)

For every rank-at-most-t approximant W to V with t<h−B_H,

||V−W||_2 ≥ sqrt(1−sqrt(B_H/(h−t))).                        (2)

The analogous transposed estimates using the autocorrelation deficit of R in the dual group also hold; one may take the better of the two bounds. The statement is complex analytic. It does not transfer these positive singular-value bounds to finite fields.

### Proof

Let I be the complement of R in the character set, |I|=n=N−r, and A=U[I,H]^*U[I,H]. Since U is unitary, 0≤A≤I_h and V*V=I_h−A. Write f_I(s)=sum_(χ∈I)χ(s). Expanding the fourth moment gives

tr A²=N^−2 sum_s c_H(s)|f_I(s)|².

Character orthogonality gives sum_s|f_I(s)|²=Nn, and f_I(0)=n. Therefore

tr A² ≤ N^−2 [h n²+(h−d_H)(Nn−n²)]
       = h n/N−d_H r n/N²=B_H.

The nullity of V equals the multiplicity of eigenvalue 1 of A; that multiplicity is at most tr A². Consequently rank V≥h−B_H and integrality gives (1).

Let a_1≥...≥a_h be the eigenvalues of A. Then σ_(t+1)(V)²=1−a_(h−t). Since (h−t)a_(h−t)²≤tr A²≤B_H, the usual rank-t approximation bound gives (2). It is positive exactly under the displayed strict condition. This also covers r=N, where B_H=0 and every singular value of V is one.

## 2. Cardinality-only consequences

If G is a p-group and h is not divisible by p, then d_H≥1: every nonidentity translation has orbit length a positive power of p; a translation-invariant set must be a union of those orbits and so have p-divisible size. More generally gcd(h,N)=1 is sufficient for d_H≥1 in any finite abelian group.

For a square m-by-m block of a p-group character table with p∤m,

rank V ≥ ceil(m²/N+m(N−m)/N²).                             (3)

Thus the previously proved odd-size abelian-2-group statement is one instance, rather than the outer limit of the mechanism. Actual d_H>1 improves it further without requiring a cardinality hypothesis. If d_H=0, the rank statement returns the ordinary flat-unitary stable-rank bound.

For the critical 2-group rectangle r=N/2−1, h=N/2+1 and d_H≥1, the inherited C02 bound and its positive δ_N are recovered exactly. This theorem gives no matching rank-minimizing ordering for noncyclic groups.

## 3. Fusion with independently routed separator inverse sums

Use the F018 model from the second-audit manuscript: r_b branches L_i Q_i^−1 R_i, arbitrary permutation-contained endpoints, and support lifts with marked weighted half-separators of size q. The accepted two-color selection yields a square rectangle of side m after r_b steps, of branch-sum rank at most t=q r_b. It starts with m_0=N, or floor(N/2) on disjoint row/column sets to remove a free diagonal, and uses

m_(j+1)=ceil((m_j−q)/3), provided m_j≥4q.

On the selected Fourier columns, compute d_H and apply (1)–(2). The sets are chosen after the fixed branch architecture is known, so independently routed branches remain covered.

A cardinality-only enhancement is always available for p-group targets: trim the final rectangle to any k≤m with p∤k and apply (3). All previous branch-rank bounds survive restriction. In particular, a 2-group target permits the largest odd k≤m. Use the maximum of this trimmed bound and the untrimmed flat-unitary bound. This avoids silently assuming the selection recurrence returns an odd size. Trimming can weaken the numerical conclusion, so no improved universal asymptotic branch exponent is claimed.

For N=64,m=21, formula (3) gives rank at least 8, whereas ceil(m²/N)=7. The same example was already in FUS-03; the new material is the deficit invariant, asymmetric/general-group theorem, p-group extension and automatic legal-trimming interface.

## 4. Scope and novelty boundary

The unchanged separator cutoff is N≤q r_b 9^(r_b)+q(3^(r_b)−1), or N≤4q r_b 9^(r_b)+2q(3^(r_b)−1)+2 with a free diagonal. Nothing here proves that 9 is optimal, that these thresholds are sharp, or that a fixed nonzero error tolerance forces logarithmically many branches. Absolute gaps under invertible diagonal rescaling are multiplied by the minimum row and column scale magnitudes. Dense preconditioners need not preserve the model.

Delvaux–Van Barel's TW470 and related Kronecker-Fourier work are essential prior art for Fourier low-rank blocks and support uncertainty. The final 2008 full text was still unavailable through the verified publisher/institutional paths in this pass. That comparison remains unresolved; the theorem above is supported by its supplied proof, not by a negative literature search.
