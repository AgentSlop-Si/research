# N64 projected-frame obstruction and a necessary inner mixing budget

## Result

For the declared N16-to-N64 nested routes and poles 1/2,...,1/9, no outer eight-Green row-masked layer can produce F64 after a prefix that commutes or anticommutes with the high-x swap. This excludes both signed-symmetry one-inner branches, including the plus-symmetric, seed-mean-preserving 128-variable branch. It is stronger than the earlier rejection for two frozen inner pullbacks.

The obstruction uses only fixed rational Green matrices. Its modular minors are therefore valid characteristic-zero certificates; no numerical center or algebraic seed is specialized modulo a prime.

A separate four-row direct-sum certificate gives a quantitative condition on a genuinely mixing varying inner layer. Each of its two high-x cross-sector blocks must have rank at least two. If its commuting part is invertible, each cross-sector rank must be at least four. These are necessary conditions and do not lower-bound application cost.

## 1. Exact sectors and rational row frames

Let X be the length-64 permutation that shifts an index by 32. Define exact projectors

    Pi_+ = (I+X)/2, Pi_- = (I-X)/2,
    E_sigma = image(Pi_sigma), dim(E_sigma)=32.

The eight fixed route permutations P_j commute with X; in fact P_j^32=X. Their scalar Green matrices G_j=(I-P_j/(j+2))^(-1) therefore commute with X as well. All are rational, with explicit denominators d_j^64-1, d_j=j+2.

For a physical row i and sigma in {+1,-1}, use the 8-by-32 rational projected frame

    V_i^sigma[j,k]=G_j[i,k]+sigma G_j[i,k+32], 0<=k<32.

These are coordinates of the projected row vectors in E_sigma, apart from a common harmless factor. The supplied certificates prove rank(V_i^sigma)=8 for every i<32 and both signs. Rows i+32 follow from commutation with X.

For the minimal row-0 certificate, use columns 0,...,7. Over the verified prime p=998244353 the determinants are

    det(V_0^+[:,0:8]) = 140062647 mod p,
    det(V_0^-[:,0:8]) = 726260818 mod p.

The verifier checks that every d_j and d_j^64-1 is nonzero modulo p, constructs every Green entry, and checks (I-P_j/d_j)G_j=I entrywise. The two actual 8-by-8 modular minors are included in `SECTOR_FRAME_CERTIFICATE.json`. Their nonzero reductions imply their rational determinants are nonzero. This remains true in every characteristic-zero extension, including the accepted seed field.

Consequently no nonzero row of a layer O=sum_j diag(a_j)G_j can be a pure X character. At a fixed row i, a coefficient vector that annihilates either projected sector must vanish because V_i^sigma has full row rank eight. This conclusion does not require every coefficient to be nonzero; it only requires the output row itself to be nonzero.

## 2. Excluding every commuting or anticommuting prefix

Suppose F64=O C, with O in the prescribed eight-Green row-masked family and

    C X=epsilon X C, epsilon=+1 or -1.

If C is singular, the equality is impossible because F64 is invertible. Otherwise C^(-1) has the same signed covariance. The zeroth Fourier row f_0 is the nonzero all-ones row and satisfies f_0 X=f_0. Hence

    row_0(O)=f_0 C^(-1),
    row_0(O) X=epsilon row_0(O).

For epsilon=+1, its minus-sector projection must vanish, contradicting the rank-eight minus frame. For epsilon=-1, its plus-sector projection must vanish, contradicting the rank-eight plus frame. Thus no such factorization exists.

Equivalently, right multiplication by an invertible commuting prefix restricts to invertible maps on E_+ and E_-, preserving each projected frame rank. An invertible anticommuting prefix exchanges the sectors by invertible maps, again preserving their ranks. Fourier rows are pure characters, while every nonzero available outer row has both characters. This is the target-specific obstruction that prevents the proposed paired rank-six gates from ever succeeding for the actual fixed frames.

In the one-inner problems, the remaining fixed bank/inner factors commute with X. If the varying inner layer has XL=epsilon LX, then the whole inner prefix has that same signed covariance. Both signed branches are therefore excluded, regardless of seed means or which inner position varies. The earlier rank-six reduction remains algebraically correct, but its solution set is now certified empty for these fixed routes and poles.

The unrestricted 512-variable varying-inner family can mix the sectors and is not excluded. Neither is the full 1536-variable three-layer family.

## 3. Four-row direct sums

The stronger rank budget uses these exact row sets:

- Plus sector, odd rows I_+={7,3,13,27}: stacking the four V_i^+ frames gives a 32-by-32 determinant 871168069 modulo p.
- Minus sector, even rows I_-={12,4,26,8}: stacking the four V_i^- frames gives a 32-by-32 determinant 682055007 modulo p.

Both stacked matrices are included in the certificate and independently regenerated. Therefore the four eight-dimensional row spaces in each case form a direct sum over characteristic zero.

For any outer layer O that could occur in a successful Fourier product, every output row is nonzero. Its coefficient vector is therefore nonzero, and full projected-frame rank makes each selected projected row nonzero. One nonzero vector chosen from each of four direct-sum spaces is linearly independent. Thus

    rank(O[I_sigma,:] Pi_sigma)=4.

The selected rows have parity opposite sigma. Their Fourier target rows vanish on E_sigma. These exact parity choices are essential.

## 4. The rank/nullity tradeoff

Consider either one-inner problem, after absorbing the commuting fixed factors:

    O' L R'=F64,

where R' commutes with X and is invertible in any successful product. In the input-variable case O'=O K with K commuting and invertible; in the middle-variable case O'=O. Multiplication by K is invertible within each sector, so the four-row direct-sum conclusion for O' is unchanged.

Write the varying inner L in X-character blocks, with

    L_(rho,sigma)=Pi_rho L|E_sigma.

Right-preconditioning the Fourier target by R'^(-1) preserves its pure-character rows. For rows I_sigma, the target has zero E_sigma component. Therefore

    O'[I_sigma,:] Pi_sigma L_(sigma,sigma)
      = -O'[I_sigma,:] Pi_(-sigma) L_(-sigma,sigma).

The first left factor has rank four. Rank subadditivity under multiplication gives

    rank(L_(-sigma,sigma))
      + nullity(L_(sigma,sigma)) >= 4.                 (1)

This holds for both signs and does not assume either diagonal block is invertible.

Every successful L is invertible. If x belongs to ker L_(sigma,sigma), its image under L lies wholly in the opposite sector; the cross block must act injectively on that kernel. Hence

    rank(L_(-sigma,sigma)) >= nullity(L_(sigma,sigma)). (2)

Combining (1) and (2) gives the unconditional bounds

    rank L_(+,-) >= 2, rank L_(-,+) >= 2.

If both diagonal blocks are invertible, (1) strengthens these to rank at least four in each direction. In particular, this stronger case applies when a candidate changes only high-x-odd masks while keeping the commuting part equal to one of the certified invertible frozen inner pullbacks.

## 5. Coefficient mixing count and cost scope

Define the high-x-odd part

    L_odd=(L-X L X)/2.

Its two cross-sector blocks occupy disjoint domain and codomain sectors, so

    rank L_odd = rank L_(+,-)+rank L_(-,+).

Thus every successful one-inner lift needs rank L_odd>=4, and rank L_odd>=8 when its commuting part is invertible.

Since each G_j commutes with X,

    L_odd=sum_j diag(a_j,odd)G_j,
    a_j,odd[i]=(a_j[i]-a_j[i+32])/2.

One unequal high-x coefficient pair contributes two nonzero entries to this diagonal. Each G_j is invertible. Rank subadditivity therefore yields

    rank L_odd <= 2 sum_j #{i<32 : a_j[i]!=a_j[i+32]}.

At least two unequal pairs across the eight inner masks are necessary in general, or at least four when the commuting part stays invertible. These counts include term multiplicities. They do not assert sufficiency or a uniform construction.

High-rank diagonal masks and their Green scans remain O(N) to apply. None of these rank conditions is a superlinear operation lower bound. A next constructive branch must use genuine mixtures of high-x-even and high-x-odd coefficients; merely commuting, anticommuting, or preserving only high-y character freedom has been excluded here.

## 6. Bounded controls and preservation

`check_sector_obstruction.py` verifies primality, fixed inverse guards, all eight cycles, P_j^32=X, all Green inverse entries, 64 projected-frame minors, and both four-row direct-sum minors. The determinant search was bounded and stopped once the displayed row sets were found; the final verifier uses only those fixed witnesses.

All arithmetic concerns fixed rational operators. No solver is run and no uploaded source is executed. Earlier seed, outer-only, and row-membership packages remain unchanged. This additive result closes the proposed signed-symmetry branch before any nonlinear search; genuine mixing remains the open constructive direction.
