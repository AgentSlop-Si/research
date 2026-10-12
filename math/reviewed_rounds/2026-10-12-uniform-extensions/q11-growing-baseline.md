Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematics, source attribution, limitations and review method are retained. Original source-report SHA-256: c903db44a360e7cb030e524ec60f46c7e0cc775f5c6aa51532b796f9d989faa7.

Review date: 12 October 2026 UTC.

# Q11 growing full-B family: independent bounded ACCEPT

Date: 2026-10-12 UTC.

## 1. Verdict and sealed target

**ACCEPT, bounded exactly as stated below.** There is no mathematical blocker in the frozen candidate. This acceptance covers an elementary full-target N-term Green representation, its paid quadratic ambient-field cost and conservative bit upper, the all-K coefficient-field impossibility, and the growing lower bound for the specifically restricted ordinary forward/reverse architecture. It does not close the broader Q11 research goal.

The reviewed candidate is `Q11_Growing_Full_B_Rank_Obstruction_CANDIDATE_2026-10-12.zip`, exactly 189,351 bytes, SHA-256 `60cde0a45af28c88195b00a566d1d8e4ffbb20d16410798ca7f578329ae0dee4`. Its manifest hash is `a21361a3c9d47ee8eee4072d6a959a670ea675f38487def884bdaf26dc0df09a`. All 22 members, all manifest entries, and the six packaged source pins were checked. The supplied read-only directory was compared byte for byte with the archive. Original research programs and both candidate programs were retained as inert data and were never imported or executed.

The target is the entire matrix, for every integer m>=1:

- q=483^m=(3·7·23)^m; N=5q²; h=(N+1)/2;
- omega is any supplied primitive complex Nth root;
- F[i,j]=omega^(ij), A[j,j]=omega^(h j²), B=(F^(-1)+A)^(-1);
- eta=omega^(q⁴), K=Q(eta), L=Q(omega).

Here K has rational degree four. The candidate's opening phrase “five-dimensional block field” refers to the five-coordinate block, not to field degree; use “degree-four block field” in integrations to avoid ambiguity. This wording does not affect any proof.

The legal summands are L_s(I-W_s)^(-1)R_s with diagonal, possibly singular endpoints, a Hamiltonian successor on the original fixed coordinates, arbitrary edge weights including zero, and 1-holonomy nonzero. There is no free diagonal or unmatched endpoint permutation in the accepted upper.

## 2. Full inverse, chirp sign and normalization

The following is an independent derivation, not an inference from finite controls. Because q is odd and coprime to 5, every residue modulo N has the unique form x=q²u+5v, with u modulo 5 and v modulo q². The cross term in h x² is divisible by N. Thus the Gauss sum is the product of a five-point sum and a square-modulus sum. In the latter, write v=s+qt. The inner sum over t is zero unless s=0 modulo q, since 2·5h is a unit modulo q. The square-modulus factor is exactly q for every supplied primitive omega, with no analytic square-root choice.

Modulo 5, h=3, and therefore the first factor is g=1+2eta²+2eta³. Reduction modulo eta⁴+eta³+eta²+eta+1 shows g²=5. Set G=qg, c=NG=5q³g. Then G²=N, c²=125q⁶, D=1-125q⁶ is a nonzero rational integer, and

rho=(1-c)/D=1/(1+c).

Let T=AF. Completing the square gives T²=NG·T^(-1), hence T³=cI. Consequently (I+T)^(-1)=rho(I-T+T²). Since F^(-1)+A=(I+AF)F^(-1), its inverse is F(I+AF)^(-1). Its three terms are, respectively,

- F[i,j]=omega^(ij);
- (FAF)[i,j]=G·omega^(-h(i+j)²);
- (F(AF)²)[i,j]=c·omega^(-h i²) delta_ij.

This proves every entry of the full matrix:

b_ij=rho[omega^(ij)-G omega^(-h(i+j)²)+c omega^(-h i²)delta_ij].

The minus sign, the unnormalized Fourier factor N, and the diagonal correction are all required. In particular, this is not merely an identity on the five-coordinate principal restriction.

## 3. Source-legal upper and all guards

For each s in {0,...,N-1}, take successor i->i+1 modulo N, set w_i=1 except w_(s-1)=0, use left diagonal mask delta_(i,s), and set the right diagonal entries to the explicit full row b_sj above. Then W_s^N=0 and

(I-W_s)^(-1)=I+W_s+...+W_s^(N-1).

Every structural permutation is still Hamiltonian even though one weighted edge is zero. Holonomy is zero and the Green denominator is exactly one. Starting at row s, all path lengths 0,...,N-1 have product one and visit all vertices once; the zero edge is only encountered when attempting the next step. Hence row s of the inverse is all ones. Left masking and right scaling give exactly delta_(i,s)b_sj. Summing N branches yields every entry of B, including every diagonal entry.

No endpoint is required to be invertible, no individual edge is divided by, and there is no extra correction summand or hidden coordinate change. The full inverse exists in characteristic zero by the explicit nonzero D. A supplied root can be verified using omega^N=1 and omega^(N/p)!=1 for p in {3,5,7,23}; these are precisely the distinct prime divisors of N.

## 4. Uniform coefficient-field obstruction

Since eta has order five, [K:Q]=4. For i=0,j=1 the diagonal term vanishes, giving

b_01=(1-Gt)/(1+c), where t=omega^(-h).

Here G and c belong to K, G is nonzero, and t=(1-(1+c)b_01)/G. Since 2h=N+1, gcd(h,N)=1, so t is primitive of order N. It follows that K(b_01)=L.

The cyclotomic degrees, calculated using the prime factorization, are

[L:Q]=4(2·3^(2m-1))(6·7^(2m-1))(22·23^(2m-1))=1056·483^(2m-1),

[L:K]=264·483^(2m-1)>1.

Every legal Green matrix with all endpoint and edge coefficients in K is a matrix over K: its finite inverse numerator and nonzero scalar denominator are in K. A finite sum remains over K. Therefore no such all-K representation can equal this full B, regardless of term count. This claim is relative to K; it is not a classification of all alternative coefficient fields.

## 5. Uniform characteristic-zero rank proof and exact scope

Put P=23^m, r=21^m, ell=N/P, zeta=omega^ell and E=Q(eta,zeta). The two root orders 5 and P are coprime, so E=Q(zeta_(5P)) and [E:Q]=4 phi(P). Choose

I={0,...,r-1}, J={ell,2ell,...,rell}.

Because r<P, all column indices are below N; r-1<ell makes the rectangle strictly separated and off diagonal. Because N/P²=5·21^(2m) is an integer, N divides (a ell)². Expanding the square in the entry formula and using 2h=1 modulo N gives

(1+c)b_(i,aell)=zeta^(ai)-G t^(i²) zeta^(-ai).

Consider over E the determinant polynomial f(T) of the r-by-r matrix with entries zeta^(ai)-G T^(i²)zeta^(-ai), indexed by 0<=i<r, 1<=a<=r. Its degree is at most d=r(r-1)(2r-1)/6. At T=0 the i=0 row is constant 1-G, and the other rows are the usual powers of the distinct zeta^a. Hence

f(0)=(1-G) product_(a<b)(zeta^b-zeta^a) != 0.

Here G²=N>1 rules out G=1. Meanwhile t generates L over E, and

[E(t):E]=[L:E]=12·21^(2m-1)·23^m=(4/7)·10143^m.

For every m>=1, d<r³/3=9261^m/3<(4/7)·10143^m. The latter inequality follows directly from 9261<10143 and 1/3<4/7, independently of any finite sample. A nonzero polynomial of degree below the minimal-polynomial degree of t cannot vanish there. Thus f(t)!=0 and rank_L B[I,J]=r=21^m.

For an ordinary forward Green cycle, all I-to-J paths are nonwrapping and cross a common cut between max(I) and min(J). The product along each path splits into a factor depending only on its row and a factor depending only on its column. Endpoint factors and the common inverse denominator preserve this outer-product form. For an ordinary reverse cycle, each path wraps; its segment from i down through zero and its segment from N-1 down to j+1 supply the same separation. Both arguments multiply edge weights but never divide by them, so zeros and singular endpoints are fully included.

Consequently, k ordinary forward/reverse Green branches have rectangle rank at most k. Any diagonal vanishes there and t isolated-entry corrections add rank at most t. Equality with B forces k+t>=21^m. The accepted two-mode/one-entry local recipe therefore cannot extend unchanged to the frozen full family. With its specific correction (0,1), that entry misses this rectangle, so the obstruction is even stronger: the rectangle has rank at most two.

The order restriction is indispensable. Interleave the selected vertices as i_0,j_1,i_1,j_2,...,i_(r-1),j_r, then visit all remaining vertices; use all weights one except a final wrap weight two. Holonomy is two and the Green denominator is -1. Its rectangle is -1 on/above the diagonal and -2 below. Subtract each previous row from its successor, from bottom upward: the resulting lower rows each have a single -1, proving determinant -1 for every r. Thus one arbitrary Hamiltonian branch already has full rectangle rank r. This explicitly disproves the attempted extension of this rank-one lemma to arbitrary structural cycles.

There is no unrestricted three-Green impossibility, arbitrary-cycle term-count lower bound, negative-chirp result, block-state recurrence bound or general circuit lower bound here. Previously accepted unrestricted lower results are neither reproved nor changed.

## 6. Complete construction and cost audit

The accepted field-operation claim uses exact arithmetic in supplied L, with integer indexing and routing charged separately. It does not treat L as a fixed-degree field.

- Build omega^0,...,omega^(N-1) in N-1 L multiplications; root certification, if absent, costs O(log N) more.
- q,N,h, coefficient exponents and locations are computed with O(log N)-bit integer arithmetic. g,G,c,D,rho need constant many field operations once these integers and powers are available.
- Every one of the N² right-endpoint entries is generated from the explicit entry formula with constant many L operations. There is no N² table supplied as free advice.
- Applying all masked rows uses N² coefficient/input multiplications, N(N-1) additions, N² charged cyclic routing visits, and N output writes. This is the actual surviving row action of each displayed Green inverse.
- Fully materializing endpoints and structural arrays charges their writes and costs O(N²) field storage. Generating and applying one row at a time uses O(N) L storage, including the root table, inputs and outputs; repeated applications require stored coefficients or renewed synthesis.

Thus both preparation and application have O(N²) field-operation upper bounds, with O(N²) O(log N)-bit indexing operations and routing accounted for. This is a dense row-expansion baseline, not an efficient low-length representation.

The canonical ambient field representation is also correct. Write s=483^(2m-1), so N=2415s and dL=1056s. Every prime divisor of s divides 2415. A root of Phi_2415(X^s) must have order exactly 2415s: if its order is n, n/gcd(n,s)=2415 forces the exponent of each prime 3,7,23 to be 2m, the exponent of 5 to be one, and no other primes. The degrees agree, proving Phi_N(X)=Phi_2415(X^s). The supplied 1057 coefficients satisfy the exact integer Moebius product identity; the largest absolute coefficient is four. Setup and dense degree-dL storage are charged, and the fixed base polynomial is not an oracle.

The sparse unreduced b_ij description has at most 28 root monomials and common denominator D, with O(log N)-bit exponents and O(log q)-bit integer numerators. This is only a compact coefficient description. Arbitrary inputs still occupy N·dL rational coordinates.

For the advertised coarse bit upper, take input numerator/denominator length at most H and form the product Q of all N·dL input denominators, of length at most N·dL·H. All output terms can be accumulated with the fixed common denominator QD, avoiding repeated denominator multiplication. Reduce exponents modulo N, then modulo Phi_2415(X^s); split by exponent residues modulo s to see that reduction growth is bounded by constants from the fixed base-degree-2415 reduction. Products of canonical degree-dL polynomials can be reduced by the same residue split with O(dL²) schoolbook coefficient work. The bit length of numerator entries is bounded by

Bbits=O(N·dL·H+log q+log N).

The proposed O(N²·dL²·Bbits²) bit bound and O(N·dL·Bbits) streaming memory bound are conservative valid upper bounds, including denominator conversion, setup, root reduction, coefficient generation and output writes. They are not unit-cost rational-coordinate claims, numerical-stability claims or bit-model speed claims.

The classical two-DFT factorization in the candidate is algebraically the same full entry formula. Smooth fixed radices 3,5,7,23 permit the familiar O(N log N) exact-L arithmetic comparator, but it is not an additive Green representation. This review makes no runtime superiority, FFT improvement, novelty or historical-priority claim.

## 7. Independent executable evidence and cold replay

The new checker imports only Python standard-library modules. It reads the pinned candidate archive as data, reconstructs expressions independently, and does not import candidate/historical code.

Evidence after the fresh run and sealed archive cold replay:

- 22 candidate members and all packaged manifest/source hashes verified;
- exact g²=5 reduction modulo Phi_5;
- all 62,075 entries of each product B(F^(-1)+A) and (F^(-1)+A)B checked at N=5,45,245;
- all 295 masked rows and outputs checked at those control sizes, plus every full branch inverse and the assembled 25-entry upper at N=5;
- original rank-21 certificate independently reconstructed at the actual m=1 target;
- new m=1 witness over p=25,661,791, omega=7,374,867: rank 21, determinant 132,537; its entire length-N Gauss sum is checked directly;
- new m=2 witness at N=272,118,787,605 over p=13,605,939,380,251, omega=10,212,877,662,042: rank 441, determinant 12,437,590,008,309;
- all 128 zero/nonzero edge patterns in both orientations of a seven-cycle, including endpoint-zero cases and full inverse checks;
- interleaved-cycle full-rank countercontrols at r=2,3,5,21;
- imprimitive root, unit holonomy, altered target entry and all five off-by-one row cuts rejected;
- exact integer Moebius identity for the supplied base modulus;
- degree/index arithmetic for m=1,...,100 as controls only.

The small controls are outside the frozen m>=1 family; q=1 is also outside the frozen range. The m=1 and m=2 controls execute only the specified rectangles and auxiliary identities, never the huge full N-by-N transforms. Finite-field ranks and finite arithmetic tests are not the uniform proof. Uniformity comes from sections 2-6 above.

The sibling `Q11_GROWING_REVIEWER_COLD_2026-10-12.json` records a clean extraction of the final review archive into a new directory, the same standalone checker run without changing originals, manifest validation, and equality with the stored result. The final outer seal binds the resulting archive bytes and replay. No external writes were performed.

## 8. Scope and remaining work

The original accepted five-dimensional arithmetic minimum-three result remains valid. For the full q=483^m family, the new upper is an N-term quadratic ambient-field baseline, the coefficient-field obstruction is relative to the degree-four K, and the rank bound applies only to ordinary canonical forward/reverse branches with the stated corrections. The interleaved-cycle counterexample is essential. Arbitrary-cycle small-length constructions, efficient growing full-B algorithms, negative-family uppers, stability and historical priority remain open.
