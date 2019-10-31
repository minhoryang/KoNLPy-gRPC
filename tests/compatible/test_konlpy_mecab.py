import pytest

from conftest import TBaseKonlpyCompatible


@pytest.mark.mecab
class TestKonlpyCompatibleMecab(TBaseKonlpyCompatible):
    TEST_PY_FILENAME = "test_mecab.py"

    @pytest.fixture(scope="module")
    def mecab_instance(self, request):
        if not request.config.getoption("grpc-real"):
            pytest.importorskip("konlpy")
            pytest.importorskip("MeCab", reason="Mecab is optional.")

        from konlpy_grpc.monkeypatch import patch

        without_jpype_patching = True
        if request.config.getoption("grpc-real"):
            without_jpype_patching = False
        patch(without_jpype=without_jpype_patching)

        from konlpy.tag._mecab import Mecab

        grpc_channel = request.getfixturevalue("grpc_channel")
        return Mecab(grpc_channel=grpc_channel)

    def test_mecab_pos_43(self, target, mecab_instance):
        target.test_mecab_pos_43(mecab_instance, target.string.__wrapped__())

    def test_mecab_pos_join(self, target, mecab_instance):
        target.test_mecab_pos_join(mecab_instance, target.string.__wrapped__())

    def test_mecab_morphs(self, target, mecab_instance):
        target.test_mecab_morphs(mecab_instance, target.string.__wrapped__())

    def test_mecab_nouns(self, target, mecab_instance):
        target.test_mecab_nouns(mecab_instance, target.string.__wrapped__())
