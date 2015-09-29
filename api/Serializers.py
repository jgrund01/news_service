from rest_framework import serializers
from api.models import NewsFeed, NewsItem


class NewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = ('url', 'md5_id')


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ('title', 'description', 'url')
