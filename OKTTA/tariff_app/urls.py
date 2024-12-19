from django.urls import include, path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'plans', views.PlansViewSet)
router.register(r'plan_users', views.PlansUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]
