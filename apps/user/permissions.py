from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff and request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff and request.method in SAFE_METHODS


def check_user(request, obj):
    # print(request.user)
    return obj.username==request.user.username or request.user.is_staff

class UserPerm(BasePermission):

    def has_permission(self, request, view):
        # if request.user.is_staff or request.user.username:
            # return request.user.is_active and request.method in SAFE_METHODS
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return check_user(request, obj) or request.method in SAFE_METHODS