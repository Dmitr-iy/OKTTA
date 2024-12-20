from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
import re

from user_app.models import Manager

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, value):
        if len(value) < 8 or len(value) > 64:
            raise serializers.ValidationError("Пароль должен содержать от 8 до 64 символов.")

        if not re.search(r'[a-zA-Zа-яА-Я]', value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну букву (латинскую или кириллическую).")

        if not re.search(r'\d', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру.")

        special_characters = r'[.!#$%&\'*+\/=?^_`{|}~ ]'
        if not re.search(special_characters, value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы один специальный символ: .!#$%&'*+/=?^_`{|}~ ")
        return value


class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Пользователь с таким email не найден.')

        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль.')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'email', 'is_active']

        extra_kwargs = {
            'id': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return Manager.objects.create(user=user, **validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'family_name', 'phone_number', 'name_company',
                  'website_link', 'plan', 'tokens_purchased']

        extra_kwargs = {
            'id': {'read_only': True},
            'plan': {'read_only': True},
            'tokens_purchased': {'read_only': True},
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.family_name = validated_data.get('family_name', instance.family_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.name_company = validated_data.get('name_company', instance.name_company)
        instance.website_link = validated_data.get('website_link', instance.website_link)
        instance.save()
        return instance

    def validate(self, value):
        print(f"Received phone number for validation: {value}")

        if value.startswith('+7'):
            value = value.replace('+7', '8', 1)
        elif value.startswith('7'):
            value = value.replace('7', '8', 1)

        phone = ''.join(filter(str.isdigit, value))
        print(f"Processed phone number: {phone}")

        if 10 > len(phone) or len(phone) > 15:
            raise ValidationError(message='Не правильный формат телефона')

        return value
