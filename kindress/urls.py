from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^accounts/', include('userena.urls')),
  url(r'^feeds/', include('kindress.kore.urls')),

  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
