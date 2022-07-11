from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics



# class LoggedIn:

#     def logged_in(self, request):
#         if self.request.user.is_authenticated:
#             True
            
# class SessionExistsEmail:

#     def session_exists_email(self, request, *args, **kwargs):
#         try:
#             username = self.request.user.username
#             user = get_user_model().objects.get(username=username)
#             return user.email
#         except Exception:
#             return Response(
#                 {
#                     'status': 404,
#                     'detail': 'Email not found. Please enter your email for verification'
#                 }
#             )

class CompleteCRUDUser(generics.RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):

        if self.wrap_perms(self, request, *args):

                return self.retrieve(request, *args, **kwargs)
        
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


class OTPVerification(generics.GenericAPIView):

    
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
