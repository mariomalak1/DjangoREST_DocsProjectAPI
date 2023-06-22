from rest_framework import permissions

class IsOwnerOfSnippetOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # return true if request is HEAD, OPTIONS, GET
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # Write permissions are only allowed to the owner of the snippet.
            return obj.owner == request.user

class IsSameUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return (request.user == obj)