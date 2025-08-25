from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import HomeworkAssignment, HomeworkSubmission, Grade, GradeComment
from .serializers import (
	HomeworkAssignmentSerializer,
	HomeworkSubmissionSerializer,
	GradeSerializer,
	GradeCommentSerializer,
)
from courses.models import Course, Lecture
from courses.services import user_is_course_teacher_or_owner
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


# Students can read; teachers create/update
@extend_schema_view(
	list=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	retrieve=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	create=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	update=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	partial_update=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	destroy=extend_schema(tags=["Homework"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
)
class HomeworkAssignmentViewSet(viewsets.ModelViewSet):
	serializer_class = HomeworkAssignmentSerializer
	permission_classes = [IsAuthenticated]
	filterset_fields = ["lecture"]
	queryset = HomeworkAssignment.objects.none()

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return HomeworkAssignment.objects.none()
		qs = HomeworkAssignment.objects.filter(lecture__course_id=self.kwargs.get("course_pk"))
		user = self.request.user
		return qs.filter(
			Q(lecture__course__owner=user)
			| Q(lecture__course__teachers=user)
			| Q(lecture__course__students=user)
		)

	def perform_create(self, serializer):
		lecture_id = self.kwargs.get("lecture_pk")
		lecture = Lecture.objects.get(id=lecture_id)
		if not user_is_course_teacher_or_owner(self.request.user, lecture.course):
			raise PermissionDenied("Only course teachers can add homework assignments")
		serializer.save(lecture_id=lecture_id)


@extend_schema_view(
	list=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	retrieve=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	create=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	update=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	partial_update=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	destroy=extend_schema(tags=["Submissions"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
)
class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
	serializer_class = HomeworkSubmissionSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ["answer_text"]
	queryset = HomeworkSubmission.objects.none()

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return HomeworkSubmission.objects.none()
		qs = HomeworkSubmission.objects.filter(assignment_id=self.kwargs.get("assignment_pk"))
		user = self.request.user
		return qs.filter(Q(student=user) | Q(assignment__lecture__course__teachers=user) | Q(assignment__lecture__course__owner=user))

	def perform_create(self, serializer):
		assignment_id = self.kwargs.get("assignment_pk")
		assignment = HomeworkAssignment.objects.select_related("lecture__course").get(id=assignment_id)
		course = assignment.lecture.course
		user = self.request.user
		is_member = (
			course.owner_id == user.id
			or course.teachers.filter(id=user.id).exists()
			or course.students.filter(id=user.id).exists()
		)
		if not is_member:
			raise PermissionDenied("You are not a member of this course")
		serializer.save(student=user, assignment_id=assignment_id)


@extend_schema_view(
	list=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	retrieve=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	create=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	update=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	partial_update=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	destroy=extend_schema(tags=["Grades"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
)
class GradeViewSet(viewsets.ModelViewSet):
	serializer_class = GradeSerializer
	permission_classes = [IsAuthenticated]
	queryset = Grade.objects.none()

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return Grade.objects.none()
		qs = Grade.objects.filter(submission__assignment_id=self.kwargs.get("assignment_pk"))
		user = self.request.user
		return qs.filter(
			Q(submission__student=user)
			| Q(submission__assignment__lecture__course__teachers=user)
			| Q(submission__assignment__lecture__course__owner=user)
		)

	def perform_create(self, serializer):
		submission = serializer.validated_data.get("submission")
		course = submission.assignment.lecture.course if submission else None
		if not course or not user_is_course_teacher_or_owner(self.request.user, course):
			raise PermissionDenied("Only teachers can grade submissions")
		serializer.save(graded_by=self.request.user)


@extend_schema_view(
	list=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	retrieve=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	create=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	update=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	partial_update=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
	destroy=extend_schema(tags=["Grade Comments"], parameters=[
		OpenApiParameter(name="course_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="lecture_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="assignment_pk", location=OpenApiParameter.PATH, required=True, type=int),
		OpenApiParameter(name="grade_pk", location=OpenApiParameter.PATH, required=True, type=int),
	]),
)
class GradeCommentViewSet(viewsets.ModelViewSet):
	serializer_class = GradeCommentSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ["text"]
	queryset = GradeComment.objects.none()

	def get_queryset(self):
		if getattr(self, "swagger_fake_view", False):
			return GradeComment.objects.none()
		qs = GradeComment.objects.filter(grade_id=self.kwargs.get("grade_pk"))
		user = self.request.user
		return qs.filter(
			Q(grade__submission__student=user)
			| Q(grade__submission__assignment__lecture__course__teachers=user)
			| Q(grade__submission__assignment__lecture__course__owner=user)
		)

	def perform_create(self, serializer):
		grade_id = self.kwargs.get("grade_pk")
		grade = Grade.objects.select_related("submission__assignment__lecture__course").get(id=grade_id)
		course = grade.submission.assignment.lecture.course
		user = self.request.user
		is_member = (
			course.owner_id == user.id
			or course.teachers.filter(id=user.id).exists()
			or grade.submission.student_id == user.id
		)
		if not is_member:
			raise PermissionDenied("Not allowed to comment on this grade")
		serializer.save(author=user, grade_id=grade_id)
