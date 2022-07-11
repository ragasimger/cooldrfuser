from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff and request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.method in SAFE_METHODS


def check_user(request, obj):
    # print(request.user)
    return obj.username==request.user.username or request.user.is_staff

class CustomNotAllowed(BasePermission):

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

class UserPerformActionPermission:

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
        else:
            self.permission_classes=[CustomNotAllowed,]
