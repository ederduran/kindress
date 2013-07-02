from django.db import models
from django.contrib.auth.models import User

from kore.helper import uploadFeedHeaderTo

class FeedBook(models.Model):
  title = models.CharField(max_length=200)
  user = models.OneToOneField(User)

  def __unicode__(self):
    return self.title

class Feed(models.Model):
  title = models.CharField(max_length=200)
  user = models.ForeignKey(User)
  link = models.URLField(max_length=500, unique=True)
  feed_book = models.ForeignKey(FeedBook, null=True, blank=True)
  last_sync = models.DateTimeField()

  def __unicode__(self):
    return self.title

class FeedItem(models.Model):
  feed = models.ForeignKey(Feed)
  title = models.CharField(max_length=500)
  content = models.TextField()
  header_img = models.ImageField(upload_to=uploadFeedHeaderTo)
  unread = models.BooleanField(default=True)

  def __unicode__(self):
    return self.title

