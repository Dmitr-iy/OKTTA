from django.contrib import admin

from chatGPT_app.models import ChatGPT


@admin.register(ChatGPT)
class ChatGPTAdmin(admin.ModelAdmin):
    pass
