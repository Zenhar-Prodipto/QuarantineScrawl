from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, related_name="liked", default=None, blank=True)
    commented = models.ManyToManyField(
        User, related_name="commented", default=None, blank=True
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    @property
    def total_likes(self):
        return self.liked.all().count()

    @property
    def top_likes(self):
        # sorted(zip(score, name), reverse=True)[:3]
        top_like_list = []
        top_like_list.append(self.liked.all().count())
        return sorted(top_like_list, reverse=True)[:3]

    @property
    def total_comments(self):
        return Comment.objects.filter(post=self.pk).all().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Like"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.TextField(default=None, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Comment"
