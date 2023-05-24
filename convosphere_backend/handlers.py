from convosphere_backend.services import MessageService
from convosphere_proto import message_pb2_grpc


def grpc_handlers(server):
    message_pb2_grpc.add_MsgControllerServicer_to_server(MessageService.as_servicer(), server)
