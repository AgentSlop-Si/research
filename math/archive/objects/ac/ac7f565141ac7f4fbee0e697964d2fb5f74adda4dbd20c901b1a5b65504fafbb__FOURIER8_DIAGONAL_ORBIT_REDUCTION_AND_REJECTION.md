# Fourier-8: a whole half-anchor diagonal-orbit rejection and a smaller exact interface

## Result and scope

No positive Fourier-8 kernel is claimed.

There are two rigorous results in this package:

1. The entire nonsingular diagonal orbit of the half-pair radix-2 anchor is impossible when the remaining paired-Green factor has the two explicitly stipulated, noncommuting Hamiltonian support orders below. This allows arbitrary diagonal endpoints and arbitrary edge coefficients, including zero. It is strictly broader than fixing the anchor itself, but remains one specified-factor, specified-support chart.
2. For the adjacent-pair anchor orbit and the same new support pair, a stated open chart is exactly equivalent to 40 explicit polynomial equations in 12 variables, with complete guards and direct reconstruction. Solvability of this adjacent-anchor chart is not established. The package also generates the half-anchor interface, which the first result proves empty.

These results do not exclude a free first layer, other remaining-factor orders, arbitrary endpoint permutations, or a general two-layer Fourier-8 kernel. They do not extend the earlier eight fixed-anchor certificates without proof. No earlier research executable was imported or run.

## 1. Field, branch grammar, and new support pair

Let zeta be a primitive eighth root, i=zeta^2, and F[r,s]=zeta^(rs). Work over any field of characteristic different from 2 containing zeta, or an extension. The exact stored coefficients lie in Z[zeta]/(zeta^4+1).

A branch inverse has the form Q=diag(a)+diag(b)P, where P e_j=e_pi(j), pi is an 8-cycle, every a_j is nonzero, and Q is invertible. This is precisely the diagonal-endpoint Green grammar for this specified support. The row-normalized form has Q=D_rho U, U=I+diag(u)P_pi. The column-normalized second branch has Q=V D_tau, V=I+P_sigma diag(v). Requiring every edge nonzero adds u_j,v_j != 0; the obstruction below does not need that extra restriction.

The orders used here are:

    pi:    [0,1,2,3,4,5,6,7]
    sigma: [0,2,5,1,7,4,6,3]

Their directed edge sets are disjoint. They do not commute: pi(sigma(0))=3 whereas sigma(pi(0))=7. This is not one of the four pairs in the earlier eight fixed-anchor charts.

Write p=pi^(-1) and s=sigma^(-1). For each column j, the support union is {j,pi(j),sigma(j)}. Choose pivot row k_j as the least index outside that union:

    (k_0,...,k_7)=(3,0,0,1,0,0,0,1).

## 2. Arbitrary outer diagonals of an anchor reduce to four ratios

Let K be block [[1,1],[1,-1]] on either the adjacent pairs (0,1),(2,3),(4,5),(6,7), or the half pairs (0,4),(1,5),(2,6),(3,7). Thus K^2=2I.

Consider first factors X1=A K B with arbitrary nonsingular diagonal A,B. This is the full diagonal orbit of this anchor, not merely X1=K. If F=X2 X1, then

    X2 A=F B^(-1) K/2.

Write B^(-1)=T C, where C is constant on each pair and T[a_j]=1, T[b_j]=t_j. Every t_j is nonzero. Since C commutes with K,

    (X2 A) C^(-1)=F T K/2.

Multiplication of a paired-Green factor by nonsingular diagonals preserves its two specified inverse supports. Therefore the whole anchor diagonal orbit is equivalent to asking whether

    M=F T K

is a sum of two allowed inverse branches on the specified supports. A solution M=Q0^(-1)+Q1^(-1) gives the exact Fourier factorization

    F=[(Q0^(-1)+Q1^(-1))/2] [K T^(-1)].

The factor 1/2 must be included: actual second-factor inverse branches are 2Q0 and 2Q1.

The entries of M are explicit:

    M[r,a_j]=zeta^(r a_j)+t_j zeta^(r b_j),
    M[r,b_j]=zeta^(r a_j)-t_j zeta^(r b_j).

The anchor itself remains a legal sparse-mask paired-Green layer. For completeness, take support orders [b0,a0,b1,a1,...] and [a0,b0,a1,b1,...]. The first W retains only edges b_j -> a_j with weight 1/i; the second retains only a_j -> b_j with weight 1/(-1-i). Both W square to zero. Left endpoints iI and diag(1-i on a_j,-1-i on b_j), respectively, give K. These constants are valid in every stated field because i has order 4. Both Green guards equal 1, and all endpoints are nonsingular. Multiplication on the right by T^(-1) preserves that. Connecting weights are zero: this does not supply a construction with all first-factor cycle edges nonzero.

## 3. Exact direction and scale restoration

Suppose M=Q0^(-1)+Q1^(-1), with Q0=D_rho U and Q1=V D_tau as above. Put x_i=rho_i^(-1), y_j=tau_j^(-1). Then

    U M V=U D_y+D_x V.                                      (1)

For each row and column define

    A_ij=M_ij+u_i M_[p(i),j],
    C_ij=M_[i,sigma(j)]+u_i M_[p(i),sigma(j)],
    a_j=A_[k_j,j],       c_j=C_[k_j,j],
    h_ij=c_j A_ij-a_j C_ij.

Off the support union, (1) says A_ij+v_j C_ij=0. Consequently every h_ij in that off-support region must vanish, even if a_j or c_j vanishes. These are necessary minors, without a pivot-nonvanishing assumption.

For a constructive iff open chart, require every u_i,a_j,c_j to be nonzero. Then all column directions are explicitly

    v_j=-a_j/c_j,

and (U M V)_ij=h_ij/c_j. The disjoint edge supports now recover every scale:

    x_i=-h_[i,s(i)]/a_[s(i)],
    y_j=h_[pi(j),j]/(c_j u_[pi(j)]).

The complete zero equations are:

* h_ij=0 for i outside {j,pi(j),sigma(j),k_j}: 32 equations.
* For i=0,...,7, with l=s(i):

    u_[pi(i)] a_l h_ii + c_i u_[pi(i)] h_[i,l]
        - a_l h_[pi(i),i] = 0.                              (2)

The second set enforces the eight diagonal scale equations. The remaining 16 support equations hold by the explicit scale definitions. Thus this is sufficient as well as necessary on the stated chart; no column-direction or scale-completion gap remains.

The full nonzero guards are:

* t_0,...,t_3 and u_0,...,u_7;
* a_j and c_j for every j;
* h_[pi(j),j] and h_[sigma(j),j] for every j;
* 1-product(u_j);
* product(c_j)-product(a_j).

The last two are the U and V invertibility guards, because 8 is even. Recover Q0=diag(1/x)U and Q1=V diag(1/y). Their diagonal coefficients, edge coefficients, endpoint masks, and Green denominators are all nonzero under these guards.

There are 12 variables t0,...,t3,u0,...,u7. Each exported system has 40 equations of maximum total degree 7. The adjacent system has 890 monomials across these equations; the half system has 880. The files contain exact expanded coefficients and reconstructible formula references. Zero-pivot branches are outside this iff chart, not implicitly excluded.

## 4. Whole half-anchor diagonal-orbit obstruction

This rejection uses only necessary off-support minors. It therefore does not require the open-chart guards a_j,c_j != 0, does not require nonzero edges, and does not depend on the scale reconstruction. Nonsingular diagonal endpoints and t_j != 0 remain part of the branch and anchor grammar.

For the half anchor, four exact minors are

    h_2,5 = -4 t1 zeta (u0-u2),
    h_3,5 =  4 t1 zeta (i-u0 u3),
    h_4,5 = -4 t1 zeta^3 (u0-u4),
    h_7,5 = -4 t1 zeta (i-u0 u7).

Hence w=u0 is nonzero and

    u2=u4=w,       u3=u7=i/w.                              (3)

After this substitution,

    w(h_4,0+h_3,4)=-4i(t0+t2).

Thus put a=t0 and t2=-a. The h_4,0 and h_2,4 equations respectively become

    E=(a^2+1)(1+i)w+i(1-a^2)=0,
    R S=0,

where

    R=(a+1)w-(a-1),
    S=-i(a-1)w-(a+1).

E and w != 0 rule out a=1 and a=-1. Set q=a^2-2ia+1 and C=(a^2+1)(1+i). The following exact identities give q=0 whichever factor of R S vanishes:

    (a+1)E = C R + (a-1)q,
    i(a-1)E + C S = -i(a+1)q.

Since a != 0 and q=0 imply a^2+1=2ia != 0, C != 0. The first identity gives R=0. Finally

    (a+1)^2(w^2-i)-(1-i)q
        = R[(a+1)w+(a-1)]

forces w^2=i.

The remaining necessary minor h_7,2 becomes

    w h_7,2=(1-a)J,
    J=(t1+1)w(zeta^3-zeta)+(t1-1)(1+i).

As a != 1, J=0. But (zeta^3-zeta)^2=2 and (1+i)^2=2i, so

    J[(t1+1)w(zeta^3-zeta)-(t1-1)(1+i)]
       =2(t1+1)^2(w^2-i)+8i t1
       =8i t1 != 0.

This contradiction rejects the whole half-anchor diagonal orbit for this support pair. Exactly eight necessary minors are used. All algebraic identities are independently checked as sparse exact polynomials by the supplied standard-library verifier. No finite-field extrapolation or numerical residual is used in this proof.

## 5. Verification, reproducibility, and honest cost

Run:

    python3 build_and_verify_interface.py

The script freshly generates both exact JSON systems and the reports. It also checks four exact rational positive controls manufactured from legal full-edge Q branches. On each it recovers every column direction and scale, verifies all 40 equations and the full inverse-sum identity, and rejects an entry-perturbed negative control. These controls validate the general interface; they are not Fourier solutions. Four splitting-prime checks per anchor separately compare all 88 exported polynomial expressions with direct formulas and check (F T K/2)(K T^(-1))=F. Finally, 12 exact coefficient identities verify the characteristic-zero obstruction, which the proof extends to any stated field.

The adjacent-anchor system is an explicit next coefficient-solving target. Root finding, field extensions, algebraic-number representation, guard testing, and coefficient recovery are not free. No running-time bound for solving it is established. With a guarded solution already supplied, recovery is fixed-size arithmetic, and applying four supplied length-8 Green branches is O(8) field arithmetic, with endpoint multiplies, permutations, additions, and all eight outputs charged. Bit complexity depends on coefficient representation.

This finite interface yields no growing-N FFT algorithm. Direct sums of local 8-cycles are not one global Hamiltonian N-cycle. Any global batching or stitching construction must explicitly supply its orders, masks, guards, extra terms, setup, and all-output application cost. No such free lift is assumed here.

The optional shifted-chart numerical probe is a separately labeled bounded exploratory record: 15 shift pairs, four starts each, at most 1200 function evaluations per start. It found no candidate; that fact proves no obstruction and is not used anywhere in the exact results. It requires NumPy/SciPy; the theorem verifier does not.

The mechanisms are algebraic support elimination and gauge normalization. Related projective/quantum-2-SAT methods are already known; novelty has not been established or claimed.
