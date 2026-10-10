# Chain checkpoint — exact cyclotomic-degeneration and zero-forcing gate v34

**Inherited:** v31 depth-three superconcentrator routing does not supply exact Fourier phases; v32 cyclotomic phase-only path-count obstruction is restricted; v33 fixed 99-edge three-layer `11 x 11` support is superconcentrating and generically full-spark but has **no known Fourier weights**. Its projective transfer family has complex dimension 56, codimension 44, with no affine-linear cross-ratio relation; that does **not** rule Fourier out.

**New proved arithmetic obstruction.** Let `zeta` be a primitive 11th root, `pi=zeta-1`, `O=Z[zeta]_(pi)`. For **arbitrary pi-integral** weights on exactly the v33 99 positions, equality `CBA=F_11` requires at least **7 nonunit edge weights**, i.e. at least seven edge coefficients vanish upon reduction modulo `pi`. The theorem does not cover coefficients with pi-adic poles or unrestricted complex values.

**Proof:** `F_11 mod pi=all-ones`, rank 1. Each support hypergraph of the 33-edge layers has a two-coordinate zero-forcing seed: `A:{0,1}`, `B:{1,2}`, `C:{2,6}`. For deletion counts `z=0..5`, exhaustive forcing maxima are respectively: `A:[2,3,3,3,3,3]`, `B:[2,3,3,3,3,4]`, `C:[2,3,3,3,3,4]`. Deleting one edge raises forcing number by at most one, so `z=6` needs <=5 seeds. For total deleted <=6, the sum of three kernel-dimension bounds is <=9. Sylvester implies rank of the reduced product >=2, contradicting rank 1.

**Cyclotomic minor fact (classical):** for any prime `p`, every k-by-k minor of `F_p` has exact `(zeta-1)`-adic valuation `k(k-1)/2`, giving local Smith exponents `0..p-1`. This is Chebotarev-style p-adic theory, **not new**.

**Verification:** 852,822 separate layer-deletion patterns exhaustive; 3682 `p=5,7` minors exhaustive and 31 `p=11` certificates; independently 18,054 small deletion patterns plus 10,800 high-deletion samples and exact resultants. 10 main test groups and cold ZIP replay pass. Full unchanged predecessor v33 ZIP embedded.

**Do not repeat:** claim dimensional deficiency alone proves no complex solution; claim this pi-integral theorem covers arbitrary complex weights; claim isolated unitary or cyclotomic restrictions yield an unrestricted FFT lower bound; hide coefficient valuation/gauge choices or operation count.

**Next exact experiment:** Determine whether exceptional supports with >=7 pi-nonunit edges can realize rank-one all-ones transfer modulo pi, then lift exact cyclotomic Fourier phases through higher pi powers. Alternatively leave this arithmetic subclass for a nonlinear polynomial invariant valid with arbitrary complex edge weights. New exact arbitrary-input sub-`N log N` FFT **not constructed**.
