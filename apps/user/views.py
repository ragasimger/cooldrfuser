'''
    From Local 
'''
from apps.user.serializers import(
    UserRegisterSerializer, AdminLevelUserSerializer, VerifyOtp, UserUpdateSerializer
)
from apps.user.permissions import IsStaff, CustomNotAllowed, UserPerformActionPermission
from apps.user.sendemails import send_otp
from apps.user.utils import CompleteCRUDUser, OTPVerification


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
    lookup_field = 'pk'
    auth_perms_error = Response(
        {
        'status': 404,
        "detail": "You are not authorized to perform this action."
        }
        )


class ResendOtp(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request, serializer, *args, **kwargs):
        email = serializer.validated_data['email']
        send_otp(email)

class VerifyOtp(OTPVerification):
    serializer_class = VerifyOtp



class AdminLevelUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("first_name")
    serializer_class = AdminLevelUserSerializer
    permission_classes = (IsStaff,)
    search_fields = ("username",)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ("username", "email", "first_name",)
