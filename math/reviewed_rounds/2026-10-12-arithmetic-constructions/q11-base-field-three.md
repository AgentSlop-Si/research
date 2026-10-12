Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, limitations and review method are retained. Original source-report SHA-256: 6711ec15838a214a6e3e787326d85e9e117754d4c68dfee22dfa5324ce70cfd1.

# Q11 distinct-cycle base-field three-Green construction: independent review

Date: 2026-10-12 UTC. Verdict: **ACCEPT SCOPED. No mathematical repair required.**

For every positive odd integer q with gcd(q,5)=1 and q congruent to 1 modulo 241, the stipulated five-coordinate block C_q admits exactly three source-legal Green summands over K=Q(eta), with three distinct directed Hamiltonian structural permutations. Two branches have all edge weights nonzero. The third is a one-edge nilpotent branch carrying a necessary off-diagonal correction and the complete diagonal calibration. The upper bound is freshly verified here; the assertion that the minimum is three also uses the separately accepted complex two-term lower bound, which this review does not rerun.

This completes the arithmetic five-dimensional base-field-three sub-obligation. It does not provide a growing full-B_N upper, an arbitrary-size/all-N upper, a negative-chirp-family upper, a stability result, or an FFT speed theorem. The common-cycle obstruction remains valid. No historical-priority judgment is made.

## 1. Frozen input, provenance, and independence

The reviewed archive is Q11_Distinct_Cycle_Base_Field_Three_Green_CANDIDATE_2026-10-12.zip, 217,908 bytes, SHA-256:

`1a428177a230cbf1ce6c32bdb7de1b11431c49dc5cd5a8eff1dca519c7cc4b42`.

The archive contains 27 manifest-bound payloads plus MANIFEST.json. Every size and SHA-256 matches. The supplied immutable directory matches every archive member byte for byte; the seven source pins match both the archived copies and the preserved original source files. The author REPORT.md has SHA-256 `9ca4000dff00b5f57c94ada22218fc3acf8face98d83e67bc24464a882a23bec`.

Principal dependencies are the accepted SP11 proof, SHA-256 `4aed4e38953ac9266f8dbe8995dae1d61046f02972f11c5434c018681eac8df5`, sections 2–2.5; its independent review, SHA-256 `79f959f1b57550e031bf99e9d7ff8e5a26f76045bda4ddf56c60f366613940e8`; its H01–H05 acceptance ledger; and the accepted common-cycle review, SHA-256 `6242262e774762595139e6d11f57fc70c6dcff31e6de3f23e8534ee512ae8865`.

Only independent_check.py, newly written for this review from the displayed mathematics, was executed. It uses Python's standard library. No author, uploaded, or historical Python program was executed, imported, compiled, or AST-parsed. Candidate JSON is inert comparison data, not a construction oracle. The reviewer reconstructs coefficients before comparing them. Candidate scripts remain bytes inside the sealed archive.

The exact arithmetic implementation represents Q[eta]/Phi_5 using rational four-vectors. Multiplication reduces the degree-four cyclotomic relation. Inverses are computed by multiplying the three nonidentity Galois conjugates and dividing by the resulting rational norm. This code does not import or reuse author arithmetic. A separate prime-field scalar implementation independently reconstructs the residue model.

## 2. Source grammar, field, and target

The source's exact allowed term is L(I-W_sigma)^(-1)R on the five original coordinates, where sigma is a Hamiltonian successor permutation, (W_sigma x)_i=w_i x_sigma(i), the diagonal endpoints may be singular, weights may be zero, and 1-product(w_i) must be nonzero. It does not require the effective nonzero-edge graph to remain Hamiltonian. No endpoint permutations, basis changes, products of Green terms, or free additive diagonal corrections are permitted.

For N=5q^2, eta=omega^(q^4) has exact order five: gcd(5q^2,q^4)=q^2 because gcd(q,5)=1. Phi_5 has degree four and is irreducible over Q, for Phi_5(X+1)=X^4+5X^3+10X^2+10X+5 is Eisenstein at 5. Thus K has degree four. All construction coefficients lie in K, with no square-root extension. The supplied primitive root is an input assumption, not a hidden root-finding operation.

The accepted principal-block formula is

c_ij = [eta^(ij) - qg eta^(-3(i+j)^2) + 5q^3g eta^(-3i^2) delta_ij]/(1+5q^3g),

g=1+2(eta^2+eta^3), g^2=5.

Both q and q^3 are retained. The denominator's product with 1-5q^3g is 1-125q^6, nonzero for every positive integral q. The accepted source derives this formula from the original Fourier/chirp inverse, including the Gauss-sum factor q and principal restriction. At q=1 the reviewer additionally verifies both matrix products with F_5^(-1)+A_5 equal I. For q>1, this is the five-dimensional principal block, not the complete B_N and not B_5.

## 3. Independent audit of the constructive identity

Change only entry (0,1) to x, forming B(x). For each j modulo five, construct A_j from rows j-2,j-1 and columns j,j+1, and v_j from those rows and column j+2. Set (a_j,b_j)^T=A_j^(-1)v_j and Q_j=[[0,1],[a_j,b_j]]. All these entries are off diagonal. Only Q_1 depends on x.

Writing

d(x)=c_41 c_02-x c_42,
a=c_43 c_02-c_03 c_42,
b(x)=c_41 c_03-x c_43,
T(x)=[[0,d(x)],[a,b(x)]],

one has Q_1=T(x)/d(x). With P=Q_4Q_3Q_2 and R=Q_0, the monodromy is M=P T(x)R/d(x). Since det(T)=-a d(x), multiplying det(M-rI) by d(x) gives exactly

H(x)=-det(P)a det(R)-r tr(P T(x)R)+r^2 d(x).

For r=3 this is affine. Therefore x=-H(0)/(H(1)-H(0)) forces r to be an eigenvalue, once the two necessary divisors are guarded. The checker reconstructs this formula, tests its affine values, and directly verifies det(M-3I)=0. The other eigenvalue s=det(M)/3 is nonzero, distinct from 3, and different from 1 by the guards below.

For each t in {3,s}, the vector (M_01,t-M_00)^T is an eigenvector. Its first coordinate is nonzero. The determinant of the two initial eigenvectors is M_01(s-3), so they are independent. Recurrence by Q_0,...,Q_4 gives y_5=t y_0 and y_6=t y_1. Since all transfers are invertible and five-periodic, extending y_(j+5)=t y_j gives a valid two-sided recurrence. Thus every consecutive two-column y matrix is invertible.

For each row i solve for (u_i^3,u_i^s) using columns i+1,i+2 in the unwrapped y sequences. The recurrence Q_(i+1) includes row i in its two defining rows and supplies column i+3; Q_(i+2) similarly supplies column i+4. Hence all twenty off-diagonal entries, including seam crossings, satisfy

B_ij=u_i^3 y_j^3+u_i^s y_j^s for i<j,
B_ij=3u_i^3 y_j^3+s u_i^s y_j^s for i>j.

This argument is symbolic and uniform; the finite exact checks are controls of its implementation.

The first branch has successor array (1,2,3,4,0), weights (1,1,1,1,3), endpoints u^3 and (1-3)y^3. Its diagonal is u_i^3 y_i^3, and its off-diagonal entries supply the first terms above.

The second branch has successor array (4,0,1,2,3), weights (s^(-1),1,1,1,1), endpoints s u^s and (1-s^(-1))y^s. A reverse path from i to j has numerator 1 for i>j, s^(-1) for i<j, and 1 on the diagonal. Its entries are therefore s u_i^s y_j^s below the diagonal, u_i^s y_j^s above, and s u_i^s y_i^s on the diagonal. The wrap weight is specifically at row 0. This is a legal different successor permutation in the fixed coordinates, with no conjugation or uncounted coordinate transformation.

Set D_i=c_ii-u_i^3y_i^3-s u_i^s y_i^s and e=c_01-x. The third successor array (1,3,4,2,0) is Hamiltonian, tracing 0→1→3→2→4→0, and is distinct from both other permutations. Its weights are (e,0,0,0,0), so W=eE_01 and W^2=0. Endpoints (1,D_1,D_2,D_3,D_4) and (D_0,1,1,1,1) give exactly

L(I-W)^(-1)R=diag(D)+eE_01.

The special endpoint choices ensure the correction coefficient is e itself. No endpoint division is required. This is one legal summand, not an independent diagonal plus a fourth Green term. Its holonomy is zero and its Green denominator is 1. Since e reduces to 10, the off-diagonal correction is essential. All endpoints happen to be nonzero on the stated family, although the source does not require that.

Summing these three branches proves all 25 entries. Direct path-product Green matrices are independently checked by both (I-W)G=I and G(I-W)=I for each branch. The exact scalar count is exactly three; minimality also uses the inherited accepted lower bound.

## 4. Complete guard proof and all-q validity

Take R=Z[eta] localized at the maximal ideal (241,eta-91). The checker proves 241 prime by trial division, and verifies that 91 is a nonidentity fifth root modulo 241. Thus evaluation eta↦91 defines the residue map to F_241. Every q congruent to 1 has q and q^3 residues 1. The target denominator reduces to 34 and the target reduces to

161 20 102 102 20
20 182 62 26 92
102 62 236 28 26
102 26 28 236 62
20 92 26 62 182.

The independently reconstructed residues, all agreeing with the frozen candidate, are:

- Initial window determinants: 188,188,184,28,184
- H(0)=231; affine slope=1; x=10; e=10
- Modified window determinants: 188,207,184,28,184
- det(Q_0),...,det(Q_4): 195,108,132,110,1
- M=[[183,153],[130,234]]
- r=3; s=173; s-r=170; s-1=172
- Eigenvector pivot M_01=153; initial eigenvector determinant=223
- Row-solving determinants: 105,13,29,57,57
- Actual branch holonomies: 3,202,0
- Green denominators: 239,40,1
- D: 110,99,137,75,111
- L1=(89,24,141,39,68), R1=(176,119,134,42,56)
- L2=(72,114,140,205,223), R2=(95,82,42,9,83)
- L3=(1,99,137,75,111), R3=(110,1,1,1,1)

The only divisions in coefficient preparation are by the target denominator, the initial and modified two-by-two window determinants, the characteristic slope, r, s, and the row-solving determinants. Green evaluation additionally divides by 1-h for each actual branch holonomy. Every such residue is explicitly nonzero. Transfer determinants, s-r, and M_01 guard the proof's invertibility/independence steps. No inverse of a zero third-branch edge is taken.

Starting in R, proceed in the formula's dependency order. At every division, the denominator's already-defined residue is nonzero, hence it is a unit of R. Reduction commutes with that division and determines the next listed residue. Induction makes every coefficient regular and every guard valid for every admitted q. Consequently the symbolic identity in section 3 holds uniformly over K. No finite-field existence is being lifted, no rational square root is assumed, and no empirical extrapolation from q=1,483,1447 occurs. This argument needs only the local ring and its unit criterion; an unproved integrally-closedness premise is not needed for this upper bound.

All primitive complex realizations of eta are related by field isomorphisms, so the construction and nonvanishing conclusions transport to every stipulated embedding. Positivity, oddness, and coprimality with 5 are retained to match the accepted ambient arithmetic family; reduction of the formulas by itself does not remove those source conditions.

## 5. Fresh exact controls and cold replay

The reviewer rebuilds the complete model at q=1,483,1447 over Q[eta]/Phi_5 and separately at q=1 over F_241. At each exact q:

- All 25 target entries and all 15 edge weights and 30 endpoint entries agree exactly with the frozen witness.
- Every intermediate window, transfer, eigenvector sequence, row solve, correction, branch matrix, and holonomy also agrees exactly.
- All guards and all witness coefficients reduce to the same independently computed residue model.
- Both Green inverse equations hold branchwise, and the sum matches all 25 entries.
- A five-coordinate input is applied using four actual weighted-successor passes per branch and agrees exactly with dense target multiplication.

The q=1 target additionally satisfies both original defining inverse equations. Branch-coefficient numerator/denominator maximum bit lengths are 70,448,515 respectively. These measurements check finite coefficients, not an asymptotic theorem.

Fresh legal mutations change 5 entries when one endpoint is perturbed, 1 entry when the third branch's nonzero edge is removed, 1 entry when D_0 is omitted, and 8 entries when the reverse wrap weight is moved from row 0 to row 4. All three q values detect every mutation. The latter gives 17 unchanged entries, agreeing with the reported routing sensitivity. These controls confirm that neither calibration nor orientation is accidentally ignored.

A cold run in a separate directory has only the sealed candidate archive and the new reviewer checker available as inputs. It uses isolated Python mode. All three rebuilt exact witness files are byte-identical to the first run. The complete result object is identical except for the expected matching-directory-presence flag. COLD_REPLAY.json binds this comparison and the reviewer checker hash. No supplied program was needed in either run.

## 6. Preparation, application, and bit-cost scope

Given eta in the fixed four-coordinate K representation and q, the rational construction uses a fixed number of K operations and guard tests. All eigenvectors, row coefficients, endpoints, edge weights, inverse Green denominators, and routing arrays are prepared explicitly. There is no free dense parameter matrix, quadratic-root oracle, factorization search, or uncharged endpoint transformation.

Because this is one fixed rational straight-line formula in q over a fixed-degree field, rational coordinate numerators and denominators have O(log q) bit length. Exact preparation therefore takes polynomial time in log q in that fixed-degree representation. The constant degree is important. This is not a unit-cost claim about arbitrary complex numbers.

If only the ambient primitive root omega is supplied, eta=omega^(q^4) costs O(log q) ambient-field multiplications by binary exponentiation, with the ordinary integer cost of constructing q^4. That does not imply polylogarithmic bit cost for arbitrary dense representations of the ambient field Q(omega), whose degree can grow with q. The accepted fixed-degree bit bound is for the explicitly represented K coefficient stage; root representation and any ambient conversion cost must remain charged separately.

For each of three branches, the stated conservative application consists of 5 right-endpoint multiplications, 4 weighted-successor passes with 20 multiplications and 20 additions, 5 prepared-denominator multiplications, and 5 left-endpoint multiplications. This totals 105 K multiplications and 60 additions across the branches, plus 10 additions to combine them. The 60 successor routing assignments, fixed-size table reads, five inputs, and five outputs are part of the work. The third branch can be cheaper but the proof does not depend on that optimization. Bit cost of applying to arbitrary exact inputs additionally depends on those input heights.

The count concerns a constant five-dimensional block only. At q>1 it constructs neither the other N-5 outputs nor a factorization of full B_N. Fewer Green summands imply no ambient FFT advantage, no practical speed comparison, and no numerical conditioning or floating-point stability bound.

## 7. Scope and remaining work

Accepted scope: for positive odd q coprime to 5 with q congruent to 1 modulo 241, the five-dimensional C_q has a source-legal base-field three-Green upper with three distinct structural cycles; the one-edge nilpotent third term contains its full diagonal calibration; the accepted two-term lower bound makes the minimum three over K itself. This completes the arithmetic five-dimensional base-field-three sub-obligation while broader upper obligations remain open.

The accepted common-cycle-two-Green-plus-diagonal obstruction remains unchanged: the present third branch has a necessary nonzero off-diagonal entry. The pre-existing quadratic-extension construction remains a valid construction, but necessity of that extension for all three-term representations is now false in this scoped family. No such general necessity was claimed by the accepted source. Preserve the two-term lower evidence level and all M-CHIRP-LOWER both-sign results. No negative-sign upper or historical-priority conclusion follows.
