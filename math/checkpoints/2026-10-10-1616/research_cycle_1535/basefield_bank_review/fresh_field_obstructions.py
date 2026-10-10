"""Independent finite arithmetic only; no author program imports or execution."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent

def val(f,x,p):
    y=0
    for a in f[::-1]: y=(y*x+a)%p
    return y

def mul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%p
    return c

def n7(p,q):
    assert pow(q,7,p)==1 and q!=1
    s2=val([-8,35,25,28,1,-17],q,p)*pow(29,-1,p)%p
    s3=val([-3,-5,-16,-4,4,19],q,p)*pow(29,-1,p)%p
    g=[-s3%p,s2,0,1]
    values=[val(g,x,p) for x in range(p)]
    disc=(-4*s2**3-27*s3**2)%p
    return dict(p=p,q=q,s2=s2,s3=s3,ascending_coefficients=g,evaluation_values=values,roots=[x for x,v in enumerate(values) if v==0],discriminant=disc,disc_euler=pow(disc,(p-1)//2,p))

c71=n7(71,48)
assert c71['roots']==[] and c71['ascending_coefficients']==[15,47,0,1]
c43=n7(43,4)
assert c43['ascending_coefficients']==[21,21,0,1]
assert c43['discriminant']==26 and c43['disc_euler']==42
assert mul([42,1],[22,1,1],43)==c43['ascending_coefficients']
g11=[12,21,2,4,0,0,1]
values11=[val(g11,x,23) for x in range(23)]
assert [x for x,v in enumerate(values11) if not v]==[7,8]
quartic=[15,20,8,15,1]
assert mul(mul([16,1],[15,1],23),quartic,23)==g11
# A quartic with no roots and no monic irreducible quadratic divisor is irreducible.
assert all(val(quartic,x,23) for x in range(23))
def modpoly(a,b,p):
    a=a[:]
    while len(a)>=len(b):
        c=a[-1]*pow(b[-1],-1,p)%p
        shift=len(a)-len(b)
        for i,v in enumerate(b): a[i+shift]=(a[i+shift]-c*v)%p
        while a and a[-1]==0: a.pop()
    return a
quadratic_factors=[]
for a in range(23):
    for b in range(23):
        if not modpoly(quartic,[b,a,1],23): quadratic_factors.append([b,a,1])
assert not quadratic_factors
report={
 'status':'PASS',
 'scope':'Frozen witnesses only; does not exclude alternative eight/fourteen-bank K representations.',
 'N7_irreducibility_at_71':c71,
 'N7_discriminant_nonsquare_at_43':c43,
 'N7_conclusion':'Frozen cubic irreducible over Q(q); its discriminant is nonsquare, so its splitting field has degree exactly 6 over Q(q).',
 'N11_non_split_at_23':dict(p=23,q=2,ascending_coefficients=g11,evaluation_values=values11,roots=[7,8],factor_degrees=[1,1,4],irreducible_quartic_ascending=quartic,quadratic_factors=quadratic_factors),
 'N11_conclusion':'Frozen sextic does not split over Q(q). At the good prime its squarefree factor degrees are 1,1,4. No exact splitting-field degree asserted.',
 'independence':'Fresh elementary integer arithmetic. No source program was imported, executed, compiled, or parsed.'}
(OUT/'FROZEN_FIELD_OBSTRUCTION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k.endswith('conclusion') or k=='status'},indent=2))
