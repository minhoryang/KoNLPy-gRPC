import time
from concurrent import futures

import grpc
import jpype
from konlpy.tag import Kkma

from .._generated import global_pb2, kkma_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class KkmaService(kkma_pb2_grpc.KkmaServicer):
    BYPASS_OPTIONS = ('flatten', 'join')
    HANDLE_OPTIONS = tuple()

    def __init__(self):
        self.engine = Kkma()  # TODO: Thread-safe? Performance?

    @staticmethod
    def _check_options(options):
        result = {}
        for option in options:
            if option.key in KkmaService.BYPASS_OPTIONS:
                pass
            elif option.key not in KkmaService.HANDLE_OPTIONS:
                raise Exception(
                    '%s option is not supported! (supported: %s)' % (
                        option.key,
                        ', '.join(KkmaService.BYPASS_OPTIONS + KkmaService.HANDLE_OPTIONS)
                    )
                )
                # TODO: context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        return result

    def Pos(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.TupleArrayResponse(
            results=[
                global_pb2.TupleArrayResponse.Tuple(
                    keyword=keyword,
                    tag=tag,
                )
                for keyword, tag in self.engine.pos(request.payload, **self._check_options(request.options))
            ],
            options=request.options,
        )

    def Nouns(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(
            results=self.engine.nouns(request.payload),
            options=request.options,
        )

    def Morphs(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(
            results=self.engine.morphs(request.payload),
            options=request.options,
        )

    def Sentences(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(
            results=self.engine.sentences(request.payload),
            options=request.options,
        )


add_to_server = kkma_pb2_grpc.add_KkmaServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kkma_pb2_grpc.add_KkmaServicer_to_server(KkmaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
