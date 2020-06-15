# python
import random
# django
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
# internal
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer
# third party
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated


# ======================
#    Local Variables
# ======================
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# ====================
#    Tweets Views
# ====================


def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse({}, status=400)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, satus=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


# ==============================
#      Pure Django
# ==============================
'''
    These views were made in pure django as an exercise and redone using 
    Django Rest Framework above.
'''


def tweet_create_view_pure_django(request, *args, **kwargs):
    '''
    Create REST API Create View using Django Rest Framework
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user or None
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    if form.errors:
        if request.is_ajax:
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    """
        REST API VIEW
        Consume by Javascript or Swift or Java/IOS/Android
        Return JSON data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, * args, **kwargs):
    """
        REST API VIEW
        Consume by Javascript or Swift or Java/IOS/Android
        Return JSON data
    """
    data = {
        "id": tweet_id,
        # "image_path": obj.image.url
    }
    status = 200

    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)
