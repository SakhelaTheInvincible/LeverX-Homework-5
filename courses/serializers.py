from rest_framework import serializers
from .models import Course, Lecture


class LectureSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lecture
		fields = ("id", "course", "topic", "presentation", "created_at", "updated_at")
		read_only_fields = ("course",)


class CourseSerializer(serializers.ModelSerializer):
	teachers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = Course
		fields = (
			"id",
			"name",
			"description",
			"owner",
			"teachers",
			"students",
			"created_at",
			"updated_at",
		)
		read_only_fields = ("owner",)

