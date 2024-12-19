from rest_framework import serializers

from chat_app.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'created_at', 'updated_at', 'integration', 'manager', 'user', 'messanger_chat_id']


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'nickname', 'sender_type', 'created_at', 'is_read', 'chat', 'messages']

        extra_kwargs = {
            'id': {'read_only': True},
            'nickname': {'read_only': True},
            'created_at': {'read_only': True},
            'is_read': {'read_only': True},
            'sender_type': {'read_only': True},
        }
