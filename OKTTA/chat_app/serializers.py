from rest_framework import serializers

from chat_app.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'created_at', 'updated_at', 'integration', 'manager', 'user']
