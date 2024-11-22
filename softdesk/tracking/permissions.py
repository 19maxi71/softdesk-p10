# from rest_framework import permissions

# class IsCreatorOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission pour s'assurer que seuls les Créateurs peuvent modifier leurs objets. 
#     Basé sur la classe BasePermission de Django REST Framework.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read permissions sont autorisées à tout le monde
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Write permissions sont autorisées uniquement si l'utilisateur est le créateur de l'objet
#         return obj.creator == request.user

# class IsContributorOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission pour s'assurer que seuls les Contributeurs peuvent modifier les objets.
#     """

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Check si le user est un contributeur du projet
#         return obj.project.contributors.filter(user=request.user).exists()

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

        # Check if the user is a contributor to the project
        has_permission = obj.project.contributors.filter(user=request.user).exists()
        if not has_permission:
            logger.debug(f"Permission denied for user {request.user} on object {obj}")
        return has_permission