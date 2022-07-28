from django.db import models
from article.models import Article
# Create your models here.

class Article_tag(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    article_tag = models.CharField(max_length=10)