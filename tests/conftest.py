import pytest
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from .factories import TeacherFactory, UserFactory, CourseFactory, LectureFactory


@pytest.fixture
def user(db):
	User = get_user_model()
	return User.objects.create_user(username="tester", password="passw0rd!", role="teacher")


@pytest.fixture(scope="session")
def django_db_setup():
	settings.DATABASES["default"] = {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": ":memory:",
		"ATOMIC_REQUESTS": False,
	}


@pytest.fixture
def api_client(db):
	return APIClient()


@pytest.fixture
def teacher_user(db):
	return TeacherFactory()


@pytest.fixture
def student_user(db):
	return UserFactory(role="student")


@pytest.fixture
def course(db, teacher_user):
	return CourseFactory(owner=teacher_user)


@pytest.fixture
def lecture(db, course):
	return LectureFactory(course=course)


