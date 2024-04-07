from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from projects.models import ExamResult

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class ProjectDetailPerms(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Everyone can use the safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Special case if method is POST - we need to allow non-owners, as long as the project is open and they have a good enough exam result.
        if request.method == "POST":
            if not obj.is_open:
                raise PermissionDenied(f"This class no longer requires tutors.")
            
            relevant_results = ExamResult.objects.filter(
                examinee=request.user, 
                exam=obj.tutor_for
            )
            if not any([result.score>=obj.required_grade for result in relevant_results]):
                raise PermissionDenied(f"You need to pass this exam with a grade of at least {obj.required_grade} in order to tutor for it.")

            return True
        
        # For all other unsafe methods, you need to be the owner
        return obj.created_by == request.user
    
class IsPledgerOrPledgeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.pledged_by == request.user) or (obj.pledged_to.created_by == request.user)