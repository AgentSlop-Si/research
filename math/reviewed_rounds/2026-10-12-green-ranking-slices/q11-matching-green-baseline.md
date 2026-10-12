Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical proof, source attribution, evidence and limitations are retained. Original source-report SHA-256: 9ba3d2f77b40170561d0fe1d9deeb86ef0130948d3dfb6f09772d64c558470ff.

Review date: 12 October 2026 UTC.

# Q11 subquadratic matching Green bridge: independent bounded ACCEPT

Date: 12 October 2026 UTC. Verdict: **ACCEPT within the exact scope below**.

## Result and provenance

For every m>=1, q=483^m and N=5q^2, the full positive-chirp target B=(F^(-1)+A)^(-1), with F_ij=omega^(ij), A_jj=omega^(h j^2), h=(N+1)/2 and any supplied primitive complex Nth root omega, has a source-legal representation by **20q+1 additive Hamiltonian-structural-cycle Green branches** over L=Q(omega). Compressed preparation is O(N) exact L operations, direct all-output application is Theta(Nq)=Theta(N^(3/2)) L operations, and streaming storage is O(N) L slots. Routing, indexing and endpoint synthesis are charged; materializing the expanded descriptors costs Theta(Nq) writes and storage.

This improves the accepted N-term quadratic additive Green baseline on this family. It remains asymptotically slower than the accepted ordinary two-DFT O(N log N) evaluator. It does not establish a faster FFT, a constant-term construction, an unrestricted lower bound, numerical stability, practical runtime superiority, a bit-model speed advantage, or historical novelty. The broader Q11 gate remains OPEN.

The reviewed candidate archive is Q11_Subquadratic_Matching_Green_Bridge_CANDIDATE_2026-10-12.zip, 255,597 bytes, SHA-256 **002831f9ada28230ceb5bd3e8c9abdb61b98af6282e06a4210181dcc5e0ca61c**. All 15 members, 14 manifest items and six source pins were verified. The accepted review and author report match the corresponding files inside the nested accepted source archive. The accepted source archive's independently verified SHA-256 is 74a0f40fef9e5e96856774018f98f76582f4a7ce64ee630b06faf3c761132add.

INDEPENDENT_DERIVATION.md was written before receipt of the sealed candidate, after reading only its draft explanation and the accepted source proof. Its SHA-256 is 91dadf4ae6d9e626dbc4351b2e2fb3cd45c3a6742302d1bcb8faf317c169d5b7. The reviewer then wrote the standalone mathematical and binding checkers in this packet. Neither author nor historical program was imported or executed; such code inside the candidate archive was treated only as inert bytes for provenance.

## 1. Frozen target and inverse guards

The inherited grammar is a sum of L_b(I-W_b)^(-1)R_b, with diagonal endpoints, singular values allowed; sigma_b is a single Hamiltonian structural cycle on the original N coordinates; (W_b x)_i=w_i x_(sigma_b(i)); zero edge weights are allowed; and 1-product_i(w_i) must be nonzero. There are no unmatched endpoint permutations or free diagonal terms.

Let eta=omega^(q^4), g=1+2eta^2+2eta^3, G=qg, c=NG and rho=(1+c)^(-1). The accepted full-target identity, with its signs and normalization preserved, is

B_ij=rho[omega^(ij)-G omega^(-h(i+j)^2)+c omega^(-h i^2)delta_ij].

Its scalar guards are uniform: g^2=5, G^2=N, c^2=125q^6, and rho=(1-c)/(1-125q^6), whose rational denominator is nonzero. This follows from the source's square-modulus Gauss factorization and the cubic identity (AF)^3=NG I. The construction is on all original N coordinates, not a five-coordinate principal restriction. All coefficients are explicit combinations of powers of the supplied root and rational numbers. There is no hidden root selection, interpolation, factorization, eigenvalue computation, or inverse oracle.

## 2. Independent block and packing proof

Set s=5q and S_a={a+su:0<=u<q}. For i in S_a and j in S_b,

ij-ib-a(j-b)=(i-a)(j-b)=s^2uv,

which is divisible by N since s^2=5N. Consequently omega^(ij) and omega^(-h i^2)omega^(-h j^2)omega^(-ij) are rank one on each S_a-by-S_b block. Multiplying the draft's factors directly gives exactly the two full-target kernel entries, since 2h=1 modulo N.

For each round t modulo odd s, use pairs {t+d,t-d}, 1<=d<=(s-1)/2, and singleton {t}. Every unordered pair {a,b} occurs once because 2 is invertible modulo s and its round must be t=(a+b)/2. Within that round the signed displacement chooses a unique d up to the displayed sign convention.

For a pair (a,b), form a path by listing S_a then S_b. Concatenate all paired paths and the singleton path into one Hamiltonian structural cycle. Give each component's final edge weight zero and all internal edges weight one. The inverse's finite walk sum is an upper-triangular all-ones matrix inside each component and zero between components. A left endpoint supported on S_a and a right endpoint supported on S_b therefore give their rank-one product on exactly S_a-by-S_b. All other entries within this paired component vanish through the masks. The masks and coefficients for distinct components occupy disjoint original coordinates, so they can be set simultaneously without any compatibility equation. Every cross-component path meets a zero edge. This disposes of the potentially problematic unwanted blocks.

For the reverse branch, reverse the Hamiltonian structural cycle and put the zero weights on each original component's first vertex. Its effective components are the reversed paths. The left support S_b and right support S_a give precisely the opposite directed block. Reversing the whole concatenated list, including component order, is exactly the inverse structural cycle. Different orders between the zero-separated reversed components would also yield the same effective weighted matrix; the sealed construction specifies a correct inverse cycle directly.

On the singleton S_t both endpoints are present. Forward and reverse give the two complementary triangles, including the diagonal in both. Their sum is the full desired rank-one singleton block plus one duplicate of its diagonal. Each S_t is a singleton only once. Thus two modes and two directions in s rounds give exactly the two full kernel matrices plus an extra diagonal.

That extra diagonal is rho omega^(i^2)-rho G omega^(-4h i^2). Its subtraction and the target's diagonal insertion are

d_i=rho c omega^(-h i^2)-rho omega^(i^2)+rho G omega^(-4h i^2).

One additional legal branch uses W=0, R=I and L=diag(d). It has inverse I. The complete sum therefore equals B entry by entry. There are 4s+1=20q+1 branches, all with holonomy zero and Green denominator exactly one. No auxiliary permutations or free calibration operation have been introduced. Entrywise equality proves correctness for every input in L^N, not merely sampled or basis inputs.

## 3. Cost, synthesis, routing and representation audit

Four tables suffice: P[k]=omega^k, U[k]=rho P[k], V[k]=-rho G P[k], and D[i]=d_i. The literal table procedure costs 4N-1 multiplications and 2N additions, excluding scalar setup and optional root certification. The final candidate separately charges O(log N) for integer-to-field scalar synthesis/root checks. Thus O(N) compressed preparation is valid. Each live endpoint is one table lookup with a fixed number of modular index operations. Writing every endpoint and route occurrence instead requires Theta(Ns) writes; the compressed claim does not hide this cost.

For each noncalibration branch, put r=(s-1)/2 and M=(r+1)q=(N+q)/2. There are M live input and output endpoints. Each paired component performs a q-term dot product and scales q outputs. Each singleton performs the weighted suffix-sum recurrence in its directed path. These are precisely the relevant entries of the displayed Green inverse, not a replacement transform. They use 2M multiplications, (r+1)(q-1) internal additions and M output additions. Calibration adds N multiplications. The exact literal schedule has

multiplications=N+4s(N+q)=N(4s+5),
additions=4s[(s+1)(q-1)/2+(N+q)/2]=2(s+1)(2N-s).

The independent checker instruments these actual operations and obtains those counts at all small test sizes. For q=483, N=1,166,445, they equal 11,273,690,925 multiplications and 11,260,855,200 additions in 9,661 displayed branches. These are algorithmic counts, not executed full-sized benchmarks.

Input weighting visits total 2(s+1)N and output scaling/accumulation visits total the same. Even enumerating each full structural cycle for both modes and both directions uses only 4sN visits. All original-coordinate movement, endpoint lookup/address construction and final output writes are charged. The formulas involve only a fixed number of O(log N)-bit words per address. Four tables plus input/output vectors use 6N field slots and only constant extra field accumulators. Scratch is explicitly initialized; no claim about a dirty-auxiliary tensor interface is involved.

The ambient cyclotomic degree d_L=1056*483^(2m-1) is linear in N, so a field slot has growing bit size. In the accepted canonical representation Phi_N(X)=Phi_2415(X^s0), s0=483^(2m-1), a root monomial reduces with constants bounded by the fixed base polynomial. After clearing input denominators into Q, the actual schedule multiplies input-dependent sums only by fixed root/scalar endpoints. The right factors are monomials; the left factors have denominator dividing D0=1-125q^6. The calibration also has denominator dividing D0. A common QD0 already suffices; the candidate's allowance of a fixed power is conservative. Sums contain polynomially many terms with polynomial-in-q scalar magnitudes. Thus Bbits=O(N*d_L*H+log q+log N) is a safe height bound, and O(N*s*d_L^2*Bbits^2) schoolbook bit work with O(N*d_L*Bbits) live bits is a valid conservative upper. This remains only an upper, not a speed comparison or numerical-stability statement.

## 4. Fresh executable evidence

check_independent.py independently builds the legal weighted Hamiltonian branches, sums their literal weighted-walk inverses, and checks recurrence equations. It does not use the optimized rank-one schedule to construct its reference Green matrices. Separately it instruments the optimized application and compares it with full target multiplication and the defining inverse.

The fresh run passes:

- 430,150 complete assembled matrix entries across q=1,1,3,3,7,11, with two distinct supplied primitive roots at q=1 and q=3; largest complete matrix N=605;
- 128,250 entries of the two defining products B(F^(-1)+A) and (F^(-1)+A)B through N=245;
- 173,000 generic branch recurrence coordinate checks, with Hamiltonian-cycle and zero-holonomy verification;
- 124 optimized vector applications, including all standard basis vectors at N=5 and N=45, zero vectors, random vectors and deterministic dense vectors; all operation counts match;
- all 2,914,905 unordered class pairs at s=2415, plus complete smaller matching checks;
- actual m=1 control over independently selected prime p=18,663,121 and primitive omega=65,536: all 1,166,445 diagonal calibrations, the full length-N Gauss sum, and 6,515 coefficient checks including 2,415 same-class off-diagonal samples;
- negative controls for omitted calibration, mutated live endpoint, removal of a zero boundary causing an unwanted crossblock, imprimitive root and unit holonomy.

The small q controls are outside the frozen m>=1 family and are algebra/implementation controls only. The m=1 control does not execute the full 9,661-branch million-coordinate transform, and no huge dense target is constructed. The infinite-family proof is sections 1-3, not extrapolation from finite fields. CHECK_RESULTS.json records exact scope and outputs.

The separate binding checker verifies every candidate manifest/source pin, nested accepted reports, the numeric cost ledger without running source programs. A cold replay of these same independent checkers from the packaged review is recorded by the final sibling seal and cold-replay receipt.

## 5. Attribution and remaining scope

The new bound is a source-model construction, not a historical-priority finding. Its weighted-cycle inverse, low-rank factor application and round-robin matching mechanisms are elementary or classical. The candidate explicitly leaves priority unresolved. The new literature orientation is accurately limited: [Butterfly Factorization](https://arxiv.org/abs/1502.01379) treats complementary-low-rank matrices through products of sparse factors; [rank-one block identification](https://arxiv.org/abs/2307.00820) concerns identifying the associated partitionings; and [Graph-Induced Rank Structures](https://arxiv.org/abs/1911.05858) discusses graph-based representations and their construction. Their primary abstracts were checked independently. This review neither proves a theorem-level equivalence to the present additive grammar nor proves a historical nonmatch.

The bounded result is: full positive B at q=483^m has an explicit 20q+1 legal zero-edge arbitrary-cycle Green upper, O(N) compressed field preparation, Theta(Nq) paid direct application, Theta(Nq) expanded writes and O(N) streaming field storage. It is a subquadratic improvement over the accepted additive dense baseline and slower than the accepted O(N log N) two-DFT evaluator.

The accepted five-dimensional minimum-three result is preserved; the broader growing-target problem remains open. The all-Q(eta) impossibility is unchanged because the new construction uses Q(omega). The ordinary-order rank lower k+t>=21^m is unchanged because the new cycles reorder residue-class components. Do not infer an unrestricted arbitrary-cycle lower bound, all-N result, constant-term optimum, negative-family extension, stability result or novelty ranking. No broader conclusion follows.
