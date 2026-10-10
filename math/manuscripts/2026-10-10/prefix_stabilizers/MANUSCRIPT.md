# Prefix stabilizer maxima and recursive coset orderings

Working manuscript. 10 October 2026 UTC.

## Abstract

For an ordering of the elements of a finite group, consider the sum of the orders of its nonempty prefix stabilizers, subtracting one at each prefix. We prove that its maximum is

\[
|G|\sum_{p\mid |G|}v_p(|G|)(1-1/p)
\]

when every pair of subgroups of the group permutes, and separately when the group is a finite prime power group. In either class, every maximizing ordering consists recursively of consecutive right cosets of a maximal subgroup, with independent maximizing orders inside the cosets. The top subgroup is recovered uniquely from the stabilizers of all proper prefixes. This characterization gives an exact recurrence for the number of labeled maximizing orderings. The symmetric group of degree three has 360 maximizing orderings, including 144 outside this hierarchy, and therefore bounds the structural theorem's scope. The proofs are complete within the stated hypotheses. Historical priority for the optimizer characterization remains unresolved; the counting principle and several related constructions are classical.

## 1 Scope and notation

Let \(G\) be a finite group of order \(m\), with identity \(e\), acting on itself by left multiplication. An ordering is a sequence \(\mathbf{x}=(x_1,\ldots,x_m)\) containing every element exactly once. Write

\[
T_j=\{x_1,\ldots,x_j\},\qquad
H_j=\operatorname{Stab}_G(T_j)=\{g\in G:gT_j=T_j\},
\]

\[
Z_G(\mathbf{x})=\sum_{j=1}^{m}(|H_j|-1),\qquad
M(G)=\max_{\mathbf{x}} Z_G(\mathbf{x}),
\tag{1}
\]

and

\[
W(m)=\sum_{p\text{ prime}}v_p(m)(1-1/p),\qquad W(1)=0.
\tag{2}
\]

The full prefix is included: \(H_m=G\), contributing \(m-1\). This convention matters for every formula below.

All elements remain labeled. Let \(A(G)\) be the number of maximizing orderings; no quotient by automorphisms or translations is taken.

A finite group is called *quasihamiltonian* here precisely when \(UV=VU\) for all subgroups \(U,V\leq G\). This is the pairwise subgroup permutability condition used in [BS20, p.2]. The weaker term *finitely quasihamiltonian* in that source is not a substitute for this hypothesis. Abelian groups satisfy the required condition. We treat all finite \(p\)-groups in a separate proof; they need not have pairwise permutable subgroups.

Under the left regular action, the orbits of a subgroup \(K\) are right cosets \(Kx\). A coset is identified with \(K\) by \(hx\mapsto h\). Changing the chosen representative changes this identification by right translation within \(K\), which preserves every left stabilizer. Thus optimization inside a coset is well defined, independently of this choice.

Define a *recursive coset ordering* without reference to optimality. The singleton group has its unique ordering. For a nontrivial group choose a maximal proper subgroup \(K\), place its distinct right cosets in any order as consecutive blocks, and in each block use a recursive coset ordering of \(K\) through the identification just described. The choices made in different blocks are independent.

This manuscript consolidates the accepted abelian proof and its nonabelian extensions [P1–P4]. Its theorem-specific proofs are given below. The only standard general group facts assumed are Lagrange's theorem, Sylow's theorem, the conjugacy-class equation, elementary quotient-group facts, and the integer Chinese remainder theorem; the required normalizer and maximal-subgroup deductions are proved explicitly. No unproved classification theorem, numerical experiment, or inaccessible prior-art result is a premise.

## 2 Main results

**Theorem 1.** Suppose that \(G\) satisfies at least one of the following conditions:

1. Every pair of subgroups of \(G\) permutes setwise.
2. \(|G|=p^a\) for a prime \(p\) and an integer \(a\geq 0\).

Then:

**Value.**
\[
M(G)=mW(m).
\tag{3}
\]

**Equality cases.** An ordering maximizes \(Z_G\) if and only if it is a recursive coset ordering. Equivalently, its top-level blocks are the right cosets of some maximal subgroup \(K\), and every induced block ordering maximizes the corresponding objective on \(K\).

**Unique top subgroup.** If \(m>1\), the top subgroup in that description is uniquely determined by the ordering, and equals
\[
K=\langle H_1,\ldots,H_{m-1}\rangle.
\tag{4}
\]

**Labeled count.**
\[
A(1)=1,\qquad
A(G)=\sum_{K\text{ maximal in }G}[G:K]!\,A(K)^{[G:K]}
\quad (m>1).
\tag{5}
\]

Every maximal subgroup occurring in this theorem is normal and has prime index. The subgroup classes in the hypotheses are inherited by subgroups, so all recursive stages remain within the theorem.

**Theorem 2.** If \(|G|=p^a\), an ordering is maximizing if and only if
\[
|H_j|=\gcd(j,p^a)\quad\text{for every }1\leq j\leq p^a.
\tag{6}
\]

In particular,
\[
M(G)=a(p-1)p^{a-1}=a|G|(1-1/p)
\tag{7}
\]

for \(a\geq1\). For \(a=0\), the value is zero. For a nontrivial \(p\)-group, equation (5) becomes
\[
A(G)=p!\sum_{K\text{ maximal in }G}A(K)^p.
\tag{8}
\]

The term *unique* in (4) concerns a given optimal ordering. Different optimal orderings may have different top subgroups. It does not say that all prefix stabilizers of one ordering are nested.

## 3 Preliminary group facts

### 3.1 Regular action and translations

**Lemma 3.1.** If a nonempty subset \(S\subseteq G\) has stabilizer \(H\), then \(|H|\) divides both \(|S|\) and \(|G|\). Moreover,
\[
\operatorname{Stab}_G(S)=\operatorname{Stab}_G(G\setminus S),
\]

and right translation preserves the stabilizer as a subgroup:
\[
\operatorname{Stab}_G(Sy)=\operatorname{Stab}_G(S).
\]

**Proof.** The left action of \(H\) is free: \(hs=s\) implies \(h=e\). Hence every \(H\)-orbit in \(S\) has \(|H|\) elements; Lagrange's theorem gives the second divisibility. Left multiplication is a permutation of \(G\), so it preserves a subset exactly when it preserves its complement. Finally, \(gSy=Sy\) is equivalent to \(gS=S\). ∎

In particular, \(|H_j|\leq\gcd(j,m)\). In mixed-prime orders the separate pointwise bounds need not be jointly attainable; the next sections handle that compatibility issue.

### 3.2 Maximal subgroups of prime power groups

**Lemma 3.2.** Every maximal proper subgroup of a nontrivial finite \(p\)-group is normal of index \(p\).

**Proof.** First prove that every proper subgroup \(L<P\) is strictly contained in its normalizer \(N_P(L)\). The class equation gives a nontrivial center \(Z(P)\). If \(Z(P)\not\subseteq L\), a central element outside \(L\) lies in \(N_P(L)\setminus L\). Otherwise \(Z(P)\subseteq L\), and induction on \(|P|\) applies to the proper subgroup \(L/Z(P)\) of \(P/Z(P)\). An element of its normalizer outside \(L/Z(P)\) lifts to an element of \(N_P(L)\setminus L\). This proves the normalizer assertion, including the base cases.

If \(L\) is maximal, \(N_P(L)>L\) forces \(N_P(L)=P\), so \(L\) is normal. The quotient \(P/L\) is a nontrivial \(p\)-group with no nontrivial proper subgroup. Choose a nonidentity element. It must generate the quotient; a cyclic group of order \(p^b\) with \(b>1\) has a nontrivial proper subgroup. Thus \(|P/L|=p\). ∎

### 3.3 Maximal subgroups under permutability

**Lemma 3.3.** If every pair of subgroups of a finite group \(G\) permutes, every maximal proper subgroup of \(G\) is normal of prime index.

**Proof.** If subgroups \(U,V\) satisfy \(UV=VU\), their product is a subgroup, and
\[
|UV|=|U||V|/|U\cap V|.
\]

Let \(P\) be a Sylow \(p\)-subgroup. For any \(g\in G\), the product \(P(gPg^{-1})\) is a \(p\)-subgroup containing \(P\). The Sylow order is maximal, so \(gPg^{-1}=P\). Consequently every Sylow subgroup is normal.

Normal subgroups of coprime orders commute elementwise: each commutator belongs to their trivial intersection. Therefore \(G\) is the direct product of its Sylow subgroups \(P_p\). Every subgroup \(K\leq G\) decomposes as
\[
K=\prod_p(K\cap P_p).
\]

Indeed, for \(x\in K\), its commuting prime-power components can each be expressed as a power of \(x\), using the Chinese remainder theorem on their pairwise coprime orders. Thus every component belongs to \(K\).

If \(K<G\) is maximal, all but one of its Sylow components must equal the corresponding \(P_p\); otherwise enlarging one deficient component gives a proper intermediate subgroup. In the remaining component, \(K\cap P_p\) must be maximal. Lemma 3.2 makes that component normal of index \(p\). Hence \(K\) is normal in \(G\) and has index \(p\). ∎

Pairwise permutability is inherited by subgroups: any two subgroups of a subgroup are also subgroups of \(G\). No classification of quasihamiltonian groups is required.

## 4 Coset restriction and consecutive blocks

The next two lemmas isolate the accounting and equality arguments. Neither requires the group itself to satisfy a hypothesis of Theorem 1 beyond the explicitly stated subgroup conditions.

### 4.1 Exact local accounting

**Lemma 4.1.** Let \(K<G\) contain every proper-prefix stabilizer of an ordering \(\mathbf{x}\). Write \(k=|K|\) and \(q=[G:K]\). Restrict the ordering to each right coset \(C\) of \(K\); after identifying \(C\) with \(K\), let \(Z_C\) be its local objective. At insertion \(j\), set
\[
C_j=Kx_j,\quad U_j=T_j\cap C_j,\quad
L_j=\{h\in K:hU_j=U_j\}.
\]

Then \(H_j\leq L_j\) for \(j<m\), and
\[
Z_G(\mathbf{x})
=\sum_C Z_C+m-k-\sum_{j<m}(|L_j|-|H_j|)
\leq qM(K)+m-k.
\tag{9}
\]

Equality in the final inequality holds exactly when every local ordering is optimal and \(H_j=L_j\) for all \(j<m\).

**Proof.** For \(j<m\), an element of \(H_j\) lies in \(K\), hence preserves the coset \(C_j\), and it preserves \(T_j\). It therefore preserves their intersection \(U_j\), giving the inclusion.

For each fixed coset, its active intersections \(U_j\), at the insertions lying in that coset, run through all nonempty prefixes of the induced ordering exactly once. Thus
\[
\sum_{j=1}^{m}(|L_j|-1)=\sum_C Z_C.
\]

At the final insertion \(L_m=K\) and \(H_m=G\), so the difference of final weights is \(m-k\). Subtracting the nonfinal inclusion deficits gives the identity in (9). The deficits and the local losses \(M(K)-Z_C\) are nonnegative; equality of their sum to zero is equivalent to equality of every one. Finite subgroup inclusion and equal orders give \(H_j=L_j\). ∎

### 4.2 Exact stabilizers of a block ordering

**Lemma 4.2.** Suppose \(K\lhd G\) has prime index \(q\). For an ordering consisting of consecutive right cosets of \(K\), every proper-prefix stabilizer lies in \(K\). Inside a partial block it equals the local stabilizer, and at each proper block boundary it is exactly \(K\). Consequently
\[
Z_G(\mathbf{x})=\sum_C Z_C+m-k.
\tag{10}
\]

**Proof.** Normality ensures that left multiplication permutes the right cosets of \(K\). A prefix stopping strictly inside a block has exactly one partially occupied coset; every other coset is empty or full. A stabilizing element must fix this unique partial coset. Since \(gKx=Kx\) implies \(gK=K\), it lies in \(K\). Conversely, an element of \(K\) fixes each full or empty coset, so it stabilizes the whole prefix precisely when it stabilizes its local partial block.

At a proper block boundary, the prefix corresponds to a nonempty proper subset of \(G/K\). This quotient has prime order. Every nonidentity element acts transitively by translation, so such a subset has trivial quotient stabilizer. The full stabilizer is therefore exactly \(K\). The final insertion has stabilizer \(G\), yielding (10). ∎

### 4.3 Equality forces whole blocks

**Lemma 4.3.** In the setting of Lemma 4.1, if equality holds in (9), the ordering consists of consecutive right cosets of \(K\), and its induced orders are optimal.

**Proof.** Local optimality and \(H_j=L_j\) follow from Lemma 4.1. Consider the insertion at which the first coset becomes complete. This is a proper prefix because at least two cosets exist. Its active local stabilizer is \(K\), hence \(H_j=K\). The whole prefix is then a union of right \(K\)-cosets. All other cosets must be empty or full. None was already full, by the choice of completion time, and one insertion completes only its own coset. Therefore all other cosets are empty. The first \(k\) elements are one complete coset.

Inductively suppose the first \(r\) completed cosets have appeared as consecutive blocks with no other coset touched. At the next completion, provided \(r+1<q\), the same equality gives \(H_j=K\), so among the remaining cosets only this one can be full and every other one is empty. Thus it forms the next block. The final coset occupies all remaining positions automatically. ∎

This argument does not assume that stabilizers of earlier prefixes continue to stabilize later prefixes.

## 5 Proof for pairwise permutable subgroups

### 5.1 Accumulation of proper-prefix stabilizers

**Lemma 5.1.** Suppose every pair of subgroups of \(G\) permutes. Put
\[
B_j=\langle H_1,\ldots,H_j\rangle.
\]

Then \(B_jx_1\subseteq T_j\) for every \(j\). In particular, \(B_{m-1}<G\) when \(m>1\).

**Proof.** The first stabilizer is trivial, so the assertion holds for \(j=1\). By subgroup permutability,
\[
B_j=H_jB_{j-1}.
\]

If \(B_{j-1}x_1\subseteq T_{j-1}\subseteq T_j\), then
\[
B_jx_1=H_jB_{j-1}x_1\subseteq H_jT_j=T_j.
\]

Induction proves the containment. Since \(T_{m-1}\) is proper, it cannot contain the entire right coset \(Gx_1=G\); hence \(B_{m-1}\neq G\). ∎

Only containment of one accumulated subgroup coset is asserted. The stabilizers themselves need not form a chain.

### 5.2 Value and complete equality cases

Proceed by induction on \(m\), with the singleton immediate. For any ordering choose a maximal subgroup \(K\) containing \(B_{m-1}\). Lemma 3.3 gives \(K\lhd G\) and prime index \(q\). By Lemma 4.1 and the inductive theorem on \(K\),
\[
Z_G\leq qM(K)+m-k
=qkW(k)+m-k
=m\bigl(W(k)+1-1/q\bigr)=mW(m).
\tag{11}
\]

Here \(m=qk\), and the last equality follows directly from the prime valuation definition of \(W\).

Conversely, choose any maximal subgroup \(K\), arrange its cosets consecutively, and choose optimal induced orders, available by induction. Lemma 4.2 gives equality in (11). Thus \(M(G)=mW(m)\).

If an ordering is optimal, the same choice of \(K\supseteq B_{m-1}\) gives equality at every step of (11). Lemma 4.3 forces consecutive coset blocks and optimal induced orders. Induction applies independently inside each block. Conversely, every recursively constructed ordering attains (11). This proves the value and equality characterization in case 1 of Theorem 1.

A useful exact restatement of the proof, for the chosen \(K\), is
\[
mW(m)-Z_G
=\sum_C\bigl(kW(k)-Z_C\bigr)
+\sum_{j<m}(|L_j|-|H_j|).
\tag{12}
\]

Every term is a nonnegative integer. This identity is part of the accounting proof, not a quantitative stability theorem for some separately defined distance between orderings.

## 6 Proof for all finite prime power groups

The accumulation lemma is not assumed in this section.

### 6.1 Value and pointwise saturation

Let \(m=p^a\) with \(a\geq1\). Lemma 3.1 gives
\[
Z_G\leq\sum_{j=1}^{p^a}\bigl(\gcd(j,p^a)-1\bigr).
\]

For each \(0\leq t<a\), exactly \((p-1)p^{a-t-1}\) indices in \(\{1,\ldots,p^a\}\) have \(p\)-adic valuation \(t\). The final index has greatest common divisor \(p^a\). Therefore
\[
\sum_{j=1}^{p^a}\gcd(j,p^a)
=\sum_{t=0}^{a-1}p^t(p-1)p^{a-t-1}+p^a
=a(p-1)p^{a-1}+p^a.
\]

Subtracting \(p^a\) proves the upper bound in (7).

Inductively choose a maximal subgroup \(K\), which is normal of index \(p\) by Lemma 3.2. Consecutive coset blocks with optimal local orders attain, by Lemma 4.2,
\[
p\,(a-1)|K|(1-1/p)+|G|-|K|
=a|G|(1-1/p).
\]

The formula includes \(a=1\) with singleton local groups. Hence the upper bound is attained. All pointwise deficits \(\gcd(j,p^a)-|H_j|\) are nonnegative; their sum vanishes exactly when each vanishes. This proves Theorem 2.

### 6.2 Saturation forces a common top subgroup

Let an ordering be optimal and set \(k=p^{a-1}\). At \(j=k\), equation (6) gives \(|H_k|=k\). Put \(K=H_k\). Since the prefix has \(k\) elements and is \(K\)-invariant,
\[
T_k=Kx_1.
\]

This subgroup is maximal and normal by Lemma 3.2. At any proper block boundary \(j=tk\), where \(1\leq t<p\), saturation also gives \(|H_{tk}|=k\). Let \(J=H_{tk}\), another normal maximal subgroup. The prefix \(T_{tk}\) contains \(Kx_1\) and is \(J\)-invariant, so it contains \(JKx_1\). If \(J\neq K\), the product \(JK\) is a subgroup strictly containing the maximal subgroup \(K\), hence equals \(G\). This would make the proper prefix all of \(G\), a contradiction. Therefore
\[
H_{tk}=K\qquad(1\leq t<p).
\tag{13}
\]

Each such boundary prefix is a union of exactly \(t\) right cosets of \(K\). Including \(T_0=\varnothing\) and \(T_m=G\), the successive differences
\[
T_{tk}\setminus T_{(t-1)k},\qquad 1\leq t\leq p,
\]

are \(K\)-invariant sets of size \(k\), hence single right cosets. Thus the ordering has consecutive \(K\)-coset blocks. This argument also covers \(p=2\), where the only proper boundary is the first one and its complement supplies the second block.

By Lemma 4.2, the global value is \(\sum_C Z_C+m-k\). Every \(Z_C\leq M(K)\), and the attained global value equals \(pM(K)+m-k\). Thus every local order is optimal. Induction proves the recursive characterization; the attainment construction proves its converse. This completes case 2 of Theorem 1 apart from the common uniqueness and counting conclusions.

## 7 Unique recovery and enumeration

Take an optimal ordering under either hypothesis, with top subgroup \(K\) and \(k=|K|\). Lemma 4.2 shows \(H_j\leq K\) for every \(j<m\). The first completed block occurs at \(j=k<m\), where \(H_k=K\). Hence
\[
\langle H_1,\ldots,H_{m-1}\rangle=K.
\]

This proves (4) and rules out representing one optimal ordering with two different top subgroups. When \(k=1\), the group has prime order, all proper nonempty prefix stabilizers are trivial, and the same equation recovers the trivial top subgroup. For the singleton there is no top subgroup to recover.

Fix a maximal subgroup \(K\) of index \(q\). Its \(q\) distinct cosets may be ordered in \(q!\) ways. Fix one representative for each coset solely to identify it with \(K\). Each block has exactly \(A(K)\) possible optimal orders. The choices are independent, giving
\[
q!A(K)^q
\]

optimal orders with that top subgroup. Changing the representatives provides different coordinates for the same orders and contributes no additional factor. Unique recovery makes the classes for distinct top subgroups disjoint. Summing them proves (5), and the common index \(p\) proves (8).

The sum, factorial, and independent-product mechanisms are standard combinatorial counting. Prior subgroup-chain recursion and rooted-tree product constructions are discussed in Section 10. The objective-specific work is the classification and the proof that top choices cannot overlap.

## 8 Examples and the limits of nesting

### 8.1 Small exact counts

For a cyclic group, each prime divisor \(q\mid m\) gives exactly one maximal subgroup of index \(q\). Thus
\[
A(C_1)=1,\qquad
A(C_m)=\sum_{q\mid m,\ q\text{ prime}}q!\,A(C_{m/q})^q.
\tag{14}
\]

A prime-order group has \(A(C_p)=p!\). For example,
\[
A(C_4)=2!(2!)^2=8,\qquad
A(C_6)=2!(3!)^2+3!(2!)^3=120,
\]
\[
A(C_8)=2\cdot 8^2=128,\qquad
A(C_{12})=2\cdot120^2+6\cdot8^3=31{,}872.
\]

The group \(C_2\times C_2\) has three maximal subgroups of order two, so its count is \(3\cdot2!\cdot(2!)^2=24\). The quaternion group \(Q_8\) has three maximal subgroups isomorphic to \(C_4\), giving \(A(Q_8)=3\cdot2!\cdot8^2=384\). The dihedral group \(D_8\) of order eight has one maximal \(C_4\) and two maximal \(C_2\times C_2\), giving
\[
A(D_8)=2!\bigl(8^2+2\cdot24^2\bigr)=2{,}432.
\]

The maxima for all groups of order four are 4, and for all groups of order eight covered here are 12. Counts distinguish group structure even when the maximum depends only on order. These values agree with the saved independent controls [P2, P4].

### 8.2 Independent branching inside cosets

In additive \(C_{12}\), consider
\[
0,6,2,8,4,10,\ 1,5,9,3,7,11.
\]

Its prefix stabilizer orders are
\[
1,2,1,2,1,6,\ 1,1,3,1,1,12,
\]

and its score is 20, which equals \(12W(12)\). Its top subgroup is the even residues. Inside that first coset the order uses a subgroup of order two; inside the second it uses a subgroup of order three. The proper-prefix stabilizers at positions two and nine have orders two and three and are not nested. This is why the theorem allows independent choices in different cosets rather than restricting all blocks to one fixed subgroup chain. The displayed orders and score have been checked directly in the accompanying validation.

## 9 The symmetric group of degree three

The next proposition concerns a group outside both hypotheses. It is included to prevent a universal interpretation of the structural theorem.

**Proposition 9.1.** In \(S_3\), \(M(S_3)=7\) and \(A(S_3)=360\). Exactly 216 optimal orders are recursive right-coset orders, and the other 144 are not.

**Proof of the value.** Put \(a=(12)\) and \(b=(23)\), composing rightmost first. The order
\[
e,a,b,ba,ab,aba
\]

has prefix stabilizers
\[
\{e\},\langle a\rangle,\{e\},\langle b\rangle,\{e\},S_3.
\tag{15}
\]

For the fourth prefix, \(T_4=\langle b\rangle\langle a\rangle\) is invariant under \(\langle b\rangle\); its stabilizer order divides \(\gcd(4,6)=2\), so this is the full stabilizer. The other entries follow directly, or by complementation and Lemma 3.1. The score is \(1+1+5=7\).

For any order, the first and fifth stabilizers are trivial and the final one is \(S_3\). The only possible nonzero proper-prefix terms satisfy
\[
|H_2|-1\leq1,\qquad |H_3|-1\leq2,\qquad |H_4|-1\leq1.
\]

If \(|H_3|=3\), the first three elements form a right coset of \(A_3\), hence all have the same parity. A pair of equal-parity elements has no nontrivial left stabilizer: an exchanging translation would have to be an odd involution. Thus \(H_2\) is trivial. The complement of \(T_4\) is a pair in the other parity coset, so \(H_4\) is also trivial. The score is then 7. If \(H_3\) is trivial, the score is at most \(5+1+1=7\). This proves the maximum.

**Proof of the count.** If \(|H_3|=3\), choose the first parity coset in two ways and order both triples arbitrarily. This gives \(2(3!)^2=72\) optimal orders.

Otherwise optimality requires \(|H_2|=|H_4|=2\). A pair in \(S_3\) has a nontrivial left stabilizer exactly when its elements have opposite parity: their ratio is then a transposition and exchanges them. Consequently the first and final unordered pairs must each have opposite parity. There are \(3\cdot3=9\) choices for the first pair, and \(2\cdot2=4\) choices for the disjoint final pair. The remaining pair occupies the middle. Ordering each pair gives \(2!^3=8\) choices. All these orders have mixed parity in the first triple, so its stabilizer is trivial. There are therefore \(9\cdot4\cdot8=288\) orders of this second type, for a total of 360.

All 72 first-type orders are hierarchical with top \(A_3\). In the second type a hierarchy must have an order-two top subgroup equal to \(H_2\). The first pair determines one of its three right cosets; either of its other two cosets can be the final pair, after which the middle pair is the last coset. Hence exactly \(9\cdot2\cdot8=144\) second-type orders are hierarchical. Thus 216 are hierarchical and 144 are not. ∎

For the order in (15), \(\langle H_2,H_4\rangle=S_3\). A proper accumulated subgroup is therefore unavailable, even at an optimum. Substituting \(S_3\) into (5) outside its hypotheses gives
\[
2!A(C_3)^2+3\cdot3!A(C_2)^3=72+144=216,
\]

which misses the 144 nonhierarchical optimizers. This refutes the unrestricted characterization and counting formula. It does not refute the numerical value \(|G|W(|G|)\), which still equals 7 in this case. All groups of smaller order are abelian: groups of prime order are cyclic, while a group of order four is cyclic or every nonidentity element has order two, which forces commutativity. Thus \(S_3\) is a smallest-order structural counterexample.

**Proposition 9.2.** Every finite solvable group has an ordering of score \(|G|W(|G|)\); consequently \(M(G)\geq |G|W(|G|)\).

**Proof.** A nontrivial solvable group has nontrivial abelianization, since otherwise its derived series could not reach the identity. A maximal proper subgroup of this finite abelian quotient gives a quotient of prime order, so \(G\) has a normal prime-index subgroup \(K\). The subgroup \(K\) is solvable. Inductively construct local orders with score \(|K|W(|K|)\) and concatenate their cosets. Lemma 4.2 gives score \(|G|W(|G|)\). ∎

No upper bound for all solvable groups, all finite groups, or all mixed-order nilpotent groups is proved in this manuscript. Nor is (5) asserted for these broader classes.

## 10 Prior art and the precise contribution boundary

### 10.1 Existing statistics and constructions

Label \(G\) by the chosen order. For \(g\in G\), let \(\sigma_g\) be the induced permutation of \(\{1,\ldots,m\}\), and let
\[
C(\sigma_g)=\{j<m:\sigma_g(\{1,\ldots,j\})=\{1,\ldots,j\}\}.
\]

This is the connectivity statistic of [Sta05, equation (1)]. A direct double count gives
\[
\sum_{g\in G}|C(\sigma_g)|
=\sum_{j<m}|H_j|
=Z_G(\mathbf{x}).
\tag{16}
\]

The last equality uses the full-prefix contribution in (1). Thus the optimization concerns a simultaneous labeling of an entire regular group, rather than the distribution of a statistic on one arbitrary permutation. The statistic and this elementary reformulation are not claimed as new.

Fixed subgroup-chain transversal constructions appear in [GVS03, Definition 2.1 and the following construction; Proposition 3.1]. Their logarithmic-signature objective is the sum of factor-block lengths. Such constructions give context for subgroup-based orders, but the inspected statements do not themselves identify every optimizer of (1). Canonical interval decompositions of individual permutations and their enumeration are treated in [Cal03]. The cosets here are recovered from simultaneous regular-group stabilizers under an extremality condition; that additional assertion needs its own comparison.

### 10.2 Classical enumeration mechanisms

[ST09, opening of Section 3] counts maximal subgroup chains recursively through their unique maximal subgroup. [MBKK18, Theorem 5 and Example 6] gives a classical direct/wreath-product description for automorphism groups of rooted trees. These are relevant antecedents for sum-over-top-choice and factorial/product counting. They count different objects. In particular, \(C_4\) has one maximal subgroup chain and eight maximizing element orderings here. Equation (5) follows from the optimizer characterization and unique top recovery; it is not presented as a new general enumeration principle.

### 10.3 The unresolved EFK comparison

[EFK92] develops a group-theoretic framework for intersecting Sperner families. For a subset \(T\subseteq G\), orbit–stabilizer gives
\[
|\operatorname{Orb}_G(T)|^{-1}=|\operatorname{Stab}_G(T)|/m,
\]

so weighted orbit inequalities are relevant comparison targets. The complete EFK mathematical body has not been read. In particular, the retained comparison still lacks Lemma 2.1, Theorem 2.1, the rest of Section 4, Proposition 5.1, Corollary 6.1, and full proof coverage. The earlier \(C_4\) control only invalidates a proposed direct substitution of a prefix chain into an antichain inequality. It does not exclude the paper as an antecedent. The previously denied retrieval route was not retried for this manuscript.

### 10.4 Defensible claim

The possible distinctive contribution is the complete optimizer characterization for the stated two classes, particularly necessity of whole coset blocks, independent branching inside those blocks, and recovery of the unique top subgroup from all proper-prefix stabilizers. The value and exact count are part of the theorem package, with elementary or classical ingredients credited above. This is a candidate contribution, not a worldwide-priority determination.

A contribution-claiming submission still needs a statement-level comparison against a readable authorized EFK copy, or a transparent disclosure that this comparison remains incomplete. Similarity of formulas is insufficient to prove equivalence; absence from selected inspected passages is insufficient to prove originality. No external specialist or journal review is represented as completed.

This manuscript contains no fusion with a separate theorem family. It proves no general Fourier algorithm, no sub-\(N\log N\) FFT, and no unrestricted Fourier sparsity optimum. A separate fixed-coefficient Fourier application in [P1–P2] is not needed for these proofs and is not expanded here.

## 11 Verification and remaining work

The companion concordance identifies exact source sections and SHA-256 pins. The abelian proof [P1] and complete review [P2], and the nonabelian proof [P3] and complete review [P4], are available. Their local reviews accept the scopes stated here. This means supplied local mathematical review, not external peer review or formal proof-assistant certification.

Historical corroboration includes 24 abelian groups, 432,647 identity-first subset states, and 96,640 identity-first permutations in [P2]; and 209,696 identity-first states and 81,360 labeled permutations in [P4]. The present preparation reads those saved records and does not relabel them as fresh runs. Some adjacent receipts named by old review texts are absent from their original directories; the available proof/review files are bound by the companion current manifest instead.

The accompanying bounded validation checks the exact input pins, the displayed cyclic recurrence values, the \(p\)-power sum identity in a finite control range, the \(C_{12}\) stabilizer sequence, and every labeled \(S_3\) ordering. These checks corroborate the formulas and examples. The general proof is Sections 3–7.

There is no identified unresolved mathematical lemma for Theorems 1–2 as stated. The remaining substantive limitation is prior-art comparison, especially EFK. Broader group classes, quantitative stability, additional weight functions, and Fourier improvements are outside this draft; none is needed to finish its present theorem contract.

## References

[BS20] Anna Giordano Bruno and Flavio Salizzoni. *Additivity of the algebraic entropy for locally finite groups with permutable finite subgroups*. arXiv:2001.02419v1, 2020. Definitions p.2 and Example 2.1 p.4. [Primary text](https://arxiv.org/pdf/2001.02419).

[Cal03] David Callan. *Counting stabilized-interval-free permutations*. arXiv:math/0310157v1, 2003; journal record identifies *Journal of Integer Sequences* 7 (2004), Article 04.1.8. The comparison uses the preprint. [Preprint](https://arxiv.org/abs/math/0310157), [journal record](https://cs.uwaterloo.ca/journals/JIS/VOL7/Callan/callan91.html).

[EFK92] Péter L. Erdős, Ulrich Faigle, and Walter Kern. *A Group-Theoretic Setting for Some Intersecting Sperner Families*. *Combinatorics, Probability and Computing* 1 (1992), 323–334. [DOI](https://doi.org/10.1017/S0963548300000377). Full-body comparison unresolved, as specified in Section 10.3.

[GVS03] María Isabel González Vasco, Martin Rötteler, and Rainer Steinwandt. *On Minimal Length Factorizations of Finite Groups*. *Experimental Mathematics* 12 (2003), no.1. Definition 2.1 and construction, PDF p.2; Proposition 3.1, PDF p.3. [Primary text](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/On-Minimal-Length-Factorizations-of-Finite-Groups.pdf).

[MBKK18] Frederick A. Matsen IV, Sara C. Billey, Arnold Kas, and Matjaž Konvalinka. *Tanglegrams: A Reduction Tool for Mathematical Phylogenetics*. 2018. Section 2.2, Theorem 5 and Example 6, printed pp.344–345. The source attributes its classical Theorem 5 to Jordan; Jordan's original paper has not been inspected here. [Primary text](https://matsen.fredhutch.org/papers/Matsen2018-bg.pdf).

[Sta05] Richard P. Stanley. *The Descent Set and Connectivity Set of a Permutation*. Author version of 16 August 2005. Equation (1), Proposition 1.1, Theorems 1.2 and 1.4. [Primary text](https://math.mit.edu/~rstan/papers/decset.pdf).

[ST09] Mirela Ștefănescu and M. Tărnăuceanu. *Counting maximal chains of subgroups of finite nilpotent groups*. *Carpathian Journal of Mathematics* 25 (2009), no.1. Theorem 2.1, Corollary 2.1, opening of Section 3, Proposition 3.1. The accessible PDF has six pages with printed pages 119–124, although its URL and masthead list 119–127; no inspection of unexposed pages is claimed. [Primary text](https://www.carpathian.cunbm.utcluj.ro/wp-content/uploads/2009-vol-25-1/carpathian_2009_25_1_119_127.pdf).

[P1] Project proof. *Exact optimality of prefix stabilizers in finite abelian groups*. 10 October 2026. `research_cycle_1744/prefix_stabilizer_optimality/PREFIX_STABILIZER_OPTIMALITY.md`.

[P2] Project review. *Independent audit of prefix-stabilizer optimality*. 10 October 2026. `research_cycle_1753/prefix_independent_review/INDEPENDENT_REVIEW.md`.

[P3] Project proof. *Nonabelian boundaries of prefix stabilizer optimality*. 10 October 2026. `research_cycle_1826/nonabelian_prefix/NONABELIAN_PREFIX_BOUNDARY.md`.

[P4] Project review. *Independent audit of the nonabelian prefix-stabilizer extension*. 10 October 2026. `research_cycle_1833/nonabelian_review/INDEPENDENT_REVIEW.md`.

[P5] Project prior-art assessment. *Prefix-stabilizer priority follow-up*. 10 October 2026. `research_cycle_2102/prefix_priority_followup/PRIMARY_COMPARISON.md`. Scope and access details are preserved in its `PRIMARY_SOURCES.json` and `SOURCE_ACCESS.json`.
