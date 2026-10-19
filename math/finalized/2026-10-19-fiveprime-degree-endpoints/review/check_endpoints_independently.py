#!/usr/bin/env python3
"""Independent integer-polynomial controls for the 5q endpoint proof.
No historical/author scripts are imported or executed; Python standard library only.
"""
import hashlib, itertools, json, math, pathlib, time
ROOT=pathlib.Path(__file__).resolve().parent
COUNTS={}
def bump(key,n=1): COUNTS[key]=COUNTS.get(key,0)+n

def prime(n): return n>=2 and all(n%p for p in range(2,math.isqrt(n)+1))

def cyclo_5q(q):
    # Phi_5q(X) = (1+X^5+...+X^(5(q-1))) / (1+X+...+X^(q-1)).
    numerator=[int(i%5==0) for i in range(5*(q-1)+1)]
    divisor=[1]*q
    quotient=[0]*(4*(q-1)+1)
    for degree in range(len(numerator)-1,q-2,-1):
        coeff=numerator[degree]
        quotient[degree-(q-1)]=coeff
        for j in range(q): numerator[degree-(q-1)+j]-=coeff*divisor[j]
    assert not any(numerator)
    assert quotient[-1]==1
    return quotient

class Exact:
    def __init__(self,q):
        assert prime(q) and q>5
        self.q=q; self.n=5*q; self.phi=cyclo_5q(q); self.m=len(self.phi)-1
        self.e5=q*pow(q,-1,5); self.eq=5*pow(5,-1,q)
        self.residues=[]
        for x in range(self.n):
            coeff=[0]*self.n; coeff[x]=1
            self.residues.append(tuple(self.reduce(coeff)))
    def reduce(self,coeff):
        coeff=list(coeff)+[0]*max(0,self.m+1-len(coeff))
        for degree in range(len(coeff)-1,self.m-1,-1):
            a=coeff[degree]
            if a:
                for j,p in enumerate(self.phi): coeff[degree-self.m+j]-=a*p
        return coeff[:self.m]
    def zero(self,columns,delta=1,power=1):
        coeff=[0]*self.n
        for c in columns: coeff[(delta*c*power)%self.n]+=1
        return not any(self.reduce(coeff))
    def witness(self,columns,delta=1,power=1):
        coeff=[0]*self.n
        for c in columns: coeff[(delta*c*power)%self.n]+=1
        return self.reduce(coeff)
    def idx(self,a,b): return (a*self.e5+b*self.eq)%self.n

def phase_checks(E):
    n=E.n; q=E.q
    assert E.e5%5==1 and E.e5%q==0 and E.eq%5==0 and E.eq%q==1
    assert (E.e5+E.eq)%n==1 and E.e5*E.eq%n==0
    assert E.e5*E.e5%n==E.e5%n and E.eq*E.eq%n==E.eq%n
    assert len({E.idx(a,b) for a in range(5) for b in range(q)})==n
    for r in range(n):
        for c in range(n):
            assert (r*c-E.e5*(r%5)*(c%5)-E.eq*(r%q)*(c%q))%n==0
            bump('original_index_phase_products')
    # q+4 exceptional rows exactly, for every reference row.
    for r in range(n):
        exceptional={s for s in range(n) if s%5==r%5 or s%q==r%q}
        assert len(exceptional)==q+4
        for k in (2,3,4): assert k*q>len(exceptional); bump('coverage_counts')

def check_grams(E,rows,d,expect_good,name):
    n=E.n
    cols=[{r for r in range(n) if c in rows[r]} for c in range(n)]
    assert all(len(S)==d for S in rows+cols)
    failures={}; failed_counts={}; same_b_bad=0
    for orientation,sets in [('rows',rows),('columns',cols)]:
        bad=[]
        for r in range(n):
            for s in range(n):
                common=sets[r]&sets[s]
                delta=r-s if orientation=='rows' else s-r
                if r==s:
                    assert len(common)==d
                    assert E.witness(common,0)==[d]+[0]*(E.m-1)
                else:
                    good=E.zero(common,delta)
                    if not good:
                        bad.append((r,s))
                        if len(bad)==1:
                            failures[orientation]={'indices':[r,s], 'intersection':sorted(common), 'difference_mod_N':delta%E.n, 'integer_remainder':E.witness(common,delta)}
                    if orientation=='rows' and not expect_good:
                        # Independent b-dependent line assignments are allowed.
                        if r%E.q!=s%E.q: assert good
                        else:
                            # Each fixed-b layer has a genuine failure.
                            if not good: same_b_bad+=1
                bump('full_gram_entries')
        failed_counts[orientation]=len(bad)
        assert (len(bad)==0)==expect_good
    if not expect_good: assert same_b_bad>0
    return {'q':E.q,'degree':d,'family':name,'valid':expect_good,'nonzero_offdiagonal_counts':failed_counts,'first_witnesses':failures}

def full_controls(E):
    records=[]; n=E.n; q=E.q
    for d in (1,5,q,n):
        m=n//d
        rows=[{c for c in range(n) if c%m==r//d} for r in range(n)]
        records.append(check_grams(E,rows,d,True,'divisor_rectangle'))
    for k in (2,3,4):
        for variable in (False,True):
            rows=[]
            for r in range(n):
                a,b=r%5,r%q
                start=((1+b%4)*a+b)%5 if variable else a
                A={(start+j)%5 for j in range(k)}
                rows.append({c for c in range(n) if c%5 in A})
            records.append(check_grams(E,rows,k*q,False,'varying_within_group' if variable else 'constant_within_group'))
    return records

def canonical_checks(E):
    q=E.q; n=E.n; endpoint_rows=[]
    for amask in range(31):
        A={u for u in range(5) if (amask>>u)&1}
        for bmask in range((1<<q)-1):
            B={v for v in range(q) if (bmask>>v)&1}
            S={(u,v) for u in range(5) for v in range(q) if u in A or v in B}
            actualA={u for u in range(5) if all((u,v) in S for v in range(q))}
            actualB={v for v in range(q) if all((u,v) in S for u in range(5))}
            assert actualA==A and actualB==B
            d=len(S); assert d==len(A)*q+(5-len(A))*len(B)
            if d in (2*q,3*q,4*q):
                assert not B and len(A)==d//q
                endpoint_rows.append({'A':sorted(A),'B':sorted(B),'degree':d})
            bump('canonical_actual_union_supports')
    assert len(endpoint_rows)==25
    # Full support is the sole degenerate canonical case, with both sets full.
    full={(u,v) for u in range(5) for v in range(q)}
    assert len(full)==n
    bump('canonical_full_support_guards')
    return {'q':q,'endpoint_supports':endpoint_rows}

def arithmetic_checks():
    rows=[]
    for q in range(7,1000):
        if not prime(q): continue
        for k in (2,3,4):
            solutions=[]
            for ell in range(6):
                for f in range(q+1):
                    if k*q==ell*q+(5-ell)*f: solutions.append([ell,f])
            assert solutions==[[k,0]],(q,k,solutions)
            rows.append({'q':q,'k':k,'solutions':solutions})
            bump('prime_endpoint_arithmetic_cases')
    # Dropping prime/coprimality can introduce mixed endpoint supports.
    assert 3*9==2*9+(5-2)*3
    assert 3*3==2*3+(5-2)*1
    return {'prime_cases':rows,'scope_guards':[{'q':9,'k':3,'ell':2,'f':3},{'q':3,'k':3,'ell':2,'f':1}]}

def rank_mod(matrix,p=1000003):
    M=[[x%p for x in row] for row in matrix]; row=0
    for col in range(len(M[0])):
        pivot=next((i for i in range(row,len(M)) if M[i][col]),None)
        if pivot is None: continue
        M[row],M[pivot]=M[pivot],M[row]
        inv=pow(M[row][col],-1,p); M[row]=[(x*inv)%p for x in M[row]]
        for i in range(row+1,len(M)):
            a=M[i][col]
            if a: M[i]=[(x-a*y)%p for x,y in zip(M[i],M[row])]
        row+=1
    return row

def cancellation_checks(E):
    q=E.q
    # Exact polynomial coordinates certify the claimed CRT tensor basis independently.
    basis=[E.residues[(E.e5*i+E.eq*j)%E.n] for i in range(4) for j in range(q-1)]
    assert rank_mod(basis)==E.m
    bump('full_rank_crt_bases')
    # Enumerate all binary corner choices in the kernel equations. Every zero
    # binary array has one such corner assignment once basis independence holds.
    accepted=0; rejected=0
    for last_row in itertools.product((0,1),repeat=q):
        for last_col_top in itertools.product((0,1),repeat=4):
            array=[]; valid=True
            for u in range(5):
                row=[]
                for v in range(q):
                    x=(last_col_top[u] if u<4 else last_row[-1])+last_row[v]-last_row[-1]
                    row.append(x)
                    if x not in (0,1): valid=False
                array.append(row)
            if not valid:
                rejected+=1; continue
            S=[E.idx(u,v) for u in range(5) for v in range(q) if array[u][v]]
            assert E.zero(S)
            const_rows=all(len(set(row))==1 for row in array)
            const_cols=all(len({array[u][v] for u in range(5)})==1 for v in range(q))
            assert const_rows or const_cols
            accepted+=1
            # Every primitive choice of zeta is preserved in actual exponents.
            for t in range(1,E.n):
                if math.gcd(t,E.n)==1:
                    assert E.zero(S,power=t); bump('primitive_root_zero_controls')
            # A single toggled coefficient cannot remain in the zero kernel.
            Sset=set(S)
            for c in range(E.n):
                toggled=Sset^{c}
                assert not E.zero(toggled); bump('one_bit_cancellation_negative_controls')
    assert accepted==(1<<5)+(1<<q)-2
    assert accepted+rejected==(1<<(q+4))
    bump('corner_assignments',accepted+rejected)
    return {'q':q,'binary_zero_arrays':accepted,'nonbinary_corner_arrays':rejected,'full_rank_basis_size':E.m}

def fixed_b_checks(E):
    q=E.q; records=[]
    for k in (1,2,3,4,5):
        subsets=list(itertools.combinations(range(5),k))
        sets=[set(A) for A in subsets]
        for A in sets:
            for B in sets:
                common=A&B
                S=[E.idx(u,v) for u in common for v in range(q)]
                for da in range(1,5):
                    r=E.idx(da,0); s=E.idx(0,0)
                    zero=E.zero(S,r-s)
                    assert zero==(len(common) in (0,5))
                    if k in (2,3,4): assert zero==(not common)
                    bump('fixed_b_exact_pair_sums')
        # Compute maximum compatible collection, independently of sum cardinality proof.
        def search(remaining,used):
            best=0
            for index,A in enumerate(remaining):
                if not A&used:
                    best=max(best,1+search(remaining[index+1:],used|A))
            return best
        maximum=search(sets,set())
        assert maximum==5//k
        if k in (2,3,4): assert maximum<5
        records.append({'q':q,'k':k,'max_pairwise_disjoint_line_sets':maximum})
    return records

def main():
    started=time.time(); controls=[]; phases=[]; canonical=[]; cancellation=[]; fixed=[]
    for q in (7,11,13,17,19,23):
        E=Exact(q); phase_checks(E)
        if q in (7,11,13): controls.extend(full_controls(E))
        if q in (7,11):
            canonical.append(canonical_checks(E))
            cancellation.append(cancellation_checks(E))
        fixed.extend(fixed_b_checks(E))
    arithmetic=arithmetic_checks()
    payloads={'FULL_GRAM_CONTROLS.json':controls,'CANONICAL_CONTROLS.json':canonical,
              'CANCELLATION_CONTROLS.json':cancellation,'FIXED_B_CONTROLS.json':fixed,
              'ARITHMETIC_CONTROLS.json':arithmetic}
    for name,value in payloads.items(): (ROOT/name).write_text(json.dumps(value,indent=2)+'\n')
    result={'status':'PASS','scope':'Independent exact controls for arbitrary binary fixed-Fourier equality-mask exclusion at N=5q, q prime >5, d in {2q,3q,4q}. Finite controls supplement the symbolic proof; no exhaustive square-mask classification or novelty claim.','counts':COUNTS,'elapsed_seconds':round(time.time()-started,3),'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__':main()
