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
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

# ======================
#    Serializers
# ======================


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError(
                "This is not a valid action for tweets")
        return value

# ==========================================
#   USED FOR SERIALIZING TWEET CREATIONS
# ------------------------------------------


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value

# ==========================================
#   USED FOR SERIALIZING RETWEET DATA
# ------------------------------------------


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent']

    def get_likes(self, obj):
        return obj.likes.count()
