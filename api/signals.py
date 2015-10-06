import django.dispatch

news_feed_saved = django.dispatch.Signal(providing_args=["md5_id", ])
