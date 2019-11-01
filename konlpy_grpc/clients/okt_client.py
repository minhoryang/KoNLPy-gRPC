from .._generated import global_pb2, okt_pb2_grpc
from . import Options, StringArrayResponse, TupleArrayResponse


class OktClient:  # TODO: Async call method needed?
    def __init__(self, grpc_channel):
        self.stub = okt_pb2_grpc.OktStub(grpc_channel)

    def pos(self, phrase, norm=False, stem=False, join=False):
        result = self.stub.Pos(global_pb2.StringRequest(payload=phrase, options=Options(norm=norm, stem=stem, join=join)))
        return TupleArrayResponse(result, join=join)

    def nouns(self, phrase):
        return StringArrayResponse(self.stub.Nouns(global_pb2.StringRequest(payload=phrase, options=None)))

    def morphs(self, phrase):
        return StringArrayResponse(self.stub.Morphs(global_pb2.StringRequest(payload=phrase, options=None)))

    def phrases(self, phrase):
        return StringArrayResponse(self.stub.Phrases(global_pb2.StringRequest(payload=phrase, options=None)))

    def normalize(self, phrase):
        return StringArrayResponse(self.stub.Normalize(global_pb2.StringRequest(payload=phrase, options=None)))[0]  # FIXME: proto can't handle this.
