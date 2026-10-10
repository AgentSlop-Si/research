import pathlib,sys,json,hashlib
p=pathlib.Path(__file__).parent;rows=json.loads((p/'SOURCE_MANIFEST.json').read_text()); selected=map(int,sys.argv[1:]);out=[]
for i in selected:
 r=rows[i-1];raw=(p/'sources'/r['sha256']).read_bytes();out += ['===== SOURCE '+str(i)+' '+r['representative_path']+' SHA256 '+r['sha256']+' =====']
 out += [str(n).rjust(4)+' '+s for n,s in enumerate(raw.decode().splitlines(),1)];out += ['===== END SOURCE '+str(i)+'; '+str(len(raw))+' bytes; '+str(r['line_count'])+' lines =====']
s='\n'.join(out)+'\n';dest=p/'read_evidence'/('sources_'+'_'.join(sys.argv[1:])+'.txt');dest.write_text(s);print(s,end='')
