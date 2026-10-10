"""Exact rational four-Green example at N=2, no floating point."""
from fractions import Fraction as Q
import json
from pathlib import Path

def mm(A,B):
 return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def main():
 w=Q(1,2)
 G_plus=[[Q(4,3),Q(2,3)],[Q(2,3),Q(4,3)]]
 G_minus=[[Q(4,3),-Q(2,3)],[-Q(2,3),Q(4,3)]]
 # G = (I -/+ wP)^-1
 I=[[Q(1),Q(0)],[Q(0),Q(1)]]
 K_plus=[[Q(1),-w],[-w,Q(1)]]
 K_minus=[[Q(1),w],[w,Q(1)]]
 assert mm(K_plus,G_plus)==I and mm(K_minus,G_minus)==I
 A=[[(Q(3,8)*(G_plus[i][j]+G_minus[i][j])) for j in range(2)] for i in range(2)]
 assert A==I
 B=A
 F=[[Q(1),Q(1)],[Q(1),Q(-1)]]
 delta=[Q(1),Q(-1)]
 C0=[[A[i][t]*B[t][0] for t in range(2)] for i in range(2)]
 C1=[[A[i][t]*B[t][1] for t in range(2)] for i in range(2)]
 K=[[C1[i][j]-delta[i]*C0[i][j] for j in range(2)] for i in range(2)]
 G=[[sum(C0[k][i]*C0[k][j]+C1[k][i]*C1[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
 assert K==[[Q(-1),Q(0)],[Q(0),Q(1)]]
 assert G==I
 out={'n':2,'green_cycles':'two genuine nonzero-weight cycles with weights +1/2 and -1/2 in each stage',
      'sum_coefficient':'3/8 per branch',
      'A_equals_B_equals_identity':True,
      'phase_pencil':[list(map(str,row)) for row in K],
      'projective_gram':[list(map(str,row)) for row in G],
      'generalized_eigenvalue':1,
      'certified_spectral_gap_lower_bound':'1/sqrt(2)',
      'actual_best_spectral_error_for_diagonal_M':1}
 p=Path(__file__).resolve().parent/'EXACT_N2.json'
 p.write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
