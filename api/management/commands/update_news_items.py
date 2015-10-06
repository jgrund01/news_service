from django.core.management.base import BaseCommand
from api.models import NewsFeed


class Command(BaseCommand):
    def handle(self, *args, **options):
        for news_feed in NewsFeed.objects.all():
            news_feed.retrieve_and_store_news_items()
