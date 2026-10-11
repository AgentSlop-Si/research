# Candidate: complete prefix optimization for every finite abelian group

11 October 2026 UTC. Fresh author candidate, pending independent review.

## 1. Scope, definitions, and conclusions

Let G be any finite abelian group, written multiplicatively, of order

    N = product_p p^(a_p).

For a labeled ordering x=(x_1,...,x_N), let T_j={x_1,...,x_j}, let
S_j={g in G : g T_j=T_j}, and set

    Z_G(x) = sum_(j=1)^N (|S_j|-1),
    B(x) = <S_j : 1 <= j < N>,
    V(G) = N sum_p a_p(1-1/p).

The full prefix is scored once and is excluded from B. The empty prefix is
not scored. For the singleton, Z=0 and there is exactly one ordering.

The candidate conclusions are:

1. For every nontrivial finite abelian G and every ordering, B(x) is proper.
   Thus the full-escape class B(x)=G is empty in this scope.
2. max_x Z_G(x)=V(G).
3. The maximizing orders are exactly the recursive maximal-subgroup
   right-coset orders. Choose a maximal proper subgroup J; order its distinct
   right cosets consecutively, with an independently optimal local element
   order in each coset under a right-translation identification with J;
   recurse to singletons.
4. Every nontrivial optimizer has unique top J=B(x).
5. For the number A(G) of labeled maximizing orders,

       A(1)=1,
       A(G)=sum_(J maximal proper in G) [G:J]! A(J)^[G:J]  (|G|>1).

The sum is over actual subgroups. There is no quotient by translations,
automorphisms, or conjugacy classes, and no extra coset-representative factor.

This covers all finite abelian groups, including any number of prime factors.
It does not extend the accepted theorem to all finite nilpotent groups:
arbitrary nonabelian three-Sylow products remain outside this proof. No
historical-priority or worldwide-novelty claim is made.

## 2. The new gate: accumulated orbit containment

For 1<=j<N put B_j=<S_1,...,S_j>. We claim

    B_j x_1 is a subset of T_j.                              (1)

For j=1, the stabilizer of a singleton under the regular left action is the
identity subgroup, so (1) holds. Suppose it holds for j-1. Since G is abelian,
the product S_j B_(j-1) is a subgroup and equals B_j. Moreover,

    S_j B_(j-1) x_1 is a subset of S_j T_j = T_j,

because B_(j-1)x_1 is contained in T_(j-1), hence in T_j. This proves (1)
inductively. At j=N-1, the orbit B_(N-1)x_1 has |B_(N-1)| elements and is
contained in a proper prefix. Consequently B(x)=B_(N-1)<G.

Only the product-equals-generated-subgroup step uses abelianity. This proof
does not assume that any individual stabilizer persists at a later prefix.
It does not compare stabilizers by inclusion. They may be incomparable.

This lemma eliminates the escape case altogether in the abelian scope. It
replaces, rather than extends, the q-adic numerical escape argument of the
accepted two-Sylow theorem.

## 3. Induction using the accepted local-coset mechanism

The local accounting, equality mechanism, and labeled counting below are the
mechanisms already established in Sections 8-9 of the accepted arbitrary
two-Sylow proof. They are recorded here to make their use at the enlarged
scope explicit. The new premise needed to apply them is Section 2.

Induct on |G|, simultaneously over all finite abelian groups. The singleton
is the stated base. Suppose |G|>1 and x is any ordering. By Section 2 choose
a maximal subgroup J containing B(x). As G is abelian, J is normal and G/J
is a nontrivial finite simple abelian group, hence cyclic of prime order p.
Thus [G:J]=p and |J|=N/p. The subgroup J is abelian, so the full induction
statement applies to J.

For each right J-coset C, restrict x to C and identify C with J by a fixed
right translation. At each global insertion j, let L_j<=J be the stabilizer
of the active local prefix in the coset receiving that insertion. For j<N,
S_j<=B(x)<=J, and S_j stabilizes the intersection with every J-coset, so
S_j<=L_j. Every nonempty local prefix appears once as an active insertion.
At the final insertion, L_N=J while S_N=G. Therefore

    Z_G(x) = sum_C Z_J(x restricted to C) + N-|J|
             - sum_(j<N) (|L_j|-|S_j|).                    (2)

All terms in the last sum are nonnegative. The inductive upper bound gives

    Z_G(x) <= p V(J)+N-N/p = V(G),                         (3)

since replacing |G| by |J| removes exactly one p from its prime factorization.
This proves the upper bound for every ordering, with no assumption that x
is already optimal.

For the converse, choose any maximal J and arrange its p cosets in consecutive
blocks, each with a locally maximizing order. No element outside J can
stabilize a proper prefix. At a block boundary its nonidentity image in the
prime cyclic quotient would have to preserve a nonempty proper set of quotient
cosets, which is impossible. Inside a block it would have to move the unique
partially filled coset to another partially filled coset, also impossible.
Thus each proper global stabilizer equals the active local stabilizer: filled
cosets are J-invariant, and empty cosets impose no condition. The deficits in
(2) vanish, and the score is V(G). This proves attainment.

## 4. Equality, unique top, and count

If x is optimal, every inequality used in (2)-(3) is an equality. In particular,
every local order is optimal and |S_j|=|L_j| for j<N. Together with S_j<=L_j,
this gives S_j=L_j.

At the first completion of a J-coset, L_j=J, hence S_j=J. The prefix must be a
union of whole J-cosets. No other coset has yet completed, so every other coset
is empty. This forces the first consecutive J-block. At every later completion
before the last, the same equality excludes any occupied but unfinished coset.
Induction over completion times forces all cosets into consecutive blocks.
Their local orders have the recursively optimal form by induction on |G|.

Conversely Section 3 showed that every such recursive choice is optimal. At
the first complete block, the global stabilizer is exactly J. All other proper
stabilizers lie in J. Hence B(x)=J, proving uniqueness of the top.

For a fixed J of prime index p, its labeled cosets can be ordered in p! ways.
Each has A(J) independent local choices, giving p! A(J)^p orders. A different
choice of a coset representative changes its identification with J bijectively
and gives no extra labeled sequence. The blocks and local orders are recovered
from the global sequence. Distinct tops cannot overlap because the top is B(x).
Summing over actual maximal subgroups proves the recurrence in Section 1.

For |G| prime, J=1 is the unique top and A(G)=|G|!. The singleton uses only its
base case and has no top subgroup.

## 5. Smallest three-prime instance and exact finite corroboration

For C30=C2 x C3 x C5 the theorem gives V=30(1/2+2/3+4/5)=59. The proper maximal
subgroups have orders 6,10,15. The accepted two-prime counts (also freshly
rechecked here) are

    A(C6)=120, A(C10)=32640, A(C15)=11301120.

Consequently

    A(C30)=5! 120^5 + 3! 32640^3 + 2! 11301120^2
           =467058592972800.

A fresh exact periodic-subset dynamic program independently of this algebraic
induction examines 33814 subsets, including empty/full, and 14587235 proper
predecessor pairs. It returns maximum 59 and exactly the count above, partitioned
by generated proper-prefix stabilizer order as follows:

    |B|=6:   2985984000000
    |B|=10:  208641982464000
    |B|=15:  255430626508800
    all other |B|: 0 among optimizers.

Its augmented chain computation finds no chain of proper periodic prefixes
whose stabilizers generate C30. The value -1 in that computation is an
unreachable-state sentinel, not an escaping maximum. Thus there is no nonvacuous
sharp full-escape value to report for C30 or any other abelian group.

The symbolic proof establishes the universal theorem. The finite controls are
corroboration, not a substitute for that proof or an independent review.

## 6. Exact obstruction to a direct mixed-base q-adic substitution

The accepted numerical proof uses a prime-power base n=q^a, for which

    sum_(j=1)^n gcd(j,n) = n[1+a(1-1/q)].

If one blindly replaces that base by n=q^a r^c for distinct q,r while retaining
the pointwise gcd caps, the divisor-sum identity instead gives

    sum_(j=1)^n gcd(j,n)
      = n[1+a(1-1/q)][1+c(1-1/r)].                       (4)

Indeed gcd is multiplicative across coprime factors and the Chinese remainder
map enumerates all pairs of residues. For a single prime power, writing
gcd(j,q^a)=sum_(d|gcd(j,q^a)) phi(d) and counting multiples gives the displayed
prime-power formula, so (4) follows without a new extremal assumption.

Take a third prime p and fully dense p-threshold levels through depth b. The
same quotient algebra with this mixed gcd cap has value

    U_dense = p^b [sum_(j=1)^n gcd(j,n)-n]
                  + b(p-1)n p^(b-1)
            = V(G) + |G| ac(1-1/q)(1-1/r).               (5)

The excess is strictly positive when a,c>=1. For n=6,p=5,b=1, the gcd sum is
15, the relaxed bound is 5*15-6=69, and the actual optimum is 59. Thus this
unmodified mixed-base envelope cannot prove even the smallest three-prime
value theorem. This is an exact obstruction to that proof substitution, not
a counterexample to the value theorem, nor a claim that every possible
multivariate densification strategy fails. Section 2 supplies another route
for abelian groups.

## 7. Why the nonabelian nilpotent gate remains open

The orbit-product step in Section 2 can fail because a product of subgroups
need not equal their generated subgroup. This is already visible in the
dihedral group D8=<r,s | r^4=s^2=1, s r s=r^(-1)>.

Using labels 2i+j for r^i s^j, the order

    0,1,2,3,5,6,4,7

has proper-prefix stabilizers, in order,

    {0}, {0,1}, {0}, {0,3}, {0}, {0,3}, {0}.

The subgroups <s>={0,1} and <rs>={0,3} generate all D8. Hence B=D8 although
the final proper prefix has only seven elements. The score is 10, below the
known prime-power optimum 12, so this does not contradict any accepted result.
It only prevents carrying the abelian no-escape lemma over to arbitrary
nonabelian nilpotent groups.

The remaining mathematical gate is a replacement upper-bound/escape argument
for arbitrary nonabelian three-Sylow products. The present proof makes no claim
to close that gate or to determine sharp escaping maxima there.

## 8. Provenance and limitations

Accepted input proofs were read and copied byte-for-byte into source_snapshots;
SOURCE_BINDINGS.json records their hashes. No original upload or accepted
control script was executed, imported, or modified. All executed mathematical
controls in this packet were freshly authored. The live Sheet was read only
to confirm its current open gate; SHEET_SNAPSHOT.json records that read.

The theorem in this file is a new author candidate in the project workflow,
not a statement of historical originality. Prior-work comparison, the existing
external-source gap, and publication priority are unchanged. Separate
adversarial review is required before calling the extension accepted. There
were no Sheet or GitHub writes.
