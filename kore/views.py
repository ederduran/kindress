from django.views.generic import ListView

from kore.models import Feed

class FeedList(ListView):
  model = Feed
  


