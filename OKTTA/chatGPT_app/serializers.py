from rest_framework import serializers

from chatGPT_app.models import ChatGPT


class GptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPT
        fields = ['id', 'name', 'title', 'text', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        text = self.context['request'].data.get('text')
        tokens_purchased = self.context['request'].user.tokens_purchased
        if len(text) / 2 <= tokens_purchased:
            print(';;', len(text))
            return super().create(validated_data)

        raise serializers.ValidationError("Недостаточно токенов.")

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
        tokens_purchased = self.context['request'].user.tokens_purchased
        instruction_file = validated_data.get('instruction_file')

        if instruction_file:
            with instruction_file.open('r', encoding='utf-8') as file:
                file_content = file.read()
                file_length = len(file_content)

            if file_length / 2 <= tokens_purchased:
                return super().create(validated_data)
            else:
                raise serializers.ValidationError("Недостаточно токенов.")
        else:
            raise serializers.ValidationError("Файл не был загружен.")

    def validate(self, data):
        if 'instruction_file' not in data:
            raise serializers.ValidationError("Instruction file is required.")
        return data
