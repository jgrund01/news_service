from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import NewsFeed, NewsItem
from api.Serializers import GetNewsFeedSerializer, PostNewsFeedSerializer, NewsItemSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def news_feed_list(request):
    if request.method == 'GET':
        news_feeds = NewsFeed.objects.all()
        serializer = GetNewsFeedSerializer(news_feeds, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostNewsFeedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def news_item_list(request, md5_feed_id):
    if request.method == 'GET':

        news_items = NewsItem.objects.filter(newsfeed__md5_id__contains=md5_feed_id)
        serializer = NewsItemSerializer(news_items, many=True)
        return JSONResponse(serializer.data)

