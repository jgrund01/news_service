from api.models import NewsFeed

for news_feed in NewsFeed.objects.all():
    news_feed.retrieve_and_store_news_items()
