# New exact C8 rank-zero upper witness

Proved an explicit upper bound in the full original model:

sin(3 pi/16) < delta_(8,0) <= sqrt(1+sqrt(sqrt(2)-1))/2
=0.6410136997181851621....

The left inequality is the accepted earlier result. The right inequality is new to this packet and is proved by an exact four-periodic phase witness. It improves 1/sqrt(2) by 0.06609308146836236..., and reduces the previously certified interval width by about 43.61 percent.

The result is not claimed to be the exact optimum. No global periodicity reduction is claimed. The construction does not invoke the retracted anti-diagonal shortcut. There were no external writes, uploads, commits, or historical-code executions.

The witness is given explicitly in PROOF.md, Section 2. Its 8-by-8 matrix decomposes into four exact 2-by-2 unitary blocks, with trace/determinant pairs (1-h,1) twice and (exp(-i pi/4)(1+h),-i) twice, h=sqrt(sqrt(2)-1). Their eigenvalues prove the claimed residual norm exactly. The original-model real core and both outer monomial matrices are specified.

The fresh exact checker passes all 15 checks. Review should focus on the sector basis and Fourier convention, exact phase-square identities, both block types, angle-branch selection, and transfer from the unitary spectrum to the external residual. Independent review has not yet been performed on this packet.

Stopping condition: the requested materially stronger explicit bound is established and frozen. Exact global minimax remains open; no further computation is running.
