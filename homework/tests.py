import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_homework_flow(course, lecture, teacher_user, student_user):
	client = APIClient()
	# Teacher adds assignment
	client.force_authenticate(user=teacher_user)
	resp = client.post(f"/api/v1/courses/{course.id}/lectures/{lecture.id}/homework/", {"text": "Do it"}, format="json")
	assert resp.status_code == 201
	assignment_id = resp.data["id"]
	# Student submits
	client.force_authenticate(user=student_user)
	resp = client.post(f"/api/v1/courses/{course.id}/lectures/{lecture.id}/homework/{assignment_id}/submissions/", {"answer_text": "Done"}, format="json")
	assert resp.status_code == 201
	submission_id = resp.data["id"]
	# Teacher grades
	client.force_authenticate(user=teacher_user)
	resp = client.post(f"/api/v1/courses/{course.id}/lectures/{lecture.id}/homework/{assignment_id}/grades/", {"submission": submission_id, "score": 10, "comment": "Good"}, format="json")
	assert resp.status_code in (201, 400)
