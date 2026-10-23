# Cycle propagation closes the odd-semiprime degree window

Date: 2026-10-23 UTC. Separate strengthening candidate, pending independent acceptance. The earlier accepted compatibility packet is unchanged. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No historical novelty, full support classification, exact nonsharp optimum, sharp gap rate, paid-cost result, or Fourier/FFT gain is claimed.

## 1. Exact new target

Let p<q be odd primes with p>=7, N=pq, and zeta any primitive complex Nth root. For an arbitrary binary N-by-N matrix R put

    D[r,c]=R[r,c] zeta^(rc).

**Candidate theorem.** A mask satisfying either D*D=dI or DD*=dI exists exactly at

    d in {0,1,p,q,pq}.

There is no prime-ratio restriction. Combining this new p>=7 result with the separately accepted p=3 and p=5 classifications gives the same degree-existence statement for every pair of distinct odd primes p<q. The accepted 3q and 5q families are inherited, not redispatched or counted as new credit.

The argument below is valid for every odd p>=3, but the new scientific credit starts at p>=7. It stays in the original binary fixed-Fourier square model, retaining both row and column consequences of either square Gram identity. No free phases, common-support spectral set, Cartesian restriction, rectangular replacement, or finite-field substitution is used.

## 2. Accepted inputs and original coordinates

The accepted compatibility report and independent acceptance are copied under sources/. The report SHA-256 is 1a51d0d0e7b3a5e418eee5b5660e5752ac14fc7b1da7e26a6e0d68a2c64b010d; the exact accepted manifest hash is e8d5d819224c7cc881b9961142e4b2b3463c5bb5a39469292a89c1334ba6924b. Its Theorem A already excludes every proper degree d>p+q-1 at all odd prime ratios, and its low-range argument leaves only 1,p below q. The original divisor masks give 0,1,p,q,pq. The new task is therefore precisely

    q<d<=q+p-1.

All d in this window are positive and less than 2q. Either square Gram identity implies the other and forces every row and column degree to be d.

Use the literal CRT idempotents e_p=q(q^{-1} mod p), e_q=p(p^{-1} mod q), original row r=a e_p+b e_q, and original column c=u e_p+v e_q. Then exactly

    zeta^(rc)=alpha^(au) beta^(bv),
    alpha=zeta^e_p, beta=zeta^e_q.

Write G_a for the q rows with first coordinate a, F_v for the p columns with second coordinate v, and L_u for the q columns with first coordinate u. On the row grid a complete q-line is G_a and a complete p-fiber has fixed b. On the column grid they are L_u and F_v.

We use the same already credited classical facts:

- Distinct rows of G_a have overlap counts in F_v independent of v. In the current window these counts are at most one, since the full overlap is at most d<2q.
- Rows differing in both coordinates have binary overlap equal to a union of complete p-fibers or a union of complete q-lines.
- Rows with equal b and different a have equal overlap counts across all p lines L_u.

The analogous statements hold for columns because the second Gram is available. The primitive cancellation statement is classical de Bruijn/Lam-Leung content, not new progress. The new ingredient is how pair-dependent cancellation propagates through column degrees.

## 3. The cycle-propagation lemma: a q-line must exist

We prove a slightly wider lemma. Suppose q<d<pq and assume, for contradiction, that **no row support contains a complete q-line**.

Call a supported entry (r,c), r=(a,b), deficient if its row does not contain the complete p-fiber F_v through c. If a row s differing from r in both coordinates supported c, primitive cancellation would force the complete line or fiber through c into S_r. Both are excluded: q-lines are absent everywhere by the assumption, and this fiber is absent from r by deficiency. Thus the entire support T_c of column c lies in the coordinate cross

    X_r = { (a,b'): b' in Z/q } union { (a',b): a' in Z/p }.

Column c has d>q supporters. Hence some s=(a',b) with a'!=a supports c. Any further supporter t=(a,b') in G_a with b'!=b differs from s in both coordinates. Their primitive overlap contains c. A q-line is unavailable in either row, so both t and s contain the full p-fiber F_v through c.

There can be at most one such t in G_a. If two rows of G_a contained F_v, their overlap would have p points in one fiber; prime-q balance would force p points in every fiber, giving overlap pq>d, impossible. Therefore T_c has at most two members in G_a (r and at most one t) and at most p-1 outside G_a. This gives

    d<=p+1<q+1<=d,

since distinct odd primes obey q>=p+2. Contradiction. No deficient entry exists.

Every row support is consequently a union of complete p-fibers. Within any G_a these fiber sets are pairwise disjoint by the same balance argument. There are q rows and only q fibers, whereas each row has d>q>p entries and must contain at least two fibers. This is impossible.

We conclude:

    If q<d<pq, at least one row contains a complete q-line.  (3.1)

No support geometry was imposed. This is a global compatibility consequence of column degrees and pair-dependent overlaps.

## 4. The interior q<d<q+p-1 is impossible at every prime ratio

Write d=q+t with 1<=t<=p-2. By (3.1), some row r=(a,b) consists of a complete line L_u and exactly t extra columns. The line is unique because d<2q. This row contains no complete p-fiber: completing any fiber beyond its one baseline entry requires p-1 extras. It also misses at least one line L_w, because it meets at most t+1<=p-1 lines.

Choose any extra column c in S_r outside L_u. A row s from another group cannot support c:

- If b_s!=b, the pair is primitive. The complete cycle through c would have to lie in r. That cannot be a q-line (r's only full line is L_u) or a p-fiber (r has none).
- If b_s=b, order-p balance makes the pair's overlap counts equal across all lines. The missing line L_w has count zero, so their entire overlap is empty.

Hence column c is supported only by the q rows of G_a, contradicting its required degree d>q. This excludes every t=1,...,p-2, with no separated-prime condition.

## 5. A q-line row at the boundary must be an exact cross

Now d=q+p-1. By (3.1), choose a row r=(a,b) containing its unique complete q-line L_u, plus p-1 extra columns T outside L_u.

Suppose r contains no complete p-fiber. For each c in T, a primitive supporting partner is impossible for the same reason as in Section 4. Thus column c has support contained in X_r. But

    |X_r|=q+p-1=d,

so **every extra column has exactly the same support X_r**. This is derived from regularity, not a common-support assumption.

Take any two distinct extra columns c_1=(u_1,v_1), c_2=(u_2,v_2). They exist because p-1>=2. Put delta_u=u_1-u_2 and delta_v=v_1-v_2. Their original column Gram on the common cross X_r is

    sum_(x,y in X_r) alpha^(x delta_u) beta^(y delta_v)
      = alpha^(a delta_u) beta^(b delta_v)
        [q 1_(delta_v=0)+p 1_(delta_u=0)-1].            (5.1)

The bracket is -1 if both differences are nonzero, p-1 if only delta_u is zero, or q-1 if only delta_v is zero. Since the columns are distinct these exhaust the possibilities, and every bracket is nonzero. This contradicts column orthogonality.

Thus r must contain a full p-fiber. Because it has only p-1 extra entries beyond L_u, all those extras complete exactly one fiber F_v, giving

    S_r=L_u union F_v.

Every q-line row at this boundary is therefore an exact cross. It suffices that one such row exists.

## 6. One cross row already violates global incidence capacity

Let r=(a,b) be the cross row from Section 5 and let

    T=F_v minus L_u,       |T|=p-1.

The total number of incidences of all rows with these columns must be

    (p-1)d=(p-1)(q+p-1).                              (6.1)

We bound that total using row-group compatibility.

### The group G_a of the cross row

Row r contributes p-1 incidences to T. For any other row t in G_a, same-group overlap counts with r are at most one in each fiber, since d<2q. Because r contains all of F_v, row t can contain at most one point of F_v, hence at most one point of T. Thus this group contributes at most

    (p-1)+(q-1)=q+p-2.                               (6.2)

### Each other group G_a'

For a row s=(a',b') with b'!=b that meets T, primitive cancellation forces s to contain F_v: the q-line through any c in T is not fully present in r. There is at most one such row in G_a', because two rows sharing a full fiber would force overlap pq>d by same-group balance.

There is also at most one row of G_a' with b'=b. If it meets T, order-p balance makes every line-overlap count equal. For any line different from L_u, r contains only the one point of that line lying in T. A nonempty overlap there forces all these counts to equal one, so this same-b row contains **all of T**. It need not contain (u,v), and no such extra conclusion is used.

These two possible supporters cannot both exist. If the primitive full-fiber supporter and the same-b supporter were distinct rows of G_a', they would share all of T, hence at least p-1>=2 points in F_v. But same-group overlap counts are at most one in every fiber because d<2q. This is a contradiction.

Therefore at most one row of each other group G_a' meets T, and that group contributes at most p-1 incidences. Across all p-1 other groups the bound is (p-1)^2. Combining with (6.2), the total capacity is at most

    q+p-2+(p-1)^2.

Subtracting this from the required incidence count (6.1) gives

    (p-1)(q+p-1)-[q+p-2+(p-1)^2]
      =(p-2)(q-1)>0.                                (6.3)

Contradiction. The boundary d=q+p-1 is impossible for every odd p>=3 and q>p. In particular, the entire previously unresolved p>=7 close-prime window is excluded. The exclusion uses only one derived cross row, not a classification of all row groups.

## 7. Completion, original inverse-row translation, and limits

The accepted all-ratio dense theorem excludes p+q-1<d<pq, Sections 4-6 exclude q<d<=q+p-1, and the accepted low range excludes 1<d<q except d=p. Zero, one, p, q, and pq all have the original fixed-phase divisor constructions. This proves the exact degree-existence classification at every p>=7,q>p.

The accepted p=3 and p=5 theorems then supply the remaining distinct odd-prime pairs. Their proofs, scope, and prior credit are unchanged. This is not a new support-pattern classification even at the allowed degrees.

The separately accepted original inverse-row equality/attainment criterion is retained as sources/INVERSE_ROW_ACCEPTANCE.md (original report SHA-256 1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee). For the original normalized Fourier target and 1<=s<=pq-1, the combined odd-semiprime degree result implies

    Delta(pq,s)=sqrt(1-s/(pq))
    iff s in {pq-1,pq-p,pq-q}.

Every other budget has a strict infimum gap, not merely nonattainment. This translation supplies no exact larger optimum or quantitative optimal gap. Degree pq is a mask witness only and corresponds to the inadmissible inverse budget s=0.

The p=11,q=23,d=33 rectangular Fano block from the earlier packet remains valid and unchanged. It shows that a purely local row-group single-clique reduction can fail even beyond q>2p-2. The present proof does not deny that example, does not turn it into a square mask, and does not require every row group to be a single clique. Its new global propagation and one-cross-row capacity argument bypass that local obstruction.

All results concern distinct odd semiprimes. General mixed-prime/composite orders, all support patterns, exact nonsharp optima, sharper or optimal gap rates, sparse-column and fixed-frame commutator problems, paid preparation/solve/decomposition/output costs, stability, implementation, and historical novelty remain outside this result. Owner status remains TO RESEARCH, priority 42.

## 8. Fresh controls and independent gate

Fresh self-authored exact controls accompany this addendum. They execute no candidate or historical scientific program. Their finite counts validate formulas and positive/negative controls; they do not prove the universal theorem. The new symbolic proof requires its own independent acceptance, separate from the accepted restricted packet.

Completed controls: 24 full original-index square masks at (p,q)=(7,11),(7,13),(11,13), with both degree counts, 4,976 Gram diagonals, and 549,568 off-diagonal Gram entries. Positive degrees 1,p,q,pq pass both Grams. Regular negative interior and boundary controls fail both Grams. An additional 1,824 literal cross-character checks cover all nonzero coordinate differences at the recorded centers, including same-first-coordinate and same-second-coordinate cases. Integer contradiction checks cover every odd prime pair p<q<=100. Normal and Python -O runs execute the same explicit checks and have identical scientific counts. Both final stderr logs are empty.
