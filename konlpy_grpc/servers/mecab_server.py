import time
from concurrent import futures

import grpc
from konlpy.tag import Mecab

from .._generated import global_pb2, mecab_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MecabService(mecab_pb2_grpc.MecabServicer):
    def __init__(self):
        self.engine = Mecab()

    def Pos(self, request, context):
        return global_pb2.TupleArrayResponse(
            results=[
                global_pb2.TupleArrayResponse.Tuple(
                    keyword=keyword,
                    tag=tag,
                )
                for keyword, tag in self.engine.pos(request.payload)
            ],
            options=request.options,
        )

    def Nouns(self, request, context):
        return global_pb2.StringArrayResponse(
            results=self.engine.nouns(request.payload),
            options=request.options,
        )

    def Morphs(self, request, context):
        return global_pb2.StringArrayResponse(
            results=self.engine.morphs(request.payload),
            options=request.options,
        )


add_to_server = mecab_pb2_grpc.add_MecabServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mecab_pb2_grpc.add_MecabServicer_to_server(MecabService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
