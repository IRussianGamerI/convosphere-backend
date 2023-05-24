from abc import ABC
from datetime import datetime

import grpc
from django_socio_grpc.protobuf.json_format import message_to_dict
from google.protobuf import empty_pb2
from django_socio_grpc import generics, mixins
from convosphere_backend.models import Message
from convosphere_backend.serializers import MessageProtoSerializer


class MessageService(mixins.AsyncCreateModelMixin, mixins.AsyncListModelMixin, mixins.AsyncUpdateModelMixin,
                     mixins.AsyncRetrieveModelMixin, mixins.AsyncPartialUpdateModelMixin, generics.GenericService):
    queryset = Message.objects.filter(is_deleted=False).order_by('-sent_time')
    serializer_class = MessageProtoSerializer
