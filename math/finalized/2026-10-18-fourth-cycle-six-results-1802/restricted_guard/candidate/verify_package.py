import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
for row in manifest['files']:
 data=(root/row['path']).read_bytes()
 assert len(data)==row['bytes']
 assert hashlib.sha256(data).hexdigest()==row['sha256']
pins=json.loads((root/'SOURCE_PINS.json').read_text())
for row in pins['dependencies']:
 assert (root/row['local']).read_bytes()==pathlib.Path(row['source']).read_bytes()
for row in pins['source_reports']:
 data=pathlib.Path(row['source']).read_bytes()
 assert hashlib.sha256(data).hexdigest()==row['sha256']
result=dict(status='PASS',manifest_sha256=hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest(),
            payloads=len(manifest['files']),dependencies=len(pins['dependencies']),source_reports=len(pins['source_reports']))
(root/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
