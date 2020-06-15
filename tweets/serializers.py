# django
from django.conf import settings
# internal
from .models import Tweet
# third party
from rest_framework import serializers


# ======================
#    Local Variables
# ======================

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

# ======================
#    Serializers
# ======================


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
