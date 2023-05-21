import re
from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from convosphere_backend.models import Topic, Message, User
from convosphere_backend.serializers import UserSerializer, TopicSerializer, MessageSerializer, UserSignupSerializer


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        print(request.user)
        return bool(request.user and request.user.is_staff)


# View for the signup endpoint
@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        return Response({"status": "success", "message": "User created successfully"})
    else:
        return Response({"status": "error", "message": serializer.errors})


@permission_classes([IsStaffOrReadOnly])
class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('username')
        if self.request.method == "GET":
            params = self.request.query_params.dict()
            if 'q' in params:
                queryset = queryset.filter(username__contains=params['q'])
        return queryset


@permission_classes([IsStaffOrReadOnly])
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        queryset = Topic.objects.all().order_by('name')
        if self.request.method == "GET":
            params = self.request.query_params.dict()
            if 'q' in params:
                queryset = queryset.filter(name__contains=params['q'])
        return queryset


@permission_classes([IsAuthenticatedOrReadOnly])
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all().order_by('-sent_time')
        if self.request.method == "GET":
            params = self.request.query_params.dict()
            if 'q' in params:
                queryset = queryset.filter(text__contains=params['q'])
            if 'topic' in params:
                queryset = queryset.filter(topic__topic_id=params['topic'])
            if 'user' in params:
                queryset = queryset.filter(user__user_id=params['user'])
            if 'min_sent_time' in params:
                queryset = queryset.filter(sent_time__gte=params['min_sent_time'])
            if 'max_sent_time' in params:
                queryset = queryset.filter(sent_time__lte=params['max_sent_time'])
            if 'slice_from' in params:
                queryset = queryset[int(params['slice_from']):]
            if 'slice_to' in params:
                queryset = queryset[:int(params['slice_to'])]
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.user_id
        data['topic'] = Topic.objects.get(topic_id=data['topic']).topic_id
        data['sent_time'] = datetime.now()
        data['parent'] = request.data['parent'] if 'parent' in request.data and Message.objects.filter(
            message_id=request.data['parent']).exists() else None

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'text' in data and instance.text != data['text']:
            data['edit_time'] = datetime.now()

        data['user'] = request.user.user_id
        data['parent'] = request.data['parent'] if 'parent' in request.data and Message.objects.filter(
            message_id=request.data['parent']).exists() else None

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.sender or not request.user.is_staff:
            return Response({'status': 'not allowed'})
        if instance.is_deleted:
            return Response({'status': 'already deleted'})
        instance.is_deleted = True
        return Response({'status': 'ok'})
