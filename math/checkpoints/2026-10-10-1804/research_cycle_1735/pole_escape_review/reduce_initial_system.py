"""Fresh exact Laurent elimination of the W2 initial system over F_11.
This is an independent audit program, not an imported source dependency.
"""
from pathlib import Path
import json, collections, math
P=Path(__file__).resolve().parent
R=json.loads((P/'REVIEW_RECEIPT.json').read_text()); n=99; prime=11
zero=(0,)*n
polys=[];labels=[]
for entry in R['exact_tropical_entries']:
    d={}
    for path,v in zip(entry['paths'],entry['path_values']):
        if v!=entry['minimum']:continue
        a=[0]*n
        for e in path:a[e]+=1
        a=tuple(a);d[a]=(d.get(a,0)+1)%prime
    if entry['minimum']==0:d[zero]=(d.get(zero,0)-1)%prime
    polys.append({a:c for a,c in d.items() if c});labels.append([entry['output'],entry['input']])
T=json.loads(Path('research_cycle_1734/pole_escape/topology_11.json').read_text())['layers']
gauge=[]
for v in range(11):
    gauge.append(next(i for i,(r,s) in enumerate(T[0]) if r==v))
    gauge.append(66+next(i for i,(r,s) in enumerate(T[2]) if s==v))
for k in gauge:
    a=[0]*n;a[k]=1;polys.append({tuple(a):1,zero:10});labels.append(['gauge',k])

def sub(poly,k,exponents,c):
    out={}
    for a,z in poly.items():
        ak=a[k]; b=[a[j]+ak*exponents[j] for j in range(n)];b[k]=0
        q=z*pow(c,ak,prime)%prime; b=tuple(b)
        out[b]=(out.get(b,0)+q)%prime
    return {a:z for a,z in out.items() if z}

eliminated=[];steps=[]
while True:
    one=next((i for i,p in enumerate(polys) if len(p)==1),None)
    if one is not None:
        outcome={'status':'CONTRADICTION','label':labels[one],'polynomial':[[list(a),c] for a,c in polys[one].items()]};break
    choices=[]
    for i,p in enumerate(polys):
        if len(p)!=2:continue
        (a,c),(b,d)=list(p.items());r=[x-y for x,y in zip(a,b)]
        for k,q in enumerate(r):
            if abs(q)==1:
                # Prefer gauge and lower total exponent spread.
                score=(0 if labels[i][0]=='gauge' else 1,sum(abs(v) for v in r),k,i)
                choices.append((score,i,k,r,(-d*pow(c,-1,prime))%prime,q))
    if not choices:
        outcome={'status':'REDUCED_WITHOUT_CONTRADICTION'};break
    _,i,k,r,rhs,q=min(choices)
    exponents=[-a//q for a in r];exponents[k]=0
    c=pow(rhs,q,prime)
    steps.append({'source_label':labels[i],'eliminated_variable':k,'rhs_coefficient_mod11':c,'rhs_exponents':exponents})
    polys=[sub(p,k,exponents,c) for p in polys]
    eliminated.append(k)

remaining=[(labels[i],p) for i,p in enumerate(polys) if p]
out={'outcome':outcome,'eliminated_variables':eliminated,'remaining_variables':sorted({j for _,p in remaining for a in p for j,v in enumerate(a) if v}),'nonzero_equation_count':len(remaining),'remaining_term_histogram':dict(collections.Counter(len(p) for _,p in remaining)),'elimination_steps':steps,'remaining_equations':[{'label':label,'terms':[{'exponents':list(a),'coefficient':c} for a,c in p.items()]} for label,p in remaining]}
(P/'LAURENT_REDUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['elimination_steps','remaining_equations']},indent=2))
