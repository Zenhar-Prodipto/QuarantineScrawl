from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="poseidon.jpg", upload_to="profile_pics")
    follow = models.ManyToManyField(User, related_name="followers", blank=True)
    follower = models.ManyToManyField(User, related_name="follows", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user_comment = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s Comment"


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.user.username}'s Like"


# class FollowModel(models.Model):
#     user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
#     follows = models.ForeignKey(
#         User, default=None, related_name="followers", on_delete=models.CASCADE
#     )
#     followers = models.ForeignKey(
#         User, default=None, related_name="follows", on_delete=models.CASCADE
#     )

#     # followers = models.ManyToManyField(User, related_name="follows")

#     def __str__(self):
#         return "follows:{}, followed by:{}".format(self.followers, self.follows)


# def save(self, *args, **kwargs):
#     super(Profile, self).save(*args, **kwargs)
