"""Certify bit-reversal between all rank-one separated-generator stages.
Produces reproducible integer parameters, independent prime-field ranks, and
full-row Jacobian minor certificates at the generic-domination thresholds.
"""
from pathlib import Path
import json,subprocess,tempfile,random
import numpy as np
from multistage_jacobian import materialize,check_differences,rank_minor

HERE=Path(__file__).resolve().parent

def bitrev(n):
    m=(n-1).bit_length()
    assert (1<<m)==n
    return [int(format(i,f'0{m}b')[::-1],2) for i in range(n)]

def run_rank(J,p):
    nrows,ncols=J.shape
    with tempfile.TemporaryDirectory() as tmp:
        f=Path(tmp)/'Jacobian.bin'
        J.astype(np.int32).tofile(f)
        output=subprocess.check_output([str(HERE/'rankmod'),str(f),str(nrows),str(ncols),str(p)],text=True)
    line1,line2=output.splitlines()
    data=dict(part.split('=') for part in line1.split())
    return (int(data['rank']),int(data['det']), [int(x) for x in line2[7:].split(',')])

def single(n,t,p,seed=99017):
    perms=[bitrev(n)]*(t-1)
    M,J,pars,stages=materialize(n,t,perms,seed,p)
    check_differences(n,t,perms,pars,M,J,seed+197,p,num=30)
    rank,det,columns=run_rank(J,p)
    target=min(n*n,n+t*(4*n-6))
    assert rank==target,(n,t,p,rank,target)
    if n<=16:
        py_rank,pycols,pydet=rank_minor(J,p)
        assert py_rank==rank and pycols==columns
        if rank==n*n: assert det==pydet
    item={'n':n,'t':t,'prime':p,'rank':rank,'theoretical_upper':target,
          'codimension':n*n-rank,'full_dimensional':rank==n*n,
          'full_rank_minor_det_mod_prime':det if rank==n*n else None,
          'full_rank_minor_column_indices':columns if rank==n*n else None}
    return item,pars

if __name__=='__main__':
    all_results=[];full=[]
    for n in (8,16,32):
        tstop=n//4+1
        for t in range(1,tstop+1):
            r1,pars=single(n,t,12289)
            r2,_=single(n,t,65537)
            all_results.extend([r1,r2])
            print('n',n,'t',t,'rank',r1['rank'],'bound',r1['theoretical_upper'],flush=True)
            if t==tstop:
                witness={'n':n,'t':t,'permutation':bitrev(n),'seed_for_audit':99017,
                         'stages':[{k:v.tolist() for k,v in par.items()} for par in pars],
                         'certificates_by_field': {'12289':r1,'65537':r2}}
                (HERE/f'WITNESS_N{n}_T{t}.json').write_text(json.dumps(witness,indent=2)+'\n')
    (HERE/'BITREV_RESULTS.json').write_text(json.dumps(all_results,indent=2)+'\n')
