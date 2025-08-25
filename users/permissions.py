from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return bool(user and user.is_authenticated and getattr(user, "is_teacher", lambda: False)())


class IsStudent(BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return bool(user and user.is_authenticated and getattr(user, "is_student", lambda: False)())

