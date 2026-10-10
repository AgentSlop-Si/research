import json,time,statistics
import numpy as np

from multi_view import SharedProjectedFourierStore,union_frequency_sets
from view_optimizer import AdaptiveSpectralOrganizer


def med_ms(fn,reps=5):
    vals=[]; last=None
    for _ in range(reps):
        t=time.perf_counter_ns(); last=fn(); vals.append((time.perf_counter_ns()-t)/1e6)
    return statistics.median(vals),last


def make_views(rng,n,C=8,q=32,clusters=1):
    view_bins={}
    per=C//clusters
    used=set()
    for g in range(clusters):
        common=[]
        while len(common)<3*q//4:
            x=int(rng.integers(n))
            if x not in used: common.append(x);used.add(x)
        for j in range(per):
            unique=[]
            while len(unique)<q-len(common):
                x=int(rng.integers(n))
                if x not in used: unique.append(x);used.add(x)
            view_bins[f'v{g*per+j}']=np.asarray(common+unique,dtype=np.intp)
    return view_bins


def setup(seed=9201,n=262144,r=256,C=8,q=32,clusters=1,updates=4096):
    rng=np.random.default_rng(seed)
    vb=make_views(rng,n,C,q,clusters)
    union,_,_=union_frequency_sets(vb,n)
    # Precomputed projected Fourier basis. Random coefficients are sufficient
    # for this planner benchmark; registration is benchmarked separately.
    proj=(rng.standard_normal((r,len(union)))+1j*rng.standard_normal((r,len(union)))).astype(np.complex128)
    c0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
    positions=np.sort(rng.choice(n,32,replace=False)).astype(np.intp)
    ops=[]
    for _ in range(updates):
        if rng.random()<.9:
            ops.append(('c',int(rng.integers(r)),complex(rng.standard_normal()*.005,rng.standard_normal()*.005)))
        else:
            ops.append(('p',int(rng.choice(positions)),complex(rng.standard_normal()*.005,rng.standard_normal()*.005)))
    return vb,union,proj,c0,positions,ops


def apply(st,op):
    kind,key,d=op
    if kind=='c':st.add_coefficient(key,d)
    else:st.add_point(key,d)


def due_names(t,scenario,C):
    if scenario=='sync':
        return [f'v{i}' for i in range(C)] if t%64==0 else []
    if scenario=='async':
        intervals=[1,2,4,8,16,32,64,128][:C]
        return [f'v{i}' for i,h in enumerate(intervals) if t%h==0]
    if scenario=='two_clusters':
        half=C//2
        if t%64==0:return [f'v{i}' for i in range(half)]
        if t%64==32:return [f'v{i}' for i in range(half,C)]
        return []
    if scenario=='shift':
        # first half synchronized, second half heterogeneous
        if t<=2048:return [f'v{i}' for i in range(C)] if t%64==0 else []
        intervals=[1,2,4,8,16,32,64,128][:C]
        return [f'v{i}' for i,h in enumerate(intervals) if (t-2048)%h==0]
    raise ValueError(scenario)


def run_one(scenario,mode,*,seed=9201,n=262144,r=256,C=8,q=32,updates=4096):
    clusters=2 if scenario=='two_clusters' else 1
    vb,union,proj,c0,positions,ops=setup(seed,n,r,C,q,clusters,updates)
    st=SharedProjectedFourierStore(n,union,proj,vb,c0,prepared_positions=positions,event_capacity=1024,promote_after=None)
    org=None
    if mode=='adaptive':
        org=AdaptiveSpectralOrganizer(st,sync_window=1,history_queries=20,min_history=4,
            replan_every=24,merge_threshold=1.07,min_sync=.45,immediate_guard=1.08)
    checksum=0.0
    snapshots=[]
    for t,op in enumerate(ops,1):
        if org is None: apply(st,op)
        else: apply(org,op)
        due=due_names(t,scenario,C)
        if due:
            if mode=='sequential':
                for name in due:checksum+=float(st.query(name)[0].real)
            elif mode=='oracle_batch':
                out=st.query_many(due)
                for name in due:checksum+=float(out[name][0].real)
            else:
                # Deliberately issue sequential calls. The organizer must infer
                # the grouping from recent behavior; no batch hint is supplied.
                for name in due:checksum+=float(org.query(name)[0].real)
        if t%256==0:
            st.compact()
            if org is not None and t in (1024,2048,3072,4096):
                snapshots.append((t,org.partition))
    extra={}
    if org is not None:
        extra={'partition':org.partition,'partition_snapshots':snapshots,
               'replans':org.stats.replans,'group_queries':org.stats.group_queries,
               'solo_queries':org.stats.solo_queries,'group_cache_hits':org.stats.group_cache_hits,
               'group_replays':org.stats.group_replays,'group_rebuilds':org.stats.group_rebuilds,
               'guarded_solo':org.stats.guarded_solo,'storage_bytes':org.storage_bytes}
    else: extra={'storage_bytes':st.storage_bytes}
    return checksum,extra


def bench_scenario(scenario,reps=5):
    rows={}
    for mode in ('sequential','oracle_batch','adaptive'):
        ms,last=med_ms(lambda:run_one(scenario,mode),reps)
        checksum,extra=last
        rows[mode]={'ms':ms,'checksum':checksum,**extra}
    ref=rows['sequential']['checksum']
    for mode in rows: rows[mode]['checksum_abs_diff']=abs(rows[mode]['checksum']-ref)
    rows['adaptive']['speedup_vs_sequential']=rows['sequential']['ms']/rows['adaptive']['ms']
    rows['adaptive']['slowdown_vs_oracle']=rows['adaptive']['ms']/rows['oracle_batch']['ms']
    rows['oracle_batch']['speedup_vs_sequential']=rows['sequential']['ms']/rows['oracle_batch']['ms']
    return rows

if __name__=='__main__':
    out={}
    for sc in ('sync','two_clusters','async','shift'):
        print('RUN',sc,flush=True)
        out[sc]=bench_scenario(sc,5)
        print(json.dumps(out[sc],indent=2),flush=True)
    open('benchmark_view_optimizer_results.json','w').write(json.dumps(out,indent=2))
