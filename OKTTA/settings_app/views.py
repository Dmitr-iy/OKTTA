from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsUserNotManager
from .models import Widget
from .serializers import WidgetSerializer

class WidgetView(APIView):
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    @extend_schema(
        summary='Получение виджет кода',
        description='Получение виджет кода в виде html',
        tags=['settings'],
    )
    def get(self, request):
        """
        Получение виджет кода
        """
        widgets = Widget.objects.all()
        serializer = self.serializer_class(widgets, many=True)
        return Response(serializer.data)
