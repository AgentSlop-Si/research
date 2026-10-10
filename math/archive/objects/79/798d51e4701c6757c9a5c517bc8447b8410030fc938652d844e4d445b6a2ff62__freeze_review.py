#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, shutil
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
DEST=HERE/'final_v1'
DEST.mkdir(exist_ok=False)
(DEST/'source').mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=[ROOT/'research_cycle_0958/augmented_content_followup/AUGMENTED_CONTENT_FOLLOWUP.md']
source += [ROOT/f'research_cycle_0958/augmented_content_followup/EXACT_CONTENT_S{s}.json' for s in [3,7,11,15,19]]
source += [ROOT/'research_cycle_0958/augmented_content_followup/S63_P5_COMPONENT_CERTIFICATE.json',
ROOT/'research_cycle_0958/composite_guard/final_v1/COMPOSITE_GUARD_EXTENSION.md',
ROOT/'research_finalization_0923/algebra/final_v1/FINAL_THEOREMS.md']
source_rows=[]
for p in source:
    d=DEST/'source'/p.name;shutil.copyfile(p,d)
    source_rows.append({'original':str(p.relative_to(ROOT)),'frozen':str(d.relative_to(DEST)),'sha256':sha(d)})
files=['REVIEW_SUMMARY.md','independent_exact_review.py','independent_boundary_controls.py','independent_s63_p5.py',
       'independent_run.log','independent_boundary_run.log','independent_s63_run.log',
       'INDEPENDENT_BOUNDARY_CONTROLS.json','INDEPENDENT_S63_P5.json']
files += [f'INDEPENDENT_EXACT_S{s}.json' for s in [3,7,11,15,19]]
for f in files:shutil.copyfile(HERE/f,DEST/f)
receipt={
 'status':'ACCEPT_SCOPED_NEXT_CYCLE_SUPPLEMENT',
 'date_utc':'2026-10-10',
 'title':'Two augmented-content families and a residue-component obstruction',
 'scope':'Independent exact verification and mathematical review, separate from all previous frozen releases.',
 'source_programs_executed':False,
 'source_programs_imported_compiled_or_parsed':False,
 'author_checker_executed':False,
 'method':'Independently authored subset Gaussian coefficients and direct full-degree multiplication matrices over the integral cyclotomic power basis; exact Faddeev-LeVerrier determinants. Independent finite-field elementary-symmetric construction and direct-U Euclidean gcds for the adverse component.',
 'accepted_claims':[
 {'id':'ACF01','claim':'c_15^+=3^12*5^9 and c_19^+=19^11, with complete canonical coefficient arrays and integer gcd Bezout witnesses','status':'ACCEPT'},
 {'id':'ACF02','claim':'For every prime p=1 mod4, p!=5, half-order squarefreeness at all primitive roots of order 15p; for every prime p=1 mod4, likewise at order 19p','status':'ACCEPT_USING_PREVIOUSLY_ACCEPTED_AUGMENTED_CRITERION'},
 {'id':'ACF03','claim':'For U=z^rP(z+z^-1), DiscU=P(2)P(-2)Disc(P)^2 and Res(U,z^s+1)=(-1)^rP(-2)Res(P,C_s)^2; hence Gamma=(-1)^rP(2)P(-2)^2[Disc(P)Res(P,C_s)]^2','status':'ACCEPT_GENERAL_POLYNOMIAL_IDENTITIES'},
 {'id':'ACF04','claim':'s63,p5 has an irreducible exact-order63 adverse resonance component and a separate good augmented component; thus an all-component/norm-unit shortcut fails while 5 does not divide c_63^+','status':'ACCEPT_EXACT_COMPONENT_CERTIFICATE'},
 {'id':'ACF05','claim':'The new d=3 mod4 families remove the remaining residual-squarefreeness guard in the accepted all-local-index overlap theorem; the forbidden simple root -1 and m+1 legal-bank minimum persist','status':'ACCEPT_WITH_INHERITED_RESONANCE_AND_DISK_THEOREMS'}],
 'exact_augmented_contents':{'3':1,'7':49,'11':161051,'15':3**12*5**9,'19':19**11},
 'all_supplied_fixed_base_coefficients_match':True,
 'all_supplied_s63_component_coefficients_match':True,
 'controls':{
  'exact_cyclotomic_arithmetic':True,'ordinary_derivative':True,'resultant_in_Gamma':True,
  'reduced_coordinate_gcd_not_norm':True,'gcd_bezout_witnesses':True,
  'symbolic_z_resultant_crosschecks_s7_s11':True,
  's7_p13_tau2_triple_zero_and_norm_trap':True,
  's19_unreduced19pow10_versus_reduced19pow11':True,
  's15_p5_ramified_exclusion_Phi15_mod5_equals_Phi3pow4':True,
  's63_p5_irreducibility_tests':'q^15625=q; gcd(f,q^25-q)=gcd(f,q^125-q)=1, and likewise for h',
  's63_p5_primitive_tests':'q^63=1; q^21!=1; q^9!=1 for both fields',
  's63_p5_adverse_direct_inverse_gcd_degrees':[[0,2],[0,2]],
  's63_p5_good_direct_inverse_gcd_degrees':[[0,0],[0,0]]},
 'not_independently_rerun':['Author exploratory 43-pair modular survey; not a premise of accepted claims'],
 'open_or_not_claimed':[
  'Uniform no-extra-unramified-prime support of augmented content',
  'General characteristic-zero nonvanishing of Gamma_s for arbitrary composite s',
  'Repeated-prime bridge; d=75 is excluded from the new 15p proof and is not a counterexample',
  'All-composite half-order simplicity',
  'Worldwide publication priority',
  'Any FFT runtime improvement'],
 'frozen_sources':source_rows,
 'review_files':[{'path':f,'sha256':sha(DEST/f)} for f in files]
}
(DEST/'ACCEPTANCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
manifest={'status':'FROZEN_INDEPENDENT_REVIEW','files':[{'path':str(p.relative_to(DEST)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(DEST.rglob('*')) if p.is_file()]}
(DEST/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'receipt':str((DEST/'ACCEPTANCE_RECEIPT.json').relative_to(ROOT)),
 'receipt_sha256':sha(DEST/'ACCEPTANCE_RECEIPT.json'),
 'review_summary_sha256':sha(DEST/'REVIEW_SUMMARY.md'),
 'manuscript_sha256':sha(DEST/'source/AUGMENTED_CONTENT_FOLLOWUP.md'),
 'manifest_sha256':sha(DEST/'MANIFEST.json')},indent=2))
