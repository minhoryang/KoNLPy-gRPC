import json

import grpc
from google.protobuf.json_format import MessageToJson

from ._generated import global_pb2, hannanum_pb2_grpc
from .clients import StringArrayResponse, TupleArrayResponse


def run():
    k = global_pb2.Option(key="flatten", value=True)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hannanum_pb2_grpc.HannanumStub(channel)  # TODO: multiple choices.
        response = stub.Pos09(global_pb2.StringRequest(payload="안녕하세요.", options=[k]))
        print("client received j> ", json.loads(MessageToJson(response)))
        print("client received >> ", TupleArrayResponse(response))
        response = stub.Nouns(global_pb2.StringRequest(payload="안녕하세요."))
        print("client received: ", StringArrayResponse(response))
        response = stub.Morphs(global_pb2.StringRequest(payload="안녕하세요."))
        print("client received: ", json.loads(MessageToJson(response)))
        response = stub.Analyze(global_pb2.StringRequest(payload="안녕하세요. 로보빌더입니다."))
        print("client received: ", json.loads(MessageToJson(response)))


if __name__ == "__main__":
    run()
