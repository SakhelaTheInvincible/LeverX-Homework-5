from django.contrib import admin
from .models import Course, Lecture


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner", "created_at")
	search_fields = ("name",)
	list_filter = ("created_at",)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
	list_display = ("id", "course", "topic", "created_at")
	search_fields = ("topic",)
	list_filter = ("course",)
