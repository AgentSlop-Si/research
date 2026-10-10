"""Fresh independent controls; never imports predecessor or candidate research code.
These are finite falsification checks, not certification of transcendental coefficients
or an implementation/benchmark of the asymptotic production algorithm.
"""
import json, math, random
from fractions import Fraction
from pathlib import Path
import numpy as np

rng = random.Random(10101356)
summary = {}

# Exact combinatorial catalogue: actual vectors versus proposed O(1) family/ID.
pattern_cases = 0
vectors = 0
max_count_over_Q = 0.0
for v in range(2, 13):
    N = 1 << v
    for k in range(v + 1):
        P = 1 << k
        for g in range(1, 9):
            Q = 1 << g
            catalog = {}
            stage_specific_count = 0
            for ell in range(k + 1, v + 1):
                L = 1 << ell
                stage = {}
                for j0 in range(0, L // 2, P):
                    truth = tuple((Q * (j0 + s)) // L for s in range(P))
                    h = (Q * j0) // L
                    if ell <= g:
                        family = ('progression', g - ell)
                        predicted = tuple(h + (s << (g - ell)) for s in range(P))
                    elif ell < g + k:
                        family = ('repeated', ell - g)
                        predicted = tuple(h + (s >> (ell - g)) for s in range(P))
                    else:
                        family = ('constant', 0)
                        predicted = (h,) * P
                    assert truth == predicted, (v, k, g, ell, j0)
                    key = family, h
                    if key in catalog:
                        assert catalog[key] == truth
                    catalog[key] = truth
                    stage[key] = truth
                    vectors += 1
                stage_specific_count += len(stage)
            # Across all three regimes, < 2Q distinct family/starting-index labels.
            assert len(catalog) <= 2 * Q, (v, k, g, len(catalog), Q)
            max_count_over_Q = max(max_count_over_Q, len(catalog) / Q)
            pattern_cases += 1
summary['phase_catalogue'] = {'parameter_cases': pattern_cases, 'lane_vectors': vectors,
                            'largest_distinct_catalogue_over_Q': max_count_over_Q,
                            'all_exact_predictions_and_2Q_bound_passed': True}

# Reverse-bit chunk construction and exact placement into packed words.
permutation_cases = 0
for v in range(1, 15):
    N = 1 << v
    d = max(1, v // 4)
    R = [int(f'{z:0{d}b}'[::-1], 2) for z in range(1 << d)]
    def rev_chunks(i):
        out = 0
        full = (v + d - 1) // d
        for _ in range(full):
            out = (out << d) | R[i & ((1 << d) - 1)]
            i >>= d
        return out >> (full*d-v)
    for k in range(v + 1):
        P = 1 << k
        b = v
        words = [0] * (N // P)
        for j in range(N):
            q = rev_chunks(j)
            assert q == int(f'{j:0{v}b}'[::-1], 2)
            words[q >> k] |= j << (b * (q & (P-1)))
        out = [(words[q >> k] >> (b*(q & (P-1)))) & ((1 << b)-1) for q in range(N)]
        assert out == [rev_chunks(j) for j in range(N)]
        permutation_cases += 1
summary['bit_reversal'] = {'layout_cases': permutation_cases, 'passed': True,
                          'note': 'Toy words may exceed hardware width; width proof is analytic.'}

# GENUINE eagerly enumerated P=2 complex tables, tiny p=0 one-exponent alphabet.
# Each complex code has b=4 bits; all 2^16 two-word keys are enumerated.
P, b, Q = 2, 4, 8
A = 11  # root approximation 11/16, used only for exact layout controls
W = [(round(16*math.cos(-2*math.pi*h/Q)), round(16*math.sin(-2*math.pi*h/Q))) for h in range(Q)]
def decode4(c):
    def real(r):
        return 0 if (r & 1) == 0 else (-1 if r & 2 else 1)
    return real(c & 3), real(c >> 2)
def quant4_scalar(n):
    return 0 if abs(n) < 256 else 1 | (2 if n < 0 else 0)
def bf4(a, c, h):
    ar, ai = decode4(a); cr, ci = decode4(c); wr, wi = W[h]
    tr, ti = wr*cr-wi*ci, wr*ci+wi*cr
    vals = [A*(16*ar+tr), A*(16*ai+ti), A*(16*ar-tr), A*(16*ai-ti)]
    q = [quant4_scalar(z) for z in vals]
    return q[0] | q[1] << 2, q[2] | q[3] << 2

def build_cross(pattern):
    keys = np.arange(1 << 16, dtype=np.uint64)
    out = np.zeros(keys.shape, dtype=np.uint64)
    for lane, h in enumerate(pattern):
        ca = ((keys >> (4*lane)) & 15).astype(np.int64)
        cb = ((keys >> (8+4*lane)) & 15).astype(np.int64)
        ar = np.where(ca & 1, np.where(ca & 2, -1, 1), 0)
        ai = np.where(ca & 4, np.where(ca & 8, -1, 1), 0)
        cr = np.where(cb & 1, np.where(cb & 2, -1, 1), 0)
        ci = np.where(cb & 4, np.where(cb & 8, -1, 1), 0)
        wr, wi = W[h]
        tr, ti = wr*cr-wi*ci, wr*ci+wi*cr
        nums = [A*(16*ar+tr), A*(16*ai+ti), A*(16*ar-tr), A*(16*ai-ti)]
        qs = [np.where(abs(z) < 256, 0, 1 + 2*(z<0)).astype(np.uint64) for z in nums]
        out |= (qs[0] | qs[1] << 2) << (4*lane)
        out |= (qs[2] | qs[3] << 2) << (8+4*lane)
    return out
patterns = {(0,2), (1,3), (0,1), (2,3), (0,0), (1,1), (2,2), (3,3)}
tables = {pat: build_cross(pat) for pat in patterns}
# Scalar check of every eager key in every table, including noncanonical zero codes.
for pat, table in tables.items():
    for key in range(1 << 16):
        expected = 0
        for lane, h in enumerate(pat):
            c, d = bf4((key >> (4*lane)) & 15, (key >> (8+4*lane)) & 15, h)
            expected |= c << (4*lane)
            expected |= d << (8+4*lane)
        assert int(table[key]) == expected
small = []
for key in range(256):
    c, d = bf4(key & 15, key >> 4, 0)
    small.append(c | d << 4)
executions = 0
for v in range(2, 9):
    N = 1 << v
    for trial in range(30):
        src = [rng.randrange(16) for _ in range(N)]
        a = [src[int(f'{j:0{v}b}'[::-1],2)] for j in range(N)]
        words = [a[j] | a[j+1] << 4 for j in range(0, N, 2)]
        for ell in range(1, v+1):
            L = 1 << ell
            # Separate scalar DIT reference, with identical total dyadic maps.
            for base in range(0, N, L):
                for j in range(L//2):
                    a[base+j], a[base+j+L//2] = bf4(a[base+j], a[base+j+L//2], Q*j//L)
            if L <= P:
                words = [small[x] for x in words]
            else:
                for base in range(0, N, L):
                    for j in range(0, L//2, P):
                        ai = (base+j)//P; bi = (base+j+L//2)//P
                        pat = tuple(Q*(j+s)//L for s in range(P))
                        payload = int(tables[pat][words[ai] | words[bi] << 8])
                        words[ai], words[bi] = payload & 255, payload >> 8
            unpacked = [(words[j//2] >> (4*(j%2))) & 15 for j in range(N)]
            assert unpacked == a
        executions += 1
summary['eager_tables'] = {'P': 2, 'complex_state_bits': 4, 'cross_patterns':len(tables),
                         'exhaustively_checked_cross_entries': len(tables)*(1<<16),
                         'small_entries':256, 'packed_vs_scalar_executions': executions,
                         'all_stages_equal': True,
                         'note':'Tiny toy precision tests layout and total semantics, not target accuracy.'}

# p=1, E=2 alphabet: real field has padded exponent=3 invalid code and overflow.
def decode8(c):
    def real(code):
        f, e, s = code & 1, (code >> 1) & 3, code >> 3
        if e == 0 or e == 3: return Fraction(0)
        return (-1 if s else 1) * Fraction(2+f, 4 if e==1 else 2)
    return real(c & 15), real(c >> 4)
def q8(x):
    ax = abs(x)
    if ax < Fraction(1,2): return 0, False
    clip = ax >= 2
    if clip: return 1 | (2 << 1) | (8 if x<0 else 0), True
    e = 1 if ax < 1 else 2
    f = int(ax * (4 if e==1 else 2)) - 2
    return f | (e << 1) | (8 if x<0 else 0), False
invalid_codes = sum(1 for c in range(256) if ((c>>1)&3)==3 or ((c>>5)&3)==3)
clipping_responses = 0
for key in range(1 << 16):
    ar, ai = decode8(key & 255); br, bi = decode8(key >> 8)
    wr, wi = Fraction(11,16), Fraction(-11,16)
    tr, ti = wr*br-wi*bi, wr*bi+wi*br
    pre = [Fraction(11,16)*(ar+tr), Fraction(11,16)*(ai+ti),
           Fraction(11,16)*(ar-tr), Fraction(11,16)*(ai-ti)]
    output = [q8(z) for z in pre]
    clipping_responses += any(c for _,c in output)
    for z, (code, clipped) in zip(pre, output):
        qz = decode8(code)[0]
        assert abs(qz) <= Fraction(3,2)
        if not clipped: assert abs(qz-z) <= Fraction(1,2)*abs(z)+Fraction(1,2)
assert invalid_codes > 0 and clipping_responses > 0
summary['invalid_and_overflow'] = {'P':1, 'complex_state_bits':8, 'all_keys': 1<<16,
                                  'codes_with_padded_invalid_exponents':invalid_codes,
                                  'responses_requiring_total_clipping':clipping_responses,
                                  'nonclipping_quantizer_bound_passed':True}

# Accurate scalar-stage stress controls at the actual conservative p schedule.
# Coefficients use ordinary floating arithmetic here; analytic certificates are separate.
max_relative = 0.0
accuracy_cases = 0
for v in range(1, 9):
    N = 1 << v
    for t in [2,4,8]:
        eps = 2.0**(-t)
        p = math.ceil(math.log2(1024*(v+1)/eps)); u=2.0**(-p)
        Q = 1 << (p+8); tau = 2.0**(-v-p)
        def qr(x):
            if abs(x)<tau: return 0.0
            e=math.floor(math.log2(abs(x)))
            z=math.ldexp(math.floor(math.ldexp(abs(x),p-e)), e-p)
            return math.copysign(z,x)
        def qc(x): return complex(qr(x.real),qr(x.imag))
        inputs=[]
        impulse=np.zeros(N,dtype=complex); impulse[N//2]=1
        inputs += [impulse, np.ones(N,dtype=complex), (-1.0)**np.arange(N),
                   np.exp(2j*math.pi*np.arange(N)*(N//2-1)/N)]
        for _ in range(8):
            inputs.append(np.array([complex(rng.uniform(-1,1),rng.uniform(-1,1))*2.0**rng.randrange(-2*v-p,1) for j in range(N)]))
        for x in inputs:
            scale=2.0**(math.floor(math.log2(max(max(abs(z.real),abs(z.imag)) for z in x)))+1)
            a=x/scale
            z=[qc(a[int(f'{j:0{v}b}'[::-1],2)]) for j in range(N)]
            for ell in range(1,v+1):
                L=1<<ell
                for base in range(0,N,L):
                    for j in range(L//2):
                        h=Q*j//L
                        w=complex(math.cos(-2*math.pi*h/Q),math.sin(-2*math.pi*h/Q))
                        i=base+j; k=i+L//2; aa=z[i]; bb=w*z[k]
                        z[i]=qc((aa+bb)/math.sqrt(2)); z[k]=qc((aa-bb)/math.sqrt(2))
            truth=np.fft.fft(x)/math.sqrt(N)
            ratio=float(np.linalg.norm(np.array(z)*scale-truth)/np.linalg.norm(x))
            assert ratio <= eps, (v,t,ratio,eps)
            max_relative=max(max_relative,ratio/eps)
            accuracy_cases += 1
summary['numerical_accuracy_stress']={'cases':accuracy_cases,'largest_error_over_requested_tolerance':max_relative,
                                     'passed':True,'not_a_certified_root_or_roundoff_proof':True}
print(json.dumps(summary, indent=2))
Path(__file__).with_name('control_results.json').write_text(json.dumps(summary, indent=2)+'\n')
