# Prior-art normalization of the Taylor packed-state lemmas

17 October 2026. Focused mathematical comparison, not a new multiplication construction or a historical-priority certification.

## Result

The general mechanism behind the accepted state lower bound is classical observability/minimal-realization theory: a state supporting future linear outputs must have dimension at least their joint observation rank. The observation matrix is, after transposition, a block Krylov matrix. The formulas `B+(B-1)h` and `K-s+1` are concrete, elementary calculations for the particular block-evaluation interface; they are not new general principles of observability or linear-state lower bounds.

There is an exact normalization that makes the comparison especially transparent. Set `q=K-s`. The reported attaining state

    (f_0,...,f_(q-1), U_(B-1))

is precisely the coefficient vector of

    F(z) mod [z^q(z-p)].

Thus its transition is the ordinary multiplication operator by `1+z` in a polynomial quotient of dimension `q+1=K-s+1`. This is a reinterpretation of the existing state, not an additional algorithm. The degree-safe restriction is essential: replacing the problem by multiplication modulo `z^K` changes the observability ranks and would give the wrong literature comparison.

The input conversion is the classical Taylor shift `A(z+1)`, followed by grouped evaluation at `p`; its coefficient matrix is the transpose of the usual lower-triangular Pascal matrix. Positive overlapping radix blocks are an exact redundant representation, not canonical digit packing. The specific simultaneous bit-volume formula is an additional representation-size calculation, not a consequence of a field-operation Taylor-shift bound.

No conclusion here establishes worldwide novelty, absence of prior art, a general algorithmic lower bound, or faster integer multiplication.

## 1. Inputs, conventions, and source scope

The two supplied reports were read without running their scripts:

- `mersenne_next_gate_20261017_1153/REPORT.md`, SHA-256 `eec1368f1f8ef61200b0310dcb616a173c2b49e9a3d50ea6c292c07a280ecdb5`.
- `fused_taylor_producer_20261017_1205/REPORT.md`, SHA-256 `6168f5834b69465c9c457e5f3b66a5a0653f3a9da6a771aedac9414a6f801db6`.

The parent assignment describes the lemmas as accepted; the local report headers still describe those packets' earlier review status. This comparison does not change review or repository status.

Use their notation: `m>=2`, `p=2^m-1`, `s|K`, `B=K/s`, and `F(z)=sum_(j=0)^(K-1) f_j z^j`. All state-space ranks below are over `Q`. Let

    E(F)_r = sum_(t=0)^(s-1) p^t f_(rs+t),
    JF = (1+z)F,
    V_h = {F : deg F < K-h}.

The accepted lookahead map is `O_h F=(E F,E JF,...,E J^h F)` on `V_h`, for `0<=h<s`.

The primary-source anchors are Kalman's original 1963 paper; Boley's author-hosted 1994 paper, which explicitly gives both discrete-time systems and the Krylov/observability correspondence; FLINT's official Taylor-shift documentation; and authors' descriptions of the 1997 and 2005 Taylor-shift papers. Exact locators and access limitations appear in Section 8. No source code, historical test program, or newly written arithmetic test was executed. No external state was changed.

## 2. Classical theorem versus the family-specific calculation

### 2.1 The standard implication

For a fixed state transition `L`, output matrix `P`, and initial encoding `S`, the future observation matrix factors as

    O_h = [P; PL; ...; PL^h] S.

Consequently `rank O_h <= rank S <= D`, where `D` is the scalar-state dimension. This is the exact linear-algebra mechanism used by the report. The corresponding infinite unobservable subspace is the common kernel of all output iterates; quotienting by it is the usual observable reduction. Kalman gives the constant-system observation-rank criterion in Section 6, Lemma 4, equation (6.6), and minimal-realization results in Section 5, Theorems 7–8. [Kalman, 1963](https://people.duke.edu/~hpgavin/SystemID/References/Kalman-JSIAM-1963.pdf).

In Boley's notation, the transpose of `[C; CA; ...; CA^h]` is `K(A^T,C^T,h+1)`. His Section 2, Theorem 1 gives Krylov rank saturation; Section 3, Theorem 2 identifies the unobservable space with the kernel of the transposed Krylov matrix. His equations (18)–(19) explicitly cover continuous and discrete time. [Boley, 1994](https://www-users.cse.umn.edu/~boley/publications/papers/Krylov94.pdf).

Neither source supplies the specific block-window formula in the supplied packets merely by stating the general theorem. One must still normalize the operators and calculate their rank.

### 2.2 Exact rank calculation for this interface

The triangular binomial identity

    J^t = sum_(j=0)^t binom(t,j) z^j

has diagonal coefficients one. Thus the stacks using `J^t` and `z^t` have the same row space. Write `W_t=E(z^t F)`. The key row difference is

    W_(t+1,r)-p W_(t,r)
      = f_(rs-1-t)-p^s f_((r+1)s-1-t).

For `F in V_h` and `t<h`, the terminal term `f_(K-1-t)` is zero. Solving across the blocks shows that the row space is exactly that spanned by

    E(F), and
    f_((r+1)s-j),  0<=r<B-1, 1<=j<=h.

These are `B+(B-1)h` independent functionals: the boundary coefficients are distinct, and each block retains at least one coefficient outside those boundary rows when `h<s`. This is the family-specific calculation. It explains precisely why each extra lookahead contributes `B-1`, rather than a generic value of `B`.

At `h=s-1`, the rank equals

    B+(B-1)(s-1)=K-s+1=dim V_(s-1).

The lower bound on `D` now follows immediately from the standard factorization. Classification: **classical method, exact specialized rank evaluation, sharp specialized corollary**. The bounded sources inspected do not establish whether the exact displayed formula has previously appeared under other notation.

The rank calculation needs only `p!=0` over `Q`; neither primality nor the Mersenne form is used. Those features belong to the surrounding integer-representation application.

## 3. Exact normalization to a finite-dimensional realization

This section is a direct algebraic identification of the supplied attaining state.

Put `q=K-s` and `g(z)=z^q(z-p)`. Split

    F(z)=F_low(z)+z^q F_tail(z),  deg F_low<q.

Since `F_tail(z)-F_tail(p)` is divisible by `z-p`,

    F mod g = F_low(z)+F_tail(p) z^q.

For `deg F<K`, `F_tail(p)=U_(B-1)`. Therefore taking a polynomial remainder modulo `g` is exactly the report's state map `S`, with no approximation or hidden extra coordinate.

In the basis `1,z,...,z^q` of `Q[z]/(g)`, multiplication by `1+z` sends the coordinate vector `x` to

    x'_0=x_0,
    x'_j=x_j+x_(j-1),       1<=j<q,
    x'_q=(p+1)x_q+x_(q-1).

For `q=0`, the sole update is `x'_0=(p+1)x_0`. These are exactly the supplied formulas. The output decoder evaluates each of the first `B-1` groups of the low coefficients at `p`, and returns `x_q` for the final output. Denote it by `C`; denote this quotient transition by `A_q`. Then

    E = C S                  on deg F<K,
    S(JF)=A_q S(F)           whenever deg F<K-1.

For every `h<s`, `S:V_h -> Q[z]/(g)` is onto: `V_h` contains every polynomial of degree at most `q`. It follows that

    O_h = [C; C A_q; ...; C A_q^h] S|_(V_h),
    rank O_h = rank [C; C A_q; ...; C A_q^h].

This removes a possible ambiguity caused by the shrinking domain `V_h`: the same rank profile also belongs to an ordinary fixed finite-dimensional observation system. At `h=s-1` it is fully observable. With scalar input vector the class of `1`, it is reachable as well, because `1,(1+z),...,(1+z)^q` form a basis. Thus the compatible quotient realization is a standard reachable/observable minimal realization.

Its characteristic and minimal polynomial are

    (lambda-1)^q (lambda-(p+1)).

There is also an exact finite Hankel normalization using only the originally required weight columns. Let `b` be the coordinate vector of the class of `1`, and let the `B`-vector `w_i=E((1+z)^i)` for `0<=i<K`. Form the block Hankel matrix

    H_(t,j)=w_(t+j),   0<=t<s, 0<=j<=q.

Every index satisfies `t+j<=K-1`. Hence no unspecified higher-degree behavior is used. Its factorization is

    H = [C; C A_q; ...; C A_q^(s-1)]
        [b, A_q b, ..., A_q^q b].

The left factor has rank `q+1` by the family calculation; the right factor is invertible by the triangular binomial basis. Thus `rank H=q+1`. This is the ordinary observability-times-reachability/Hankel-rank obstruction specialized to the accepted finite weight sequence. Boley discusses the corresponding Krylov-product/Hankel factorization in Section 3. [Boley, 1994](https://www-users.cse.umn.edu/~boley/publications/papers/Krylov94.pdf).

Equivalently, since `p!=0`, the state can be expressed as the first `q` Taylor coefficients at zero together with `F(p)`: recover the tail coordinate by

    U_(B-1) = [F(p)-sum_(j=0)^(q-1) f_j p^j]/p^q.

This is the usual polynomial-remainder/Chinese-remainder viewpoint, with one jet at zero and one ordinary value at `p`. This rational-coordinate equivalence says nothing by itself about the bit cost of computing or storing either coordinate system.

The construction extends the degree-safe behavior beyond the requested polynomial range in one particular way. It does **not** assert that the original finite-window outputs of arbitrary higher-degree polynomials agree with this extension. Minimality for the original bounded problem still uses its own rank lower bound; minimality of one chosen infinite extension alone would not prove that lower bound.

## 4. Why nilpotent truncation is a different comparison

Let `N` be multiplication by `z` modulo `z^K` on the full `K`-coefficient space. The tempting pair `(I+N,E)` is not the preceding quotient system. Its last-block row difference includes

    -p^s f_(K-1-t),

which is not zero for an unrestricted initial state. The same elimination now extracts `h` boundary layers from **all B blocks**, rather than only the first `B-1`. For `0<=h<s`, this gives

    rank [E; E(I+N); ...; E(I+N)^h] = B(h+1).

At `h=s-1` the rank is `K`. The original report instead restricts the input to `V_h`, killing the terminal `h` coefficients and producing `B+(B-1)h`.

Therefore it would be inaccurate to describe `K-s+1` as the Kalman observable dimension of the unqualified `K`-dimensional nilpotent-truncated shift. The correct normalization is the degree-safe observation restriction, or equivalently the quotient realization in Section 3.

The earlier two-term witness is also a standard quotient-factorization test in explicit form. Existence of `E J=L E` on the allowed domain requires `ker E` to be preserved by the relevant transition. The witness `z^(s-1)-p z^(s-2)` is in `ker E` but its degree-safe image is not. The witness is useful for this interface; the kernel-invariance obstruction is general linear algebra.

## 5. Classical Taylor/binomial packing normalization

Let `a=(a_0,...,a_(K-1))^T`, and define the conventional lower Pascal matrix `P` by `P_(i,j)=binom(i,j)` for `i>=j`. In ascending coefficient order,

    c=P^T a,
    C(z)=A(z+1),
    c_j=sum_(i=j)^(K-1) binom(i,j) a_i.

The transpose matters: the standard sequence transform with output index on the upper summation limit is not literally the same orientation. More generally, the coefficient Taylor-shift matrix has entries `binom(i,j) tau^(i-j)` in row `j`, column `i`; these matrices compose by addition of shift parameters and invert by negating the parameter.

An elementary normalization to the classical factorial-convolution form is

    j! c_j = sum_(i=j)^(K-1) (i! a_i)/(i-j)!.

Set `alpha_t=(K-1-t)! a_(K-1-t)` and `beta_t=1/t!`. Then

    c_j=(alpha*beta)_(K-1-j)/j!.

This is an identity over `Q`; its use over other rings requires the relevant factorials to be invertible, or a separately paid denominator treatment. FLINT's official generic-polynomial documentation lists Horner, divide-and-conquer, and single-convolution Taylor shift. Its word-modular convolution routine explicitly requires a prime modulus at least the polynomial length. [FLINT generic-polynomial documentation](https://raw.githubusercontent.com/flintlib/flint/main/doc/source/gr_poly.rst), [FLINT word-modular documentation](https://raw.githubusercontent.com/flintlib/flint/main/doc/source/nmod_poly.rst).

The packing matrix `E` has disjoint block rows `(1,p,...,p^(s-1))`, and the complete transform is simply

    U=E P^T a.

Equivalently write `C(z)=sum_r z^(rs) C_r(z)` with `deg C_r<s`; then `U_r=C_r(p)` and `X=C(p)=sum_r U_r(p^s)^r`. This is grouped polynomial evaluation after a Taylor shift. The Mersenne identity contributes `2^m=p+1`, aligning the old binary-chunk evaluation point with the shifted evaluation point. It does not create a new Taylor transform.

Unlike canonical radix or nonoverlapping Kronecker encodings, these coefficients may exceed `p^s-1`. Hence the representation is redundant, and exact reconstruction uses the weighted sum, not concatenation or fixed-width truncation.

The report's streamed weights are precisely columns of this composed matrix:

    w_(r,i)=(E P^T)_(r,i).

Their boundary recurrence is Pascal's identity plus cancellation at the two ends of a finite weighted window. The scaled-binomial updates are the usual consecutive-term ratio for a binomial coefficient. These basic identities are classical; the particular fused organization and its full bit ledger are implementation-specific results requiring their own proof and comparison.

Taylor-shift algorithms over integer coefficients were already compared by von zur Gathen and Gerhard in 1997. Johnson, Krandick, and Ruslanov's 2005 work explicitly uses signed digits, suspended normalization, radix reduction, and delayed carries in Taylor shift. Those sources rule out treating Taylor shift itself, or the general use of redundant arithmetic to delay carries, as new here. They do not by themselves settle the exact current block interface or rank formula. [1997 author-uploaded paper record](https://www.researchgate.net/publication/221564511_Fast_algorithms_for_Taylor_shifts_and_certain_difference_equations), [2005 author-uploaded paper record](https://www.researchgate.net/publication/221564150_Architecture-aware_classical_Taylor_shift_by_1).

## 6. Attribution and implication map

| Packet claim or device | Relation to established theory | What still belongs to this specific family |
|---|---|---|
| `A(z+1)` and binomial coefficients | Direct classical Taylor shift / transposed Pascal transform | Choosing `p=2^m-1` and this destination interface |
| Packing `s` consecutive coefficients | Grouped polynomial evaluation | Its exact redundant block widths and use in the smaller matrix interface |
| No closed state on just `E(F)` | Standard failure of kernel invariance | The two-term witness and exact affected block values |
| Stack future outputs to lower-bound state | Direct observability/rank factorization | Correct degree-safe domain and computed rank |
| `B+(B-1)h` | A block Krylov/observability rank profile | Boundary elimination and independence calculation |
| `D_min=K-s+1` | Minimal-realization argument after the rank calculation | Sharp value for this interface and its quotient normalization |
| Attaining state | Polynomial remainder state in `Q[z]/(z^(K-s)(z-p))` | This modulus and decoder fit the selected grouped outputs |
| Simultaneous volume `Theta(mK+K^2/s)` | Positivity, binomial identities, coefficient-size estimates | Uniform aggregation over these blocks and a simultaneous legal maximizer |
| Fused streamed producer | Classical binomial-window identities organized for selected outputs | Exact streaming schedule, scratch-width checks, and bit-operation invoice |

“Family-specific” is a mathematical classification, not a historical novelty verdict. A formula can be a correct useful specialization even if it is immediate from standard tools or has appeared elsewhere under another normalization.

The scalar-rank statements do not lower-bound the bit complexity of arbitrary algorithms. They constrain fixed linear state and linear output recovery under the stated transitions. Nonlinear encoding of a finite legal input set, time-varying methods, direct final-output computation, and alternative factorizations are outside those hypotheses. Nor do classical `O(M(K))` coefficient-ring Taylor-shift counts certify this integer interface's conversion, coefficient growth, recursive multiplication, normalization, or binary readout costs.

## 7. Recommended claim language and stopping point

A defensible summary is:

> We specialize the classical observability-rank method to degree-safe Taylor-Horner updates with grouped evaluation outputs. For this interface we compute the exact rank `B+(B-1)h`, obtain the sharp fixed-linear-state minimum `K-s+1`, and identify an attaining quotient-polynomial state. The input representation is classical Taylor shifting followed by redundant grouped evaluation. These interface calculations are not general lower bounds or a faster multiplication theorem.

This targeted comparison establishes the relation to standard theory and the proper scope of the accepted lemmas. It does not establish first publication of the specialized formulas. A worldwide-new label would need substantially broader bibliographic and equivalence work; search absence is not evidence sufficient for that label.

The requested bounded comparison is complete. No further construction or experiment is needed to state this classification.

## 8. Primary sources and inspection record

1. R. E. Kalman, *Mathematical Description of Linear Dynamical Systems*, Journal of the Society for Industrial and Applied Mathematics, Series A: Control 1(2), 152–192 (1963), DOI `10.1137/0301010`. Original paper inspected in a university-hosted PDF. Relevant locations: printed p. 169, Theorems 7–8; printed p. 170, Lemmas 3–4 and equation (6.6); printed pp. 176–180, canonical realization examples. [PDF](https://people.duke.edu/~hpgavin/SystemID/References/Kalman-JSIAM-1963.pdf).

2. Daniel L. Boley, *Krylov Space Methods on State-Space Control Models*, Circuits, Systems, and Signal Processing 13, 733–758 (1994), DOI `10.1007/BF02523124`. Author-hosted manuscript inspected. Section 2, equations defining block Krylov sequences and Theorem 1; Section 3, equations (18)–(24), Theorem 2. The manuscript PDF has its own page numbering, with Section 3 beginning on manuscript p. 9. [PDF](https://www-users.cse.umn.edu/~boley/publications/papers/Krylov94.pdf).

3. FLINT project, official `gr_poly` documentation, Taylor-shift functions; official `nmod_poly` documentation, “Taylor shift.” Inspected 17 October 2026. These are mutable `main` sources and are cited as current algorithm documentation, not dated priority evidence. [Generic](https://raw.githubusercontent.com/flintlib/flint/main/doc/source/gr_poly.rst), [word-modular](https://raw.githubusercontent.com/flintlib/flint/main/doc/source/nmod_poly.rst).

4. Joachim von zur Gathen and Jürgen Gerhard, *Fast Algorithms for Taylor Shifts and Certain Difference Equations*, ISSAC 1997, pp. 40–47, DOI `10.1145/258726.258745`. The author-uploaded record and abstract were inspected. The publisher DOI endpoint was inaccessible in this tool. Used only to establish the explicitly stated prior comparison of six integral Taylor-shift algorithms; no uninspected theorem or cost bound is attributed to it. [Author-uploaded record](https://www.researchgate.net/publication/221564511_Fast_algorithms_for_Taylor_shifts_and_certain_difference_equations).

5. Jeremy R. Johnson, Werner Krandick, and Anatole D. Ruslanov, *Architecture-aware Classical Taylor Shift by 1*, ISSAC 2005, pp. 200–207, DOI `10.1145/1073884.1073913`; also Drexel Technical Report DU-CS-05-06, May 2005. Author-uploaded abstract and technical-report opening text were available in indexed search results; direct full-page/PDF retrieval was unreliable. Used only for those explicit abstract-level techniques. [Author-uploaded record](https://www.researchgate.net/publication/221564150_Architecture-aware_classical_Taylor_shift_by_1).

All algebraic normalization and implication steps above are supplied explicitly, so the conclusions do not depend on treating an inaccessible paper as inspected or on inferring a theorem from search snippets.
