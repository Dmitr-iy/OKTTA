from django.contrib import admin

from integrations_app.models import Integration

@admin.register(Integration)
class ManagementAdmin(admin.ModelAdmin):
    pass
