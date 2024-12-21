
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatGPT_app.models import ChatGPT
from chatGPT_app.serializers import GptSerializer, FileGptSerializer
from common.permissions import IsUserNotManager


# Представление для работы с моделью ChatGPT.
class GptViewSet(viewsets.ModelViewSet):
    queryset = ChatGPT.objects.all()
    serializer_class = GptSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    @action(detail=False, methods=['post'], url_name='file_upload')
    def file_upload(self, request):
        """
        Загрузка файла
        """
        request.validated_data['user'] = request.user
        serializer_class = FileGptSerializer
        serializer_class = serializer_class(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        chat_gpt_instance = ChatGPT(
            instruction_file=serializer_class.validated_data['instruction_file'],
            user=request.user
        )
        chat_gpt_instance.save()
        return Response({'status': 'file uploaded'}, status=status.HTTP_201_CREATED)
