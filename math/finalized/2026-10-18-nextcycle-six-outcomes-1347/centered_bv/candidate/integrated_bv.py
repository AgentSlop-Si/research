"""Source-bound bounded-variation-original provider to accepted full outer execution.

All numerical dependencies are byte-identical accepted sources in runtime/.
This adapter owns the original/provider/row/outer association in trusted Python.
No externally supplied sparse result, coefficient record, or callback is accepted.
"""
from dataclasses import dataclass
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'runtime'))
import bounded_variation as front
from sparse_output import produce_medians
from outer_wrapper import Header, Outer, ReceiptLedger
from full_transfer import FullTransfer, TransferConfig


@dataclass(frozen=True, slots=True)
class SourceBoundOutput:
    source: front.Source
    estimates: front.Estimates
    final: object
    target: str
    _owner: object


class IntegratedBoundedVariation:
    def __init__(self, original, *, replay_source=False):
        if type(replay_source) is not bool:
            raise ValueError('exact boolean replay switch required')
        self.state='FRONTEND'
        self.estimates,self.front_receipt=front.produce(original)
        self.source=self.estimates.source
        self.source_replay_receipt=None
        if replay_source:
            okay,self.source_replay_receipt=front.replay(original,self.estimates)
            if not okay:raise ValueError('actual original/source replay failed')
        # The immutable Source is a sufficient exact description of the admitted
        # block original; it retains all blocks, F, N and the representation consumed.
        L=ReceiptLedger(); self.ledger=L
        source=self.source; estimates=self.estimates
        L.charge(source.m,source.N,source.F,source.energy,source.variation_l1,
                 source.variation_factor,source.h,source.scale,estimates.bits,count=64)
        for block in source.blocks:
            L.charge(*block,count=24)
        candidates=[];row=[]
        for k,(real,imag) in estimates.pairs:
            candidates.append(k);row.append((real,imag))
            L.charge(k,real,imag,count=24)
        candidates=tuple(candidates);rows=(tuple(row),)
        L.charge(len(candidates),count=2*len(candidates)+16)
        produced=produce_medians(4*source.N,estimates.bits,candidates,rows,L)
        self.produced=produced
        self.outer=Outer(Header(source.N,4*source.N,5,estimates.bits),produced,L)
        for expected,actual in zip(estimates.pairs,produced.output.pairs):
            L.charge(expected[0],expected[1][0],expected[1][1],
                     actual[0],actual[1][0],actual[1][1],count=24)
            if expected != actual:raise AssertionError('one-row identity failed')
        if len(estimates.pairs)!=len(produced.output.pairs):
            raise AssertionError('one-row length changed')
        L.charge(len(estimates.pairs),len(produced.output.pairs),count=8)
        self.transfer=FullTransfer(self.outer,TransferConfig(1,4,source.scale,4))
        self._owner=object();self.output=None;self.state='READY'

    def run(self):
        self.ledger.charge(count=8)
        if self.state!='READY':raise ValueError('integrated transfer is single-use')
        self.state='RUNNING'
        try:
            result=self.transfer.run()
            self.transfer.validate_output(result)
            self.output=SourceBoundOutput(self.source,self.estimates,result,
                                         'negative unitary U_N of the actual original u0',self._owner)
            self.ledger.charge(self.source.N,self.source.scale,result.bits,count=40)
            self.state='COMPLETE'
            return self.output
        except Exception:
            self.state='FAILED'
            raise

    def validate_output(self,output):
        self.ledger.charge(count=32)
        if self.state!='COMPLETE' or type(output) is not SourceBoundOutput or output is not self.output:
            raise ValueError('foreign or substituted integrated output')
        if output._owner is not self._owner or output.source is not self.source or output.estimates is not self.estimates:
            raise ValueError('foreign or substituted original association')
        self.transfer.validate_output(output.final)
        if output.final.binding is not self.outer.binding or self.outer.binding.run is not self.produced:
            raise ValueError('foreign or substituted median association')
        return output

    def receipt(self):
        return {'state':self.state,'front_production':self.front_receipt,
                'source_replay':self.source_replay_receipt,
                'outer_transfer':self.transfer.receipt(),
                'accounting':'Fresh disjoint front/replay/comparison ledgers plus one cumulative median/adapter/outer ledger and one cumulative scalar ledger. Export/oracles/process work are separate.'}
