import time
from concurrent import futures

import grpc
import jpype

from konlpy.tag import Hannanum

from .._generated import global_pb2, hannanum_pb2, hannanum_pb2_grpc
from ..monkeypatch import _ORIGINAL, KEY_TAG_HANNANUM


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HannanumService(hannanum_pb2_grpc.HannanumServicer):
    HANDLE_OPTIONS = ("ntags:09", "ntags:22", "flatten", "join")

    def __init__(self):
        self.engine = _ORIGINAL[KEY_TAG_HANNANUM]() if KEY_TAG_HANNANUM in _ORIGINAL else Hannanum()  # TODO: Thread-safe? Performance?

    @staticmethod
    def _check_options(options):
        result = {}
        for option in options:
            if option.key not in HannanumService.HANDLE_OPTIONS:
                raise Exception("%s option is not supported! (supported: %s)" % (option.key, ", ".join(HannanumService.HANDLE_OPTIONS)))
                # TODO: context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            elif option.key in ("ntags:09", "ntags:22"):
                raise Exception("ntags option is already covered by Pos09(), Pos22().")
            elif option.key in HannanumService.HANDLE_OPTIONS:
                result[option.key] = option.value
        return result

    def Pos09(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        options = self._check_options(request.options)
        result = self.engine.pos(request.payload, ntags=9, **options)
        if options.get("join", False):
            return global_pb2.TupleArrayResponse(
                results=[global_pb2.TupleArrayResponse.Tuple(keyword=keyword, tag=None) for keyword in result], options=request.options
            )
        return global_pb2.TupleArrayResponse(
            results=[global_pb2.TupleArrayResponse.Tuple(keyword=keyword, tag=tag) for keyword, tag in result], options=request.options
        )

    def Pos22(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        options = self._check_options(request.options)
        result = self.engine.pos(request.payload, ntags=22, **options)
        if options.get("join", False):
            return global_pb2.TupleArrayResponse(
                results=[global_pb2.TupleArrayResponse.Tuple(keyword=keyword, tag=None) for keyword in result], options=request.options
            )
        return global_pb2.TupleArrayResponse(
            results=[global_pb2.TupleArrayResponse.Tuple(keyword=keyword, tag=tag) for keyword, tag in result], options=request.options
        )

    def Nouns(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(results=self.engine.nouns(request.payload), options=request.options)

    def Morphs(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(results=self.engine.morphs(request.payload), options=request.options)

    def Analyze(self, request, context):
        jpype.attachThreadToJVM()  # XXX: Performance Incresed. (Still don't know yet)
        return global_pb2.StringArrayResponse(results=[repr(self.engine.analyze(request.payload))], options=request.options)  # FIXME! Proto can't handle this.


add_to_server = hannanum_pb2_grpc.add_HannanumServicer_to_server


SERVICE_NAME = hannanum_pb2._HANNANUM.full_name


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_to_server(HannanumService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
