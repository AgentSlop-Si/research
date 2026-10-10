"""Verify source hashes bundled in SHA256SUMS.txt (standard library only)."""
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    count=0
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        if not line.strip():continue
        digest, rel=line.split('  ',1)
        item=ROOT/rel
        assert item.is_file(),f'missing: {rel}'
        assert sha256(item.read_bytes()).hexdigest()==digest,f'corrupt: {rel}'
        count+=1
    print(f'{count} file hashes verified')

if __name__=='__main__':main()
