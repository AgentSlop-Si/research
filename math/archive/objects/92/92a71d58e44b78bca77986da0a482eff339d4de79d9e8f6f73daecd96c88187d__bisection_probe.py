"""Experimental balanced cuts of the multi-layout interaction graph.
All arithmetic statements are verified separately, never assumed from optimization.
"""
import random, time
import networkx as nx
from moving_partition import *

def input_line_permutations(n, perms):
    seq=list(range(n));allseq=[seq]
    for p in perms:
        seq=[seq[p[j]] for j in range(n)]
        allseq.append(seq)
    return allseq

def build_interaction_graph(n,perms):
    G=nx.Graph();G.add_nodes_from(range(n))
    for seq in input_line_permutations(n,perms):
        for u,v in zip(seq[:-1],seq[1:]):
            if G.has_edge(u,v):G[u][v]['weight']+=1
            else:G.add_edge(u,v,weight=1)
    return G

def bisection_score(n,perms,initial):
    cap,path,costs=moving_partition_budget(n,list(initial),perms,[1]*(len(perms)+1))
    return cap,path,costs

def minimize(n,perms,seed=1,restarts=20):
    G=build_interaction_graph(n,perms)
    rng=random.Random(seed)
    seeds=[]
    k=n.bit_length()-1
    for mask in range(1,n):
        _,costs,_=None,None,None
        seeds.append((mask_boundary(mask,k),mask))
    seeds=sorted(seeds)[:min(30,len(seeds))]
    partitions=[(set(parity_set(n,m)),set(parity_set(n,m,1))) for _,m in seeds]
    for z in range(restarts):
        a=set(rng.sample(range(n),n//2));partitions.append((a,set(range(n))-a))
    best=[]
    for i,par in enumerate(partitions):
        cut=nx.algorithms.community.kernighan_lin_bisection(G,partition=par,weight='weight',max_iter=25,seed=i+seed)
        a=cut[0]
        budget,path,costs=bisection_score(n,perms,a)
        best.append((budget, sorted(a),costs))
    return sorted(best), G

if __name__=='__main__':
 for k in (6,7,8):
    n=1<<k; tr=transformations(k)
    progs={
      'bitrev_middle_rotate':[tr['bitrev'],tr['bitrev_then_rotl'],tr['bitrev']],
      'bitrev_middle_xor':[tr['bitrev'],tr['bitrev_then_xor'],tr['bitrev']],
      'all_bitrev':[tr['bitrev']]*3,
      'all_rot':[tr['rotl']]*3,
      'mix_both':[tr['bitrev_then_rotl'],tr['bitrev_then_xor'],tr['bitrev_then_rotl']],
    }
    for name,ps in progs.items():
        start=time.time(); found,G=minimize(n,ps,restarts=10)
        best_budget=found[0][0]
        rank=None
        if best_budget < n//2:
            C=found[0][1]
            budget,sets,_=moving_partition_budget(n,C,ps,[1]*4)
            R=sorted(set(range(n))-set(sets[-1]))
            rank=fourier_block_rank(n,R,C,12289)
        print(k,name,'min budget',best_budget,'rank',rank,'gap',None if rank is None else rank-best_budget,'edges',G.number_of_edges(),'time',round(time.time()-start,2),flush=True)
