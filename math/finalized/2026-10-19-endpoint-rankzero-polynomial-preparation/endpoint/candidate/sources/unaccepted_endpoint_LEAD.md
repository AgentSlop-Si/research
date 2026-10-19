# Uniform endpoint exclusion at N = 3q, d = 2q

Date: 2026-10-19 (UTC). New analytic result, submitted for independent review.

## Statement

Let q>3 be prime. There is no binary 3q-by-3q Fourier mask D[r,c]=R[r,c] zeta_(3q)^(rc) with DD*=D*D=2q I.

This excludes one infinite family of degrees left at the endpoint of the general upper-range theorem. It does not classify all degrees for N=3q.

## Coordinates and cancellation facts

Use CRT coordinates r=(a,b) in Z/3 x Z/q and c=(u,v) in Z/3 x Z/q, absorbing harmless units into the primitive roots so the character is omega_3^(au) omega_q^(bv). Every row and column support has size 2q. A column fiber is F_v, the three columns with fixed v.

Rows in one fixed a-group have overlap q or 2q: overlap is at least 4q-3q=q, is a multiple of q by prime character cancellation, and is at most the row degree 2q. Their restrictions to each F_v therefore have scalar product respectively one or two, independent of v. Overlap 2q holds exactly when their complete supports are identical.

A primitive-character binary overlap at order 3q is either a union of full three-element fibers, or a union of full q-element lines with fixed u. This follows from the elementary binary CRT vanishing-sum lemma.

## Step 1: every row has exactly two entries in every column fiber

Fix one a-group of q rows. Suppose some row r contains all three columns in a fiber F_v. It cannot share its complete support with another row: two such rows would have fiber scalar product three, whereas the allowed values are one or two. Its overlap with every other row is therefore q. At F_v each other row must consequently have weight one.

The other q-1 singleton restrictions cannot differ, since their scalar products must be one or two rather than zero. They are all the same singleton. Hence every pair of different rows in the entire a-group has overlap q. Their restrictions in every fiber have pairwise scalar product one.

Any family of q>=5 binary length-three vectors with pairwise scalar product one has a common singleton baseline and at most two extra entries in total. To prove this: zero vectors are impossible; if every weight were at least two, the only possible family consists of distinct two-subsets, of which there are at most three (a weight-three vector cannot coexist with a weight-two vector). Thus some vector is a singleton. All others contain its coordinate, and their extra-coordinate sets are pairwise disjoint, giving at most two extras.

Summing over q fibers, the total number of entries in this a-group is at most q(q+2), less than the required q(2q), contradiction. Thus no row restriction has weight three. Each row has total weight 2q across q fibers and every restriction has weight at most two, so every restriction has weight exactly two.

For a row r define its missing-column function f_r(v) in Z/3: the unique column omitted by r in F_v.

## Step 2: a repeated missing function is constant

Within one a-group, two rows whose restrictions agree in even one fiber have fiber overlap two, hence complete overlap 2q and identical full supports. There are only three possible two-element restrictions in a fiber. Thus the q rows have at most three distinct missing functions. Since q>3, some missing function f is shared by two distinct rows r_1,r_2.

Take any row s in another a-group, with missing function g. At most one of r_1,r_2 has the same b-coordinate as s, so s differs primitively from at least one of them. The corresponding intersection has one or two entries in every fiber. It cannot be a union of full three-element fibers, so it is a union of q-lines. Therefore its subset of u-coordinates is fixed, independently of v.

If f is nonconstant, this fixed intersection cannot have size two: that would force both supports, and hence f, to be constant. It must have size one, say the coordinate t. Then in every fiber f(v) and g(v) are the two distinct coordinates other than t. Because f is nonconstant, it uses exactly those two coordinates, which determine t uniquely; g is uniquely determined as its pointwise swap.

Consequently, if f were nonconstant, every one of the 2q rows in the other two a-groups would have exactly the same missing function g. A column omitted by g would then receive no entries from those 2q rows and at most q entries from the original a-group, contradicting its required degree 2q. Thus f is constant.

## Step 3: all missing functions are constant

For any row s in another a-group, the preceding primitive-overlap argument says that its support intersects the constant two-coordinate support of f in a fixed subset of coordinates in every fiber. If this subset has size two, g=f is constant. If it has size one, the second omitted coordinate is fixed, so g is again constant. Hence every row in both other a-groups has a constant missing function.

Choose either of those groups. Its q>3 rows take only three possible constant missing functions, so one is repeated. Applying the same primitive-overlap argument to that repeated function and every row in the original a-group forces all original missing functions to be constant too.

Thus every row support consists of two entire q-lines with fixed u-coordinates.

## Step 4: contradiction from an order-three row difference

Choose two rows in different a-groups but with the same b-coordinate. Their phase difference has order three. Each row uses two of the three q-lines, so their intersection consists of one or two whole q-lines. Their scalar product is q times the sum of one or two distinct third roots of unity, multiplied by a unit phase. Such a sum is nonzero. This contradicts row orthogonality.

The proof is complete. No finite census is used. No historical program, external write, repository change, or owner-status update was performed.
