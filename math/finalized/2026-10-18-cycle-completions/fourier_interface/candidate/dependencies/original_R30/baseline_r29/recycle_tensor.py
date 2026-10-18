"""R29: liveness-compiled C tensor kernels. Attributed R28 / Alman-Rao graph.

Compile a scalar operation DAG to reusable byte-word slots. Every arithmetic
operation, exact-division guard, and signed-overflow guard is retained.
This is a tensor LEAF, not a cyclic FFT or an asymptotic exponent improvement.
"""
from dataclasses import dataclass
from pathlib import Path
import sys
import heapq
import struct

_FORMAT=struct.Struct("<BHHHBHH")
_OPS={"add":0,"neg":1,"divide":2,"left":3}
_NAMES=("add","neg","divide","left")
_NONE=65535

BASE = Path(__file__).resolve().parent / 'baseline_r28'
sys.path.insert(0,str(BASE))
import tensor_blocks as old
from tensor_blocks import Grid, Tape, Meter, copy, need, read_number, write_number

@dataclass(frozen=True)
class Step:
    op: str
    dest: int
    args: tuple
    shift: int
    free: tuple

@dataclass(frozen=True)
class Program:
    axes: int
    mode: str
    inverse: bool
    code: bytes
    outputs: tuple
    slots: int
    peak_live: int
    logical_words: int
    calls: dict

class Builder:
    def __init__(self,n):
        self.inputs=2*n
        self.ops=[]
    def emit(self,op,*args,k=0):
        dest=self.inputs+len(self.ops)
        self.ops.append((op,args,k))
        return dest
    def add(self,a,b):return self.emit('add',a,b)
    def neg(self,a):return self.emit('neg',a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def div(self,a,k):return self.emit('divide',a,k=k)
    def left(self,a,k):return a if k==0 else self.emit('left',a,k=k)
    def phase(self,z,k):
        r,i=z
        return self._phase(z,k%4)
    def _phase(self,z,k):
        r,i=z
        if k==0:return r,i
        if k==1:return self.neg(i),r
        if k==2:return self.neg(r),self.neg(i)
        return i,self.neg(r)

def _walsh(b,values,mode,scale=0):
    n=len(values);radix=4 if mode=='ar4' else 8
    if mode=='walsh' or n<radix:
        out=[b.left(a,scale) for a in values];h=1
        while h<n:
            for start in range(0,n,2*h):
                for j in range(h):
                    a,c=out[start+j],out[start+j+h]
                    out[start+j]=b.add(a,c)
                    out[start+j+h]=b.sub(a,c)
            h*=2
        return out
    size=n//radix
    subs=[_walsh(b,values[t*size:(t+1)*size],mode,scale+(t!=0)) for t in range(radix)]
    result=[None]*n
    for j in range(size):
        if radix==4:
            a,c,d,e=(v[j] for v in subs)
            tot=b.div(b.add(b.add(c,d),e),1);diff=b.sub(a,tot)
            vals=(b.add(a,tot),b.add(diff,d),b.add(diff,c),b.add(diff,e))
        else:
            a,c,d,e,f,g,h,i=(v[j] for v in subs)
            b1=b.add(c,d);b2=b.add(e,i);b3=b.add(g,h)
            tot=b.div(b.add(b.add(b.add(b1,b2),b3),f),1);diff=b.sub(a,tot)
            dd=b.add(diff,e);ee=b.add(diff,f);hh=b.add(diff,i)
            vals=(b.add(a,tot),b.add(b.add(ee,d),h),b.add(b.add(ee,c),g),b.add(ee,b2),
                  b.add(dd,b1),b.add(b.add(hh,d),g),b.add(b.add(hh,c),h),b.add(dd,b3))
        for t,v in enumerate(vals):result[t*size+j]=v
    return result

def compile_program(axes,mode='ar4',inverse=False):
    need(type(axes) is int and 0<=axes<=12,'compiler axes 0..12')
    need(mode in ('ar4','ar8','walsh'),'known Walsh kernel')
    need(type(inverse) is bool,'boolean inverse')
    n=1<<axes;b=Builder(n)
    values=[(2*j,2*j+1) for j in range(n)]
    if axes:
        sign=-1 if inverse else 1
        z=[b.phase(v,-sign*j.bit_count()) for j,v in enumerate(values)]
        re=_walsh(b,[v[0] for v in z],mode)
        im=_walsh(b,[v[1] for v in z],mode)
        half,odd=divmod(axes,2);outputs=[]
        for j,v in enumerate(zip(re,im)):
            r,i=b.phase(v,sign*(half-j.bit_count()))
            if odd:
                r,i=(b.sub(r,i),b.add(r,i)) if sign==1 else (b.add(r,i),b.sub(i,r))
            outputs.extend((b.div(r,half+odd),b.div(i,half+odd)))
    else:outputs=list(range(2*n))
    # Last-use compilation; output values remain live through serialization.
    m=len(b.ops);last=[-1]*(2*n+m)
    for t,(_,args,_) in enumerate(b.ops):
        for a in args:last[a]=t
    for a in outputs:last[a]=m
    need(all(x>=0 for x in last),'no dead arithmetic/input in this graph')
    node_slot={i:i for i in range(2*n)};free=[];capacity=2*n
    peak=live=2*n;code=bytearray();calls=dict(add=0,neg=0,divide=0,left=0)
    for t,(op,args,k) in enumerate(b.ops):
        argslots=tuple(node_slot[a] for a in args)
        dest=heapq.heappop(free) if free else capacity
        if dest==capacity:capacity+=1
        live+=1;peak=max(peak,live);node_slot[2*n+t]=dest
        releases=[]
        for a in set(args):
            if last[a]==t:
                slot=node_slot.pop(a);releases.append(slot);heapq.heappush(free,slot);live-=1
        calls[op]+=1
        rs=sorted(releases)
        code.extend(_FORMAT.pack(_OPS[op],dest,argslots[0],argslots[1] if len(argslots)>1 else _NONE,k,
                                 rs[0] if rs else _NONE,rs[1] if len(rs)>1 else _NONE))
    outs=tuple(node_slot[a] for a in outputs)
    need(len(set(outs))==2*n and live==2*n,'unique complete live outputs')
    return Program(axes,mode,inverse,bytes(code),outs,capacity,peak,2*n+m,calls)

class RecyclingGrid(Grid):
    """Original checked arithmetic; only allocation lifetime changes.

    release() wipes every dead bit-word once. close() wipes remaining outputs.
    This control proves memory savings without a faster arithmetic primitive.
    """
    def __init__(self,bits,fraction_bits):
        super().__init__(bits,fraction_bits)
        self.workspace={}
        self.released_words=0
    def track(self,word):
        key=id(word)
        need(key not in self.workspace,'word tracked once')
        self.workspace[key]=word
        self.peak_words=max(self.peak_words,len(self.workspace))
        return word
    def release(self,word):
        need(self.workspace.pop(id(word),None) is word,'live owned word')
        for i in range(len(word)):word[i]=0
        self.arithmetic_steps+=len(word);self.released_words+=1
    def close(self):
        for word in self.workspace.values():
            for i in range(len(word)):word[i]=0
            self.arithmetic_steps+=len(word);self.released_words+=1
        self.workspace.clear()

def execute_recycled(program,grid,values):
    need(isinstance(grid,RecyclingGrid),'recycling grid required')
    need(len(values)==1<<program.axes,'complete tensor fiber')
    slots=[None]*program.slots
    for j,z in enumerate(values):slots[2*j:2*j+2]=z
    values.clear()  # This internal entry point consumes its owned input-word list.
    # Do not retain a second reference to released input words in this function.
    for op,dest,ia,ib,k,free1,free2 in _FORMAT.iter_unpack(program.code):
        a=slots[ia]
        if op==0:out=grid.add(a,slots[ib])
        elif op==1:out=grid.neg(a)
        elif op==2:out=grid.divide(a,k)
        else:out=old.shift_left(grid,a,k)
        slots[dest]=out
        for slot in (free1,free2):
            if slot!=_NONE:
                grid.release(slots[slot]);slots[slot]=None
    return [(slots[program.outputs[2*j]],slots[program.outputs[2*j+1]]) for j in range(1<<program.axes)]

class Arena:
    """Reusable signed-bit words; no growing integer arithmetic or hidden FFT.

    Reads/writes are to resident word slots. This is not a fixed-tape machine.
    Slots are separately allocated bytearrays; each byte stores one logical bit.
    """
    def __init__(self,program,grid):
        self.program=program;self.grid=grid;self.w=grid.bits
        self.words=[grid.track(bytearray(self.w)) for _ in range(program.slots)]
        self.calls=dict(add=0,neg=0,divide=0,left=0)
    def load(self,values):
        need(len(values)==1<<self.program.axes,'complete tensor fiber')
        for j,z in enumerate(values):
            for t,word in enumerate(z):
                self.grid.check(word);self.words[2*j+t][:]=word
                self.grid.arithmetic_steps+=self.w
    def run(self):
        self.calls=dict(add=0,neg=0,divide=0,left=0)
        words=self.words;w=self.w;g=self.grid
        for op,dest,ia,ib,k,_free1,_free2 in _FORMAT.iter_unpack(self.program.code):
            a=words[ia];out=words[dest]
            self.calls[_NAMES[op]]+=1
            # dest never aliases any operand. Dead slots may be overwritten later.
            if op==0:
                b=words[ib];carry=0
                for j in range(w):
                    v=a[j]+b[j]+carry;out[j]=v&1;carry=v>>1
                g.arithmetic_steps+=8*w
                need(a[-1]!=b[-1] or out[-1]==a[-1],'signed addition headroom')
            elif op==1:
                carry=1
                for j in range(w):
                    v=1-a[j]+carry;out[j]=v&1;carry=v>>1
                g.arithmetic_steps+=6*w
                need(not(a[-1] and out[-1]),'signed negation headroom')
            elif op==2:
                need(0<=k<w,'binary division extent')
                need(not any(a[:k]),'division discards only reserved zero bits')
                out[:w-k]=a[k:];out[w-k:]=bytes((a[-1],))*k
                g.arithmetic_steps+=6*w;g.exact_divisions+=int(k>0)
            else:
                need(0<k<w,'left shift extent');sign=a[-1]
                need(all(bit==sign for bit in a[-(k+1):]),'left shift signed headroom')
                out[:k]=bytes(k);out[k:]=a[:w-k];g.arithmetic_steps+=6*w
        return [(words[self.program.outputs[2*j]],words[self.program.outputs[2*j+1]])
                for j in range(1<<self.program.axes)]


def c_block(source,address_bits,selected,coefficients,grid,inverse=False,outer_rows=1,
            mode='ar4',backend='arena',program=None):
    """Same <=8-axis sequential bucket layout as R28, with a smaller word arena.

    program=None charges compilation per call. Explicit supplied Program is a
    prepared-plan interface, and must match dimension, mode and direction.
    """
    axes=tuple(sorted(selected))
    need(type(address_bits) is int and address_bits>=0,'address bits')
    need(type(coefficients) is int and coefficients>=1 and type(outer_rows) is int and outer_rows>=1,'positive record shape')
    need(len(axes)<=8 and len(set(axes))==len(axes) and all(type(a)is int and 0<=a<address_bits for a in axes),'bounded distinct axes')
    need(mode in ('ar4','ar8','walsh'),'known Walsh kernel')
    need(backend in ('arena','recycle'),'known memory backend')
    need(type(inverse) is bool,'boolean inverse')
    need(len(source.data)==outer_rows*(1<<address_bits)*2*grid.bits*coefficients,'complete C payload')
    if not axes:return source
    if program is None:program=compile_program(len(axes),mode,inverse)
    need(isinstance(program,Program) and (program.axes,program.mode,program.inverse)==(len(axes),mode,inverse),'matching compiled program')
    if backend=='recycle':need(isinstance(grid,RecyclingGrid),'recycling grid required')
    n=1<<len(axes);record=2*grid.bits*coefficients
    routes=[]
    for addr in range(1<<address_bits):
        key=0
        for p in axes:key=(key<<1)|((addr>>(address_bits-1-p))&1)
        routes.append(key)
    source.rewind();buckets=[Tape(source.meter) for _ in range(n)]
    for _ in range(outer_rows):
        for route in routes:copy(source,buckets[route],record)
    source.finish()
    for t in buckets:t.rewind()
    outputs=[Tape(source.meter) for _ in range(n)]
    fibers=outer_rows*(1<<(address_bits-len(axes)))*coefficients
    if backend=='arena':arena=Arena(program,grid)
    for _ in range(fibers):
        if backend=='arena':
            # Tape.read supplies short-lived untracked buffers; copy into owned arena.
            for j,t in enumerate(buckets):
                for component in range(2):
                    word=t.read(grid.bits);grid.check(word)
                    arena.words[2*j+component][:]=word
                    grid.arithmetic_steps+=grid.bits
            answer=arena.run()
            if hasattr(grid,'program_calls'):
                for k,v in arena.calls.items():grid.program_calls[k]+=v
        else:
            values=[read_number(t,grid) for t in buckets]
            answer=execute_recycled(program,grid,values)
        for t,v in zip(outputs,answer):write_number(t,v)
        if backend=='recycle':grid.close()
        del answer, v
    if backend=='arena':
        grid.close();del arena
    for t in buckets:t.finish();t.erase()
    for t in outputs:t.rewind()
    result=Tape(source.meter)
    for _ in range(outer_rows):
        for route in routes:copy(outputs[route],result,record)
    for t in outputs:t.finish();t.erase()
    source.erase();result.rewind();return result


def c_tensor(source,address_bits,selected,coefficients,grid,inverse=False,outer_rows=1,
             mode='ar4',max_block=8,backend='arena',programs=None):
    axes=tuple(selected)
    need(type(max_block)is int and 1<=max_block<=8,'block size 1..8')
    need(type(address_bits)is int and address_bits>=0,'address bits')
    need(len(set(axes))==len(axes) and all(type(a)is int and 0<=a<address_bits for a in axes),'valid distinct selected axes')
    # Source compilation once per distinct width in a complete call; no answer cache.
    local={} if programs is None else programs
    for start in range(0,len(axes),max_block):
        block=axes[start:start+max_block];key=(len(block),mode,inverse)
        if key not in local:local[key]=compile_program(*key)
        source=c_block(source,address_bits,block,coefficients,grid,inverse,outer_rows,mode,backend,local[key])
    if not axes:source=c_block(source,address_bits,(),coefficients,grid,inverse,outer_rows,mode,backend)
    return source

if __name__=='__main__':
    for d in (2,4,6,8,10,12):
        for mode in ('ar4','ar8'):
            p=compile_program(d,mode)
            print(d,mode,p.logical_words,p.slots,p.peak_live,p.calls,flush=True)
