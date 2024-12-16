from django.contrib import admin

from user_app.models import Manager, User

@admin.register(Manager)
class ManagementAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
