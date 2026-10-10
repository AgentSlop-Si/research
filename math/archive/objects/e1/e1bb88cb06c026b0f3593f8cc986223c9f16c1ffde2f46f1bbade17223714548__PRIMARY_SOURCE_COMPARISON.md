# Focused primary-source and inherited-source comparison

Checked 2026-10-10. This records actual inspected mathematical sources and a
bounded search, not a novelty certification. No supplied programs were run.

## 1. Complementary inverse-submatrix ranks

Raf Vandebril and Marc Van Barel, *A short note on the nullity theorem*,
KU Leuven report TW397 (July 2004), Section 3, Theorem 1 and Corollary 1,
printed pp. 4-5 (PDF pp. 6-7):
https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf

Corollary 1 states precisely the rank identity with swapped complements used
in this audit. Its theorem does not assume invertibility of a principal
subblock. The report attributes the nullity theorem to Gustafson and the
matrix formulation to Fiedler-Markham; those original papers were not
independently opened in this audit. The inverse-separator bound here is an
immediate application, with a self-contained kernel proof supplied for clarity.
No credit for a new inverse-nullity theorem is warranted.

## 2. Graph-induced rank structures

S. Chandrasekaran, E. N. Epperly, and N. Govindarajan, *Graph-Induced Rank
Structures and their Representations*, arXiv:1911.05858v3 (2021), Section 2.1,
Propositions 2.1-2.3, printed pp. 5-8:
https://arxiv.org/pdf/1911.05858

Proposition 2.1 records preservation of complementary off-diagonal block
ranks under inversion. The next propositions formulate graph-induced rank
bounds and their algebra, including inverse closure. This is a direct
antecedent for translating sparse support structure into inverse rank
structure. The inspected statements do not assert this independently routed
flat-unitary branch-count obstruction. Their usual boundary-edge budget can
be large for high-degree vertices; our small vertex-separator budget is
justified by the complementary-rank formula, rather than by replacing a
vertex count with an edge count.

## 3. Weighted separators and treewidth

Zdenek Dvorak and Sergey Norin, *Treewidth of graphs with balanced
separations*, arXiv:1408.3869, introduction, pp. 1-2:
https://arxiv.org/pdf/1408.3869

The paper recalls that treewidth t supplies, for any nonnegative vertex
weights, a weighted balanced separation of order at most t+1, crediting
Robertson-Seymour, *Graph Minors II* (1986). Its stated balance convention is
2/3 on two sides. We do not misquote that convention as the half-component
statement used here: a direct weighted-centroid proof in the audit supplies
the latter. This is classical tree-decomposition machinery, not a new
separator theorem. The original 1986 article was not independently read.

Hermann Gruber, *On Balanced Separators, Treewidth, and Cycle Rank*,
arXiv:1012.1344, Section 1 and Theorem 2, was also inspected for conventions:
https://arxiv.org/pdf/1012.1344

It distinguishes separator normalizations and surveys the width relations.
The present argument avoids relying on a convention-sensitive inequality by
proving the precise weighted component balance it needs.

## 4. Column-two matrices and graph representations

Peter Nelson and Stefan H. M. van Zwam, *On the existence of asymptotically
good linear codes in minor-closed classes*, Section 2, printed p. 4:
https://www.math.uwaterloo.ca/~apnelson/asympgood.pdf

This paper calls matrices with at most two nonzero entries per column frame
matrices and sets out their graph representation, including loops and
parallel edges. It notes the special convention issue for singleton columns
over GF(2). Our graph is an unsigned support/counting graph, not a claimed
GF(2) gain-graph representation. Full-rank component counts are established
directly from invertibility. The terminology and graph language are
classical; the source is not claimed to state the current sum obstruction.

## 5. Exact inherited theorem inspected, not merely its review summary

The audit independently read the complete inherited
FFT_SEPARATION_RANK_THEORY/THEOREM.md from the master_v25 tree. Its exact path
and hash are in INPUT_PROVENANCE.json. The previously accepted review's C04
was also read, together with its source dispositions for S11 and S23.

The inherited theorem explicitly proves:

- independent row/column order pairs, simultaneous half-selection, and a
  common rectangle of side floor(N/2^d);
- rank of a branch sum at most the sum of separation-rank budgets;
- the all-length complex Fourier lower bound via Frobenius/operator norms,
  already yielding logarithmically many Hamiltonian Green branches;
- the analogous operator-norm approximation gap.

Thus those conclusions are not new Hamiltonian theorems in the present work.
The inherited result also covers an abstract ordered-separation-rank class.
Arbitrarily many cycle blocks alone do not escape it: concatenate their
orders, and at most one block straddles any strict separator. Invertible
D+EP cycle blocks can be normalized using either their nonzero diagonal
product or nonzero cycle-edge product, absorbing monomial factors into
endpoints. Zero endpoint factors only lower ranks. Hence even that full
multi-cycle specialization already follows by an elementary extension of
the old ordering argument, without a cycle-count penalty.

The inspected inherited theorem does not establish a uniform constant
ordered-separation rank for arbitrary attached-tree column-two supports.
The current proof instead uses fresh weighted vertex separators at every
restriction and requires no global ordering with uniformly small separated
rank. This is the substantive verified generalization. It also yields the
stated general bounded-treewidth variant. This comparison does not prove
that every such new branch is outside every old abstract class, nor does it
claim an exhaustive search of all historical project documents.

## 6. Search scope and remaining priority question

Focused public queries included combinations of Fourier, inverse sums,
pseudoforests, treewidth, flat unitaries, separators, and nullity. No inspected
primary paper or inherited theorem stated the complete attached-tree,
independently routed, flat-unitary result with these bounds. A sparse or
negative search result is not evidence of originality. The proof consists
of classical inverse-rank and separator ingredients plus an elementary
iterated two-color rectangle selection. Publication priority of their full
application remains unresolved.
