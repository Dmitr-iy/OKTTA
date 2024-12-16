from django.contrib import admin

from chat_app.models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass
