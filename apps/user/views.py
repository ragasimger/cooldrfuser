'''
    From Local 
'''
from apps.user.serializers import(
    UserRegisterSerializer, AdminLevelUserSerializer, UserUpdateSerializer, VerifyOtpSerializer, ResendOtpSerializer
)
from apps.user.permissions import IsStaff, UserPerformActionPermission
from apps.user.sendemails import send_otp
from apps.user.utils import CompleteCRUDUser, OTPResent, OTPVerification


'''
    From Packages
'''
from rest_framework import (
    filters, viewsets, generics
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

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
    permission_classes=[IsAuthenticated,]
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
