from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from chat_app.webhook import webhook
from user_app.views import RegistrationView, CustomTokenObtainPairView, confirm_email
from integrations_app.urls import router as integrations_approuter
from user_app.urls import router as users_approuter
from chat_app.urls import router as chat_approuter
from tariff_app.urls import router as tariff_approuter
from chatGPT_app.urls import router as chatGPT_approuter
from settings_app.views import WidgetView

router = routers.DefaultRouter()
router.registry.extend(integrations_approuter.registry)
router.registry.extend(users_approuter.registry)
router.registry.extend(chat_approuter.registry)
router.registry.extend(tariff_approuter.registry)
router.registry.extend(chatGPT_approuter.registry)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/registration/', RegistrationView.as_view()),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('api/settings/', WidgetView.as_view()),

    path('webhook/<id_integration>/', webhook, name='webhook'),

    path('confirm/<str:token>/', confirm_email, name='confirm_email'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
]
