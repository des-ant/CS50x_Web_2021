from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="posts_liked")
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [self.likes.all().count()]
        }


class UserFollowing(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name="unique_followers")
        ]

        ordering = ["-created"]

    def serialize(self):
        return {
            "id": self.id,
            "follower": self.follower.username,
            "followed": self.followed.username
        }