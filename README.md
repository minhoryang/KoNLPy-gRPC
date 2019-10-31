# KoNLPy-gRPC
Redesigned KoNLPy (Wrapper) for Usability and Portability with gRPC.

## gRPC Compile needed!
```bash
python -m grpc_tools.protoc -I protos/ --python_out=konlpy_grpc/_generated/ --grpc_python_out=konlpy_grpc/_generated/ protos/*.proto
```

## Server
```bash
python -m pip install konlpy
```

```bash
python -m konlpy_grpc server
python -m konlpy_grpc hannanum_server
python -m konlpy_grpc kkma_server
python -m konlpy_grpc komoran_server
python -m konlpy_grpc mecab_server
python -m konlpy_grpc okt_server
```

## Tests
```bash
python -m pytest
python -m pytest --grpc-fake-server
python -m pytest --grpc-real-server=[::]:50051
python -m pytest --konlpy-repo=../konlpy
```

## TODO
- [x] [P0] client.py will be a konlpy-alike module.
  - [x] [P0] KoNLPy monkey-patcher
- [P1] gRPC Proto Compile
- [P1] setup.py, requirements.txt, bumpversion, ...
  - PyPI Register
- [P1] KoNLPy Version Matching (set minimum) and Follow-up
- [P1] gRPC retry/timeout/error_handling logic <!-- google.api_core.* or grpc-retry-py -->
- [P2] Dockerize / Register
  - k8s and istio?
- [P2] CI
- [P3] Button for deploying this to AWS/GCS/Azure now! (and connect by README.)
- [P3] CustomDic?
- [P3] Stream I/O
- [P3] Redesign tests/ with grpc-testing
- [P4] Java Edition for KoNLPy-gRPC-Server
  - gRPC protos deploy/versioning

## Additional Links
- [KoNLPy/KoNLPy](https://github.com/konlpy/konlpy)
- [Pruned KoNLPy v0.5.2-rc.1](https://github.com/minhoryang/konlpy)
  - Currently, servers rely on KoNLPy v0.5.2-rc.1 version.

## License
GNU GPLv3
