# Independent adversarial review: leading-c family

Date: 20 October 2026 UTC.
Verdict: **ACCEPTED within the exact scope n=c p^r, p odd prime, r>=2, s>r, 1<=c<p, q primitive of order p^s.**

The completed frozen author package is author.

- REPORT.md SHA-256: `012c2bdcf24d01c15641c938ac7b240c078ed8089e46fd9d0ebe0e34069092a6`.
- MANIFEST.json SHA-256 and package seal: `9159078187512872a2e297b0ae0b53493d3b8ddcb39f891561d5190e2f0282cb`.
- All 10 manifest-listed files were independently checked for byte length and SHA-256. The manifest seal matches SEAL.sha256.

I reviewed the complete manuscript against independently derived calculations and requested no mathematical revision. No essential lemma or derivational help was supplied to the author. The final verdict binds only these exact frozen bytes. Source files and accepted baseline files were not changed; no external state was changed.

## Scope checked independently

The accepted range is p odd prime, r >= 2, s > r, 1 <= c < p, N = p^r, n = cN, and q a characteristic-zero primitive p^s-th root, with v(q-1) = 1. The proven derivative valuation is

D_c = (c+1)N/2 + cB - p,
B = r(p-1)p^(r-1)/2.

This is not an arbitrary-degree statement. No leading-digit-c theorem with c >= p, no intermediate-digit extension, no arbitrary odd-composite order, and no global F020 closure follows.

## Independent derivation checks

The half-W cap for the accepted leading-two family extends to every m < pN without a new inequality. Both W and its capped tail R are digit-linear on that interval. Their difference W(m)/2 - R(m) has a strictly positive contribution from every digit below position r and a zero contribution at position r. Thus equality occurs exactly at m = dN, for 0 <= d < p. This is an unlimited digit calculation, not an inference from finite checks.

The complement identity is valid with endpoint cN-1 because every relevant divisor p^b divides cN. At the last index the uncapped edge weight is N, not cN. Consequently

R(cN-1) = cW(N)/2 - N + rho.

For every 1 <= u <= floor(cN/2), superadditivity applied to u,u,cN-2u gives

W(u) - R(2u-1) <= N-rho.

Together with the strict consecutive-string cap estimate this compares every nonmonic Newton term to the monic term outside the proposed disks. It works for both parities and includes the even constant term. The beta disks are disjoint because rho lies strictly between beta/p and beta; classes modulo beta identify equal disks. This proves a full cover without root simplicity or root-count assumptions.

The polynomial terms attaining minimal coefficientwise weight cW(N)/2 are exactly k=dN with 0 <= d <= c and d congruent to c modulo 2. Their other superadditive equalities hold because the relevant leading digits are below p and doubling creates no carries. All other Newton terms are strictly higher.

For the original ordinary derivative put j=k-m, a=(cN-k)/2. Its bracket is bounded by

W(a)+R(m)+p^ord_p(j)
 <= W(cN-j)/2+p^ord_p(j)
 = (cW(N)-N)/2 + p^ord_p(j)-W(j-1)/2.

The last score has unique maximizer j=p^2, by the successive differences of the pure-power scores; its maximum is p. Equality in half-W forces m=dN. Parity then forces d congruent to c-1 modulo 2, and m<cN gives 0 <= d <= c-1. Every such pair (k,m)=(dN+p^2,dN) really attains equality. The no-carry calculation uses

a = ((c-d-1)/2)N + (N-p^2)/2.

Thus the derivative now has several tied pivots, not a single pivot; the tied unit sum must be proved nonzero on the polynomial residual locus. Its common weight is exactly D_c.

## Phase and block units

With t=q-1, the leading unit of 1-q^j at its true valuation p^ord_p(j) is -j/p^ord_p(j) modulo p, for 1 <= j < p^s. This statement follows either from the intermediate root q^(p^b) or from the first surviving binomial coefficient. It remains valid above the ramification threshold for the resulting products; no characteristic-p truncation of the entire field is used.

If U(m) denotes the product of these edge units, complete N-blocks give

U(dN) = d! U(N)^d, 0 <= d < p.

Every nonendpoint edge in a block has the same leading unit as in the first block; the endpoint of block l contributes the additional factor l. The factor d! is indispensable.

The even-step factorial has unit 2^a U(a). For t0 < p and a0=(N-p^2)/2,

unit((q^2;q^2)_(t0 N+a0))
 = 2^t0 t0! U(N)^t0 unit((q^2;q^2)_a0).

The residual factor 2^t0 uses Frobenius 2^N=2 in F_p. In the partial block, 2l<N for 1 <= l <= a0, so translation by 2t0N does not alter its edge units. The precise range t0 arising in the proof is safely below p.

On any rho-disk, every length-N Newton block has the same Gauss residual as the first length-N block. Translation of its index by N changes each center by valuation at least N>rho. Therefore N_(dN) and N_N^d have equal normalized leading residuals, not merely equal valuations.

Adjoin omega with omega^2=w_N and put Z=N_N/omega. The surviving original H terms consequently give the polynomial

M_c(Z) = c! sum_(0 <= t0 <= floor(c/2)) Z^(c-2t0)/(2^t0 t0! (c-2t0)!).

There is no alternating sign: the even-step factors give positive powers 2^t0 in the denominator. The ordinary-derivative pivots, when normalized by L_N omega^(c-1), give exactly c M_(c-1)(Z), with

L_N=w_N/[(1-q^(p^2))(q^2;q^2)_((N-p^2)/2)].

The factor z^(p^2-1) has residue +1. The omega choice is harmless: changing its sign changes the normalizations and Z by the matching parity signs.

## Separability and use of the ordinary derivative

For c<p, all factorial denominators exist in the residue field. The exact polynomial identities

M_c'(Z)=cM_(c-1)(Z),
M_c(Z)=Z M_(c-1)(Z)+(c-1)M_(c-2)(Z)

imply gcd(M_c,M_(c-1))=1 by descending to M_0=1. Hence M_c is separable in Z. This is not the claim that the translated polynomial in Y is separable: Z has residual u_a Y^(N/beta), so the translated H residual has Frobenius multiplicities N/beta. The actual ordinary derivative has been evaluated separately in characteristic zero and normalized at its own true valuation. Its residual is nonzero at every residual root of H precisely by the coprimality just proved.

For odd c, M_c has the root Z=0 and the corresponding strict-interior roots must not be excluded. M_(c-1)(0) is a nonzero unit. For even c, M_c(0) is a nonzero unit, so every root is on its disk boundary. The leading degree cN/beta of the integral normalized polynomial gives exactly that many roots in each disk, counting multiplicity before the ordinary-derivative argument. This root count is valid despite the repeated residual.

## Original P and kernel checks

The original identity H_n(v^2)=v^n P_n(v+v^-1) is exact. Since H roots reduce to -1 and P roots reduce to zero, choose the branch v near i. Both coordinate derivatives 2v and 1-v^-2 are units, and the identity is differentiated in characteristic zero before restricting to roots. The term containing P_n then vanishes exactly. Thus ordinary-derivative valuations, not merely multiplicities, transfer with unit factors. No claim about the P derivative away from roots is required.

Both original polynomials are monic, so their discriminants have valuation nD_c. The original recurrence has no zero edge below n, making adjacent P polynomials coprime. The ordinary diagonal CD identity at a P_n root is the product P_n' P_(n-1) divided by w_(n-1), so its algebraic-square kernel is nonzero. No positivity or absolute-value square argument is involved.

## Independence

I read the previously accepted leading-two author report and its independent audit as context. The new checker does not import the new author checker or the prior audit checker. Actual-field checks are constructed from the Gaussian Pascal recursion in the full cyclic group algebra, then reduced modulo Phi_(p^s) only when valuations and units are extracted. The original H/P coordinate and ordinary CD identities are checked separately from the original recurrence over exact rational q.

No derivational lemma has been sent to the author. The author supplied the intended scope and corrected an early, unfrozen derivative-value transcription before the audit. Only testing progress has been sent back. The completed frozen manuscript was then compared in full, every manifest entry was verified, and no mathematical revision was requested or needed. The independent controls completed successfully before this verdict was sealed.


## Independent finite controls and manuscript disposition

The unlimited theorem rests on the verified mathematical arguments, not on finite searches. The exact controls are additional falsification and transcription checks.

- Integer and block-phase controls cover 136 parameter rows across 22 (p,r) choices: p=3 through r=9, p=5 through r=6, p=7 through r=5, p=11 through r=4, plus (17,3) and (31,2). Every leading digit c<p is included. Every relevant m, cover index, and one-variable derivative index in those ranges is checked, not sampled.
- Forty-three rows exhaust the complete ordinary-derivative double sum, totaling 5,123,633 pairs. The complete equality set is checked, not just the proposed winners.
- Exact Hermite recurrence, ordinary derivative, and coprimality controls cover all 346 values of c<p across 13 primes up to p=101.
- Sixty exact rational q/degree pairs, q=2,-2,2/3 and degrees 1 through 20, verify the both-parity Newton identity, the original ordinary derivative identity, the original H/P Laurent coordinate identity, and the full ordinary algebraic-square diagonal CD identity.
- Fourteen actual cyclotomic parameter cases cover 48 translated centers: (p,r,s)=(3,2,3) with c=1,2; (5,2,3) with c=1,2,3,4; (7,2,3) with c=3,4,5,6; (5,3,4) with c=3,4; and (3,4,5) with c=1,2. Every surviving polynomial and ordinary-derivative coefficient unit agrees with the independently computed factorial/block products.
- Twenty-nine of those actual-center tests have D_c>e=v(p). The additional odd-r cases (p,r,s,c)=(5,3,4,3) and (5,3,4,4) give D_c=695 and 1815/2, respectively, with e=500, at centers 0 and 1.
- A separate check constructs polynomials from the actual-field residual coefficient lists, not predicted Hermites. All 48 actual polynomial/ordinary-derivative pairs have gcd degree zero. Their leading degrees and smallest nonzero degrees give exactly the asserted total and strict-interior multiplicities.

The actual-field arithmetic is deliberately different from the author's reduced-ring recurrence: Gaussian coefficients are built by the Pascal recursion in the full cyclic group algebra. Canonical Phi reduction is followed by conversion to the t=q-1 basis of degree less than e. Exact weights j+e ord_p(coefficient) have distinct residues modulo e, so their minimum is exact. The unit of an integer p-power is included through p/t^e reducing to -1, including the integer multipliers from ordinary differentiation. There is no floating root computation and no characteristic-p field truncation at or above e.

The accepted leading-two source and its accepted audit also had their entire manifests and seals independently verified as context. Their hashes are retained in BASELINE_BINDINGS.json. The general source is bound in SOURCE_BINDING.json. No new author-checker functions were imported into the independent scripts.

No mathematical defect was found. The frozen proof closes the full single-leading-digit gate under its stated prime-power assumptions, including every inner root when c is odd, exact original ordinary derivative values, both original discriminants, and the original algebraic-square kernel. It does not accept arbitrary intermediate digits, arbitrary degrees below p^s, arbitrary odd-composite orders, or global F020/F023 closure.
