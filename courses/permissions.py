from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		user = request.user
		return bool(user and user.is_authenticated and getattr(user, "is_teacher", lambda: False)())


class IsCourseTeacherOrOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		if request.method in SAFE_METHODS:
			return True
		course = getattr(obj, "course", obj)
		owner_id = getattr(course, "owner_id", None)
		teachers = getattr(course, "teachers", None)
		return (owner_id == user.id) or (hasattr(teachers, "filter") and teachers.filter(id=user.id).exists())


class IsCourseMemberOrTeacher(BasePermission):
	def has_permission(self, request, view):
		user = request.user
		if not user or not user.is_authenticated:
			return False
		course = getattr(getattr(view, 'kwargs', {}), 'get', lambda *_: None)('course_pk')
		if course is None:
			return True
		return True

