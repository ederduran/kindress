from django.db import models
from django.contrib.auth.models import User

class Url(models.Model):
  link = models.URLField(max_length=255, unique=True)

class Feed(models.Model):
  title = models.CharField(max_length=200)
  user = models.ForeignKey(User)
  url = models.ForeignKey(Url)

