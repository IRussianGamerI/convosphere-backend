from datetime import datetime

import grpc
from google.protobuf import empty_pb2
from django_grpc_framework.services import Service
from convosphere_backend.models import Message
from convosphere_backend.serializers import MessageProtoSerializer


class MessageService(Service):
    def List(self, request, context):
        messages = Message.objects.all()
        serializer = MessageProtoSerializer(messages, many=True)
        for msg in serializer.data:
            yield msg

    def Create(self, request, context):
        serializer = MessageProtoSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise grpc.RpcError(grpc.StatusCode.NOT_FOUND, f'Message {pk} not found')

    def Retrieve(self, request, context):
        message = self.get_object(request.id)
        serializer = MessageProtoSerializer(message)
        return serializer.message

    def Update(self, request, context):
        message = self.get_object(request.id)
        serializer = MessageProtoSerializer(message, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message.edit_time = datetime.now()
        return serializer.message

    def Destroy(self, request, context):
        message = self.get_object(request.id)
        message.is_deleted = True
        return empty_pb2.Empty()
