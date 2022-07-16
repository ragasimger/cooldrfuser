'''
    From Local 
'''
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import (
    filters, viewsets, generics
)
from apps.user.process_social.serializers import (
    FacebookSocialAuthSerializer, GoogleSocialAuthSerializer, TwitterAuthSerializer
)
from apps.user.serializers import(
    UserRegisterSerializer, AdminLevelUserSerializer, UserUpdateSerializer, VerifyOtpSerializer, ResendOtpSerializer
)
from apps.user.permissions import IsStaff, UserPerformActionPermission
from apps.user.sendemails import send_otp
from apps.user.utils import CompleteCRUDUser, OTPResent, OTPVerification

'''
    From Packages
'''

# Package Imports End


class UserRegistration(generics.CreateAPIView, CreateModelMixin):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        serializer.validated_data['is_active'] = False
        serializer.save()
        email = serializer.data['email']
        send_otp(email)


class PerformUserAction(CompleteCRUDUser, UserPerformActionPermission):
    serializer_class = UserUpdateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'
    auth_perms_error = Response(
        {
            'status': 404,
            "detail": "You are not authorized to perform this action."
        }
    )


class ResendOtp(OTPResent):
    serializer_class = ResendOtpSerializer


class VerifyOtp(OTPVerification):
    serializer_class = VerifyOtpSerializer


class AdminLevelUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("first_name")
    serializer_class = AdminLevelUserSerializer
    permission_classes = (IsStaff,)
    search_fields = ("username",)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ("username", "email", "first_name",)


class FacebookLoginSignUpView(SocialLoginView):
    serializer_class = FacebookSocialAuthSerializer
    adapter_class = FacebookOAuth2Adapter


class TwitterLoginSignUpView(SocialLoginView):
    serializer_class = TwitterAuthSerializer
    adapter_class = TwitterOAuthAdapter


class GoogleLoginSignUpView(SocialLoginView):
    serializer_class = GoogleSocialAuthSerializer
    adapter_class = GoogleOAuth2Adapter
