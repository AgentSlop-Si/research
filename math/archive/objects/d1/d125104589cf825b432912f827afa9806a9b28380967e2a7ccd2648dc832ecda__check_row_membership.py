#!/usr/bin/env python3
"""Fresh exact controls for rank strata and the Fourier paired-row reduction."""
from pathlib import Path
import sys,json,random
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'seed_compatibility_gate'))
from check_n16_outer_gate import PRIME as P,green,multiply,pivots,LABELS
from check_lift_defects import cover_and_splice
from check_hierarchical_lift import lift
def rank(a):return len(pivots(a))
def solve_row(t,b):
    # Solve transpose(t)c=b, preserving every rank stratum and free variable.
    mat=[list(col)+[x] for col,x in zip(zip(*t),b)];r=0;cols=[]
    for c in range(len(t)):
        pivot=next((i for i in range(r,len(mat)) if mat[i][c]),None)
        if pivot is None:continue
        mat[r],mat[pivot]=mat[pivot],mat[r]
        inv=pow(mat[r][c],-1,P);mat[r]=[x*inv%P for x in mat[r]]
        for i in range(len(mat)):
            if i!=r:
                f=mat[i][c];mat[i]=[(x-f*y)%P for x,y in zip(mat[i],mat[r])]
        cols.append(c);r+=1
    if any(not any(row[:-1]) and row[-1] for row in mat):return None
    particular=[0]*len(t)
    for row,c in enumerate(cols):particular[c]=mat[row][-1]
    null=[]
    for c in range(len(t)):
        if c in cols:continue
        v=[0]*len(t);v[c]=1
        for row,pivot in enumerate(cols):v[pivot]=-mat[row][c]%P
        null.append(v)
    full_support_possible=all(particular[j] or any(v[j] for v in null) for j in range(len(t)))
    return particular,null,full_support_possible
def strata():
    results=[]
    for r in range(9):
        t=[[int(i==j and i<r) for j in range(64)] for i in range(8)]
        b=[int(j<r) for j in range(64)]
        solution=solve_row(t,b);assert solution is not None and solution[2]
        bad=b[:];bad[63]=1;assert solve_row(t,bad) is None
        assert rank(t)==r and rank(t+[bad])==r+1
        if r>=2:
            forced=b[:];forced[0]=0;assert solve_row(t,forced) is not None and not solve_row(t,forced)[2]
        results.append({'rank':r,'membership_positive':True,'nonmembership_negative':True,'nonzero_guards_checked':True})
    return results
def paired_synthetic():
    out=[]
    for i in range(32):
        excluded={i,i+32};other=[j for j in range(64) if j not in excluded]
        rows=[]
        for j in other[:6]+[i,i+32]:rows.append([int(k==j) for k in range(64)])
        # An invertible 8-by-8 Vandermonde mix avoids privileging coordinate rows.
        mix=[[pow(r+1,c,P) for c in range(8)] for r in range(8)]
        t=multiply(mix,rows);w=[[row[k] for k in other] for row in t]
        assert rank(t)==8 and rank(w)==6
        assert all(solve_row(t,[int(k==j) for k in range(64)]) is not None for j in excluded)
        broken=[row[:] for row in rows];broken[6][other[6]]=1
        tt=multiply(mix,broken);ww=[[row[k] for k in other] for row in tt]
        assert rank(tt)==8 and rank(ww)==7
        assert solve_row(tt,[int(k==i) for k in range(64)]) is None
        out.append({'row_pair':[i,i+32],'positive_wrong_rank':6,'negative_wrong_rank':7})
    return out
def real_route_identities():
    gs=[]
    for j,label in enumerate(LABELS):
        t,p,_=cover_and_splice(4,4,label);_,pl,_=lift(t,p,4,4,label);gs.append(green(pl,j+2))
    u=pow(3,(P-1)//64,P);inv64=pow(64,-1,P)
    fi=[[inv64*pow(u,(-i*j)%64,P)%P for j in range(64)] for i in range(64)]
    bank=[[0]*64 for _ in range(64)]
    for block in range(8):
        for i in range(8):
            for j in range(8):bank[8*block+i][8*block+j]=pow(u,8*i*j,P) if block in [0,1,4,5] else int(i==j)
    k=multiply(gs[0],bank);r=multiply(bank,gs[1]);rng=random.Random(171616)
    recs=[]
    for sign in (1,-1):
        coefficients=[[rng.randrange(1,P) for j in range(8)] for i in range(32)]
        coefficients += [[sign*x%P for x in row] for row in coefficients]
        l=[[sum(coefficients[i][j]*gs[j][i][c] for j in range(8))%P for c in range(64)] for i in range(64)]
        assert rank(l)==64
        for branch in ('input','middle'):
            u0=multiply(multiply(k,l),fi) if branch=='input' else multiply(multiply(l,r),fi)
            transported=[multiply(g,u0) for g in gs]
            for i in range(32):
                for j in range(8):
                    for c in range(64):assert transported[j][i+32][c]==sign*((-1)**c)*transported[j][i][c]%P
            recs.append({'branch':branch,'signed_symmetry':sign,'entrywise_pair_checks':32*8*64,
                         'inner_rank':64,'fixed_factors':'independent commuting controls, not the algebraic seed'})
    return recs
def main():
    result={'status':'PASS','rank_strata':strata(),'paired_rank_controls':paired_synthetic(),
            'actual_route_identity_controls':real_route_identities(),
            'scope':'Algebraic identities and guards only; no N64 coefficient solution or nonexistence claim.'}
    (HERE/'ROW_MEMBERSHIP_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','rank_strata':9,'paired_positive_negative_cases':32,'route_cases':4}))
if __name__=='__main__':main()
