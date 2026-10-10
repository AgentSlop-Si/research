#!/usr/bin/env python3
"""Independent data-only audit. No inherited research module is executed/imported.
Exact Q[z]/(1+z+...+z^10) implemented with canonical integer vectors;
coefficient strings parsed with a restricted AST. Certificates streamed by item.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from collections import Counter
from itertools import combinations
import ast, gzip, hashlib, json, math, time

BASE=Path(__file__).resolve().parents[2]
SRC=BASE/'research_cycle_1734/pole_escape'
OUT=Path(__file__).resolve().parent
START=time.monotonic()
CHECKS=[]
def require(test,message):
    if not test: raise AssertionError(message)
def passed(message):
    CHECKS.append(message); print('PASS:',message,flush=True)
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()

def canonical(values,den=1):
    a=list(values)+[0]*max(0,11-len(values))
    # z^11=1, followed by z^10=-sum_{j=0}^9 z^j.
    for j in range(len(a)-1,10,-1):a[j%11]+=a[j]
    q=a[10]; a=[a[j]-q for j in range(10)]
    if den<0:a=[-v for v in a];den=-den
    g=abs(den)
    for v in a:g=math.gcd(g,v)
    return (tuple(v//g for v in a),den//g)
FZERO=canonical([0]); FONE=canonical([1]); Z=canonical([0,1])
@lru_cache(maxsize=100000)
def fa(a,b):
    x,d=a;y,e=b; g=math.gcd(d,e)
    return canonical([u*(e//g)+v*(d//g) for u,v in zip(x,y)],d*(e//g))
def fn(a):return (tuple(-v for v in a[0]),a[1])
@lru_cache(maxsize=200000)
def fm(a,b):
    if a==FZERO or b==FZERO:return FZERO
    if a==FONE:return b
    if b==FONE:return a
    x,d=a;y,e=b;c=[0]*19
    for i,u in enumerate(x):
        if u:
            for j,v in enumerate(y):
                if v:c[i+j]+=u*v
    return canonical(c,d*e)
@lru_cache(maxsize=10000)
def fi(a):
    require(a!=FZERO,'division by zero field coefficient')
    cols=[fm(a,canonical([0]*j+[1])) for j in range(10)]
    mat=[[Fraction(cols[j][0][i],cols[j][1]) for j in range(10)]+[Fraction(i==0)] for i in range(10)]
    for j in range(10):
        k=next(k for k in range(j,10) if mat[k][j]);mat[j],mat[k]=mat[k],mat[j]
        s=mat[j][j];mat[j]=[v/s for v in mat[j]]
        for i in range(10):
            if i!=j and mat[i][j]:
                s=mat[i][j];mat[i]=[u-s*v for u,v in zip(mat[i],mat[j])]
    vals=[row[-1] for row in mat];den=math.lcm(*(q.denominator for q in vals))
    result=canonical([q.numerator*(den//q.denominator) for q in vals],den)
    require(fm(a,result)==FONE,'field inverse identity')
    return result
@lru_cache(maxsize=20000)
def fp(a,n):
    if n<0:return fp(fi(a),-n)
    r=FONE
    while n:
        if n&1:r=fm(r,a)
        a=fm(a,a);n//=2
    return r
@lru_cache(maxsize=50000)
def parsec(s):
    def walk(t):
        if isinstance(t,ast.Constant) and type(t.value) is int:return canonical([t.value])
        if isinstance(t,ast.Name) and t.id=='zeta':return Z
        if isinstance(t,ast.UnaryOp):
            a=walk(t.operand)
            if isinstance(t.op,ast.USub):return fn(a)
            if isinstance(t.op,ast.UAdd):return a
        if isinstance(t,ast.BinOp):
            a=walk(t.left)
            if isinstance(t.op,ast.Pow):
                require(isinstance(t.right,ast.Constant) and type(t.right.value) is int,'integer exponent')
                return fp(a,t.right.value)
            b=walk(t.right)
            if isinstance(t.op,ast.Add):return fa(a,b)
            if isinstance(t.op,ast.Sub):return fa(a,fn(b))
            if isinstance(t.op,ast.Mult):return fm(a,b)
            if isinstance(t.op,ast.Div):return fm(a,fi(b))
        raise ValueError('Unsupported coefficient expression')
    return walk(ast.parse(s,mode='eval').body)

# Sparse edge exponent vectors, unlike inherited dense-vector representation.
MONE=()
def mon(v):return tuple((i,int(n)) for i,n in enumerate(v) if n)
def edge_mon(edges):return tuple(sorted(Counter(edges).items()))
@lru_cache(maxsize=250000)
def mm(a,b):
    d=dict(a)
    for i,n in b:
        d[i]=d.get(i,0)+n
        if not d[i]:del d[i]
    return tuple(sorted(d.items()))
def mp(a,n):return tuple((i,k*n) for i,k in a if k*n)
def pput(p,m,c):
    v=fa(p.get(m,FZERO),c)
    if v!=FZERO:p[m]=v
    elif m in p:del p[m]
def pm(a,b):
    p={}
    for m,c in a.items():
        for n,d in b.items():pput(p,mm(m,n),fm(c,d))
    return p

def poly(terms):
    out={}
    for t in terms:
        require(len(t['exponent'])==99 and all(type(v) is int for v in t['exponent']),'valid exponent vector')
        m=mon(t['exponent']);c=parsec(t['coefficient'])
        require(c!=FZERO and m not in out,'canonical certificate polynomial')
        out[m]=c
    return out

def subst_monomial(p,x,c,m):
    out={}
    for e,a in p.items():
        d=dict(e);n=d.pop(x,0)
        pput(out,mm(tuple(d.items()),mp(m,n)),fm(a,fp(c,n)))
    return out

def subst_poly(p,x,r):
    out={}; powers={0:{MONE:FONE},1:r}
    for e,c in p.items():
        d=dict(e);n=d.pop(x,0)
        require(n>=0,'polynomial substitution cannot consume negative exponent')
        if n not in powers:
            for k in range(2,n+1):
                if k not in powers:powers[k]=pm(powers[k-1],r)
        base=tuple(d.items())
        for m,b in powers[n].items():pput(out,mm(base,m),fm(c,b))
    return out

def normalize(p,mandatory):
    if not p:return p,()
    support={i for m in p for i,n in m}; shifts=[]
    for i in sorted(support):
        v=min(dict(m).get(i,0) for m in p)
        require(v>=0 or i in mandatory,'negative exponent on optional edge')
        if v and i in mandatory:shifts.append((i,v))
    shift=tuple(shifts)
    return {mm(m,mp(shift,-1)):c for m,c in p.items()},shift

def stream_top(path):
    """Yield top-level (key,item,is_array_item) without loading whole certificate."""
    dec=json.JSONDecoder()
    with open(path,'r') as f:
        buf='';pos=0;eof=False
        def more():
            nonlocal buf,pos,eof
            buf=buf[pos:];pos=0
            s=f.read(65536);buf+=s
            if not s:eof=True
        def ws():
            nonlocal pos
            while True:
                while pos<len(buf) and buf[pos].isspace():pos+=1
                if pos<len(buf) or eof:return
                more()
        def char(c):
            nonlocal pos
            ws();require(pos<len(buf) and buf[pos]==c,'JSON expected '+c);pos+=1
        def value():
            nonlocal pos
            ws()
            while True:
                try:v,end=dec.raw_decode(buf,pos);pos=end;return v
                except json.JSONDecodeError:
                    if eof:raise
                    more()
        char('{')
        while True:
            ws()
            if buf[pos]=='}':pos+=1;break
            key=value();char(':')
            if key in ('remaining_equations','elimination_steps'):
                char('[');ws()
                if buf[pos]!=']':
                    while True:
                        yield key,value(),True;ws()
                        if buf[pos]==']':break
                        char(',')
                char(']')
            else:yield key,value(),False
            ws()
            if buf[pos]=='}':continue
            char(',')

def capture(path):
    metadata={};steps=[];eq={}
    for key,v,one in stream_top(path):
        if key=='elimination_steps':steps.append(v)
        elif key=='remaining_equations':
            label=tuple(v['label']);require(label not in eq,'duplicate label');eq[label]=poly(v['terms'])
        else:metadata[key]=v
    return metadata,steps,eq

def summary(eq):
    ps=[p for p in eq.values() if p]
    return {'variables':sorted({i for p in ps for m in p for i,n in m}),
            'equations':len(ps),'terms':sum(map(len,ps)),
            'max_terms':max(map(len,ps),default=0),'histogram':dict(sorted(Counter(map(len,ps)).items()))}

def comparable(eq):return {k:v for k,v in eq.items() if v}
def equations_hash(eq):
    data=[(list(k),[(list(m),list(c[0]),c[1]) for m,c in sorted(p.items())]) for k,p in sorted(eq.items()) if p]
    return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()

manifest=json.loads((SRC/'SYMBOLIC_REDUCTION_REVIEW_ENTRY.json').read_text())
hashes={}
for line in (SRC/'SYMBOLIC_REDUCTION_SHA256SUMS.txt').read_text().splitlines():
    expected,name=line.split(maxsplit=1);p=SRC/name
    actual=sha(p);require(actual==expected,'hash mismatch '+name);hashes[str(p.relative_to(BASE))]=actual
for item in manifest['files']+manifest['accepted_prerequisite_sources']:
    p=BASE/item['path'];actual=sha(p)
    require(actual==item['sha256'] and p.stat().st_size==item['bytes'],'entry manifest mismatch '+str(p))
    hashes[item['path']]=actual
for name in ('full_fourier_linear_reduction.json','full_fourier_linear_reduction_30steps.json'):
    h=hashlib.sha256()
    with gzip.open(SRC/(name+'.gz'),'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    require(h.hexdigest()==sha(SRC/name),'gzip mismatch')
passed('All manifest/source hashes and both decompressed certificate hashes match')
require(fp(Z,11)==FONE and sum(1 for _ in Z[0])==10,'field sanity')
s=FZERO
for j in range(11):s=fa(s,fp(Z,j))
require(s==FZERO,'Phi11 identity')
passed('Independent exact cyclotomic arithmetic and restricted coefficient parser initialized')

L=json.loads((SRC/'topology_11.json').read_text())['layers']
require(len(L)==3 and all(len(a)==33 and len(set(map(tuple,a)))==33 for a in L),'99 unique layer edges')
paths={(i,j):[] for i in range(11) for j in range(11)}
# Reconstruct through endpoint-indexed joins in CBA order.
for c,(i,v) in enumerate(L[2]):
    for b,(vb,u) in enumerate(L[1]):
        if vb==v:
            for a,(ua,j) in enumerate(L[0]):
                if ua==u:paths[i,j].append((a,33+b,66+c))
entries={}
for (i,j),ps in paths.items():
    p={MONE:fn(fp(Z,(i*j)%11))}
    for es in ps:pput(p,edge_mon(es),FONE)
    entries['entry',i,j]=p
mandatory={e for ps in paths.values() if len(ps)==1 for e in ps[0]}
unique_entries=[(i,j) for (i,j),ps in paths.items() if len(ps)==1]
# Expand every 2x2 determinant directly, including cancellation of intersecting paths.
minors={}; singleton_details=[]
for i,k in combinations(range(11),2):
    for j,l in combinations(range(11),2):
        signed=Counter()
        for a in paths[i,j]:
            for b in paths[k,l]:signed[edge_mon(a+b)]+=1
        for a in paths[i,l]:
            for b in paths[k,j]:signed[edge_mon(a+b)]-=1
        signed={m:n for m,n in signed.items() if n}
        if len(signed)==1:
            m,n=next(iter(signed.items()));target=fa(fp(Z,(i*j+k*l)%11),fn(fp(Z,(i*l+k*j)%11)))
            require(target!=FZERO,'nonzero Fourier minor')
            minors['minor',i,k,j,l]={m:canonical([n]),MONE:fn(target)}
            mandatory.update(e for e,v in m)
            singleton_details.append({'label':['minor',i,k,j,l],'sign':n,'edges':[e for e,v in m for _ in range(v)]})
require(len(unique_entries)==22 and len(minors)==4 and len(mandatory)==63,'mandatory topology counts')
passed('121 CBA entry equations and all 3025 two-row minors freshly expanded: 22 unique entries, four monomial minors, 63 mandatory edges')
mono=json.loads((SRC/'full_fourier_monomial_reduction.json').read_text())
require(mono['initial_mandatory_edges']==sorted(mandatory),'mandatory source equality')
# A -> D1 A, B -> D2 B D1^-1, C -> C D2^-1.
# Gauges in A select distinct D1 coordinates; gauges in C select distinct D2 coordinates.
gauges=mono['safe_gauge_edges'];used=set();gauge_coordinates=[]
for x in gauges:
    require(x in mandatory,'mandatory gauge')
    if x<33:coordinate=('D1',L[0][x][0])
    elif x>=66:coordinate=('D2',L[2][x-66][1])
    else:raise AssertionError('Unsupported mixed-layer gauge')
    require(coordinate not in used,'independent gauge coordinate');used.add(coordinate);gauge_coordinates.append([x,*coordinate])
require(len(gauges)==21,'21 independent gauges')
passed('21 simultaneous gauge fixes verified on distinct internal diagonal coordinates')
eq={**entries,**minors};eliminated=set();mono_records=[]
for k,s in enumerate(mono['substitutions']):
    x=s['variable'];c=parsec(s['coefficient']);m=mon(s['exponent']);reason=tuple(s['reason'])
    require(x not in eliminated and all(i!=x and i not in eliminated for i,n in m),'fresh monomial variable/dependencies')
    require(c!=FZERO,'nonzero monomial coefficient')
    if reason[0]=='gauge_fix':
        require(k<21 and x==gauges[k] and m==MONE and c==FONE,'gauge record')
    else:
        require(reason in eq and len(eq[reason])==2,'two-term source exists')
        a,b=eq[reason]
        require(set(i for i,n in a)<=mandatory or set(i for i,n in b)<=mandatory,'one binomial monomial is nonzero')
        mandatory.update(i for e in (a,b) for i,n in e)
        delta=dict(mm(a,mp(b,-1))).get(x,0)
        require(abs(delta)==1,'monomial solve exponent plus/minus one')
        require(not subst_monomial(eq[reason],x,c,m),'monomial substitution annihilates source')
    require(x in mandatory and all(i in mandatory for i,n in m),'only mandatory monomial dependencies')
    eq={lab:subst_monomial(p,x,c,m) for lab,p in eq.items()}
    eliminated.add(x);mono_records.append((x,c,m))
expected_mono={tuple(e['label']):poly(e['terms']) for e in mono['remaining_equations']}
require(comparable(eq)==expected_mono,'exact monomial-stage equation equality')
require(mono['current_mandatory_edges']==sorted(mandatory),'final mandatory list')
require(mono['eliminated_variables']==sorted(eliminated),'monomial eliminated list')
ms=summary(eq)
require(ms['variables']==mono['remaining_variables'] and len(ms['variables'])==52 and ms['equations']==97,'monomial counts')
passed('All 47 monomial/gauge records replay exactly; all 97 equations and 52 active variables match')

meta30,steps30,equations30=capture(SRC/'full_fourier_linear_reduction_30steps.json')
meta,steps,final_expected=capture(SRC/'full_fourier_linear_reduction.json')
require(steps[:30]==steps30,'30-step prefix identity')
linear_records=[];guard_records=[];normalizations=[];pivot_receipts=[]
eq=comparable(eq)
for number,s in enumerate(steps,1):
    normalized={};shifts=[]
    for lab,p in eq.items():
        q,shift=normalize(p,mandatory);normalized[lab]=q
        if shift:shifts.append({'label':list(lab),'mandatory_monomial':list(shift)})
    eq=normalized;normalizations.append({'before_step':number,'shifts':shifts})
    x=s['variable'];label=tuple(s['source_label']);source=poly(s['source_equation']);replacement=poly(s['replacement'])
    require(x not in eliminated and label in eq and eq[label]==source,'exact recorded pivot source '+str(number))
    pivots=[(m,c) for m,c in source.items() if dict(m).get(x)]
    require(len(pivots)==1,'one pivot term')
    pivot,c=pivots[0];d=dict(pivot);require(d.pop(x)==1,'linear degree one')
    require(all(i in mandatory for i in d),'no optional edge divisor')
    require(all(i!=x and i not in eliminated for m in replacement for i,n in m),'valid replacement dependencies')
    require(all(n>=0 or i in mandatory for m in replacement for i,n in m),'mandatory Laurent replacement denominators')
    require(not subst_poly(source,x,replacement),'replacement solves pivot exactly')
    required=x in mandatory
    require(required==s['replacement_required_nonzero_in_original_problem'],'recorded guard flag')
    if required:guard_records.append({'step':number,'variable':x,'source_label':list(label),'replacement_terms':len(replacement),'automatically_nonzero_constant':len(replacement)==1 and MONE in replacement,'replacement':s['replacement']})
    linear_records.append((x,replacement))
    eq={lab:subst_poly(p,x,replacement) for lab,p in eq.items()}
    require(sum(map(len,eq.values()))==s['remaining_total_terms'],'intermediate term count '+str(number))
    eliminated.add(x)
    pivot_receipts.append({'step':number,'variable':x,'pivot_denominator_monomial':list(d.items()),'nonzero_field_coefficient':True,'source_and_replacement_verified':True,'output_terms':sum(map(len,eq.values()))})
    if number==30:
        require(comparable(eq)==equations30,'full exact 30-step checkpoint match')
        passed('Independent replay matches every equation of the 30-step checkpoint')
    print('REPLAY linear',number,'variable',x,'terms',sum(map(len,eq.values())),flush=True)
# The final generator normalizes once at the start of the attempted, uncommitted step.
normalized={};shifts=[]
for lab,p in eq.items():
    q,shift=normalize(p,mandatory);normalized[lab]=q
    if shift:shifts.append({'label':list(lab),'mandatory_monomial':list(shift)})
eq=normalized;normalizations.append({'after_final_step':True,'shifts':shifts})
require(comparable(eq)==final_expected,'full final exact equation equality')
fs=summary(eq)
require(len(steps)==36 and len(fs['variables'])==16 and fs['equations']==59 and fs['terms']==30694 and fs['max_terms']==6271,'final statistics')
require(fs['variables']==meta['remaining_variables'] and meta['remaining_nonzero_equations']==fs['equations'],'final metadata')
require({str(k):v for k,v in fs['histogram'].items()}==meta['term_histogram'],'final term histogram')
require(not any(len(p)==1 and MONE in p for p in eq.values()),'no displayed nonzero constant contradiction')
require(all(n>=0 for p in eq.values() for m in p for i,n in m),'final equations polynomial')
passed('All 36 linear substitutions, pivots, normalizations and 59 final equations match exactly')

remaining_mandatory=sorted(set(fs['variables'])&mandatory)
require(len(remaining_mandatory)==8,'eight surviving mandatory coordinates')
# All dependency graphs are triangular in reverse chronological reconstruction.
known=set(fs['variables'])
for x,r in reversed(linear_records):
    require(all(i in known for m in r for i,n in m),'linear reverse-reconstruction dependencies')
    known.add(x)
for x,c,m in reversed(mono_records):
    require(all(i in known for i,n in m),'monomial reverse-reconstruction dependencies')
    known.add(x)
require(known==set(range(99)),'all original coefficients reconstruct')
passed('Reverse reconstruction is triangular for all 99 edges, conditional on eight surviving and six nonconstant eliminated guards')

# Express the six nonconstant reconstruction guards entirely in final coordinates.
# Laurent monomial factors below use only the eight surviving mandatory edges.
replacements=dict(linear_records)
final_guard_sources={98:replacements[98],95:replacements[95],46:replacements[46],48:replacements[48]}
final_guard_sources[89]=subst_poly(replacements[89],46,replacements[46])
n95=pm({((91,1),):FONE},replacements[95])
a96=replacements[96][MONE];b96=replacements[96][((95,-1),)]
n96={m:fm(a96,c) for m,c in n95.items()}
pput(n96,((91,1),),b96)
final_guard_sources[96]=n96
# Exact rational identity: R96(N95/x91) = N96/N95.
require(pm(n95,{MONE:a96})=={m:fm(a96,c) for m,c in n95.items()},'guard96 numerator construction')
final_guards=[]
for x in [98,96,89,95,46,48]:
    p,shift=normalize(final_guard_sources[x],mandatory)
    require(all(i in fs['variables'] and n>=0 for m in p for i,n in m),'final-coordinate guard polynomial')
    require(all(i in remaining_mandatory for i,n in shift),'guard normalization uses surviving mandatory variables')
    scale=next(iter(p.values()));p={m:fm(c,fi(scale)) for m,c in p.items()}
    final_guards.append({'eliminated_mandatory_edge':x,'terms':[{'exponent':[[i,n] for i,n in m],'coefficient_numerators':list(c[0]),'coefficient_denominator':c[1]} for m,c in sorted(p.items())], 'normalizing_mandatory_monomial':list(shift), 'term_count':len(p), 'extra_denominator_guard_edge':95 if x==96 else None})
(OUT/'FINAL_COORDINATE_GUARDS.json').write_text(json.dumps({'field_basis':'1,zeta,...,zeta^9; Phi11(zeta)=0','nonzero_surviving_coordinates':remaining_mandatory,'nonzero_guard_polynomials':final_guards,'scope':'Each listed guard must be nonzero. For edge96 the extra rational denominator is the edge95 guard, already required nonzero. Each polynomial is scaled by a nonzero field constant and by mandatory Laurent monomials only.'},indent=2)+'\n')
passed('Six nonconstant guard numerators expressed exactly in the final sixteen coordinates')

# Prepare human-readable and machine-readable guard/cancellation data without changing certificates.
# Factor cancellation may use only these verified nonzero sources; no assumption that an optional edge is nonzero.
receipt={
 'status':'PASS: exact necessary reduction verified; no factorization or impossibility conclusion',
 'review_method':'Fresh checker; custom exact cyclotomic field and restricted AST; direct entry/minor expansion; streamed certificates; no inherited programs executed or imported',
 'coefficient_field':'Q[zeta]/(1+zeta+...+zeta^10)',
 'source_hashes':hashes,
 'fresh_checker_sha256':sha(Path(__file__)),
 'checks':CHECKS,
 'topology':{'edges':99,'entry_equations':121,'two_by_two_minors_checked':3025,'unique_entries':22,'monomial_minors':singleton_details,'mandatory_edges':sorted(mandatory)},
 'gauge_coordinates':gauge_coordinates,
 'monomial_stage':{'substitutions':47,'gauges':21,'monomial_eliminations':26,**ms,'canonical_equations_sha256':equations_hash(expected_mono)},
 'linear_stage':{'steps':36,'thirty_step_checkpoint_verified':True,'all_pivots_only_mandatory_denominators':True,'pivots':pivot_receipts},
 'final_stage':{**fs,'canonical_equations_sha256':equations_hash(eq),'nonzero_constant_found':False,'factorization_found':False},
 'reconstruction':{'remaining_mandatory_variables':remaining_mandatory,'eliminated_mandatory_variables':[g['variable'] for g in guard_records],'automatically_nonzero_constants':[g['variable'] for g in guard_records if g['automatically_nonzero_constant']],'nonconstant_eliminated_guards':[g['variable'] for g in guard_records if not g['automatically_nonzero_constant']],'all_99_variables_reverse_reconstruct':True,'guard_file':'RECONSTRUCTION_GUARDS.json','final_coordinate_guard_file':'FINAL_COORDINATE_GUARDS.json','final_guard_term_counts':{str(g['eliminated_mandatory_edge']):g['term_count'] for g in final_guards},'scope':'Final polynomial equations alone are necessary. Reverse reconstruction requires surviving mandatory coordinates and each recorded mandatory replacement to be nonzero. No sufficiency claim without these checks.'},
 'normalization_file':'NORMALIZATION_LEDGER.json',
 'safe_next_step':'Factor equations exactly over Q(zeta11), cancel only nonzero constants, surviving mandatory monomials, or factors proved nonzero by the retained reverse-reconstruction guards. Keep every optional-zero component unless separately certified impossible. For solving, use a guarded rational reconstruction or saturation with explicit nonzero constraints.',
 'runtime_seconds':time.monotonic()-START
}
(OUT/'RECONSTRUCTION_GUARDS.json').write_text(json.dumps({'remaining_mandatory_variables':remaining_mandatory,'reverse_evaluation_order':[x for x,r in reversed(linear_records)],'eliminated_mandatory_guards':guard_records},indent=2)+'\n')
(OUT/'NORMALIZATION_LEDGER.json').write_text(json.dumps(normalizations,indent=2)+'\n')
(OUT/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'final':fs,'remaining_mandatory':remaining_mandatory,'nonconstant_guards':receipt['reconstruction']['nonconstant_eliminated_guards'],'runtime_seconds':receipt['runtime_seconds']},indent=2),flush=True)
