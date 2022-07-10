from django.urls import path, include

from apps.user.views import PerformUserAction

urlpatterns = [

    path("<int:pk>/", PerformUserAction.as_view(), name="user_action"),
]