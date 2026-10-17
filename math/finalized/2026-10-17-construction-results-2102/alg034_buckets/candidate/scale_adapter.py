"""Bounded live exact producer -> normalized constant source -> theorem BUCKETS.

No certificate, digest, or supplied constant payload substitutes for executing
our pinned structured producer on separately supplied original raw/state data.
"""
from dataclasses import dataclass
from hashlib import sha256
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import json
import sys
from constant_buckets import ConstantBucketEngine, Failure, M_FIXED

PRODUCER_PIN='9bbd77a44f8a265f170b1993b63cae71d8f5a8da9f108a85d68b2a7719fca717'
BASE=Path(__file__).resolve().parent
PACKET_SCHEMA='ALG034_Q16_THEOREM_CONSTANT_BOUND_V1'
MAX_JSON_BYTES=8*1024*1024
MAX_TREE_NODES=500_000
MAX_TREE_DEPTH=16
MAX_SERIALIZED_INTEGER_BITS=4096
# Fixed uniform envelopes for the strictly bounded canonicalizer, parser,
# encoding/copy/hash/compare work, and trusted-source parsing/loading.
CANONICAL_BIT_WORK=1<<90
CANONICAL_STORAGE_BITS=1<<44
DEPENDENCY_BIT_WORK=1<<75
DEPENDENCY_STORAGE_BITS=1<<42


def load_producer():
    path=BASE/'vendor'/'structured_producer.py'
    data=path.read_bytes()
    if sha256(data).hexdigest()!=PRODUCER_PIN:
        raise Failure('DEPENDENCY_PIN: structured producer')
    name='alg034_scale_pinned_structured_producer'
    if name in sys.modules:
        module=sys.modules[name]
        if getattr(module,'_verified_source_pin',None)!=PRODUCER_PIN:
            raise Failure('DEPENDENCY_IDENTITY: structured producer')
    else:
        spec=spec_from_file_location(name,path)
        module=module_from_spec(spec);sys.modules[name]=module
        spec.loader.exec_module(module)
        module._verified_source_pin=PRODUCER_PIN
    return module,len(data)


def canonical(obj):
    """Bound the full tree before encoding; no unknown hooks or coercions."""
    nodes=0; budget=MAX_JSON_BYTES
    def visit(v,depth=0):
        nonlocal nodes,budget
        nodes+=1
        if nodes>MAX_TREE_NODES or depth>MAX_TREE_DEPTH:
            raise Failure('RESOURCE_LIMIT: canonical tree')
        kind=type(v)
        if v is None or kind is bool: budget-=5
        elif kind is int:
            bits=abs(v).bit_length()
            if bits>MAX_SERIALIZED_INTEGER_BITS:
                raise Failure('RESOURCE_LIMIT: serialized integer')
            budget-=bits*30103//100000+2
        elif kind is str:
            if len(v)>2048: raise Failure('RESOURCE_LIMIT: serialized text')
            budget-=2+12*len(v)
        elif kind is list:
            if len(v)>131072: raise Failure('RESOURCE_LIMIT: serialized list')
            budget-=2+len(v)
            for x in v: visit(x,depth+1)
        elif kind is dict:
            if len(v)>64: raise Failure('RESOURCE_LIMIT: serialized mapping')
            budget-=2+2*len(v)
            for k,x in v.items():
                if type(k) is not str: raise Failure('GRAMMAR: mapping keys')
                visit(k,depth+1);visit(x,depth+1)
        else: raise Failure('GRAMMAR: unsupported canonical type')
        if budget<0: raise Failure('RESOURCE_LIMIT: canonical bytes')
    visit(obj)
    data=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
    if len(data)>MAX_JSON_BYTES: raise Failure('RESOURCE_LIMIT: encoded bytes')
    return data


def strict_loads(text):
    if type(text) is not str or len(text)>MAX_JSON_BYTES:
        raise Failure('GRAMMAR_OR_RESOURCE: bounded JSON text required')
    try:
        if len(text.encode('utf8'))>MAX_JSON_BYTES:
            raise Failure('RESOURCE_LIMIT: JSON UTF8 bytes')
    except UnicodeEncodeError:
        raise Failure('GRAMMAR: unpaired Unicode surrogate')
    def integer(s):
        if len(s.lstrip('-'))>1234: raise Failure('RESOURCE_LIMIT: JSON integer digits')
        return int(s)
    def bad(s): raise Failure('GRAMMAR: noninteger JSON number')
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise Failure('GRAMMAR: duplicate JSON key')
            out[k]=v
        return out
    try:
        out=json.loads(text,parse_int=integer,parse_float=bad,parse_constant=bad,object_pairs_hook=pairs)
    except (json.JSONDecodeError,RecursionError):
        raise Failure('GRAMMAR: invalid JSON')
    canonical(out)
    return out

@dataclass(frozen=True)
class IntegratedRun:
    header_bytes: bytes
    numerators: tuple
    bits: int
    def packet(self):
        # Every call is a separately paid export, using the declared fixed
        # CANONICAL_* envelope; it is not silently included in an old receipt.
        out=json.loads(self.header_bytes)
        out['bucket_numerators']=[list(row) for row in self.numerators]
        canonical(out)
        return out

class ScaleAdapter:
    """Paid engine reuse for this one normalized constant source family.

    Exact raw input 2^-F delta_0 and any valid singleton-block phase state are
    admitted at M=2^28. Unsupported structured inputs truthfully fail rather
    than pretending the constant specialization is a general sparse backend.
    """
    def __init__(self):
        self.producer,self.producer_source_bytes=load_producer()
        self.engine=None
        self.producer_work=0;self.producer_storage=0
        self.canonical_calls=0;self.verifier_comparisons=0;self.adapter_calls=0
        self.producer_attempts=0
    def execute(self,raw,state,t=16,q=None,p=None,sigma=1,tau=0):
        # Charge bounded control/copies/property JSON decodes and rejected
        # producer attempts as well as the returned arithmetic receipt.
        # Arbitrary oversized in-memory input is outside this successful-run
        # envelope and gets no successful numerical/resource certificate.
        self.producer_attempts+=1
        run=self.producer.execute(raw,state,t,q,p)
        self.producer_work+=run.ledger['total_bit_work_upper']
        self.producer_storage+=run.ledger['cumulative_storage_upper_bits']
        self.adapter_calls+=1
        if run.status!='EXACT_TARGET_CERTIFIED' or run.N!=M_FIXED:
            raise Failure('UNSUPPORTED_STRUCTURE: nonzero N=2^28 required')
        if run.period!=((1,0),)*4:
            raise Failure('UNSUPPORTED_STRUCTURE: exact unit impulse at index zero required')
        # Equal Fourier period (1,1,1,1) forces the original quarter-axis vector
        # to delta_0 by the exact four-point inverse. Producer validates raw.
        F=run.context['raw']['F']
        alpha_exponent=-F
        source_exponent=run.value_exponent-alpha_exponent
        plan=run.policy['plan']
        formal_radius_exponent=plan['accepted_serial_radius_factor']['scale']-alpha_exponent
        if formal_radius_exponent > -464:
            raise Failure('TARGET_BUDGET: formal accepted radius exceeds rho')
        if run.policy['q'] < 464:
            raise Failure('TARGET_BUDGET: downstream q>=464 required')
        if self.engine is None:
            self.engine=ConstantBucketEngine()
            self.engine.ledger.bytework(self.producer_source_bytes+len(Path(__file__).read_bytes()))
        result=self.engine.run(run.period,source_exponent,sigma,tau)
        header={
            'schema':PACKET_SCHEMA,
            'producer':run.packet(),
            'source':{'schema':'EXACT_CONSTANT_SOURCE_V1','N':run.N,
                'period':[[1,0]]*4,'value_exponent':source_exponent,
                'norm_squared':1,'alpha_exponent':alpha_exponent,
                'producer_exact_error':0,'requantization_exact_error':0,
                'formal_policy_radius_over_alpha':{'coefficient':1,'scale':formal_radius_exponent}},
            'downstream':{'backend':'ALG034_Q16_CONSTANT_FREQUENCY_BACKEND_V1',
                'm':28,'beta':[5,56],'k':32,'B':131072,'r':57,'P':464,
                'sigma':sigma,'tau':tau,'bucket_bits':result.bits,
                'complex_max_error':{'coefficient':1,'scale':-464},
                'target':'ideal_Q16_BUCKETS_on_U_negative(Px)/alpha',
                'second_transform_target':'R(Px)/alpha=delta_0',
                'legacy_rounded_execution':False,'full_recovery_executed':False}}
        self.producer_work+=self.producer.EXPORT_BIT_WORK_BOUND
        self.producer_storage+=self.producer.EXPORT_STORAGE_BITS_BOUND
        header_bytes=canonical(header);self.canonical_calls+=1
        return IntegratedRun(header_bytes,result.numerators,result.bits)
    def verify(self,raw,state,t,q,packet,p=None,sigma=1,tau=0):
        actual=canonical(packet);self.canonical_calls+=1
        run=self.execute(raw,state,t,q,p,sigma,tau)
        expected=canonical(run.packet());self.canonical_calls+=2
        self.verifier_comparisons+=1
        if actual!=expected:
            raise Failure('SEMANTIC_MISMATCH: bound full output/context differs from replay')
        return {'status':'SEMANTICALLY_VERIFIED_THEOREM_CONSTANT_BUCKETS',
            'bound_to_separately_supplied_original_context':True,
            'external_origin_authenticated':False,'historical_execution_attested':False,
            'full_recovery_executed':False,'receipt':self.receipt()}
    def receipt(self,additional_packet_exports=0,additional_json_parses=0):
        if (type(additional_packet_exports) is not int or additional_packet_exports<0
                or type(additional_json_parses) is not int or additional_json_parses<0):
            raise Failure('GRAMMAR: export/parse counts')
        charges=self.canonical_calls+additional_packet_exports+2*additional_json_parses+self.verifier_comparisons+self.producer_attempts+1
        numeric=self.engine.ledger.report() if self.engine else {'total_bit_work_upper':0,'cumulative_storage_upper_bits':0}
        return {'producer_bit_work_upper':self.producer_work,
            'producer_cumulative_storage_upper_bits':self.producer_storage,
            'numerical':numeric,'canonical_parser_compare_charges':charges,
            'total_bit_work_upper':self.producer_work+numeric['total_bit_work_upper']+charges*CANONICAL_BIT_WORK+DEPENDENCY_BIT_WORK,
            'cumulative_storage_upper_bits':self.producer_storage+numeric['cumulative_storage_upper_bits']+charges*CANONICAL_STORAGE_BITS+DEPENDENCY_STORAGE_BITS,
            'adapter_calls':self.adapter_calls,'producer_attempts':self.producer_attempts,'semantic_comparisons':self.verifier_comparisons,
            'model':'schoolbook bit work and cumulative logical storage, not CPU/RSS',
            'no_N_or_W_allocation':True,'actual_FFT_roots':0,'actual_FFT_butterflies':0,
            'representation_change':'exact period-four source plus full B-entry output'}
