from django.contrib.auth import get_user_model
from django.db.models import Q, Prefetch
from .models import Course


def user_is_course_teacher_or_owner(user, course: Course) -> bool:
	if not user or not user.is_authenticated:
		return False
	return (course.owner_id == user.id) or course.teachers.filter(id=user.id).exists()


def user_is_course_member(user, course: Course) -> bool:
	if not user or not user.is_authenticated:
		return False
	if user_is_course_teacher_or_owner(user, course):
		return True
	return course.students.filter(id=user.id).exists()


def get_courses_for_user_queryset(user):
	qs = Course.objects.all().select_related("owner").prefetch_related("teachers", "students")
	if not user or not user.is_authenticated:
		return qs.none()
	if getattr(user, "is_teacher", lambda: False)():
		return qs.filter(Q(owner=user) | Q(teachers=user))
	return qs.filter(Q(students=user) | Q(teachers=user) | Q(owner=user))


