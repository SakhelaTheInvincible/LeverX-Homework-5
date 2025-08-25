from rest_framework import serializers
from .models import HomeworkAssignment, HomeworkSubmission, Grade, GradeComment


class HomeworkAssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = HomeworkAssignment
		fields = ("id", "lecture", "text", "created_at", "updated_at")


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = HomeworkSubmission
		fields = ("id", "assignment", "student", "answer_text", "created_at", "updated_at")
		read_only_fields = ("student",)


class GradeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Grade
		fields = ("id", "submission", "graded_by", "score", "comment", "created_at", "updated_at")
		read_only_fields = ("graded_by",)


class GradeCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = GradeComment
		fields = ("id", "grade", "author", "text", "created_at", "updated_at")
		read_only_fields = ("author",)

