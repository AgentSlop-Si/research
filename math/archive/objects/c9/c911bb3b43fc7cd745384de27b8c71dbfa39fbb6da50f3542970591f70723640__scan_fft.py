"""Literal full-array scan realization of radix-two DFT, not a speedup.

Two ordinary scans per butterfly layer, with all preparation and routing
explicit. Counter includes arithmetic even at reset/identity coefficients.
"""
from collections import Counter


class Gates:
    def __init__(self,f):self.f=f;self.zero=f.zero;self.one=f.one;self.count=Counter()
    def add(self,a,b):self.count['add']+=1;return self.f.add(a,b)
    def sub(self,a,b):self.count['sub']+=1;return self.f.sub(a,b)
    def mul(self,a,b):self.count['mul']+=1;return self.f.mul(a,b)
    def neg(self,a):self.count['neg']+=1;return self.f.neg(a)
    def inv(self,a):self.count['inverse']+=1;return self.f.inv(a)


def scan(c,x,a,b,forward=True):
    n=len(x);y=[c.zero]*n
    order=range(n) if forward else range(n-1,-1,-1)
    previous=None
    for i in order:
        y[i]=c.mul(b[i],x[i])
        if previous is not None:y[i]=c.add(y[i],c.mul(a[i],y[previous]))
        previous=i
    return y


def scan_fft(field,n,q,values):
    if n<2 or n&(n-1) or len(values)!=n:raise ValueError('dyadic N>=2 required')
    c=Gates(field);powers=[field.one]
    for _ in range(1,n):powers.append(c.mul(powers[-1],q))
    if c.mul(powers[-1],q)!=field.one or powers[n//2]==field.one:
        raise ValueError('primitive Nth root required')
    minus_two=c.neg(c.add(field.one,field.one))
    minus_half=c.inv(minus_two)
    depth=n.bit_length()-1
    rev=[0]*n
    for i in range(1,n):rev[i]=(rev[i>>1]>>1)|((i&1)<<(depth-1))
    data=[values[rev[i]] for i in range(n)]
    before=dict(c.count);layers=[];length=2
    while length<=n:
        half=length//2;stride=n//length
        permutation=[];a_up=[];b_up=[];a_low=[];b_low=[]
        for start in range(0,n,length):
            for j in range(half):
                permutation.extend((start+j,start+j+half))
                a_up.extend((minus_half,field.zero))
                b_up.extend((field.one,c.mul(minus_two,powers[j*stride])))
                a_low.extend((field.zero,field.one));b_low.extend((field.one,field.one))
        routed=[data[j] for j in permutation]
        upper=scan(c,routed,a_up,b_up,False)
        lower=scan(c,upper,a_low,b_low,True)
        data=[field.zero]*n
        for i,j in enumerate(permutation):data[j]=lower[i]
        layers.append(dict(length=length,one_way_scans=2,routing_copies=2*n,
                           scan_output_writes=2*n,coefficient_values=4*n))
        length*=2
    return data,dict(field_operations=dict(c.count),initial_preparation=before,
                     one_way_scans=2*depth,layers=layers,bit_reversal_copies=n,
                     full_output_writes=n,root_supplied=True,
                     note='Exact ordinary FFT refactored into scans; deliberately not a speedup.')


def inverse_scan_matrix(f,a,b,forward=True):
    n=len(a);out=[[f.zero]*n for _ in range(n)]
    for i in range(n):
        if b[i]==f.zero:raise ValueError('singular scan')
        inv=f.inv(b[i]);out[i][i]=inv
        neighbor=i-1 if forward else i+1
        if 0<=neighbor<n:out[i][neighbor]=f.neg(f.mul(a[i],inv))
    return out


def inverse_support_lower_bound(n,ordinary=True):
    if n<2:raise ValueError('N>=2 required')
    return (n-1).bit_length()+(1 if ordinary else 0)
