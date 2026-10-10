"""Independent Phase 30 checks, with exact integer + finite-field witnesses."""
import unittest,math
from cyclotomic_rank_certificate import result
from abelian_rank_certificate import run
from linear_cse_probe import build_before,build_after
from full_cse_probe import compile120
from fused120 import make_fused120_plan
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR

class Phase30RankTests(unittest.TestCase):
 def test_cyclic_trace_rank(self):
  for n in (1,2,3,4,8,15,16,60,120):
   with self.subTest(n=n):
    r=result(n)
    self.assertEqual(r['witnesses']['trace']['rank_mod_p'],r['divisor_count'])
    self.assertNotEqual(r['witnesses']['trace']['minor_determinant_mod_p'],0)
 def test_cyclic_traceless_rank(self):
  for n in (5,8,16,30,60,120):
   with self.subTest(n=n):
    r=result(n)
    self.assertEqual(r['witnesses']['traceless']['rank_mod_p'],n-r['divisor_count'])
    self.assertNotEqual(r['witnesses']['traceless']['minor_determinant_mod_p'],0)
 def test_cyclic_generic_full(self):
  for n in (3,6,9,12,24,32,60):
   with self.subTest(n=n):
    r=result(n)
    self.assertEqual(r['witnesses']['unrestricted']['rank_mod_p'],n)
 def test_noncylcic_subgroup_count(self):
  for ns,expected in (((3,3),5),((4,2),6),((4,4),10),((8,8),22),((3,3,3),14)):
   with self.subTest(ns=ns):
    rr=run(ns)
    self.assertEqual(rr['cyclic_subgroup_count'],expected)
    self.assertEqual(rr['witnesses']['traceless']['rank_mod_p'],math.prod(ns)-expected)
 def test_galois_bound_matches_all_three(self):
  for ns in ((8,4),(5,5,3),(4,2,3)):
   with self.subTest(ns=ns):
    r=run(ns);N=r['order'];c=r['cyclic_subgroup_count']
    self.assertEqual([r['witnesses'][k]['rank_mod_p'] for k in ('trace','traceless','unrestricted')],[c,N-c,N])
 def test_nonrational_twiddle_count(self):
  for h in (1,2,4,8,16,32,64):
   g=8*h
   count=0
   for u in range(8):
    for q in range(h):
     k=(u*q)%g
     # roots of unity in Q are +/-1, so their orders divide two.
     irrational=g//math.gcd(g,k)>2
     self.assertEqual(irrational,u!=0 and q!=0,(h,u,q))
     count+=irrational
   self.assertEqual(count,7*(h-1))
   self.assertEqual(15*count,105*(h-1))
 def test_symbolic_linear_cse(self):
  before,bouts=build_before();after,aouts=build_after()
  self.assertEqual((len(before.nodes)-120,len(after.nodes)-144),(522,516))
  self.assertEqual((before.reused,after.reused),(0,0))
  for comp in (before,after):
   formset=set()
   for value in comp.byvector:
    first=next((v for v in value if v),0)
    key=value if first>=0 else tuple(-v for v in value)
    self.assertNotIn(key,formset)
    formset.add(key)
 def test_no_field_cse(self):
  for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
   with self.subTest(field=p):
    c,outputs,stats=compile120(make_fused120_plan(120,p=p,gen=gen))
    self.assertEqual((stats['preadd'],stats['postadd'],stats['midmul']),(522,516,140))
    self.assertEqual((stats['add_reuses'],stats['mul_reuses']),(0,0))
    self.assertEqual(stats['total'],1178)
    self.assertEqual(len(set(outputs)),120)

if __name__=='__main__':unittest.main()
