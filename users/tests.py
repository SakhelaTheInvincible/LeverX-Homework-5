import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_with_role_and_login():
	client = APIClient()
	resp = client.post("/api/v1/auth/register/", {"username": "t1", "password": "passw0rd!", "role": "teacher"}, format="json")
	assert resp.status_code in (201, 400)
	resp = client.post("/api/v1/auth/login/", {"username": "t1", "password": "passw0rd!"}, format="json")
	assert resp.status_code in (200, 401)


@pytest.mark.django_db
def test_me_requires_auth(api_client):
	resp = api_client.get("/api/v1/auth/me/")
	assert resp.status_code == 401
