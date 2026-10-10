# Hero17 Phase18: exact magnetic-resolvent averaging

10 October 2026. New intake after the immutable Q30/Q32 supplement. Source ZIP: Library `[private-id]`, SHA256 `5e31a6b1c5c105a74f691b5fb086b81d87efbf487cc2c74e77a57ee486801ceb`. The source's programs and historical logs were read as inert text; none was executed, imported, compiled, or AST-parsed. All executed controls in this directory are freshly authored.

## Verdict and exact model

The main construction is valid: a growing number K of generically noncommuting magnetic resolvents can share a complete O(N) exact-field evaluator. Its result is a circulant, and therefore is not the nontrivial Fourier matrix. The weighted extension and restricted rank/support barriers also survive the proof checks below.

Let N=KM>=1. The coefficient domain is a field of characteristic not dividing N, with a **supplied** primitive Nth root omega. Let q=omega^M. The exact arithmetic model charges each field addition, subtraction, multiplication, and inversion; integer addresses use O(log N) bits. Alpha and beta are supplied field elements. Root or field discovery, input parsing beyond this representation, modular bit complexity, floating-point stability, and practical speed are separate obligations. No finite-word precision transfer to the Q30 inverse theorem follows just from this exact identity.

For N=1, omega=q=1 and the identities reduce directly to scalar arithmetic. Below the cyclic determinant proof is written for N>=2; this avoids pretending that the identity and cyclic permutation are distinct at N=1.

Define S e_i=e_(i+1), U e_i=q^i e_i, so US=qSU. Put

W_j=alpha S+beta q^j U, Q_j=I-W_j,
d=1-beta^K, c=alpha^K, D=d I-c S^K,
Delta=d^M-alpha^N=d^M-c^M.

All indices are cyclic modulo N. Every inverse in the theorem is guarded by Delta!=0.

## 1. Legality is equivalent, not merely sufficient

For N>=2, Q_j is cyclic bidiagonal. In its determinant expansion a permutation choosing one shifted off-diagonal entry must choose them all; otherwise a row/column conflict propagates around the cycle. Thus only the diagonal and full-cycle terms survive, giving

det Q_j=product_i(1-beta q^(i+j))-alpha^N
       =(1-beta^K)^M-alpha^N=Delta.

The q phases run through all Kth roots exactly M times; the product identity follows from t^K-1. Since S^K consists of K disjoint M-cycles, the same scalar-cycle argument gives det D=(d^M-c^M)^K=Delta^K. At M=1 each cycle is a scalar d-c, with the same result. At N=1, det Q_0=1-alpha-beta=Delta directly.

Consequently every Q_j is invertible if and only if D is invertible, if and only if Delta is nonzero. Individual diagonal entries 1-beta q^(i+j) may vanish even when this determinant is nonzero; a per-branch solver that divides by those entries is only a reference on its smaller domain. The fused solver below handles these cases.

The branches are conjugate: Q_j=S^(-j)Q_0 S^j. For K>1 and alpha beta!=0, their commutators are nonzero because they are a nonzero multiple of (q^j-q^l)[S,U], and [S,U]=(1-q)SU. Their inverses therefore also fail to commute pairwise. These are genuinely different noncommuting branches, notwithstanding their simple average.

## 2. Root-of-unity cancellation and exact fusion

Set X=alpha S, Y_j=beta q^j U. Then Y_j X=q X Y_j. Induction gives the finite q-binomial expansion

(X+Y_j)^t=sum_(h=0)^t [t choose h]_q X^(t-h)Y_j^h.

For t=K, every intermediate coefficient [K choose h]_q, 0<h<K, vanishes: its numerator includes 1-q^K=0, while the denominator factors 1-q^r, r<K, are all nonzero. Hence

W_j^K=alpha^K S^K+beta^K I,
I-W_j^K=D.

This also holds trivially at K=1. Since D is a polynomial in W_j, it commutes with W_j and is independent of j. Under Delta!=0,

Q_j^(-1)=D^(-1)sum_(t=0)^(K-1)W_j^t.

The average (1/K)sum_j q^(jh) is 1 for h=0 and 0 for 1<=h<K; characteristic not dividing N ensures K is invertible. Applying this filter to the truncated expansion leaves only X^t. Therefore

R_0=(1/K)sum_j Q_j^(-1)
   =D^(-1) P_K(S), P_K(S)=sum_(r=0)^(K-1)alpha^r S^r.        (1)

This is an exact operator identity on every input, not a data-dependent shortcut.

## 3. Fully charged evaluator, including degeneracies

### 3.1 Sliding numerator

Set z=P_K(S)x. Compute z_0=sum_(r=0)^(K-1)alpha^r x_(-r) by updating successive powers of alpha, in O(K) field operations. Then

z_i=alpha z_(i-1)+x_i-alpha^K x_(i-K), i=1,...,N-1.           (2)

The cancellation follows by shifting the geometric window. It costs O(N) operations and writes every z_i. No inversion or division by 1-alpha^N occurs, so resonance alpha^N=1 is allowed. K=1 is an exact copy, alpha=0 gives z=x, and K=N remains within O(N) work.

### 3.2 K cyclic solves

Solve d y_i-c y_(i-K)=z_i. If d=0, Delta!=0 forces c!=0, and

y_i=-z_(i+K)/c,                                            (3)

requiring one scalar inverse and N multiplications, plus a constant number of sign operations. If d!=0, set r=c/d and u_i=z_i/d. In each residue class s modulo K, let i_t=s+tK. An initial zero-boundary pass computes

B_s=sum_(t=0)^(M-1)r^(M-1-t)u_(i_t).

The periodic value immediately before t=0 is B_s/(1-r^M). The denominator is nonzero because d^M(1-r^M)=Delta. A second pass y_(i_t)=r y_(i_(t-1))+u_(i_t) emits the solution. Summed over all K cycles, both passes have N steps. The cases c=0, M=1 and d=0 are covered, without hidden linear-system or Fourier subroutines.

Powers alpha^K, beta^K, r^M take O(log N) field multiplications; only a constant number of field inversions are needed. The whole execution, supplied-parameter preparation, input access, indexing, and N output writes cost O(N), using O(N) retained field elements and O(N) address traffic.

If supplied-root validation is requested, factor the integer N by trial division in O(sqrt N) O(log N)-word operations and test omega^N=1 and omega^(N/l)!=1 for every distinct prime l|N. At most O(log N) binary powers are needed, for O(log^2 N) field work. These are within the stated O(N) **mixed field/address-operation** bound. They do not find a primitive root, prove an arbitrary supplied field implementation correct, or turn large finite-field arithmetic into unit-cost bit operations.

### 3.3 Source operation count checked statically

Let P(t)=floor(log2 t)+popcount(t), the source's counted binary-power cost for t>=1. On its d!=0 branch and K>1, the source application graph has exactly

P(K)+3K+4(N-1)   numerator field operations,
6N+K            strided-solve field operations,
10N+4K-4+P(K)    total online field operations.

For N=65536,K=64,alpha=2,beta=3,p=65537, the guards hold. Static counting gives 655619 online operations. Supplied-root validation and parameter setup add

P(N)+P(N/2)+2P(M)+2P(K)+5=74,

so 655693 reproduces the historical fused count without running its code. This is a count of the declared graph, not an optimal arithmetic count. The d=0 branch uses a unary sign change when preparing -c; if unary negation is a paid field subtraction, add that constant operation rather than hiding it. This does not change the theorem or the displayed d!=0 benchmark. We do not certify the historical 38.48x reference comparison as a practical performance claim.

## 4. Exact averaged rank

Because D is invertible, rank R_0=rank P_K(S). The shift has N distinct eigenvalues lambda in the supplied root-rich field. A zero of P_K(lambda) occurs exactly when (alpha lambda)^K=1 but alpha lambda!=1. Such a zero forces alpha^N=1. Conversely, when alpha^N=1 exactly K of the N eigenvalues satisfy the first condition, and precisely one gives alpha lambda=1; its geometric sum is K!=0. Thus

rank R_0=N if alpha^N!=1;
rank R_0=N-K+1 if alpha^N=1.                               (4)

Legality Delta!=0 is retained in both cases. In particular, an average of invertible branches need not be invertible.

## 5. Weighted sectors: complete coefficient and work contract

For 0<=ell<K, define R_ell=(1/K)sum_j q^(-j ell)Q_j^(-1). The same filter selects exactly ell appearances of Y_j. Hence

R_ell=D^(-1) beta^ell [sum_(r=0)^(K-1-ell)
             alpha^r [r+ell choose ell]_q S^r] U^ell.        (5)

For all terms in this sum,

[r+ell choose ell]_q=product_(i=1)^ell(1-q^(r+i))
                    /product_(i=1)^ell(1-q^i).

The denominator is nonzero because ell<K. Expand product_i(1-q^i z)=sum_(h=0)^ell c_h z^h using O(ell^2) field work and O(ell) storage, charging its coefficients and denominator inverse. Equation (5)'s numerator is a linear combination of ell+1 geometric windows of length K-ell with ratios alpha q^h. Prepare the ratios successively. Prepare and apply U^ell using a phase recurrence in O(N), not N separate uncharged exponentiations. Evaluate each window by (2), accumulate, then run the common strided solve. The resulting total is

O((ell+1)N+ell^2+K) field operations, O(N+ell) retained storage.

Fixed ell gives O(N). Growing ell does not; emitting all K sector vectors already needs NK output entries. This is not a free simultaneous all-sector transform.

Because D and the shift polynomial commute with S, while U^ell S=q^ell S U^ell,

R_ell S=q^ell S R_ell, and [R_ell,S^K]=0.                    (6)

For ell=0, (1) shows the stronger [R_0,S]=0. Different K or alpha/beta values do not change that stronger commutation of unweighted averages: any linear combination of them remains circulant.

## 6. Exact Fourier obstruction, with its scope retained

Assume characteristic other than 2 for the source's stated parity formula. Let F[k,t]=omega^(-kt), T e_i=omega^i e_i. Fourier intertwining gives

F S^K-S^K F=(T^(-K)-S^K)F.

Multiplication by F preserves rank. On each residue cycle i=s+tK, the kernel equation for T^(-K)-S^K propagates one coordinate; its consistency product is

product_(t=0)^(M-1)omega^[-K(s+Kt)]=(-1)^[K(M-1)]=(-1)^(N-K).

Thus each of K cycles has nullity 1 if N-K is even, and 0 if it is odd. Consequently

rank[F,S^K]=N-K if N-K is even, and N otherwise.              (7)

If A commutes with S^K and F=A+E, then [F,S^K]=[E,S^K], whose rank is at most 2 rank E. This proves the source's additive repair lower bound. For K<N it rules out equality of F with any sum of the fixed-K weighted sectors. For K=N, S^K=I and the bound is 0; this gate does not apply. For unweighted averages use K=1 irrespective of their original branch count: the correction rank is at least N/2 for even N and (N-1)/2 for odd N. These are representation-specific rank barriers, not unrestricted algorithm lower bounds.

## 7. Weyl-line barrier and its explicit limitation

For odd prime N, W_(a,b)=S^a T^b form a basis of all matrices. Directly evaluating the trace gives the Fourier coefficient

c_(a,b)=(1/N)sum_t omega^[-t^2-(a+b)t]
        =(G/N)omega^[(a+b)^2/4], G=sum_t omega^(-t^2).        (8)

The exponent1/4 means inverse4 modulo the integer N, not division by4 in the coefficient field. Completing the square proves the displayed phase, and the classical algebraic Gauss identity G^2=(-1)^((N-1)/2)N proves G!=0 whenever the characteristic does not divide N. For completeness, write chi for the quadratic character on Z/NZ with chi(0)=0. The number of t with t^2=u is 1+chi(u), so G=sum_u chi(u)omega^(-u). In G^2 substitute v=u t with u!=0: the inner sum over u is N-1 for t=-1 and -1 otherwise. Since sum_t chi(t)=0, this gives G^2=N chi(-1). The argument is algebraic and survives reduction to the coefficient field. Thus every Fourier Weyl coefficient is nonzero, including after admissible finite-field specialization.

Powers of a nonidentity single-direction Weyl monomial occupy one line through0 in the two-dimensional index plane over the prime residue field Z/NZ. Polynomial functions, and rational functions with invertible denominators, of that monomial remain in the same span. B such linear lines cover at most1+B(N-1) points, so covering all N^2 Fourier coefficients needs B>=N+1. Multiplying each term by left/right Weyl monomials translates its support into an affine line of N points, yielding B>=N. These are support-coverage necessities only. Arbitrary diagonal endpoints and general products are outside the grammar.

Indeed, for nonzero alpha,beta with alpha^N,beta^N!=1,

(I-alpha S)^(-1)(I-beta T)^(-1)
 =sum_(a,b) alpha^a beta^b S^a T^b
    /[(1-alpha^N)(1-beta^N)]

has full Weyl support, yet applies with one diagonal scaling and one cyclic recurrence in O(N) exact operations. This invalidates any attempted promotion of full support into a general time lower bound. It does not make that product Fourier.

## 8. Fresh evidence and source scope

The new small controls independently build every original branch matrix and invert it by modular elimination. They compare the average and **every weighted sector** with both the q-binomial formula and a separately authored sliding-window/strided executor, on every input basis vector.

They cover 106 legal parameter cases and reject 38 singular cases, including 36 legal d=0 cases, 60 genuinely noncommuting cases, K=1, K=N, N=1, alpha=0, beta=0, and resonance. They check 12,400 unweighted and 46,596 weighted full basis entries; 106 exact averaged ranks; 45 commutator ranks; and 373 nonzero Weyl coefficients. Finite controls do not substitute for the general proofs above.

A separate fresh large-vector control reconstructs the 65,536-coordinate case with 64 branches using a new dense input. Its direct branch solver and fused solver do not import source functions or one another. The result file records full output equality, a direct-DFT mismatch control, and the statically reconstructed count. This validates the construction independently, without certifying the submitted program or its historical timing/reference ledger.

## 9. Prior art and research transition

The finite q-binomial theorem is classical. Stoyanovsky's primary two-page note gives the yx=qxy expansion; root-of-unity specialization is the immediate vanishing argument in §2 above. Ishibashi's 2026 article, §3 equation 3.1, uses the same standard cyclic shift/modulation representation, with its parameter written q^2. Its representation machinery is background; it is not a verified claim that the exact resolvent-average executor already appears there.

- https://arxiv.org/html/0812.4916v2
- https://link.springer.com/article/10.1007/s00220-026-05604-6

Roots-of-unity filtering, cyclic linear recurrences, and Gauss-sum support arguments are also classical. The source's specific synthesis is a valid project construction; worldwide priority remains unestablished. One source bullet incorrectly calls the cited author “S. S. Stoyanovsky”; the verified paper author is A. V. Stoyanovsky. This bibliographic typo does not affect the proof.

Research transition: accept a constructive example showing that growing noncommuting branch count does not by itself force KN work. Keep its exact symmetry and inverse guards. It does not close the Fourier problem or general Q30 bounded-word inverse preparation. A later architecture must both escape the relevant commutants and match the Fourier intertwining/seed constraints; branch counting or full Weyl support alone cannot establish its cost or correctness.
