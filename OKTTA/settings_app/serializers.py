from rest_framework import serializers

from settings_app.models import Widget


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['widget_code']
