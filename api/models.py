from django.db import models

from django.utils import timezone


class NewsFeed(models.Model):

    url = models.URLField(max_length=255)
    md5_id = models.CharField(max_length=255)

    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)




class NewsItem(models.Model):

    news_text = models.TextField()

    news_feed = models.ForeignKey(NewsFeed)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
