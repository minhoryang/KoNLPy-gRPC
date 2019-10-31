import grpc
import pytest

from konlpy_grpc._generated.global_pb2 import Option, StringRequest


@pytest.fixture(scope="module")
def komoran_stub(request):
    """Check the preconditions and Prepare the stub."""
    from konlpy_grpc._generated.komoran_pb2_grpc import KomoranStub

    if not request.config.getoption("grpc-real"):
        pytest.importorskip("konlpy")
        pytest.importorskip("jpype")

    # Prepare the grpc-server/channel later.
    grpc_channel = request.getfixturevalue("grpc_channel")
    return KomoranStub(grpc_channel)


@pytest.mark.komoran
class TestKomoran:
    @staticmethod
    def test_komoran_pos(komoran_stub):
        s = StringRequest(payload="안녕하세요.")
        r = komoran_stub.Pos(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_komoran_pos_with_bypass_option(komoran_stub):
        o = Option(key="flatten", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o])
        p = komoran_stub.Pos(r)
        print(p)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_komoran_pos_with_wrong_option(komoran_stub):
        o = Option(key="wrong", value=False)
        r = StringRequest(payload="안녕하세요.", options=[o])
        with pytest.raises((grpc.RpcError, Exception)) as e:  # FIXME: Exception -> CustomExc
            p = komoran_stub.Pos(r)
            print(p, e)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_komoran_nouns(komoran_stub):
        s = StringRequest(payload="안녕하세요.")
        r = komoran_stub.Nouns(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_komoran_morphs(komoran_stub):
        s = StringRequest(payload="안녕하세요.")
        r = komoran_stub.Morphs(s)
        print(r)
        # No unhandled exception raised, test passed!
