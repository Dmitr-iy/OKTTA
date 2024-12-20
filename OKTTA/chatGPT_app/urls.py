from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'gpt-settings', views.GptViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
