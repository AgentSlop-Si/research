#!/usr/bin/env python3
"""Independent exact reconstruction from JSON data, never source-code imports.

The stage derivative is reconstructed by masked dense matrices; all permutation
operators are explicit matrices, avoiding the source's gather-index contexts and
prefix/suffix Jacobian implementation. Modular elimination is separately written.
"""
from pathlib import Path
import hashlib, json, math, platform, subprocess, time
import numpy as np

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'source_data'
NAMES=('d','a','b','c','e')
N=256
RESULT={"method":"independent masked dense differential; explicit permutation matrices", "N":N}
START=time.monotonic()

def read(name): return json.loads((DATA/name).read_text())
def save():
    RESULT['elapsed_seconds']=round(time.monotonic()-START,3)
    (ROOT/'FRESH_RESULTS.json').write_text(json.dumps(RESULT,indent=2)+'\n')
def emit(label,value):
    RESULT[label]=value; save(); print(label,json.dumps(value),flush=True)
def sha(a): return hashlib.sha256(np.asarray(a,dtype='<u4').tobytes()).hexdigest()
def prime(p): return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def mm(a,b,p):
    assert a.shape[1]*(p-1)**2 < 2**63
    return (a@b)%p
def compose(factors,p):
    out=np.eye(factors[0].shape[0],dtype=np.int64)
    for f in factors: out=mm(f,out,p)
    return out
def stage(g,p):
    n=len(g[0]); lower=np.tri(n,k=-1,dtype=np.int64)
    return (np.diag(g[0])+lower*np.outer(g[1],g[2])+lower.T*np.outer(g[3],g[4]))%p
def perm(column):
    v=[]
    for k in range(1<<len(column)):
        q=0
        for bit,c in enumerate(column):
            if (k>>bit)&1: q^=c
        v.append(q)
    assert sorted(v)==list(range(len(v)))
    return np.eye(len(v),dtype=np.int64)[v],v
def factors(g,P,p):
    out=[]
    for k in range(4):
        out.append(stage(g[k],p))
        if k<3: out.append(P[k])
    return out
def differential(g,P,p,rows,cols):
    """Build L dS R for all stage parameters with dense masked sums."""
    fs=factors(g,P,p); n=len(g[0][0]); low=np.tri(n,k=-1,dtype=np.int64)
    J=np.empty((len(rows)*len(cols),20*n),dtype=np.int64)
    for s in range(4):
        pos=2*s
        L=compose(fs[pos+1:],p) if pos+1<len(fs) else np.eye(n,dtype=np.int64)
        R=compose(fs[:pos],p) if pos else np.eye(n,dtype=np.int64)
        X=L[rows,:]; Y=R[:,cols]
        # Derivatives: d_i=E_ii; a_i=e_i*(b_j 1[j<i])_j;
        # b_j=(a_i 1[i>j])_i*e_j^T, and analogous upper terms.
        lefts=[X, X, mm(X,low*g[s][1][:,None],p), X,
               mm(X,low.T*g[s][3][:,None],p)]
        rights=[Y, mm(low*g[s][2][None,:],Y,p), Y,
                mm(low.T*g[s][4][None,:],Y,p), Y]
        for t,(A,B) in enumerate(zip(lefts,rights)):
            J[:,(s*5+t)*n:(s*5+t+1)*n]=np.einsum('ui,iv->uvi',A,B,optimize=False).reshape(len(rows)*len(cols),n)%p
    return J
def rank(A,p):
    path=ROOT/'temporary_matrix.bin'; np.asarray(A,dtype='<u4').tofile(path)
    ans=json.loads(subprocess.check_output([str(ROOT/'modular_elimination'),str(path),str(A.shape[0]),str(A.shape[1]),str(p)],text=True))
    path.unlink()
    return ans
def py_det(A,p):
    A=A.copy()%p; d=1
    for j in range(len(A)):
        nonzero=np.flatnonzero(A[j:,j])
        if not len(nonzero): return 0
        k=j+int(nonzero[0])
        if j!=k: A[[j,k]]=A[[k,j]]; d=-d
        pivot=int(A[j,j]); d=d*pivot%p
        w=A[j+1:,j]*pow(pivot,-1,p)%p
        A[j+1:,j+1:]=(A[j+1:,j+1:]-w[:,None]*A[j,j+1:])%p
    return int(d)
def output(g,P,p,rows,cols): return compose(factors(g,P,p),p)[np.ix_(rows,cols)]
def fd_test(g,P,p,J,rows,cols,indices):
    n=len(g[0][0]); base=output(g,P,p,rows,cols)
    for idx in indices:
        k,t,i=idx//(5*n),(idx//n)%5,idx%n
        cp=g.copy(); cp[k,t,i]=(cp[k,t,i]+1)%p
        difference=(output(cp,P,p,rows,cols)-base)%p
        assert np.array_equal(difference.ravel(),J[:,idx]),(p,idx)
    return len(indices)

def main():
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'modular_elimination.cpp'),'-o',str(ROOT/'modular_elimination')],check=True)
    cfg=read('AFFINE_LAYOUT.json'); P=[]; indices=[]
    for col in cfg['affine_shuffle_columns']:
        mat,idx=perm(col); P.append(mat); indices.append(idx)
    (ROOT/'EXPLICIT_PERMUTATIONS.json').write_text(json.dumps(indices,indent=2)+'\n')
    g=np.array([[row[n] for n in NAMES] for row in read('GENERATOR_POINT_1.json')],dtype=np.int64)
    g2=np.array([[row[n] for n in NAMES] for row in read('GENERATOR_POINT_2.json')],dtype=np.int64)
    assert g.shape==g2.shape==(4,5,N)
    cert=read('witness28.json'); selected=cert['pivots_784']; tp=read('two_point_minor_indices.json')
    assert cert['minor_output_rows']==cert['minor_input_cols']==list(range(28))
    assert len(selected)==len(set(selected))==784 and min(selected)>=0 and max(selected)<5120
    assert len(tp['J1_parameter_indices'])==906 and len(tp['J2_parameter_indices'])==118
    for a in [tp['J1_parameter_indices'],tp['J2_parameter_indices']]:
        assert len(a)==len(set(a)) and min(a)>=0 and max(a)<5120
    emit('input_validation',{'integer_parameter_shape':list(g.shape),'point1_range':[int(g.min()),int(g.max())],'all_three_permutations_bijective':True,'toffoli_sequence_used':False,'witness_rows_cols_zero_based':list(range(28)),'parameter_order':'stage-major; d,a,b,c,e; index 0..255','unused_parameter_indices':[k*1280+t*256+i for k in range(4) for t,i in [(1,0),(2,255),(3,255),(4,0)]]})
    # Independent exact small-model all-column derivative control.
    small=np.arange(1,81,dtype=np.int64).reshape(4,5,4)
    smallP=[np.eye(4,dtype=np.int64)[v] for v in ([2,0,3,1],[3,2,1,0],[1,3,0,2])]
    sj=differential(small,smallP,101,list(range(4)),list(range(4)))
    fd_test(small,smallP,101,sj,list(range(4)),list(range(4)),range(80))
    assert rank(sj,101)['rank']==16
    # Test both implementations on nonsingular and singular matrices.
    ctrl=np.array([[0,2,3],[4,5,6],[7,8,10]],dtype=np.int64)
    for p in [101,12289,65537]:
        assert prime(p)
        assert rank(ctrl,p)['determinant']==py_det(ctrl,p)==p-5
        bad=ctrl.copy();bad[1]=bad[0]
        assert rank(bad,p)['rank']==2 and rank(bad,p)['determinant']==0
    emit('small_controls',{'all_80_parameter_derivatives_exact':True,'jacobian_rank':16,'determinant_controls':True})
    for p in [12289,65537]:
        J=differential(g,P,p,list(range(32)),list(range(32)))
        positions=[i*32+j for i in range(28) for j in range(28)]
        minor=J[np.ix_(positions,selected)]
        r=rank(minor,p); dp=py_det(minor,p)
        assert r['rank']==784 and r['determinant']==dp==cert['determinants_784_by_field'][str(p)]
        probes=[k*1280+t*256+((31*k+47*t+19)%256) for k in range(4) for t in range(5)]
        probes += RESULT['input_validation']['unused_parameter_indices']
        fd_test(g,P,p,J,list(range(32)),list(range(32)),probes)
        emit('minor_'+str(p),{'rank':r['rank'],'determinant':r['determinant'],'second_python_determinant':dp,'matrix_sha256_uint32le':sha(minor),'finite_difference_columns':probes})
        lr=rank(J,p)
        assert lr['rank']==906
        emit('leading32_'+str(p),{'pointwise_modular_rank':lr['rank'],'matrix_sha256_uint32le':sha(J),'pivot_parameter_indices':lr['pivots']})
        sd=[rank(stage(st,p),p)['determinant'] for st in g]
        assert all(sd)
        emit('stage_invertibility_'+str(p),{'four_stage_determinants':sd,'all_nonzero':True,'leading32_output_rank':rank(output(g,P,p,list(range(32)),list(range(32))),p)['rank']})
        if p==12289:
            K=compose([P[0],stage(g[1],p),P[1],stage(g[2],p),P[2]],p)
            assert np.count_nonzero(K[:32,:32])==1024
            base=output(g,P,p,list(range(32)),list(range(32)))
            probes2=[(0,0),(0,31),(31,0),(31,31),(11,23),(21,7)]
            for i,j in probes2:
                a=g.copy();b=g.copy();ab=g.copy()
                a[3,0,i]+=1;b[0,0,j]+=1;ab[3,0,i]+=1;ab[0,0,j]+=1
                diff=(output(ab,P,p,list(range(32)),list(range(32)))-output(a,P,p,list(range(32)),list(range(32)))-output(b,P,p,list(range(32)),list(range(32)))+base)%p
                expected=np.zeros((32,32),dtype=np.int64);expected[i,j]=K[i,j]
                assert np.array_equal(diff,expected)
            curvature=np.zeros((1024,1),dtype=np.int64);curvature[0,0]=K[0,0]
            cr=rank(np.column_stack([J[:,lr['pivots']],curvature]),p)
            assert cr['rank']==907
            emit('second_order',{'all_1024_K_entries_nonzero':True,'K00':int(K[0,0]),'K32_sha256_uint32le':sha(K[:32,:32]),'mixed_finite_difference_probes':probes2,'tangent_plus_K00E00_rank':cr['rank']})
            J2=differential(g2,P,p,list(range(32)),list(range(32)))
            B=np.column_stack([J[:,tp['J1_parameter_indices']],J2[:,tp['J2_parameter_indices']]])
            br=rank(B,p); assert br['rank']==1024 and br['determinant']==4142
            emit('two_point_tangent_span',{'rank':br['rank'],'determinant':br['determinant'],'matrix_sha256_uint32le':sha(B),'point2_modular_rank':rank(J2,p)['rank']})
            dup=minor.copy();dup[:,1]=dup[:,0]
            dr=rank(dup,p);assert dr['rank']==783 and dr['determinant']==0
            z=np.zeros_like(g); zj=differential(z,P,p,list(range(32)),list(range(32)))
            assert not np.any(zj)
            emit('negative_controls',{'duplicate_minor_column_rank':dr['rank'],'duplicate_minor_column_determinant':dr['determinant'],'zero_stages_jacobian_is_zero':True})
    RESULT['status']='ALL_INDEPENDENT_CHECKS_PASSED'
    RESULT['runtime']={'python':platform.python_version(),'numpy':np.__version__,'int64_safety_bound_256_times_65536_squared':256*65536**2}
    save();print(RESULT['status'],flush=True)

if __name__=='__main__': main()
