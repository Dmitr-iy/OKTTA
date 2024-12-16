from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema

import integrations_app.views


class Fix1(OpenApiViewExtension):
    target_class = integrations_app.views.IntegrationViewSet

    def view_replacement(self):
        @extend_schema(tags=['integrations'])
        class Fixed(self.target_class):
            @extend_schema(
                summary='Получение списка интеграций',
                description='Получение списка всех интеграций',
            )
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)

            @extend_schema(
                summary='Получение интеграции',
                description='Получение интеграции по id',
                tags=['integrations'],
            )
            def retrieve(self, request, *args, **kwargs):
                return super().retrieve(request, *args, **kwargs)

            @extend_schema(
                summary='Создание интеграции',
                description='Создание интеграции. Поля: name, api_key, is_active. Поле is_active по умолчанию True',
                tags=['integrations'],
            )
            def create(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)

            @extend_schema(
                summary='Обновление интеграции',
                description='Обновление интеграции. Поля: name, api_key, is_active',
                tags=['integrations'],
            )
            def update(self, request, *args, **kwargs):
                return super().update(request, *args, **kwargs)

            @extend_schema(
                summary='Удаление интеграции',
                description='Удаление интеграции по id',
                tags=['integrations'],
            )
            def destroy(self, request, *args, **kwargs):
                return super().destroy(request, *args, **kwargs)

            @extend_schema(
                summary='Генерация QR-кода',
                description='Генерация QR-кода для интеграции с WhatsApp',
                tags=['integrations'],
            )
            def qr_code(self, request, *args, **kwargs):
                return super().qr_code(request, *args, **kwargs)

            @extend_schema(
                summary='Создание интеграции WhatsApp',
                description='Создание интеграции WhatsApp. Поля: name, api_key, is_active.'
                            ' Поле is_active по умолчанию True',
                tags=['integrations'],
            )
            def create_integration(self, request, *args, **kwargs):
                return super().create_integration(request, *args, **kwargs)

        return Fixed
