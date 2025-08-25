from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.models import Course


class IsTeacherForCourse(BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		if request.method in SAFE_METHODS:
			return True
		lecture = getattr(obj, "lecture", None)
		if lecture is None and hasattr(obj, "assignment"):
			lecture = obj.assignment.lecture
		course = lecture.course if lecture else None
		if not course:
			return False
		return course.owner_id == user.id or course.teachers.filter(id=user.id).exists()


class IsStudentSelf(BasePermission):
	def has_object_permission(self, request, view, obj):
		user = request.user
		if request.method in SAFE_METHODS:
			return True
		if hasattr(obj, "student_id"):
			return obj.student_id == user.id
		return False

