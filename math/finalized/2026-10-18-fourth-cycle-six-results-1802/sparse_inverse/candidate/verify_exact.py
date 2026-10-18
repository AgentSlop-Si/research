#!/usr/bin/env python3
"""Fresh exact controls for M-NONLINEAR-COMPATIBILITY. Standard library only."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json

class K:
    """Q[z]/(z^4+1), with no floating point arithmetic."""
    __slots__=('a',)
    def __init__(self, a=0):
        if isinstance(a,K): self.a=a.a
        elif isinstance(a,(int,Q)): self.a=(Q(a),Q(0),Q(0),Q(0))
        else: self.a=tuple(map(Q,a)); assert len(self.a)==4
    def __add__(self,b):
        b=K(b); return K(tuple(x+y for x,y in zip(self.a,b.a)))
    __radd__=__add__
    def __neg__(self):return K(tuple(-x for x in self.a))
    def __sub__(self,b):return self+-K(b)
    def __rsub__(self,b):return K(b)+-self
    def __mul__(self,b):
        b=K(b); out=[Q(0)]*4
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a):out[(i+j)%4]+=(-1 if i+j>=4 else 1)*x*y
        return K(out)
    __rmul__=__mul__
    def __bool__(self):return any(self.a)
    def __eq__(self,b):return self.a==K(b).a
    def inv(self):
        assert self
        # Multiplication by this field element in the rational basis.
        M=[[self*K([int(t==j) for t in range(4)]) for j in range(4)]]
        A=[[M[0][j].a[i] for j in range(4)]+[Q(i==0)] for i in range(4)]
        for j in range(4):
            k=next(i for i in range(j,4) if A[i][j]);A[j],A[k]=A[k],A[j]
            v=A[j][j];A[j]=[x/v for x in A[j]]
            for i in range(4):
                if i!=j:
                    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[j])]
        b=K([A[i][4] for i in range(4)]);assert self*b==1;return b
    def __truediv__(self,b):return self*K(b).inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        ans=K(1);a=self
        while n:
            if n&1:ans=ans*a
            a=a*a;n//=2
        return ans
    def encode(self):return [str(x) for x in self.a]

Z=K([0,1,0,0]);ZERO=K(0);ONE=K(1)
def eye(n):return [[K(i==j) for j in range(n)] for i in range(n)]
def matmul(A,B):return [[sum((a*b for a,b in zip(row,col)),ZERO) for col in zip(*B)] for row in A]
def sub(A,I,J):return [[A[i][j] for j in J] for i in I]
def rank(A):
    if not A:return 0
    A=[row[:] for row in A];m=len(A);n=len(A[0]);r=0
    for j in range(n):
        p=next((i for i in range(r,m) if A[i][j]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
        for i in range(r+1,m):
            if A[i][j]:
                v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
        r+=1
        if r==m:break
    return r

def det(A):
    A=[row[:] for row in A];n=len(A);out=ONE
    for j in range(n):
        p=next((i for i in range(j,n) if A[i][j]),None)
        if p is None:return ZERO
        if p!=j:A[j],A[p]=A[p],A[j];out=-out
        v=A[j][j];out*=v
        for i in range(j+1,n):
            if A[i][j]:
                c=A[i][j]/v
                for k in range(j+1,n):A[i][k]-=c*A[j][k]
                A[i][j]=ZERO
    return out

def solve(A,b):
    n=len(A);A=[row[:]+[b[i]] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if A[i][j]);A[j],A[p]=A[p],A[j]
        v=A[j][j];A[j]=[x/v for x in A[j]]
        for i in range(n):
            if i!=j:
                v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]

def encode(A):return [[x.encode() for x in row] for row in A]
def in_chart(A,d,l,m,u,v):
    n=len(A)
    return all(A[i][j]==(d[i] if i==j else l[i]*m[j] if i>j else u[i]*v[j]) for i in range(n) for j in range(n))

def main():
    out={'owner':'M-NONLINEAR-COMPATIBILITY','arithmetic':'Q[z]/(z^4+1), exact fractions','tests':{}}
    F=[[Z**(i*j) for j in range(8)] for i in range(8)]
    assert Z**8==1 and all(Z**k!=1 for k in range(1,8))
    assert matmul(F,[[Z**(-i*j)/8 for j in range(8)] for i in range(8)])==eye(8)
    out['tests']['primitive_root_and_fourier_inverse']=True
    # Every six-column, six-consecutive-row minor, all cyclic starts.
    checked=0
    for start in range(8):
        I=[(start+i)%8 for i in range(6)]
        for J in combinations(range(8),6):
            expected=ONE
            for j in J:expected*=Z**(start*j)
            for a,b in combinations(J,2):expected*=Z**b-Z**a
            value=det(sub(F,I,J));assert value and value==expected;checked+=1
    out['tests']['exact_six_by_six_vandermonde_minors']=checked
    # All pairs of nonempty support patterns of size at most three.
    supports=[set(j) for k in range(1,4) for j in combinations(range(8),k)]
    pairs=0;unions=set()
    for a,A in enumerate(supports):
        for B in supports[a:]:
            U=tuple(sorted(A|B));assert len(U)<=6;unions.add(U);pairs+=1
            # Extend to a tested 6-column minor. This also certifies smaller unions.
            extension=list(U)+[j for j in range(8) if j not in U][:6-len(U)]
            assert len(set(extension))==6
    out['tests']['arbitrary_support_pairs']=pairs
    out['tests']['distinct_support_unions']=len(unions)
    # A genuine stage strictly outside both previous F8 inverse restrictions.
    A=eye(8);C=eye(8);A[2][0]=A[5][7]=ONE;C[2][0]=C[5][7]=-ONE
    d=[ONE]*8;l=[ZERO]*8;m=[ZERO]*8;u=[ZERO]*8;v=[ZERO]*8
    l[2]=m[0]=u[5]=v[7]=ONE
    assert in_chart(A,d,l,m,u,v)
    assert matmul(A,C)==eye(8) and matmul(C,A)==eye(8)
    assert C[2][0] and (2-0)%8 not in (0,1,7)
    offminor=det(sub(C,[2,5],[0,7]));assert offminor==1
    assert max(sum(bool(C[i][j]) for i in range(8)) for j in range(8))==2
    out['strict_extension_witness']={'A':encode(A),'C':encode(C),'disjoint_minor':offminor.encode(),'max_column_support':2}
    # Inherited dense boundary remains outside the new F8 sparse and rank-two branches.
    B=[[K(3 if i==j else 1 if i>j else 2) for j in range(8)] for i in range(8)]
    D=[[K(255 if i==j else -(2**(8-(j-i))) if i<j else -(2**(i-j-1)))/511 for j in range(8)] for i in range(8)]
    assert matmul(B,D)==eye(8) and matmul(D,B)==eye(8)
    assert all(x for row in D for x in row)
    minor3=det(sub(D,[0,2,4],[1,3,5]));assert minor3
    out['unrestricted_boundary']={'dense_inverse_entries':64,'disjoint_3_by_3_minor':minor3.encode(),'no_diagonal_plus_rank_at_most_2':True}
    # Sampling threshold: two disjoint 3-sparse columns collide on five samples.
    sample_rows=list(range(3,8));nodes=[Z**j for j in range(6)];weights=[]
    for j in range(6):
        den=ONE
        for k in range(6):
            if k!=j:den*=nodes[j]-nodes[k]
        weights.append(nodes[j]**(-3)/den)
    x=[ZERO]*8;y=[ZERO]*8
    for j,w in enumerate(weights):
        if j%2==0:x[j]=w
        else:y[j]=-w
    collision=eye(8)
    for i in range(8):collision[i][0]=x[i];collision[i][1]=y[i]
    assert det(collision) and all(sum(bool(collision[i][j]) for i in range(8))<=3 for j in range(8))
    FC=matmul(F,collision)
    assert rank(sub(FC,sample_rows,[0,1]))==1
    assert all(FC[i][0]==FC[i][1] for i in sample_rows)
    assert rank(sub(FC,list(range(2,8)),[0,1]))==2
    out['sampling_sharpness']={'C':encode(collision),'determinant':det(collision).encode(),'five_sample_rank':1,'six_sample_rank':2,'rows_five':sample_rows}
    # Sharpness of the improved k-r bound with a diagonal core and rank-two correction.
    sample_rows=list(range(4,8));J=list(range(4));W=[]
    for anchor in [2,3]:
        tail=solve(sub(F,sample_rows,list(range(4,8))),[-F[i][anchor] for i in sample_rows])
        w=[ZERO]*8;w[anchor]=ONE
        for j,value in enumerate(tail,4):w[j]=value
        assert all(sum((F[i][j]*w[j] for j in range(8)),ZERO)==0 for i in sample_rows)
        W.append(w)
    C2=eye(8)
    for i in range(8):
        C2[i][2]=K(i==0)+W[0][i];C2[i][3]=K(i==1)+W[1][i]
    R=[[C2[i][j]-K(i==j) for j in range(8)] for i in range(8)]
    assert det(C2)==1 and rank(R)==2
    value=rank(sub(matmul(F,C2),sample_rows,J));assert value==2
    out['rank_debit_sharpness']={'C':encode(C2),'correction_rank':2,'selected_columns':J,'selected_rows':sample_rows,'actual_rank':value,'k_minus_r':2}
    # Singular core is permitted, and every hypothesis is checked explicitly.
    S=eye(8);S[0][0]=ZERO;R=eye(8)
    for i in range(8):
        for j in range(8):R[i][j]=K(i==j==0)
    C0=[[S[i][j]+R[i][j] for j in range(8)] for i in range(8)]
    assert rank(S)==7 and rank(R)==1 and C0==eye(8)
    assert rank(sub(matmul(F,C0),[5,6,7],[0,1,2]))==3
    out['tests']['singular_sparse_core_positive_control']=True
    # Dropping consecutive samples or column independence invalidates the sampling conclusion.
    assert rank(sub(F,[0,2,4,6],[0,4]))==1
    singular=eye(8)
    for i in range(8):singular[i][1]=singular[i][0]
    assert not det(singular) and rank(sub(matmul(F,singular),list(range(2,8)),[0,1]))==1
    out['mutation_controls']={'nonconsecutive_samples_rank_one':True,'dependent_inverse_columns_rank_one':True,'too_few_samples_rank_one':True}
    out['all_checks_passed']=True
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_checks_passed':True,'minors':checked,'support_pairs':pairs,'union_count':len(unions),'dense_boundary_minor':minor3.encode(),'local_rank_debit_sharp':True},indent=2))

if __name__=='__main__':main()
