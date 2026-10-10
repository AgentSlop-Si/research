from math import comb, log


def constants(h: int):
    v = comb(h, 3)
    n0 = v**3
    i0 = 3*v*v
    d_nbr = comb(h-3, 3) + 3*(h-3)
    m = h**3
    W = 2*n0 + i0*(v*d_nbr + (h+1))
    Delta = 2*v*v*(v - 3*h*(h+1))
    p = (W-1).bit_length()
    Wstar = 1 << p
    S = Wstar*m - Delta
    lam = S / Wstar
    theta = log(lam) / log(m)
    return locals()

if __name__ == '__main__':
    c = constants(24)
    for k in ['h','v','n0','i0','d_nbr','m','W','Delta','p','Wstar','S','lam','theta']:
        print(f'{k} = {c[k]}')
    print('1-theta =', 1-c['theta'])
    assert c['v'] > 3*c['h']*(c['h']+1)
    assert 2**(c['p']-1) < c['W'] <= 2**c['p']
    assert c['Delta'] > 0
