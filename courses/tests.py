import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_teacher_creates_course_and_adds_student(teacher_user, student_user):
	client = APIClient()
	client.force_authenticate(user=teacher_user)
	# create course
	resp = client.post("/api/v1/courses/", {"name": "C1", "description": "D"}, format="json")
	assert resp.status_code == 201
	course_id = resp.data["id"]
	# add student
	resp = client.post(f"/api/v1/courses/{course_id}/add-student/{student_user.id}/")
	assert resp.status_code == 200


@pytest.mark.django_db
def test_student_sees_own_courses(course, student_user):
	course.students.add(student_user)
	client = APIClient()
	client.force_authenticate(user=student_user)
	resp = client.get("/api/v1/courses/")
	assert resp.status_code == 200
	ids = [c["id"] for c in resp.data.get("results", [])] if isinstance(resp.data, dict) else [c["id"] for c in resp.data]
	assert course.id in ids
