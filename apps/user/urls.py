'''
    From Packages 
'''
from apps.user.views import(
    UserRegistration, ResendOtp, VerifyOtp
)
from django.conf import settings
from django.urls import path

from rest_framework.routers import(
    DefaultRouter, SimpleRouter
)
router = DefaultRouter() if settings.DEBUG else SimpleRouter()


'''
    From Local 
'''


urlpatterns = [
    path("create-user/", UserRegistration.as_view(), name="create_user"),
    path("resend/otp/", ResendOtp.as_view(), name="resend_otp"),
    path("verify/otp/", VerifyOtp.as_view(), name="verify_otp"),
]
