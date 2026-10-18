#!/usr/bin/env python3
"""Fresh exact verifier; no historical program or numerical solver is imported.
Arithmetic is Q[z]/(z^4+1), z=exp(-2*pi*i/8).
"""
from fractions import Fraction as Q
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
Z=(Q(0),)*4; ONE=(Q(1),Q(0),Q(0),Q(0))
def elt(x):return (Q(x),Q(0),Q(0),Q(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 c=[Q(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   k=i+j;c[k%4]+=x*y*(-1 if k>=4 else 1)
 return tuple(c)
def root(k):
 k%=8;c=[Q(0)]*4;c[k%4]=Q(-1 if k>=4 else 1);return tuple(c)
def conj(a):
 c=Z
 for k,v in enumerate(a):c=add(c,mul(elt(v),root(-k)))
 return c
def inv(a):
 assert a!=Z
 # Solve the rational multiplication matrix for a*b=1.
 cols=[mul(a,root(k)) for k in range(4)]
 t=[[cols[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
 for j in range(4):
  p=next(i for i in range(j,4) if t[i][j]);t[j],t[p]=t[p],t[j]
  v=t[j][j];t[j]=[v2/v for v2 in t[j]]
  for i in range(4):
   if i!=j:
    v=t[i][j];t[i]=[u-v*w for u,w in zip(t[i],t[j])]
 b=tuple(t[i][4] for i in range(4));assert mul(a,b)==ONE;return b
def mm(A,B):
 return [[sumf(mul(a,b) for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sumf(it):
 s=Z
 for a in it:s=add(s,a)
 return s
def adj(A):return [[conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def eye(n,a=1):return [[elt(a if i==j else 0) for j in range(n)] for i in range(n)]
def mi(A):
 n=len(A); T=[list(r)+eye(n)[i] for i,r in enumerate(A)]
 for j in range(n):
  p=next(i for i in range(j,n) if T[i][j]!=Z);T[j],T[p]=T[p],T[j]
  a=inv(T[j][j]);T[j]=[mul(a,v) for v in T[j]]
  for i in range(n):
   if i!=j:
    a=T[i][j];T[i]=[sub(u,mul(a,v)) for u,v in zip(T[i],T[j])]
 B=[r[n:] for r in T];assert mm(A,B)==eye(n) and mm(B,A)==eye(n);return B
R=[
 [0,0,1,1,0,0,1,1],
 [0,1,0,1,0,1,0,1],
 [1,1,0,0,1,1,0,0],
 [1,0,1,0,1,0,1,0],
 [0,0,1,1,0,0,1,1],
 [1,0,1,0,1,0,1,0],
 [1,1,0,0,1,1,0,0],
 [0,1,0,1,0,1,0,1]]
assert all(set(r)<={0,1} and sum(r)==4 for r in R)
assert all(sum(c)==4 for c in zip(*R))
H=[[root(i*j) for j in range(8)] for i in range(8)]
D=[[H[i][j] if R[i][j] else Z for j in range(8)] for i in range(8)]
assert mm(adj(D),D)==eye(8,4) and mm(D,adj(D))==eye(8,4)
# Independent exponent histogram rule for every ordered Gram entry in both orders:
# a0+a1*z+...+a7*z^7 reduces to (a0-a4,...,a3-a7).
histograms={}
for order in ('columns','rows'):
 allh=[]
 for i in range(8):
  for j in range(8):
   h=[0]*8
   for k in range(8):
    included=R[k][i]*R[k][j] if order=='columns' else R[i][k]*R[j][k]
    if included:h[(k*(j-i))%8]+=1
   rem=[h[t]-h[t+4] for t in range(4)]
   assert rem==[4 if i==j else 0,0,0,0]
   allh.append({'i':i,'j':j,'histogram':h,'remainder':rem})
 histograms[order]=allh
# Graph traversal of all 16 vertices; a d-by-d block decomposition is impossible.
seen={0};todo=[0]
while todo:
 v=todo.pop()
 nbr=[8+j for j in range(8) if R[v][j]] if v<8 else [i for i in range(8) if R[i][v-8]]
 for w in nbr:
  if w not in seen:seen.add(w);todo.append(w)
assert len(seen)==16
cols=[{i for i in range(8) if R[i][j]} for j in range(8)]
assert len(cols[0]&cols[1])==2 and cols[0]!=cols[1]
# Full original simultaneous-inverse-row witness, unnormalized by sqrt(8).
A=[[sub(H[i][j],D[i][j]) for j in range(8)] for i in range(8)]
M=[[mul(elt(4),v) for v in row] for row in mi(adj(A))]
B=[[mul(elt(Q(1,4)),v) for v in row] for row in adj(A)]
assert mm(M,B)==eye(8) and mm(B,M)==eye(8)
assert all(sum(v!=Z for v in row)==4 for row in B)
assert all(sum(v!=Z for v in col)==4 for col in zip(*B))
E=[[sub(M[i][j],H[i][j]) for j in range(8)] for i in range(8)]
assert mm(E,adj(E))==eye(8,4) and mm(adj(E),E)==eye(8,4)
# A count-preserving 2-by-2 support switch is a rejected negative control.
Rp=[r[:] for r in R]
for i,j in ((0,0),(0,2),(2,0),(2,2)):Rp[i][j]=1-Rp[i][j]
assert all(sum(r)==4 for r in Rp) and all(sum(c)==4 for c in zip(*Rp))
Dp=[[H[i][j] if Rp[i][j] else Z for j in range(8)] for i in range(8)]
assert mm(adj(Dp),Dp)!=eye(8,4)
# CRT transcription controls for the infinite family, no numerical roots used.
# r = a mod 8, b mod m; c = e mod 8, f mod m. Pairing is
# rc/(8m) = inv(m mod 8)*a*e/8 + inv(8 mod m)*b*f/m mod 1.
crt_cases=[]
for m in (1,3,5,7,9,11,15):
 n=8*m
 if m==1:crt_cases.append({'m':m,'entries':64,'passed':True});continue
 u=pow(m,-1,8);v=pow(8,-1,m)
 for r in range(n):
  for c in range(n):
   a,b=r%8,r%m;e,f=c%8,c%m
   assert (r*c-m*u*a*e-8*v*b*f)%n==0
 # Mask R8[u*a mod 8,e] times the full m Fourier matrix.
 # This absorbs the unit multiplier and gives exact tensor Gram 4*m I.
 rowsums=[sum(R[(u*(r%8))%8][c%8] for c in range(n)) for r in range(n)]
 colsums=[sum(R[(u*(r%8))%8][c%8] for r in range(n)) for c in range(n)]
 assert set(rowsums)==set(colsums)=={4*m}
 crt_cases.append({'m':m,'N':n,'d':4*m,'entries':n*n,'passed':True})
(ROOT/'GRAM_CERTIFICATE.json').write_text(json.dumps(histograms,indent=2)+'\n')
res={'status':'PASS','arithmetic':'Q[z]/(z^4+1), exact rational tuples',
 'binary_mask':R,'N':8,'d':4,'gram_entries_verified':128,
 'row_and_column_degree':4,'bipartite_vertices_reached':16,
 'full_block_decomposition_possible':False,
 'original_inverse_witness_verified':True,'inverse_row_and_column_support':4,
 'unnormalized_error_gram':'4 I_8','normalized_squared_error':'1/2',
 'negative_control_preserves_degrees_but_fails_Gram':True,
 'CRT_transcription_controls':crt_cases,
 'uniform_divisibility_conjecture':'UNRESOLVED; 4 divides 8; this is not a nondivisor counterexample'}
(ROOT/'RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print('PASS: 128 whole-Gram entries, original inverse witness, connected support, negative control, CRT transcription.')
