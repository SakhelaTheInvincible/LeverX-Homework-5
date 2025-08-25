from django.contrib import admin
from .models import HomeworkAssignment, HomeworkSubmission, Grade


@admin.register(HomeworkAssignment)
class HomeworkAssignmentAdmin(admin.ModelAdmin):
	list_display = ("id", "lecture", "created_at")
	list_filter = ("lecture",)


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
	list_display = ("id", "assignment", "student", "created_at")
	list_filter = ("assignment", "student")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = ("id", "submission", "graded_by", "score", "created_at")
	list_filter = ("graded_by", "score")
