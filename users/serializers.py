from django.contrib.auth import get_user_model
from rest_framework import serializers
from .validators import validate_role


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)
	role = serializers.CharField(validators=[validate_role])

	class Meta:
		model = User
		fields = ("id", "username", "email", "password", "first_name", "last_name", "role")


	def create(self, validated_data):
		password = validated_data.pop("password")
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user

	def validate_username(self, value: str) -> str:
		if " " in value:
			raise serializers.ValidationError("Username must not contain spaces")
		return value


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "username", "email", "first_name", "last_name", "role")

