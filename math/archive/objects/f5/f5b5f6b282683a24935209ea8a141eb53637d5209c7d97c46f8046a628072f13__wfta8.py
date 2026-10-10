"""Exact positive-DFT8 diagonal codelet: 26 additions + 4 nonidentity field products.
Decomposition F8 = A8 diag(1,1,1,i,1,i,omega8*(1+i)/2,omega8*(1-i)/2) B8.
All pre/post maps have integral entries (add/sub only). Source: classical WFTA8 structure,
independently derived using even/odd decimation and two-point diagonalization.
"""

def prepare_diag8(omega8, p, counter=None, known_i=None):
    inv2 = (p+1)//2
    i = omega8*omega8%p if known_i is None else known_i
    cs=omega8*((1+i)%p)%p*inv2%p
    cd=omega8*((1-i)%p)%p*inv2%p
    if counter is not None:
        counter.muls+=4+(known_i is None)  # reuse supplied i when available
        counter.adds+=2
    return (1,1,1,i,1,i,cs,cd)

def before8(x,p,c):
    if len(x)!=8:raise ValueError('8 input coordinates required')
    s=[(x[j]+x[j+4])%p for j in range(4)]
    t=[(x[j]-x[j+4])%p for j in range(4)]
    c.adds+=8
    e0=(s[0]+s[2])%p; e1=(s[0]-s[2])%p
    e2=(s[1]+s[3])%p; e3=(s[1]-s[3])%p
    ts=(t[1]+t[3])%p;td=(t[1]-t[3])%p
    c.adds+=6
    return (e0,e2,e1,e3,t[0],t[2],ts,td)

def after8(z,p,c):
    if len(z)!=8:raise ValueError('8 scaled channels required')
    out=[0]*8
    out[0]=(z[0]+z[1])%p;out[4]=(z[0]-z[1])%p
    out[2]=(z[2]+z[3])%p;out[6]=(z[2]-z[3])%p
    u0=(z[4]+z[5])%p;u1=(z[4]-z[5])%p
    v0=(z[6]+z[7])%p;v1=(z[6]-z[7])%p
    out[1]=(u0+v0)%p;out[5]=(u0-v0)%p
    out[3]=(u1+v1)%p;out[7]=(u1-v1)%p
    c.adds+=12
    return out

def fft8_wfta(x,omega8,p,c):
    d=prepare_diag8(omega8,p)
    a=before8(x,p,c)
    z=[]
    for val,co in zip(a,d):
        if co!=1:
            val=val*co%p;c.muls+=1
        z.append(val)
    return after8(z,p,c)
