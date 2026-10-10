"""Adversarial toy demo for bounded-printer conditioned radix selection.

This is NOT a proof of the Fourier theorem. It checks the selector logic under
deliberately terrible print times and local condition bounds, using k=log2(N)
so astronomical N is represented only by the integer k.
"""
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass(frozen=True)
class Record:
    idx:int; b:int; print_steps:int; khat:int; rho:float


def make_records(count=6):
    out=[]
    for t in range(1,count+1):
        out.append(Record(
            idx=t,
            b=t+1,
            print_steps=2**(t*t+2),
            khat=2**(2**t),
            rho=1/(t+1),
        ))
    return out


def budget_R_from_k(k:int)->int:
    # R(N)=floor(log2 log2 N) when k=log2 N.
    return max(2,k.bit_length()-1)


def select(records,k:int):
    R=budget_R_from_k(k)
    eligible=[]
    for r in records:
        m=1<<r.b
        if r.print_steps>k: continue
        if m*m>k: continue
        if r.khat>R: continue
        eligible.append(r)
    return (eligible[-1] if eligible else None),R


def main():
    records=make_records()
    # k = 2^p, hence R ~= p.  The last probe is big enough to admit record 4
    # despite Khat_4 = 2^16 = 65536.
    p_values=[20,80,300,700,3000,70000]
    rows=[]
    for p in p_values:
        k=1<<p
        rec,R=select(records,k)
        rows.append({
            'p_log2_k':p,
            'k_bit_length':k.bit_length(),
            'condition_budget_R':R,
            'selected_record':None if rec is None else rec.idx,
            'selected_b':None if rec is None else rec.b,
            'selected_rho':None if rec is None else rec.rho,
        })
    path=Path(__file__).with_name('bounded_printer_selector_demo.json')
    path.write_text(json.dumps(rows,indent=2))
    for row in rows: print(row)
    print('wrote',path)

if __name__=='__main__': main()
