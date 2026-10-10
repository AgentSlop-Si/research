"""Independent basis audit: three separate exact circuits versus closed-form DFT.
No OCR, numerics, or stochastic equality test. For each e_j, checks all N outputs.
"""
import argparse,json,time
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
from fused60 import make_fused60_plan,transform_fused
from fused120 import make_fused120_plan,transform_fused120
from wfta15 import make_wfta_plan,transform_wfta

def run(field=P,gen=GENERATOR,lengths=(120,240,480,960)):
    t0=time.time();summaries=[]
    for n in lengths:
        if (field-1)%n:continue
        p_new=make_fused120_plan(n,p=field,gen=gen)
        p_old=make_fused60_plan(n,p=field,gen=gen)
        p_alt=make_wfta_plan(n,p=field,gen=gen)
        root=n_root(n,field,gen)
        for j in range(n):
            v=[0]*n;v[j]=1
            y,_=transform_fused120(v,p_new)
            old,_=transform_fused(v,p_old)
            alt,_=transform_wfta(v,p_alt)
            step=pow(root,j,field);z=1
            for k in range(n):
                if y[k]!=z or old[k]!=z or alt[k]!=z:
                    raise AssertionError(dict(n=n,j=j,k=k,expected=z,new=y[k],old=old[k],alt=alt[k]))
                z=z*step%field
        rec=dict(n=n,field=field,unique_entries=n*n,comparisons=3*n*n,
                 exact_basis_agreement=True,root_order_n=n)
        summaries.append(rec)
        print('audit',field,n,'entries',n*n,'elapsed',round(time.time()-t0,2),flush=True)
    return dict(field=field,lengths=[x['n'] for x in summaries],rows=summaries,
                distinct_matrix_entries=sum(x['unique_entries'] for x in summaries),
                independent_exact_DFT_comparisons=sum(x['comparisons'] for x in summaries),
                elapsed_seconds=round(time.time()-t0,3))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--field',choices=('primary','alternate'),default='primary');parser.add_argument('--max-n',type=int,default=960)
    args=parser.parse_args()
    p,g=(P,GENERATOR) if args.field=='primary' else (ALT_P,ALT_GENERATOR)
    data=run(p,g,tuple(n for n in (120,240,480,960) if n<=args.max_n))
    filename='AUDIT_PHASE29_'+args.field.upper()+'.json'
    with open(filename,'w') as f:json.dump(data,f,indent=2)
    print(json.dumps({k:data[k] for k in ('distinct_matrix_entries','independent_exact_DFT_comparisons','elapsed_seconds')},indent=2))
