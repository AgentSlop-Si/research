#!/usr/bin/env python3
"""Independent, bounded Phase 5 audit. Uploaded programs are never imported or executed."""
import hashlib, itertools, json, math, pathlib, random, zipfile, stat
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'extracted'/'fft_hero0_phase5_joint_frame_2026-10-10'

def provenance():
    m=json.loads((SRC/'SHA256SUMS.json').read_text())['artifacts']
    for a in m:
        d=(SRC/a['name']).read_bytes()
        assert len(d)==a['size_bytes'] and hashlib.sha256(d).hexdigest()==a['sha256']
    archive=SRC/'prior_phase4_bundle.zip'
    ancestor=ROOT/'audit'/'prior_evidence'/'approved_phase4_archive.zip'
    assert archive.read_bytes()==ancestor.read_bytes()
    members=[]
    with zipfile.ZipFile(archive) as z:
        for i in z.infolist():
            p=pathlib.PurePosixPath(i.filename)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
            assert not stat.S_ISLNK(i.external_attr>>16) and not (i.flag_bits&1)
            assert i.file_size<20_000_000
            if not i.is_dir():
                data=z.read(i);members.append({'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return {'verified_source_manifest_entries':len(m),'ancestor_byte_identical':True,'nested_inventory':members}

def prime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def divisors(n):
    return [d for d in range(2,n+1) if n%d==0 and prime(d)]
def field(q):
    p=2*q+1
    while not prime(p):p+=2*q
    v=next(g for g in range(2,p) if pow(g,2*q,p)==1 and all(pow(g,2*q//d,p)!=1 for d in divisors(2*q)))
    return p,v

def direct(x,root,p):
    return [sum(v*pow(root,k*j,p) for j,v in enumerate(x))%p for k in range(len(x))]

def modular():
    rng=random.Random(492073);rows=[];entries=0;scanned=0
    for q,m in [(2,1),(3,3),(6,3),(8,2),(9,3),(12,4),(15,3),(16,4),(25,5),(35,5),(45,5),(55,5),(63,7),(72,8),(77,7)]:
        k=q//m;p,eta=field(q);z=eta*eta%p;w=pow(z,-1,p);wm=pow(w,k,p);wk=pow(w,m,p);im=pow(m,-1,p)
        for a in list(a for a in range(1,q) if math.gcd(a,q)==1)[:3]:
            beta=3%q
            phases=[[pow(eta,2*(a*t*(t-1)//2+(a*b*m+beta)*t)+(q%2)*t,p) for t in range(m)] for b in range(k)]
            for trial in range(3):
                x=[rng.randrange(p) for _ in range(q)]
                D=[[sum(phases[b][t]*x[b*m+t]*pow(wm,-r*t,p) for t in range(m))%p for r in range(m)] for b in range(k)]
                recovered=[pow(phases[b][t],-1,p)*im*sum(D[b][r]*pow(wm,r*t,p) for r in range(m))%p for b in range(k) for t in range(m)]
                assert recovered==x
                V=[[sum(recovered[b*m+t]*pow(wk,ell*b,p) for b in range(k))%p for t in range(m)] for ell in range(k)]
                Y=[0]*q
                for ell in range(k):
                    for j in range(m):Y[ell+j*k]=sum(V[ell][t]*pow(w,ell*t,p)*pow(wm,j*t,p) for t in range(m))%p
                truth=direct(x,w,p);assert Y==truth;entries+=q
                # Derive each antiperiodic Green scan directly from a small K-DFT.
                accum=[0]*q
                for r in range(m):
                    betar=(beta+r*k)%q
                    f=direct([D[b][r] for b in range(k)],wk,p)
                    idx=[a*j%q for j in range(q)]
                    gauge=[pow(eta,2*(a*j*(j-1)//2+betar*j)+(q%2)*j,p) for j in range(q)]
                    terms=[]
                    for j,ii in enumerate(idx):
                        boundary=pow(eta,-2*(m*(ii+betar)+a*m*(m-1)//2)-(q%2)*m,p)
                        force=(f[ii%k]-boundary*f[(ii+a*m)%k])%p
                        terms.append(force*pow(gauge[j],-1,p)%p)
                    seed=sum(terms)*pow(2,-1,p)%p;prefix=0;scan=[0]*q
                    for j,ii in enumerate(idx):scan[ii]=gauge[j]*(seed-prefix)%p;prefix=(prefix+terms[j])%p
                    projected=[pow(phases[b][t],-1,p)*pow(wm,r*t,p)*D[b][r]%p for b in range(k) for t in range(m)]
                    assert scan==direct(projected,w,p);scanned+=q
                    accum=[(u+v)%p for u,v in zip(accum,scan)]
                assert [im*v%p for v in accum]==truth
        rows.append({'Q':q,'M':m,'K':k,'prime':p,'root_order':2*q})
    return {'cases':rows,'exact_aggregate_entries':entries,'exact_green_scan_entries':scanned}

def floating():
    rng=np.random.default_rng(380421);rows=[];maxerr=0.;transfers=0;moments=0
    for k,m in [(1,2),(3,2),(2,3),(3,4),(2,5),(3,6),(2,7)]:
        q=k*m;phase=np.exp(2j*np.pi*rng.random((k,m)))
        Fm=np.exp(-2j*np.pi*np.outer(np.arange(m),np.arange(m))/m)/np.sqrt(m)
        Fq=np.exp(-2j*np.pi*np.outer(np.arange(q),np.arange(q))/q)/np.sqrt(q)
        # Columns e_r / sqrt(M) form the synthesis isometry E.
        E=np.zeros((q,q),complex);P=[]
        for r in range(m):
            Pr=np.zeros((q,q),complex)
            for b in range(k):
                e=np.conj(phase[b])*np.exp(-2j*np.pi*r*np.arange(m)/m)
                E[b*m:(b+1)*m,b*m+r]=e/np.sqrt(m)
                Pr[b*m:(b+1)*m,b*m:(b+1)*m]=np.outer(e,e.conj())
            P.append(Pr)
        errs=[np.linalg.norm(E.conj().T@E-np.eye(q)),np.linalg.norm(sum(P)/m-np.eye(q))]
        J=Fq@E;errs.append(np.linalg.norm(J.conj().T@J-np.eye(q)))
        for b in range(k):
            for ell in range(k):
                T=Fm@np.diag(np.conj(phase[b])*np.exp(-2j*np.pi*ell*np.arange(m)/q))@Fm.T
                errs.append(np.linalg.norm(T.conj().T@T-np.eye(m)));transfers+=1
                # Full physical block-to-selected-output map has singular values 1/sqrt(K).
                A=Fq[np.ix_(ell+k*np.arange(m),b*m+np.arange(m))]
                errs.append(np.max(abs(np.linalg.svd(A,compute_uv=False)-1/np.sqrt(k))))
        x=rng.normal(size=q)+1j*rng.normal(size=q)
        L=(rng.normal(size=(5,q))+1j*rng.normal(size=(5,q)))/np.sqrt(q)
        # Include arbitrary nonunit diagonal preweights and postprocessing.
        x*=np.exp(np.linspace(-.5,.5,q));mu=L@x
        y=np.array([L@(pr@x) for pr in P])
        Cpop=sum(np.outer(v-mu,(v-mu).conj()) for v in y)/m
        eenergy=float(np.vdot(x,x).real)
        for s in range(1,m+1):
            cs=np.zeros((5,5),complex);total=0.;cnt=0
            for subset in itertools.combinations(range(m),s):
                bar=sum(P[r] for r in subset)/s;v=bar@x-x
                total+=float(np.vdot(v,v).real)
                vv=L@v;cs+=np.outer(vv,vv.conj());cnt+=1
                op=0 if s==m else max(1,m/s-1)
                errs.append(abs(np.linalg.norm(bar-np.eye(q),2)-op))
                # Exact deterministic energy formula in orthogonal bank coordinates.
                cap=sum(float(np.vdot(x,P[r]@x).real)/m for r in subset)
                expected=eenergy+((m/s-1)**2-1)*cap
                errs.append(abs(np.vdot(v,v).real-expected)/eenergy)
            cs/=cnt;theory=(m-s)/(s*(m-1))*Cpop
            errs.append(np.linalg.norm(cs-theory)/max(1,np.linalg.norm(Cpop)))
            errs.append(abs(total/cnt/eenergy-(m-s)/s));moments+=1
        maxerr=max(maxerr,max(errs));assert max(errs)<2e-11
        rows.append({'Q':q,'M':m,'K':k,'max_residual':max(errs)})
    return {'cases':rows,'transfer_matrices':transfers,'subset_size_moments':moments,'maximum_scaled_residual':maxerr}

def main():
    out={'provenance':provenance(),'modular':modular(),'numerical':floating(),'uploaded_code_executed':False,'status':'PASS'}
    (ROOT/'audit'/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='provenance'},indent=2))
if __name__=='__main__':main()
