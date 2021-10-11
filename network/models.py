from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.db.models import (
    DateField, DateTimeField, DurationField, Field, Func, IntegerField,
    TimeField, Transform, fields,
)
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=264)
    time_of_creation = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    now = datetime.now()

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "content": self.content,
            "time_of_creation": self.time_of_creation.strftime("%b %d %Y, %I:%M %p")
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=64)
    item_id = models.IntegerField()

    def __str__(self):
        return f"{self.user} commented: {self.comment}"



class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
    #item_id = models.IntegerField()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")
