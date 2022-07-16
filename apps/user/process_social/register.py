
from django.contrib.auth import authenticate
from apps.user.process_social.gen_password import generate_password
from apps.user.process_social.serializers import FacebookSocialAuthSerializer, GoogleSocialAuthSerializer, TwitterAuthSerializer
from authentication.models import User
import random
from rest_framework.exceptions import AuthenticationFailed
from dj_rest_auth.views import LoginView

import os
from dj_rest_auth.registration.views import SocialLoginView


# class CustomLogin(LoginView):

#     def post(self, request):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data['email']
#         username = self.request.username
#         user = User.objects.filter(username=username)
#         self.serializer.is_valid(raise_exception=True)

#         if user.auth_provider=="facebook":
#             self.serializer_class = FacebookSocialAuthSerializer
#         elif user.auth_provider=="twitter":
#             self.serializer_class = TwitterAuthSerializer
#         else:
#             self.serializer_class = GoogleSocialAuthSerializer

# log = CustomLogin()

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    random_username = username + str(random.randint(0, 1000))
    return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider != filtered_user_by_email[0].auth_provider:

            raise AuthenticationFailed(
                detail=f'Please continue your login using {filtered_user_by_email[0].auth_provider}'
            )

    else:
        gen_pass = generate_password()
        user = {
            'username': generate_username(name),
            'email': email,
            'password': gen_pass
        }

        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        return user

    user = User.objects.get(email=email)

    return user
