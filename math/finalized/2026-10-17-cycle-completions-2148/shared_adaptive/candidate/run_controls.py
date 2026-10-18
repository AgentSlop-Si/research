#!/usr/bin/env python3
"""Fresh producer controls; built-in * used only here as an endpoint oracle.
No historical control program is imported or executed.
"""
import copy, hashlib, json, pathlib, random, zipfile
from shared_dispatcher import (Dispatcher, Elementary, native_plan, compile_sparse,
    check_structure, check_execution, evaluate_shared, split_blocks, slot_width,
    pack, assemble, digest)
HERE=pathlib.Path(__file__).resolve().parent
SEED=202610172130


def case(label,a,b,**kwargs):
    d=Dispatcher(**kwargs);out=d.multiply(a,b)
    assert out==a*b,(label,a,b)
    result={'label':label,'input_bits':[abs(a).bit_length(),abs(b).bit_length()],
            'output_sha256':digest(out),**d.summary()}
    print(label,result['input_bits'],result['dispatcher'],result['backend']['charged_bit_work'],flush=True)
    return result,d


def main():
    rng=random.Random(SEED);results={'seed':SEED,'products':[],'negative_controls':[],'width_controls':0}
    for label,a,b in [('zero',0,1<<10000),('signs',-19,23),('one',1,1),('shifted-core',-(2051<<131072),4099<<65536)]:
        row,_=case(label,a,b);results['products'].append(row)
    for n in [1023,1024,1025,2048,4096,8192]:
        for replicate in range(2):
            a=rng.getrandbits(n)|(1<<(n-1))|1;b=rng.getrandbits(n)|(1<<(n-1))|1
            if replicate:a=-a
            row,_=case('random-dense-'+str(n)+'-'+str(replicate),a,b);results['products'].append(row)
    # Large legal odd perturbation. Its rank and binary-block alignment are actual.
    P=native_plan(17,Elementary());E=((1<<17)+P.block_bits-1)//P.block_bits*P.block_bits
    C=(1<<11)+1;X=(C<<E)+P.point
    assert X.bit_length().bit_length()-1==17 and X&1
    row,d=case('distinct-odd-shared-family',X,X);results['products'].append(row)
    assert d.stats['sparse_shared']==1 and d.stats['calls']==1
    cert=d.certificates[0];blocks=(split_blocks(X,P.block_bits,Elementary()),)*2
    record=cert['execution'];children=[]
    for r in record['rows']:
        left=[0]*len(blocks[0]);right=[0]*len(blocks[1]);conv=[0]*(2*len(left)-1)
        for i,v in r['input_terms'][0]:left[i]=v
        for i,v in r['input_terms'][1]:right[i]=v
        for i,v in r['product_terms']:conv[i]=v
        if r['slot_bits']:
            U=pack(left,r['slot_bits'],Elementary());V=pack(right,r['slot_bits'],Elementary())
            assert pack(conv,r['slot_bits'],Elementary())==U*V
            children.append((U,V))
    assert len(set(children))==2*P.rank-1
    assert sum(U&1 for U,V in children)>=P.rank-1
    results['positive_family']={'rank':17,'exponent':E,'point':P.point,'core_constant':C,
        'input_bits':X.bit_length(),'distinct_child_pairs':len(set(children)),
        'odd_children':sum(U&1 for U,V in children),'actual_child_bits':sorted({abs(U).bit_length() for U,V in children}),
        'large_operand_multiplications':sum(max(p,q)>P.block_bits*2 for p,q in d.E.products),
        'shared_dag':record,'certificate':cert['certificate'],'summary':d.summary()}
    # Multi-block generic sparse support, arbitrary legal values (not an advised formula).
    for r in [12,14,16]:
        plan=native_plan(r,Elementary());s=plan.block_bits
        K=((1<<r)+s-1)//s
        positions=[0,2,K//2,K]
        aa=sum((rng.randrange(1,1<<s)|1)<<(s*k) for k in positions)
        bb=sum((rng.randrange(1,1<<s)|1)<<(s*k) for k in [0,3,K//2+1,K])
        row,dd=case('four-arbitrary-blocks-r'+str(r),aa,-bb);results['products'].append(row)
        assert dd.stats['sparse_shared']==1 and dd.stats['calls']==1
    # Repeated normalized nonconstant blocks: common contents 3 and 5, one product node.
    plan=native_plan(15,Elementary());s=plan.block_bits;K=((1<<15)+s-1)//s
    F=plan.point+2
    A=3*F+(9*F<<(K*s));B=5*F+(15*F<<((K+1)*s))
    row,dd=case('common-content-repeated-polynomial',A,B);results['products'].append(row)
    c=dd.certificates[0]['certificate'];ex=dd.certificates[0]['execution']
    assert [x['common_content'] for x in c['sides']]==[3,5]
    assert len(c['leaves'])==1 and len(c['product_nodes'])==1 and ex['memo_hits']>0
    results['common_content']={'contents':[3,5],'leaf_count':1,'product_node_count':1,
        'edge_count':len(c['edges']),'memo_hits':ex['memo_hits'],'memo_misses':ex['memo_misses']}
    # Nonconstant polynomial vanishes at a node: certified zero width and no packed call.
    Z=plan.point+(plan.point<<(K*s))
    row,zz=case('zero-nodal-row',Z,Z);results['products'].append(row)
    assert any(r['bound']==0 and r['slot_bits']==0 for r in zz.certificates[0]['execution']['rows'])
    # Recognizer threshold adversary: a single additional occupied block forces exact fallback.
    dense_near=A+(1<<s)+(1<<(2*s))+(1<<(3*s))
    row,nn=case('fifth-block-negative-control',dense_near,B);results['products'].append(row)
    assert nn.stats['dense_fallback']>=1
    # Equality adversary: changing one primitive leaf must create another DAG leaf.
    different=A+(1<<(K*s))
    row,mm=case('near-equal-polynomial-control',different,B);results['products'].append(row)
    assert len(mm.certificates[0]['certificate']['leaves'])>1
    # Same input through forced dense policy: all elementary backend charges paid.
    p=native_plan(14,Elementary());e=((1<<14)+p.block_bits-1)//p.block_bits*p.block_bits
    x=(513<<e)+p.point
    shared,ds=case('cost-comparison-shared',x,x)
    dense,db=case('cost-comparison-dense',x,x,force_dense=True)
    assert shared['output_sha256']==dense['output_sha256']
    results['cost_comparison']={'shared':shared,'dense':dense,
        'charged_work_ratio_dense_over_shared':dense['backend']['charged_bit_work']/shared['backend']['charged_bit_work'],
        'claim':'deterministic primitive-charge comparison, not timing or asymptotic fitting'}
    # Structural certificate tampering. Every mutation has a fixed rejection target.
    original=cert['certificate'];execution=cert['execution']
    def reject_structure(label,mutator):
        bad=copy.deepcopy(original);mutator(bad)
        assert not check_structure(bad,blocks,P,Elementary(),4),label
        results['negative_controls'].append(label)
    reject_structure('missing-input-support',lambda c:c['sides'][0]['terms'].pop())
    reject_structure('wrong-common-content',lambda c:c['sides'][0].__setitem__('common_content',2))
    reject_structure('changed-leaf-coefficient',lambda c:c['leaves'][0].__setitem__(0,c['leaves'][0][0]+1))
    reject_structure('wrong-product-edge-scale',lambda c:c['edges'][0].__setitem__(2,c['edges'][0][2]+1))
    reject_structure('wrong-point',lambda c:c.__setitem__('point',c['point']+2))
    reject_structure('wrong-node-window',lambda c:c['nodes'].__setitem__(0,c['nodes'][0]-1))
    reject_structure('wrong-outer-offset',lambda c:c['sides'][0].__setitem__('outer_shift',1))
    def reject_execution(label,mutator):
        bad=copy.deepcopy(execution);mutator(bad)
        assert not check_execution(original,bad,blocks,P,Elementary()),label
        results['negative_controls'].append(label)
    reject_execution('wrong-slot-width',lambda e:e['rows'][0].__setitem__('slot_bits',e['rows'][0]['slot_bits']-8))
    reject_execution('wrong-envelope',lambda e:e['rows'][0].__setitem__('bound',e['rows'][0]['bound']+1))
    reject_execution('wrong-convolution',lambda e:e['rows'][0]['product_terms'][0].__setitem__(1,e['rows'][0]['product_terms'][0][1]+1))
    reject_execution('wrong-interpolation-output',lambda e:e['output_terms'][0].__setitem__(1,e['output_terms'][0][1]+1))
    changed_blocks=(list(blocks[0]),list(blocks[1]));changed_blocks[0][1]=1
    assert not check_structure(original,changed_blocks,P,Elementary(),4)
    results['negative_controls'].append('certificate-replay-on-changed-input')
    for q in range(1,41):
        for delta in [-1,0,1]:
            B=(1<<(8*q-1))+delta;w,b=slot_width(1,1,B,Elementary())
            assert w==8*(((2*B).bit_length()+7)//8) and (1<<w)>2*b
            results['width_controls']+=1
    # Outer shift is represented and verified at the row/compiler API, even though
    # root power-of-two normalization normally removes it from integer dispatch.
    directA=[0,0,3*F,0,9*F];directB=[0,5*F,0,15*F]
    cc=compile_sparse(directA,directB,plan,Elementary(),4)
    assert [side['outer_shift'] for side in cc['sides']]==[2,1]
    assert check_structure(cc,(directA,directB),plan,Elementary(),4)
    oo,ee=evaluate_shared(cc,(directA,directB),plan,Elementary())
    assert check_execution(cc,ee,(directA,directB),plan,Elementary())
    results['outer_shift_control']={'shifts':[2,1],'output_support':sorted(oo)}
    # Source provenance: read bytes only, never import/execute historical files.
    # Portable provenance I/O only; mathematical controls above are unchanged.
    pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
    assert pins['archive_sha256']=='936bf7706643fc130c7cb1197848bf1c2bf193be533cdc01e6c3b265351c1581'
    for name,digest in pins['source_members'].items():
        assert hashlib.sha256((HERE/'source'/name).read_bytes()).hexdigest()==digest
    assert hashlib.sha256((HERE/'shared_dispatcher.py').read_bytes()).hexdigest()==pins['new_producer_sha256']
    for role,digest in pins['accepted_documents'].items():
        assert hashlib.sha256((HERE/pins['public_accepted_document_paths'][role]).read_bytes()).hexdigest()==digest
    results['totals']={'complete_products':len(results['products'])+2,
        'negative_certificate_controls':len(results['negative_controls']),'width_controls':results['width_controls'],
        'source_child_products_checked':len(children),'all_passed':True}
    (HERE/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    (HERE/'EXAMPLE_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps(results['totals'],indent=2),flush=True)

if __name__=='__main__':main()
