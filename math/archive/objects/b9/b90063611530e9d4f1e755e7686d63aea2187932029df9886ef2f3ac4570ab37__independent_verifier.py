#!/usr/bin/env python3
"""Independent N16 certificate audit: Python integers/Fractions only, no solver or NumPy."""
from fractions import Fraction
from math import isqrt,lcm
from pathlib import Path
import hashlib,json
BASE=Path(__file__).parent
N=16;Q=256;TERMS=8

def addmat(a,b,sign=1):return [[x+sign*y for x,y in zip(row,other)] for row,other in zip(a,b)]
def multiply(a,b):
    cols=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col)) for col in cols] for row in a]
def cproduct(a,b):
    ar,ai=a;br,bi=b
    return addmat(multiply(ar,br),multiply(ai,bi),-1),addmat(multiply(ar,bi),multiply(ai,br))
def csum(*a):
    out=([row[:] for row in a[0][0]],[row[:] for row in a[0][1]])
    for b in a[1:]:out=addmat(out[0],b[0]),addmat(out[1],b[1])
    return out

def normnum(pair):return max(sum(abs(x)+abs(y) for x,y in zip(r,i)) for r,i in zip(*pair))
def shapecheck(a,shape):
    if not shape:assert type(a) is int;return
    assert type(a) is list and len(a)==shape[0]
    for row in a:shapecheck(row,shape[1:])
def cycles(p):
    seen=set();out=[]
    for i in range(len(p)):
        if i in seen:continue
        c=[];j=i
        while j not in seen:seen.add(j);c.append(j);j=p[j]
        assert j==i;out.append(c)
    return out

def prescribed_orders():
    out=[]
    for axis in ('H','V'):
        for c in (0,1):
            for sign in (-1,1):
                p=[4*((x+sign*(2*y+c))%4)+y if axis=='H' else 4*x+(y+sign*(2*x+c))%4 for x in range(4) for y in range(4)]
                cc=cycles(p);tails=[min(cyc) for cyc in cc];sp=p[:]
                for j,t in enumerate(tails):sp[t]=p[tails[(j+1)%len(tails)]]
                assert sorted(sp)==list(range(N)) and len(cycles(sp))==1
                out.append(sp)
    return out

def fraction_record(q):return {'numerator':str(q.numerator),'denominator':str(q.denominator),'decimal_summary':float(q)}
def as_fraction(record):return Fraction(int(record['numerator']),int(record['denominator']))

def verify():
    raw=(BASE/'sources/DYADIC_AFFINE_CHART.json').read_bytes();chart=json.loads(raw)
    assert chart['dyadic_exponent']==60
    cr=chart['center_real'];ci=chart['center_imag'];vr=chart['directions_real'];vi=chart['directions_imag']
    for c in (cr,ci):shapecheck(c,[3,N,TERMS])
    for v in (vr,vi):shapecheck(v,[3,N,TERMS,Q])
    scale=1<<60;orders=prescribed_orders();poles=[d**N-1 for d in range(2,10)];assert all(p>0 for p in poles)
    common=lcm(*poles);den=scale*common;den3=den**3
    gs=[]
    for term,p in enumerate(orders):
        d=term+2;g=[[0]*N for _ in range(N)]
        for col in range(N):
            row=col
            for power in range(N):g[row][col]=d**(N-power)*(common//poles[term]);row=p[row]
        invp=[0]*N
        for j,i in enumerate(p):invp[i]=j
        # Exact left-inverse identity for every entry; no cyclic direction assumed silently.
        assert all(d*g[i][j]-g[invp[i]][j]==d*common*int(i==j) for i in range(N) for j in range(N))
        gs.append(g)
    bankr=[[int(i==j) for j in range(N)] for i in range(N)];banki=[[0]*N for _ in range(N)]
    for start in (0,4):
        for i in range(4):
            for j in range(4):
                phase=(i*j)%4;bankr[start+i][start+j]=(1,0,-1,0)[phase];banki[start+i][start+j]=(0,1,0,-1)[phase]
    bank=bankr,banki;assert normnum(bank)==4
    layers=[];directions=[]
    for l in range(3):
        parts=[]
        for center in (cr,ci):parts.append([[sum(center[l][i][j]*gs[j][i][k] for j in range(TERMS)) for k in range(N)] for i in range(N)])
        layers.append(tuple(parts));delta=[]
        for t in range(Q):
            parts=[]
            for directions_part in (vr,vi):parts.append([[sum(directions_part[l][i][j][t]*gs[j][i][k] for j in range(TERMS)) for k in range(N)] for i in range(N)])
            delta.append(tuple(parts))
        directions.append(delta)
    h0,h1,h2=layers;bh0=cproduct(bank,h0);prefix=cproduct(h1,bh0);suffix=cproduct(cproduct(h2,h1),bank);product=cproduct(h2,prefix)
    # Independently build each of the 256 derivative columns by the product rule.
    row_sums=[0]*Q;jacobian_digest=hashlib.sha256()
    for t in range(Q):
        deriv=csum(cproduct(directions[2][t],prefix),cproduct(cproduct(h2,directions[1][t]),bh0),cproduct(suffix,directions[0][t]))
        for i in range(N):
            for j in range(N):
                q=N*i+j;r=deriv[0][i][j]-(den3 if q==t else 0);im=deriv[1][i][j]
                row_sums[q]+=abs(r)+abs(im);jacobian_digest.update((str(r)+','+str(im)+';').encode())
    epsilon=Fraction(max(row_sums),den3)
    # Algebraic primitive-root enclosure, verified by integer inequalities.
    Z=1<<160;s0=isqrt(2*Z*Z);s1=s0+1;c=isqrt((2*Z+s0)*Z);d=isqrt((2*Z-s1)*Z)
    assert s0*s0<=2*Z*Z<s1*s1
    assert c*c<=(2*Z+s0)*Z<(c+1)*(c+1)
    assert d*d<=(2*Z-s1)*Z<(d+1)*(d+1)
    assert 0<2*s1<3*Z and c>0 and d>0 and c*c+d*d<4*Z*Z
    powers=[(1,0,1)]
    for e in range(1,16):
        a,b,v=powers[-1];powers.append((a*c-b*d,a*d+b*c,v*2*Z))
    residual_exact_approx=Fraction(0);worst_entry=None
    for i in range(N):
        for j in range(N):
            r,im,v=powers[(i*j)%16]
            err=Fraction(abs(product[0][i][j]*v-r*den3)+abs(product[1][i][j]*v-im*den3),den3*v)
            if err>residual_exact_approx:residual_exact_approx=err;worst_entry=[i,j]
    residual=residual_exact_approx+Fraction(120,Z)
    hs=[Fraction(normnum(h),den) for h in layers]
    ls=[]
    for l in range(3):
        ls.append(Fraction(max(sum(abs(directions[l][t][0][i][k])+abs(directions[l][t][1][i][k]) for t in range(Q) for k in range(N)) for i in range(N)),den))
    c2=8*(ls[2]*ls[1]*hs[0]+ls[2]*hs[1]*ls[0]+hs[2]*ls[1]*ls[0]);c3=12*ls[2]*ls[1]*ls[0]
    rho=Fraction(1,10**9);q=epsilon+c2*rho+c3*rho*rho;image=residual+q*rho
    margins=[];sensitivities=[]
    for l in range(3):
        for i in range(N):
            for j in range(TERMS):
                base=Fraction(max(abs(cr[l][i][j]),abs(ci[l][i][j])),scale)
                sensitivity=Fraction(sum(abs(vr[l][i][j][t])+abs(vi[l][i][j][t]) for t in range(Q)),scale)
                margin=base-rho*sensitivity;assert margin>0;margins.append(margin);sensitivities.append(sensitivity)
    assert epsilon<1 and q<1 and image<rho and len(margins)==384
    calc={'polydisk_radius':rho,'residual_upper_bound':residual,'center_derivative_defect_bound':epsilon,
          'quadratic_derivative_constant':c2,'cubic_derivative_constant':c3,'contraction_factor_bound':q,
          'image_radius_upper_bound':image,'physical_nonzero_margin':min(margins),'max_physical_direction_row_norm':max(sensitivities)}
    source=json.loads((BASE/'sources/EXACT_CONTRACTION_CERTIFICATE.json').read_text())
    for name,value in calc.items():assert value==as_fraction(source[name]),name
    assert hs==list(map(as_fraction,source['layer_matrix_bounds'])) and ls==list(map(as_fraction,source['layer_direction_bounds']))
    assert poles==source['fixed_pole_denominators']
    result={'status':'ACCEPTED_EXACT_N16_LOCAL_EXISTENCE','chart_sha256':hashlib.sha256(raw).hexdigest(),
      'arithmetic':'Python arbitrary-precision integers and fractions only; no numerical libraries or solver',
      'source_bounds_match_exactly':True,'full_complex_entry_equations':256,'physical_endpoint_guards':384,
      'chart_complex_dimension':256,'physical_parameter_dimension':384,'chart_injective_by_derivative_defect':True,
      'orders':orders,'fixed_pole_denominators':poles,'common_Green_denominator':str(common),'layer_denominator':str(den),
      'root_enclosure':{'Z':str(Z),'s0':str(s0),'s1':str(s1),'real_numerator':str(c),'imag_numerator':str(d),'denominator':str(2*Z),'power_l1_error_bound':fraction_record(Fraction(120,Z))},
      'worst_residual_entry':worst_entry,'jacobian_defect_columns_digest':jacobian_digest.hexdigest(),
      'layer_matrix_bounds':list(map(fraction_record,hs)),'layer_direction_bounds':list(map(fraction_record,ls)),
      'bounds':{name:fraction_record(value) for name,value in calc.items()},
      'all_endpoint_margins':list(map(fraction_record,margins)),
      'scope':'Full N16 fixed-model Fourier coefficient existence in the supplied exact affine chart; no larger-size lift or speedup'}
    (BASE/'INDEPENDENT_CERTIFICATE.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('ACCEPTED: independent exact bounds match the constructor fractions in all reported quantities')
    print(json.dumps({k:float(v) for k,v in calc.items()},sort_keys=True))

if __name__=='__main__':verify()
