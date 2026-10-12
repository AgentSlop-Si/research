# GTSL — Growing Tensor-Union Savings Ladder
## Candidate exact O(N log log N) / O(N) Fourier theory

**Date:** 2026-10-12  
**Status:** proved compiler-to-complexity theorem + exact Cooley–Tukey macro identity + conjectural growing Green/scan tensor-union compiler.  
**Goal:** exact DFT on arbitrary fresh dense inputs, all outputs explicit, all scalar preparation/routing/arithmetic charged.

Target hierarchy:

\[
\boxed{\rho<1\text{ fixed} \Longrightarrow
T(N)=O\!\left(N(\log N)^{\log_2(2\rho)}\right)=o(N\log N)}
\]

for \(1/2<\rho<1\),

\[
\boxed{\rho=\tfrac12 \Longrightarrow T(N)=O(N\log\log N),}
\]

and

\[
\boxed{\rho<\tfrac12 \Longrightarrow T(N)=O(N).}
\]

The symbol \(\rho\) measures how much of the two **recursive tensor-axis
banks** remains after exact algebraic union/fusion.

This is NOT the already-known "one finite tensor saving" mechanism by itself.
The current public OpenAI Fourier work already uses finite tensor savings to
obtain a fixed power saving.  GTSL's research target is a **growing family**
of Fourier-specific union macros whose saving approaches the critical
half-union threshold \(\rho=1/2\).

-------------------------------------------------------------------------------
1. Exact balanced Cooley–Tukey macro
-------------------------------------------------------------------------------

Let

\[
N=ab,
\]

and let \(\omega_N\) be a primitive \(N\)-th root.  Write

\[
n=n_1+a n_2,\qquad
0\le n_1<a,\quad0\le n_2<b,
\]

and

\[
k=k_2+b k_1,\qquad
0\le k_1<a,\quad0\le k_2<b.
\]

Then

\[
\omega_N^{kn}
=
\omega_a^{k_1n_1}
\omega_b^{k_2n_2}
\omega_N^{k_2n_1}.
\]

Therefore \(F_N\) is computed exactly by:

1. \(a\) independent \(b\)-point DFTs along \(n_2\);
2. \(N\) twiddle scalings \(\omega_N^{k_2n_1}\);
3. \(b\) independent \(a\)-point DFTs along \(n_1\);
4. fixed input/output index permutations.

If \(C(n)\) is charged exact circuit work, the ordinary separated-axis
macro gives

\[
C(ab)
\le
aC(b)+bC(a)+\kappa ab
\tag{1}
\]

for a model-dependent constant \(\kappa\) covering twiddles, permutations,
root-table amortization and simple linear work.

The algebraic identity is classical.  GTSL asks whether the two recursive
banks in (1) can be executed **jointly**, with shared intermediate linear
forms, rather than as separate axis calls.

-------------------------------------------------------------------------------
2. Definition: a tensor-union macro
-------------------------------------------------------------------------------

For balanced dyadic factors

\[
a=2^{\lfloor w/2\rfloor},
\qquad
b=2^{\lceil w/2\rceil},
\qquad
N=2^w,
\]

a \(\rho(w)\)-tensor-union compiler is a uniform exact circuit satisfying

\[
\boxed{
C(2^w)
\le
\rho(w)
\left[
aC(b)+bC(a)
\right]
+
\kappa 2^w.
}
\tag{2}
\]

Important:

- \(\rho=1\) is just ordinary axis-separated Cooley–Tukey.
- A "saving" must reduce input-dependent arithmetic, not only setup.
- All generated scalar constants, indices, routing and storage schedules are
  charged according to the same model.
- A dense matrix or a smaller FFT cannot be hidden as one primitive.
- The compiler may use unbounded complex coefficients, but their generation
  and magnitude ledger must be explicit.

Put

\[
f(w)=\frac{C(2^w)}{2^w}.
\]

Then (2) becomes

\[
\boxed{
f(w)
\le
\rho(w)
\left[
f(\lfloor w/2\rfloor)+
f(\lceil w/2\rceil)
\right]
+
\kappa.
}
\tag{3}
\]

So the entire asymptotic question has become a recurrence on the **bit
length \(w=\log_2N\)**.

-------------------------------------------------------------------------------
3. Fixed-saving theorem
-------------------------------------------------------------------------------

## Theorem 3.1

Assume that for all sufficiently large \(w\),

\[
\rho(w)\le\rho<1.
\]

Then:

### Case A: \(1/2<\rho<1\)

Let

\[
\alpha=\log_2(2\rho).
\]

Then \(0<\alpha<1\) and

\[
\boxed{
C(N)=O\!\left(N(\log N)^\alpha\right).
}
\tag{4}
\]

### Case B: \(\rho=1/2\)

\[
\boxed{
C(N)=O(N\log\log N).
}
\tag{5}
\]

### Case C: \(\rho<1/2\)

\[
\boxed{
C(N)=O(N).
}
\tag{6}
\]

### Proof sketch

For powers \(w=2^j\), (3) reduces to

\[
f(2^j)\le2\rho\,f(2^{j-1})+\kappa.
\]

Write \(q=2\rho\).

- If \(q>1\), then \(f(2^j)=O(q^j)\). Since
  \(j=\log_2 w\),
  \[
  q^j=w^{\log_2q}=w^\alpha.
  \]
- If \(q=1\), then \(f(2^j)=O(j)=O(\log w)\).
- If \(q<1\), the affine recurrence is bounded.

Odd \(w\) only changes the two children by one bit, and the same asymptotic
induction applies.

Multiplying by \(N=2^w\) proves (4)–(6).

QED.

-------------------------------------------------------------------------------
4. Why the half-union threshold is the real target
-------------------------------------------------------------------------------

A finite uniform saving such as

\[
\rho=0.999
\]

already yields a true power saving because

\[
\log_2(2\rho)<1.
\]

But the strongest regime occurs at

\[
\boxed{\rho=\frac12.}
\]

At that point, two recursive axis banks cost only as much as **one**
separate bank, up to linear overhead.

Then the \(\log N\)-level recursion collapses to recursion depth on the
bit-length:

\[
w\to w/2\to w/4\to\cdots,
\]

hence only

\[
O(\log\log N)
\]

linear-work macro levels.

This is the central GTSL objective.

-------------------------------------------------------------------------------
5. Relation to the current public tensor-saving result
-------------------------------------------------------------------------------

The 2026 public exact-Fourier result already proves sub-\(N\log N\)
complexity by a finite tensor saving, and separately gives a uniform

\[
O\!\left(N(\log N)^{1-10^{-13}}\right)
\]

algorithm in an exact-complex supplied-root model.

GTSL does **not** claim that "tensor saving implies Fourier speedup" is new.

The project-specific stronger target is:

\[
\boxed{
\rho(w)\longrightarrow\frac12
}
\]

through a growing family of explicit Fourier-specific Green/scan union
macros.

A fixed saving gives a fixed power \((\log N)^\alpha\).

The half-union limit changes the complexity class to

\[
N\log\log N,
\]

and a strict half-union gives linear time.

-------------------------------------------------------------------------------
6. How much saving would beat the current uniform comparator?
-------------------------------------------------------------------------------

The fixed-saving exponent is

\[
\alpha=\log_2(2\rho).
\]

To beat a comparator

\[
N(\log N)^{1-\delta},
\]

it is enough that

\[
\log_2(2\rho)<1-\delta,
\]

or

\[
\boxed{
\rho<2^{-\delta}.
}
\tag{7}
\]

For the reported

\[
\delta=10^{-13},
\]

even an extremely small **uniform** improvement below
\(2^{-10^{-13}}\) would asymptotically improve the exponent.

GTSL aims much further: \(\rho\to1/2\).

-------------------------------------------------------------------------------
7. Phase 36 volume tax: why coefficients must grow
-------------------------------------------------------------------------------

The project's Phase 36 gives, for a fan-in-two exact complex linear DAG,

\[
\sum_j
\log_2\max(1,|a_j|+|b_j|)
\ge
\frac N2\log_2N
\tag{8}
\]

for the unnormalized Fourier matrix.

Suppose a GTSL circuit has

\[
s(N)
\le
K N(\log_2N)^\alpha
\]

single-output gates.

Then at least one gate obeys

\[
\boxed{
|a_j|+|b_j|
\ge
2^{
(\log_2N)^{1-\alpha}/(2K)
}.
}
\tag{9}
\]

Indeed the maximum log-weight is at least the average required budget.

Therefore any genuine \(\alpha<1\) tensor-union compiler must deliberately
leave the bounded-coefficient model.

This is not a bug.

It is a design contract:

> **shared tensor work must be paid for by controlled coefficient
> amplification.**

For an \(O(N)\) circuit (\(\alpha=0\)), polynomially growing coefficient
magnitudes are unavoidable in this model.

GTSL therefore records coefficient height at every macro rather than
silently assuming unit-modulus twiddles.

-------------------------------------------------------------------------------
8. Why our project has useful seed structures
-------------------------------------------------------------------------------

## 8.1 Phase 56: exact nonseparable Green Fourier factorizations

Phase 56 rigorously certifies finite exact factorizations

\[
F_N=L\,S_2 D S_1\,R
\]

at

\[
N=5,7,8,11,13,
\]

where each \(S_i\) is a sum of independently ordered Hamiltonian Green
resolvents.

These codelets are not asymptotically fast—the total Green inventory is
\(N-1\)—but they prove that exact Fourier phase structure can live in
**nonseparable scan networks**, not only standard butterflies.

Their Green terms have one-pass prefix executors, making them useful atoms
for union search.

## 8.2 Phase 45 / Winograd scalar sharing

The project has exact fixed-size examples where a fused tensor/Winograd
kernel uses fewer online operations than a more axis-separable comparator,
and Phase 45 shows large root/twiddle banks can share a much smaller exact
coefficient table.

This does not imply an asymptotic saving.

It does show that:

- tensor-axis separation is not automatically arithmetic-optimal;
- scalar preparation can be shared without hiding it;
- exact finite-field auditing of the complete fused graph is already part
  of the project workflow.

## 8.3 Green diagonal conjugacy

If

\[
G=(I-W)^{-1}
\]

and \(D\) is invertible diagonal, then

\[
DGD^{-1}
=
(I-DWD^{-1})^{-1}.
\]

So Cooley–Tukey twiddle diagonals can be pushed through a Green scan by
reweighting its cycle edges.

This means recursive axis networks can be algebraically rearranged before
we count common prefix/suffix states.

That is the main GTSL fusion handle.

-------------------------------------------------------------------------------
9. Green Tensor-Union Compiler Conjecture
-------------------------------------------------------------------------------

Take the exact balanced Cooley–Tukey macro for

\[
N=ab,\qquad a\approx b\approx\sqrt N.
\]

Replace the recursive child transforms by their current best exact
Green/scan/DAG representations.

Push all diagonal twiddles as far as possible through Green terms using
diagonal conjugacy.

Canonicalize all intermediate linear forms over the cyclotomic field.

Then merge:

- identical prefix traces;
- identical suffix traces;
- shared weighted totals;
- shared sparse edge updates;
- common input-independent scalar chains;
- common tensor-axis subexpressions.

### Conjecture 9.1 — Half-Union

There is a uniform exact family for dyadic \(N=2^w\) with

\[
\boxed{
\rho(w)\le\frac12+o(1)
}
\tag{10}
\]

and \(O(N)\) nonrecursive overhead per balanced merge.

A stronger form has eventually

\[
\rho(w)\le\frac12.
\]

An even stronger form has

\[
\rho(w)\le\frac12-\varepsilon
\]

for a fixed \(\varepsilon>0\).

Consequences:

- \(\rho=1/2\): \(O(N\log\log N)\);
- \(\rho<1/2\): \(O(N)\);
- any fixed \(\rho<1\): an explicit power saving.

-------------------------------------------------------------------------------
10. What "union" is allowed to do
-------------------------------------------------------------------------------

A macro may:

1. create new linear forms with arbitrary prepared complex scalars;
2. reuse any previously computed form;
3. use exact Green prefix/suffix recurrences;
4. insert sparse permutations and diagonal scalings;
5. exploit tensor-axis symmetries;
6. use coefficient amplification, fully recorded;
7. share input-independent scalar tables.

It may NOT:

- charge a dense transform as one gate;
- invoke an uncharged smaller FFT;
- use repeated-input caching;
- use parallel wall time instead of sequential work;
- hide \(N^2\) precomputed data;
- count only exotic multiplications while ignoring additions.

The final macro is flattened to a one-output linear DAG and verified
entrywise.

-------------------------------------------------------------------------------
11. Exact certification contract
-------------------------------------------------------------------------------

For every proposed merge:

1. emit the complete scalar DAG;
2. canonicalize coefficients in the appropriate cyclotomic field;
3. verify all \(N^2\) transfer entries for research sizes;
4. verify the equivalent Weyl relation
   \[
   MX=ZM,\qquad Me_0=\mathbf1
   \]
   at the final transform;
5. count every addition/subtraction and nonidentity scalar multiplication;
6. count scalar preparation separately;
7. record maximum coefficient modulus and the Phase-36 volume budget;
8. record live-memory and index/routing work.

The existing `linear_dag_certifier.py` is already designed for this style of
exact audit.

-------------------------------------------------------------------------------
12. First decisive experiments
-------------------------------------------------------------------------------

### A. N=16 -> balanced 4 x 4 merge

Construct the two ordinary child banks and the twiddle layer exactly.

Replace each 4-point child with every available exact small Green/WFTA
representation.

Search for a union DAG with cost

\[
<
\rho
\bigl[
4C(4)+4C(4)
\bigr]
+
\kappa16
\]

for the smallest possible \(\rho\).

### B. N=64 -> balanced 8 x 8 merge

Use:

- the exact Phase-56 8-point Green Fourier factorization;
- the archived 8-point WFTA;
- ordinary radix/split-radix representations.

Push the 64-point twiddle diagonal through each representation and perform
global common-subexpression elimination.

Measure

\[
\boxed{
\rho_6
=
\frac{
C_{\rm union}(64)-\kappa64
}{
8C(8)+8C(8)
}.
}
\]

### C. N=256 -> 16 x 16 merge

Do not search from scratch.

Lift only algebraic patterns that survived N=64 and use the exact
cyclotomic DAG verifier.

The key statistic is the sequence

\[
\rho_4,\rho_6,\rho_8,\ldots
\]

not one isolated codelet win.

GTSL needs evidence that this sequence trends toward \(1/2\).

-------------------------------------------------------------------------------
13. A useful scaling lemma for a discovered macro family
-------------------------------------------------------------------------------

Suppose an exact symbolic rewrite schema works for every balanced dyadic
pair and proves

\[
\rho(w)
\le
\rho_*+\frac{c}{w^\gamma}
\]

for some \(\rho_*<1\).

Then:

- if \(\rho_*>1/2\), GTSL gives a fixed power saving;
- if \(\rho_*=1/2\), the remaining asymptotic is at most
  \(N\) times a polylogarithm in \(\log N\), with the exact power depending
  on the convergence rate;
- if \(\rho_*<1/2\), the normalized recurrence is contracting and total
  work is \(O(N)\).

Thus a growing rewrite pattern is mathematically far more valuable than a
better fixed-size FFT constant.

-------------------------------------------------------------------------------
14. Falsifiers
-------------------------------------------------------------------------------

Reject GTSL if one proves any of:

1. **Tensor-axis direct-sum rigidity:** in the allowed exact scan/DAG grammar,
   \[
   \rho(w)\ge1-o(1).
   \]
2. Green prefix traces from the two balanced axes are algebraically
   independent except for \(o\) of the total work.
3. Any \(\rho<1\) union needs scalar preparation or coefficient
   representation of \(\Omega(N\log N)\) work.
4. Coefficient amplification required by the volume budget destroys the
   exact unit-cost model once a bit/precision model is charged.
5. All observed finite savings reduce to one fixed tensor gadget already
   covered by the known finite-tensor-savings framework, with no improving
   \(\rho(w)\).

Any such result is a meaningful restricted barrier.

-------------------------------------------------------------------------------
15. Novelty boundary
-------------------------------------------------------------------------------

Classical / current ingredients include:

- Cooley–Tukey;
- multidimensional and vector-radix FFTs;
- Winograd codelets;
- tensor products/Kronecker transforms;
- bounded-coefficient determinant lower bounds;
- the 2026 finite-tensor-savings exact-Fourier construction.

Therefore GTSL does **not** claim invention of tensor-axis sharing or finite
tensor savings.

The project-specific target is the stronger asymptotic mechanism

\[
\boxed{
\text{growing exact Green/scan union}
\quad\Longrightarrow\quad
\rho(w)\to\frac12,
}
\]

together with an explicit coefficient-amplification ledger and all-input
cyclotomic DAG verification.

That stronger half-union conjecture is presently unproved.

-------------------------------------------------------------------------------
16. Bottom line
-------------------------------------------------------------------------------

Let

\[
f(w)=C(2^w)/2^w.
\]

Ordinary Cooley–Tukey has essentially

\[
f(w)\approx
f(w/2)+f(w/2)+O(1).
\]

GTSL asks for

\[
f(w)
\le
\rho(w)
\left[
f(w/2)+f(w/2)
\right]
+O(1).
\]

The thresholds are exact:

\[
\boxed{
\rho<1
\Rightarrow o(N\log N),
}
\]

\[
\boxed{
\rho=\tfrac12
\Rightarrow O(N\log\log N),
}
\]

\[
\boxed{
\rho<\tfrac12
\Rightarrow O(N).
}
\]

Our existing Green, Winograd, scalar-sharing and exact-DAG results give
concrete atoms for searching such union macros.

The new research question is no longer
"find another Fourier factorization."

It is:

> **Can two balanced recursive Fourier banks be algebraically unioned so
> that asymptotically only one bank's worth of input-dependent work
> remains?**
