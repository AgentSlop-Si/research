#!/usr/bin/env python3
"""Fresh rational interval comparison. No supplied code is run or imported.
Usage: python pr622_moment_comparison_check.py CANDIDATE.zip PR623_EXPECTED.json PR624_EXPECTED.json
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json,sys,zipfile,hashlib
D=10**70

def outward(lo,hi):return F(lo.numerator*D//lo.denominator,D),F(-((-hi.numerator*D)//hi.denominator),D)

def logunit(x):
    # 1 <= x <= 2; atanh series through exponents 1..179.
    assert 1<=x<=2
    z=(x-1)/(x+1);z2=z*z;term=z;s=F(0)
    for j in range(90):s+=2*term/(2*j+1);term*=z2
    tail=2*term/(181*(1-z2))
    return s,s+tail

@lru_cache(None)
def logbounds(x):
    k=0
    while x>2:x/=2;k+=1
    a,b=logunit(x);c,d=logunit(F(2))
    return outward(a+k*c,b+k*d)

def expbounds(lo,hi):
    assert 0<=lo<=hi<F(1,100)
    def partial(t):
        term=F(1);s=term
        for j in range(1,26):term=term*t/j;s+=term
        first=term*t/26
        return s,first/(1-t/27)
    a,_=partial(lo);b,tail=partial(hi)
    return outward(a,b+tail)

def moment(profile,b):
    lo=hi=F(0)
    for rs,count in profile.items():
        r=int(rs);assert 0<r<73 and isinstance(count,int) and count>=0
        l,h=logbounds(F(73,r));e,f=expbounds(b*l,b*h)
        coeff=F(r*count,73*7168);lo+=coeff*e;hi+=coeff*f
    return lo-1,hi-1

def frac(x):return f'{x.numerator}/{x.denominator}'
def main():
    if len(sys.argv)!=4:raise SystemExit(__doc__)
    arc,p623,p624=map(Path,sys.argv[1:])
    z=zipfile.ZipFile(arc)
    claimed=json.loads(z.read('PR623_PR624_COMPARISON.json'))
    candidate=json.loads(z.read('pr622/candidate/PROFILE.json'))
    old=json.loads(z.read('pr622/baseline/EXPECTED.json'))['global']['global_profile']
    assert candidate==claimed['candidate']['profile']
    pinned=[]
    for f,label,expected in [(p623,623,'8fe7f49fac1d8fe96f8ecd19b51ce94be28288d0'),(p624,624,'ffc5ad2aa36839e24544bfc045fbe60f80ac270d')]:
        raw=f.read_bytes();git=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert git==expected
        data=json.loads(raw);row=next(r for r in claimed['sources'] if r['pr']==label)
        assert data['global']==row['global']
        pinned.append({'pr':label,'git_blob_sha1':git,'sha256':hashlib.sha256(raw).hexdigest(),'global':data['global']})
    c=F(claimed['candidate']['native_complex_lower']);cup=F(claimed['candidate']['native_complex_next'])
    b623=F(pinned[0]['global']['complex_lower']);b624=F(pinned[1]['global']['complex_lower'])
    assert b623>cup>c>b624
    delta={r:candidate.get(r,0)-old.get(r,0) for r in sorted(candidate.keys()|old.keys(),key=int)}
    delta={r:v for r,v in delta.items() if v}
    assert delta=={'1':1,'3':-4,'16':2,'21':-1}
    for profile in [candidate,old,*[r['global']['global_profile'] for r in pinned]]:
        assert sum(int(r)*n for r,n in profile.items())==520704
    assert 73*7168-520704==2560
    checks=[]
    specs=[('candidate lower',candidate,c,-1),('candidate next',candidate,cup,1),
           ('old lower',old,F('0.001638101302431117748332'),-1),('old next',old,F('0.001638101302431117748333'),1),
           ('PR623 reported lower',pinned[0]['global']['global_profile'],b623,-1),
           ('PR624 reported lower',pinned[1]['global']['global_profile'],b624,-1),
           ('candidate at PR623 lower',candidate,b623,1),
           ('PR624 at candidate lower',pinned[1]['global']['global_profile'],c,1)]
    for name,profile,b,sign in specs:
        lo,hi=moment(profile,b)
        assert hi<0 if sign<0 else lo>0,(name,lo,hi)
        checks.append({'case':name,'saving':frac(b),'moment_minus_one_lower':frac(lo),'moment_minus_one_upper':frac(hi),'strict_sign':sign})
    result={'status':'PASS_NARROW_PROFILE_COMPARISON','archive_sha256':hashlib.sha256(arc.read_bytes()).hexdigest(),
      'source_pins':pinned,'exact_profile_delta':delta,'rank_mass':520704,'live':7168,'dimension':73,'deficit':2560,
      'declared_saving_order':'PR623 > candidate > PR624','threshold_order':'PR623 > candidate > PR624 follows from strict moment signs and monotonicity',
      'pr623_lower_minus_candidate_lower':frac(b623-c),
      'checks':checks,'proof_parameters':{'log_atanh_terms':90,'exp_degree':25,'outward_decimal_grid_digits':70},
      'scope':'Profiles and exact moments only. Does not validate owner maps, source-provider semantics, full upstream replay, all-size algorithmic hypotheses, numerical stability, runtime, integer kappa, or originality.'}
    Path(__file__).with_name('pr622_moment_comparison_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 8 strict rational moment comparisons; 2 pinned Git blobs; 4 profile masses; threshold ordering PR623 > candidate > PR624')
if __name__=='__main__':main()
