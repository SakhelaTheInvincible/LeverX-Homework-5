from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db import models as dj_models
from .models import Course, Lecture
from .serializers import CourseSerializer, LectureSerializer
from .permissions import IsCourseTeacherOrOwner, IsTeacherOrReadOnly
from .services import get_courses_for_user_queryset, user_is_course_teacher_or_owner
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


@extend_schema_view(
	list=extend_schema(tags=["Courses"]),
	retrieve=extend_schema(tags=["Courses"]),
	create=extend_schema(tags=["Courses"]),
	update=extend_schema(tags=["Courses"]),
	partial_update=extend_schema(tags=["Courses"]),
	destroy=extend_schema(tags=["Courses"]),
)
class CourseViewSet(viewsets.ModelViewSet):
	serializer_class = CourseSerializer
	permission_classes = [IsAuthenticated & (IsTeacherOrReadOnly | IsCourseTeacherOrOwner)]
	filterset_fields = ["name"]
	search_fields = ["name", "description"]
	ordering_fields = ["created_at", "updated_at", "name"]
	queryset = Course.objects.none()

	def perform_create(self, serializer):
		course = serializer.save(owner=self.request.user)
		course.teachers.add(self.request.user)

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return Course.objects.none()
		return get_courses_for_user_queryset(self.request.user)

	@extend_schema(tags=["Courses"], parameters=[OpenApiParameter(name="student_id", location=OpenApiParameter.PATH, required=True, type=int)])
	@action(detail=True, methods=["post"], url_path="add-student/(?P<student_id>[^/.]+)")
	def add_student(self, request, pk=None, student_id=None):
		course = self.get_object()
		if not user_is_course_teacher_or_owner(request.user, course):
			return Response({"detail": "Not allowed"}, status=403)
		User = get_user_model()
		try:
			student = User.objects.get(pk=student_id)
		except User.DoesNotExist:
			return Response({"detail": "Student not found"}, status=404)
		course.students.add(student)
		return Response({"detail": "Student added"})

	@extend_schema(tags=["Courses"], parameters=[OpenApiParameter(name="student_id", location=OpenApiParameter.PATH, required=True, type=int)])
	@action(detail=True, methods=["post"], url_path="remove-student/(?P<student_id>[^/.]+)")
	def remove_student(self, request, pk=None, student_id=None):
		course = self.get_object()
		if not user_is_course_teacher_or_owner(request.user, course):
			return Response({"detail": "Not allowed"}, status=403)
		User = get_user_model()
		try:
			student = User.objects.get(pk=student_id)
		except User.DoesNotExist:
			return Response({"detail": "Student not found"}, status=404)
		course.students.remove(student)
		return Response({"detail": "Student removed"})

	@extend_schema(tags=["Courses"], parameters=[OpenApiParameter(name="teacher_id", location=OpenApiParameter.PATH, required=True, type=int)])
	@action(detail=True, methods=["post"], url_path="add-teacher/(?P<teacher_id>[^/.]+)")
	def add_teacher(self, request, pk=None, teacher_id=None):
		course = self.get_object()
		if not user_is_course_teacher_or_owner(request.user, course):
			return Response({"detail": "Not allowed"}, status=403)
		User = get_user_model()
		try:
			teacher = User.objects.get(pk=teacher_id)
		except User.DoesNotExist:
			return Response({"detail": "Teacher not found"}, status=404)
		course.teachers.add(teacher)
		return Response({"detail": "Teacher added"})


@extend_schema_view(
	list=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
	retrieve=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
	create=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
	update=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
	partial_update=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
	destroy=extend_schema(tags=["Lectures"], parameters=[OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int)]),
)
class LectureViewSet(viewsets.ModelViewSet):
	serializer_class = LectureSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ["topic"]
	ordering_fields = ["created_at", "updated_at", "topic"]
	queryset = Lecture.objects.none()

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return Lecture.objects.none()
		course_id = self.kwargs.get("course_pk")
		qs = Lecture.objects.filter(course_id=course_id)
		user = self.request.user
		return qs.filter(
			dj_models.Q(course__owner=user)
			| dj_models.Q(course__teachers=user)
			| dj_models.Q(course__students=user)
		)

	def perform_create(self, serializer):
		course_id = self.kwargs.get("course_pk")
		course = Course.objects.get(id=course_id)
		if not user_is_course_teacher_or_owner(self.request.user, course):
			from rest_framework.exceptions import PermissionDenied
			raise PermissionDenied("Not allowed to create lecture for this course")
		serializer.save(course_id=course_id)
