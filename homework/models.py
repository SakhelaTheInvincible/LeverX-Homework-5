from django.db import models
from django.conf import settings
from courses.models import Lecture


class HomeworkAssignment(models.Model):
	lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name="homework_assignment")
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Homework for {self.lecture}"


class HomeworkSubmission(models.Model):
	assignment = models.ForeignKey(HomeworkAssignment, on_delete=models.CASCADE, related_name="submissions")
	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="homework_submissions")
	answer_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("assignment", "student")

	def __str__(self) -> str:
		return f"{self.student} - {self.assignment}"


class Grade(models.Model):
	submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name="grade")
	graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="given_grades")
	score = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Grade {self.score} for {self.submission}"


class GradeComment(models.Model):
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="comments")
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="grade_comments")
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
