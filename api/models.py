from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
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
        super(NewsFeed, self).save(*args, **kwargs)

    def get_news_items(self):
        feed = feedparser.parse(self.url)

        for i in range(0, len(feed['entries'])):
            news_item = NewsItem()
            news_item.title = feed['entries'][i].title
            news_item.url = feed['entries'][i].link
            news_item.news_feed = self
            news_item.save()

    def get_md5_key(self):
        return hashlib.sha224(self.url).hexdigest()


class NewsItem(models.Model):
    title = models.CharField(max_length=CHARACTER_LENGTH_LIMIT)
    url = models.URLField(max_length=CHARACTER_LENGTH_LIMIT)

    news_feed = models.ForeignKey(NewsFeed)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)


# @receiver(post_save, sender=NewsFeed, dispatch_uid="server_post_save")
# def notify_server_config_changed(sender, instance, **kwargs):
#     """ Notifies a client that a news feed has been updated.
#
#         This function is executed when we save a NewsFeed model, and it
#         makes a POST request on the WAMP-HTTP bridge, allowing us to
#         make a WAMP publication from Django.
#     """
#     requests.post("http://127.0.0.1:8080/notify",
#                   json={
#                       'topic': 'clientconfig.' + instance.ip,
#                       'args': [model_to_dict(instance)]
#                   })
