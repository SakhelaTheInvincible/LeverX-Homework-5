from django.db import models
from django.conf import settings


class Course(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_courses")
	teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teaching_courses", blank=True)
	students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="enrolled_courses", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return self.name


class Lecture(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lectures")
	topic = models.CharField(max_length=255)
	presentation = models.FileField(upload_to="presentations/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["course", "created_at"]

	def __str__(self) -> str:
		return f"{self.course.name} - {self.topic}"

