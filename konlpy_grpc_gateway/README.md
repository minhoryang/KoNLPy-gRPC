# KoNLPy-gRPC-Gateway

## Generate
```bash
go get -u github.com/grpc-ecosystem/grpc-gateway/protoc-gen-grpc-gateway
protoc -I ../protos/ -I $GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis --grpc-gateway_out=logtostderr=true,grpc_api_configuration=gateway.yaml:_generated --go_out=plugins=grpc:_generated --swagger_out=logtostderr=true,grpc_api_configuration=gateway.yaml:_generated ../protos/*.proto
```

## Run
```bash
go get -u github.com/minhoryang/KoNLPy-gRPC/konlpy_grpc_gateway
go install github.com/minhoryang/KoNLPy-gRPC/konlpy_grpc_gateway
$GOPATH/bin/konlpy_grpc_gateway -endpoint "[::]:50051" -swagger_dir _generated
```
It will run at http://localhost


## Docker Build (gRPC and Gateway)
```bash
DOCKER_BUILDKIT=1 docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t minhoryang/konlpy-grpc:v0.1.0 -f Dockerfile .
```

## Docker Run (gRPC and Gateway)
```bash
docker run -it -p 50051:50051 -p 80:80 minhoryang/konlpy-grpc:v0.1.0
```

## Thanks
https://github.com/grpc-ecosystem/grpc-gateway
