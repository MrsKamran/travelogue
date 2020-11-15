from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from datetime import datetime

class Posts(models.Model):
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    content = models.TextField(max_length=300)
    date = models.DateField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Reviews(models.Model):
    date = models.DateField('review date')
    content = models.TextField(max_length=300)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    # change the default sort
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for posts_id: {self.posts_id} @{self.url}"




