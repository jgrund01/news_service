from api.models import NewsFeed


for news_feed in NewsFeed.objects.all():
    news_feed.get_news_items()
