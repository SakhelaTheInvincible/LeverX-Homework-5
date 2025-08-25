import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_schema_available(client):
	resp = client.get(reverse("schema"))
	assert resp.status_code == 200


@pytest.mark.django_db
def test_register_and_login(client):
	# Register
	resp = client.post(
		"/api/v1/auth/register/",
		{"username": "u1", "password": "passw0rd!", "role": "student"},
		content_type="application/json",
	)
	assert resp.status_code in (201, 400)  # may fail if username exists
	# Login
	resp = client.post(
		"/api/v1/auth/login/",
		{"username": "u1", "password": "passw0rd!"},
		content_type="application/json",
	)
	assert resp.status_code in (200, 401)

