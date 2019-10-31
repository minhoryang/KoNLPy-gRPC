import pytest

from conftest import TBaseKonlpyCompatible


@pytest.mark.hannanum
class TestKonlpyCompatibleHannanum(TBaseKonlpyCompatible):
    TEST_PY_FILENAME = "test_hannanum.py"

    @pytest.fixture(scope="module")
    def hannanum_instance(self, request):
        if not request.config.getoption("grpc-real"):
            pytest.importorskip("konlpy")
            pytest.importorskip("jpype")

        from konlpy_grpc.monkeypatch import patch, revert

        without_jpype_patching = True
        if request.config.getoption("grpc-real"):
            without_jpype_patching = False
        patch(without_jpype=without_jpype_patching)

        from konlpy.tag._hannanum import Hannanum

        grpc_channel = request.getfixturevalue("grpc_channel")
        yield Hannanum(grpc_channel=grpc_channel)
        revert()

    def test_hannanum_analyze(self, target, hannanum_instance):
        target.test_hannanum_analyze(hannanum_instance, target.string.__wrapped__())

    def test_hannanum_nouns(self, target, hannanum_instance):
        target.test_hannanum_nouns(hannanum_instance, target.string.__wrapped__())

    def test_hannanum_morphs(self, target, hannanum_instance):
        target.test_hannanum_morphs(hannanum_instance, target.string.__wrapped__())

    def test_hannanum_pos_9(self, target, hannanum_instance):
        target.test_hannanum_pos_9(hannanum_instance, target.string.__wrapped__())

    def test_hannanum_pos_22(self, target, hannanum_instance):
        target.test_hannanum_pos_22(hannanum_instance, target.string.__wrapped__())

    def test_hannanum_pos_join(self, target, hannanum_instance):
        target.test_hannanum_pos_join(hannanum_instance, target.string.__wrapped__())
