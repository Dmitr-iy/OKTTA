from rest_framework import serializers

from chatGPT_app.models import ChatGPT


class GptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPT
        fields = ['id', 'name', 'title', 'text', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        if 'instruction_file' not in self.context.get('request').data:
            if not (data.get('name') or data.get('title') or data.get('text')):
                raise serializers.ValidationError(
                    "At least one of 'name', 'title', or 'text' must be provided."
                )
        return data

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)


class FileGptSerializer(serializers.ModelSerializer):
    instruction_file = serializers.FileField()

    class Meta:
        model = ChatGPT
        fields = ['instruction_file']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        if 'instruction_file' not in data:
            raise serializers.ValidationError("Instruction file is required.")
        return data
