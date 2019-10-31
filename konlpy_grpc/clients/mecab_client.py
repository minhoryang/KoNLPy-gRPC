from .._generated import global_pb2, mecab_pb2_grpc
from . import Options, StringArrayResponse, TupleArrayResponse


class MecabClient:  # TODO: Async call method needed?
    def __init__(self, grpc_channel):
        self.stub = mecab_pb2_grpc.MecabStub(grpc_channel)

    def pos(self, phrase, flatten=True, join=False):
        result = self.stub.Pos(global_pb2.StringRequest(payload=phrase, options=Options(flatten=flatten, join=join)))
        return TupleArrayResponse(result, join=join)

    def nouns(self, phrase):
        return StringArrayResponse(self.stub.Nouns(global_pb2.StringRequest(payload=phrase, options=None)))

    def morphs(self, phrase):
        return StringArrayResponse(self.stub.Morphs(global_pb2.StringRequest(payload=phrase, options=None)))
