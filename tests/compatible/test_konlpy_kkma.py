import pytest

from conftest import TBaseKonlpyCompatible


@pytest.mark.kkma
class TestKonlpyCompatibleKkma(TBaseKonlpyCompatible):
    TEST_PY_FILENAME = "test_kkma.py"

    @pytest.fixture(scope="module")
    def kkma_instance(self, request):
        if not request.config.getoption("grpc-real"):
            pytest.importorskip("konlpy")
            pytest.importorskip("jpype")

        from konlpy_grpc.monkeypatch import patch, revert

        without_jpype_patching = True
        if request.config.getoption("grpc-real"):
            without_jpype_patching = False
        patch(without_jpype=without_jpype_patching)

        from konlpy.tag._kkma import Kkma

        grpc_channel = request.getfixturevalue("grpc_channel")
        yield Kkma(grpc_channel=grpc_channel)
        revert()

    def test_kkma_nouns(self, target, kkma_instance):
        target.test_kkma_nouns(kkma_instance, target.string.__wrapped__())

    def test_kkma_morphs(self, target, kkma_instance):
        target.test_kkma_morphs(kkma_instance, target.string.__wrapped__())

    def test_kkma_pos(self, target, kkma_instance):
        target.test_kkma_pos(kkma_instance, target.string.__wrapped__())

    def test_kkma_pos_join(self, target, kkma_instance):
        target.test_kkma_pos_join(kkma_instance, target.string.__wrapped__())

    def test_kkma_sentences(self, target, kkma_instance):
        target.test_kkma_sentences(kkma_instance, target.string.__wrapped__())
