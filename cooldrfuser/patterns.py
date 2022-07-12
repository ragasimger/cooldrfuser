from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from dj_rest_auth import urls

schemapatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(
        url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

authpatterns = [
    path("", include("apps.authentication.urls")),
]

registerpatterns = [
    path("", include("apps.user.urls")),
]
useractionpatterns = [
    path("", include("apps.user.actionurls")),
]


all_patterns = [
    path("user-action/", include(useractionpatterns)),
    path("user-auth/", include(authpatterns)),
    path("register-user/", include(registerpatterns)),
    path("admin-level-user/", include("apps.user.adminlevelurls")),
    path("auth-api/", include("apps.user.djurls")),
    path("docs/", include(schemapatterns)),
]