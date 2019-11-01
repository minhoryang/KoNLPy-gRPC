if __name__ == "__main__":  # FIXME: with click! (or sdispater/cleo)
    import sys

    if len(sys.argv) != 2:
        raise Exception()
    mode = sys.argv[1]
    if mode == "test":
        pass  # TODO: python -m pytest (...)
    elif mode == "build:grpc":
        pass  # TODO: python -m grpc_tools.protoc -I protos/ --python_out=konlpy_grpc/_generated/ --grpc_python_out=konlpy_grpc/_generated/ protos/*.proto
    elif mode == "coverage":
        pass  # TODO: (REQUIRED: test)
        # python -m pytest --cov=konlpy_grpc --cov-report=xml --konlpy-repo=../konlpy
        # python -m pytest --cov=konlpy_grpc --cov-report=xml --cov-append --konlpy-repo=../konlpy --grpc-fake-server
        # python -m pytest --cov=konlpy_grpc --cov-report=xml --cov-append --konlpy-repo=../konlpy --grpc-real-server=[::]:50051
    elif mode == "coverage:html":
        from coverage import Coverage

        c = Coverage()
        c.load()
        c.html_report(directory="covhtml")
    elif mode == "git:cleanup":
        pass  # TODO
    elif mode == "bumpversion":
        pass  # TODO: bump2version --allow-dirty --dry-run --verbose patch
    elif mode in ("requirements.txt", "poetry:requirements.txt"):  # XXX: https://github.com/sdispater/poetry/issues/100#issuecomment-409807277
        import tomlkit

        with open("poetry.lock") as t:
            lock = tomlkit.parse(t.read())
            for p in lock["package"]:
                if not p["category"] == "dev":
                    print(f"{p['name']}=={p['version']}")
    elif mode in ("requirements-dev.txt", "poetry:requirements-dev.txt"):  # XXX: https://github.com/sdispater/poetry/issues/100#issuecomment-409807277
        import tomlkit

        with open("poetry.lock") as t:
            lock = tomlkit.parse(t.read())
            for p in lock["package"]:
                if p["category"] == "dev":
                    print(f"{p['name']}=={p['version']}")
    else:
        raise Exception()
