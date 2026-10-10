"""Run against either original or hardened module directory; no source writes."""
import collections
import json
import platform
import sys
from pathlib import Path
import numpy as np
import scipy

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from arbitrary_output import ArbitraryBinsDFTPlan, AutoOutputPlan, ProductiveProjectionPlanner
from multi_view import SharedProjectedFourierStore, union_frequency_sets

class CountDeque(collections.deque):
    visited=0
    def __iter__(self):
        for row in super().__iter__():
            self.visited+=1
            yield row
    def __reversed__(self):
        for row in super().__reversed__():
            self.visited+=1
            yield row

def backing(a):
    while isinstance(a.base,np.ndarray): a=a.base
    return a.nbytes

out={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}}
out['shared_history']=[]
for retained in (10,1000,100000):
    st=SharedProjectedFourierStore(8,[0],np.ones((2,1)),{'v':[0]})
    for _ in range(retained): st.add_coefficient(0,1)
    st.query('v');st.events=CountDeque(st.events);st.add_coefficient(0,1)
    got=st.query('v')
    out['shared_history'].append({'retained_prior_events':retained,'H':st.views['v'].backlog,
        'visited_events':st.events.visited,'storage_bytes':st.storage_bytes,'correct':bool(got[0]==retained+1)})

n=65536;full=np.ones(n,np.complex128);proj=full[:4][None,:]
st=SharedProjectedFourierStore(n,[0,1,2,3],proj,{'v':[0]},[1])
out['projection_retention']={'visible_bytes':st.projection.nbytes,'backing_bytes':backing(st.projection),'owns':bool(st.projection.flags.owndata)}
full[:]=100;st.add_coefficient(0,1)
out['projection_retention']['after_external_mutation']=float(st.query('v')[0].real)

st=SharedProjectedFourierStore(8,[0],np.ones((10,1)),{'a':[0],'b':[0]},event_capacity=0)
st.add_coefficient(0,1);st.query_many(['a','b'])
out['unavailable_history_fusion']={'strategy':st.views['a'].strategy,'r':10,'q_each':1,'H':1,'consumers':2}
st=SharedProjectedFourierStore(8,list(range(8)),np.ones((4,8)),{'a':[0],'b':[0],'current':list(range(8))},event_capacity=0)
st.add_coefficient(0,1);st.query('current');st.query_many(['a','b','current'])
out['current_view_fusion']={'strategy':st.views['a'].strategy}

rng=np.random.default_rng(20261008);x=rng.normal(size=1024);y=rng.normal(size=1024);bins=[0,11,1023]
p=AutoOutputPlan(1024,bins,sample=x,reps=1)
got=p.project_stream_with_sample(y,[])[0]
out['different_sample']={'max_absolute_error':float(np.max(np.abs(got-np.fft.fft(y)[bins])))}
p=ProductiveProjectionPlanner(1024,[1],max_pruned_trials=0);p.project([x,y],expected_count=2)
out['zero_trials']={'actual_pruned_trials':sum(t['strategy']=='arbitrary_pruned' for t in p.stats.trials)}

out['constant_signal_zero_bin']=[]
for n in (4096,65536,262144,1048576):
    p=ArbitraryBinsDFTPlan(n,[n-1]);got=p.execute(np.ones(n))[0]
    out['constant_signal_zero_bin'].append({'n':n,'radix':p.k,'expected':0,'absolute_error':float(abs(got))})

checks=0;maxerr=0.
for n in (1,2,3,6,8,15,16,31,64,127,128):
    x=rng.normal(size=n)+1j*rng.normal(size=n);want=np.fft.fft(x)
    for q in sorted(set((1,min(3,n),n))):
        bins=rng.integers(n,size=q)
        for k in (d for d in range(1,n+1) if n%d==0):
            for backend in ('numpy','scipy'):
                got=ArbitraryBinsDFTPlan(n,bins,radix=k,backend=backend).execute(x)
                err=float(np.max(np.abs(got-want[bins])));maxerr=max(maxerr,err);checks+=1
                np.testing.assert_allclose(got,want[bins],atol=2e-9,rtol=3e-11)
out['arbitrary_bin_sweep']={'comparisons':checks,'max_absolute_error':maxerr,'passed':True}

checks=0;maxerr=0.
for n in (1,3,8,31,64):
    for r in (0,1,4):
        basis=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n));c=rng.normal(size=r)+1j*rng.normal(size=r)
        vb={name:rng.integers(n,size=min(n+2,7)) for name in ('a','b','c')}
        union,_,_=union_frequency_sets(vb,n);projection=np.fft.fft(basis,axis=1)[:,union]
        for cap in (None,0,1,3,64):
            st=SharedProjectedFourierStore(n,union,projection,vb,c,event_capacity=cap,prepared_positions=[0,n-1])
            x=c@basis
            for t in range(60):
                d=complex(rng.normal()*.1,rng.normal()*.1)
                if r and t%2:
                    i=t%r;st.add_coefficient(i,d);x+=d*basis[i]
                else:
                    j=t%n;st.add_point(j,d);x[j]+=d
                if t%3==0:
                    names=list(vb)[:1+t%3] if t%2 else list(vb)
                    result=st.query_many(names);expected=np.fft.fft(x)
                    for name,got in result.items():
                        err=float(np.max(np.abs(got-expected[vb[name]])));maxerr=max(maxerr,err);checks+=1
                        np.testing.assert_allclose(got,expected[vb[name]],atol=2e-9,rtol=3e-11)
                        got[:]=999  # returned arrays must not alias caches
                        np.testing.assert_allclose(st.query(name),expected[vb[name]],atol=2e-9,rtol=3e-11)
                if t%11==0: st.compact()
out['multi_consumer_sweep']={'comparisons':checks,'max_absolute_error':maxerr,'passed':True}
print(json.dumps(out,indent=2))
