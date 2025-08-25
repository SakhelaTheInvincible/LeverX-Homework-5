from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	class Roles(models.TextChoices):
		TEACHER = "teacher", "Teacher"
		STUDENT = "student", "Student"

	role = models.CharField(max_length=20, choices=Roles.choices)

	def is_teacher(self) -> bool:
		return self.role == self.Roles.TEACHER

	def is_student(self) -> bool:
		return self.role == self.Roles.STUDENT
