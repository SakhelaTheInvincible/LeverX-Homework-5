from rest_framework import serializers


def validate_role(value: str) -> str:
	if value not in {"teacher", "student"}:
		raise serializers.ValidationError("Role must be 'teacher' or 'student'")
	return value

