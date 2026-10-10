"""Fresh reviewer arithmetic only. Does not import/read/execute any supplied source."""
import json
from pathlib import Path
import numpy as np
out={'method':'Reviewer-authored integer/finite-field counterexample arithmetic; no supplied code execution/import/compile/AST.'}
# A valid primitive-root tensor coordinate and an invertible first-leg map.
p=2013265921;q=8;m=2;omega=pow(31,(p-1)//16,p)
assert pow(omega,16,p)==1 and pow(omega,8,p)==p-1
# h=0,t=4,u=0: T[s,0,4,0]=omega^(-8s)=(-1)^s.
v=[1 if s%2==0 else p-1 for s in range(q)]
a=[p-1]*q
integer_dot=sum(x*y for x,y in zip(a,v)); exact=integer_dot%p
wrapped=int(np.dot(np.array(a,dtype=np.int64),np.array(v,dtype=np.int64)))
observed=wrapped%p
assert exact==0 and observed!=exact and integer_dot>2**63-1
# Other map rows are e_1,...,e_7: determinant first-row first-column = p-1.
out['phase6_int64_overflow']={'source_id':'S31','source_lines':'141-159','p':p,'q':q,'m':m,'omega':omega,'tensor_coordinate':[0,0,4,0],'first_map_row':a,'other_rows':'e_1,...,e_7','map_determinant_mod_p':p-1,'contracted_tensor_fiber':v,'integer_dot':integer_dot,'signed_int64_dot':wrapped,'exact_residue':exact,'actual_numpy_dot_residue':observed,'scope':'transform_legs only; Python-integer endpoint_gauges and FFT paths are separate.'}
# N=16,K=M=4, true C=I+J, with zero seed and one innovation.
k=4;C=[[1+int(i==j) for j in range(k)]for i in range(k)]
cols=[[0]*k,[0]*k,[1,0,0,0],[2,1,1,1]]
true_residuals=[[(cols[t+1][i]-sum(C[i][j]*cols[t][j]for j in range(k)))%p for i in range(k)]for t in range(3)]
assert [sum(bool(x)for x in row)for row in true_residuals]==[0,1,0]
chosen_residuals=cols[1:]
# A single spike matching moments 5,1 would have node=1/5, not in mu_4.
node=pow(5,-1,p);power=pow(node,4,p)
assert power!=1
out['phase9_unobservable_seed']={'source_id':'S25','source_lines':'44-64,153-174,208-234','p':p,'N':16,'K':4,'M':4,'s':1,'true_dense_circulant':C,'columns':cols,'true_innovations':true_residuals,'seed_spectra':'both identically zero','chosen_controller':'all eigenvalues zero','chosen_residual_supports':[sum(bool(v)for v in row)for row in chosen_residuals],'last_two_syndromes':[5,1],'necessary_single_spike_node':node,'node_fourth_power':power,'conclusion':'A true <=1-spike-per-transition recurrence with clean first transition is rejected by the source chosen-controller sparse decoder. Require observable seed modes, a narrower completeness claim, or a different learner.'}
# Dual family: each true innovation has one spectral mode, but the chosen zero
# controller sees an accumulated two-mode residual after activating seed-zero modes.
wk=pow(omega,4,p);iv4=pow(4,-1,p)
spectral_cols=[[0]*4,[0]*4,[iv4]*4,[(5+pow(wk,b,p))*iv4%p for b in range(4)]]
first=[iv4]*4;second=[pow(wk,b,p)*iv4%p for b in range(4)]
assert all((spectral_cols[3][i]-sum(C[i][j]*spectral_cols[2][j]for j in range(4)))%p==second[i] for i in range(4))
dual_node=(5+wk)*pow(6,-1,p)%p
assert pow(dual_node,4,p)!=1
out['phase9_spectral_unobservable_seed']={'source_id':'S26','source_lines':'24-44,69-88','p':p,'N':16,'K':4,'M':4,'s':1,'true_controller':'I+J','columns':spectral_cols,'true_innovation_spectra':[[0,0,0,0],[1,0,0,0],[0,1,0,0]],'learned_zero_controller_residual_spectra':[[0,0,0,0],[1,0,0,0],[5,1,0,0]],'necessary_single_mode_node_from_spatial_probes':dual_node,'node_fourth_power':pow(dual_node,4,p),'conclusion':'True one-spectral-mode-per-transition family member is rejected because the selected zero controller yields an undecodable residual.'}
# Fully spatially dense versions, so the counterexample does not rely on zero input coordinates.
ones=[1]*4;dense_cols=[ones,[5]*4,[26,25,25,25],[127,126,126,126]]
dense_true=[[(dense_cols[t+1][i]-sum(C[i][j]*dense_cols[t][j]for j in range(4)))%p for i in range(4)]for t in range(3)]
assert all(all(row)for row in dense_cols) and [sum(bool(v)for v in row)for row in dense_true]==[0,1,0]
last=[(v-5*pow(4,-1,p)*sum(dense_cols[2]))%p for v in dense_cols[3]]
assert sum(last)%p==0 and sum(last[b]*pow(wk,-b,p)for b in range(4))%p==1
out['phase9_dense_input_boundary']={'source_id':'S25','columns':dense_cols,'true_innovations':dense_true,'all_input_coordinates_nonzero':True,'seed_spectrum':[4,0,0,0],'learned_lambda':[5,0,0,0],'last_residual':last,'last_two_syndromes':[0,1],'conclusion':'No <=1-spike vector has zero zeroth Fourier moment and nonzero first moment; the source BM order exceeds the budget and rejects. The actual I+J controller satisfies the one-spike promise.'}
dual_dense=[ones,[5]*4,[(25+pow(wk,b,p)*iv4)%p for b in range(4)],[(125+(pow(wk,b,p)+pow(wk,2*b,p))*iv4)%p for b in range(4)]]
assert all(all(row)for row in dual_dense)
node=(wk+pow(wk,2,p))*pow(2,-1,p)%p
assert pow(node,4,p)!=1
expected=[[0]*4,[pow(wk,b,p)*iv4%p for b in range(4)],[pow(wk,2*b,p)*iv4%p for b in range(4)]]
assert all((dual_dense[t+1][i]-sum(C[i][j]*dual_dense[t][j]for j in range(4)))%p==expected[t][i]for t in range(3)for i in range(4))
out['phase9_spectral_dense_input_boundary']={'source_id':'S26','columns':dual_dense,'all_input_coordinates_nonzero':True,'seed_spectrum':[4,0,0,0],'learned_lambda':[5,0,0,0],'true_innovation_spectra':[[0,0,0,0],[0,1,0,0],[0,0,1,0]],'last_learned_residual_spectrum':[0,1,1,0],'necessary_single_mode_node':node,'node_fourth_power':pow(node,4,p),'conclusion':'Source zero-mode convention cannot decode the late two-mode residual with budget s=1; original controller has one mode per innovation.'}
# N2 F3 baseline exception, independent of Schur implementation.
dets=[{'a':a,'b':b,'det':((1-a)*(2-b)-1)%3}for a in (1,2)for b in (1,2)]
assert all(x['det']for x in dets)
out['phase8_invertible_baseline_exception']={'source_id':'S06','source_lines':'164-179','N':2,'p':3,'F':[[1,1],[1,2]],'residual_determinants_for_all_invertible_diagonal_baselines':dets,'conclusion':'No invertible block-diagonal baseline has rank-one residual; the companion S08 already identifies this exception.'}
# Count consistency only, not rerunning any supplied audit.
ns=[7,17,30,60,119,128,256];basis=2*sum(n*n for n in ns);intertwining=sum(n*n for n in [17,60,128])
assert (basis,intertwining,basis+intertwining,sum(ns))==(201838,20273,222111,617)
out['phase17_stored_count_arithmetic']={'basis_entries':basis,'intertwining_entries':intertwining,'total':basis+intertwining,'green_impulses':sum(ns),'scope':'Arithmetic consistency of loop bounds and stored counts; no transform execution.'}
# Endpoint lambda>0 implicit validation domains do not affect these examples.
Path(__file__).with_name('INDEPENDENT_ARITHMETIC_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
