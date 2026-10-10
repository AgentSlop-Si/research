from pathlib import Path
import subprocess,sys,json,time
ROOT=Path(__file__).resolve().parent
CHECKS=[('fft_control_variate_fusion_research','verify_fusion_identity.py'),
        ('fft_control_variate_fusion_research','review_edge_checks.py'),
        ('fft_control_variate_fusion_research','run_audit.py'),
        ('fft_composed_graph_fusion_research','run_audit.py'),
        ('fft_composed_graph_fusion_research','review_edge_checks.py'),
        ('fft_fusion_exact_gate_research','verify_fusion.py')]
if __name__=='__main__':
    records=[]
    for folder,script in CHECKS:
        start=time.perf_counter()
        r=subprocess.run([sys.executable,script],cwd=ROOT/folder,capture_output=True,text=True)
        records.append({'folder':folder,'script':script,'exit_code':r.returncode,
                        'seconds':time.perf_counter()-start,'stdout':r.stdout,'stderr':r.stderr})
        print(('PASS' if r.returncode==0 else 'FAIL')+' '+folder+'/'+script,flush=True)
        if r.returncode: break
    ok=len(records)==len(CHECKS) and all(r['exit_code']==0 for r in records)
    (ROOT/'rerun_results.json').write_text(json.dumps({'status':'PASS' if ok else 'FAIL','runs':records},indent=2)+'\n')
    raise SystemExit(0 if ok else 1)
