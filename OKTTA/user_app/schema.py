from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

import integrations_app.views
import user_app.views


class Fix1(OpenApiViewExtension):
    target_class = user_app.views.UserViewSet

    def view_replacement(self):
        @extend_schema(tags=['users'])
        class Fixed(self.target_class):
            @extend_schema(
                summary='Получение списка пользователей',
                description='Список всех пользователей',
            )
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)

            @extend_schema(
                summary='Получение пользователя',
                description='Получение пользователя по id',
                tags=['users'],
            )
            def retrieve(self, request, *args, **kwargs):
                return super().retrieve(request, *args, **kwargs)

            @extend_schema(
                summary='Обновление пользователя',
                description='Обновление данных пользователя',
                tags=['users'],
            )
            def update(self, request, *args, **kwargs):
                return super().update(request, *args, **kwargs)

            @extend_schema(
                summary='Получение менеджеров пользователя',
                description='Получение менеджеров пользователя. Можно фильтровать по id и is_active',
                parameters=[
                    OpenApiParameter(
                        name='id',
                        type=int,
                        location=OpenApiParameter.QUERY,
                        required=False,
                    ),
                    OpenApiParameter(
                        name='is_active',
                        type=bool,
                        location=OpenApiParameter.QUERY,
                        required=False,
                    ),
                ],
                responses={200: user_app.views.ManagerSerializer},
                tags=['users'],
            )
            def my_managers(self, request, *args, **kwargs):
                return super().my_managers(request, *args, **kwargs)

            @extend_schema(
                summary='интеграции пользователя',
                description='Получение списка интеграции пользователя. Можно фильтровать по id и is_active',
                parameters=[
                    OpenApiParameter(
                        name='id',
                        type=int,
                        location=OpenApiParameter.QUERY,
                        required=False,
                    ),
                    OpenApiParameter(
                        name='is_active',
                        type=bool,
                        location=OpenApiParameter.QUERY,
                        required=False,
                    ),
                ],
                responses={200: integrations_app.views.IntegrationsSerializer},
                tags=['users'],
            )
            def my_integrations(self, request, *args, **kwargs):
                return super().my_integrations(request, *args, **kwargs)

            @extend_schema(
                summary='Статистика сообщений и количества чатов пользователя',
                description='Статистика сообщений и количества чатов пользователя. \n\n'
                            'Принимает id пользователя. \n\n Возвращает: данные пользователя,'
                            ' список чатов с их id и количеством сообщений, \n\n'
                            'количество чатов пользователя.',
                examples=[
                    OpenApiExample(
                        'Пример ответа',
                        value={
                            "user_data": {"data user"},
                            "chat_message_count": [{
                                "chat_id": 1,
                                "message_count": 8
                                },
                                {
                                  "chat_id": 2,
                                  "message_count": 4
                                }
                              ],
                            "chat_count": 2
                        },
                    ),
                ],
                tags=['statistics'],
            )
            def statistics(self, request, *args, **kwargs):
                return super().statistics(request, *args, **kwargs)

        return Fixed


class Fix2(OpenApiViewExtension):
    target_class = user_app.views.ManagerViewSet

    def view_replacement(self):
        @extend_schema(tags=['managers'])
        class Fixed(self.target_class):
            @extend_schema(
                summary='Получение списка менеджеров',
                description='Список всех менеджеров',
            )
            def list(self, request, *args, **kwargs):
                return super().list(request, *args, **kwargs)

            @extend_schema(
                summary='Создание менеджера',
                description='Создание менеджера. Поля: email. Поле is_active по умолчанию False. '
                            'Для изменения поля is_active необходимо подтвердить email.',
                tags=['managers'],
            )
            def create(self, request, *args, **kwargs):
                return super().create(request, *args, **kwargs)

            @extend_schema(
                summary='Получение менеджера',
                description='Получение менеджера по id',
                tags=['managers'],
            )
            def retrieve(self, request, *args, **kwargs):
                return super().retrieve(request, *args, **kwargs)

            @extend_schema(
                summary=' Удаление менеджера',
                description='Удаление менеджера по id',
                tags=['managers'],
            )
            def destroy(self, request, *args, **kwargs):
                return super().destroy(request, *args, **kwargs)
        return Fixed
