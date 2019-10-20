if __name__ == "__main__":  # TODO: shame on you
    import sys

    if len(sys.argv) != 2:
        raise Exception()
    mode = sys.argv[1]
    if mode == "server":
        from . import server

        server.serve()
    elif mode == "client":
        from . import client

        client.run()
    elif mode == "hannanum_server":
        from .servers import hannanum_server as server

        server.serve()
    elif mode == "kkma_server":
        from .servers import kkma_server as server

        server.serve()
    elif mode == "komoran_server":
        from .servers import komoran_server as server

        server.serve()
    elif mode == "mecab_server":
        from .servers import mecab_server as server

        server.serve()
    elif mode == "okt_server":
        from .servers import okt_server as server

        server.serve()
    else:
        raise Exception()
