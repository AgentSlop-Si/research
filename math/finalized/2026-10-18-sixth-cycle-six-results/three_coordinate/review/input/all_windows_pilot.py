import sys,json,time
sys.path.insert(0,'.');import pilot as a
reps=[[(0,16),(0,17),(0,18)],[(0,8),(0,9),(0,7)],[(0,8),(0,9),(0,16)],[(0,8),(0,9),(1,7)],[(0,7),(0,8),(1,7)],[(0,8),(0,16),(1,8)]]
out=[]
for L in reps:
 t=time.time();Q,F,g=a.system(L,True);r=a.rank(Q,F);rr={'label':L,'kind':a.kind(L),'rank_target':r,'seconds':time.time()-t};out.append(rr);print(json.dumps(rr),flush=True)
open('ALL_WINDOWS_PILOT.json','w').write(json.dumps(out,indent=2)+'\n')
