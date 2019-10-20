import time
from concurrent import futures

import grpc
import jpype
from konlpy.tag import Hannanum

from .._generated import global_pb2, hannanum_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HannanumService(hannanum_pb2_grpc.HannanumServicer):
    BYPASS_OPTIONS = ('flatten', 'join')
    HANDLE_OPTIONS = ('ntags:09', 'ntags:22')

    def __init__(self):
        self.engine = Hannanum()  # TODO: Thread-safe? Performance?

    @staticmethod
    def _check_options(options):
        result = {}
        for option in options:
            if option.key in HannanumService.BYPASS_OPTIONS:
                pass
            elif option.key not in HannanumService.HANDLE_OPTIONS:
                raise Exception(
                    '%s option is not supported! (supported: %s)' % (
                        option.key,
                        ', '.join(HannanumService.BYPASS_OPTIONS + HannanumService.HANDLE_OPTIONS)
                    )
                )
                # TODO: context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            elif option.key in ('ntags:09', 'ntags:22'):
                raise Exception('ntags option is covered by Pos09(), Pos22().')
        return result

    def Pos09(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.TupleArrayResponse(
            results=[
                global_pb2.TupleArrayResponse.Tuple(
                    keyword=keyword,
                    tag=tag,
                )
                for keyword, tag in self.engine.pos(request.payload, ntags=9, **self._check_options(request.options))
            ],
            options=request.options,
        )

    def Pos22(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.TupleArrayResponse(
            results=[
                global_pb2.TupleArrayResponse.Tuple(
                    keyword=keyword,
                    tag=tag,
                )
                for keyword, tag in self.engine.pos(request.payload, ntags=22, **self._check_options(request.options))
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


add_to_server = hannanum_pb2_grpc.add_HannanumServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_to_server(HannanumService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
