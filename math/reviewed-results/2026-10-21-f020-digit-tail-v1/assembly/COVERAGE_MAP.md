# F020 one leading digit and short tail coverage assembly

21 October 2026 UTC. Assembly of existing accepted results only. This map claims no new theorem, proof, historical priority, public-package acceptance, or external publication. The assembled map itself is submitted for separate verification.

## Conclusion and exact common scope

The accepted source scopes exhaust

    n = c p^r + d,
    p an odd prime, r >= 2, s > r,
    1 <= c < p, 0 <= d < p,
    q any characteristic-zero primitive p^s-th root.

Throughout, P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1), H_n(z)=sum_k [n choose k]_q z^k, and w_j=product_(u=1)^j(1-q^u), w_0=1. Every original P_n and H_n is squarefree, and at every P_n root xi the original algebraic-square kernel sum_(j=0)^(n-1)P_j(xi)^2/w_j is nonzero. No mathematical exception remains inside this parameter rectangle. This is a union of accepted statements, not a new proof of them.

The only nonzero base-p positions allowed are r and possibly 0. Since (p-1)p^r+p-1 < p^(r+1) <= p^s, all required recurrence edges and CD denominators are nonzero, including the simultaneous upper endpoints c=d=p-1. Neither arbitrary intermediate digits nor arbitrary n<p^s follows.

## Seven disjoint branches

The source IDs below refer to exact identities in SOURCE_IDENTITIES.json.

1. Z: d=0, every 1<=c<p. The complete single-leading-digit theorem was accepted on 20 October 2026. ALL zero-tail credit is inherited, including even c>=4 and odd c>=3. Later zero-tail assemblies add no theorem credit.
2. L1O: c=1 and odd 1<=d<p. Already accepted on 20 October as the historical even-degree low-digit family. The word even describes total degree, not the tail. Its separate fresh final review, not the concurrent exploratory review, is the accepting authority.
3. L1E: c=1 and even 2<=d<p. Already accepted on 20 October as the historical odd-degree low-digit family. That source also includes d=0, assigned exclusively to Z here to keep the map disjoint.
4. ELO: even 2<=c<p and odd 1<=d<p. The accepted every-even-leading/every-odd-tail theorem covers this branch. The general d=1 and c=2 odd-tail results are inherited. Relative to those supplied predecessors, the source's added sector was even c>=4 and odd d>=3.
5. ELE: even 2<=c<p and even 2<=d<p. The accepted every-even-leading/every-positive-even-tail theorem covers this branch, including c=d=p-1. All c=2 even tails and c=4,d=2 are inherited. The source's added range relative to those predecessors was even c>=4 and even d>=2 except (c,d)=(4,2).
6. OLO: odd 3<=c<p and odd 1<=d<p. The accepted odd-leading/odd-tail theorem covers this branch. Its d=1 result is inherited, not newly credited; its added sector was odd c>=3 and odd d>=3.
7. OLE: odd 3<=c<p and even 2<=d<p. The newly accepted odd-leading/even-tail theorem covers this branch. The d=2 result is inherited; its added sector was odd c>=3 and even d>=4. This acceptance is bound to author manifest b8784a006cd2fcf162ad6f425f8bae1ea5fe033014368227ac22917964d8d3cf and review manifest 1401e4a95c0f8983953fe93b041a071b6e26d441d5db10da4999b8f0ba862ba7.

Exhaustiveness does not depend on a numerical grid: first split d=0 from d>0; in the latter case split c=1, c even, and c odd>=3; then split the tail parity. Those alternatives are mutually exclusive and exhaustive for every odd p. Overlapping specializations are not counted as extra degree families or credited again.

## Root and valuation regimes must remain separate

In an algebraic p-adic embedding put v(q-1)=1, N=p^r, B=r(p-1)p^(r-1)/2, h=floor(r/2), beta=p^h, and L=N/beta. In particular beta is NOT p^ceil(r/2). For later leading-digit rho disks, rho=beta/2 for even r and rho=p^(h-1)(2p-1)/2 for odd r. The geometric centers are x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta, with i^2=-1 and square roots near 1. Counts are established with multiplicity before the accepting source proves simplicity.

- Z has cL roots in each rho disk and ordinary derivative value D_c=(c+1)N/2+cB-p at every root. Even c has only boundary roots. Odd c has (c-1)L boundary and L strict-interior roots per disk. Exact deeper interior geometry is not supplied by this theorem.
- L1E has d=2m shallow roots of X-value 1/2 and N inner roots in closed BETA-radius disks, with derivative values (n-1)/2 and D_1+m respectively. There is a simple exact zero among the N inner roots. Its finer beta cover is historical leading-one data, not a cL-per-rho-disk assertion for positive tails.
- L1O has d=2m+1, d-1 shallow roots and N+1 inner roots. Its inner cover has radius alpha=beta-1 for even r and alpha=beta for odd r. Shallow derivative value is (n-1)/2. At an inner root with x=v(X), the value is m+x+min(D_1,N+B-2x). The source excludes x=p/2 and includes split inner clusters. There is no zero root. Do not replace this geometry with the later cL rho-disk geometry.
- ELE has d shallow roots plus cN high roots. Every rho disk has cL high roots, all on the boundary. High derivative value is D_c+d/2; shallow value is (n-1)/2. There is no zero root.
- ELO has one simple exact zero, d-1 shallow roots, and cN high boundary roots, cL in each rho disk. The central disk also contains that exact zero. The zero derivative value is K+m, with K=cN/2+cB and d=2m+1. Noncentral or r>=3 high-root derivative values are m+x+min(D_c,N+E-2x), E=(c-1)N/2+cB. The r=2 central boundary classes require the source's separate ordinary-derivative correction analysis. At p>=5, affected roots above R_c(-alpha)=0 mod p gain correction order 1, or 2 when p divides 2d+1; both cases are resolved. The p=3 case is inherited separately as described below.
- OLO has d-1 shallow roots and cN+1 high roots, with no zero root. Each noncentral rho disk has cL roots, (c-1)L boundary and L interior; the central disk has cL+1, with (c-1)L boundary and L+1 interior. At r=2 its p+1 central interior roots have X-value p^2/(p+1). Ordinary derivative values depend on x and the resolved central boundary correction class; they are not constant across all high roots. The exact source formulas, including both correction orders, remain attached to OLO, not generalized to L1O or OLE.
- OLE has d shallow roots plus cN high roots, cL per rho disk with (c-1)L boundary and L interior. The L central interior roots contain one simple exact zero and L-1 nonzero roots. High derivative value is D_c+d/2; shallow value is (n-1)/2. Individual deeper nonzero interior values are not asserted. All r=2 and prime-boundary cases in this branch are accepted without an exception.

The common conclusion is simplicity and original-kernel nonvanishing. There is no single all-root derivative, kernel-valuation, discriminant, or disk-radius formula asserted for the entire seven-branch union. Original characteristic-zero ordinary derivatives are taken before reduction; repeated residuals are not differentiated as a substitute. The identity H_n(v0^2)=v0^n P_n(v0+v0^(-1)) transfers multiplicity and root-derivative valuations on the unramified branch near i, but does not identify normalized P and H units. Exact P zero maps to H root -1; H_n(0)=1.

## Boundary checks

- At p=3, c is 1 or 2 and d is 0,1,2. These six pairs are exactly Z for both c, L1O at (1,1), L1E at (1,2), ELO at (2,1), and ELE at (2,2). No odd-c>=3 branch is needed. No r=2 endpoint is missing.
- The historical p=3,r=2,d=1 leading-one adverse control at s=3 is P_10 with Newton hull (0,15),(4,6),(10,0): four central roots of X-value 9/4, not a pair of value 3/2. It illustrates why L1O must retain its separate complete root cover. The theorem itself holds for every s>2.
- At p=3,c=2,d=1,r=2, ELO invokes the separately accepted original P_19 completion; its central derivative value is 76/3 for every s>2. The p>=5 scalar correction formula is not applied at p=3.
- Odd c>=3 requires p>=5. The OLE endpoint p=5,c=3,d=4,r=2 is accepted. OLO includes the simultaneous first-layer/first-correction cancellation p=7,c=3,d=3; it is resolved, not an open or nonsimple case.
- c=p-1 belongs to the even-leading branches; d=p-1 belongs to the positive-even-tail branches. The largest odd c is p-2 and largest odd d is p-2. All are covered at r=2 as well as r>=3, and at s=r+1 as well as larger s.

## Recovered leading-one acceptance and publication evidence

The intact accepted comparison archive is SHA-256 c86929554da6cba650c0eb13ede9384e1515cfd220522983e0031e39331aa5fe, with root manifest 952a6175b389b582ab4ae28491a380fa9cc8d699a45f8af0f2ea9b9240241bf8. The historical accepted-theorem/leading-two/even-low-digit chain retains L1O, and its nested odd-low-digit retains L1E. Both proof reports, fresh accepting reviews, verdicts, and original author/review manifests are byte-exact in that archive. SOURCE_IDENTITIES.json records them separately from the projected Z identities.

The repository's immutable 20 October publication at commit f2b7a52c383e93307f3ea2162cf959bd486c3e1d already includes both sources:

- Odd d, even total degree: https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-even/PROOF.md
- Fresh accepting odd-d review: https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-even/REVIEW.md
- Even d, odd total degree: https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-odd/PROOF.md
- Accepting even-d review: https://github.com/AgentSlop-Si/research/blob/f2b7a52c383e93307f3ea2162cf959bd486c3e1d/math/reviewed-results/2026-10-20-f020/low-odd/REVIEW.md

The retained publication receipt records exact remote text readback for all six low-even/low-odd proof, review, and verdict files. Its release ZIP has only blob identity and size verification, not complete remote raw-byte readback; this map does not upgrade that limitation. No fresh network read or external write was made here.

The historical table-capture paragraph is omitted from this public reading copy. It was corroborating history only, not mathematical proof authority or a current live-table observation.

## Remaining exclusions and work

There is no missing mathematical proof obligation inside the stated one-leading-digit-plus-short-tail rectangle. The needed work here is assembly verification and any separately authorized delivery or table reconciliation, not a new c=1 theorem. This does not close F020/F023 globally, revise its status or priority, settle arbitrary intermediate digits or arbitrary degrees, p=2, r<2, s<=r, composite phase orders, unrelated finite characteristics, historical originality, or FFT/algorithmic cost. Excluded sectors are not thereby declared false or unresolved by every other source. Existing local/all-A hypotheses and separately accepted broader results are unchanged.

No source file was modified. No supplied mathematical program or accepted control suite was executed. The checks performed here are read-only byte hashing, JSON/ZIP inventory inspection, and direct reading of accepted statements and verdicts. Separate verification is required for this exact assembled map; the existing source acceptances remain their original acceptances.
