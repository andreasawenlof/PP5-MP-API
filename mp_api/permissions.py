from rest_framework import permissions


class IsComposerOrOwner(permissions.BasePermission):
    """
    Composers have full access, owners can edit their own objects.
    """

    def has_permission(self, request, view):
        return request.user.profile.is_composer  # ✅ Full access for composers

    def has_object_permission(self, request, view, obj):
        # ✅ Owners can modify their own objects
        return request.user.profile.is_composer or obj.owner == request.user


class IsComposerOrReviewer(permissions.BasePermission):
    """
    Custom permission: Grants access to composers OR reviewers.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            (user.profile.is_composer or user.profile.is_reviewer)
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow the owner of a profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # ✅ Read permissions granted to everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # ✅ Only the owner can modify
        return obj.owner == request.user


class IsReviewer(permissions.BasePermission):
    """
    Reviewers can only access "Ready for Review" tracks.
    Once they submit feedback, they **cannot** edit or delete it.
    """

    def has_permission(self, request, view):
        return request.user.profile.is_reviewer  # ✅ Only reviewers can pass

    def has_object_permission(self, request, view, obj):
        # ✅ Reviewers can see only tracks marked as "Ready for Review"
        if hasattr(obj, 'status') and obj.status == "ready_for_review":
            return True

        # ❌ Reviews cannot be edited or deleted after submission
        if hasattr(obj, "reviewed_at"):
            return request.method in permissions.SAFE_METHODS  # Read-only

        return False  # Deny everything else
