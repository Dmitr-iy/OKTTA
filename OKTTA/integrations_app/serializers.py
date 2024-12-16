from rest_framework import serializers

from integrations_app.models import Integration


class IntegrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = ('id_integration', 'name', 'api_key', 'created_at', 'is_active', 'user')
        read_only_fields = ('id_integration', 'created_at', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        return Integration.objects.create(user=user, **validated_data)
