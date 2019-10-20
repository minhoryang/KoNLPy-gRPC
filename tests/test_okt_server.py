import grpc
import pytest

from konlpy_grpc._generated.global_pb2 import Option, StringRequest


@pytest.fixture(scope="module")
def okt_stub(request):
    """Check the preconditions and Prepare the stub."""
    from konlpy_grpc._generated.okt_pb2_grpc import OktStub

    if not request.config.getoption("grpc-real"):
        pytest.importorskip("konlpy")
        pytest.importorskip("jpype")

    # Prepare the grpc-server/channel later.
    grpc_channel = request.getfixturevalue("grpc_channel")
    return OktStub(grpc_channel)


@pytest.mark.okt
class TestOkt:
    @staticmethod
    def test_okt_pos(okt_stub):
        s = StringRequest(payload="안녕하세요.")
        r = okt_stub.Pos(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_pos_with_handle_option(okt_stub):
        o1 = Option(key="norm", value=True)
        o2 = Option(key="stem", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o1, o2])
        p = okt_stub.Pos(r)
        print(p)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_pos_with_bypass_option(okt_stub):
        o = Option(key="join", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o])
        p = okt_stub.Pos(r)
        print(p)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_pos_with_wrong_option(okt_stub):
        o = Option(key="wrong", value=False)
        r = StringRequest(payload="안녕하세요.", options=[o])
        with pytest.raises(
            (grpc.RpcError, Exception)
        ) as e:  # FIXME: Exception -> CustomExc
            p = okt_stub.Pos(r)
            print(p, e)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_nouns(okt_stub):
        s = StringRequest(payload="안녕하세요.")
        r = okt_stub.Nouns(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_morphs(okt_stub):
        s = StringRequest(payload="안녕하세요.")
        r = okt_stub.Morphs(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_phrases(okt_stub):
        s = StringRequest(payload="안녕하세요. 로보빌더입니다.")
        r = okt_stub.Phrases(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_okt_normalize(okt_stub):
        s = StringRequest(payload="안녕하세요.")
        r = okt_stub.Normalize(s)
        print(r)
        # No unhandled exception raised, test passed!
