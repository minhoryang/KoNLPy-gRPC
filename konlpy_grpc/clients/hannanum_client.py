import ast

from .._generated import global_pb2, hannanum_pb2_grpc
from . import Options, StringArrayResponse, TupleArrayResponse


class HannanumClient:  # TODO: Async call method needed?
    def __init__(self, grpc_channel):
        self.stub = hannanum_pb2_grpc.HannanumStub(grpc_channel)

    def analyze(self, phrase):
        # TODO: gRPC Error Handling/Retry Logic Required!
        return ast.literal_eval(
            StringArrayResponse(self.stub.Analyze(global_pb2.StringRequest(payload=phrase, options=None)))[0]
        )  # FIXME: Proto can't handle this.

    def pos(self, phrase, ntags=9, flatten=True, join=False):
        if ntags == 9:
            result = self.stub.Pos09(global_pb2.StringRequest(payload=phrase, options=Options(flatten=flatten, join=join)))
            return TupleArrayResponse(result, join=join)
        elif ntags == 22:
            result = self.stub.Pos22(global_pb2.StringRequest(payload=phrase, options=Options(flatten=flatten, join=join)))
            return TupleArrayResponse(result, join=join)
        else:
            raise Exception("ntags in [9, 22]")  # XXX: Same as konlpy.tag._hannanum.Hannanum.pos()'s Exception.

    def nouns(self, phrase):
        return StringArrayResponse(self.stub.Nouns(global_pb2.StringRequest(payload=phrase, options=None)))

    def morphs(self, phrase):
        return StringArrayResponse(self.stub.Morphs(global_pb2.StringRequest(payload=phrase, options=None)))
