"""Independent recurrence controls, authored for the 3p+1 review.
No candidate or previous checker is imported or executed.
Coefficients are exact elements of F_p[T]/T^cut, q=1+T.
"""
from math import comb, prod
from fractions import Fraction
from pathlib import Path
import json

# An X polynomial is a list of dictionaries representing coefficients in T.
def step(previous, current, n, p, cut):
    answer = [{}] + [dict(a) for a in current]
    correction = [(k, comb(n,k)%p) for k in range(1, min(n,cut-1)+1)]
    for power, coefficient in enumerate(previous):
        for tpower, a in coefficient.items():
            for k, b in correction:
                if b and tpower+k < cut:
                    answer[power][tpower+k] = (answer[power].get(tpower+k,0)+a*b)%p
    return [{k:a for k,a in row.items() if a} for row in answer]

def recurrence(N,p,cut):
    seq = [[{0:1}], [{},{0:1}]]
    for n in range(1,N): seq.append(step(seq[-2],seq[-1],n,p,cut))
    return seq

def terms(poly):
    return {(j,k):a for j,row in enumerate(poly) for k,a in row.items()}

def control(poly, slope, height, expected, p):
    pp = terms(poly) if isinstance(poly,list) else poly
    assert pp and min(Fraction(k)+j*slope for j,k in pp) == height
    leading = {(j,k):a for (j,k),a in pp.items() if Fraction(k)+j*slope==height}
    assert leading == {m:a%p for m,a in expected.items() if a%p}, (p, slope, height, leading, expected)
    higher = [Fraction(k)+j*slope-height for j,k in pp if Fraction(k)+j*slope>height]
    return {'height':str(height),'leading':[[j,k,a] for (j,k),a in sorted(leading.items())], 'next_gap':str(min(higher)) if higher else None}

def derivative(poly,p):
    return {(j-1,k):j*a%p for (j,k),a in terms(poly).items() if j and j*a%p}

def euler_minus_one(poly,p):
    return {(j,k):(j-1)*a%p for (j,k),a in terms(poly).items() if (j-1)*a%p}

def hull(poly):
    points=[(j,min(row)) for j,row in enumerate(poly) if row]
    result=[]
    for pt in points:
        while len(result)>1:
            a,b=result[-2:]
            if (b[1]-a[1])*(pt[0]-b[0])<(pt[1]-b[1])*(b[0]-a[0]):break
            result.pop()
        result.append(pt)
    return result

output=[]
for p in [5,7,11,13,17,19,23,29,31]:
    n=3*p+1; cut=4*p+4; ramification=p*(p-1)
    a=Fraction(2*p-1,2*p); g=Fraction(p+1,4)
    L=Fraction(5*p-3,2); W=L+p
    c=(-1)**((p+1)//2)%p; d=prod(range(1,p-1,2))%p
    assert W<ramification and W<cut
    seq=recurrence(n,p,cut)
    V,G,F=seq[n-2:n+1]
    checks={}
    checks['V_alpha']=control(V,a,L,{(2*p,(p-1)//2):d,(0,int(L)):-d},p)
    checks['V_one']=control(V,Fraction(1),L,{(0,int(L)):-d},p)
    checks['F_alpha']=control(F,a,n*a,{(n,0):1,(p+1,2*p-1):-3},p)
    checks['F_one']=control(F,Fraction(1),Fraction(3*p),{(p+1,2*p-1):-3,(2,3*p-2):-3*c},p)
    checks['F_gamma']=control(F,g,W,{(2,3*p-2):-3*c,(0,int(W)):-3*d},p)
    checks['Euler_alpha']=control(euler_minus_one(F,p),a,3*p-2+2*a,{(2*p+2,p-1):3*c,(2,3*p-2):-3*c},p)
    # The full derivative at alpha DOES NOT admit the often-tempting claimed
    # residual. Euler cancellation is essential and checked above.
    dp=derivative(F,p)
    checks['derivative_one']=control(dp,Fraction(1),Fraction(3*p-1),{(p,2*p-1):-3,(1,3*p-2):-6*c},p)
    checks['derivative_gamma']=control(dp,g,3*p-2+g,{(1,3*p-2):-6*c},p)
    expected_hull=[(0,int(W)),(2,3*p-2),(p+1,2*p-1),(3*p+1,0)]
    assert hull(F)==expected_hull,(p,hull(F))
    assert all(j%2==0 for j,row in enumerate(F) if row)
    assert 6*c%p and -3*c%p and -6*c%p and d
    disc=2*p*(3*p-2+a)+(p-1)*(3*p-1)+2*(3*p-2+g)
    assert disc==9*p*p+Fraction(p-7,2)
    output.append({'p':p,'status':'PASS','ramification_lower_bound':ramification,'truncation':cut,'alpha':str(a),'gamma':str(g),'L':str(L),'W':str(W),'outer_euler_perturbation_gap':str(W-(3*p-2+2*a)),'newton_vertices':expected_hull,'derivative_valuations':{'outer':str(3*p-2+a),'middle':str(3*p-1),'central':str(3*p-2+g)},'discriminant_valuation':str(disc),'checks':checks})
    print('PASS',p,expected_hull,flush=True)
Path(__file__).with_name('RECURRENCE_CHECKS.json').write_text(json.dumps({'status':'PASS','controls':output,'rigor_note':'Each tested weighted height is below W, and W<p(p-1)<=v(p), so reduction mod p discards only terms strictly above every tested height. The T truncation cut exceeds W. These are finite transcription controls; the infinite-prime statement requires the written symbolic proof.'},indent=2)+'\n')
