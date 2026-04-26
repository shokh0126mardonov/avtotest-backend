from rest_framework.permissions import BasePermission

from .models import User, RoleChoice


class AdminPermissions(BasePermission):
    message = "siz bu methoddan foydalana olmaysin"

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.ADMIN


class StudentPermissions(BasePermission):
    message = "siz bu methoddan foydalana olmaysin"

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.STUDENT


class InstructorPermissions(BasePermission):
    message = "siz bu methoddan foydalana olmaysin"

    def has_permission(self, request, view):
        return request.user.role == RoleChoice.INSTRUCTOR
