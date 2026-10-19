# Development and rejected routes

The initial local approach retained the same-group off-diagonal Gram K with entries 0,1,2. It correctly observed that K+(d/q)I is positive definite, that at most five rows in one five-coordinate fiber have weight at least three, and that the K=2 graph is a disjoint union of cliques. Further finite local patterns give an upper-degree reduction, but were not needed for the final proof and are not imported as dependencies.

The accepted first-interior clique decomposition cannot simply be reused here: its adjacency is overlap one, whereas the middle interval also permits overlap two. No full-square-block or common-support premise was assumed.

The decisive route uses column regularity before local classification. Each supported entry has a primitive partner because d>q+4. The classical binary overlap alternative then forces the complete row to be a union of full CRT cycles. The proof derives its later common pair and permutation structure from this union form and same-group orthogonality.

All numerical exploration was used for ideas only. The retained final checker uses exact integer arithmetic. There was no external solver, service limit, arbitrary-phase relaxation, or external write. The negative cross-shape mask has valid same-group rectangular row Grams and both degree counts, but explicitly fails full-square Grams.
