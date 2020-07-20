from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10000,default='')
    image = models.ImageField()
    caption = models.CharField(max_length=100000, default='')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username + '-' + str(self.pk)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=10000, default='')
    comment = models.CharField(max_length=100000, default='')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment + '-' + self.user.username
