FROM golang:latest AS gateway-build
WORKDIR /build
COPY konlpy_grpc_gateway/go.mod konlpy_grpc_gateway/go.sum ./
RUN go mod download
COPY konlpy_grpc_gateway .
RUN go build -o konlpy_grpc_gateway .

FROM python:latest AS swagger-merge
WORKDIR /build
COPY --from=gateway-build /build/_generated/ /build/konlpy_grpc_gateway/_generated/
COPY tools/merge.swagger.py merge.swagger.py
RUN python3 merge.swagger.py

FROM minhoryang/konlpy:v0.5.2 AS konlpy-grpc
LABEL maintainer="Minho Ryang <minhoryang@gmail.com>"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name="minhoryang/konlpy-grpc"
LABEL org.label-schema.description="KoNLPy gRPC/HTTP Server"
LABEL org.label-schema.version="v0.1.0"

WORKDIR /app
COPY --from=ochinchina/supervisord:latest /usr/local/bin/supervisord /usr/local/bin/supervisord
COPY --from=gateway-build /build/konlpy_grpc_gateway /app/konlpy_grpc_gateway
COPY --from=swagger-merge /build/konlpy_grpc_gateway/_generated/index.swagger.json /app/_generated/index.swagger.json
COPY tools/supervisor.conf /app/supervisor.conf

# RUN python3 -m pip install konlpy-grpc
RUN python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ konlpy-grpc

CMD ["/usr/local/bin/supervisord", "-c", "supervisor.conf"]
ENTRYPOINT []
