import pytest

from konlpy_grpc._generated.global_pb2 import StringRequest


@pytest.fixture(scope="module")
def mecab_stub(request):
    """Check the preconditions and Prepare the stub."""
    from konlpy_grpc._generated.mecab_pb2_grpc import MecabStub

    if not request.config.getoption("grpc-real"):
        pytest.importorskip("konlpy")
        pytest.importorskip("MeCab.Tagger", reason="Mecab is optional.")

    # Prepare the grpc-server/channel later.
    grpc_channel = request.getfixturevalue("grpc_channel")
    return MecabStub(grpc_channel)


@pytest.mark.mecab
class Testmecab:
    @staticmethod
    def test_mecab_pos(mecab_stub):
        s = StringRequest(payload="안녕하세요.")
        r = mecab_stub.Pos(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_mecab_nouns(mecab_stub):
        s = StringRequest(payload="안녕하세요.")
        r = mecab_stub.Nouns(s)
        print(r)
        # No unhandled exception raised, test passed!

    @staticmethod
    def test_mecab_morphs(mecab_stub):
        s = StringRequest(payload="안녕하세요.")
        r = mecab_stub.Morphs(s)
        print(r)
        # No unhandled exception raised, test passed!
