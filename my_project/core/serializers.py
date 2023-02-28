from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def is_valid(self, raise_exception=False):
        """Get password_repeat and remove from initial data"""
        self._password_repeat = self.initial_data.pop('password_repeat')
        return super().is_valid(raise_exception=raise_exception)

    def validate_email(self, value):
        """Ensure email doesn't exist"""
        if self.Meta.model.objects.filter(email=value).exists():
            raise serializers.ValidationError(['User with such email already exists'])
        return value

    def validate_password(self, value):
        """Ensure password is valid"""
        validate_password(value)
        return value

    def validate(self, data):
        """Ensure passwords match"""
        if data.get('password') != self._password_repeat:
            raise serializers.ValidationError({'password_repeat': ['Passwords must match']})
        return data

    def create(self, validated_data):
        """Create user"""
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        """Ensure email exists"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(["User with such email doesn't exist"])
        return value


# class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(required=False, max_length=50)
#     first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
#     last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
#     email = serializers.EmailField(required=False, allow_blank=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']
#
#
# class PasswordUpdateSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#
#     def validate_new_password(self, value):
#         validate_password(value)
#         return value