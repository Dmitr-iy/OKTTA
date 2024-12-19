from django.contrib import admin

from chat_app.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
