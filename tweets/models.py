# python
import random
# django
from django.conf import settings
from django.db import models

# ======================
#   Local Variables
# ======================

User = settings.AUTH_USER_MODEL

# ======================
#   Tweets Models
# ======================


class Tweet(models.Model):
    # map to SQL data
    # id = models.AutoField(primary_key=True)
    # many users can many tweets
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
