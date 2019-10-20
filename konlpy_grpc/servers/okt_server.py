import time
from concurrent import futures

import grpc
import jpype
from konlpy.tag import Okt

from .._generated import global_pb2, okt_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class OktService(okt_pb2_grpc.OktServicer):
    BYPASS_OPTIONS = ('join', )
    HANDLE_OPTIONS = ('norm', 'stem')

    def __init__(self):
        self.engine = Okt()  # TODO: Thread-safe? Performance?

    @staticmethod
    def _check_options(options):
        result = {}
        for option in options:
            if option.key in OktService.BYPASS_OPTIONS:
                pass
            elif option.key not in OktService.HANDLE_OPTIONS:
                raise Exception(
                    '%s option is not supported! (supported: %s)' % (
                        option.key,
                        ', '.join(OktService.BYPASS_OPTIONS + OktService.HANDLE_OPTIONS)
                    )
                )
                # TODO: context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            else:
                result[option.key] = option.value
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
            results=self.engine.morphs(request.payload, **self._check_options(request.options)),
            options=request.options,
        )

    def Phrases(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(
            results=self.engine.phrases(request.payload),
            options=request.options,
        )

    def Normalize(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(
            results=self.engine.normalize(request.payload),
            options=request.options,
        )


add_to_server = okt_pb2_grpc.add_OktServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    okt_pb2_grpc.add_OktServicer_to_server(OktService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
