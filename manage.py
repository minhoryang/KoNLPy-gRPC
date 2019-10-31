if __name__ == "__main__":  # FIXME: with click!
    import sys
    import os

    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, CURRENT_DIR)

    if len(sys.argv) != 2:
        raise Exception()
    mode = sys.argv[1]
    if mode == "test":
        import pytest

        pytest.main([CURRENT_DIR])
    elif mode == "test-fake":
        import pytest

        pytest.main([CURRENT_DIR, "--grpc-fake-server"])
    else:
        raise Exception()
