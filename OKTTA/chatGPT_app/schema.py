from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema

import chatGPT_app.views
import chatGPT_app.serializers


class Fix1(OpenApiViewExtension):
    target_class = chatGPT_app.views.GptViewSet

    def view_replacement(self):
        @extend_schema(tags=['gpt-settings'])
        class Fixed(self.target_class):
            @extend_schema(
                summary='Получение списка gpt-settings',
                description='Получение списка всех gpt-settings',
            )
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)

            @extend_schema(
                summary='Получение gpt-settings',
                description='Получение gpt-settings по id',
            )
            def retrieve(self, request, *args, **kwargs):
                return super().retrieve(request, *args, **kwargs)

            @extend_schema(
                summary='Создание gpt-settings',
                description='Создание gpt-settings. Поля: name, title, text.',
            )
            def create(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)

            @extend_schema(
                summary='Обновление gpt-settings',
                description='Обновление gpt-settings.',
            )
            def update(self, request, *args, **kwargs):
                return super().update(request, *args, **kwargs)

            @extend_schema(
                summary='Удаление gpt-settings',
                description='Удаление gpt-settings по id',
            )
            def destroy(self, request, *args, **kwargs):
                return super().destroy(request, *args, **kwargs)

            @extend_schema(
                summary='Создание gpt-settings',
                description='Создание gpt-settings принимает файл',
                request=chatGPT_app.serializers.FileGptSerializer
            )
            def file_upload(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)

        return Fixed
