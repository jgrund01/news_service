from rest_framework import serializers
from api.models import NewsFeed, NewsItem


class GetNewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = ('url', 'md5_id')


class PostNewsFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = ('url',)


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ('title', 'description', 'url')
