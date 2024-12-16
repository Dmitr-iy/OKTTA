from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema

import chat_app.views


class Fix1(OpenApiViewExtension):
    target_class = chat_app.views.ChatViewSet

    def view_replacement(self):
        @extend_schema(tags=['chats'])
        class Fixed(self.target_class):
            @extend_schema(
                summary='Получение списка чатов',
                description='Получение списка всех чатов',
            )
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)

            @extend_schema(
                summary='Получение чата',
                description='Получение чата по id',
                tags=['chats'],
            )
            def retrieve(self, request, *args, **kwargs):
                return super().retrieve(request, *args, **kwargs)

            @extend_schema(
                summary='Получение списка чатов пользователя',
                description='Получение списка чатов конкретного пользователя',
                tags=['chats'],
            )
            def my_chats(self, request, *args, **kwargs):
                return super().my_chats(request, *args, **kwargs)

        return Fixed
