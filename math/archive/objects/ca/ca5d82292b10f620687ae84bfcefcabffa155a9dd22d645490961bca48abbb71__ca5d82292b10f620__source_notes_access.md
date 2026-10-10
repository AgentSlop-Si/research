# Primary-source access notes: Brockett–Dobkin thin matrix multiplication

Access checked 2026-10-09. This records what was actually readable; lack of access is not evidence against a total-arithmetic theorem.

## 1978 correction: full text verified

Publisher landing page: <https://epubs.siam.org/doi/10.1137/0207021>

The landing page explicitly marks the correction as free access. Following its actual PDF links succeeded:

- <https://epubs.siam.org/doi/epdf/10.1137/0207021>
- <https://epubs.siam.org/doi/pdf/10.1137/0207021?download=true>

R. W. Brockett and D. Dobkin, *Errata: On the Number of Multiplications Required for Matrix Multiplication*, SIAM J. Comput. 7(2), p. 238 (1978).

The correction changes two signs in the original paper's page 625: both summation terms in formula (*) must be subtracted, while the two parenthesized terms in the preceding equation must be added. These are the only mathematical corrections stated. Web full-text references: `turn113view1` and `turn113view2`.

## 1976 paper: construction still not obtained in this access pass

<https://epubs.siam.org/doi/10.1137/0205041>

R. W. Brockett and D. Dobkin, *On the Number of Multiplications Required for Matrix Multiplication*, SIAM J. Comput. 5(4), pp. 624–628 (1976).

The publisher abstract was readable. Both actual publisher links, View PDF and Download PDF, redirected to the abstract/access page. References: `turn103view0`, `turn114view0`, `turn114view1`. A search result exposed a small fragment of the paper's formulas, but not enough to reconstruct the algorithm reliably.

The Harvard Robotics Laboratory public bibliography (<https://hrl.harvard.edu/publications/>) was readable but does not list this paper. The author's old Harvard homepage returned 404. No accessible author-deposited 1976 copy was found in the Harvard/Princeton searches.

## Other authorized leads

- Yale's official technical-report index lists Dobkin's 1973 thesis as YALEU/DCS/TR023: <https://engineering.yale.edu/academic-study/departments/computer-science/technical-reports>. Its actual institutional PDF endpoint is <https://engineering.yale.edu/download_file/view/[private-id]/3815>. The web reader recognized 103 pages but extracted no text (`turn137view0`); screenshots and direct download were unsuccessful in the parent agent's access pass. Its construction remains unread.
- A 1982 CWI lecture collection cites the 1976 paper and a 1976 oral communication by Brockett. Its officially hosted PDF is 11 MB, exceeding this web reader's size limit: <https://ir.cwi.nl/pub/13444> and <https://ir.cwi.nl/pub/13444/13444D.pdf>. Its relevance beyond those citations remains unchecked.
- The official Waterloo report <https://cs.uwaterloo.ca/research/tr/1973/CS-73-27.pdf> is Robert L. Probert's *On the Complexity of Matrix Multiplication*. The web reader timed out; construction content remains unchecked.

No claim about the absence of an O(n²) total-arithmetic algorithm follows from these access results. The parent has independent later-source support for such a bound; recovering and auditing the uniform construction remains the outstanding task.

## 1992 matrix-product verification paper: indexed snippets only

B. Ravikumar, *A note on checking matrix products (extended abstract)*, Proceedings of the 1992 ACM/SIGAPP Symposium on Applied Computing, pp. 937–943, DOI: 10.1145/130069.130111.

Official publisher routes:

- <https://dl.acm.org/doi/10.1145/130069.130111>
- <https://dl.acm.org/doi/pdf/10.1145/130069.130111>

The full paper was not obtained. Opening the publisher PDF returned HTTP 403 (`turn135view0`); the following findings come only from search-index excerpts of that same official ACM PDF, not from reading the paper in context.

- The B–D result is stated for an n × n matrix multiplied by an n × log n matrix, with O(n²) **nonscalar multiplications** (`turn134search0`, `turn135search1`). The nonscalar qualifier must be retained. This excerpt does not by itself establish O(n²) total arithmetic, or give an addition circuit.
- A separate excerpt says that the paper works with integer matrices and discusses addition and multiplication of pairs of integers (`turn139search0`). The next clause is truncated, so the arithmetic cost convention cannot be verified from that excerpt.
- An excerpt concerning additions was found (`turn138search0`), but its formula is garbled and its context unavailable. It cannot safely be attributed to the B–D construction rather than to a verification subroutine. No addition bound is recovered from it.
- No construction, uniformity argument, preprocessing bound, or coefficient-size control was recovered from this paper in this access pass.

The official author CV <https://ravi.cs.sonoma.edu/vitae.pdf> confirms the paper's bibliographic entry (`turn135search0`). The readable author homepages <https://ravi.cs.sonoma.edu/> (`turn134view2`) and <https://homepage.cs.uri.edu/faculty/ravikumar/> (`turn139view0`) did not directly expose this paper. The official conference PDF <https://www.sigapp.org/sac/sac1992/SAC%201992%20Proceedings.pdf> is only 14 pages of front matter/index (`turn134view0`), not the article.

This lead adds useful domain and operation-count qualifiers but does not resolve the total-arithmetic construction gap. These access limitations do not contradict a separately verified later statement of a total O(n²) result.
