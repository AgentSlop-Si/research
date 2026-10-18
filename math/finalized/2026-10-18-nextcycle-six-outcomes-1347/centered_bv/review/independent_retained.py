"""Fresh retained-operator audit using algebraic-root intervals only.

Membership is rebuilt from the literal row stencil, not production endpoints.
The candidate numerical kernel, its iterator, and its trig oracle are not imported.
"""
from independent_review import *

def divide(x,y,n=1):
    assert y[0]>0
    lows=[(a*U)//(b*n) for a in x for b in y]
    highs=[ceildiv(a*U,b*n) for a in x for b in y]
    return min(lows),max(highs)
def power(x,n):
    p=[v**n for v in x]
    if n%2==0 and x[0]<=0<=x[1]:p.append(0)
    d=1<<(Q*(n-1))
    return min(p)//d,ceildiv(max(p),d)
def complex_mul(x,y):
    return add(mul(x[0],y[0]),neg(mul(x[1],y[1]))),add(mul(x[0],y[1]),mul(x[1],y[0]))

def main():
    started=time.monotonic()
    saved=json.loads((SOURCE/'OUTPUT.json').read_text());src=saved['source'];est=saved['estimates'];out=saved['output']
    N=src['N'];M=4*N;m=M.bit_length()-1;D=5;s=D*m;h=16*s+1;t=2*h+2;L=M//4;q=M//(8*s)
    sine_roots=roots(2*M);phase_roots=roots(N);eta=Fraction(1,1<<(8*m));rounding=Fraction(1,1<<out['normalized_bits'])
    assert t==1764 and t<M and q==4
    amplitude={};counts={k:0 for k,_ in est['pairs']};rows=[];count=0
    def amp(r):
        if r not in amplitude:
            if r==0:value=(Fraction(2*(2*L+1)*U,M).__floor__(),Fraction(2*(2*L+1)*U,M).__ceil__())
            else:
                den=sine_roots[r][1]
                a=divide(sine_roots[((2*L+1)*r)%(2*M)][1],den,M)
                b=divide(sine_roots[((2*q+1)*r)%(2*M)][1],den,2*q+1)
                value=scale(mul(a,power(b,s)),2)
            assert max(abs(v) for v in value)<4*U
            amplitude[r]=value
        return amplitude[r]
    for ell,pair in enumerate(out['pairs']):
        total=((0,0),(0,0));l1=Fraction(0);terms=0
        phase=phase_roots[(-((N-1)//2)*ell)%N]
        for k,(a,b) in est['pairs']:
            # k-4 ell belongs to [-h,h+1] modulo M; direct original stencil.
            if ((k-4*ell+h)%M)>=t:continue
            r=(4*ell-k)%M;gain=amp(r)
            coefficient=(mul(gain,phase[0]),mul(gain,phase[1]))
            re=scale(add(scale(coefficient[0],a),scale(coefficient[1],-b)),1,1<<est['bits'])
            im=scale(add(scale(coefficient[0],b),scale(coefficient[1],a)),1,1<<est['bits'])
            total=(add(total[0],re),add(total[1],im));terms+=1;count+=1;counts[k]+=1
            l1+=Fraction(abs(a)+abs(b),1<<est['bits'])
        error=squared_error(pair,total,out['bits']+src['scale']);allowed=(eta*l1+rounding)**2
        assert error<=allowed,(ell,error,allowed)
        rows.append({'row':ell,'retained_terms':terms,'target_interval':total,'squared_error_upper':fj(error),'squared_allowed':fj(allowed)})
    assert count==21609==out['incidences'];assert set(counts.values())=={441}
    assert max(r['retained_terms'] for r in rows)==out['max_row_terms']
    report={'all_retained_operator_rows_checked':N,'independently_enumerated_incidences':count,
        'rows_per_supported_column':441,'max_row_terms':max(r['retained_terms'] for r in rows),
        'unique_amplitude_residues':len(amplitude),'all_interval_amplitude_caps_pass':True,
        'contract':'|2^-sigma Y_ell-(C Z)_ell| <= eta sum_k(|Re Z_k|+|Im Z_k|)+2^-b for every row',
        'source':'Independent 512-bit algebraic roots, literal stencil membership and exact interval sine ratios; no candidate numerical routines imported',
        'scope':'All incidences included in retained-operator assembly. Production coefficient records are transient and are not separately reproduced by this audit.',
        'seconds':time.monotonic()-started,'rows':rows}
    dump('INDEPENDENT_RETAINED_CHECKS.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
