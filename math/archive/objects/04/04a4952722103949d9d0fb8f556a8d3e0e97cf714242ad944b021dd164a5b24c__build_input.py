from phase31_rectangular import export_input
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('n',type=int);p.add_argument('outfile',type=Path);p.add_argument('--plant',action='store_true');a=p.parse_args()
print(json.dumps(export_input(a.outfile,a.n,plant=a.plant)))
