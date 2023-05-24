from rest_framework.fields import CharField
from rest_framework import serializers
from django_socio_grpc import proto_serializers

from convosphere_backend.models import User, Message, Topic
from convosphere_backend.grpc import convosphere_backend_pb2


class MessageProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Message
        proto_class = convosphere_backend_pb2.Message
        proto_class_list = convosphere_backend_pb2.MessageList
        fields = ['id', 'parent', 'topic', 'sender', 'text', 'sent_time', 'edit_time', 'is_deleted']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "is_superuser", "is_active", "date_joined", "last_login"]


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class LoginRequestSerializer(serializers.Serializer):
    model = User
    username = CharField(required=True)
    password = CharField(required=True)
