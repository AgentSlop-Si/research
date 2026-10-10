"""Verify packaged file hashes and the preserved predecessor archive."""
import hashlib,os,sys,zipfile
root=os.path.dirname(os.path.abspath(__file__))
manifest=os.path.join(root,'SHA256SUMS.txt')
if not os.path.isfile(manifest):
    raise SystemExit('SHA256SUMS.txt missing')
counts=0
for line in open(manifest):
    h,rel=line.rstrip('\n').split('  ',1)
    fn=os.path.join(root,rel)
    assert os.path.isfile(fn),rel
    assert hashlib.sha256(open(fn,'rb').read()).hexdigest()==h,rel
    counts+=1
archive=os.path.join(root,'prior_checkpoint_full.zip')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
print('SHA-256 files checked:',counts)
print('Preserved previous archive integrity: OK')
