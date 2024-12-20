from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from django.core.cache import cache

from chat_app.models import Chat, Message
from chat_app.serializers import ChatSerializer, MessageSerializer
from .webhook import send_message

logger = logging.getLogger(__name__)


class ChatViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'my_chats':
            return Chat.objects.filter(user=self.request.user)

        return Chat.objects.all()

    @action(detail=False, methods=['get'], url_name='my_chats')
    def my_chats(self, request):
        """
        Эндпоинт для получения чатов пользователя.
        """
        chats = self.get_queryset()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='statistics')
    def statistics(self, request):
        """
        Эндпоинт для получения статистики чатов.
        """
        chats = self.get_queryset()
        chat_statistics = []

        for chat in chats:
            message_count = cache.get(f'message_count_{chat.id}')
            if message_count is None:
                message_count = chat.message_count()
                cache.set(f'message_count_{chat.id}', message_count, timeout=60)
            chat_data = {
                'id': chat.id,
                'name': chat.name,
                'message_count': message_count,
            }
            chat_statistics.append(chat_data)

        return Response(chat_statistics, status=status.HTTP_200_OK)


class MessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, 'managers') and user.managers.exists():
            sender_type = 'manager'
            nickname = user.managers.first().email
        else:
            sender_type = 'user'
            nickname = user.email

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            nickname=nickname,
            chat=serializer.validated_data['chat'],
            sender_type=sender_type,
            messages=serializer.validated_data['messages']
        )

        chat = serializer.validated_data['chat']
        chat_id = chat.messanger_chat_id
        full_name = f'{user.first_name}: {message.messages}'
        api_key = chat.integration.api_key

        send_message(chat_id, full_name, api_key)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
