import grpc
import pytest

from konlpy_grpc._generated.global_pb2 import Option, StringRequest


@pytest.fixture(scope="module")
def hannanum_stub(request):
    """Check the preconditions and Prepare the stub."""
    from konlpy_grpc._generated.hannanum_pb2_grpc import HannanumStub

    if not request.config.getoption("grpc-real"):
        pytest.importorskip("konlpy")
        pytest.importorskip("jpype")

    # Prepare the grpc-server/channel later.
    grpc_channel = request.getfixturevalue("grpc_channel")
    return HannanumStub(grpc_channel)


@pytest.mark.hannanum
class TestHannanum:
    @staticmethod
    def test_hannanum_pos09(hannanum_stub):
        s = StringRequest(payload="안녕하세요.")
        r = hannanum_stub.Pos09(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_pos22(hannanum_stub):
        s = StringRequest(payload="안녕하세요.")
        r = hannanum_stub.Pos22(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_pos09_with_bypass_option(hannanum_stub):
        o = Option(key="flatten", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o])
        p = hannanum_stub.Pos09(r)
        print(p)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_pos09_with_wrong_option(hannanum_stub):
        o = Option(key="wrong", value=False)
        r = StringRequest(payload="안녕하세요.", options=[o])
        with pytest.raises(
            (grpc.RpcError, Exception)
        ) as e:  # FIXME: Exception -> CustomExc
            p = hannanum_stub.Pos09(r)
            print(p, e)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_pos09_with_additional_ntags_option(hannanum_stub):
        o = Option(key="ntag:09", value=True)
        r = StringRequest(payload="안녕하세요.", options=[o])
        with pytest.raises(
            (grpc.RpcError, Exception)
        ) as e:  # FIXME: Exception -> CustomExc
            p = hannanum_stub.Pos09(r)
            print(p, e)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_nouns(hannanum_stub):
        s = StringRequest(payload="안녕하세요.")
        r = hannanum_stub.Nouns(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_hannanum_morphs(hannanum_stub):
        s = StringRequest(payload="안녕하세요.")
        r = hannanum_stub.Morphs(s)
        print(r)
        # No unhandled exception raised, test passed!
