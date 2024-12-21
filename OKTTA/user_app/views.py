from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from django.core.cache import cache

from common.permissions import IsUserNotManager
from integrations_app.models import Integration
from integrations_app.serializers import IntegrationsSerializer
from .models import Manager
from .serializers import RegistrationSerializer, MyTokenObtainPairSerializer, UserSerializer, ManagerSerializer

User = get_user_model()

# Регистрация
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @extend_schema(summary='Регистрация пользователя', description='Регистрация пользователя',
                   request=RegistrationSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# Токен для авторизации
class CustomTokenObtainPairView(APIView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.create(serializer.validated_data))

# Пользователь
class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    def filter_queryset(self, queryset):
        if self.action == 'my_managers':
            is_active = self.request.query_params.get('is_active', None)
            if is_active is not None:
                if is_active.lower() == 'true':
                    queryset = queryset.filter(is_active=True)
                elif is_active.lower() == 'false':
                    queryset = queryset.filter(is_active=False)
            pk = self.request.query_params.get('id')
            if pk is not None:
                return Manager.objects.filter(user=self.request.user, id=pk)
        return super().filter_queryset(queryset)

    def get_queryset(self):

        if self.action == 'my_managers':
            return Manager.objects.filter(user=self.request.user)

        if self.action == 'my_integrations':
            return Integration.objects.filter(user=self.request.user)

        return User.objects.all()

    @action(detail=False, methods=['get'], url_name='my_integrations')
    def my_integrations(self, request):
        """
        Получение интеграций пользователя
        """
        integrations = self.get_queryset()
        serializer = IntegrationsSerializer(integrations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_name='my_managers')
    def my_managers(self, request):
        """
        Получение менеджеров пользователя
        """
        managers = self.get_queryset()
        filtered_managers = self.filter_queryset(managers)
        serializer = ManagerSerializer(filtered_managers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_name='statistics_user')
    def statistics(self, request, pk=None):
        """
        Эндпоинт для получения статистики пользователя.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User  not found."}, status=404)

        user_data = self.serializer_class(user).data
        chat_message_count = cache.get(f'chat_message_count_{user.id}')
        print(chat_message_count)
        chat_count = cache.get(f'chat_count_{user.id}')
        print('chat_count', chat_count)

        response_data = {
            'user_data': user_data,
            'chat_message_count': chat_message_count,
            'chat_count': chat_count
        }
        return Response(response_data)

# создание, удаление, получение менеджера
class ManagerViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAuthenticated | IsUserNotManager]

    def create(self, request, *args, **kwargs):
        """
        Создает менеджера
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        manager = serializer.save()
        return Response(self.get_serializer(manager).data, status=status.HTTP_201_CREATED)


def generate_token(manager):
    """
    Генерирует токен для подтверждения почты менеджера
    """
    print(manager.id)
    return signing.dumps(manager.id)


def confirm_email(request, token):
    """
    Подтверждает почту менеджера
    """
    try:
        manager_id = signing.loads(token)
        manager = get_object_or_404(Manager, id=manager_id)
        manager.is_active = True
        manager.save()
        return HttpResponse('почта подтверждена')
    except signing.BadSignature:
        raise SuspiciousOperation("ссылка устарела")
