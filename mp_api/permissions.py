from rest_framework import permissions


class IsEditorOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow editors
    """

    def has_permission(self, request, view):
        if request.user.profile.is_editor:  # Check if user is an editor
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are granted to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile
        return obj.owner == request.user


class IsReviewer(permissions.BasePermission):
    """
    Custom permission to allow only reviewers to view and edit their reviews.
    """

    def has_permission(self, request, view):
        return request.user.profile.is_reviewer  # Only reviewers can pass
