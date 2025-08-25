from django.urls import path, include
from rest_framework_nested import routers
from .views import CourseViewSet, LectureViewSet
from homework.views import (
	HomeworkAssignmentViewSet,
	HomeworkSubmissionViewSet,
	GradeViewSet,
	GradeCommentViewSet,
)


router = routers.SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")

courses_router = routers.NestedSimpleRouter(router, r"courses", lookup="course")
courses_router.register(r"lectures", LectureViewSet, basename="course-lectures")

lectures_router = routers.NestedSimpleRouter(courses_router, r"lectures", lookup="lecture")
lectures_router.register(r"homework", HomeworkAssignmentViewSet, basename="lecture-homework")

assignments_router = routers.NestedSimpleRouter(lectures_router, r"homework", lookup="assignment")
assignments_router.register(r"submissions", HomeworkSubmissionViewSet, basename="assignment-submissions")
assignments_router.register(r"grades", GradeViewSet, basename="assignment-grades")
grades_router = routers.NestedSimpleRouter(assignments_router, r"grades", lookup="grade")
grades_router.register(r"comments", GradeCommentViewSet, basename="grade-comments")


urlpatterns = [
	path("", include(router.urls)),
	path("", include(courses_router.urls)),
	path("", include(lectures_router.urls)),
	path("", include(assignments_router.urls)),
	path("", include(grades_router.urls)),
]

