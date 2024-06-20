from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow creators of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
           return obj.author.user == request.user     
        return True 