from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id')
        return request.user.is_superuser or Subscription.objects.filter(user=request.user, course=course_id).exists()

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
