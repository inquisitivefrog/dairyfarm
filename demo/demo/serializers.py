from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 12:
            raise serializers.ValidationError(
                'Password must be at least 12 characters long.')
        try:
            validate_password(value)
        except ValidationError as error:
            raise serializers.ValidationError(list(error.messages))
        return value

    def create(self, validated_data):
        user = User(email=validated_data["email"],
                    username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
