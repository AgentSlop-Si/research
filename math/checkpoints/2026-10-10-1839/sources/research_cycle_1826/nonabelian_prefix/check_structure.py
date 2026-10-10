#!/usr/bin/env python3
"""Fresh structure and direct-permutation checks; only new local code is imported."""
from itertools import permutations
from functools import lru_cache
from pathlib import Path
import json
from fresh_nonabelian_dp import permutation_group, quaternion, dihedral, subgroup_closure

OUT=Path(__file__).resolve().parent

def subgroups(table):
    n=len(table);seen={1};todo=[1]
    while todo:
        h=todo.pop()
        for g in range(n):
            if h>>g&1:continue
            k=subgroup_closure(h|(1<<g),table)
            if k not in seen:seen.add(k);todo.append(k)
    return sorted(seen,key=lambda h:(h.bit_count(),h))

def product(h,k,table):
    return sum(1<<x for x in {table[a][b] for a in range(len(table)) if h>>a&1 for b in range(len(table)) if k>>b&1})

def recurrence(table,subs):
    @lru_cache(None)
    def count(h):
        if h==1:return 1
        proper=[k for k in subs if k!=h and k&h==k]
        maximal=[k for k in proper if not any(k!=q and k&q==k for q in proper)]
        total=0
        for k in maximal:
            q=h.bit_count()//k.bit_count();fac=1
            for i in range(2,q+1):fac*=i
            total+=fac*count(k)**q
        return total
    return count((1<<len(table))-1)

def literal_stabilizer(s,table):
    return frozenset(g for g in range(len(table)) if {table[g][x] for x in s}==s)

def exhaustive(name,table):
    n=len(table);best=-1;count=0;hist={};failed=0
    for rest in permutations(range(1,n)):
        order=(0,)+rest;s=set();score=0;acc=1
        for x in order:
            s.add(x);h=literal_stabilizer(s,table);score+=len(h)-1
        hist[score]=hist.get(score,0)+n
        if score>best:best=score;count=n
        elif score==best:count+=n
    return dict(group=name,maximum=best,labeled_optimal_orders=count,score_histogram=hist,identity_first_orders=__import__('math').factorial(n-1))

results=[]
for name,data in [('S3',permutation_group(3)),('D8',dihedral(4)),('Q8',quaternion()),('M16',dihedral(8,5))]:
    labels,table=data;subs=subgroups(table)
    permutable=all(product(h,k,table)==product(k,h,table) for h in subs for k in subs)
    inverse=[next(g for g in range(len(table)) if table[x][g]==0) for x in range(len(table))]
    normal=all(all({table[table[g][x]][inverse[g]] for x in range(len(table)) if h>>x&1}=={x for x in range(len(table)) if h>>x&1} for g in range(len(table))) for h in subs)
    result=dict(group=name,subgroup_count=len(subs),pairwise_permutable=permutable,all_subgroups_normal=normal,formal_abelian_count_recurrence=recurrence(table,subs))
    if len(table)<=8:result['direct_permutation_check']=exhaustive(name,table)
    if name=='S3':
        # The cycle labels here are e, a=(12), b=(23), ba, ab, aba on {0,1,2}.
        elements=list(permutations(range(3)));idx={x:i for i,x in enumerate(elements)}
        e=idx[(0,1,2)];a=idx[(1,0,2)];b=idx[(0,2,1)]
        order=[e,a,b,table[b][a],table[a][b],table[table[a][b]][a]]
        masks=[];s=set();acc=1;contain=[]
        for x in order:
            s.add(x);h=literal_stabilizer(s,table);masks.append(sorted(h));acc=subgroup_closure(acc|sum(1<<z for z in h),table)
            contain.append(all(z in s for z in range(len(table)) if acc>>z&1))
        result['explicit_witness']=dict(symbols=['e','a','b','ba','ab','aba'],element_indices=order,stabilizer_indices=masks,stabilizer_orders=[len(h) for h in masks],accumulated_containment=contain)
    results.append(result)
expected=json.loads((OUT/'fresh_exact_results.json').read_text())
for item in results:
    dp=next(x for x in expected if x['group']==item['group'])
    if 'direct_permutation_check' in item:
        assert item['direct_permutation_check']['maximum']==dp['maximum']
        assert item['direct_permutation_check']['labeled_optimal_orders']==dp['labeled_optimal_orders']
    if item['pairwise_permutable'] or item['group']=='D8':
        assert item['formal_abelian_count_recurrence']==dp['labeled_optimal_orders']
assert results[0]['formal_abelian_count_recurrence']==216
assert results[0]['explicit_witness']['stabilizer_orders']==[1,2,1,2,1,6]
assert results[0]['explicit_witness']['accumulated_containment']==[True,True,True,False,False,True]
assert results[-1]['pairwise_permutable'] and not results[-1]['all_subgroups_normal']
(OUT/'structure_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
