# Internal gauges and the remaining pole escape

## Established result

Let a finite directed acyclic network have designated boundary source vertices with no incoming edges and designated boundary sink vertices with no outgoing edges. Every other vertex is internal. Edge coefficients lie in a valued field K, with valuation v: K* → Γ in an ordered abelian group; coefficients equal to zero are permitted and their edges are deleted. An internal diagonal gauge multiplies an edge u→v by g(u)/g(v), where g is nonzero at each vertex and has valuation zero at all boundary vertices.

**Gauge criterion.** Such gauges make every edge coefficient integral if and only if every surviving directed source-to-sink path has nonnegative total valuation.

Here an edge coefficient is integral when it is zero or its valuation is nonnegative. The statement does not require all original edges to survive, all vertices to remain source-reachable, or the remaining network to be connected.

### Proof

Write w(u→v) for the valuation of a surviving edge. If h(u)=v(g(u)), the transformed valuation is w(u→v)+h(u)−h(v). Its sum over a source-to-sink path is unchanged because both endpoint potentials are zero. This proves necessity.

For sufficiency, identify all boundary vertices as a single vertex b. Every directed cycle in this quotient that uses b decomposes into original source-to-sink paths, so has nonnegative weight. A cycle not using b would already have been a cycle in the original acyclic network, which is impossible. Thus the quotient has no negative directed cycle. Adjoin an auxiliary source with a zero-weight edge to every quotient vertex and let d(v) be the shortest-path weight from it. This minimum exists: removing nonnegative cycles never increases path weight, and there are only finitely many simple paths. In particular d(v) lies in Γ, even if Γ is not discrete or Archimedean.

For each quotient edge u→v, d(v)≤d(u)+w(u→v). Set h(v)=d(v)−d(b), and lift these potentials to the original vertices. Every boundary potential is zero and every transformed edge valuation is nonnegative. The potentials belong to the actual value group, so elements g(v) of K with these valuations exist. This proves sufficiency.

### Exact finite controls

The fresh program `verify_gauge_controls.py` checks all 4^8=65,536 assignments of valuations from {zero coefficient, −1,0,1} to the eight edges of a two-source, two-internal-vertex, two-sink complete adjacent-layer network. It independently compares:

1. all surviving source-to-sink path valuations being nonnegative;
2. the quotient difference constraints having no negative cycle, with explicit shortest-distance gauges;
3. direct enumeration of the 25 internal gauges in {−2,−1,0,1,2}^2.

All three agree: 18,769 assignments are integralizable and 46,767 are not. Zero edges, disconnected vertices, and absence of surviving source-to-sink paths are included. The exhaustive checks support the proof; they are not substituted for the general proof.

## Consequence for the accepted 99-edge Fourier problem

Use the fixed support in `topology_11.json`, the unnormalized Fourier matrix F11=(ζ^(ij)), and an extension of the cyclotomic valuation with v(ζ−1)>0. Every Fourier entry has valuation zero and residue one. The accepted v34 graph certificate excludes all integral factorizations CBA=F11 on this support, allowing any permitted edge to vanish.

Therefore, if an algebraic factorization exists, **at each chosen place above 11 it has a surviving source-to-sink path with strictly negative total valuation**. This is stronger and gauge-invariant compared with saying that some individual coefficient has a pole. In particular, arbitrary internal diagonal gauges do not rescue this factorization into the integral model. The endpoint gauges are required to have valuation zero; allowing nonunit endpoint changes alters the target and is outside this statement.

## Correct entrywise tropical constraints

For output i and input j let P(i,j) be the surviving source-to-sink paths and let W(p) be their total edge valuation. The transfer equation is

    sum over p in P(i,j) of product of its coefficients − ζ^(ij) = 0.

In a valued field the minimum valuation among the nonzero terms of a zero sum must be attained at least twice. Hence

    min({0} ∪ {W(p): p in P(i,j)})

must be attained at least twice, counting the constant target term once. This yields exactly the following alternatives:

- If every path has nonnegative valuation, at least one path must have valuation zero.
- If some path has negative valuation, at least two paths must share the smallest negative valuation, and their initial coefficients must cancel collectively.
- If a pair has exactly one surviving path, that path has valuation exactly zero.

For the original support there are 22 graph-unique paths. They must all survive in any factorization because every Fourier entry is nonzero, and each has path valuation zero. It is incorrect to infer that all paths have nonnegative valuation from the unit transfer entries. Multi-path cancellation is the unresolved escape mechanism.

These minimum conditions are necessary. They are not sufficient for an algebraic factorization, not even for simultaneous solvability of the initial-form equations.

## Complex-to-algebraic transfer, with nonzero conditions explicit

The 121 equations CBA=F11 are polynomial equations over the number field Q(ζ). All edge positions outside the support are fixed to zero; the 99 allowed positions are variables. If this polynomial system has a complex solution, the weak Nullstellensatz gives a solution over the algebraic closure of Q(ζ), and its finitely many coordinates lie in a number field. Thus any complex existence result would yield an algebraic witness to which the preceding valuation arguments apply.

This does not assign a valuation to arbitrary given complex coefficients or preserve that particular complex solution. It replaces an existential complex solution by an existential algebraic one.

If exact nonzero support is required, the polynomial system must also include the equation

    z * (product of all coefficients required to be nonzero) − 1 = 0

with an extra variable z. For a specified zero/nonzero pattern, set zero edges to zero and include this equation for the required nonzero edges. A claimed gauge chart may only divide by coefficients whose nonvanishing is established or encoded. The invertibility of the three square factors follows from CBA=F11 being invertible, so no additional determinant inequality is needed for that consequence. This transfer by itself provides no impossibility theorem for unrestricted complex weights.

## Scope

No supplied program was run or imported. The accepted topology JSON was copied and read as data. New proofs, controls, and searches are confined to this directory. The accepted v34 data are unchanged. No external files were written.

## A tropical pole pattern exists, but its initial face is excluded

A bounded 90-second mixed-integer search returned a feasible incumbent. It did not prove optimality. After dividing every valuation by two, the resulting 99-edge vector has values in {−1,0,1}; its 28 nonzero coordinates, using zero-based within-layer indices, are:

- A: a13=−1, a20=1, a25=−1, a31=1.
- B: b0=b1=b8=b9=b12=b13=b19=b23=b30=b31=−1; b14=b18=1.
- C: c14=c18=c20=c25=c31=−1; c12=c16=c19=c21=c26=c28=c32=1.

All other coordinates have valuation zero. `tropical_pole_witness.json` stores this vector with the exact source edge order. All 121 entry equations pass the tied-minimum test, including all 22 unique paths having valuation zero. There are 31 entries with a strictly negative minimum, and the smallest path valuation is −2. An independent reviewer rebuilt every path by forward traversal and verified the original doubled vector with exact integers. Scaling by positive one-half preserves every entrywise minimum tie.

This is a witness only to the entrywise tropical relaxation. It is **not** a Fourier factorization or a liftable valuation vector. In fact the whole initial-term face is ruled out as follows.

Let x0,…,x98 be the nonzero leading coefficients of the edges in the global order A0,…,A32,B0,…,B32,C0,…,C32. Four of the entry initial equations are:

    (output1,input5): x28*x48*x67 = 1
    (output1,input6): x6*x48*x67 = 1
    (output6,input5): x28*x48*x83 = 1
    (output6,input6): x6*x48*x83 + x12*x36*x72 = 1

The first two imply x28=x6. The third then sets the first summand in the fourth to one, forcing x12*x36*x72=0, a contradiction. This argument works over any residue field and uses the nonzero status of leading coefficients explicitly. The reviewer derived this certificate; `root_check_four_equation_obstruction.json` independently regenerates the four equations and checks their exact minimum supports.

The exactly-two-minimizer subsystem alone had no such contradiction: the reviewer produced a ±1 assignment satisfying all 50 extracted binomials. It is the additional multi-term equation that exposes this face. The explicit four-equation certificate supersedes any attempt to infer a contradiction from the binomials alone.

### Independent 2-by-2 minor obstruction

For a layered acyclic network, expansion of a transfer minor cancels every intersecting path family in pairs. The remaining terms are vertex-disjoint path families, each with coefficient +1 or −1. Distinct such families have distinct edge sets because each used internal vertex has exactly one incoming and one outgoing edge in the family, and the input vertices uniquely label the paths. Thus no hidden multiplicity or further monomial cancellation remains.

Every 2-by-2 Fourier minor has valuation one under v(ζ−1)=1. The same tied-minimum test can therefore be applied to its disjoint-family monomials together with a target term of valuation one.

All 3,025 minors were generated from disjoint paths and checked exactly. Eight fail for this vector. A particularly short certificate is the polynomial identity, valid for all edge coefficients on the fixed support:

    det H[[0,7],[0,3]] = −x23*x31*x33*x53*x66*x73,
    where H=CBA.

The Fourier target minor is ζ^21−1, which has valuation one. The displayed monomial has valuation zero for the witness, and for every positive scaling of it. Thus this entire ray cannot be an algebraic Fourier factorization. An independent reviewer verified all 3,025 expanded polynomials by multiplying the entry path polynomials and collecting integer monomials, rather than using disjoint-path filtering. It agrees on all eight failures and the exact displayed identity.

The four-entry contradiction excludes the entire same-initial-support face; the monomial-minor contradiction excludes every positive scaling of this particular vector. Neither assertion excludes every possible pole pattern.

## All single-monomial minor constraints are now exhausted

A separate exact enumeration covered all 705,431 nonempty minors at orders 1 through 11. It found:

- Order1: exactly22 one-family minors, namely the known unique paths.
- Order2: exactly4 one-family minors.
- Orders3–11: no one-family minors.

There are no unreachable minors. The latter reproduces support superconcentration, not Fourier compatibility.

The reviewer and a separately authored reproduction in `verify_all_order_monomials.py` both expand each source subset forward through destination choices, carrying the used-destination mask and capping matching counts at two. They then use exact integer matrix multiplication with counts capped at two. These are independently written implementations of the same capped-count algorithm, not different algorithms. The reproduction was written and run without reading, running, or importing the reviewer program; it additionally validates every reported unique-family edge set directly. Before each cap every entry is at most 4 times the number of k-subsets (at most1848), ruling out integer overflow. Capping at two preserves exactly the distinctions zero, one, and at least two. All 705,431 counts agree. Every one of the 26 unique-family certificate edge sets was independently checked as a valid matching in each layer with the required endpoints.

For a k-by-k single-family minor, its monomial coefficient is ±1, so the Fourier equation requires the sum of its edge valuations to equal k(k−1)/2. This formula uses v(ζ−1)=1; it does not assume edge valuations are integers. The resulting 26-by-99 rational incidence matrix has rank26, and appending the required valuation column still gives rank26. Hence all single-monomial minor valuation equations are mutually consistent; they provide no linear inconsistency certificate. Because every order was enumerated, searching for additional one-family minors on this unchanged topology cannot strengthen this particular test.

## Bounded stronger searches and limitations

The original entrywise search used integer weights in [−2,2] after fixing 22 gauge coordinates, and a 90-second cap. Its exact feasible witness and later exclusion are reported above.

A next bounded model imposed all121 entrywise conditions plus all12 two-by-two minor polynomials having at most two monomial terms. The weights were integers in [−3,3], with the same gauge fixing, and at least one negative entry minimum was required. It reached its 90-second cap without an incumbent. This is inconclusive; it does not establish infeasibility, even within those bounds. In particular it says nothing about fractional valuations in ramified extensions.

A separate continuous-weight feasibility model is recorded independently. Any candidate from this model must pass exact rational reconstruction and every required tied-minimum test before it is reported as a witness. The bounded searches are exploratory tools; the accepted conclusions above depend on explicit proof, exact certificates, and independent checking.

The continuous-weight feasibility search found another exactly reconstructed integer candidate in 3.7 seconds. It has 12 nonzero edge valuations and seven negative entry minima. It passes all 121 entry conditions and the 12 imposed small-minor conditions, but fails 23 other two-by-two minor tests. Adding all 23 failed-minor constraints gave a third exactly reconstructed candidate: all 121 entries and all 35 imposed minors pass, while 12 previously unchecked minors fail. This third vector has eight negative entry minima. Both candidates were independently checked using exact rational arithmetic and direct determinant expansion. After adding the 12 further cuts, the next 90-second round had no incumbent. The bounded sequence ends inconclusively with 47 included minor constraints; it does not exhaust all valuation patterns or establish infeasibility.

The feasibility models bounded every gauge-normalized edge valuation in [−2,2] and required the sum of the entry minima to be at most −1. These are search restrictions, not necessary bounds for arbitrary algebraic solutions under the Fourier normalization. The reported feasible candidates happen to have integer coordinates. No conclusion about ramification follows from that fact.

## Additional exact nonzero information

The union of the edges in all 26 single-monomial minors has size63, exactly21 in each support layer. Since every Fourier minor is nonzero, every one of these63 edge coefficients must be nonzero in any factorization. Relative to the original55 forced edges from unique entries, the added global edge indices are

    17,31,32,33,39,46,84,96.

The mandatory A-edges meet internal rows1 through10 but not row0; mandatory C-edges meet all11 internal columns. Thus21 internal diagonal gauge normalizations can be made using individually proved nonzero edges. For the remaining A-row0, the only allowed indices are0,11,22. Invertibility of A forces at least one of them nonzero. The three charts that respectively require a0≠0, a11≠0, or a22≠0 therefore cover every possible factorization and can complete the22 internal gauge fixes. None of these charts may be assumed alone to cover the whole problem.

`monomial_linear_consistency_certificate.json` makes the rank claim completely explicit: a specified26-by-26 incidence submatrix has determinant−1, and setting only w17=w31=w32=1 satisfies all26 monomial-minor valuation equations. This is only a solution of the26 linear equations. For example entry(output0,input4) then has both path valuations equal to1, so fails the unit-target condition. The reviewer independently checks both the determinant and this limitation.

## Accepted checkpoint and experimental continuation

The gauge theorem, necessary negative-path consequence, exact tropical witnesses and their exclusions, all-order monomial-minor enumeration,63-edge necessity, and chart coverage above are independently reviewed. The unrestricted algebraic and complex Fourier existence questions remain open on this fixed topology.

Separate files whose names begin `full_fourier_` or `reduce_full_fourier_` contain a subsequent exploratory symbolic-elimination continuation. They are not part of the accepted conclusions in this report unless separately reviewed. In particular, smaller residual systems must not be mistaken for a Fourier assignment or an impossibility proof.
