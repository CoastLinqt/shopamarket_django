from django.db import models

from django.contrib.auth.models import User


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "avatar_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=250, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, unique=True)
    src = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)
    alt = models.CharField(max_length=200, blank=True)
