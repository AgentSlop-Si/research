"""Row/column path Green sum: a genuinely growing-order mixing primitive.

On an LxL grid, N=L^2, let Q transpose row-major/column-major indices.
M = T^-1 + eps Q T^-1 Q^T. With eps=1/100, two tridiagonal
solves give an O(N) application, and an all-order balanced-cut
singular-value obstruction is proved in GRID_THEOREM.md.

This does NOT compute a DFT, and does NOT establish a faster FFT.
"""

from green_solver_standalone import tri_solve
from linear_inverse import MOD


def transpose_order(side):
    """Involutory matrix-transpose permutation of length side**2."""
    return [(j%side)*side + (j//side) for j in range(side*side)]


def apply_grid(x, side, eps=None, p=MOD):
    assert side>=2 and len(x)==side*side
    if eps is None:
        eps=pow(100,-1,p)
    order=transpose_order(side)
    transformed=[x[j] for j in order]
    first=tri_solve(x,p)
    second=tri_solve(transformed,p)
    return [(first[i]+eps*second[order[i]])%p for i in range(len(x))]


def grid_edges(side):
    """Edges of the square grid; all are in one of the two path graphs."""
    result=[]
    for i in range(side):
        for j in range(side):
            v=i*side+j
            if i+1<side:result.append((v,v+side))
            if j+1<side:result.append((v,v+1))
    return result


def two_path_edges(side):
    n=side*side
    perm=transpose_order(side)
    return ([(i,i+1) for i in range(n-1)],
            [(perm[i],perm[i+1]) for i in range(n-1)])


def crossing_count(edges, selected):
    S=set(selected)
    return sum((u in S)!=(v in S) for u,v in edges)


def induced_matching_path(edges, selected):
    """Select crossing edges at spacing >=3 in each Hamilton path.

    Color edges by their position mod 3. Same-color edges in a path are
    an induced matching in the *full path*: their 2k endpoints span no
    additional path edges. Returns the largest of the three colors.
    """
    S=set(selected)
    classes=[[],[],[]]
    for i,(u,v) in enumerate(edges):
        if (u in S)!=(v in S):
            classes[i%3].append((u,v))
    return max(classes, key=len)


def grid_balanced_check(side,selected):
    assert side%2==0 and len(selected)==side*side//2
    egrid=crossing_count(grid_edges(side),selected)
    a,b=two_path_edges(side)
    e1=crossing_count(a,selected)
    e2=crossing_count(b,selected)
    assert egrid>=side, (side,egrid)
    assert e1+e2>=egrid, (side,e1,e2,egrid)
    match1=induced_matching_path(a,selected)
    match2=induced_matching_path(b,selected)
    assert len(match1)*3>=e1
    assert len(match2)*3>=e2
    # Matching endpoints must form diagonal off-cut minors.
    for path,matching in ((a,match1),(b,match2)):
        endpoints=set()
        for u,v in matching: endpoints.update((u,v))
        induced=[(u,v) for u,v in path if u in endpoints and v in endpoints]
        assert len(induced)==len(matching), (matching,induced)
    return dict(side=side, N=side*side, grid_boundary=egrid,
                first_path_boundary=e1, second_path_boundary=e2,
                first_induced_matching=len(match1),
                second_induced_matching=len(match2))
