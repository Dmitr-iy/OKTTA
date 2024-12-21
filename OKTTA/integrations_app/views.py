import os
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import qrcode
import io
import base64

from common.permissions import IsUserNotManager
from integrations_app.models import Integration
from integrations_app.serializers import IntegrationsSerializer


def generate_qr_code(self, data, file_path=None):
    """Генерация QR-кода и возврат его в формате base64."""
    qr = qrcode.make(data)

    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        qr.save(file_path, format="PNG")
        print(file_path)

    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_image = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{qr_code_image}"


class IntegrationViewSet(viewsets.ModelViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationsSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    def create(self, request, *args, **kwargs):
        """
        Эндпоинт для создания интеграции.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        integration = serializer.save()
        return Response(self.get_serializer(integration).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        Эндпоинт для удаления интеграции.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_name='qr_code')
    def qr_code(self, request):
        """
        Эндпоинт для генерации QR-кода.
        """
        id_integration = request.query_params.get("id_integration")
        data = f'http://localhost:8000/api/integrations?integration_id={id_integration}/'
        file_path = "path/qr_code.png"
        if data:
            return Response(generate_qr_code(self, data, file_path), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create_integration')
    def create_integration(self, request):
        """
        Эндпоинт для создания интеграции WhatsApp.
        """
        integration_id = request.data.get('integration_id')

        if not integration_id:
            return Response({'error': 'integration_id are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={
            'name': 'WhatsApp',
            'api_key': 'your_api_key',
            'user': request.user.id,
        })
        serializer.is_valid(raise_exception=True)
        integration = serializer.save()
        return Response(self.get_serializer(integration).data, status=status.HTTP_201_CREATED)
