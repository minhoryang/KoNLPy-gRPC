# from https://github.com/kataev/pytest-grpc/issues/5
# FIXME: use grpcio-testing, not pytest-grpc.

import grpc
import pytest
import pytest_grpc


@pytest.fixture(scope="module")
def grpc_servicer(request):
    """Fetch grpc_servicer according to filename of each tests.

    - request.node (with `scope='module'`) will be a name of `test_*.py`.
    """
    result = []
    print(request.node.name)

    if "hannanum" in request.node.name:
        from konlpy_grpc.servers.hannanum_server import HannanumService, add_to_server as add_hannanum

        result.append((add_hannanum, HannanumService()))
    if "kkma" in request.node.name:
        from konlpy_grpc.servers.kkma_server import KkmaService, add_to_server as add_kkma

        result.append((add_kkma, KkmaService()))
    if "komoran" in request.node.name:
        from konlpy_grpc.servers.komoran_server import KomoranService, add_to_server as add_komoran

        result.append((add_komoran, KomoranService()))
    if "mecab" in request.node.name:
        from konlpy_grpc.servers.mecab_server import MecabService, add_to_server as add_mecab

        result.append((add_mecab, MecabService()))
    if "okt" in request.node.name:
        from konlpy_grpc.servers.okt_server import OktService, add_to_server as add_okt

        result.append((add_okt, OktService()))

    return result


@pytest.fixture(scope="module")
def grpc_server(_grpc_server, grpc_addr, grpc_servicer):
    for adder, servicer in grpc_servicer:
        adder(servicer, _grpc_server)

    _grpc_server.add_insecure_port(grpc_addr)
    _grpc_server.start()
    yield _grpc_server
    _grpc_server.stop(grace=None)


@pytest.fixture(scope="module")
def grpc_create_channel(request, grpc_addr):
    """grpc_channel made here (and also launch the grpc-server).

    There are 3 modes with `pytest-grpc`:
    - (default): Open a socket, Launch grpc-server, call through grpc-server.
    - grpc-fake: Open a socket, Launch grpc-server, but call directly.
    - grpc-real: Connect to grpc-real-server`s addr!

    'grpc-real' option doesn't needed to launch grpc-server, that's why we decoupled 'grpc_server' fixture.
    """

    def _create_channel(credentials=None, options=None):
        is_real = request.config.getoption("grpc-real")
        if is_real:
            return grpc.insecure_channel(is_real, options)

        grpc_server = request.getfixturevalue("grpc_server")
        if request.config.getoption("grpc-fake"):
            return pytest_grpc.plugin.FakeChannel(grpc_server, credentials)
        if credentials is not None:
            return grpc.secure_channel(grpc_addr, credentials, options)
        return grpc.insecure_channel(grpc_addr, options)

    return _create_channel


@pytest.hookimpl
def pytest_addoption(parser):
    parser.addoption("--grpc-real-server", action="store", dest="grpc-real")
    parser.addoption("--konlpy-repo", action="store", dest="konlpy-repo")
