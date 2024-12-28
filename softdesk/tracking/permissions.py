from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to ensure only creators can modify their objects.
    Based on Django REST Framework's BasePermission class.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed if the user is the creator of the object
        has_permission = obj.creator == request.user
        if not has_permission:
            logger.debug(f"Permission denied for user {request.user} on object {obj}")
        return has_permission

class IsContributorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to ensure only contributors can modify objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # # Check if the user is a contributor to the project
        # has_permission = obj.project.contributors.filter(user=request.user).exists()
        # if not has_permission:
        #     logger.debug(f"Permission denied for user {request.user} on object {obj}")
        # return has_permission
        has_permission = Contributor.objects.filter(user=request.user, project=obj.project).exists()
        if not has_permission:
            logger.debug(f"Permission denied for user {request.user} on object {obj}")
        return has_permission