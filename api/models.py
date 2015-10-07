from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from signals import news_feed_saved
from django.forms.models import model_to_dict

import feedparser
import hashlib
import requests

CHARACTER_LENGTH_LIMIT = 255


class NewsFeed(models.Model):
    url = models.URLField(max_length=CHARACTER_LENGTH_LIMIT)
    md5_id = models.CharField(max_length=CHARACTER_LENGTH_LIMIT)
    last_cron_run = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.md5_id = self.get_md5_key()
        news_feed_saved.send(sender=self.__class__, md5_id=self.md5_id)
        super(NewsFeed, self).save(*args, **kwargs)

    def retrieve_and_store_news_items(self):
        feed = feedparser.parse(self.url)

        news_feed_updated = False
        for i in range(0, len(feed['entries'])):
            if not news_item_exists(feed['entries'][i].link):
                news_feed_updated = True
                news_item = NewsItem()
                news_item.title = feed['entries'][i].title
                news_item.url = feed['entries'][i].link
                news_item.news_feed = self
                news_item.save()

        if news_feed_updated:
            news_feed_saved.send(sender=self.__class__, md5_id=self.md5_id)

    def get_md5_key(self):
        return hashlib.sha224(self.url).hexdigest()


class NewsItem(models.Model):
    title = models.CharField(max_length=CHARACTER_LENGTH_LIMIT)
    url = models.URLField(max_length=CHARACTER_LENGTH_LIMIT)

    news_feed = models.ForeignKey(NewsFeed)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)


@receiver(news_feed_saved, dispatch_uid="news_feed_saved")
# should this be run by cron or each time a feed is updated?
def notify_channel_of_update(**kwargs):
    requests.post("http://127.0.0.1:8080/notify",
                  json={
                      'topic': kwargs['md5_id'],
                      # 'topic': '15c8b4f3d878845c7066f483426049a0308df7fa1f6dca88f9d23e36',
                      'args': [1]
                  })


def news_item_exists(url):
    if len(NewsItem.objects.filter(url=url)) == 0:
        return False
    return True
