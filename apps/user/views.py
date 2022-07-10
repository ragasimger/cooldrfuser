'''
    From Local 
'''
from apps.user.serializers import(
    UserRegisterSerializer, AdminLevelUserSerializer, VerifyOtp, UserUpdateSerializer
)
from apps.user.permissions import IsStaff, UserPerm
from apps.user.sendemails import send_otp


'''
    From Packages
'''
from rest_framework import (
    filters, viewsets, generics, views
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.renderers import JSONRenderer

class UserRegistration(generics.CreateAPIView, CreateModelMixin):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        serializer.validated_data['is_active'] = False
        serializer.save()
        email = serializer.data['email']
        send_otp(email)


class PerformUserAction(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserUpdateSerializer
    # permission_classes = [UserPerm,]
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'
    auth_perms_error = Response(
        {
        'status': 404,
        "detail": "You are not authorized to perform this action."
        }
        )

    def get_user_id(self, request, *args, **kwargs):

        serializer = self.serializer_class(self.get_object())
        return serializer.data['id']

    def check_staff_status(self, request, *args, **kwargs):

        return self.request.user.is_staff


    def wrap_perms(self, request, *args):

        id_ = self.get_user_id(self, request)
        staff = self.check_staff_status(self, request)
        if self.request.user.id == id_ or staff:

            return True

    def get(self, request, *args, **kwargs):

        if self.wrap_perms(self, request, *args):

            return self.retrieve(request, *args, **kwargs)
        
        self.permission_classes=[UserPerm,]
        return self.auth_perms_error

    def put(self, request, *args, **kwargs):

        if self.wrap_perms(self, request, *args):
            # needs work for the otp (if created in last hour -> pass) to confirm changes

            return self.update(request, *args, **kwargs)

        return self.auth_perms_error

    def patch(self, request, *args, **kwargs):

        if self.wrap_perms(self, request, *args):
            # needs work for the otp (if created in last hour -> pass) to confirm changes

            return self.partial_update(request, *args, **kwargs)

        return self.auth_perms_error

    def delete(self, request, *args, **kwargs):

        if self.wrap_perms(self, request, *args):
            # needs work for the otp (if created in last hour -> pass) to confirm changes

            return self.destroy(request, *args, **kwargs)

        return self.auth_perms_error


class ResendOtp(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    
    def post(self, request, serializer, *args, **kwargs):
        email = serializer.validated_data['email']
        send_otp(email)

class VerifyOtp(generics.GenericAPIView):
    serializer_class = VerifyOtp

    # def check_email_exists_session(self, request, *args, **kwargs):
    #     try:
    #         username = self.request.user.username
    #         user = get_user_model().objects.get(username=username)
    #         return user.email
    #     except Exception:
    #         return Response(
    #             {
    #                 'status': 404,
    #                 'detail': 'Email not found. Please enter your email for verification'
    #             }
    #         )

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = get_user_model().objects.get(email=email)
            if not user.exists():
                return Response(
                    {
                        'status': 404,
                        'detail': "Invalid email"
                    }
                )
            if user.otp!=otp:
                return Response(
                    {
                        'status': 404,
                        'detail': "Invalid OTP"
                    }
            )
            user.is_active = True
            user.save()

        except Exception:
            return Response(
                {
                    'status': 404,
                    "detail": "Action wasn't performed correctly."
                }
            )


class AdminLevelUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by("first_name")
    serializer_class = AdminLevelUserSerializer
    permission_classes = (IsStaff,)
    search_fields = ("username",)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ("username", "email", "first_name",)
