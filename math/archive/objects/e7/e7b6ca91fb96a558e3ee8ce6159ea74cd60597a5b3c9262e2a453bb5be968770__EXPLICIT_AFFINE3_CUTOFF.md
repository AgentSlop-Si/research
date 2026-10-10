# A symbolic explicit cutoff for four rank-one R-A3-R stages

No large graph is constructed for this deduction. It follows from a counted bit-reversal rectangle and the approved collapse/discrepancy inequalities.

Let N=2^m and R_m be bit reversal. Choose

W=t=(N-1)/3 for evenm,
W=(N+1)/3 and t=(2N-1)/3 for oddm.

The count C_m=#{i<W:R_m(i)<t} is exactly

C_m=(N+3m-1)/9 for evenm,
C_m=(2N+3m+2)/9 for oddm.

Consequently this rectangle has discrepancy

C_m-Wt/N = m/3+1/9-(-1)^m/(9N).                 (1)

This is a proved witness value; no global-maximal-discrepancy claim is needed.

## Count recurrence

The basesm=1 andm=2 both haveC_m=1. Advance fromm tom+2, so the new length is4N, and write a new input index as4j+r. Bit reversal gives

R_(m+2)(4j+r)=N*rev_2(r)+R_m(j).

For evenm, W_new=t_new=N+W=4W+1. Among the admissible indices, residue r=0 contributesW+1 automatically; r=2 contributes exactly the old countC_m; r=1,3 contribute nothing. Thus C_(m+2)=C_m+W+1.

For oddm, W_new=N+W=4W-1 and t_new=2N+t. Residues r=0,2 each contributeW automatically, residue r=1 contributes the old countC_m, and r=3 contributes nothing. Thus C_(m+2)=C_m+2W.

Induction gives the displayed count formulas. Subtracting Wt/N proves(1).

## Fourier consequence

For four order-one stages in the word S4 R S3 A3 S2 R S1, conjugation byA3 has order at most5 and the merged middle stage has order at most6. The three-stage discrepancy theorem therefore forces

D_grid(R) <= 2+6+1=9.

But(1) is strictly greater than9 for everym>=27. Hence this particular four-stage architecture cannot equal the natural complex Fourier matrix at any dyadicN>=2^27. An affine output endpoint still suffices even with arbitrary input reordering, because the proof uses the output-prefix discrepancy inequality.

This is an explicit sufficient exclusion threshold, not the optimal first failing size. It neither requires nor asserts a huge exact maxflow run. The unspecified-constant Schmidt theorem is unnecessary for this quantitative consequence. No unrestricted arithmetic lower bound follows.
