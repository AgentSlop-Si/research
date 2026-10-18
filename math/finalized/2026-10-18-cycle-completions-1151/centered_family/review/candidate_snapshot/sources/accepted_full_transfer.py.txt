"""Complete, source-bound retained outer transfer; new candidate 2026-10-18.

Consumes the accepted local ProducedMedians association. This is not a source
signal, random-recovery, or dense-fallback implementation. The only numerical
loop consumes every coefficient from the accepted Outer generator.
"""
from dataclasses import dataclass
from outer_wrapper import Outer, ReceiptLedger


class TransferContractError(ValueError):
    pass


class OuterDenseRequired(TransferContractError):
    pass


@dataclass(frozen=True, slots=True)
class TransferConfig:
    beta_numerator: int
    beta_denominator: int
    scale_power: int
    input_width_constant: int


@dataclass(frozen=True, slots=True)
class TransferOutput:
    pairs: tuple
    bits: int
    normalized_bits: int
    scale_power: int
    incidences: int
    accumulator_signed_bits: int
    max_row_terms: int
    max_accumulator_abs: int
    binding: object
    _owner: object


def round_div_pow2(value, shift, ledger):
    """Signed nearest-even; one rounding, after the exact row sum."""
    ledger.integer(value); ledger.integer(shift)
    if shift < 0:
        raise TransferContractError('negative rounding shift')
    divisor = 1 << shift
    lower, remainder = divmod(value, divisor)
    twice = 2 * remainder
    result = lower + int(twice > divisor or (twice == divisor and lower % 2 != 0))
    ledger.charge(value,shift,divisor,lower,remainder,twice,result,count=24)
    return result


def exact_complex_product(a, b, c, d, ledger):
    """(a+i b)(c+i d), without any intermediate rounding."""
    for v in (a,b,c,d): ledger.integer(v)
    ac, bd, ad, bc = a*c, b*d, a*d, b*c
    real, imag = ac-bd, ad+bc
    ledger.charge(a,b,c,d,ac,bd,ad,bc,real,imag,count=32)
    return real, imag


class FullTransfer:
    """Single-use complete stream -> exact scatter -> N rounded scaled outputs.

    Validation/replay paid by Outer remains in the same cumulative ReceiptLedger.
    Empty support still pays N initialization and N output records. No E-record
    list, coefficient table, phase table, or output-time transcendental pass.
    """
    def __init__(self, outer, config):
        if type(outer) is not Outer:
            raise TransferContractError('exact bound Outer required')
        self.outer = outer
        self.ledger = outer.ledger
        self.state = 'VALIDATING'
        L=self.ledger
        L.charge(count=16)
        if type(config) is not TransferConfig:
            raise TransferContractError('exact immutable TransferConfig required')
        for value in (config.beta_numerator,config.beta_denominator,
                      config.scale_power,config.input_width_constant):
            L.integer(value)
        bn,bd,sigma,d=(config.beta_numerator,config.beta_denominator,
                       config.scale_power,config.input_width_constant)
        if bd<=0 or bn<=0 or 2*bn>=bd or d<1:
            raise TransferContractError('0<beta<1/2 and d>=1 required')
        G=outer.validate_binding(outer.binding)
        if outer.binding.header.estimate_bits != 16*G.m+16:
            raise TransferContractError('theorem estimate grid P=16m+16 required')
        if abs(sigma)>d*G.m:
            raise TransferContractError('scale power exceeds declared d*m range')
        L.charge(bn,bd,sigma,d,G.m,count=24)
        self.config=config
        self.geometry=G
        self._owner=object()
        self.output=None
        self.coefficients_evaluated=0
        self.expected_incidences=0
        # The guard is checked before numerical preparation or N allocations.
        if G.dense_required:
            self.state='DENSE_REQUIRED'
            raise OuterDenseRequired('OUTER_DENSE_REQUIRED: original normalized input is needed by a separate dense transform')
        P=outer.binding.header.estimate_bits
        w=P+2*G.m+2
        log_t=(G.t-1).bit_length()
        self.accumulator_signed_bits=G.p+w+4+log_t
        self.accumulator_limit=1 << (self.accumulator_signed_bits-1)
        self.coefficient_limit=4 << G.p
        self.estimate_limit=(3*G.M*G.M) << P
        self.b=((bn+2*bd)*G.m+bd-1)//bd
        self.shift=G.p+P-self.b
        if self.shift<0:
            raise TransferContractError('output grid finer than product grid')
        L.charge(P,w,log_t,self.accumulator_signed_bits,self.accumulator_limit,
                 self.coefficient_limit,self.estimate_limit,self.b,self.shift,count=48)
        for k,(a,b) in outer.binding.output.pairs:
            L.integer(k);L.integer(a);L.integer(b)
            L.charge(k,a,b,self.estimate_limit,count=16)
            if abs(a)>=self.estimate_limit or abs(b)>=self.estimate_limit:
                raise TransferContractError('every-tape Cartesian estimate bound |z|<3M^2 violated')
        for r0,r1,prefix in outer.binding.endpoints:
            L.charge(r0,r1,prefix,self.expected_incidences,count=12)
            if prefix != self.expected_incidences:
                raise TransferContractError('inconsistent incidence prefix')
            self.expected_incidences += r1-r0
        L.charge(self.expected_incidences,count=8)
        self.state='READY'

    def run(self):
        L=self.ledger; G=self.geometry; B=self.outer.binding
        L.charge(count=8)
        if self.state!='READY':
            raise TransferContractError('full transfer is single-use')
        self.state='RUNNING'
        try:
            real=[0]*G.N; imag=[0]*G.N; counts=[0]*G.N
            L.charge(G.N,count=3*G.N+16)
            ordinal=0; largest=0; max_terms=0
            for incidence in self.outer.incidences():
                L.charge(ordinal,incidence.ordinal,count=8)
                if incidence.ordinal!=ordinal:
                    raise TransferContractError('incomplete, repeated or reordered coefficient stream')
                record=self.outer.coefficient(incidence)
                self.coefficients_evaluated+=1
                self.outer.validate_coefficient(record)
                if record.incidence is not incidence or record.p!=G.p:
                    raise TransferContractError('coefficient stream binding/grid mismatch')
                c,d=record.real,record.imag
                L.charge(c,d,self.coefficient_limit,count=12)
                if abs(c)>=self.coefficient_limit or abs(d)>=self.coefficient_limit:
                    raise TransferContractError('certified coefficient range violated')
                k,(a,b)=B.output.pairs[incidence.support_ordinal]
                if k!=incidence.k:
                    raise TransferContractError('estimate/coefficient source mismatch')
                re,im=exact_complex_product(a,b,c,d,L)
                ell=incidence.ell
                nr,ni=real[ell]+re,imag[ell]+im
                nc=counts[ell]+1
                L.charge(ell,nr,ni,nc,self.accumulator_limit,ordinal,count=32)
                if nc>G.t or abs(nr)>=self.accumulator_limit or abs(ni)>=self.accumulator_limit:
                    raise TransferContractError('every-prefix accumulator bound violated')
                real[ell],imag[ell],counts[ell]=nr,ni,nc
                largest=max(largest,abs(nr),abs(ni));max_terms=max(max_terms,nc)
                ordinal+=1
                L.charge(ordinal,largest,max_terms,count=12)
            if ordinal!=self.expected_incidences or self.coefficients_evaluated!=ordinal:
                raise TransferContractError('truncated coefficient stream')
            sigma=self.config.scale_power
            bits=self.b-sigma
            scale_shift=max(0,-bits)
            bits=max(0,bits)
            L.charge(bits,scale_shift,self.b,sigma,count=16)
            output=[]
            for ell in range(G.N):
                a=round_div_pow2(real[ell],self.shift,L)
                b=round_div_pow2(imag[ell],self.shift,L)
                # Exact scale-back; exponent is made nonnegative if necessary.
                a <<= scale_shift; b <<= scale_shift
                output.append((a,b))
                L.charge(ell,a,b,bits,scale_shift,count=24)
            pairs=tuple(output)
            L.charge(G.N,bits,ordinal,largest,count=G.N+24)
            self.output=TransferOutput(pairs,bits,self.b,sigma,ordinal,
                  self.accumulator_signed_bits,max_terms,largest,B,self._owner)
            self.state='COMPLETE'
            return self.output
        except Exception:
            self.state='FAILED'
            raise

    def validate_output(self, output):
        """In-process output identity, not serialized external attestation."""
        self.ledger.charge(count=16)
        if self.state!='COMPLETE' or type(output) is not TransferOutput or output is not self.output:
            raise TransferContractError('foreign or substituted completed output')
        if output._owner is not self._owner or output.binding is not self.outer.binding:
            raise TransferContractError('foreign or substituted output origin')
        return output

    def receipt(self):
        # Bounded observation; report/serialization is a separate harness cost.
        return {'state':self.state,'expected_incidences':self.expected_incidences,
                'coefficients_evaluated':self.coefficients_evaluated,
                'outer_and_scatter':self.ledger.report(),
                'scalar':None if self.outer.kernel is None else self.outer.kernel.paid.report()}
