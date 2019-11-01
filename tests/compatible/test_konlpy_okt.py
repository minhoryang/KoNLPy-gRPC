import pytest

from conftest import TBaseKonlpyCompatible


@pytest.mark.okt
class TestKonlpyCompatibleOkt(TBaseKonlpyCompatible):
    TEST_PY_FILENAME = "test_openkoreantext.py"

    @pytest.fixture(scope="module")
    def okt_instance(self, request):
        if not request.config.getoption("grpc-real"):
            pytest.importorskip("konlpy")
            pytest.importorskip("jpype")

        from konlpy_grpc.monkeypatch import patch

        without_jpype_patching = True
        if request.config.getoption("grpc-real"):
            without_jpype_patching = False
        patch(without_jpype=without_jpype_patching)

        from konlpy.tag._okt import Okt

        grpc_channel = request.getfixturevalue("grpc_channel")
        return Okt(grpc_channel=grpc_channel)

    def test_tkorean_pos(self, target, okt_instance):
        target.test_tkorean_pos(okt_instance, target.string.__wrapped__())

    def test_tkorean_pos_1(self, target, okt_instance):
        target.test_tkorean_pos_1(okt_instance, target.string.__wrapped__())

    def test_tkorean_pos_2(self, target, okt_instance):
        target.test_tkorean_pos_2(okt_instance, target.string.__wrapped__())

    def test_tkorean_pos_3(self, target, okt_instance):
        target.test_tkorean_pos_3(okt_instance, target.string.__wrapped__())

    def test_tkorean_pos_join(self, target, okt_instance):
        target.test_tkorean_pos_join(okt_instance, target.string.__wrapped__())

    def test_tkorean_nouns(self, target, okt_instance):
        target.test_tkorean_nouns(okt_instance, target.string.__wrapped__())

    def test_tkorean_phrases(self, target, okt_instance):
        target.test_tkorean_phrases(okt_instance, target.string.__wrapped__())

    def test_tkorean_morphs(self, target, okt_instance):
        target.test_tkorean_morphs(okt_instance, target.string.__wrapped__())

    def test_tkorean_normalize(self, target, okt_instance):
        target.test_tkorean_normalize(okt_instance, target.string.__wrapped__())
