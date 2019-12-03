import time
from concurrent import futures

import grpc

from grpc_reflection.v1alpha import reflection

from .servers import hannanum_server, kkma_server, komoran_server, mecab_server, okt_server


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # XXX: grpc doesn't support ProcessPoolExecutor.

    hannanum_server.add_to_server(hannanum_server.HannanumService(), server)
    kkma_server.add_to_server(kkma_server.KkmaService(), server)
    komoran_server.add_to_server(komoran_server.KomoranService(), server)
    mecab_server.add_to_server(mecab_server.MecabService(), server)
    okt_server.add_to_server(okt_server.OktService(), server)

    SERVICE_NAMES = (
        reflection.SERVICE_NAME,
        hannanum_server.SERVICE_NAME,
        kkma_server.SERVICE_NAME,
        komoran_server.SERVICE_NAME,
        mecab_server.SERVICE_NAME,
        okt_server.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
