from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from chat_app.models import Chat
from chat_app.serializers import ChatSerializer


class ChatViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

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
