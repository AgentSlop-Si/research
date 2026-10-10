"""Explore exact gamma-resultant polynomial of reciprocal 4-sparse Hankel gates.

This is an optional mathematical audit, not part of the certified runtime.
"""
from resultant_gate import det_mod, interp_newton, strip_trivial_factors, eval_poly
from reciprocal_union import det_pencil_samples
from annihilator_engine import Work,RecurrenceGreen,dense_from_shift_defects,direct_one_frequency,batch_inverse_nonzero
import random,json,sys,time


def res_at(T,w,p,co,s=4):
    a=det_pencil_samples(T,w,0,p,co,s)
    b=det_pencil_samples(T,w,1,p,co,s)
    d=s+1
    aa=list(reversed(a+[0]*(d+1-len(a))))
    bb=list(reversed(b+[0]*(d+1-len(b))))
    syl=[]
    for c in (aa,bb):
        for t in range(d):
            syl.append([0]*t+c+[0]*(d-1-t))
    return det_mod(syl,p,co)


def find_resultant_coeff(T,p,s=4,co=None):
    bound=(s+1)**2*(2*s+1)
    if co is None:co=Work()
    t0=time.monotonic()
    vals=[res_at(T,w,p,co,s) for w in range(bound+1)]
    coef=interp_newton(vals,p,co)
    for w in (bound+1,bound+2):
        assert eval_poly(w,coef,p,co)==res_at(T,w,p,co,s)
    red,z,o=strip_trivial_factors(coef,p,co)
    return {'degree':len(coef)-1,'zero_factor':z,'one_factor':o,
            'reduced_degree':len(red)-1,'palindromic':red==red[::-1],
            'ops':co.arithmetic(),'elapsed_s':time.monotonic()-t0},coef,red


def run():
    p=2013265921;n=64;eng=RecurrenceGreen(n,p,31)
    rng=random.Random(21025)
    results=[]
    for mode in ('two-factor','generic','three-factor'):
        h=[0]*n;h[3]=7;h[35]=11
        if mode=='two-factor':
            r=dense_from_shift_defects(dense_from_shift_defects(h,13,17,p),29,29,p)
        elif mode=='three-factor':
            r=dense_from_shift_defects(dense_from_shift_defects(dense_from_shift_defects(h,5,17,p),11,29,p),19,41,p)
        else:r=[rng.randrange(1,p) for _ in range(n)]
        R=[direct_one_frequency(r,eng.powers[k],p) for k in range(16)]
        if not all(R):continue
        T=batch_inverse_nonzero(R,p)
        out,_,_=find_resultant_coeff(T,p)
        out['mode']=mode;results.append(out)
        print(out,flush=True)
    with open('RESULTANT_PATTERN.json','w') as f:json.dump(results,f,indent=2)
if __name__=='__main__':run()
