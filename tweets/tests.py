# django
from django.conf.auth import get_user_model
from django.test import TestCase
# internal
from .models import Tweet

User = get_user_model()


class TweetTestCase(TestCase):
    def setup(self):
