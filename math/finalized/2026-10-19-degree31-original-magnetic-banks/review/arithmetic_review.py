#!/usr/bin/env python3
"""Independent arithmetic and source-binding review; imports only our new checker."""
import argparse, hashlib, json, random, runpy
from pathlib import Path
M = runpy.run_path(str(Path(__file__).with_name('literal_review.py')))
F, P, D, O, Z, Q = M['Field'], M['P'], M['D'], M['ONE'], M['ZERO'], M['ORDER']
require = M['require']

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def blob(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--output', type=Path, default=Path('ARITHMETIC_REVIEW.json'))
    args = ap.parse_args(); c = args.candidate
    mod = [11, 2] + [0] * 29 + [1]
    f = F(mod)
    field_receipt = json.loads((c/'FIELD_IRREDUCIBILITY.json').read_text())
    require(field_receipt['modulus_ascending'] == mod, 'selected modulus')
    require(field_receipt['all_frobenius_remainders'] == f.field_proof['frobenius_remainders'], 'all 31 Frobenius residues')
    require(field_receipt['gcd_with_X53_minus_X'] == [1], 'irreducibility gcd receipt')
    probe = json.loads((c/'ARITHMETIC_PROBE.json').read_text())
    require(int(probe['order']) == Q and probe['bits'] == Q.bit_length() == 178, '178-bit order')
    mask = 2**128 - 1
    require(int(probe['wrapped_order']) == Q & mask and Q & mask != Q, 'wrapped-order negative control')
    a, b = map(tuple, (probe['a'],probe['b']))
    require(f.mul(a,b) == tuple(probe['a_times_b']), 'C++ field multiplication')
    require(f.inverse(a) == tuple(probe['inverse']), 'C++ inversion versus Euclid')
    exponents = [2**128-1, 2**128, 2**128+1, 2**127-1, 2**127, Q-2, Q-1, Q, (Q+3)//8, (Q-1)//2]
    require([int(row['exponent']) for row in probe['power_cases']] == exponents, 'exact exponent list')
    powers = []
    for row, e in zip(probe['power_cases'], exponents):
        val = f.power(a,e)
        require(val == tuple(row['value']), 'arbitrary precision element power')
        powers.append({'exponent':str(e),'value':list(val)})
    require(f.power(a,2**128) != O and f.power(a,Q) != f.power(a,Q&mask), 'power truncation detects change')
    h = list(map(tuple,probe['split_polynomial']))
    roots = [f.add(a,f.scalar(j)) for j in range(1,8)]
    require(len(h)==8 and h[-1]==O and len(set(roots))==7,'seven-root probe polynomial')
    def peval(poly,x):
        z=Z
        for coeff in reversed(poly): z=f.add(f.mul(z,x),tuple(coeff))
        return z
    require(all(peval(h,x)==Z for x in roots),'known probe factorization')
    # A degree <7 residue is uniquely determined by its seven values at
    # these distinct roots. This independently checks polynomial powering
    # without reproducing candidate polynomial modular exponentiation.
    polynomial_checks=[]
    for key,e,base in [('exact_split',Q,[Z,O]),('wrapped_split',Q&mask,[Z,O]),
                       ('exact_factor_power',(Q-1)//2,probe['factor_base']),
                       ('truncated_factor_power',((Q-1)//2)&mask,probe['factor_base'])]:
        remainder=probe[key]
        require(1<=len(remainder)<=7,'bounded polynomial residue degree')
        for coeff in remainder: f.element(coeff)
        values=[]
        for x in roots:
            actual=peval(remainder,x);expected=f.power(peval(base,x),e)
            require(actual==expected,'polynomial powers verified by evaluation uniqueness')
            values.append(list(actual))
        polynomial_checks.append({'key':key,'exponent':str(e),'seven_evaluation_values':values})
    require(probe['exact_split']==[list(Z),list(O)] and probe['wrapped_split']!=probe['exact_split'],'splitting exponent negative control')
    require(all(f.mul(peval(probe['exact_factor_power'],x),peval(probe['exact_factor_power'],x))==O for x in roots),'factor characters')
    require(any(f.mul(peval(probe['truncated_factor_power'],x),peval(probe['truncated_factor_power'],x))!=O for x in roots),'factor exponent negative control')
    require(f.mul(tuple(probe['exact_sqrt']),tuple(probe['exact_sqrt']))==tuple(probe['square']),'sqrt exact result')
    require(f.mul(tuple(probe['truncated_sqrt']),tuple(probe['truncated_sqrt']))!=tuple(probe['square']),'sqrt exponent negative control')
    require(f.mul(a,tuple(probe['truncated_inverse']))!=O,'inverse exponent negative control')
    require(Q%8==5 and 23*23%P==P-1,'sqrt parameters')
    for name,e in [('inverse',Q-2),('sqrt',(Q+3)//8),('factor',(Q-1)//2)]:
        require(e>mask and int(probe['exponent_low128'][name])==e&mask,'large derived exponent')
    # Generic division checks the production-style reduction, including every
    # basis pair, deterministic dense pairs, and the all-52 worst case.
    basis=[tuple(int(i==j) for i in range(D)) for j in range(D)]
    rng=random.Random(202610192745)
    pairs=[(a,b) for a in basis for b in basis]
    pairs += [(tuple(rng.randrange(P) for _ in range(D)),tuple(rng.randrange(P) for _ in range(D))) for _ in range(100)]
    worst=(P-1,)*D;pairs.append((worst,worst))
    for a,b in pairs:
        generic=M['divrem'](M['polymul'](a,b),mod)[1]
        generic=tuple(generic+[0]*(D-len(generic)))
        require(f.mul(a,b)==generic,'ordinary convolution versus generic long division')
    raw=[(min(k+1,2*D-1-k,D))*(P-1)**2 for k in range(2*D-1)]
    require(max(raw)==83824 and 2**16<=max(raw)<2**17,'degree31 carry boundary')
    packed=sum((P-1)<<(16*i) for i in range(D))**2
    unpacked=[(packed>>(16*i))&65535 for i in range(2*D-1)]
    require(raw!=unpacked,'unsafe 16-bit raw convolution corruption')
    good=M['divrem'](raw,mod)[1];bad=M['divrem'](unpacked,mod)[1]
    require(good!=bad,'unsafe 16-bit reduced field corruption')
    reduced=raw[:]
    for k in range(2*D-2,D-1,-1):
        reduced[k-D]-=11*reduced[k]
        reduced[k-D+1]-=2*reduced[k]
    bound=(1+11+2)*83824
    require(bound==1173536 and max(map(abs,reduced))<=bound<2**31,'signed C++ reduction bound')
    source=(c/'search_degree31.cpp').read_text()
    verifier=(c/'verify_literal.cpp').read_text()
    required=['using Big=mpz_class;', 'F power(Big e)const', 'Poly powmod(Poly x,Big e,const Poly&h)',
        'return power(ORDER-2);', 'powmod({F(0),F(1)},ORDER,h)', 'd.power((ORDER+3)/8)',
        'c[i-D]-=11*c[i];c[i-D+1]-=2*c[i];', 'uint64_t rng=202610192024ULL;']
    for token in required: require(token in source,'unbounded exponent/source path: '+token)
    require('powmod(r,(ORDER-1)/2,h)' in verifier,'unbounded factorization exponent')
    require('get_ui(' not in source+verifier and '__int128' not in source+verifier,'no narrowing active exponent conversion')
    require('limit>100000' in source and 'if(splits){hit=true' in source,'bounded first-hit search controls')
    known={'search_degree29.cpp':('cff1a29b7ef8e79f8142b53c29ec3ccb796dd345b72d7c402663fba38fd5fbd7','da2e096377c2f7447f8d793a878f2b0a628d20c1'),
      'verify_literal.cpp':('6dfbf846c580940adac51ab5bcc28cd9ee3d9d99ff5bf1d9c0075107817a5ee5','43c62fec3d05ab04b48e4c58dc204115a70f6264'),
      'independent_literal_check.py':('15f01f5ba3843f8adc418995ecfd921380d531372969917d1d443b394d8a65f2','6e16418f4f6ab8bb93b63bb4fa6c5d2d32cbd851')}
    for name,(h,b) in known.items():
        raw=(c/'sources'/name).read_bytes();require(hashlib.sha256(raw).hexdigest()==h and blob(raw)==b,'published source pin')
    pinned=[]
    for entry in json.loads((c/'SOURCE_PINS.json').read_text())['sources']:
        path=c/entry['copy']; raw=path.read_bytes()
        require(len(raw)==entry['bytes'] and sha(path)==entry['sha256'] and blob(raw)==entry['git_blob_sha1'],'local dependency pin')
        origin=Path(entry['original_path'])
        if origin.exists(): require(raw==origin.read_bytes(),'source copy equality')
        pinned.append(entry)
    out={'verdict':'PASS','field_order':str(Q),'order_bits':178,'field_proof':f.field_proof,
        'source_pins':pinned,'exact_power_cases':powers,'polynomial_power_checks':polynomial_checks,
        'polynomial_method':'Distinct-root evaluation uniqueness, different from modular polynomial powering',
        'differential_field_products':len(pairs),'ordinary_raw_convolution_max':83824,
        'signed_reduction_bound':bound,'reduction_no_high_feedback':True,
        'unsafe16_raw_corruption':True,'unsafe16_reduced_corruption':True,
        'correct_worst_product':good,'incorrect_16bit_product':bad,
        'negative_controls':['wrapped order','2^128 power wraps to zero','inverse exponent','splitting exponent','sqrt exponent','factor exponent'],
        'active_cpp_unbounded_exponents_audited':True,'source_hashes':{name:sha(c/name) for name in ['search_degree31.cpp','verify_literal.cpp','arithmetic_probe.cpp','ARITHMETIC_PROBE.json','FIELD_IRREDUCIBILITY.json','SOURCE_PINS.json']}}
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: irreducibility; 178-bit powers; 1,062 product comparisons; six exponent and two convolution negative controls.')
if __name__=='__main__':main()
