"""Independent reverse-position graph DP and image-set prefix verification.
No author program is imported or executed. Author JSON is only compared at the end.
"""
import json, math, hashlib
from pathlib import Path

HERE=Path(__file__).parent
P,R=13,17
N=8*P*R

def conflicts(i,d,j,e):
    if i==j:return True
    if i>j:return conflicts(j,e,i,d)
    L=d*e//math.gcd(d,e)
    start=i+(L!=d)
    stop=j-(L!=e)
    return start+(-start)%L>stop

def review_graph():
    forbidden={N//2,N//P,N//R}
    allowed=[d for d in range(2,N) if N%d==0 and d not in forbidden]
    vertices=sorted((j,d) for j in range(1,N) for d in allowed if j%d==0)
    neighbors=[0]*len(vertices)
    edges=0
    for a,(i,d) in enumerate(vertices):
        for b in range(a+1,len(vertices)):
            j,e=vertices[b]
            if conflicts(i,d,j,e):
                neighbors[a]|=1<<b;neighbors[b]|=1<<a;edges+=1
    groups={}
    for a,(i,d) in enumerate(vertices):groups.setdefault(i,[]).append(a)
    # Descending positions, choosing none or exactly one divisor type per position.
    # State is the set of forbidden unprocessed earlier vertices. No shifted
    # forward masks or per-vertex author recurrence is used.
    states={0:0};peak=1;transitions=0
    for j,group in sorted(groups.items(),reverse=True):
        before=(1<<min(group))-1
        new={}
        for ban,score in states.items():
            tail=ban&before
            new[tail]=max(new.get(tail,-1),score);transitions+=1
            for a in reversed(group):
                if ban>>a&1:continue
                nextban=tail|(neighbors[a]&before)
                value=score+vertices[a][1]-1
                new[nextban]=max(new.get(nextban,-1),value);transitions+=1
        states=new;peak=max(peak,len(states))
    assert set(states)=={0}
    controls=[
        ('exact period conflict retained',conflicts(104,8,208,52),True),
        ('same-position types conflict',conflicts(52,4,52,13),True),
        ('left endpoint legal',conflicts(8,8,12,4),False),
        ('right endpoint legal',conflicts(4,4,8,8),False),
        ('both endpoints forbidden',conflicts(4,2,6,3),True),
        ('interior common multiple',conflicts(4,2,10,2),False),
    ]
    for name,actual,expected in controls:assert actual==expected,name
    return {'N':N,'allowed_orders':allowed,'forbidden_maximal_orders':sorted(forbidden),
            'vertices':len(vertices),'pairs':len(vertices)*(len(vertices)-1)//2,
            'edges':edges,'maximum_independent_weight':states[0],
            'reverse_position_states_peak':peak,'reverse_position_transitions':transitions,
            'endpoint_controls':[name for name,_,_ in controls]}

def review_witness(outer_order):
    # D8 realized as actual permutations of the square, composed explicitly.
    square=[tuple((i+(-x if b else x))%4 for x in range(4)) for b in range(2) for i in range(4)]
    lookup={v:i for i,v in enumerate(square)}
    prod=[[lookup[tuple(a[b[x]] for x in range(4))] for b in square] for a in square]
    coords=[(g%8,(g//8)%P,g//(8*P)) for g in range(N)]
    def mul(g,h):
        d,c,t=coords[g];e,z,u=coords[h]
        return prod[d][e]+8*((c+z)%P)+8*P*((t+u)%R)
    order=[d+8*c+8*P*t for d in outer_order for c in range(P) for t in range(R)]
    assert len(order)==N and len(set(order))==N
    images=[0]*N;prefix=0;score=0;profile=[];generators=set()
    for k,y in enumerate(order,1):
        prefix|=1<<y
        stab=[]
        for g in range(N):
            images[g]|=1<<mul(g,y)
            if images[g]==prefix:stab.append(g)
        assert stab and k%len(stab)==0
        profile.append(len(stab));score+=len(stab)-1
        if k<N:generators.update(stab)
    B={0};basis=[]
    for g in sorted(generators):
        if g in B:continue
        basis.append(g);queue=list(B)
        while queue:
            h=queue.pop()
            for a in basis:
                v=mul(a,h)
                if v not in B:B.add(v);queue.append(v)
    return {'outer_D8_order':outer_order,'score':score,'proper_generated_subgroup_order':len(B),
            'translation_prefix_image_equalities':N*N,'profile':profile,
            'full_prefix_stabilizer':profile[-1]}

def main():
    graph=review_graph()
    witnesses=[review_witness(x) for x in ([0,4,2,6,1,5,7,3],[0,4,1,5,2,6,3,7])]
    candidate=json.loads((HERE/'p13_r17_check.json').read_text())
    assert graph['maximum_independent_weight']==candidate['graph']['maximum']==3739
    assert graph['vertices']==candidate['graph']['vertices']==1968
    assert graph['edges']==candidate['graph']['edges']==41901
    for own,author in zip(witnesses,candidate['group_witnesses']):
        assert own['score']==author['score']
        assert own['proper_generated_subgroup_order']==author['B_order']
        assert own['profile']==author['stabilizer_profile']
    assert witnesses[0]['score']==5948 and witnesses[0]['proper_generated_subgroup_order']==884
    assert witnesses[1]['score']==5506 and witnesses[1]['proper_generated_subgroup_order']==1768
    wrong=review_witness([0,1,2,3,4,5,6,7])
    assert wrong['score']==5506 and wrong['proper_generated_subgroup_order']==884
    escape_bound=graph['maximum_independent_weight']+N-1
    assert escape_bound==5506
    # Previously accepted abelian/two-Sylow maxima are explicit inherited premises.
    subgroup_premises=[(884,2532),(136,332),(104,252)]
    local_bounds=[{'order':h,'accepted_maximum':m,'index':N//h,'bound':N//h*m+N-h} for h,m in subgroup_premises]
    assert all(x['bound']==5948 for x in local_bounds)
    result={'status':'ACCEPT bounded D8 x C13 x C17 maxima under stated inherited subgroup premises',
            'scope':'One finite pair only; no uniform p13/r statement, equality classification, count, novelty or speed claim.',
            'graph':graph,'witnesses':witnesses,'escape_upper_bound':escape_bound,
            'unrestricted_upper_bound':max(escape_bound,max(x['bound'] for x in local_bounds)),
            'inherited_subgroup_bounds':local_bounds,
            'negative_wrong_encoding':{'score':wrong['score'],'proper_generated_subgroup_order':wrong['proper_generated_subgroup_order'],'rejected_as_escape':True},
            'author_program_executed':False,'candidate_json_sha256':hashlib.sha256((HERE/'p13_r17_check.json').read_bytes()).hexdigest(),
            'reviewer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'INDEPENDENT_REVIEW_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='witnesses'},indent=2))

if __name__=='__main__':main()
