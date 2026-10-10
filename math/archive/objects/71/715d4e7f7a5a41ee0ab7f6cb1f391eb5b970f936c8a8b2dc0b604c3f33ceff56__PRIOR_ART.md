# Prior art, credit, and distinction

- Fourier diagonalization of cyclic shifts, sparse circulant identities, rational Fourier sums, Cooley–Tukey and Bluestein are standard Fourier/computer-algebra facts.
- The linear feedback shift register synthesis of **Berlekamp–Massey** is established coding-theory work; see https://encyclopediaofmath.org/wiki/Berlekamp-Massey_algorithm and https://math.berkeley.edu/~berlek/research_interests/algorithms.html. We use a prefix candidate followed by a full-vector, independently verified defect certificate. We do not claim to invent BM.
- The majority-vote algorithm of **Boyer–Moore** is standard. Projective ratio comparison is a simple exact adaptation to recurrence graph edges; no inversion per edge is needed.
- Pruned FFTs, input sparsity, fast rational series and Newton inversion are established. The Phase17 source notes the FFTW pruned FFT page: https://fftw.org/pruned.html.
- Sparse graph / permutation cycles and the noncommuting Green factorization originate from the preserved Phase16/17 project checkpoints; these sources and predecessors remain acknowledged and immutable.

**Specific Phase18 contribution:** a complete, exact, verified interaction (including a separately supplied multi-filter union) of a noncommuting Green transform with sparse defects of a *long-range shift graph*, including majority/prefix candidate discovery, whole-vector certification, singular-frequency repair, full cost/fallback accounting, a generic short-annihilator dimension obstruction and a precision stress test. It is an architecture integration and conditional structured-input upper bound, not a priority claim for an unrestricted FFT algorithm.
