#!/usr/bin/env python3
"""Fresh exact native-Newton sparse/shared dispatcher with elementary fallback.
No imported historical program. Every multiplication of arithmetic data goes
through Elementary.mul. Python * appears only in resource accounting, list
allocation, and small loop/index dimensions, not operand multiplication.
"""
from dataclasses import dataclass, field
from collections import Counter
import hashlib


def bits(a): return max(1, abs(a).bit_length())

def digest(a):
    return hashlib.sha256(bytes([int(a < 0)]) + abs(a).to_bytes((bits(a)+7)//8, 'little')).hexdigest()


@dataclass
class Elementary:
    work: Counter = field(default_factory=Counter)
    counts: Counter = field(default_factory=Counter)
    max_mul_bits: int = 0
    products: list = field(default_factory=list)

    def tick(self, kind, cost, count=1):
        self.work[kind] += cost; self.counts[kind] += count

    def add(self, a, b):
        self.tick('add', max(bits(a), bits(b))+1)
        return a+b

    def shift(self, a, k):
        assert k >= 0
        self.tick('shift', bits(a)+k)
        return a << k

    def mul(self, a, b):
        """Signed bitwise shift-and-add; no host large integer multiplication.
        Charged bound includes both repeated shifts and accumulator additions.
        """
        sign = -1 if (a < 0) != (b < 0) else 1
        a, b = abs(a), abs(b)
        if bits(a) < bits(b): a, b = b, a
        p, q = bits(a), bits(b)
        self.tick('schoolbook', 8*(p+q+1)*(q+1))
        self.max_mul_bits = max(self.max_mul_bits, p, q)
        self.products.append((p,q))
        out = 0; shift = 0
        while b:
            if b & 1: out += a << shift
            b >>= 1; shift += 1
        return sign*out

    def divmod(self, a, b):
        """Elementary nonnegative binary long division."""
        assert a >= 0 and b > 0
        p, q = bits(a), bits(b)
        self.tick('long_division', 8*(p+q+1)*(max(0,p-q)+1))
        rem=a; quotient=0
        for k in range(max(0,p-q),-1,-1):
            v=b << k
            if rem >= v: rem -= v; quotient |= 1 << k
        return quotient,rem

    def exact(self, a, b):
        sign = -1 if (a < 0) != (b < 0) else 1
        q,r=self.divmod(abs(a),abs(b))
        if r: raise ArithmeticError('nonexact division')
        return sign*q

    def mod(self, a, modulus):
        if modulus <= 0: raise ArithmeticError('nonpositive modulus')
        _,r=self.divmod(abs(a),modulus)
        return modulus-r if a < 0 and r else r

    def gcd(self, a, b):
        a,b=abs(a),abs(b)
        while b: _,r=self.divmod(a,b);a,b=b,r
        return a

    def inverse(self, a, mod):
        old_r,r=mod,self.mod(a,mod); old_t,t=0,1
        while r:
            q,rem=self.divmod(old_r,r)
            old_r,r=r,rem;old_t,t=t,self.add(old_t,-self.mul(q,t))
        if old_r != 1: raise ArithmeticError('not invertible')
        return self.mod(old_t,mod)

    def summary(self):
        return {'charged_bit_work':sum(self.work.values()), 'work_by_primitive':dict(self.work),
                'counts':dict(self.counts),'max_schoolbook_operand_bits':self.max_mul_bits,
                'schoolbook_calls':len(self.products)}


def binomial(x,j,E):
    a=1
    for h in range(1,j+1): a=E.exact(E.mul(a,x-h+1),h)
    return a


@dataclass
class Plan:
    rank: int
    point: int
    block_bits: int
    weights: tuple
    nodes: tuple
    rows: tuple
    interpolation: tuple


def native_plan(r,E):
    assert r >= 2
    L=1
    for j in range(1,r+1): L=E.mul(E.exact(L,E.gcd(L,j)),j)
    d=E.exact(L,r); k=0;modulus=1
    for p in range(2,r+1):
        if any(E.mod(p,h) == 0 for h in range(2,p)): continue
        q=1
        while True:
            nxt=E.mul(q,p)
            if E.mod(d,nxt):break
            q=nxt
        if q == 1: continue
        u=1
        while True:
            nxt=E.mul(u,p)
            if E.mod(L,nxt):break
            u=nxt
        residue=E.mod(-E.inverse(E.exact(L,u),q),q)
        correction=E.mod(E.mul(E.mod(residue-k,q),E.inverse(modulus,q)),q)
        k=E.add(k,E.mul(modulus,correction));modulus=E.mul(modulus,q)
    if d==1:k=1
    assert modulus==d and 1<=k<=max(1,d-1)
    P=E.add(1,E.mul(k,L));W=[1]
    for j in range(1,r+1):W.append(E.mul(W[-1],E.add(1,E.exact(P-1,j))))
    beta=E.exact(W[-1],d);s=beta.bit_length()-1
    # Build all possible dimension-only nodes once; exact minimax translation.
    b={x:tuple(((-1 if j%2 else 1)*binomial(x,j,E)) for j in range(r))
       for x in range(-(r-1),2*r-1)}
    norms={x:sum(abs(a) for a in row) for x,row in b.items()}
    a=min(range(r),key=lambda a:(max(norms[-a],norms[2*r-2-a]),a))
    xs=tuple(range(-a,2*r-1-a))
    target=-P-xs[0]
    iw=tuple(binomial(target,j,E) for j in range(2*r-1))
    return Plan(r,P,s,tuple(W[:-1]),xs,tuple(b[x] for x in xs),iw)


def valuation(a,E):
    assert a>0
    blob=a.to_bytes((a.bit_length()+7)//8,'little')
    E.tick('dense_scan',len(blob)*8)
    for i,v in enumerate(blob):
        if v: return (i<<3)+(v & -v).bit_length()-1
    raise AssertionError


def split_blocks(a,s,E):
    """Disjoint bounded byte windows; each s+7-bit window is extracted once."""
    blob=a.to_bytes((bits(a)+7)//8,'little');E.tick('dense_scan',len(blob)*16)
    out=[];mask=(1<<s)-1;length=max(1,(a.bit_length()+s-1)//s)
    for j in range(length):
        offset=j*s;start=offset//8;within=offset%8
        width=(within+s+7)//8
        value=int.from_bytes(blob[start:start+width],'little')
        out.append((value>>within)&mask)
    return out


def canonical(a,plan,E):
    c=[0]*plan.rank
    for j in range(plan.rank-1,-1,-1):c[j],a=E.divmod(a,plan.weights[j])
    assert a==0
    return tuple(c)


def evaluate(c,row,E):
    ans=0
    for a,b in zip(c,row):
        if a and b:ans=E.add(ans,E.mul(a,b))
    return ans


def interpolate(v,plan,E):
    row=list(v);answer=0
    for w in plan.interpolation:
        answer=E.add(answer,E.mul(row[0],w))
        row=[E.add(b,-a) for a,b in zip(row,row[1:])]
    return answer


def pack(row,w,E):
    assert w%8==0
    b=w//8;pos=bytearray(len(row)*b);neg=bytearray(len(row)*b)
    for i,v in enumerate(row):
        data=abs(v).to_bytes(b,'little');dest=neg if v<0 else pos
        dest[i*b:(i+1)*b]=data
    E.tick('packed_stream',len(pos)*24)
    return int.from_bytes(pos,'little')-int.from_bytes(neg,'little')


def unpack(value,w,length,bound,E):
    b=w//8;Q=1<<w;negative=value<0
    if negative:value+=1<<(w*length)
    if value<0 or value.bit_length()>w*length:raise ArithmeticError('allocation')
    data=value.to_bytes(length*b,'little');borrow=0;out=[]
    for j in range(length):
        v=int.from_bytes(data[j*b:(j+1)*b],'little')+borrow
        if v>=Q//2:v-=Q;borrow=1
        else:borrow=0
        if abs(v)>bound:raise ArithmeticError('bound')
        out.append(v)
    if borrow!=int(negative):raise ArithmeticError('final borrow')
    E.tick('packed_stream',length*w*4)
    return out


def assemble(coefficients,s,last,E):
    """Nonnegative binary carry, then one bounded byte write per output block.
    A sparse mapping has bounded size; the dense fallback supplies a list.
    No repeated shifts of either the full output or a shrinking s-bit buffer.
    """
    carry=0;digits=[];mask=(1<<s)-1
    is_dense=isinstance(coefficients,(list,tuple))
    for i in range(last+1):
        coefficient=coefficients[i] if is_dense else coefficients.get(i,0)
        value=E.add(coefficient,carry)
        if value<0:raise ArithmeticError('negative outer coefficient')
        digits.append(value&mask);carry=value>>s
    while carry:digits.append(carry&mask);carry >>= s
    data=bytearray((len(digits)*s+7)//8)
    for i,digit in enumerate(digits):
        offset=i*s;start=offset//8;within=offset%8
        chunk=(digit<<within).to_bytes((within+s+7)//8,'little')
        # Only the initial boundary byte can contain an earlier block's bits.
        data[start] |= chunk[0]
        data[start+1:start+len(chunk)]=chunk[1:]
    E.tick('dense_output',len(data)*24)
    return int.from_bytes(data,'little')


def slot_width(L,A,B,E):
    bound=E.mul(L,E.mul(A,B))
    return 8*max(1,(((bound<<1).bit_length()+7)//8)),bound


def intern(seq,item,E):
    # Bounded exact linear search; no hash assumptions in the theorem.
    for i,v in enumerate(seq):
        E.tick('certificate_compare',max(1,sum(bits(a) for a in item)))
        if v==item:return i
    seq.append(item);return len(seq)-1


def compile_sparse(a_blocks,b_blocks,plan,E,limit):
    supports=[[(i,v) for i,v in enumerate(bs) if v] for bs in (a_blocks,b_blocks)]
    if any(len(s)>limit for s in supports):return None
    leaves=[];sides=[]
    for support in supports:
        terms=[];common=0
        for k,v in support:
            c=canonical(v,plan,E);content=0
            for digit in c:content=E.gcd(content,digit)
            if content==0:raise ArithmeticError('empty occupied block')
            primitive=tuple(E.exact(d,content) for d in c)
            leaf=intern(leaves,primitive,E);terms.append([k,content,leaf])
            common=E.gcd(common,content)
        outer_shift=min(k for k,_,_ in terms)
        sides.append({'common_content':common,'outer_shift':outer_shift,
            'terms':[[k-outer_shift,E.exact(c,common),i] for k,c,i in terms]})
    products=[];edges=[]
    for ka,ca,ia in sides[0]['terms']:
        for kb,cb,ib in sides[1]['terms']:
            pair=tuple(sorted((ia,ib)));node=intern(products,pair,E)
            edges.append([ka+kb,node,E.mul(ca,cb)])
    return {'version':1,'rank':plan.rank,'point':plan.point,'block_bits':plan.block_bits,
        'nodes':list(plan.nodes),'leaves':[list(x) for x in leaves],
        'sides':sides,'product_nodes':[list(x) for x in products],'edges':edges}


def check_structure(cert,blocks,plan,E,limit):
    """Certificate checker: bind every represented block to the actual input.
    It does not call the compiler or trust declared support/maxima/content.
    """
    try:
        if cert['version']!=1 or cert['rank']!=plan.rank or cert['point']!=plan.point:return False
        if cert['block_bits']!=plan.block_bits or cert['nodes']!=list(plan.nodes):return False
        leaves=cert['leaves'];products=cert['product_nodes']
        if len(leaves)>2*limit or len(products)>limit*limit:return False
        for leaf in leaves:
            if len(leaf)!=plan.rank or any(type(z)!=int or z<0 for z in leaf):return False
            g=0
            for z in leaf:g=E.gcd(g,z)
            if g!=1:return False
        if len({tuple(p) for p in products})!=len(products):return False
        for p in products:
            if len(p)!=2 or p!=sorted(p) or any(type(i)!=int or i<0 or i>=len(leaves) for i in p):return False
        for side,bs in zip(cert['sides'],blocks):
            g=side['common_content'];offset=side['outer_shift'];terms=side['terms']
            if type(g)!=int or g<=0 or type(offset)!=int or offset<0 or len(terms)>limit:return False
            recovered={};coefficient_gcd=0
            for k,c,leaf_id in terms:
                if any(type(z)!=int for z in (k,c,leaf_id)) or k<0 or c<=0 or not 0<=leaf_id<len(leaves):return False
                k+=offset
                if k in recovered or k>=len(bs):return False
                scalar=E.mul(g,c);digits=[E.mul(scalar,z) for z in leaves[leaf_id]]
                value=0
                for z,w in zip(digits,plan.weights):value=E.add(value,E.mul(z,w))
                # Canonicality is checked separately, so alternate equal-value digit vectors cannot pass.
                if tuple(digits)!=canonical(bs[k],plan,E):return False
                recovered[k]=value;coefficient_gcd=E.gcd(coefficient_gcd,scalar)
            if coefficient_gcd!=g:return False
            if recovered!={i:v for i,v in enumerate(bs) if v}:return False
            if min(recovered)!=offset:return False
        if len(cert['sides'])!=2:return False
        expected=[]
        for ka,ca,ia in cert['sides'][0]['terms']:
            for kb,cb,ib in cert['sides'][1]['terms']:
                pair=sorted((ia,ib))
                if pair not in products:return False
                expected.append([ka+kb,products.index(pair),E.mul(ca,cb)])
        if expected!=cert['edges']:return False
        if set(e[1] for e in expected)!=set(range(len(products))):return False
        return True
    except (KeyError,TypeError,ValueError,IndexError,ArithmeticError):return False


def evaluate_shared(cert,blocks,plan,E):
    """Memoize normalized leaves, product nodes, and equal scalar products.
    All memo keys in this branch are polynomial-size; dense children stay virtual.
    """
    cache=[];hits=0;misses=0
    def smallmul(a,b):
        nonlocal hits,misses
        key=tuple(sorted((a,b)))
        for old,value in cache:
            E.tick('memo_compare',bits(a)+bits(b))
            if old==key:hits+=1;return value
        value=E.mul(a,b);cache.append((key,value));misses+=1;return value
    common=smallmul(cert['sides'][0]['common_content'],cert['sides'][1]['common_content'])
    combined={}
    for k,node,c in cert['edges']:
        key=(k,node);combined[key]=E.add(combined.get(key,0),c)
    scales={key:smallmul(common,c) for key,c in combined.items()}
    offset=cert['sides'][0]['outer_shift']+cert['sides'][1]['outer_shift']
    support=sorted({k+offset for k,_ in scales});column_values={k:[] for k in support}
    rows=[]
    for x,basis in zip(plan.nodes,plan.rows):
        values=[evaluate(leaf,basis,E) for leaf in cert['leaves']]
        ps=[smallmul(values[a],values[b]) for a,b in cert['product_nodes']]
        h={k:0 for k in support}
        for (k,node),scale in scales.items():h[k+offset]=E.add(h[k+offset],smallmul(scale,ps[node]))
        maxima=[];row_terms=[]
        for side in cert['sides']:
            terms=[]
            for k,c,i in side['terms']:
                v=smallmul(smallmul(side['common_content'],c),values[i]);terms.append([k+side['outer_shift'],v])
            row_terms.append(terms);maxima.append(max(abs(v) for _,v in terms))
        L=max(len(blocks[0]),len(blocks[1]));w,bound=slot_width(L,maxima[0],maxima[1],E)
        if not bound:w=0
        rows.append({'node':x,'input_terms':row_terms,'slot_bits':w,'bound':bound,
                     'product_terms':[[k,h[k]] for k in support]})
        for k in support:column_values[k].append(h[k])
    output={k:interpolate(v,plan,E) for k,v in column_values.items()}
    if any(v<0 for v in output.values()):raise ArithmeticError('invalid reconstructed column')
    execution={'rows':rows,'output_terms':[[k,v] for k,v in sorted(output.items())],
               'memo_hits':hits,'memo_misses':misses,'unique_scalar_products':len(cache),
               'symbolic_product_nodes':len(cert['product_nodes']),
               'edge_count_before_combining':len(cert['edges']),'edge_count_after_combining':len(scales)}
    return output,execution


def check_execution(cert,execution,blocks,plan,E):
    """Different direct sparse-convolution checker, no DAG evaluation/cache reuse.
    It verifies source row widths, every sparse convolution column, interpolation.
    """
    try:
        if len(execution['rows'])!=len(plan.nodes):return False
        values={}
        for record,x,basis in zip(execution['rows'],plan.nodes,plan.rows):
            if record['node']!=x:return False
            expected_rows=[]
            for bs in blocks:
                expected_rows.append([[k,evaluate(canonical(v,plan,E),basis,E)] for k,v in enumerate(bs) if v])
            if expected_rows!=record['input_terms']:return False
            A=max(abs(v) for _,v in expected_rows[0]);B=max(abs(v) for _,v in expected_rows[1])
            w,bound=slot_width(max(map(len,blocks)),A,B,E)
            if not bound:w=0
            if (w,bound)!=(record['slot_bits'],record['bound']):return False
            conv={}
            for i,a in expected_rows[0]:
                for j,b in expected_rows[1]:conv[i+j]=E.add(conv.get(i+j,0),E.mul(a,b))
            if [[k,v] for k,v in sorted(conv.items())]!=record['product_terms']:return False
            for k,v in conv.items():values.setdefault(k,[]).append(v)
        expected=[[k,interpolate(v,plan,E)] for k,v in sorted(values.items())]
        return expected==execution['output_terms']
    except (KeyError,TypeError,ValueError,IndexError,ArithmeticError):return False


class Dispatcher:
    def __init__(self,base_bits=1024,support_limit=4,verify=True,force_dense=False):
        if type(base_bits)!=int or type(support_limit)!=int or base_bits<8 or support_limit<1:raise ValueError('invalid parameters')
        self.base_bits=base_bits;self.limit=support_limit;self.verify=verify
        self.force_dense=force_dense;self.E=Elementary();self.plans={};self.stats=Counter();self.certificates=[]

    def plan(self,r):
        if r not in self.plans:self.plans[r]=native_plan(r,self.E)
        return self.plans[r]

    def multiply(self,a,b,depth=0):
        if type(a)!=int or type(b)!=int:raise TypeError('integer operands required')
        E=self.E;self.stats['calls']+=1;self.stats['max_depth']=max(self.stats['max_depth'],depth)
        if not a or not b:self.stats['zero']+=1;return 0
        sign=-1 if (a<0)!=(b<0) else 1;a,b=abs(a),abs(b)
        original_bits=max(bits(a),bits(b));ta=valuation(a,E);tb=valuation(b,E)
        E.tick('shift_extract',bits(a)+bits(b));a >>= ta;b >>= tb
        n=max(bits(a),bits(b))
        if ta or tb:self.stats['shift_extractions']+=1
        if n<=self.base_bits:
            self.stats['base']+=1;return sign*E.shift(E.mul(a,b),ta+tb)
        r=n.bit_length()-1;plan=self.plan(r);s=plan.block_bits
        ab=split_blocks(a,s,E);bb=split_blocks(b,s,E);blocks=(ab,bb)
        E.tick('support_recognition',sum(map(len,blocks))*max(1,s))
        sparse=None if self.force_dense else compile_sparse(ab,bb,plan,E,self.limit)
        if sparse is not None:
            if not check_structure(sparse,blocks,plan,E,self.limit):raise ArithmeticError('structural certificate rejected')
            output,execution=evaluate_shared(sparse,blocks,plan,E)
            if self.verify and not check_execution(sparse,execution,blocks,plan,E):raise ArithmeticError('execution certificate rejected')
            self.stats['sparse_shared']+=1
            result=assemble(output,s,max(output),E)
            self.certificates.append({'input_bits':original_bits,'core_bits':n,'sign':sign,
                'shifts':[ta,tb],'core_digests':[digest(a),digest(b)],'certificate':sparse,'execution':execution})
            E.tick('certificate_digest',bits(a)+bits(b))
            return sign*E.shift(result,ta+tb)
        self.stats['dense_fallback']+=1
        L=max(len(ab),len(bb));ab+= [0]*(L-len(ab));bb+=[0]*(L-len(bb))
        ac=[canonical(v,plan,E) for v in ab];bc=[canonical(v,plan,E) for v in bb]
        requests=[]
        for row in plan.rows:
            ar=[evaluate(c,row,E) for c in ac];br=[evaluate(c,row,E) for c in bc]
            A=max(map(abs,ar));B=max(map(abs,br))
            if not A or not B:requests.append(None);continue
            w,bound=slot_width(L,A,B,E);U=pack(ar,w,E);V=pack(br,w,E)
            requests.append((U,V,w,bound))
        if any(q and max(bits(q[0]),bits(q[1]))>=n for q in requests):
            self.stats['noncontracting_guard']+=1;return sign*E.shift(E.mul(a,b),ta+tb)
        columns=[]
        for q in requests:
            if q is None:self.stats['zero_rows']+=1;columns.append([0]*(2*L-1));continue
            U,V,w,bound=q;value=self.multiply(U,V,depth+1)
            columns.append(unpack(value,w,2*L-1,bound,E))
        out=[interpolate([row[k] for row in columns],plan,E) for k in range(2*L-1)]
        result=assemble(out,s,2*L-2,E)
        return sign*E.shift(result,ta+tb)

    def summary(self):return {'dispatcher':dict(self.stats),'backend':self.E.summary()}
