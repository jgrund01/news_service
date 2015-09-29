from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^news_feed/$', views.news_feed_list),
    url(r'^news_feed/(?P<md5_feed_id>.*)/$', views.news_item_list)
]
