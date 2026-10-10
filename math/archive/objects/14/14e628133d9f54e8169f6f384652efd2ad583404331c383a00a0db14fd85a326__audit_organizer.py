"""Bounded independent v3 organizer audit; never modifies package sources."""
import sys, json, collections, time, statistics
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from multi_view import SharedProjectedFourierStore, union_frequency_sets
from view_optimizer import AdaptiveSpectralOrganizer

out={}
checks=0; maxerr=0.
for seed in range(12):
    rng=np.random.default_rng(8100+seed); n=(32,64,128)[seed%3]; r=(0,1,4,8)[seed%4]
    basis=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n)); c=rng.normal(size=r)+1j*rng.normal(size=r)
    vb={name:np.r_[np.arange(5),rng.integers(n,size=5)] for name in ('a','b','c','d')}
    union,_,_=union_frequency_sets(vb,n); proj=np.fft.fft(basis,axis=1)[:,union]
    for cap in (None,0,1,8,128):
        st=SharedProjectedFourierStore(n,union,proj,vb,c,event_capacity=cap,prepared_positions=[0,n-1],promote_after=None)
        org=AdaptiveSpectralOrganizer(st,history_queries=10,min_history=2,replan_every=4,replan_min_updates=3,replan_max_updates=12,probe_period_updates=15,probe_window_updates=8,merge_threshold=1.01,min_sync=.3)
        x=c@basis
        for t in range(160):
            d=complex(rng.normal()*.1,rng.normal()*.1)
            if r and t%2:
                i=t%r;org.add_coefficient(i,d); x+=d*basis[i]
            else:
                j=t%n;org.add_point(j,d);x[j]+=d
            if t%3==0:
                names=list(vb) if t<75 else [name for name in vb if rng.random()<.6]
                if t%2: got=org.query_many(names)
                else:got={name:org.query(name) for name in names}
                ref=np.fft.fft(x)
                for name,arr in got.items():
                    maxerr=max(maxerr,float(np.max(np.abs(arr-ref[vb[name]]))));checks+=1
                    np.testing.assert_allclose(arr,ref[vb[name]],atol=2e-9,rtol=3e-11)
                    arr[:]=12345
                    np.testing.assert_allclose(org.query(name),ref[vb[name]],atol=2e-9,rtol=3e-11)
            if t%11==0:org.compact()
            if t%17==0:org.replan()
out['numerical_sweep']={'checked_outputs':checks,'max_absolute_error':maxerr,'passed':True,'note':'60 workloads, each 160 updates, bounded/unbounded history, rank zero, duplicate bins, replay/rebuild/compact, merge/split, sequential/batch and returned-array mutation'}

def simple(C=2,q=1,r=2):
    vb={str(i):list(range(q)) for i in range(C)}
    st=SharedProjectedFourierStore(max(8,q),list(range(q)),np.ones((r,q)),vb,promote_after=None)
    org=AdaptiveSpectralOrganizer(st,min_history=2,probe_window_updates=4,replan_every=100000,replan_min_updates=100000)
    for name in vb:org.history[name].extend([0,1])
    org.replan()
    return st,org

class CountDeque(collections.deque):
    visited=0
    def __iter__(self):
        for row in super().__iter__():self.visited+=1;yield row
    def __reversed__(self):
        for row in super().__reversed__():self.visited+=1;yield row

st,org=simple()
for _ in range(10000):org.add_coefficient(0,1)
org.query('0');st.events=CountDeque(st.events);org.add_coefficient(0,1);arr=org.query('0')
out['group_suffix_scan']={'H':1,'retained_prior_events':10000,'visited_events':st.events.visited,'correct':bool(arr[0]==10001)}

out['cache_hit_copy_counts']=[]
for C in (2,8,32):
    st,org=simple(C,8);org.query('0')
    old={n:st.views[n].cached for n in st.views}
    org.query('0')
    replaced=sum(st.views[n].cached is not old[n] for n in st.views)
    out['cache_hit_copy_counts'].append({'consumers':C,'q_each':8,'requested_consumers':1,'member_cache_arrays_replaced':replaced,'complex_values_copied_on_one_hit':8*replaced+8,'complex_values_copied_C_query_burst':8*C*replaced+8*C})

out['update_replan_cost']=[]
for C in (4,8,16,32):
    st=SharedProjectedFourierStore(8,[0],np.ones((1,1)),{str(i):[0] for i in range(C)},promote_after=None)
    org=AdaptiveSpectralOrganizer(st,min_history=2,probe_window_updates=1)
    org.add_coefficient(0,1)
    for h in org.history.values():h.extend([0,1])
    count=[0];original=org._cluster_metrics
    def counted(m):count[0]+=1;return original(m)
    org._cluster_metrics=counted
    t=time.perf_counter_ns();org.add_coefficient(0,1);ms=(time.perf_counter_ns()-t)/1e6
    out['update_replan_cost'].append({'consumers':C,'update_ms':ms,'cluster_metric_calls':count[0],'replans_inside_update':org.stats.replans})

st,org=simple();before=len(org.stats.partitions)
for _ in range(200):org.replan()
out['partition_history']={'before':before,'after_200_replans':len(org.stats.partitions),'bounded':False,'included_in_storage_bytes':False}

st,org=simple();st.drop_view('1')
try:org.query('0');out['drop_view']='no error'
except Exception as e:out['drop_view']=type(e).__name__+': '+str(e)
st,org=simple();st.add_view('new',[0])
try:org.replan();out['add_view_then_replan']='no error'
except Exception as e:out['add_view_then_replan']=type(e).__name__+': '+str(e)

rng=np.random.default_rng(744);n=32;r=3;bins=[0,2,5,9]
proj=rng.normal(size=(r,4))+1j*rng.normal(size=(r,4)); c=rng.normal(size=r)+1j*rng.normal(size=r)
st=SharedProjectedFourierStore(n,bins,proj,{'a':bins,'b':bins},c,promote_after=None)
for t in range(500):
    st.add_coefficient(t%r,complex(rng.normal(),rng.normal()));st.query('a')
st.query('b')
out['same_version_cache_roundoff']={'same_version':st.views['a'].version==st.views['b'].version,'bitwise_identical':bool(np.array_equal(st.views['a'].cached,st.views['b'].cached)),'max_absolute_difference':float(np.max(np.abs(st.views['a'].cached-st.views['b'].cached)))}
print(json.dumps(out,indent=2))
