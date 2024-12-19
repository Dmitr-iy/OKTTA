from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Plan

User = get_user_model()


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'tokens']
        extra_kwargs = {
            'id': {'read_only': True},
            'tokens': {'read_only': True},
            'price': {'read_only': True},
            'name': {'read_only': True},
        }


class UsersSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'plan', 'tokens_purchased']
        extra_kwargs = {
            'id': {'read_only': True},
            'tokens_purchased': {'read_only': True},
            'email': {'read_only': True},
        }

    def update(self, instance, validated_data):
        plan = validated_data.pop('plan', None)
        if plan:
            instance.plan = plan
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     plan_data = validated_data.pop('plan', None)
    #     if plan_data:
    #         plan = Plan.objects.get(id=plan_data['id'])
    #         instance.plan = plan
    #     instance.tokens_purchased = validated_data.get('tokens_purchased', instance.tokens_purchased)
    #     instance.save()
    #     return instance
