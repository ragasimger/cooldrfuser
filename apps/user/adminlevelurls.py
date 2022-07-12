'''
    From Packages 
'''
from apps.user.views import(
    AdminLevelUserViewSet
)
from django.conf import settings
from django.urls import path, include

from rest_framework.routers import(
    DefaultRouter, SimpleRouter
)
router = DefaultRouter() if settings.DEBUG else SimpleRouter()


'''
    From Local 
'''


router.register(r"create", AdminLevelUserViewSet,
                basename="admin_level_user_create")

urlpatterns = [
    path("", include(router.urls)),
]
