import time
from concurrent import futures

import grpc

from .servers import hannanum_server, kkma_server, komoran_server, mecab_server, okt_server


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # XXX: grpc doesn't support ProcessPoolExecutor.
    hannanum_server.add_to_server(hannanum_server.HannanumService(), server)
    kkma_server.add_to_server(kkma_server.KkmaService(), server)
    komoran_server.add_to_server(komoran_server.KomoranService(), server)
    mecab_server.add_to_server(mecab_server.MecabService(), server)
    okt_server.add_to_server(okt_server.OktService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
