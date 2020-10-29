from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="poseidon.jpg", upload_to="profile_pics")
    follows = models.ManyToManyField(User, related_name="+")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.username}'s Comment"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Like"


# def save(self, *args, **kwargs):
#     super(Profile, self).save(*args, **kwargs)
