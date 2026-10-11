"""Independent review arithmetic; reads inert JSON only, never research programs."""
import json, hashlib, math, time, copy
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
checks=[]
def require(test,label):
    if not test: raise AssertionError(label)
    checks.append(label)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads((ROOT/path).read_text())
def knorm(v,d=1):
    assert len(v)==10 and d
    g=math.gcd(d,*v)
    if d<0:g=-g
    return (tuple(x//g for x in v),d//g)
Z=knorm([0]*10); O=knorm([1]+[0]*9)
def kadd(a,b):
    av,ad=a;bv,bd=b
    if ad==bd:return knorm([x+y for x,y in zip(av,bv)],ad)
    g=math.gcd(ad,bd)
    return knorm([x*(bd//g)+y*(ad//g) for x,y in zip(av,bv)],ad*(bd//g))
def kneg(a):return (tuple(-x for x in a[0]),a[1])
@lru_cache(maxsize=200000)
def kmul(a,b):
    if a==Z or b==Z:return Z
    av,ad=a;bv,bd=b
    # Two independently organized reductions agree on every distinct product.
    long=[0]*19
    cyc=[0]*11
    for i,x in enumerate(av):
        for j,y in enumerate(bv):
            long[i+j]+=x*y
            cyc[(i+j)%11]+=x*y
    for i in range(18,9,-1):
        t=long[i]
        for j in range(11):long[i-j]-=t
    cycred=[cyc[i]-cyc[10] for i in range(10)]
    assert long[:10]==cycred
    return knorm(cycred,ad*bd)
def qtrim(p):
    while p and not p[-1]:p.pop()
    return p
def qdiv(a,b):
    a=list(a);b=qtrim(list(b)); assert b
    q=[Fraction(0)]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        d=len(a)-len(b);c=a[-1]/b[-1];q[d]=c
        for j,x in enumerate(b):a[d+j]-=c*x
        qtrim(a)
    return qtrim(q),a
def qsub(a,b):return qtrim([(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def qmul(a,b):
    p=[Fraction(0)]*max(0,len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):p[i+j]+=x*y
    return qtrim(p)
@lru_cache(maxsize=10000)
def kinv(a):
    assert a!=Z
    oldr=[Fraction(1)]*11;r=qtrim([Fraction(x,a[1]) for x in a[0]])
    oldt=[];t=[Fraction(1)]
    while r:
        q,nr=qdiv(oldr,r);oldr,r=r,nr;oldt,t=t,qsub(oldt,qmul(q,t))
    assert len(oldr)==1
    _,v=qdiv([x/oldr[0] for x in oldt],[Fraction(1)]*11)
    d=math.lcm(*[x.denominator for x in v]);out=knorm([int(x*d) for x in v]+[0]*(10-len(v)),d)
    assert kmul(a,out)==O
    return out
# Sparse multivariate polynomials use exponent tuples.
def clean(p):return {m:c for m,c in p.items() if c!=Z}
def padd(a,b):
    p=dict(a)
    for m,c in b.items():p[m]=kadd(p.get(m,Z),c)
    return clean(p)
def pneg(a):return {m:kneg(c) for m,c in a.items()}
def psub(a,b):return padd(a,pneg(b))
def pmul(a,b):
    p={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            m=tuple(x+y for x,y in zip(ma,mb));p[m]=kadd(p.get(m,Z),kmul(ca,cb))
    return clean(p)
def ppow(a,n):
    arity=len(next(iter(a))) if a else 1
    p={(0,)*arity:O}
    for _ in range(n):p=pmul(p,a)
    return p
def pscale(a,c):return clean({m:kmul(x,c) for m,x in a.items()})
def parse(terms,n):
    p={}
    for m,v,d in terms:
        assert len(m)==n and len(v)==10 and isinstance(d,int) and d>0
        assert all(isinstance(x,int) and x>=0 for x in m)
        assert tuple(m) not in p
        p[tuple(m)]=knorm(v,d)
    return clean(p)
def compress(terms,n,keep):
    p=parse(terms,n)
    assert all(all(m[i]==0 for i in range(n) if i not in keep) for m in p)
    return {tuple(m[i] for i in keep):c for m,c in p.items()}
def udiv(a,b):
    assert b
    a=dict(a);q={};bm=max(b)[0];bc=b[(bm,)];bi=kinv(bc)
    while a and max(a)[0]>=bm:
        am=max(a)[0];d=am-bm;c=kmul(a[(am,)],bi);q[(d,)]=c
        a=psub(a,{(m[0]+d,):kmul(v,c) for m,v in b.items()})
    return q,a
def ugcd(a,b):
    while b:_,r=udiv(a,b);a,b=b,r
    return pscale(a,kinv(a[max(a)])) if a else {}
def coeffs_b(p):
    return {i:{(e,):c for (b,e),c in p.items() if b==i} for i in range(max(m[0] for m in p)+1)}
def sylvester(a,b):
    ac=coeffs_b(a);bc=coeffs_b(b);m=max(ac);n=max(bc);N=m+n
    matrix=[]
    for row in range(n):matrix.append([ac.get(m-(col-row),{}) if row<=col<=row+m else {} for col in range(N)])
    for row in range(m):matrix.append([bc.get(n-(col-row),{}) if row<=col<=row+n else {} for col in range(N)])
    # Subset DP evaluates Leibniz determinant without dividing by pivots.
    partial={0:{(0,):O}}
    for row in range(N):
        nxt={}
        for mask,val in partial.items():
            for col in range(N):
                if mask>>col&1:continue
                term=pmul(val,matrix[row][col]);sign=(-1)**sum(bool(mask>>k&1) for k in range(col+1,N))
                if sign<0:term=pneg(term)
                nm=mask|1<<col;nxt[nm]=padd(nxt.get(nm,{}),term)
        partial=nxt
    return partial[(1<<N)-1],matrix

def eval_axis(p,axis,value):
    arity=len(next(iter(p))) if p else 1
    powers={0:O}
    for i in range(1,max((m[axis] for m in p),default=0)+1):powers[i]=kmul(powers[i-1],value)
    out={}
    for m,c in p.items():
        nm=m[:axis]+m[axis+1:];out[nm]=kadd(out.get(nm,Z),kmul(c,powers[m[axis]]))
    return clean(out)
def scalar_eval(p,value):
    out=eval_axis(p,0,value)
    return out.get((),Z)
def base_checks():
    baseline=read('research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json')
    recpath=ROOT/'research_cycle_2310/hnonzero_continuation_review/RECEIPT.json'
    require(digest(recpath)=='22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e','accepted base review receipt pin')
    rec=json.loads(recpath.read_text())
    require(digest(ROOT/rec['candidate_path'])==rec['candidate_sha256'],'accepted affine candidate pin')
    for p,h in rec['source_hashes'].items():require(digest(ROOT/p)==h,'historical inert pin '+p)
    for p,h in baseline['source_hashes'].items():require(digest(ROOT/p)==h,'base inert pin '+p)
    atlas=read('research_cycle_2014/fused_chart_atlas/CERTIFICATE.json')
    src=read('research_cycle_1805/guarded_fourier_reduction/CERTIFICATE.json')
    branch=baseline['branches'][1]['retained_branch']
    require(branch['retained_equations']==atlas['equations'],'all accepted residual identities preserved')
    require(branch['retained_guards']==atlas['guards'],'all accepted guards preserved')
    require(len(branch['retained_equations'])==50,'50 retained residuals')
    require(len(branch['retained_guards'])==19,'19 retained guards')
    require('x41' in branch['retained_guards'] and 'x83' in branch['retained_guards'],'original q and e nonzero guards')
    require('b!=0' in branch['additional_guards'],'accepted b nonzero guard')
    require(branch['conditions']==['Q_H!=0','d!=0','F_M!=0'],'exact accepted regular branch conditions')
    a=compress(baseline['A'],4,[0,3]);beta=compress(baseline['B'],4,[0,3])
    require(min(m[0] for m in a)==3 and min(m[1] for m in a)==1,'A exact b^3 e monomial content')
    require(min(m[0] for m in beta)==3 and min(m[1] for m in beta)==1,'B exact b^3 e monomial content')
    a={(b-3,e-1):c for (b,e),c in a.items()};beta={(b-3,e-1):c for (b,e),c in beta.items()}
    H=compress(atlas['polynomials']['Q_H'],7,[5]);D25=compress(atlas['polynomials']['Q_D25'],7,[5]);C1=compress(atlas['polynomials']['Q_C1'],7,[5])
    return baseline,atlas,branch,a,beta,H,D25,C1

def validate(candidate,baseline,atlas,branch,a,beta,H,D25,resultant,fa_coeffs):
    poly=candidate['polynomials']
    require(candidate['variables']==[11,83],'candidate b,e variable order')
    require(candidate['retained_exception']==baseline['branches'][1],'complete original exception wrapper unchanged')
    ledger=candidate['retained_denominator_exclusions']
    for key in ['coordinate_ledger','E41_den','E41_denominator_quotient','c_den','c_clearing_exponent']:
        require(ledger[key]==baseline[key],'unchanged cancellation ledger '+key)
    require(candidate['common_monomial']['powers']==[3,1],'only b^3 e canceled')
    require(candidate['common_monomial']['nonzero_justification']==['retained additional guard b!=0','original guard x83=e!=0'],'monomial guards cited exactly')
    for k,expected,arity in [('alpha',a,2),('beta',beta,2),('H',H,1),('D25',D25,1),('resultant_b',resultant,1)]:
        require(parse(poly[k],arity)==expected,'independent source binding '+k)
    require(poly['F_A_clearing_exponent']==1,'F_A exact c clearing exponent')
    require([parse(p,2) for p in poly['F_A_cleared_q_coefficients']]==fa_coeffs,'F_A independent cleared q coefficients')
    fac=candidate['resultant_factorization']
    require(fac['H_multiplicity']==9 and fac['D25_multiplicity']==4,'H and D25 factor multiplicities')
    require(fac['unit']=='resultant_unit','resultant unit binding')
    product=parse(poly['resultant_unit'],1)
    require(set(product)=={(0,)},'factorization nonzero scalar')
    product=pmul(product,pmul(ppow(H,9),ppow(D25,4)))
    linears=[];decics=[]
    for index,record in enumerate(fac['factors']):
        f=parse(record['poly'],1)
        require(record['degree']==max(f)[0],'correct recorded degree factor '+str(index))
        require(f[max(f)]==O,'monic resultant factor '+str(index))
        require(isinstance(record['multiplicity'],int) and record['multiplicity']>0,'positive multiplicity '+str(index))
        product=pmul(product,ppow(f,record['multiplicity']))
        if record['degree']==1:linears.append(index)
        elif record['degree']==10:decics.append(index)
        else:require(False,'only checked linear factors and a decic allowed')
    require(product==resultant,'complete exact resultant factorization')
    require(len(linears)==5 and len(decics)==1,'exact five linear factors and one decic')
    require(parse(poly['F10'],1)==parse(fac['factors'][decics[0]]['poly'],1),'F10 exact factor binding')
    require(fac['factors'][decics[0]]['multiplicity']==1,'F10 multiplicity one')
    cases=candidate['linear_zero_branch_certificates']
    require([c['factor_index'] for c in cases]==linears,'every linear zero case covered once')
    observed=[]
    for record in cases:
        i=record['factor_index'];root=knorm(*record['root'])
        require(scalar_eval(parse(fac['factors'][i]['poly'],1),root)==Z,'linear root correct '+str(i))
        sa=eval_axis(a,1,root);sb=eval_axis(beta,1,root)
        require(parse(record['alpha_specialization'],1)==sa,'exact specialized alpha '+str(i))
        require(parse(record['beta_specialization'],1)==sb,'exact specialized beta '+str(i))
        U=parse(record['U'],1);V=parse(record['V'],1);G=parse(record['G'],1)
        require(padd(pmul(U,sa),pmul(V,sb))==G,'exact specialized Bezout '+str(i))
        require(pmul(G,parse(record['alpha_over_G'],1))==sa,'G divides specialized alpha '+str(i))
        require(pmul(G,parse(record['beta_over_G'],1))==sb,'G divides specialized beta '+str(i))
        require(G and G[max(G)]==O,'specialized G monic nonzero '+str(i))
        # An independently computed Euclidean gcd also agrees, including degree drops.
        require(ugcd(sa,sb)==G,'independent specialized gcd '+str(i))
        observed.append([i,max(sa)[0],max(sb)[0],max(G)[0]])
        if G=={(0,):O}:
            require(record['outcome']=='excluded: U*alpha+V*beta=1 on this linear zero branch','unit-gcd exclusion wording '+str(i))
        else:
            require(max(G)[0]==1,'remaining G exactly linear')
            broot=knorm(*record['b_root']);require(scalar_eval(G,broot)==Z,'remaining G root')
            require(record['c_clearing_power']==1,'guard obstruction clearing exponent')
            require(record['outcome']=='excluded: G=0 forces F_A=0, contrary to retained F_A!=0','guard obstruction outcome')
            require('F_A!=0' in branch['additional_guards'],'F_A guard retained')
            require(len(record['F_A_cleared_specialization'])==2 and len(record['F_A_cleared_over_G'])==2,'both q coefficients certified')
            for j in range(2):
                ac=eval_axis(fa_coeffs[j],1,root)
                require(parse(record['F_A_cleared_specialization'][j],1)==ac,'F_A specialization '+str(j))
                require(pmul(G,parse(record['F_A_cleared_over_G'][j],1))==ac,'G divides F_A coefficient '+str(j))
            require(broot!=Z and scalar_eval(H,root)!=Z,'guard obstruction c denominator nonzero')
    expected=[
      {'name':'F10_nonzero','condition':'F10(e)!=0','outcome':'excluded under the complete retained exception by the factored resultant and zero-branch exclusions'},
      {'name':'F10_zero','condition':'F10(e)=0','outcome':'retained unresolved','inputs':[11,41,83],'additional_equations':['F10(e)=0'],'q_reconstruction':'q remains a retained input; original q!=0 guard retained','definitions_and_predicates':'execute every unchanged retained_exception definition and test every unchanged residual, guard, condition and denominator exclusion','forward_map':'identity on the retained inputs (b,q,e)','reverse_map':'identity on the retained inputs (b,q,e)'}]
    require(candidate['new_exhaustive_refinement']==expected,'exhaustive disjoint refinement and identity maps')
    positive=['necessary_degree_10_e_condition','all_linear_resultant_zero_cases_accounted_for','all_50_original_residuals_retained','all_19_original_guards_retained','original_q_nonzero_retained','all_canceled_denominators_retained']
    negative=['exception_infeasible','F10_sufficient','F10_irreducible','feasible_point_found','dimension','novelty','full_Fourier_factorization','global_chart_refinement']
    require(candidate['claims']=={**{k:True for k in positive},**{k:False for k in negative}},'bounded claims without feasibility or full-factorization overreach')
    return observed

if __name__=='__main__':
    start=time.monotonic();baseline,atlas,branch,a,beta,H,D25,C1=base_checks()
    candidate_path='research_cycle_2325/f11_affine_exception/CANDIDATE.json'
    require(digest(ROOT/candidate_path)=='67cb144d8adc3c25909e2e6c13b5bcf32abe49ccef69ab51fb77a1f508aacd0f','fixed candidate bytes')
    candidate=read(candidate_path)
    for p,h in candidate['source_hashes'].items():require(digest(ROOT/p)==h,'candidate source pin '+p)
    print('Computing independent division-free determinant...',flush=True)
    resultant,matrix=sylvester(a,beta)
    require(bool(resultant),'resultant formally nonzero')
    print('Resultant computed, degree',max(resultant)[0], 'elapsed',time.monotonic()-start,flush=True)
    content={}
    for coeff in list(coeffs_b(a).values())+list(coeffs_b(beta).values()):
        content=ugcd(content,coeff)
        if content=={(0,):O}:break
    require(content=={(0,):O},'joint K[e] content is one')
    print('GCD is precisely b^3 e up to a K unit; elapsed',time.monotonic()-start,flush=True)
    cn=compress(atlas['polynomials']['Q_c_num'],7,[1,5]);cd=compress(atlas['polynomials']['Q_c_den'],7,[1,5])
    fa=parse(atlas['polynomials']['F_A'],7);fa_coeffs=[{},{}]
    require(max(m[2] for m in fa)==1 and max(m[3] for m in fa)==1,'source F_A affine in c and q')
    for mon,coef in fa.items():
        require(all(mon[i]==0 for i in [0,4,6]),'source F_A uses only b,c,q,e')
        term=pmul({(mon[1],mon[5]):coef},pmul(ppow(cn,mon[2]),ppow(cd,1-mon[2])))
        fa_coeffs[mon[3]]=padd(fa_coeffs[mon[3]],term)
    observed=validate(candidate,baseline,atlas,branch,a,beta,H,D25,resultant,fa_coeffs)
    print('All five linear zero cases and retained decic verified; elapsed',time.monotonic()-start,flush=True)
    passed_checks=list(checks)
    # Deliberate semantic corruptions are checked without the fixed candidate hash gate.
    mutations=[]
    def mutation(label,edit):
        bad=copy.deepcopy(candidate);edit(bad);mutations.append((label,bad))
    def coefficient_bad(c,path):
        x=c
        for key in path:x=x[key]
        x[0][1][0]+=1
    mutation('alpha coefficient',lambda c:coefficient_bad(c,['polynomials','alpha']))
    mutation('resultant coefficient',lambda c:coefficient_bad(c,['polynomials','resultant_b']))
    mutation('factor multiplicity',lambda c:c['resultant_factorization']['factors'][0].update(multiplicity=2))
    mutation('remove fifth zero case',lambda c:c['linear_zero_branch_certificates'].pop())
    mutation('Bezout U coefficient',lambda c:coefficient_bad(c,['linear_zero_branch_certificates',0,'U']))
    mutation('linear root coefficient',lambda c:c['linear_zero_branch_certificates'][0]['root'][0].__setitem__(0,1))
    mutation('guard F_A quotient coefficient',lambda c:coefficient_bad(c,['linear_zero_branch_certificates',1,'F_A_cleared_over_G',0]))
    mutation('drop q coefficient proof',lambda c:c['linear_zero_branch_certificates'][1]['F_A_cleared_over_G'].pop())
    mutation('remove residual',lambda c:c['retained_exception']['retained_branch']['retained_equations'].pop('41'))
    mutation('remove q guard',lambda c:c['retained_exception']['retained_branch']['retained_guards'].pop('x41'))
    mutation('introduce optional x0 nonzero',lambda c:c['retained_exception']['retained_branch']['additional_guards'].append('x0!=0'))
    mutation('drop denominator exclusion',lambda c:c['retained_denominator_exclusions']['coordinate_ledger'].pop())
    mutation('change clearing power',lambda c:c['polynomials'].update(F_A_clearing_exponent=2))
    mutation('remove unresolved decic',lambda c:c['new_exhaustive_refinement'].pop())
    mutation('assert infeasibility',lambda c:c['claims'].update(exception_infeasible=True))
    mutation('assert sufficiency',lambda c:c['claims'].update(F10_sufficient=True))
    rejected=[]
    for label,bad in mutations:
        try:validate(bad,baseline,atlas,branch,a,beta,H,D25,resultant,fa_coeffs)
        except (AssertionError,KeyError,IndexError):rejected.append(label)
        else:raise AssertionError('negative control accepted: '+label)
    checks=passed_checks
    for p,h in candidate['source_hashes'].items():require(digest(ROOT/p)==h,'final source recheck '+p)
    require(digest(ROOT/candidate_path)=='67cb144d8adc3c25909e2e6c13b5bcf32abe49ccef69ab51fb77a1f508aacd0f','final candidate recheck')
    receipt={'status':'PASS independent exact arithmetic and semantic checks','checks':checks,'exact_check_count':len(checks),'negative_controls_rejected':rejected,'coefficient_products_dual_checked':kmul.cache_info().misses,'elapsed_seconds':time.monotonic()-start,'resultant_degree':max(resultant)[0],'gcd_up_to_nonzero_scalar':'b^3 e','specializations_factor_index_alpha_degree_beta_degree_gcd_degree':observed,'method':'Python standard-library exact rational arithmetic; every K product dual-reduced; division-free 5 by 5 Sylvester determinant; independent K[e] and K[b] Euclidean gcds; exact Bezout, factorization, and guard-divisibility checks','author_or_inherited_programs_read_or_executed':False,'modular_or_numerical_inference':False}
    (OUT/'ARITHMETIC_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS',len(checks),'exact checks;',len(rejected),'semantic negative controls rejected; elapsed',time.monotonic()-start,flush=True)
