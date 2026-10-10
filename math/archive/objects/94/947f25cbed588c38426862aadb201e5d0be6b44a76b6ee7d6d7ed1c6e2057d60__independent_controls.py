"""Fresh review controls. Does not read, import, execute, compile or parse supplied programs.
Only mathematical definitions and small synthetic package data are evaluated.
"""
import json, math, hashlib
from pathlib import Path

out={"control_origin":"Fresh independent reviewer-authored controls for this review", "supplied_programs_executed":False,"supplied_programs_imported":False,"supplied_programs_compiled":False,"supplied_programs_ast_parsed":False,"controls":[]}
# Enumerate the parity cut directly rather than using a source boundary formula.
k,t,r=9,2,2
n=1<<k;q=math.ceil(math.log2(4*r*t));mask=1<<q
bits=[(j & mask).bit_count()%2 for j in range(n)]
changes=sum(bits[j]!=bits[j+1] for j in range(n-1))
unweighted=t*changes;weighted=r*unweighted
assert (q,mask,changes,unweighted,weighted)==(4,16,31,62,124)
# For this identical parity layout the existing exact-rank formula's branch is N/2.
rank=n//2
assert k>t*q and weighted<n//4 and weighted<rank
out['controls'].append({'name':'GF2 scan-order capacity weighting','source_index':43,'k':k,'stages':t,'scan_order':r,'layout':'identity interstage map','low_bit_quota':q,'selected_mask':mask,'directly_enumerated_boundaries_per_stage':changes,'unweighted_reported_capacity':unweighted,'required_order_weighted_capacity':weighted,'reported_gap_if_unweighted':rank-unweighted,'correct_weighted_gap':rank-weighted,'theorem_still_excludes_this_example':True,'finding':'The source report is underweighted for r>1; the example does not refute the depth theorem.'})
# Odd-prime requirement is structural: W_r^2=(-1)^r I for n=2.
# Build I-alpha W_r from its definition and take a 2x2 determinant.
p=5;n=2;alpha=2;omega=4
mats=[]
for character in (0,1):
 w=[[0,0],[0,0]]
 for j in range(n):w[(j+1)%n][j]=pow(omega,character*j,p)
 a=[[(int(i==j)-alpha*w[i][j])%p for j in range(n)] for i in range(n)]
 d=(a[0][0]*a[1][1]-a[0][1]*a[1][0])%p
 mats.append({'character':character,'denominator_matrix':a,'determinant':d})
assert (1-pow(alpha,n,p))%p!=0 and mats[0]['determinant']!=0 and mats[1]['determinant']==0
out['controls'].append({'name':'Even-length Weyl packet boundary','source_indices':[67,70],'n':n,'p':p,'alpha':alpha,'primitive_root':omega,'shared_guard':(1-pow(alpha,n,p))%p,'literal_green_denominators':mats,'finding':'Common guard 1-alpha^n is insufficient at n=2: one literal Green inverse is singular although character_packet_apply accepts the preliminary guard. Intended domain must exclude even n.'})
# Prototype inv(0,p)=pow(0,p-2,p)=0 cannot be a multiplicative inverse.
p=11;claimed=pow(0,p-2,p)
assert claimed==0 and 0*claimed%p!=1
out['controls'].append({'name':'Prototype zero-inverse arithmetic','source_index':67,'p':p,'zero_power_p_minus_two':claimed,'multiplicative_inverse_identity':False,'finding':'A helper returning pow(a,p-2,p) without a zero check silently returns zero for a singular denominator.'})
# Count exact ordered distinct prefix choices without source code.
sizes=[4,8,16,32,64]
count=sum(2*n*(n-1)*n*(n-1)*(n-2) for n in sizes)
assert count==2076565824
out['controls'].append({'name':'Phase38 exhaustive prefix ledger','source_indices':[74,77,78],'sizes':sizes,'fields':2,'ordered_mapping_prefixes':count,'larger_sampled_cases':4,'samples_per_larger_case':200000,'total_larger_samples':800000,'finding':'Historical wrapper count is arithmetically consistent, but is not proof those operations ran.'})
# Demonstrate stale-manifest/double-inclusion from a synthetic preexisting file list.
old=b'{"generation":1}\n';new=b'{"generation":2}\n'
initial_files=['MANIFEST.json','code.py']; checksums={'MANIFEST.json':hashlib.sha256(old).hexdigest()}; zip_members=initial_files+['SHA256SUMS.txt','MANIFEST.json']
assert checksums['MANIFEST.json']!=hashlib.sha256(new).hexdigest() and zip_members.count('MANIFEST.json')==2
out['controls'].append({'name':'Preexisting manifest packaging model','source_index':52,'archive_manifest_occurrences':zip_members.count('MANIFEST.json'),'manifest_hash_matches_rewritten_bytes':False,'finding':'The source order of inventory, hashing, rewriting, and appending produces stale manifest hash and duplicate archive member on a rerun with a preexisting manifest. Synthetic data only.'})
Path(__file__).with_name('INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'independent_control_count':len(out['controls']),'all_control_assertions_passed':True,'supplied_code_execution':False}))
