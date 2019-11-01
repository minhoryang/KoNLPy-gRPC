import pytest

from conftest import TBaseKonlpyCompatible


@pytest.mark.komoran
class TestKonlpyCompatibleKomoran(TBaseKonlpyCompatible):
    TEST_PY_FILENAME = "test_komoran.py"

    @pytest.fixture(scope="module")
    def komoran_instance(self, request):
        if not request.config.getoption("grpc-real"):
            pytest.importorskip("konlpy")
            pytest.importorskip("jpype")

        from konlpy_grpc.monkeypatch import patch

        without_jpype_patching = True
        if request.config.getoption("grpc-real"):
            without_jpype_patching = False
        patch(without_jpype=without_jpype_patching)

        from konlpy.tag._komoran import Komoran

        grpc_channel = request.getfixturevalue("grpc_channel")
        return Komoran(grpc_channel=grpc_channel)

    def test_komoran_nouns(self, target, komoran_instance):
        target.test_komoran_nouns(komoran_instance, target.string.__wrapped__())

    def test_komoran_pos(self, target, komoran_instance):
        target.test_komoran_pos(komoran_instance, target.string.__wrapped__())

    def test_komoran_pos_join(self, target, komoran_instance):
        target.test_komoran_pos_join(komoran_instance, target.string.__wrapped__())

    def test_komoran_morphs(self, target, komoran_instance):
        target.test_komoran_morphs(komoran_instance, target.string.__wrapped__())
