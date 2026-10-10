"""Independent Phase32 reconstruction, exact online controls, and metadata audit.
No uploaded program is executed. Uses an independent triangular solver and
recursive radix-two Fourier reference.
"""
from pathlib import Path
import random,json,hashlib,itertools
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'phase32/fft_green_phase32_constructive'
P=998244353
def solve(A,B):
    n=len(A);r=len(B[0]);M=[row.copy()+rhs.copy()for row,rhs in zip(A,B)]
    for j in range(n):
        k=next((i for i in range(j,n)if M[i][j]),None)
        if k is None:raise ValueError('singular')
        M[j],M[k]=M[k],M[j]
        inv=pow(M[j][j],-1,P)
        for i in range(j+1,n):
            q=M[i][j]*inv%P
            for h in range(j,n+r):M[i][h]=(M[i][h]-q*M[j][h])%P
    X=[[0]*r for i in range(n)]
    for i in range(n-1,-1,-1):
        inv=pow(M[i][i],-1,P)
        for h in range(r):X[i][h]=(M[i][n+h]-sum(M[i][j]*X[j][h]for j in range(i+1,n)))*inv%P
    return X
def rank(M):
    M=[[v%P for v in row]for row in M];r=0
    for j in range(len(M[0])):
        i=next((i for i in range(r,len(M))if M[i][j]),None)
        if i is None:continue
        M[r],M[i]=M[i],M[r];inv=pow(M[r][j],-1,P)
        for i in range(r+1,len(M)):
            q=M[i][j]*inv%P
            M[i][j:]=[(x-q*y)%P for x,y in zip(M[i][j:],M[r][j:])]
        r+=1
        if r==len(M):break
    return r
def fourier(x,w):
    if len(x)==1:return x.copy()
    a=fourier(x[::2],w*w%P);b=fourier(x[1::2],w*w%P);m=len(a);phase=1;out=[0]*(2*m)
    for j in range(m):
        z=phase*b[j]%P;out[j]=(a[j]+z)%P;out[j+m]=(a[j]-z)%P;phase=phase*w%P
    return out
def greensolve(cycle,alpha,x):
    n=len(x);h=x[cycle[1]]
    for j in range(2,n):h=(x[cycle[j]]+alpha*h)%P
    y=[0]*n;y[cycle[0]]=(x[cycle[0]]+alpha*h)*pow(1-pow(alpha,n,P),-1,P)%P
    for j in range(1,n):y[cycle[j]]=(x[cycle[j]]+alpha*y[cycle[j-1]])%P
    return y

class Model:
    def __init__(self,n,k,extra=0,seed=320031):
        self.n=n;self.k=k;self.q=k+extra;self.z=pow(3,(P-1)//n,P)
        rng=random.Random(seed+17*n+k);self.cycles=[];succs=[]
        for j in range(self.q):
            while True:
                cyc=list(range(n));rng.shuffle(cyc);nxt=[0]*n
                for a,b in zip(cyc,cyc[1:]+cyc[:1]):nxt[a]=b
                slope=(nxt[1]-nxt[0])%n;affine=all(nxt[x]==(slope*x+nxt[0])%n for x in range(n))
                if affine or nxt in succs or any(all(nxt[v[x]]==v[nxt[x]]for x in range(n))for v in succs):continue
                break
            succs.append(nxt);self.cycles.append(cyc)
        self.positions=[]
        for cyc in self.cycles:
            pos=[0]*n
            for j,x in enumerate(cyc):pos[x]=j
            self.positions.append(pos)
        for attempt in range(50):
            self.alpha=[];self.values=[]
            for j in range(self.q):
                while True:
                    a=rng.randrange(2,P-1)
                    if pow(a,n,P)!=1:break
                self.alpha.append(a);den=pow(1-pow(a,n,P),-1,P);powers=[den]
                for j in range(1,n):powers.append(powers[-1]*a%P)
                self.values.append(powers)
            self.gates=[[0]*n for j in range(self.q)]
            try:
                for i in range(n):
                    response=[[self.green(s,i,j)for s in range(self.q)]for j in range(k)]
                    rhs=[pow(self.z,-i*j%n,P)for j in range(k)]
                    B=[[rhs[j],-response[j][k]%P if extra else 0]for j in range(k)]
                    sol=solve([row[:k]for row in response],B)
                    if extra:
                        if any(z[1]==0 for z in sol):raise ValueError('zero null direction')
                        vals=None
                        for tau in range(1,k+5):
                            trial=[(z[0]+tau*z[1])%P for z in sol]+[tau]
                            if all(trial):vals=trial;break
                        if vals is None:raise ValueError('zero gate')
                    else:vals=[z[0]for z in sol]
                    if not all(vals):raise ValueError('zero gate')
                    assert all(sum(response[j][s]*vals[s]for s in range(self.q))%P==rhs[j]for j in range(k))
                    for s in range(self.q):self.gates[s][i]=vals[s]
                self.resamples=attempt;break
            except ValueError:continue
        else:raise AssertionError('no parameter found')
    def green(self,s,i,j):return self.values[s][(self.positions[s][i]-self.positions[s][j])%self.n]
    def entry(self,i,j):return sum(self.gates[s][i]*self.green(s,i,j)for s in range(self.q))%P
    def exact(self,i,j):return pow(self.z,-i*j%self.n,P)
    def apply(self,x):
        out=[0]*self.n
        for cyc,a,gate in zip(self.cycles,self.alpha,self.gates):
            v=greensolve(cyc,a,x)
            out=[(z+g*w)%P for z,g,w in zip(out,gate,v)]
        return out
    def fingerprint(self):
        h=hashlib.sha256()
        for cyc,a in zip(self.cycles,self.alpha):h.update(str((cyc,a)).encode())
        for gate in self.gates:h.update(str(gate).encode())
        return h.hexdigest()

results=[];bugs=[];residuals=[]
for filename in ['audit.json','audit_large.json','audit_extra.json','audit_seven.json']:
    for old in json.loads((SRC/filename).read_text()):
        n=old['N'];k=len(old['interpolated_columns']);extra=old['greens']-k;M=Model(n,k,extra)
        assert M.fingerprint()==old['fingerprint_sha256'] and M.resamples==old['parameter_resamples']
        for j in range(k):
            got=M.apply([int(i==j)for i in range(n)]);assert got==[M.exact(i,j)for i in range(n)]
        actual_column=k;got=M.apply([int(i==k)for i in range(n)]);column_errors=sum(x!=M.exact(i,k)for i,x in enumerate(got))
        rng=random.Random(9000+n+k);x=[rng.randrange(P)for i in range(n)];y=M.apply(x)
        dense_errors=sum(a!=b for a,b in zip(y,fourier(x,pow(M.z,-1,P))))
        phase=[pow(M.z,-i%n,P)for i in range(n)]
        shift_errors=sum(a!=b*p%P for a,b,p in zip(M.apply(x[-1:]+x[:-1]),y,phase))
        second_errors=sum(a!=b for a,b in zip(M.apply([x[i]*phase[i]%P for i in range(n)]),y[1:]+y[:1]))
        assert column_errors==dense_errors==n and shift_errors>0 and second_errors>0
        assert column_errors==old['out_of_sample_column_mismatches']and dense_errors==old['dense_input_mismatches']and shift_errors==old['Weyl_shift_defect_nonzeros']
        if old['out_of_sample_basis_column']!=actual_column:
            assert old['out_of_sample_basis_column']==M.cycles[-1][-1]
            bugs.append({'source_file':filename,'N':n,'fitted_columns':list(range(k)),'reported_probe_column':old['out_of_sample_basis_column'],'actual_probe_column':actual_column,'cause':'Source loop reuses j while checking cycle successors.'})
        if k==5 and extra==0 and n<=64:
            residual=[[M.entry(i,j)-M.exact(i,j)for j in range(k,n)]for i in range(n)]
            rk=rank(residual);assert rk==n-k
            residuals.append({'N':n,'rank':rk,'expected':n-k})
            assert all(rank([[M.green(s,i,j)for j in range(6)]for s in range(5)]+[[M.exact(i,j)for j in range(6)]])==6 for i in range(n))
        results.append({'source_file':filename,'N':n,'q':M.q,'fitted_columns':k,'fingerprint_match':True,'actual_probe_column':actual_column,'probe_errors':column_errors,'dense_errors':dense_errors,'first_weyl_errors':shift_errors,'second_weyl_errors':second_errors})
        print('Verified',filename,n,'q',M.q,'true missing column',actual_column,flush=True)

full=[]
for n in [8,16]:
    M=Model(n,n)
    assert all(M.entry(i,j)==M.exact(i,j)for i in range(n)for j in range(n))
    x=list(range(n));assert M.apply(x)==fourier(x,pow(M.z,-1,P))
    full.append({'N':n,'q':n,'all_entries_exact':True,'online_cost':'O(N^2)','naive_setup_cost':'O(N^4)'})

M=Model(8,3,seed=423);monomials=[]
for i in range(8):
    exps=[tuple((M.positions[s][i]-M.positions[s][assign[s]])%8 for s in range(3))for assign in itertools.permutations(range(3))]
    assert len(set(exps))==6
    for omit in range(3):assert len({tuple(e[s]for s in range(3)if s!=omit)for e in exps})==6
    augmented={tuple((M.positions[s][i]-M.positions[s][assign[s]])%8 for s in range(3))for assign in itertools.permutations(range(4),3)}
    assert len(augmented)==24

rng=random.Random(6232);sparse_tests=0
for n in [4,8,16]:
    for trial in range(3):
        cyc=list(range(n));rng.shuffle(cyc);a=rng.randint(2,1000);A=[[int(i==j)for j in range(n)]for i in range(n)]
        for before,after in zip(cyc,cyc[1:]+cyc[:1]):A[after][before]=(A[after][before]-a)%P
        x=[rng.randrange(P)for i in range(n)];sol=solve(A,[[v]for v in x]);assert [z[0]for z in sol]==greensolve(cyc,a,x);sparse_tests+=1
out={'passed':True,'uploaded_code_executed':False,'seeded_cases':results,'reporting_bugs':bugs,'residual_ranks':residuals,'full_q_equals_N_controls':full,'monomial_uniqueness_rows_checked':8,'independent_sparse_gaussian_controls':sparse_tests,'scope':'Exact finite-field partial-column constructions; no full Fourier identity for q<N is claimed.'}
(ROOT/'PHASE32_INDEPENDENT_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print('Phase32 complete; reporting-only index bugs:',len(bugs),flush=True)
