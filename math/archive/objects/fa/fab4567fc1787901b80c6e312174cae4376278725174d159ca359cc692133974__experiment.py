#!/usr/bin/env python3
"""Exact, bounded two-round synthetic-transform experiment. Python stdlib only.

This is a finite additive-circuit experiment, not the upstream layer compiler.
All complex coefficients are represented by one real component; the imaginary
component is an independent identical copy. No upstream code is executed.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def combine(a, b, sa=1, sb=1):
    out = {i: sa * v for i, v in a.items()}
    for i, v in b.items():
        out[i] = out.get(i, 0) + sb * v
        if not out[i]:
            del out[i]
    return out


def canonical(v):
    s = 1 if v[min(v)] > 0 else -1
    return tuple(sorted((i, int(s * a)) for i, a in v.items())), s


class DAG:
    def __init__(self, n):
        self.n = n
        self.forms = [{i: 1} for i in range(n)]
        self.gates = []
        self.known = {((i, 1),): i for i in range(n)}

    def add(self, a, b, sign=1):
        va = self.forms[a[0]]
        vb = self.forms[b[0]]
        assert not (va.keys() & vb.keys()), 'non-cancellation grammar'
        val = combine(va, vb, a[1], sign * b[1])
        key, out_sign = canonical(val)
        if key in self.known:
            return self.known[key], out_sign
        node = len(self.forms)
        self.forms.append(dict(key))
        self.gates.append((a[0], a[1] * out_sign, b[0], sign * b[1] * out_sign))
        self.known[key] = node
        return node, out_sign

    def value(self, ref):
        return {i: Q(ref[1] * v) for i, v in self.forms[ref[0]].items()}


def monomial_refs(record, exponent):
    r = len(record)
    out = [None] * r
    for k, (node, sign) in enumerate(record):
        q, j = divmod(k + exponent, r)
        out[j] = (node, sign * (-1 if q % 2 else 1))
    return out


def stage_refs(dag, data, t, r, stage):
    u = t >> stage
    out = list(data)
    routes = []
    for base in range(0, t, u):
        for k in range(u // 2):
            a = data[(base + k) * r:(base + k + 1) * r]
            b = data[(base + k + u // 2) * r:(base + k + u // 2 + 1) * r]
            plus = [dag.add(x, y) for x, y in zip(a, b)]
            minus = [dag.add(x, y, -1) for x, y in zip(a, b)]
            exponent = -(2 * r // u) * k
            out[(base + k) * r:(base + k + 1) * r] = plus
            out[(base + k + u // 2) * r:(base + k + u // 2 + 1) * r] = monomial_refs(minus, exponent)
            if exponent % (2 * r):
                routes.append({'record': base + k + u // 2, 'exponent_mod_2r': exponent % (2*r)})
    return out, routes


def stage_numerical(data, t, r, stage, truncate):
    """Separate numerical implementation used only for rounding tests."""
    u = t >> stage
    out = list(data)
    for base in range(0, t, u):
        for k in range(u // 2):
            lo, hi = (base+k)*r, (base+k+u//2)*r
            aa, bb = data[lo:lo+r], data[hi:hi+r]
            plus = [(a+b)/2 for a,b in zip(aa,bb)]
            minus = [(a-b)/2 for a,b in zip(aa,bb)]
            twiddled = [Q(0)]*r
            for j,v in enumerate(minus):
                q,h=divmod(j-(2*r//u)*k,r)
                twiddled[h]=(-1 if q%2 else 1)*v
            if truncate:
                plus=list(map(lambda v: Q(int(v)),plus))
                twiddled=list(map(lambda v: Q(int(v)),twiddled))
            out[lo:lo+r]=plus
            out[hi:hi+r]=twiddled
    return out


def fourier_reference(t, r):
    """Closed-form normalized synthetic DFT, stored in bit-reversed order."""
    ans=[{} for _ in range(t*r)]
    bits=t.bit_length()-1
    for j in range(t):
        slot=int(f'{j:0{bits}b}'[::-1],2)
        for k in range(t):
            exp=-(2*r//t)*j*k
            for coefficient in range(r):
                winding,destination=divmod(coefficient+exp,r)
                ans[slot*r+destination][k*r+coefficient]=Q(-1 if winding%2 else 1,t)
    return ans


def lower_bound_certificate(rows):
    """Exhaustive incidence certificate for all helpful 2/3-support sums.

    In a cancellation-free binary circuit for distinct 4-support outputs,
    every non-output node has size 2 or 3. A triple serving at most one output
    is unshared. If k outputs use a (3,1) split, there are at least k triples
    and 2N-k pair-use incidences. Pair reuse <=2 implies at least
    ceil((2N-k)/2) pair gates. Total >= N+k+ceil((2N-k)/2) >= 2N.
    """
    n=len(rows)
    counts={2: Counter(), 3: Counter()}
    output_keys=[]
    partitions=[]
    for row in rows:
        assert len(row)==4 and all(abs(v)==1 for v in row.values())
        key,_=canonical(row)
        output_keys.append(key)
        terms=sorted(row)
        for size in (2,3):
            for subset in combinations(terms,size):
                p,_=canonical({i:row[i] for i in subset})
                counts[size][p]+=1
        parts=[]
        for mate in terms[1:]:
            first=(terms[0],mate)
            second=tuple(i for i in terms if i not in first)
            pa,_=canonical({i:row[i] for i in first})
            pb,_=canonical({i:row[i] for i in second})
            parts.append((pa,pb))
        partitions.append(parts)
    unique_outputs=len(set(output_keys))==n
    max_pair=max(counts[2].values())
    max_triple=max(counts[3].values())
    valid=unique_outputs and max_pair<=2 and max_triple<=1
    cert={'distinct_outputs_up_to_sign':unique_outputs,
          'pair_patterns':len(counts[2]),'max_pair_output_incidence':max_pair,
          'triple_patterns':len(counts[3]),'max_triple_output_incidence':max_triple,
          'cancellation_free_addition_lower_bound':2*n if valid else None,
          'proof_inequalities':[
              {'triple_outputs':k,'bound':n+k+(2*n-k+1)//2} for k in range(n+1)]}
    return cert,partitions


def enumerate_pair_partitions(partitions):
    best=10**9
    best_assignment=None
    multiplicity=0
    histogram=Counter()
    for assignment in product(range(3),repeat=len(partitions)):
        pairs=set()
        for options,choice in zip(partitions,assignment):
            pairs.update(options[choice])
        size=len(pairs)
        histogram[size]+=1
        if size<best:
            best=size
            best_assignment=assignment
            multiplicity=1
        elif size==best:
            multiplicity+=1
    return {'assignments_examined':3**len(partitions), 'minimum_pairs':best,
            'optimal_assignments':multiplicity,
            'pair_count_histogram':dict(sorted(histogram.items()))},best_assignment


def candidate_from_partition(rows, partitions, choices):
    dag=DAG(len(rows))
    outs=[]
    for row,options,choice in zip(rows,partitions,choices):
        pairrefs=[]
        for pair in options[choice]:
            (i,si),(j,sj)=pair
            ref=dag.add((i,si),(j,sj))
            # Orient this canonical pair as in the target row.
            orient=int(row[i]/si)
            pairrefs.append((ref[0],ref[1]*orient))
        outs.append(dag.add(*pairrefs))
    assert [dag.value(o) for o in outs]==rows
    return dag,outs


def lift_dirty(dag, outs):
    """Emit actual invertible rational mixer and transparent scratch schedule.

    Each edge gets a role except that a binary gate reuses its first input
    role as its first outgoing role. Copy operations are additive shears;
    dirty values are never overwritten or assumed zero. Four complete mixer
    traversals and two copies/injections are explicitly charged.
    """
    n=dag.n
    outgoing=defaultdict(list)
    for g,(a,sa,b,sb) in enumerate(dag.gates,n):
        outgoing[a].append(('g',g,0))
        outgoing[b].append(('g',g,1))
    for o,(v,s) in enumerate(outs):
        outgoing[v].append(('o',o,0))
    roles={}
    nextrole=0
    mixer=[]
    inputs=[]
    for v in range(len(dag.forms)):
        edges=outgoing[v]
        assert edges
        if v<n:
            pivot=nextrole
            nextrole+=1
            inputs.append(pivot)
        else:
            a,sa,b,sb=dag.gates[v-n]
            pivot=roles[('g',v,0)]
            other=roles[('g',v,1)]
            assert pivot!=other
            if sa==-1:
                mixer.append(('neg',pivot,None,None))
            mixer.append(('add',pivot,other,Q(sb)))
        roles[edges[0]]=pivot
        for e in edges[1:]:
            new=nextrole
            nextrole+=1
            roles[e]=new
            mixer.append(('add',new,pivot,Q(1)))
    assert nextrole==len(dag.gates)+len(outs)
    scratch=nextrole
    dim=2*n+scratch
    state=[{i:Q(1)} for i in range(dim)]
    counts=Counter()
    word=[]
    peak_norm=Q(1)
    peak_denominator=1
    def emit(op,dst,src=None,weight=None):
        nonlocal peak_norm,peak_denominator
        counts[op]+=1
        word.append([op,dst,src,str(weight) if weight is not None else None])
        if op=='neg':
            state[dst]={i:-v for i,v in state[dst].items()}
        else:
            state[dst]=combine(state[dst],state[src],1,weight)
        peak_norm=max(peak_norm,sum(abs(v) for v in state[dst].values()))
        peak_denominator=max(peak_denominator,max((v.denominator for v in state[dst].values()),default=1))
    def mix(inverse=False):
        ops=reversed(mixer) if inverse else mixer
        for op,dst,src,w in ops:
            emit(op,2*n+dst,2*n+src if src is not None else None,
                 -w if inverse and w is not None else w)
    def inject(sign):
        for j,(v,s) in enumerate(outs):
            emit('add',n+j,2*n+roles[('o',j,0)],Q(sign*s,4))
    def copy(sign):
        for i,p in enumerate(inputs):
            emit('add',2*n+p,i,Q(sign))
    mix();inject(-1);mix(True);copy(1)
    mix();inject(1);mix(True);copy(-1)
    expected=[{i:Q(1)} for i in range(dim)]
    for j,ref in enumerate(outs):
        expected[n+j]=combine(expected[n+j],dag.value(ref),1,Q(1,4))
    assert state==expected,'dirty full-state map mismatch'
    serial=[sorted((i,str(v)) for i,v in row.items()) for row in state]
    digest=hashlib.sha256(json.dumps(serial,separators=(',',':')).encode()).hexdigest()
    return {'full_state_dimension':dim,'scratch_roles':scratch,
            'mixer_shears':sum(op[0]=='add' for op in mixer),
            'mixer_sign_flips':sum(op[0]=='neg' for op in mixer),
            'complete_word_shears':counts['add'],
            'complete_word_sign_flips':counts['neg'],
            'normalizing_quarter_coefficients':2*n,
            'general_scalar_multiplications':0,
            'shear_operand_reads':2*counts['add'],
            'shear_destination_writes':counts['add'],
            'signed_quarter_output_updates':2*n,
            'maximum_intermediate_row_l1_norm':str(peak_norm),
            'maximum_intermediate_coefficient_denominator':peak_denominator,
            'source_and_scratch_restoration':True,
            'all_input_and_dirty_basis_columns_checked':dim,
            'full_state_matrix_sha256':digest},word,serial


def run_case(t,r,start=0,exhaustive=False):
    assert t & (t-1)==0 and r & (r-1)==0 and (2*r)%t==0
    n=t*r
    dag=DAG(n)
    refs=[(i,1) for i in range(n)]
    routes=[]
    for s in (start,start+1):
        refs,route=stage_refs(dag,refs,t,r,s)
        routes.extend({'stage':s,**x} for x in route)
    rows=[dag.value(o) for o in refs]
    cert,partitions=lower_bound_certificate(rows)
    assert cert['cancellation_free_addition_lower_bound']==len(dag.gates)==2*n
    baseline_profile,baseline_word,baseline_matrix=lift_dirty(dag,refs)
    result={'t':t,'r':r,'start_stage':start,'real_scalar_inputs':n,
            'baseline_add_sub':len(dag.gates),'candidate_add_sub':len(dag.gates),
            'baseline_and_candidate_final_quarter_scales':n,
            'general_multiplications':0,'lower_bound_certificate':cert,
            'routing':{'signed_twiddle_records':routes,
                       'explicit_twiddle_coefficient_reads_if_materialized':len(routes)*r,
                       'explicit_twiddle_coefficient_writes_if_materialized':len(routes)*r,
                       'fused_signed_edge_count':2*len(dag.gates)+n,
                       'fixed_tape_routing_not_implemented':True},
            'dirty_lift':baseline_profile}
    artifacts={'baseline_word':baseline_word,'full_state_matrix':baseline_matrix,
               'normalized_target_matrix':[
                   sorted((i,str(v/4)) for i,v in row.items()) for row in rows]}
    if exhaustive:
        enumeration,assignment=enumerate_pair_partitions(partitions)
        candidate,candidate_out=candidate_from_partition(rows,partitions,assignment)
        cp,cw,cm=lift_dirty(candidate,candidate_out)
        assert cp['full_state_dimension']==baseline_profile['full_state_dimension']
        assert cm==baseline_matrix
        result['pair_partition_enumeration']=enumeration
        result['candidate_dirty_lift']=cp
        result['candidate_add_sub']=len(candidate.gates)
        artifacts['candidate_word']=cw
        artifacts['candidate_optimal_pair_assignment']=assignment
    # Independently check the full untruncated transform against its defining sum.
    full=DAG(n)
    fr=[(i,1) for i in range(n)]
    for s in range(t.bit_length()-1):
        fr,_=stage_refs(full,fr,t,r,s)
    matrix=[{i:v/t for i,v in full.value(o).items()} for o in fr]
    assert matrix==fourier_reference(t,r)
    result['closed_form_full_fourier_check']=True
    return result,artifacts


def rounding_counterexample():
    t,r=4,2
    # Coordinates in units of 2^-p for p=1, constants only, all in disk.
    x=[Q(2),Q(0),Q(1),Q(0),Q(1),Q(0),Q(0),Q(0)]
    staged=x
    exact=x
    for s in range(2):
        staged=stage_numerical(staged,t,r,s,True)
        exact=stage_numerical(exact,t,r,s,False)
    fused=[Q(int(v)) for v in exact]
    assert staged!=fused and staged[0]==0 and fused[0]==1
    return {'p':1,'inputs_in_grid_units':list(map(str,x)),
            'staged_rounded_outputs_in_grid_units':list(map(str,staged)),
            'fused_once_rounded_outputs_in_grid_units':list(map(str,fused)),
            'interpretation':'Multiply grid units by 1/2. DC differs: 0 versus 1/2.'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,default=Path(__file__).parent/'results')
    args=ap.parse_args();args.out.mkdir(exist_ok=True)
    cases=[]
    for t,r,s in [(4,2,0),(4,4,0),(4,8,0),(8,4,0),(8,4,1),
                  (8,8,0),(16,8,0),(16,8,1),(16,8,2),(16,16,0)]:
        result,artifacts=run_case(t,r,s,exhaustive=(t,r,s)==(4,2,0))
        cases.append(result)
        name=f't{t}_r{r}_s{s}'
        (args.out/(name+'_certificate.json')).write_text(json.dumps(artifacts,indent=2)+'\n')
    summary={'scope':'Finite exact cancellation-free signed-addition experiment; no frame-profile or asymptotic certificate.',
             'cases':cases,'rounded_interface_counterexample':rounding_counterexample()}
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for c in cases:
        print(f"t={c['t']}, r={c['r']}, stage={c['start_stage']}: "
              f"{c['baseline_add_sub']} baseline additions = restricted optimum; "
              f"dirty full dimension {c['dirty_lift']['full_state_dimension']} checked")
    print('All exact checks passed. No addition saving in the tested grammar.')


if __name__=='__main__':
    main()
