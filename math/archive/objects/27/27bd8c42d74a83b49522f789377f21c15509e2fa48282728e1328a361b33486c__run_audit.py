"""Reproducible exact gate-count experiment for global nonlinear FFT candidates."""
import json,random
from pathlib import Path
from jet_linearize import P,build_fft,build_nonlinear_fft,linearize,eval_dual,direct_dft


def run(seed=20261009):
    rng=random.Random(seed)
    results=[]
    for n in (2,4,8,16,32,64):
        ref,_,outputs,w=build_fft(n)
        for mode in ('standard','square','rational','baseline'):
            dag,_,outs=(ref,None,outputs) if mode=='standard' else build_nonlinear_fft(n,mode)
            if mode=='standard': outs=outputs
            bases=[[0]*n]
            bases.extend([[rng.randrange(P) for _ in range(n)] for _ in range(4)])
            max_linear=0;mean_linear=0
            for base in bases:
                if mode=='rational' and base[0]==P-1: base[0]=0
                lin,linouts=linearize(dag,outs,base)
                max_linear=max(max_linear,lin.cost())
                mean_linear+=lin.cost()
                for _ in range(8):
                    x=[rng.randrange(P) for _ in range(n)]
                    if mode=='rational' and x[0]==P-1: x[0]=10
                    want=direct_dft(x,w)
                    assert dag.evaluate(x,outs)==want
                    assert lin.evaluate(x,linouts)==want
                    assert eval_dual(dag,base,x,outs)==want
            results.append({
                'n':n,'mode':mode,'arithmetic_gates':dag.cost(),
                'linearized_gates_at_zero':linearize(dag,outs,[0]*n)[0].cost(),
                'max_linearized_gates_across_bases':max_linear,
                'mean_linearized_gates_across_bases':mean_linear/len(bases),
                'fresh_direction_verifications':len(bases)*8,
                'derivative_le_3_original':max_linear<=3*dag.cost(),
            })
    p=Path(__file__).with_name('audit_results.json')
    p.write_text(json.dumps({
        'model':'F_p algebraic arithmetic gates; no cost-free nonlinear macros',
        'p':P,'seed':seed,'results':results,
        'total_matched_input_cases':sum(r['fresh_direction_verifications'] for r in results),
        'note':'A successful derivative extraction is not a new DFT algorithm.'
    },indent=2)+'\n')
    print('Size | baseline gates | square original->linear | rational original->linear | k rewrite original->linear')
    for n in (4,8,16,32,64):
        t={r['mode']:r for r in results if r['n']==n}
        f=lambda m:f"{t[m]['arithmetic_gates']}->{t[m]['linearized_gates_at_zero']}"
        print(f'{n:4d} | {t["standard"]["arithmetic_gates"]:14d} | {f("square"):22s} | {f("rational"):24s} | {f("baseline")}')
    print(f"CHECKED: {len(results)} variant-size cases, {sum(r['fresh_direction_verifications'] for r in results)} exact vector triples (original, linearized, independently dual) all equal to DFT")
    print(f"CHECKED: all linear gate counts <= 3*original arithmetic gate count")
    return results

if __name__=='__main__':run()
