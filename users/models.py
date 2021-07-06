from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from PIL import Image
from django.core.files.storage import default_storage as storage

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="poseidon.jpg", upload_to="profile_pics")
    follow = models.ManyToManyField(User, related_name="followers", blank=True)
    follower = models.ManyToManyField(User, related_name="follows", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
