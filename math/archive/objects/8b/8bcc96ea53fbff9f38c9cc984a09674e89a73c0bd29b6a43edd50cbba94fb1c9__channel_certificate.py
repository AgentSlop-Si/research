# Independent exact cyclotomic certificate, no uploaded imports/execution.
from sympy import QQ
from pathlib import Path
import json
K=QQ.cyclotomic_field(8); z=K.unit; O=K.zero; E=K.one
r=[0,1,2,4,3,5,6,7];c=[0,1,4,5,2,3,6,7]
M=[[z**(i*j%8) for j in c] for i in r]
def solve(a,b,n=3,free=O):
    A=[list(x)+[y] for x,y in zip(a,b)]; piv=[];pos=0
    for col in range(n):
        q=next((q for q in range(pos,len(A)) if A[q][col]),None)
        if q is None:continue
        A[pos],A[q]=A[q],A[pos]
        v=A[pos][col];A[pos]=[v0/v for v0 in A[pos]]
        for j in range(len(A)):
            if j!=pos:
                v=A[j][col];A[j]=[a0-v*b0 for a0,b0 in zip(A[j],A[pos])]
        piv.append(col);pos+=1
    assert all(any(row[:n]) or not row[n] for row in A)
    x=[free]*n
    for j,col in enumerate(piv):x[col]=A[j][-1]-sum((A[j][k]*x[k] for k in range(n) if k not in piv),O)
    assert all(sum((u*v for u,v in zip(row,x)),O)==val for row,val in zip(a,b))
    return x
def lower(T):
    U=[[T[i][j] if j<i else E for j in range(3)] for i in range(8)]
    V=[[E if j==k else O for k in range(3)] for j in range(3)]
    for j in range(3,8):
        V.append(solve(U[j+1:],[T[i][j] for i in range(j+1,8)],free=E))
    assert all(sum((a*b for a,b in zip(U[i],V[j])),O)==T[i][j] for i in range(8) for j in range(i))
    # Constant invertible change of generator basis avoiding every zero output generator.
    for t in range(2,30):
        W=[[E,K.convert(t+i),K.convert((t+i)**2)] for i in range(3)]
        # U'=U W, V'=W^-1 V.
        Up=[[sum((U[i][k]*W[k][j] for k in range(3)),O) for j in range(3)] for i in range(8)]
        if all(all(row) for row in Up):
            Vp=[solve(W,v) for v in V]
            assert all(sum((a*b for a,b in zip(Up[i],Vp[j])),O)==T[i][j] for i in range(8) for j in range(i))
            return Up,Vp,t
    raise AssertionError('No small basis found')
U,V,t=lower(M)
# Strict upper is lower for J M J, where J reverses the order, then reverse generators.
T=[list(reversed(row)) for row in reversed(M)]
P,Q,s=lower(T);P=list(reversed(P));Q=list(reversed(Q))
assert all(sum((a*b for a,b in zip(P[i],Q[j])),O)==M[i][j] for i in range(8) for j in range(i+1,8))
# Convert output-weighted prefix/suffix to raw scalar scans with nonzero row generators.
f_a=[[O]+[U[i][k]/U[i-1][k] for i in range(1,8)] for k in range(3)]
f_b=[[U[i][k]*V[i][k] for i in range(8)] for k in range(3)]
b_a=[[P[i][k]/P[i+1][k] for i in range(7)]+[O] for k in range(3)]
b_b=[[P[i][k]*Q[i][k] for i in range(8)] for k in range(3)]
d=[M[i][i]-sum((f_b[k][i]+b_b[k][i] for k in range(3)),O) for i in range(8)]
for j in range(8):
    x=[E if i==j else O for i in range(8)]; y=[d[i]*x[i] for i in range(8)]
    for k in range(3):
        h=O
        for i in range(8):h=f_a[k][i]*h+f_b[k][i]*x[i];y[i]+=h
        h=O
        for i in reversed(range(8)):h=b_a[k][i]*h+b_b[k][i]*x[i];y[i]+=h
    assert y==[M[i][j] for i in range(8)]
def encode(x):
    if isinstance(x,list):return [encode(y) for y in x]
    return str(K.to_sympy(x))
report={'field':'Q[z]/(z^4+1), with z primitive eighth root','row_order':r,'col_order':c,'forward_a':encode(f_a),'forward_b':encode(f_b),'backward_a':encode(b_a),'backward_b':encode(b_b),'diagonal':encode(d),'change_of_basis_parameters':[t,s],'exact_basis_columns_passed':8,'certificate':'Three independent raw forward scans plus three raw backward scans plus diagonal; no output weights needed.'}
Path(__file__).with_name('channel_certificate.json').write_text(json.dumps(report,indent=2))
print('EXACT_F8_THREE_CHANNEL_CERTIFICATE_PASS', 'basis_columns=8', 'generator_basis_parameters', t,s)
