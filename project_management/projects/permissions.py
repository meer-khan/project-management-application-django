from rest_framework import permissions
from .models import ProjectMember

class IsProjectOwner(permissions.BasePermission):
    """Only project owners can manage user roles and delete projects."""
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsProjectEditor(permissions.BasePermission):
    """Editors can edit project details but not delete or manage roles."""

    def has_object_permission(self, request, view, obj):
        try:
            member = ProjectMember.objects.get(user=request.user, project=obj)
            return member.role in ['owner', 'editor']
        except ProjectMember.DoesNotExist:
            return False

class IsProjectReader(permissions.BasePermission):
    """Readers can only view the project but not modify it."""

    def has_object_permission(self, request, view, obj):
        try:
            member = ProjectMember.objects.get(user=request.user, project=obj)
            return member.role in ['owner', 'editor', 'reader']
        except ProjectMember.DoesNotExist:
            return False
