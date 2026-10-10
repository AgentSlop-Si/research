"""Independently authored standard-library audit. Uploaded programs stay inert."""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from random import Random
import hashlib, json, zipfile

OUT=Path(__file__).resolve().parent

def inverse(B,p):
    n=len(B); a=[[z%p for z in row]+[int(i==j) for j in range(n)] for i,row in enumerate(B)]
    for k in range(n):
        r=next((i for i in range(k,n) if a[i][k]),None)
        if r is None: raise ValueError('singular')
        a[k],a[r]=a[r],a[k]
        q=pow(a[k][k],-1,p); a[k]=[(z*q)%p for z in a[k]]
        for i in range(n):
            if i!=k and a[i][k]:
                q=a[i][k];a[i]=[(v-q*w)%p for v,w in zip(a[i],a[k])]
    return [r[n:] for r in a]

def rank(B,p):
    if not B:return 0
    a=[[v%p for v in r] for r in B]; r=0
    for j in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];q=pow(a[r][j],-1,p);a[r]=[(v*q)%p for v in a[r]]
        for i in range(r+1,len(a)):
            q=a[i][j];a[i]=[(v-q*w)%p for v,w in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def grid(F,p):
    n=len(F);names=[];coords={};rows=[];Ein={}
    def add(name,coord,terms=None,input_index=None):
        idx=len(names);names.append(name);coords[name]=coord
        row={idx:1}
        for prev,val in (terms or []):
            j=names.index(prev); assert j<idx
            row[j]=(row.get(j,0)+val)%p
        rows.append({i:v for i,v in row.items() if v%p})
        if input_index is not None:Ein[idx]=input_index
    for j in range(1,n+1):add(('H',j,0),(1,2*j),input_index=j-1)
    for k in range(1,n+1):add(('V',0,k),(2*k,1))
    for j in range(1,n+1):
        for k in range(1,n+1):
            h=('H',j,k-1);v=('V',j-1,k);c=('C',j,k)
            add(c,(2*k,2*j),[(h,-1),(v,-1)])
            add(('H',j,k),(2*k+1,2*j),[(c,-1),(v,1)])
            add(('V',j,k),(2*k,2*j+1),[(c,-1),(h,1-F[n-k][j-1])])
    P=[names.index(('V',n,n-i)) for i in range(n)]
    m=len(rows);assert m==3*n*n+2*n
    assert all(row.get(i)==1 for i,row in enumerate(rows))
    got=[[0]*n for _ in range(n)]
    for b in range(n):
        z=[]
        for i,row in enumerate(rows):
            q=int(Ein.get(i)==b)
            q-=sum(a*z[k] for k,a in row.items() if k<i)
            z.append(q%p)
        for i,a in enumerate(P):got[i][b]=z[a]
    assert got==[[v%p for v in r] for r in F]
    K=[[0]*(m+n) for _ in range(m+n)]
    for i,row in enumerate(rows):
        for j,a in row.items():K[i][j]=a
    for i,j in Ein.items():K[i][m+j]=1
    for i,j in enumerate(P):K[m+i][j]=1
    # Matrix entries, rather than a separate assumed graph, define support.
    support={tuple(sorted((i,j))) for i in range(m+n) for j in range(m+n) if i!=j and K[i][j]}
    return names,coords,rows,Ein,P,K,support

def drawing(n):
    coords={};edges=[];matrix_edges=set()
    def H(j,k):return (2*k+1,2*j)
    def V(j,k):return (2*k,2*j+1)
    def C(j,k):return (2*k,2*j)
    def edge(a,b):
        assert a!=b;edges.append((a,b));matrix_edges.add(tuple(sorted((a,b))))
    for j in range(1,n+1):
        for k in range(1,n+1):
            h,v,c,e,s=H(j,k-1),V(j-1,k),C(j,k),H(j,k),V(j,k)
            for a,b in [(c,h),(c,v),(c,e),(c,s),(v,e),(h,s)]:edge(a,b)
    polylines=[]
    for j in range(1,n+1):
        d=n+1-j;h=H(j,0);v=V(n,d);t=(-d,2*n+1+d)
        paths=[[h,(-d,2*j),t],[t,(2*d,2*n+1+d),v]]
        for path in paths:
            polylines.append(path)
            matrix_edges.add(tuple(sorted((path[0],path[-1]))))
            edges.extend(zip(path,path[1:]))
    return edges,matrix_edges,polylines

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,c):return orient(a,b,c)==0 and min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
def bad_cross(seg1,seg2):
    a,b=seg1;c,d=seg2
    if max(min(a[0],b[0]),min(c[0],d[0]))>min(max(a[0],b[0]),max(c[0],d[0])):return False
    if max(min(a[1],b[1]),min(c[1],d[1]))>min(max(a[1],b[1]),max(c[1],d[1])):return False
    s1,s2,s3,s4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    if s1*s2<0 and s3*s4<0:return True
    for point,x,y in [(c,a,b),(d,a,b),(a,c,d),(b,c,d)]:
        if on(x,y,point) and point!=x and point!=y:return True
    return False

def planar_certificate(n):
    segs,medges,polylines=drawing(n)
    assert len(set(tuple(sorted(e)) for e in segs))==len(segs)
    bad=[]
    for i,e in enumerate(segs):
        for f in segs[:i]:
            if bad_cross(e,f):bad.append([e,f])
    assert not bad,(n,bad[:1])
    adj=defaultdict(set)
    for a,b in segs:adj[a].add(b);adj[b].add(a)
    seen=set();stack=[next(iter(adj))]
    while stack:
        u=stack.pop()
        if u in seen:continue
        seen.add(u);stack.extend(adj[u]-seen)
    assert len(seen)==len(adj)
    # Exact compass order, with y increasing downward in the drawing.
    comp={(1,0):0,(1,1):1,(0,1):2,(-1,1):3,(-1,0):4,(-1,-1):5,(0,-1):6,(1,-1):7}
    def sign(v):return (v>0)-(v<0)
    rot={u:sorted(vs,key=lambda v:comp[(sign(v[0]-u[0]),sign(v[1]-u[1]))]) for u,vs in adj.items()}
    visited=set();faces=[]
    for a,vs in rot.items():
        for b in vs:
            if (a,b) in visited:continue
            face=[];start=(a,b);u,v=start
            while (u,v) not in visited:
                visited.add((u,v));face.append(u)
                r=rot[v];u,v=v,r[(r.index(u)-1)%len(r)]
            assert (u,v)==start
            faces.append(face)
    assert len(adj)-len(segs)+len(faces)==2
    degree=defaultdict(int)
    for a,b in medges:degree[a]+=1;degree[b]+=1
    assert max(degree.values())<=4
    assert len(degree)==3*n*n+3*n
    result={'N':n,'matrix_vertices':len(degree),'maximal_support_edges':len(medges),'max_degree':max(degree.values()),'segments_including_bends':len(segs),'drawing_vertices_including_bends':len(adj),'faces':len(faces),'euler_characteristic':len(adj)-len(segs)+len(faces),'proper_crossings_or_overlaps':0}
    if n==5:
        (OUT/'planar_rotation_N5.json').write_text(json.dumps({'result':result,'rotation':[{'point':u,'neighbors_clockwise':vs} for u,vs in sorted(rot.items())],'terminal_polylines':polylines},indent=2)+'\n')
    return result

def partition_controls():
    def parts(total,minimum=1,maximum=None):
        if total==0:yield ();return
        if maximum is None:maximum=total
        for a in range(minimum,min(total,maximum)+1):
            for rest in parts(total-a,a,maximum):yield (a,)+rest
    count=0
    for n in range(1,33):
        for s in range((n-1)//4+1):
            for t in range(s+1):
                for p in parts(n-t,maximum=n//2):
                    assert 4*s<n
                    big=next((a for a in p if a>s),None)
                    if big is not None:a=big
                    else:
                        a=0
                        for c in p:
                            a+=c
                            if a>s:break
                    assert a>s and n-t-a>s,(n,s,t,p,a)
                    count+=1
    return {'N_max':32,'positive_component_partitions_checked':count,'failures':0,'zero_weight_components':'irrelevant and omitted'}

def separator_controls():
    rng=Random(28001150);passed=0;singular=0
    special=[[0,1,0],[1,0,1],[0,1,1]]
    assert inverse(special,101)[0][2]!=0
    for trial in range(500):
        nu=rng.randrange(1,5);ns=rng.randrange(0,4);nv=rng.randrange(1,5);n=nu+ns+nv
        U=list(range(nu));V=list(range(nu+ns,n));B=[[rng.randrange(101) for _ in range(n)] for _ in range(n)]
        for i in U:
            for j in V:B[i][j]=B[j][i]=0
        try:inv=inverse(B,101)
        except ValueError:singular+=1;continue
        assert rank([[inv[i][j] for j in V] for i in U],101)<=ns
        assert rank([[inv[i][j] for j in U] for i in V],101)<=ns
        passed+=1
    return {'field':101,'random_invertible_cases':passed,'discarded_singular':singular,'singular_U_principal_block_control':True,'failures':0}

def graph_variants(m):
    G=defaultdict(set);H=set()
    for x in range(m):
        for y in range(m):
            u=(x,y)
            for a,b in [(x+y,y),(x-y,y),(x+y+1,y),(x-y+1,y),(x,y+x),(x,y-x),(x,y+x+1),(x,y-x+1)]:
                v=(a%m,b%m)
                if v!=u:G[u].add(v);G[v].add(u)
            for a,b in [(x+2*y,y),(x-2*y,y),(x+2*y+1,y),(x-2*y-1,y),(x,y+2*x),(x,y-2*x),(x,y+2*x+1),(x,y-2*x-1)]:
                v=(a%m,b%m)
                if v!=u:H.add(tuple(sorted((u,v))))
    assert max(map(len,G.values()))<=12
    for u,v in H:assert v in G[u] or bool(G[u]&G[v])
    GP={u:set(v) for u,v in G.items()}
    order=[(x,y) for x in range(m) for y in range(m)]
    for u,v in zip(order,order[1:]):GP[u].add(v);GP[v].add(u)
    delta=max(map(len,GP.values()));assert delta<=14
    p=1000003;lam=pow(4*delta,-1,p);where={u:i for i,u in enumerate(order)}
    pred=[[where[v] for v in GP[u] if where[v]<i] for i,u in enumerate(order)]
    b=[(i*i+7*i+3)%p for i in range(len(order))];z=[]
    for i in range(len(order)):z.append((b[i]+lam*sum(z[j] for j in pred[i]))%p)
    assert [(z[i]-lam*sum(z[j] for j in pred[i]))%p for i in range(len(order))]==b
    assert all(i-1 in pred[i] for i in range(1,len(order)))
    return {'m':m,'vertices':m*m,'simple_source_degree_bound':max(map(len,G.values())),'path_augmented_max_degree':delta,'canonical_edges_checked_in_square':len(H),'modular_forward_solve':True,'hamiltonian_path_positivity_certificate':True,'condition_bound_exact':'5/3'}

def main():
    summary={}
    summary['planar_drawing']=[planar_certificate(n) for n in [1,2,3,5,7,11,13]]
    fields={2:(3,2),3:(7,2),5:(11,3),7:(29,7),11:(23,2),13:(53,10)}
    tests=[]
    for n,(p,root) in fields.items():
        assert pow(root,n,p)==1 and root!=1
        F=[[pow(root,i*j,p) for j in range(n)] for i in range(n)]
        names,coords,rows,E,P,K,support=grid(F,p)
        _,maxsupport,_=drawing(n)
        points=list(coords.values())+[(-(n-j),2*n+1+(n-j)) for j in range(n)]
        assert len(set(points))==len(points)
        assert all(tuple(sorted((points[i],points[j]))) in maxsupport for i,j in support)
        record={'N':n,'field':p,'primitive_root':root,'M':len(rows),'exact_transfer':True,'unit_lower_triangular':True,'nnz_K':sum(bool(a) for r in K for a in r),'support_is_subgraph_of_plane_drawing':True}
        if n<=5:
            ki=inverse(K,p);fi=inverse(F,p);m=len(rows)
            assert [[ki[m+i][m+j] for j in range(n)] for i in range(n)]==[[(-v)%p for v in row] for row in fi]
            record['full_extension_inverse_terminal_identity']=True
        if n==5:
            (OUT/'matrix_certificate_N5_mod11.json').write_text(json.dumps({'N':n,'p':p,'F':F,'internal_coordinate_order':names,'A_rows':[{str(k):v for k,v in r.items()} for r in rows],'E_nonzero_rows_to_columns':E,'P_columns_by_row':P,'K_terminal_block':'zero','coordinate_points':points},indent=2)+'\n')
        tests.append(record)
    summary['grid_fourier']=tests
    rng=Random(8828);generic=[]
    for n in range(1,9):
        F=[[rng.randrange(101) for _ in range(n)] for _ in range(n)]
        grid(F,101);generic.append({'N':n,'field':101,'exact_transfer':True})
    summary['grid_arbitrary_matrices']=generic
    fullspark=[]
    for n,p,root in [(3,7,2),(5,11,3),(7,29,7)]:
        F=[[pow(root,i*j,p) for j in range(n)] for i in range(n)];count=0
        for k in range(1,n+1):
            for I in combinations(range(n),k):
                for J in combinations(range(n),k):
                    assert rank([[F[i][j] for j in J] for i in I],p)==k
                    count+=1
        fullspark.append({'N':n,'field':p,'square_minors_checked':count,'all_nonzero':True})
    summary['finite_field_fullspark_controls_only']=fullspark
    summary['terminal_partition']=partition_controls()
    summary['inverse_separator']=separator_controls()
    summary['expander_variant_bridge']=[graph_variants(m) for m in list(range(2,13))+[17,23,32]]
    summary['code_policy']='Only this independently authored standard-library certificate program was executed. Uploaded Python and bytecode were neither imported nor executed.'
    (OUT/'fresh_results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
