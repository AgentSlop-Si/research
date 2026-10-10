import unittest
import numpy as np
from multi_view import SharedProjectedFourierStore,union_frequency_sets

class TestMultiView(unittest.TestCase):
    def test_shared_updates_and_independent_queries(self):
        rng=np.random.default_rng(313); n=512;r=7
        view_bins={'fast':[1,3,9,17],'slow':[2,7,100],'mix':[3,7,11,255]}
        union,_,_=union_frequency_sets(view_bins,n)
        basis=rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))
        proj=np.fft.fft(basis,axis=1)[:,union]
        c=rng.standard_normal(r)+1j*rng.standard_normal(r)
        prepared=[5,77]
        st=SharedProjectedFourierStore(n,union,proj,view_bins,c,prepared_positions=prepared,event_capacity=12)
        x=c@basis
        for t in range(25):
            if t%3:
                i=t%r;d=.01*(t+1)*(1+1j);st.add_coefficient(i,d);x+=d*basis[i]
            else:
                j=prepared[t%2];d=.02*(1-1j);st.add_point(j,d);x[j]+=d
            if t%2==0:
                got=st.query('fast');self.assertTrue(np.allclose(got,np.fft.fft(x)[view_bins['fast']],rtol=3e-11,atol=3e-9))
            if t%7==0:
                got=st.query('slow');self.assertTrue(np.allclose(got,np.fft.fft(x)[view_bins['slow']],rtol=3e-11,atol=3e-9))
        # slow view may have lost history; exact rebuild must still work.
        for name,b in view_bins.items():
            self.assertTrue(np.allclose(st.query(name),np.fft.fft(x)[b],rtol=3e-11,atol=3e-9))
        st.compact()
    def test_union_mapping(self):
        u,_,idx=union_frequency_sets({'a':[9,1,9],'b':[2,1]},16)
        self.assertEqual(u.tolist(),[1,2,9]);self.assertEqual(idx['a'].tolist(),[2,0,2])

    def test_query_many_fused(self):
        rng=np.random.default_rng(99);n=256;r=5
        vb={'a':[1,2,3,4,5],'b':[3,4,5,6,7],'c':[4,5,8]}
        union,_,_=union_frequency_sets(vb,n)
        basis=rng.standard_normal((r,n))+1j*rng.standard_normal((r,n));proj=np.fft.fft(basis,axis=1)[:,union]
        c=np.ones(r,dtype=np.complex128);st=SharedProjectedFourierStore(n,union,proj,vb,c,event_capacity=64)
        x=c@basis
        for t in range(20):
            i=t%r;d=.01*(1+1j);st.add_coefficient(i,d);x+=d*basis[i]
        out=st.query_many(['a','b','c']);fx=np.fft.fft(x)
        for name,b in vb.items():self.assertTrue(np.allclose(out[name],fx[b],rtol=3e-11,atol=3e-9))
        self.assertIn(st.views['a'].strategy,('batch_rebuild','rebuild','replay'))

if __name__=='__main__':unittest.main()
