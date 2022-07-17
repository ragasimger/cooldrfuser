from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from dj_rest_auth.views import (
    PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView
)


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetView.as_view(),
         name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(),
         name='rest_password_change'),
]