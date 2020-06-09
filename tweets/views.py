import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .forms import TweetForm
from .models import Tweet


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content,
                    "likes": random.randint(0, 100)} for x in qs]

    data = {
        "isUser": False,
        "response": tweets_list
    }

    return JsonResponse(data)


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_view(request, tweet_id):
    """
    REST API VIEW
    Consume by js
    return json data
    """
    status = 200

    data = {
        "id": tweet_id
    }

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content

    except Tweet.DoesNotExist:
        status = 404
        data['message'] = "Not Found"

    return JsonResponse(data, status=status)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()

    return render(request, 'components/form.html', context={"form":form})
