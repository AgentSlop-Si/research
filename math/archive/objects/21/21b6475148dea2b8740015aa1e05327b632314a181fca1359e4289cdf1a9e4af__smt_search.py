#!/usr/bin/env python3
"""Bounded exact cancellation-aware SLP search through system Z3 C API.
All coefficients live on the half-integer grid in [-2,2]. A gate is
u+v, u-v, -u+v, -u-v, 2u, or u/2; every gate costs one operation.
Signed outputs are free metadata. Five-bit arithmetic is nonwrapping on
all constrained operations. UNSAT would apply only to this grid/budget.
"""
import argparse, ctypes, json, time
from pathlib import Path
TARGET=[[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,-1,0,1,0,-1,0],[0,1,0,-1,0,1,0,-1],[1,0,0,1,-1,0,0,-1],[0,1,-1,0,0,-1,1,0],[1,0,0,-1,-1,0,0,1],[0,1,1,0,0,-1,-1,0]]
def bv(k): return '(_ bv%d 5)'%(k%32)
def conj(xs): return '(and '+ ' '.join(xs)+')'
def disj(xs): return '(or '+ ' '.join(xs)+')'
def smt(k,timeout):
 assert 1 <= k <= 24, "5-bit predecessor indices support budgets 1..24"
 s=['(set-option :timeout %d)'%timeout,'(set-option :produce-models true)','(set-logic QF_BV)']
 def dec(n,typ): s.append('(declare-const %s %s)'%(n,typ))
 def ass(x):s.append('(assert %s)'%x)
 def val(i,j): return bv(2*int(i==j)) if i<8 else 'v_%d_%d'%(i,j)
 def pick(name,n,j):
  ans=val(n-1,j)
  for i in range(n-2,-1,-1):ans='(ite (= %s %s) %s %s)'%(name,bv(i),val(i,j),ans)
  return ans
 for g in range(8,8+k):
  for nm in ['a','b','op']: dec('%s_%d'%(nm,g),'(_ BitVec 5)')
  for nm in ['sa','sb']:dec('%s_%d'%(nm,g),'Bool')
  a,b,op='a_%d'%g,'b_%d'%g,'op_%d'%g
  ass('(bvult %s %s)'%(a,bv(g)));ass('(bvult %s %s)'%(b,bv(g)));ass('(bvule %s %s)'%(op,bv(2)))
  ass('(=> (= %s %s) (bvule %s %s))'%(op,bv(0),a,b))
  for j in range(8):
   v='v_%d_%d'%(g,j); dec(v,'(_ BitVec 5)')
   ass('(and (bvsge %s %s) (bvsle %s %s))'%(v,bv(-4),v,bv(4)))
   va,vb=pick(a,g,j),pick(b,g,j)
   va='(ite sa_%d (bvneg %s) %s)'%(g,va,va);vb='(ite sb_%d (bvneg %s) %s)'%(g,vb,vb)
   ass('(ite (= %s %s) (= %s (bvadd %s %s)) (ite (= %s %s) (= %s (bvmul %s %s)) (= (bvmul %s %s) %s)))'%(op,bv(0),v,va,vb,op,bv(1),v,bv(2),va,bv(2),v,va))
 # All eight target rows must be available up to a separately recorded sign.
 for row in TARGET:
  ass(disj([conj(['(= v_%d_%d %s)'%(g,j,bv(sign*2*c)) for j,c in enumerate(row)]) for g in range(8,8+k) for sign in [1,-1]]))
 s+=['(check-sat)','(get-info :reason-unknown)']
 return '\n'.join(s)+'\n'
def solve(src):
 z=ctypes.CDLL('libz3.so.4'); p=ctypes.c_void_p
 z.Z3_mk_config.restype=p; z.Z3_mk_context.argtypes=[p];z.Z3_mk_context.restype=p
 z.Z3_eval_smtlib2_string.argtypes=[p,ctypes.c_char_p];z.Z3_eval_smtlib2_string.restype=ctypes.c_char_p
 z.Z3_del_context.argtypes=[p];z.Z3_del_config.argtypes=[p]
 c=z.Z3_mk_config();ctx=z.Z3_mk_context(c)
 result=z.Z3_eval_smtlib2_string(ctx,src.encode()).decode()
 if result.splitlines()[0]=='sat':result+=z.Z3_eval_smtlib2_string(ctx,b'(get-model)').decode()
 z.Z3_del_context(ctx);z.Z3_del_config(c)
 return result
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--gates',type=int,default=15);a.add_argument('--timeout-ms',type=int,default=120000);a.add_argument('--output',default='results');o=a.parse_args()
 p=Path(o.output);p.mkdir(exist_ok=True);stem='slp_%d'%o.gates;src=smt(o.gates,o.timeout_ms);(p/(stem+'.smt2')).write_text(src)
 t=time.monotonic();raw=solve(src);dt=time.monotonic()-t;(p/(stem+'.log')).write_text(raw);print(raw[:300]);print('seconds',dt)
 (p/(stem+'.json')).write_text(json.dumps({'budget':o.gates,'timeout_ms':o.timeout_ms,'elapsed_seconds':dt,'status':raw.splitlines()[0],'scope':'5-bit nonwrapping encoding; half-integer coefficients in [-2,2]; binary signed add, doubling, exact halving charged equally'},indent=2))
