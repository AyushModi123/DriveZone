from rest_framework.permissions import BasePermission, IsAuthenticated

class IsActivePermission(BasePermission):
    """
    Allows access only to active users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
    
class IsNotAuthenticated(IsAuthenticated):
    """
    Allow access only to non authenticated users.
    """
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return False
        return True
    
class IsSchoolPermission(IsAuthenticated):
    """
    Allows access only to  authenticated, active schools.
    """
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_school
        return False

class IsLearnerPermission(IsAuthenticated):
    """
    Allows access only to  authenticated, active learner.
    """
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_learner
        return False
    
class BlockInstructorPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return not request.user.is_instructor
        return False

class BlockSchoolPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return not request.user.is_school
        return False
    
class BlockLearnerPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return not request.user.is_learner
        return False

class RequiredProfileCompletionPermission(IsAuthenticated):
    """
    Allows access only to authenticated, active users with the required profile completion level.
    """
    def __init__(self, required_level):
        self.required_level = required_level
    
    def __call__(self):
        """
        This method is necessary so that arguments can be passed in permission.
        """
        return self
    
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            user_completion_level = request.user.profile_completion_level
            return user_completion_level >= self.required_level
        return False
