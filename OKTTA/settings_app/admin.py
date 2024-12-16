from django.contrib import admin

from settings_app.models import Widget

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    pass
# Register your models here.
