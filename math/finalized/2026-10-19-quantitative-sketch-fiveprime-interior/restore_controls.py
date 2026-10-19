"""Restore one exact control file outside this sealed publication tree."""
from pathlib import Path
import base64,gzip,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
ENCODED='fiveprime/candidate/NEGATIVE_CONTROLS.json.gz.base64'
ENCODED_HASH='e545bcc328a3dbd086b758ee17fa4281e0dace879c0ee50142c77ddb24d80897'
ORIGINAL_HASH='f273537a04ec5b1a543133d25fe784871451da81830c7aae112a70a29d74bfdd'
def restore(destination):
 p=Path(destination).expanduser().resolve()
 if p==ROOT or ROOT in p.parents: raise ValueError('Choose an output outside this sealed packet')
 if p.exists(): raise ValueError('Output already exists; refusing to overwrite')
 data=(ROOT/ENCODED).read_bytes()
 if len(data)!=498413 or hashlib.sha256(data).hexdigest()!=ENCODED_HASH: raise ValueError('Encoded-byte integrity failure')
 compressed=base64.b64decode(b''.join(data.split()),validate=True)
 if len(compressed)!=368954: raise ValueError('Compressed-byte size failure')
 original=gzip.decompress(compressed)
 if len(original)!=27522877 or hashlib.sha256(original).hexdigest()!=ORIGINAL_HASH: raise ValueError('Original-byte integrity failure')
 with p.open('xb') as f: f.write(original)
 if p.read_bytes()!=original: raise ValueError('Restored disk bytes differ')
 return {'status':'PASS','restored_path':str(p),'bytes':len(original),'sha256':ORIGINAL_HASH,'packet_modified':False}
if __name__=='__main__':
 try:
  if len(sys.argv)!=2: raise ValueError('Usage: python restore_controls.py /path/outside/packet/NEGATIVE_CONTROLS.json')
  print(json.dumps(restore(sys.argv[1]),indent=2))
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)})); sys.exit(1)
