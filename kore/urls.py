from django.conf.urls.defaults import *

from kore.views import FeedList

urlpatterns = patterns('kindress.kore.views',
  (r'^$', FeedList.as_view()),
)

