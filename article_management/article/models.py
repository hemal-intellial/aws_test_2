from turtle import title
from django.db import models
from tag.models import Tag
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Article(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    draft = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now())