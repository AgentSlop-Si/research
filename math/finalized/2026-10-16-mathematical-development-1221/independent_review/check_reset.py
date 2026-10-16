import itertools,json
count=0
for F in [1,2,4]:
 for B in [1,2,4]:
  for events in itertools.product(['A','B',0,1,3],repeat=5):
   a=b=rent=alg=0;dp={(0,0):0}
   for event in events:
    nxt={}
    for (i,j),cost in dp.items():
     if event in ['A','B']:
      ni,nj=i+(event=='A'),j+(event=='B')
      if ni+nj<B:nxt[(ni,nj)]=min(nxt.get((ni,nj),10**9),cost)
      nxt[(0,0)]=min(nxt.get((0,0),10**9),cost+F)
     else:
      nxt[(i,j)]=min(nxt.get((i,j),10**9),cost+event*(i+2*j+3*i*j))
      nxt[(0,0)]=min(nxt.get((0,0),10**9),cost+F)
    dp=nxt
    if event=='A':a+=1
    elif event=='B':b+=1
    else:
     r=event*(a+2*b+3*a*b)
     if rent+r>=F:alg+=F;a=b=rent=0
     else:alg+=r;rent+=r
    if a+b>=B:alg+=F;a=b=rent=0
   assert alg<=2*min(dp.values()),(F,B,events,alg,dp)
   count+=1
print(json.dumps({'independent_schedules':count,'all_pass':True,'scope':'Finite transcription controls; arbitrary-sequence result relies on separately reviewed interval proof.'}))
