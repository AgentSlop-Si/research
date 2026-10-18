"""Live original-input-bound sparse supplier -> original ideal Q16 BUCKETS.

The adapter never accepts a caller-supplied descriptor or purported producer
result. It executes the pinned fresh supplier against separately supplied
canonical original raw/state, then consumes its exact modal representation.
"""
from dataclasses import dataclass
from pathlib import Path
from hashlib import sha256
from importlib.util import spec_from_file_location,module_from_spec
import json,sys
from nonconstant_buckets import SparseBucketEngine,Failure,M,P,K,MAX_SUPPORT
BASE=Path(__file__).resolve().parent
PRODUCER_PIN='5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed'
SCHEMA='ALG034_Q16_SPARSE_ORIGINAL_INTEGRATION_V1'
MAX_JSON_BYTES=8*1024*1024;MAX_NODES=500000;MAX_INT_BITS=12288
CANONICAL_WORK=1<<100;CANONICAL_STORAGE=1<<50

def canonical(obj):
    count=0;budget=MAX_JSON_BYTES
    def walk(v,depth):
        nonlocal count,budget
        count+=1
        if count>MAX_NODES or depth>16:raise Failure('RESOURCE_LIMIT: canonical tree')
        kind=type(v)
        if v is None or kind is bool:budget-=5
        elif kind is int:
            bits=abs(v).bit_length()
            if bits>MAX_INT_BITS:raise Failure('RESOURCE_LIMIT: serialized integer')
            budget-=bits*30103//100000+3
        elif kind is str:
            if len(v)>4096:raise Failure('RESOURCE_LIMIT: serialized text')
            budget-=2+12*len(v)
        elif kind is list:
            if len(v)>131072:raise Failure('RESOURCE_LIMIT: serialized list')
            budget-=len(v)+2
            for u in v:walk(u,depth+1)
        elif kind is dict:
            if len(v)>64:raise Failure('RESOURCE_LIMIT: serialized mapping')
            budget-=2*len(v)+2
            for k,u in v.items():
                if type(k)is not str:raise Failure('GRAMMAR: canonical mapping keys')
                walk(k,depth+1);walk(u,depth+1)
        else:raise Failure('GRAMMAR: canonical exact built-in types')
        if budget<0:raise Failure('RESOURCE_LIMIT: encoded byte bound')
    walk(obj,0)
    out=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
    if len(out)>MAX_JSON_BYTES:raise Failure('RESOURCE_LIMIT: encoded bytes')
    return out

def strict_loads(text):
    if type(text)is not str or len(text)>MAX_JSON_BYTES:raise Failure('GRAMMAR_OR_RESOURCE: JSON text')
    try:
        if len(text.encode('utf8'))>MAX_JSON_BYTES:raise Failure('RESOURCE_LIMIT: UTF8 bytes')
    except UnicodeEncodeError:raise Failure('GRAMMAR: Unicode surrogate')
    def integer(s):
        if len(s.lstrip('-'))>3700:raise Failure('RESOURCE_LIMIT: JSON integer digits')
        return int(s)
    def bad(s):raise Failure('GRAMMAR: noninteger JSON value')
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise Failure('GRAMMAR: duplicate JSON key')
            out[k]=v
        return out
    try:out=json.loads(text,parse_int=integer,parse_float=bad,parse_constant=bad,object_pairs_hook=pairs)
    except (json.JSONDecodeError,RecursionError):raise Failure('GRAMMAR: invalid JSON')
    canonical(out);return out

def producer():
    source=BASE/'vendor'/'sparse_supplier.py';data=source.read_bytes()
    if sha256(data).hexdigest()!=PRODUCER_PIN:raise Failure('DEPENDENCY_PIN: fresh sparse supplier')
    name='fresh_nonconstant_alg034_sparse_supplier_'+PRODUCER_PIN[:12]
    if name in sys.modules:
        module=sys.modules[name]
        if getattr(module,'_verified_source_pin',None)!=PRODUCER_PIN:raise Failure('DEPENDENCY_IDENTITY: fresh supplier')
    else:
        spec=spec_from_file_location(name,source);module=module_from_spec(spec);sys.modules[name]=module
        spec.loader.exec_module(module);module._verified_source_pin=PRODUCER_PIN
    return module,len(data)

@dataclass(frozen=True)
class IntegratedRun:
    header_bytes:bytes
    numerators:tuple
    bits:int
    def packet(self):
        # Every external export is an additional documented fixed charge.
        out=json.loads(self.header_bytes);out['bucket_numerators']=[list(x) for x in self.numerators]
        canonical(out);return out

class SparseAdapter:
    def __init__(self):
        self.producer,self.producer_bytes=producer();self.engine=None
        self.calls=0;self.attempts=0;self.canonical_calls=0;self.comparisons=0
        self.producer_work=0;self.producer_storage=0
    def execute(self,raw,state,t=16,q=None,p=None,sigma=1,tau=17,query_bits=None):
        self.attempts+=1
        src=self.producer.execute(raw,state,t,q,p,query_bits)
        self.producer_work+=src.ledger['total_bit_work_upper']
        self.producer_storage+=src.ledger['cumulative_storage_upper_bits']
        if src.status!='NONZERO_EXACT_MODAL_SOURCE' or src.N!=M or len(src.entries)>MAX_SUPPORT:
            raise Failure('UNSUPPORTED_STRUCTURE: nonzero theorem-size sparse original with at most16 entries')
        # The exact descriptor comes only from live, validated original input.
        # No roots, coefficients, hashes or flags supplied by a caller replace it.
        alpha_exp=src.h-src.F;policy=src.policy
        formal_exp=policy['plan']['accepted_serial_radius_factor']['scale']-alpha_exp
        if policy['q']<P or formal_exp>-P:raise Failure('PRECISION: normalized formal producer radius')
        if self.engine is None:
            self.engine=SparseBucketEngine();self.engine.ledger.bytes(self.producer_bytes+len(Path(__file__).read_bytes()))
        result=self.engine.run(src.entries,src.h,sigma,tau)
        self.calls+=1
        header={'schema':SCHEMA,'producer_source_sha256':PRODUCER_PIN,'producer':src.packet(),
            'source':{'N':src.N,'entries':[list(x) for x in src.entries], 'h':src.h,
                'alpha':{'coefficient':1,'scale':alpha_exp},
                'normalized_norm_squared':{'numerator':src.energy,'denominator_power_two':2*src.h},
                'source_representation_error':0,'source_requantization_error':0,
                'formal_policy_radius_over_alpha':{'coefficient':1,'scale':formal_exp},
                'consumption':'exact computed sparse-modal descriptor; no length-N query scan'},
            'downstream':{'backend':'FRESH_SPARSE_MODAL_FREQUENCY_BUCKETS_V1','m':28,'M':M,'beta':[5,56],
                'k':32,'B':131072,'T':2048,'g':512,'H':1536,'r':57,'ell':1048576,'W':119537551,
                'P':P,'sigma':sigma,'tau':tau,'bucket_bits':result.bits,
                'complex_max_error':{'coefficient':1,'scale':-P},
                'target':'original_ideal_Q16_BUCKETS_on_U_negative(Px)/alpha',
                'second_transform_target':'R(x)/alpha', 'legacy_rounded_execution':False,
                'full_recovery_executed':False,'outer_transfer_and_t_guard_proved':False,
                'certificate_grid_bits':K,'tail_grid_units':result.tail_grid_units,
                'active_bins':list(result.active_bins),'certificates':[list(c) for c in result.certificates]}}
        self.producer_work+=self.producer.EXPORT_BIT_WORK_BOUND
        self.producer_storage+=self.producer.EXPORT_STORAGE_BITS_BOUND
        hb=canonical(header);self.canonical_calls+=1
        return IntegratedRun(hb,result.numerators,result.bits)
    def verify(self,raw,state,t,q,packet,p=None,sigma=1,tau=17,query_bits=None):
        supplied=canonical(packet);self.canonical_calls+=1
        actual=self.execute(raw,state,t,q,p,sigma,tau,query_bits)
        expected=canonical(actual.packet());self.canonical_calls+=2;self.comparisons+=1
        if supplied!=expected:raise Failure('SEMANTIC_MISMATCH: original input, schedule, source or full output')
        return {'status':'SEMANTICALLY_VERIFIED_NONCONSTANT_THEOREM_BUCKETS',
            'bound_to_separately_supplied_original_input':True,'external_origin_authenticated':False,
            'historical_execution_attested':False,'full_recovery_executed':False,'receipt':self.receipt()}
    def receipt(self,additional_packet_exports=0,additional_json_parses=0):
        if any(type(x)is not int or x<0 for x in (additional_packet_exports,additional_json_parses)):
            raise Failure('GRAMMAR: external serialization counts')
        count=self.canonical_calls+self.attempts+self.comparisons+additional_packet_exports+2*additional_json_parses+1
        numerical=self.engine.ledger.report() if self.engine else {'total_bit_work_upper':0,'cumulative_storage_upper_bits':0}
        return {'producer_bit_work_upper':self.producer_work,'producer_cumulative_storage_upper_bits':self.producer_storage,
            'numerical':numerical,'canonical_copy_parse_compare_charges':count,
            'total_bit_work_upper':self.producer_work+numerical['total_bit_work_upper']+count*CANONICAL_WORK,
            'cumulative_storage_upper_bits':self.producer_storage+numerical['cumulative_storage_upper_bits']+count*CANONICAL_STORAGE,
            'successful_calls':self.calls,'producer_attempts':self.attempts,'semantic_comparisons':self.comparisons,
            'full_output_coordinates_per_call':131072,'actual_FFT_roots':0,'actual_FFT_butterflies':0,
            'no_N_or_W_array':True,'source_representation':'live sparse-original exact Fourier modes',
            'model':'schoolbook bit work and cumulative logical storage; not CPU/RSS'}
