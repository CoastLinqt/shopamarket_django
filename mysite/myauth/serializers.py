from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250, required=True)
    username = serializers.CharField(max_length=250, required=True)

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "name", "email")

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        Profile.objects.create(
            user=user, fullName=validated_data["name"], email=validated_data["email"]
        )

        return user


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250, required=True)

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password")


class ProfileImagesSerializer(serializers.ModelSerializer):
    alt = serializers.CharField(max_length=200)
    src = serializers.ImageField

    class Meta:
        model = Profile
        fields = ("alt", "src")


class ProfileEditSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(max_length=250, required=True)
    phone = serializers.CharField(max_length=20, required=True)
    email = serializers.CharField(max_length=250, required=True)
    src = serializers.ImageField
    alt = serializers.CharField

    class Meta:
        model = Profile
        fields = ("fullName", "phone", "email", "src", "alt")

    def update(self, instance: Profile, validated_data):
        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.src = validated_data.get("src", instance.src)
        instance.alt = validated_data.get("alt", instance.alt)
        instance.save()
        return instance
