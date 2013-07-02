from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
  title = models.CharField(max_length=200)
  user = models.ForeignKey(User)
  link = models.URLField(max_length=500, unique=True)
  last_sync = models.DateTimeField()

class FeedItem(models.Model):
  feed = models.ForeignKey(Feed)
  title = models.CharField(max_length=500)
  content = models.TextField()
  header_img = models.ImageField()
  unread = models.BooleanField(default=True)
  
