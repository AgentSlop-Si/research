"""New read-only mathematical controls; no research module imports."""
import json
from pathlib import Path

p, n, omega, alpha, delta = 97, 8, 33, 33, 2
r = [49, 49, 65, 65, 11, 11, 72, 72]
h = [(r[j] - alpha * r[(j-delta) % n]) % p for j in range(n)]
def ev(a, z):
    return sum(c * pow(z, j, p) for j, c in enumerate(a)) % p

root_grid = []
for k in range(n):
    z = pow(omega, k, p)
    q = (1-alpha*pow(z,delta,p)) % p
    raw = ev(r,z)
    rational = ev(h,z)*pow(q,-1,p) % p
    assert raw == rational
    root_grid.append({'k':k,'z':z,'raw':raw,'rational':rational})
assert h == [1,1,0,0,0,0,0,0]
off_grid = {'z':0,'raw':ev(r,0),'rational':ev(h,0)}
assert off_grid['raw'] != off_grid['rational']

# This general two-defect example illustrates pole information loss. No
# assertion is made that it passes the nonzero-resultant / linear-gcd gate.
a = [1]+[0]*7
b = [(x+1) % p for x in a]
ha = [(a[j]-a[(j-1)%n]) % p for j in range(n)]
hb = [(b[j]-b[(j-1)%n]) % p for j in range(n)]
assert ha == hb == [1,96,0,0,0,0,0,0]
fa = [ev(a,pow(omega,k,p)) for k in range(n)]
fb = [ev(b,pow(omega,k,p)) for k in range(n)]
assert fa[1:] == fb[1:] and fa[0] != fb[0]
result = {'nonresonant_accepted_historical_witness': {'N':n,'p':p,'omega':omega,'alpha':alpha,'delta':delta,'r':r,'h':h,'root_grid_identity':root_grid,'off_grid_mismatch':off_grid}, 'general_two_defect_pole_information_loss': {'qualification':'Interface countercontrol only. Nonzero resultant and linear gcd are not claimed.','r1':a,'r2':b,'common_h':ha,'DFT1':fa,'DFT2':fb,'reduced_rational_function':'(1-z)/(1-z)=1','unrecovered_pole':'k=0; the two full transforms differ by N=8 there.'},'inherited_programs_executed':False}
out=Path(__file__).with_name('INTERFACE_CONTROL_RESULTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
