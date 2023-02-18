from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allows admin users to modify objects, while allowing all users to retrieve objects.
    """

    def has_object_permission(self, request, view, obj):
        # Allow all users to retrieve objects
        if request.method in SAFE_METHODS:
            return True
        # Only allow admin users to modify objects
        return obj.creator == request.user

    def has_permission(self, request, view):
        if request.method == "GET":
            # apply permission rules for GET requests
            return True
        elif request.method == "POST":
            # apply permission rules for POST requests
            return request.user.is_superuser
        else:
            # other request methods are not allowed
            return False


class IsAdminOrReadOnlyDetails(BasePermission):
    """
    Allows admin users to modify objects, while allowing all users to retrieve objects.
    """

    def has_object_permission(self, request, view, obj):
        # Allow all users to retrieve objects
        if request.method in SAFE_METHODS:
            return True
        # Only allow admin users to modify objects
        return request.user.is_superuser
