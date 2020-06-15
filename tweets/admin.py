# django
from django.contrib import admin
# internal
from .models import Tweet

# ======================
#   Admin Class
# ======================


class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
