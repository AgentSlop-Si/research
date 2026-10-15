# Q29 fixed-instance full-polynomial aggregate acceptance

14 October 2026 UTC.

## Verdict and exact scope

**ACCEPT the full fixed instance t=27, p=5, e=3 in the source-bound primitive
component q=alpha(1+pi).** The previously conditional aggregate implication is
now discharged by the immutable all-27-primary-factor acceptance.

In the complete DVR A described below, with v_pi(pi)=1, the monic polynomials
have exact ordinary discriminant valuations

    v_pi Disc U1687 = 127737,  deg U1687 = 1686,
    v_pi Disc R843  =  63831,  deg R843  = 843.

Both polynomials are squarefree over the characteristic-zero coefficient
field. Their discriminants divided by the displayed powers of pi are units;
their unnormalized discriminants are not units. The source polynomial
H1687=(z+1)U1687 is also squarefree, and its ordinary discriminant valuation
is127887. This last assertion is a direct fixed-instance corollary.

There is no remaining mathematical gate for these fixed-instance conclusions.
Uniform Q29, other t,p,e, and all-layer/algorithmic support claims are outside
this acceptance. The broader parent's open status and priority54 are preserved.
This review makes no external write and supplies no publication-execution
approval or performance improvement claim.

## 1. Accepted evidence and independence

The structural proof was sealed before the batch completed:

- `CONDITIONAL_AGGREGATE_REVIEW.md`, SHA256
  `ffbd467499b2a140954e97ee1841eef203f57522dab54ee90e074a8c0b5f6487`;
- `REMAINDER_CERTIFICATE.json`, SHA256
  `22c59b1c4add215740da1f073b8a0bd718ab4a93d36bc89a802ef12117d04c47`;
- `CONDITIONAL_MANIFEST.json`, SHA256
  `0ee611c835a492cc42dfaacdb689cb06bbe756d0affe1c6476b4b8c8bd6b90a2`.

Those bytes remain unchanged. The certificate reconstructs the small residual
factor directly by a freshly written Gaussian-Pascal calculation over
F5[alpha]/(alpha18+alpha9+1), supplies explicit Bezout identities, and checks
all primary centers and exceptional endpoints. Its source-bound endpoint
check also decodes the accepted F constant coefficient without invoking the
producer.

The final primary theorem is
`q29_remaining_pairs_2044/THEOREM_AND_PROOF.md`, SHA256
`3a086d0468a0a961132a50dda737b1f1540f3e9a6fe7bde95f28174d77887a97`.
Its manifest is
`fd65ee49da6a80a25d394fc63390935ac65fdfdaf6c10b3513f27da4330a1f4f`.
The independent primary review is
`q29_remaining_pairs_independent_2044/INDEPENDENT_REVIEW.md`, SHA256
`495ca3fcda320ecf23a3511e0f2fe00ebc0cb5d9428a15fb8da14a6feb913e3b`;
its final verdict and manifest are respectively
`719afd229accff45ec3889a375c2909b24463d2e3a8f48ee158a7349b2c65dac` and
`d0b7af992acc2802d80463a2cb8ba17108fe2543b153f493c020348a95dead81`.

The primary review independently reconstructed every new representative
j=2,...,13 by a reciprocal-R recurrence, against the author's direct-H
recurrence, and compared all2,160,000 new raw scalar bytes, all414,720 terminal
scalar bytes, and all172,800 inner scalar bytes. It also accepted the original
source-bound j=0 and j=1,26 dependencies, without modifying their archives.

This aggregate review did not run either large producer or another worker's
program. My fresh `check_coverage.py` reads their accepted coefficient arrays,
recomputes valuations, the entire-content and Newton guards, ordinary
derivative minima and tails, all96 terminal quintic conclusions, all24 inner
quintic conclusions, local scaling and six annular cross-resultants. Every
representative gives4731, and the labels are exactly0,...,26 with no collision.

My separate fresh `check_final_bindings.py` verifies all444 author-manifest
entries and all663 independent-review-manifest entries, their exact sizes and
hashes, each per-center certificate and acceptance, the final numeric coverage,
and all351 explicit center differences by a newly written power-of-alpha
calculation. `FINAL_BINDING_CHECKS.json` records the complete binding list.
The source-bound reported resource receipts satisfy their180-second,
256-MiB-per-process and1800-second aggregate ceilings. No resource expansion
or additional ring precision was used in the aggregate audit.

The live-stage coverage checker intentionally retains its
`AWAIT_FINAL_BATCH_REVIEW` status and `global_claim_enabled:false`: it is a
per-center gate, not a final-acceptance writer. This new review and its final
verdict are the separate final discharge, pinned to the completed primary
review. They do not rewrite the earlier conditional checkpoint.

## 2. Common complete field and precision

Let O=Z5[alpha]/Phi27(alpha), with Phi27(T)=T18+T9+1. Since ord27(5)=18,
O is the unramified degree18 integer ring. Let pi=zeta125-1 and
A=O[pi]. The polynomial Phi125(1+T) is Eisenstein of degree100, so A is a
complete DVR with v_pi(5)=100. Every packet uses the same fixed q=alpha(1+pi)
and primitive projection. No Frobenius transfer between changed q-values
is used. The CRT source binding is alpha=q1000 and1+pi=q2376.

Every new nonshared raw jet is the actual quotient A/(pi100), truncated at
v-degree100. Primitive-field projection precedes all valuations. Independently
certified weighted content60 yields an entire integral normalized
F_j(Y)=pi^-60 H1687(-alpha^j(1+piY);q) modulo pi40. The omitted coefficients
contribute at least40 after normalization; finite-array length is never used
as a substitute for this whole-polynomial precision bound.

In the complete Eisenstein extension rho2=pi, F precision80rho loses50rho at
the terminal normalization, leaving30rho. The additional normalized-quintic
step loses5rho, leaving25rho. The inner normalization has50rho precision.
Ordinary integer derivatives retain v_rho(5)=200. The terminal coefficient
tail is at least7k-50 for k>=8; raw derivative tails are at least99r for root
value r. All decisive values lie strictly below their actual error bounds.

All96 actual terminal constants have exact value5rho. Their normalized
residue has nonzero coefficients in degrees0,1,5, hence nonzero constant
derivative and five nonzero simple residue roots. The constant-zero branch
allowed in the frozen general lemma is not needed in this completed batch.
The only disclosed source repair was the separately pinned center-domain
guard change from1/26 to2..13, after a pre-recurrence rejection; arithmetic
was unchanged and fresh parameter controls preceded the retry.

## 3. The twelve remaining roots and every global resultant

The Gaussian block identity at the residue root alpha gives

    U1687(z) modpi = (1+z27)^62 Ebar(z),
    Ebar(z) = H13(z;alpha)/(z+1).

The fresh certificate proves that Ebar is monic of degree12, squarefree, and
nonzero at each -alpha^j. Since27 is prime to5, the27 roots of1+z27 are
distinct. Hensel lifting of these pairwise coprime monic factors in complete
A gives the exact characteristic-zero factorization

    U1687 = E product_(j=0)^26 P_j,
    deg E=12, deg P_j=62.

This requires pairwise coprimality of the displayed primary factors, not
squarefreeness of the repeated residual factor inside an individual P_j.
Squarefreeness of Ebar implies Disc(E) is a unit. Every one of the351
cross-primary resultants and27 E/primary resultants is a unit, by coprime
reductions. Consequently all1686 roots are covered, with no unexamined tail:

    27*62 + 12 = 1674+12 = 1686.

Each accepted local degree62 monic discriminant is4731 in original-v units.
The change z=-alpha^j(1+v) has unit scale, so it does not change the valuation.
At j!=0, the persistent H factor z+1 is an analytic unit on that primary disk;
at j=0 it was removed by the already accepted shared-center normalization.
No extra pi60 content factor is inserted into a monic discriminant.

The exact same-q reciprocal pairing is {0},{1,26},...,{13,14}. For monic P_j,
the partner is z62 P_j(1/z)/P_j(0), with P_j(0) a unit; the discriminant
multiplier is P_j(0)^-122. This accounts for every pair once. Thus

    v_pi Disc U1687
      = sum_(j=0)^26 v_pi Disc P_j
      = 4731 + 2*13*4731 = 127737.

The value is finite, so U1687 is squarefree. The monic leading coefficient is1,
and no degree12 or cross-resultant correction is missing.

## 4. Reciprocal quotient, branch points, and the final value

The exact reciprocal identity is

    U1687(z)=z843 R843(w),  w=z+2+z^-1=(1+z)^2/z.

For a monic R with roots w_i, the quadratic factors
z2+(2-w_i)z+1 have discriminants w_i(w_i-4); pairwise resultants are
(w_i-w_j)^2. Therefore the ordinary discriminant identity, including its
positive sign, is

    Disc U1687 = (Disc R843)^2 R843(0) R843(4).

It is not legitimate to infer U squarefreeness merely from R squarefreeness
without excluding the branch values0 and4. Those endpoint gates are explicit:

    U(-1)=-R(0),  v_pi U(-1)=75;
    U(1)= R(4),   v_pi U(1)=0;
    U(0)=1.

The first value comes from the independently decoded F0 valuation15 and the
accepted actual-root normalization U(-1)=pi60 F0. The decoded source has
precision140 for F, hence precision200 after multiplication, safely above75.
The second value follows from the fresh nonzero residue2^62 Ebar(1). These
exclude z=-1,+1 and the pole z=0. They are actual characteristic-zero
nonvanishing statements, not conclusions drawn from a finite-ring zero.

It follows that R843 is squarefree and

    v_pi Disc R843 = (127737-75-0)/2 = 63831.

The quotient degree count is shared31 plus13*62 nonshared plus6 residual,
total843. The residual degree6 reciprocal factor is separately certified
squarefree and disjoint from all relevant w-centers in the fresh certificate.
The shared-center quotient contribution is(4731-75)/2=2328; adding13*4731
gives the same63831, providing a second accounting check.

Finally H1687=(z+1)U1687 has no repeated persistent root because U(-1)!=0.
The product discriminant identity adds2*v_pi U(-1)=150, so its value is127887.
This corollary uses no new computation and makes no claim for another layer.

## 5. Remaining boundaries

The complete fixed instance and its exact ordinary discriminant valuations
are accepted. The broader Q29 parent remains open at54. Extending the result
to other layers or parameters requires new source-bound algebra or proofs;
the identical values across this batch are not a uniformity theorem.

Any table/repository publication still has its own approved destination,
source commit, fresh preimage/readback, rich-text preservation and application
ordering requirements. No publication action was performed by this review.
The earlier forty-root, ten-root, shared-center, pair1/26, conditional aggregate,
and final primary packets remain sealed and are dependencies, not replacements.
