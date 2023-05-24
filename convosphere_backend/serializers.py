from rest_framework.fields import CharField
from rest_framework import serializers
from django_grpc_framework import proto_serializers

from convosphere_backend.models import User, Message, Topic
from convosphere_proto import message_pb2


class MessageProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Message
        proto_class = message_pb2.Msg
        fields = "__all__"


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
