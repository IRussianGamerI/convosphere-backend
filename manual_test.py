import grpc

from convosphere_backend.grpc import convosphere_backend_pb2, convosphere_backend_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = convosphere_backend_pb2_grpc.MessageControllerStub(channel)

    print("--------------Create--------------")
    response = stub.Create(convosphere_backend_pb2.Message(sender=1, topic=1, text="Hello there!"))
    print(response)

    print("--------------Retrieve--------------")
    response = stub.Retrieve(convosphere_backend_pb2.MessageRetrieveRequest(id=response.id))
    print(response)

    print("--------------List--------------")
    print(stub.List(convosphere_backend_pb2.MessageListRequest()))

    print("------------Update--------------")
    response = stub.Update(convosphere_backend_pb2.Message(id=response.id, sender=1, topic=1, text="Hello World!"))
    print(response)

    print("--------------PartialUpdate--------------")
    response = stub.PartialUpdate(
        convosphere_backend_pb2.MessagePartialUpdateRequest(id=response.id, sender=2, text="Hello World again!",
                                                            _partial_update_fields=["sender", "text"])
    )
    print(response)

    print("--------------Destroy--------------")
    response = stub.PartialUpdate(
        convosphere_backend_pb2.MessagePartialUpdateRequest(id=response.id, is_deleted=True,
                                                            _partial_update_fields=["is_deleted"])
    )
    print(response)

    print("--------------List--------------")
    print(stub.List(convosphere_backend_pb2.MessageListRequest()))
