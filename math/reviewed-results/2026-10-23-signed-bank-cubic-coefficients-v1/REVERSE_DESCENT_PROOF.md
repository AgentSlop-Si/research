# Reverse gcd descent for the original deterministic coefficient generator

23 October 2026 UTC. Candidate for independent review. This packet changes only the two coprime-combination routines in the accepted deterministic generator. It retains the original gate, exact coefficient space U, accepted fast axis test, and every root-field and bank obligation. No historical research program is executed and no historical novelty is claimed.

## 1. Result and source boundary

Retain N odd, d >= 4, N >= 8d-10, m=N-d, a coefficient field k containing a primitive Nth root q, char(k) not dividing N, and the ORIGINAL envelope E and U=E-perp from the all-characteristics source. Retain the accepted fast-axis packet and its supplied list of 2N explicitly represented distinct scalars.

Replacing the two forward coprime-combination loops by the reverse gcd-descent algorithm below reduces the COMPLETE deterministic coefficient stage from O(N^4) additions/multiplications and O(N^3) inversions to O(N^3) additions/multiplications and O(N^2) inversions, with O(N^2) live field-element storage. These are schoolbook bounds. All failed trials, basis construction, input/output coefficients, and scalar-list handling are charged. This matches, rather than improves, the pre-existing expected O(N^3) Las Vegas coefficient bound.

This packet does not incorporate the separate later-range composition. The original gate is retained here. It changes neither bank count, splitting fields, actual root recovery, nor warm application. It claims no faster full Fourier/FFT algorithm.

## 2. Exact amortized selection lemma

Let a be a nonzero polynomial of degree v >= 1 and let b_1,...,b_s span a polynomial space W. Suppose gcd(a,b_1,...,b_s)=1 and deg b_j <= L, with L >= v. Assume a supplied represented list of v+2 distinct field elements; removing zero leaves at least v+1 distinct nonzero elements. Then a p in W with gcd(a,p)=1 can be found by schoolbook arithmetic in

    O((s+v)L^2) additions/multiplications,
    O((s+v)L) inversions,
    O(sL+v^2+L) live field-element storage.

The same bounds hold if a given nonzero linear functional phi on W must also satisfy phi(p) != 0. Evaluation of phi by its coefficient vector is charged in O(L) operations per use. The algorithm never factors a, extracts roots, differentiates a, or assumes squarefreeness or perfectness of the field.

### Forward gcd-chain preparation

Normalize a to be monic and set A_0=a. Scan the given basis. For each b_j compute gcd(A_current,b_j). If unchanged, discard this direction from the chain. If it strictly decreases, record the polynomial p_i=b_j and the new monic divisor A_i. Thus

    A_i = gcd(A_(i-1),p_i),
    deg A_i < deg A_(i-1).

Stop once A_ell=1. The hypothesis guarantees termination. There are ell <= v strict decreases, at most s gcd computations in the scan, and no field extension or factorization. Each recorded p_i is an ORIGINAL basis member, not a polynomial multiple of one.

### Reverse unwind

Set P=p_ell. The already computed equality A_ell=gcd(A_(ell-1),p_ell)=1 proves the base case. For i=ell-1,...,1, maintain gcd(A_i,P)=1. Write

    A=A_(i-1), D=A_i, p=p_i,
    Delta=deg A-deg D > 0.

Try the first Delta+1 nonzero scalars lambda from the fixed list, forming the full coefficient vector

    C_lambda = p + lambda P.

Test gcd(A,C_lambda)=1 exactly. Accept the first success and replace P by C_lambda. On completion gcd(a,P)=1 and P remains a scalar linear combination of the given basis, hence is in the SAME W.

### Why only Delta+1 trials are needed, with multiplicities

Let e_lambda=gcd(A,p+lambda P), monic, for nonzero lambda. Since gcd(A,p)=D and gcd(D,P)=1, every irreducible factor of D divides p but not P. Consequently gcd(D,e_lambda)=1 for every nonzero lambda.

For distinct lambda and mu, a common irreducible factor of e_lambda and e_mu would divide their difference (lambda-mu)P, hence P, and would also divide p and A. It would therefore divide D and P, a contradiction. Thus the e_lambda are pairwise coprime, not merely unequal.

For any set of tested distinct nonzero scalars, each e_lambda divides A, all are pairwise coprime, and each is coprime to D. Therefore, WITH THEIR FULL MULTIPLICITIES,

    D product_lambda(e_lambda) divides A.

It follows that sum_lambda deg(e_lambda) <= Delta. Each failed trial has deg(e_lambda)>=1, so at most Delta trials fail. The next distinct nonzero scalar must succeed. This argument is valid over every field and uses irreducible factorization only as a proof device.

The strict degree drops telescope:

    sum_(i=1)^ell (deg A_(i-1)-deg A_i)=v.

The unwind omits the terminal base level. Hence its total number of gcd trials, including successes, is at most

    sum_(i=1)^(ell-1) (Delta_i+1) <= v+ell-1 <= 2v-1.

The exact endpoint of that inequality is deliberately conservative; no decrease is charged more than once. This is the improvement over separately paying v+1 trials for every forward direction.

### Optional nonzero linear functional

First run the unconstrained algorithm above. If phi(P)!=0, return P. Otherwise find a basis member u with phi(u)!=0; one exists by hypothesis and the scan costs O(sL). Set D=gcd(a,u). For nonzero lambda,

    C_lambda=u+lambda P,
    phi(C_lambda)=phi(u)!=0.

Because gcd(a,P)=1, the same argument applies to A=a, p=u, and D=gcd(a,u). At most v-deg D scalar trials fail, so at most v-deg D+1 <= v+1 nonzero trials suffice. This extra single pencil preserves W and the functional exactly; it is not an unproved simultaneous-preservation induction. It also works when a divides u, in which case the first nonzero scalar succeeds.

The fixed list has v+1 nonzero elements even if it contains zero, and therefore supplies every unwind and repair choice. The algorithm checks actual coprimality at every accepted choice.

## 3. Cost proof without fast polynomial primitives

All basis members and constructed combinations have degree <= L. A gcd between a divisor of a and such a polynomial costs O(L^2) additions/multiplications and O(L) inversions by ordinary polynomial long division and Euclid, including reductions when the basis degree exceeds the current modulus degree.

- Forward scan: at most s gcds, O(sL^2) arithmetic and O(sL) inversions.
- Reverse unwind: at most 2v-1 trials, each O(L^2) arithmetic and O(L) inversions. Forming and writing C_lambda costs O(L), separately absorbed.
- Functional repair: one extra gcd, at most v+1 candidate gcds, O(sL) for functional/basis scans, and O(L) per candidate functional evaluation if checked redundantly. This adds O(vL^2+sL) arithmetic and O(vL+L) inversions.
- All comparisons of monic gcds, degree tests, scalar filtering, coefficient reads/writes, and the final output cost no more than these bounds. The original represented input scalar list is not assumed free to create.

The input basis occupies O(sL) field elements. The descending chain has at most v nonconstant/constant records and total stored degrees O(v^2). Two streamed full-length candidates and Euclid buffers use O(L). Store only original basis indices for p_i, not duplicate basis polynomials. No recursion stack copies full linear combinations: unwind iteratively using one current P.

The only borrowed algorithms here are ordinary dense linear algebra, polynomial long division, and classical Euclid, at the explicitly counted schoolbook costs. No half-gcd, FFT multiplication, fast factorization, modular-composition oracle, or unpriced root operation is used. The algorithmic observation is the reverse traversal and degree-drop charge for the failed candidates; no historical originality claim is made.

## 4. Application to the two original pencils

Use the exact spaces and endpoint facts from the accepted original two-pencil theorem:

    V0={g/[t(t-1)] : g in U, g(0)=0}, r=m-2,
    V1={g/(t-1) : g in U}, n=m-1.

They have gcd one. V0 has independent constant and degree-r endpoint functionals. The accepted linear solve supplies f0 in V0 with f0(0)=coefficient_r(f0)=1. For the FIRST combination apply the new lemma with a=f0, W=V0, and

    phi(f)=coefficient_r(f)-f(0).

It returns f1 in V0 with gcd(f0,f1)=1 and phi(f1)!=0, exactly the original first-pencil contract. No change to U, endpoint normalization, or reciprocal witness proof is made. The existing first pencil still requires at most 2r+3=2m-1 scalar trials to produce monic f with f(0)!=0 and gcd(f,rev_r f)=1.

Set h0=t f and W={h in V1: coefficient_n(h)=0}. The accepted decomposition V1=k h0+W still gives gcd(h0,W)=1. For the SECOND combination apply the new lemma with a=h0 and this W, without a functional. It returns h1 in the SAME W and gcd(h0,h1)=1; hence h1(0)!=0. The second pencil remains h_Z=h0+Z h1 and g_Z=(t-1)h_Z, with no coefficient-space substitution.

Both lemma instances have s,L,v=O(N), so together they cost O(N^3) arithmetic, O(N^2) inversions, and O(N^2) storage. Their required lists have v+2 <= N+1 elements, hence are supplied by the SAME 2N-element list already needed by the accepted fast final guard. No extra field-size or positive-characteristic assumption is introduced.

## 5. Complete coefficient-stage ledger

1. Build the exact original E and a basis of U; form V0,V1,W and solve endpoint constraints: O(N^3) additions/multiplications, O(N) dense elimination pivot inversions, O(N^2) storage.
2. The TWO reverse-descent coprime combinations, including functional repair and every failed trial: O(N^3) additions/multiplications, O(N^2) inversions, O(N^2) storage.
3. Original reciprocal pencil, at most 2m-1 scalar tests: O(N^3) additions/multiplications, O(N^2) inversions.
4. Accepted exact reciprocal-gcd axis test and unchanged squarefreeness/nonzero-constant guards on at most 2N final-pencil scalars: O(N^3) additions/multiplications, O(N^2) inversions.
5. Scalar-list filtering, basis/candidate/coefficient reads and writes, output coefficients, and reusable buffers are included. The separate list-construction and representation costs remain explicit.

TOTAL: O(N^3) coefficient-field additions/multiplications, O(N^2) coefficient-field inversions, and O(N^2) live coefficient-field elements. No expected-time assertion replaces the deterministic bound. No historical novelty assertion follows from the asymptotic improvement.

## 6. Unchanged fields, roots, and physical-bank costs

Retain the supplied certified coefficient-field interface and q. In the finite case retain the SAME quadratic field E0=F_(Q^2) with its O(Q^3) base-field setup. Q>=N+1, hence E0 contains the required 2N distinct represented scalars. List writes are O(N) field elements; representation/counter and bit costs remain additional. In characteristic zero the usual integer list works; arbitrary infinite positive-characteristic fields still need the effective distinct-element interface.

Every original post-coefficient ledger entry remains paid: a genuine splitting field, or the same conservative m!-degree finite overfield construction; actual recovery and checking of all distinct nonzero roots; axis and Vandermonde amplitudes; raw weights; every original branch inverse; all output/storage coordinates; and extension arithmetic expanded to base coordinates. The enormous finite overfield recipe is not reduced. With t=m! and R=Q^2 its modulus recipe remains O(t^2 R^(t+floor(t/2))) coefficient-field work and its root scan O(m t^2 R^t).

The subsequent O(N^3) root-field preparation, O(N^2) root-field storage, and the literal warm bank counts remain unchanged. In particular B=2m+2, with 2BN^2 multiplications and 2BN^2-BN-N additions per literal warm application, plus the existing read/write costs. This is not an end-to-end polynomial-time compiler, a smaller-bank theorem, an efficient splitting/root algorithm, or a Fourier/FFT speedup.
