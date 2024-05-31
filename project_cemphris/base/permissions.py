from rest_framework.permissions import BasePermission, IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

class IsActivePermission(BasePermission):
    """
    Allows access only to active users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
    
class IsInstructorPermission(IsAuthenticated, IsActivePermission):
    """
    Allows access only to  authenticated, active instructors.
    """
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            try:
                return bool( request.user.instructor)                
            except ObjectDoesNotExist:
                return False
    
class IsLearnerPermission(IsAuthenticated, IsActivePermission):
    """
    Allows access only to  authenticated, active learner.
    """
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            try:
                return bool(request.user.learner)                
            except ObjectDoesNotExist:
                return False