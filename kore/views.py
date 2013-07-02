from django.views.generic import ListView

from kore.models import Feed, FeedItem

class FeedList(ListView):
  context_object_name = 'feed_list'
  queryset = Feed.objects.all()

class FeedItemList(ListView):
  model = FeedItem
  context_object_name = 'item_list'

