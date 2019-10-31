import pytest


@pytest.mark.compatible
class TBaseKonlpyCompatible:
    @staticmethod
    def _add_path(test_base):
        import sys
        import pathlib

        test_path = str(pathlib.Path(test_base) / "test")
        if test_path not in sys.path:
            sys.path.insert(0, test_path)

    @staticmethod
    def _import_test_py(filename):
        import importlib

        module_name = filename.split(".")[0]
        return importlib.__import__(module_name)

    @pytest.fixture(scope="class")
    def target(self, request):
        konlpy_repo = request.config.getoption("konlpy-repo")  # FIXME
        if not konlpy_repo:
            pytest.skip("konlpy-repo option required!")

        self._add_path(konlpy_repo)
        return self._import_test_py(self.TEST_PY_FILENAME)
