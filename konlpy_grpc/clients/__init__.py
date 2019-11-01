from .._generated import global_pb2


def TupleArrayResponse(response, join=False):
    if join:
        return [result.keyword for result in response.results]
    return [(result.keyword, result.tag) for result in response.results]


def StringArrayResponse(response):
    return [result for result in response.results]


def Options(**kwargs):
    return [global_pb2.Option(key=key, value=bool(value)) for key, value in kwargs.items()]


# TODO: gRPC Inject `grpc_channel` and context in here!
