"""Numerical sanity checks for the *known* unitary 2x2 FFT entropy barrier.

This is NOT a proof of a new lower bound. The exact mathematical argument is
in THEOREM.md and is originally due to Ailon (2013). Normalized complex
DFT here, unlike the modular-field Good-Thomas implementation.
"""
import math,cmath


def row_entropy(matrix):
    total=0.0
    for row in matrix:
        for z in row:
            u=abs(z)**2
            if u>1e-28:total-=u*math.log2(u)
    return total


def entropy_trajectory(n):
    if n<2 or n&(n-1):raise ValueError('power of two >=2')
    matrix=[[complex(i==j) for j in range(n)] for i in range(n)]
    levels=[row_entropy(matrix)]
    count=0; size=n
    while size>1:
        h=size//2
        for start in range(0,n,size):
            for j in range(h):
                r,s=start+j,start+h+j
                u,v=matrix[r][:],matrix[s][:]
                phase=cmath.exp(-2j*math.pi*j/size)/math.sqrt(2)
                invsq=1/math.sqrt(2)
                matrix[r]=[(a+b)*invsq for a,b in zip(u,v)]
                matrix[s]=[(a-b)*phase for a,b in zip(u,v)]
                count+=1
        levels.append(row_entropy(matrix))
        size=h
    return {'N':n,'entropies':levels,'gate_count':count,
            'known_unitary_lower_bound':n*(n.bit_length()-1)//2,
            'final_entropy_target':n*math.log2(n),
            'max_column_l2_deviation':max(abs(sum(abs(matrix[i][j])**2 for i in range(n))-1) for j in range(n))}
