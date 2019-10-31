import grpc
import pytest

from konlpy_grpc._generated.global_pb2 import Option, StringRequest


@pytest.fixture(scope="module")
def kkma_stub(request):
    """Check the preconditions and Prepare the stub."""
    from konlpy_grpc._generated.kkma_pb2_grpc import KkmaStub

    if not request.config.getoption("grpc-real"):
        pytest.importorskip("konlpy")
        pytest.importorskip("jpype")

    # Prepare the grpc-server/channel later.
    grpc_channel = request.getfixturevalue("grpc_channel")
    return KkmaStub(grpc_channel)


@pytest.mark.kkma
class TestKkma:
    @staticmethod
    def test_kkma_pos(kkma_stub):
        s = StringRequest(payload="안녕하세요.")
        r = kkma_stub.Pos(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_kkma_pos_with_bypass_option(kkma_stub):
        o = Option(key="flatten", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o])
        p = kkma_stub.Pos(r)
        print(p)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_kkma_pos_with_wrong_option(kkma_stub):
        o = Option(key="wrong", value=False)
        r = StringRequest(payload="안녕하세요.", options=[o])
        with pytest.raises((grpc.RpcError, Exception)) as e:  # FIXME: Exception -> CustomExc
            p = kkma_stub.Pos(r)
            print(p, e)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_kkma_nouns(kkma_stub):
        s = StringRequest(payload="안녕하세요.")
        r = kkma_stub.Nouns(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_kkma_morphs(kkma_stub):
        s = StringRequest(payload="안녕하세요.")
        r = kkma_stub.Morphs(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_kkma_sentences(kkma_stub):
        s = StringRequest(payload="안녕하세요. 로보빌더입니다.")
        r = kkma_stub.Sentences(s)
        print(r)
        # No unhandled exception raised, test passed!
